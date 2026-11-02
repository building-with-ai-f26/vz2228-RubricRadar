import copy
import json
import os
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError

from radar import (ReviewError, check_inputs, confirmed_requirements, validate_evaluation,
                   validate_requirements, call_model, EXTRACTION, DRAFT_LIMIT)

INSTRUCTIONS = 'Compare two alternatives. Justify a recommendation.'
DRAFT = 'Option A is cheaper. Option B offers better reach.\n\nI recommend A because our budget is limited.'
ORIGINALS = [{'text': 'Compare two alternatives.', 'source': 'Compare two alternatives.', 'ambiguity': ''},
             {'text': 'Justify a recommendation.', 'source': 'Justify a recommendation.', 'ambiguity': ''}]
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
        for exc in [HTTPError('url', 401, 'secret response', {}, None), URLError('secret response')]:
            urlopen.side_effect = exc
            with self.assertRaises(ReviewError) as ctx: call_model('Task', {}, EXTRACTION)
            self.assertNotIn('secret response', str(ctx.exception))


if __name__ == '__main__': unittest.main()
