import copy
import json
import os
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError

from radar import (ReviewError, check_inputs, confirmed_requirements, validate_evaluation,
                   validate_requirements, call_model, EXTRACTION, DRAFT_LIMIT, evaluate)

INSTRUCTIONS = 'Compare two alternatives. Justify a recommendation.'
DRAFT = 'Option A is cheaper. Option B offers better reach.\n\nI recommend A because our budget is limited.'
ORIGINALS = [{'text': 'Compare two alternatives.', 'source': 'Compare two alternatives.'},
             {'text': 'Justify a recommendation.', 'source': 'Justify a recommendation.'}]
REQS = confirmed_requirements('\n'.join(r['text'] for r in ORIGINALS), ORIGINALS)
REPORT = {'findings': [
    {'requirement_id': 'R1', 'status': 'Met', 'explanation': 'Compares cost and reach.', 'gap': '',
     'evidence': [{'quote': 'Option A is cheaper. Option B offers better reach.', 'paragraph': 1}]},
    {'requirement_id': 'R2', 'status': 'Met', 'explanation': 'Links choice to budget.', 'gap': '',
     'evidence': [{'quote': 'I recommend A because our budget is limited.', 'paragraph': 2}]}],
    'recommendations': [], 'limitations': []}


class ContractTests(unittest.TestCase):
    def test_blank_and_oversized_inputs_are_blocked(self):
        for instructions, draft in [(' ', DRAFT), (INSTRUCTIONS, '\n'), (INSTRUCTIONS, 'x'*(DRAFT_LIMIT+1))]:
            with self.assertRaises(ReviewError): check_inputs(instructions, draft)

    def test_requirement_sources_must_exist(self):
        bad = copy.deepcopy(ORIGINALS); bad[0]['source'] = 'Invented rubric'
        with self.assertRaises(ReviewError): validate_requirements({'requirements': bad}, INSTRUCTIONS)

    def test_requirement_sources_accept_whitespace_and_preserve_original(self):
        instructions = 'Compare\u00a0two\n  alternatives. Justify a recommendation.'
        data = {'requirements': copy.deepcopy(ORIGINALS)}
        checked = validate_requirements(data, instructions)
        self.assertEqual(checked[0]['source'], 'Compare\u00a0two\n  alternatives.')
        self.assertIn(checked[0]['source'], instructions)

    def test_requirement_sources_reject_changed_wording(self):
        for source in ('Compare three alternatives.', 'Compare two options.',
                       'Compare two alternatives. Justify an invented recommendation.'):
            data = {'requirements': copy.deepcopy(ORIGINALS)}
            data['requirements'][0]['source'] = source
            with self.assertRaises(ReviewError):
                validate_requirements(data, INSTRUCTIONS)

    def test_student_changes_are_traceable_and_duplicates_blocked(self):
        reqs = confirmed_requirements('Compare two alternatives.\nDiscuss risks.', ORIGINALS)
        self.assertFalse(reqs[0]['student_added'])
        self.assertTrue(reqs[1]['student_added'])
        self.assertEqual(reqs[1]['source'], '')
        with self.assertRaises(ReviewError): confirmed_requirements('Same\nSame', ORIGINALS)

    def test_valid_evidence_is_retained(self):
        self.assertEqual(validate_evaluation(copy.deepcopy(REPORT), REQS, DRAFT), REPORT)

    def test_wrong_paragraph_or_quote_downgrades_and_removes_advice(self):
        for evidence in ([{'quote': 'Invented evidence', 'paragraph': 1}],
                         [{'quote': 'I recommend A because our budget is limited.', 'paragraph': 1}], []):
            report = copy.deepcopy(REPORT)
            report['findings'][0]['evidence'] = evidence
            report['recommendations'] = [{'label': 'Required fix', 'requirement_ids': ['R1'],
                                           'action': 'Change it', 'why': 'A reason', 'approach': 'Consider this'}]
            checked = validate_evaluation(report, REQS, DRAFT)
            self.assertEqual(checked['findings'][0]['status'], 'Needs Review')
            self.assertEqual(checked['findings'][0]['evidence'], [])
            self.assertEqual(checked['recommendations'], [])

    def test_missing_and_duplicate_findings_rejected(self):
        for findings in ([REPORT['findings'][0]], [REPORT['findings'][0]]*2):
            report = copy.deepcopy(REPORT);report['findings'] = findings
            with self.assertRaises(ReviewError): validate_evaluation(report, REQS, DRAFT)

    def test_invalid_status_and_excess_recommendations_rejected(self):
        report = copy.deepcopy(REPORT); report['findings'][0]['status'] = 'A+'
        with self.assertRaises(ReviewError): validate_evaluation(report, REQS, DRAFT)
        report = copy.deepcopy(REPORT)
        report['recommendations'] = [{'label': 'Optional enhancement', 'requirement_ids': [],
                                       'action': 'Consider risks', 'why': 'Depth', 'approach': 'Ask why'}]*4
        with self.assertRaises(ReviewError): validate_evaluation(report, REQS, DRAFT)

    def test_unknown_recommendation_id_rejected(self):
        report = copy.deepcopy(REPORT)
        report['recommendations'] = [{'label': 'Required fix', 'requirement_ids': ['R99'],
                                       'action': 'Change it', 'why': 'Reason', 'approach': 'Ask why'}]
        with self.assertRaises(ReviewError): validate_evaluation(report, REQS, DRAFT)

    @patch.dict(os.environ, {'OPENROUTER_API_KEY': ''})
    def test_missing_key_is_actionable(self):
        with self.assertRaisesRegex(ReviewError, 'not configured'): call_model('Task', {}, EXTRACTION)

    @patch.dict(os.environ, {'OPENROUTER_REVIEW_MAX_TOKENS': ''})
    @patch('radar.call_model', return_value=(copy.deepcopy(REPORT), {}))
    def test_review_budget_default_and_override(self, model):
        for setting, expected in [('', 16000), ('24000', 24000)]:
            with patch.dict(os.environ, {'OPENROUTER_REVIEW_MAX_TOKENS': setting}):
                evaluate(INSTRUCTIONS, DRAFT, REQS)
                self.assertEqual(model.call_args.kwargs['max_tokens'], expected)

    @patch('radar.call_model')
    def test_invalid_review_budget_is_blocked_before_request(self, model):
        for setting in ('abc', '0', '-1', '32001'):
            with patch.dict(os.environ, {'OPENROUTER_REVIEW_MAX_TOKENS': setting}):
                with self.assertRaisesRegex(ReviewError, 'OPENROUTER_REVIEW_MAX_TOKENS'):
                    evaluate(INSTRUCTIONS, DRAFT, REQS)
        model.assert_not_called()

    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'synthetic-test-key'})
    @patch('radar.request.urlopen')
    def test_incomplete_responses_explain_the_stop_reason(self, urlopen):
        for reason, message in [('length', 'output token limit'),
                                ('content_filter', 'content filter'),
                                ('error', 'provider stopped'),
                                (None, 'provider stopped'),
                                ('secret-provider-detail', 'provider stopped')]:
            with self.subTest(reason=reason):
                response = MagicMock()
                response.__enter__.return_value.read.return_value = json.dumps({
                    'choices': [{'finish_reason': reason,
                                 'message': {'content': 'private assignment response'}}],
                    'usage': {'prompt_tokens': 200, 'completion_tokens': 7000,
                              'completion_tokens_details': {'reasoning_tokens': 6500},
                              'private': 'private assignment response'}}).encode()
                urlopen.return_value = response
                with self.assertRaisesRegex(ReviewError, message) as ctx:
                    call_model('Task', {}, EXTRACTION)
                self.assertEqual(ctx.exception.diagnostics['requested_max_tokens'], 7000)
                self.assertEqual(ctx.exception.diagnostics['reasoning_tokens'], 6500)
                self.assertEqual(ctx.exception.diagnostics['output_tokens'], 7000)
                self.assertNotIn('private assignment response', json.dumps(ctx.exception.diagnostics))
                self.assertNotIn('secret-provider-detail', json.dumps(ctx.exception.diagnostics))
                self.assertNotIn('private assignment response', str(ctx.exception))
                self.assertNotIn('secret-provider-detail', str(ctx.exception))
                if reason != 'length':
                    self.assertNotIn('shorter', str(ctx.exception))

    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'synthetic-test-key'})
    @patch('radar.request.urlopen')
    def test_request_privacy_and_provider_errors(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({
            'choices': [{'finish_reason': 'stop', 'message': {'content': '{"requirements": []}'}}],
            'usage': {'cost': 0.001}}).encode()
        urlopen.return_value = response
        _, meta = call_model('Task', {'instructions': INSTRUCTIONS}, EXTRACTION)
        body = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual(body['provider'], {'data_collection': 'deny', 'zdr': True, 'require_parameters': True})
        self.assertEqual(meta['cost_usd'], 0.001)
        self.assertEqual(body['max_tokens'], 7000)
        call_model('Task', {}, EXTRACTION, max_tokens=16000)
        self.assertEqual(json.loads(urlopen.call_args.args[0].data)['max_tokens'], 16000)
        for exc in [HTTPError('url', 401, 'secret response', {}, None), URLError('secret response')]:
            urlopen.side_effect = exc
            with self.assertRaises(ReviewError) as ctx: call_model('Task', {}, EXTRACTION)
            self.assertNotIn('secret response', str(ctx.exception))


if __name__ == '__main__': unittest.main()
