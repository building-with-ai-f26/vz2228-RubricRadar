"""Mocked HTTP/auth/storage contracts. These do not execute Postgres RLS."""
from copy import deepcopy
import io
import json
import time
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from auth import Auth, AuthSession
from archive import Archive, make_snapshot, validate_snapshot
from supabase_api import CloudAPI, CloudConfig, CloudError, NoRedirect
from test_radar import INSTRUCTIONS, DRAFT, ORIGINALS, REQS, REPORT

A = '10000000-0000-0000-0000-000000000001'
B = '10000000-0000-0000-0000-000000000002'
P = '20000000-0000-0000-0000-000000000001'
R = '30000000-0000-0000-0000-000000000001'
T = '40000000-0000-0000-0000-000000000001'
USER = {'id': A, 'email_confirmed_at': '2026-11-17T12:00:00Z', 'identities': [{'provider': 'google'}]}
TOKEN = {'access_token': 'private-access', 'refresh_token': 'private-refresh', 'expires_in': 3600}


def snapshot():
    return make_snapshot(INSTRUCTIONS, DRAFT, ORIGINALS, REQS, REPORT)


def signed_in():
    api = MagicMock()
    auth = Auth(api)
    auth.session = AuthSession(A, TOKEN['access_token'], TOKEN['refresh_token'], time.time() + 3600)
    return auth, api


class TransportTests(unittest.TestCase):
    def test_config_refuses_secret_keys_and_non_supabase_origins(self):
        for url, key in [('http://demo.supabase.co', 'sb_publishable_test'),
                         ('https://demo.supabase.co.evil.test', 'sb_publishable_test'),
                         ('https://user:password@demo.supabase.co', 'sb_publishable_test'),
                         ('https://demo.supabase.co', 'sb_secret_private'),
                         ('https://demo.supabase.co', 'legacy-jwt-service-role')]:
            with self.subTest(url=url), self.assertRaises(CloudError):
                CloudConfig(url, key)
        self.assertNotIn('sb_publishable_test', repr(CloudConfig('https://demo.supabase.co', 'sb_publishable_test')))
        self.assertEqual(CloudConfig.from_settings({'SUPABASE_URL': 'https://demo.supabase.co/',
                         'SUPABASE_PUBLISHABLE_KEY': 'sb_publishable_test'}).url, 'https://demo.supabase.co')

    @patch('supabase_api.request.build_opener')
    def test_request_has_user_token_timeout_and_bounded_response(self, build):
        response = build.return_value.open.return_value.__enter__.return_value
        response.read.return_value = b'[]'
        api = CloudAPI(CloudConfig('https://demo.supabase.co', 'sb_publishable_test'))
        self.assertEqual(api.send('GET', '/rest/v1/rr_classes', token='private-access'), [])
        req = build.return_value.open.call_args.args[0]
        self.assertEqual(req.get_header('Authorization'), 'Bearer private-access')
        self.assertEqual(req.get_header('Apikey'), 'sb_publishable_test')
        self.assertEqual(build.return_value.open.call_args.kwargs['timeout'], 20)
        response.read.assert_called_once_with(2_000_001)
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.test'))
        self.assertTrue(any(isinstance(h, NoRedirect) for h in build.call_args.args))

    @patch('supabase_api.request.build_opener')
    def test_remote_details_are_redacted_and_requests_are_not_retried(self, build):
        api = CloudAPI(CloudConfig('https://demo.supabase.co', 'sb_publishable_test'))
        for status in (302, 400, 401, 403, 409, 422, 429, 500):
            build.return_value.open.side_effect = HTTPError('private-url', status, 'private-body', {}, io.BytesIO(b'private-body'))
            with self.assertRaises(CloudError) as caught:
                api.send('POST', '/auth/v1/token?grant_type=password', body={'password': 'private-password'})
            self.assertEqual(caught.exception.status, status)
            self.assertNotIn('private-', str(caught.exception))
        self.assertEqual(build.return_value.open.call_count, 8)
        build.return_value.open.side_effect = URLError('private-network-detail')
        with self.assertRaises(CloudError) as caught:
            api.send('GET', '/rest/v1/rr_classes')
        self.assertNotIn('private-network-detail', str(caught.exception))

    @patch('supabase_api.request.build_opener')
    def test_malformed_and_oversized_responses_are_safe(self, build):
        api = CloudAPI(CloudConfig('https://demo.supabase.co', 'sb_publishable_test'))
        for body in (b'private-non-json', b'x' * 2_000_001):
            build.return_value.open.return_value.__enter__.return_value.read.return_value = body
            with self.assertRaises(CloudError) as caught:
                api.send('GET', '/rest/v1/rr_classes')
            self.assertNotIn('private-non-json', str(caught.exception))


class AuthTests(unittest.TestCase):
    def test_sign_in_uses_server_verified_identity_and_does_not_share_sessions(self):
        api = MagicMock(); api.send.side_effect = [TOKEN, USER]
        auth = Auth(api); other = Auth(api)
        session = auth.sign_in_google('synthetic-id-token', auth.google_challenge())
        self.assertEqual(session.user_id, A)
        self.assertIsNone(other.session)
        self.assertNotIn('private-', repr(session))
        self.assertEqual(api.send.call_args.args, ('GET', '/auth/v1/user'))

    def test_failed_login_or_unconfirmed_email_clears_old_session(self):
        for response in ({**USER, 'email_confirmed_at': None}, {'id': B}):
            auth, api = signed_in(); api.send.side_effect = [TOKEN, response]
            with self.assertRaises(CloudError): auth.sign_in_google('synthetic-id-token', auth.google_challenge())
            self.assertIsNone(auth.session)
        auth, api = signed_in(); api.send.side_effect = CloudError('Refused', status=401)
        with self.assertRaises(CloudError): auth.sign_in_google('synthetic-id-token', auth.google_challenge())
        self.assertIsNone(auth.session)

    def test_google_nonce_is_hashed_for_browser_and_raw_for_supabase_once(self):
        api = MagicMock(); api.send.side_effect = [TOKEN, USER]
        auth = Auth(api); public_nonce = auth.google_challenge()
        raw_nonce = auth._google.nonce
        self.assertEqual(len(public_nonce), 64)
        self.assertNotEqual(raw_nonce, public_nonce)
        self.assertEqual(auth.google_challenge(), public_nonce)
        auth.sign_in_google('synthetic-id-token', public_nonce)
        self.assertEqual(api.send.call_args_list[0].args, ('POST', '/auth/v1/token?grant_type=id_token'))
        self.assertEqual(api.send.call_args_list[0].kwargs['body'], {
            'provider': 'google', 'id_token': 'synthetic-id-token', 'nonce': raw_nonce})
        self.assertIsNone(auth._google)
        api.send.reset_mock()
        with self.assertRaises(CloudError): auth.sign_in_google('synthetic-id-token', public_nonce)
        api.send.assert_not_called()
        self.assertIsNone(auth.session)

    def test_refresh_rotates_token_and_checks_identity(self):
        auth, api = signed_in(); auth.session.expires_at = 0
        api.send.side_effect = [{**TOKEN, 'refresh_token': 'rotated'}, USER]
        self.assertEqual(auth.verified_session().refresh_token, 'rotated')
        self.assertEqual(api.send.call_args_list[0].kwargs['body'], {'refresh_token': 'private-refresh'})
        auth.session.expires_at = 0
        api.send.side_effect = [TOKEN, {**USER, 'id': B}]
        with self.assertRaises(CloudError): auth.verified_session()
        self.assertIsNone(auth.session)

    def test_verification_failure_or_identity_change_fails_closed(self):
        for response in ({**USER, 'id': B}, {'id': A}, CloudError('Network failure')):
            auth, api = signed_in()
            if isinstance(response, Exception): api.send.side_effect = response
            else: api.send.return_value = response
            with self.assertRaises(CloudError): auth.verified_session()
            self.assertIsNone(auth.session)

    def test_google_expired_cross_session_cancelled_and_invalid_attempts_fail_closed(self):
        for invalid in ('expired', 'other-session', 'cancelled', 'empty', 'oversized', 'non-string'):
            auth, api = signed_in(); challenge = auth.google_challenge()
            credential = 'synthetic-id-token'
            if invalid == 'expired': auth._google.expires_at = 0
            elif invalid == 'other-session': challenge = Auth(api).google_challenge()
            elif invalid == 'cancelled': auth.cancel_google()
            elif invalid == 'empty': credential = ''
            elif invalid == 'oversized': credential = 'x' * 16385
            else: credential = {'credential': 'invalid'}
            with self.subTest(invalid=invalid), self.assertRaises(CloudError):
                auth.sign_in_google(credential, challenge)
            api.send.assert_not_called()
            self.assertIsNone(auth.session); self.assertIsNone(auth._google)

    def test_google_provider_and_verified_email_required(self):
        for user in ({**USER, 'identities': [{'provider': 'email'}]}, {**USER, 'email_confirmed_at': None}):
            auth, api = signed_in(); api.send.side_effect = [TOKEN, user]
            with self.assertRaises(CloudError):
                auth.sign_in_google('synthetic-id-token', auth.google_challenge())
            self.assertIsNone(auth.session)

    def test_google_refused_token_is_not_retried_and_challenge_is_consumed(self):
        auth, api = signed_in(); api.send.side_effect = CloudError('Refused', status=401)
        challenge = auth.google_challenge()
        with self.assertRaises(CloudError): auth.sign_in_google('synthetic-id-token', challenge)
        self.assertEqual(api.send.call_count, 1)
        self.assertIsNone(auth._google); self.assertIsNone(auth.session)
        self.assertNotEqual(auth.google_challenge(), challenge)

    def test_logout_clears_local_state_even_when_network_fails(self):
        auth, api = signed_in(); api.send.side_effect = CloudError('Network failure')
        with self.assertRaises(CloudError): auth.sign_out()
        self.assertIsNone(auth.session)

    def test_malformed_google_session_response_never_creates_session(self):
        for data in (None, {}, {**TOKEN, 'expires_in': True}, {**TOKEN, 'access_token': ''}):
            auth, api = signed_in(); api.send.return_value = data
            with self.subTest(data=data), self.assertRaises(CloudError):
                auth.sign_in_google('synthetic-id-token', auth.google_challenge())
            self.assertIsNone(auth.session)


class ArchiveTests(unittest.TestCase):
    def test_guest_cannot_read_or_save_and_makes_no_requests(self):
        api = MagicMock(); store = Archive(Auth(api))
        for action in (store.list_classes, lambda: store.create_class('Synthetic class'),
                       lambda: store.save_review(P, T, snapshot())):
            with self.assertRaises(CloudError): action()
        api.send.assert_not_called()

    def test_snapshot_is_independent_and_drops_unknown_metadata(self):
        original = deepcopy(REPORT)
        saved = make_snapshot(INSTRUCTIONS, DRAFT, ORIGINALS, REQS, original,
                              {'cost_usd': 0.01, 'raw_response': 'private'}, {'access_token': 'private'})
        self.assertEqual(saved['extract_meta']['cost_usd'], 0.01)
        self.assertNotIn('raw_response', saved['extract_meta'])
        self.assertNotIn('access_token', saved['review_meta'])
        original['findings'].clear()
        self.assertEqual(len(saved['result']['findings']), 2)

    def test_snapshot_refuses_invented_evidence_changed_requirements_and_extra_fields(self):
        variants = []
        bad = snapshot(); bad['result']['findings'][0]['evidence'][0]['quote'] = 'Invented'; variants.append(bad)
        bad = snapshot(); bad['confirmed'][0]['source'] = 'Invented'; variants.append(bad)
        bad = snapshot(); bad['api_key'] = 'private'; variants.append(bad)
        bad = snapshot(); bad['review_meta']['cost_usd'] = float('inf'); variants.append(bad)
        for bad in variants:
            with self.assertRaises(CloudError): validate_snapshot(bad)

    def test_archive_pagination_and_current_record_reads(self):
        auth, api = signed_in(); store = Archive(auth)
        row = {'id': P, 'owner_id': A}
        for action in (lambda: store.list_classes(offset=100),
                       lambda: store.list_projects(P, offset=100),
                       lambda: store.list_reviews(P, offset=100)):
            api.send.side_effect = [USER, [row]]
            action()
            query = parse_qs(urlsplit(api.send.call_args.args[1]).query)
            self.assertEqual(query['offset'], ['100'])
            self.assertEqual(query['order'], ['created_at.desc,id.desc'])
        for action in (lambda: store.get_class(P), lambda: store.get_project(P)):
            api.send.side_effect = [USER, [row]]
            self.assertEqual(action()['id'], P)

    def test_owner_is_verified_not_supplied_by_form(self):
        auth, api = signed_in(); api.send.side_effect = [USER, [{'id': P, 'owner_id': A}]]
        Archive(auth).create_class('Synthetic class')
        data = api.send.call_args.kwargs
        self.assertEqual(data['body']['owner_id'], A)
        self.assertEqual(data['token'], 'private-access')
        self.assertIn('owner_id=eq.', api.send.call_args.args[1])

    def test_response_with_other_owner_is_not_returned(self):
        auth, api = signed_in(); api.send.side_effect = [USER, [{'id': P, 'owner_id': B}]]
        with self.assertRaises(CloudError): Archive(auth).list_classes()

    def test_empty_update_or_delete_is_not_success(self):
        auth, api = signed_in(); store = Archive(auth)
        for action in (lambda: store.save_project(P, 'Synthetic', INSTRUCTIONS, project_id=R),
                       lambda: store.delete('projects', P, confirmed=True)):
            api.send.side_effect = [USER, []]
            with self.assertRaises(CloudError): action()

    def test_duplicate_save_fetches_identical_snapshot_without_overwrite(self):
        auth, api = signed_in(); saved = snapshot()
        row = {'id': R, 'owner_id': A, 'project_id': P, 'snapshot': saved}
        api.send.side_effect = [USER, [], [row]]
        self.assertEqual(Archive(auth).save_review(P, T, saved)['id'], R)
        calls = api.send.call_args_list
        self.assertEqual([c.args[0] for c in calls], ['GET', 'POST', 'GET'])
        self.assertIn('ignore-duplicates', calls[1].kwargs['prefer'])
        self.assertEqual(parse_qs(urlsplit(calls[1].args[1]).query)['on_conflict'], ['owner_id,save_token'])
        api.send.side_effect = [USER, [], [{**row, 'project_id': B}]]
        with self.assertRaises(CloudError): Archive(auth).save_review(P, T, saved)

    def test_load_validates_snapshot_and_never_calls_model(self):
        auth, api = signed_in(); row = {'id': R, 'owner_id': A, 'snapshot': snapshot()}
        api.send.side_effect = [USER, [row]]
        with patch('radar.call_model') as model:
            self.assertEqual(Archive(auth).load_review(R)['snapshot'], snapshot())
        model.assert_not_called()
        row['snapshot']['result']['findings'] = []
        api.send.side_effect = [USER, [row]]
        with self.assertRaises(CloudError): Archive(auth).load_review(R)

    def test_storage_failure_does_not_mutate_working_snapshot(self):
        auth, api = signed_in(); working = snapshot(); before = deepcopy(working)
        api.send.side_effect = [USER, CloudError('Network failure')]
        with self.assertRaises(CloudError): Archive(auth).save_review(P, T, working)
        self.assertEqual(before, working)

    def test_deletion_requires_confirmation_and_server_counts(self):
        auth, api = signed_in(); store = Archive(auth)
        with self.assertRaises(CloudError): store.delete('classes', P)
        api.send.assert_not_called()
        counts = {'classes': 1, 'projects': 2, 'reviews': 3}
        api.send.side_effect = [USER, [{'id': P, 'owner_id': A}], counts]
        self.assertEqual(store.deletion_counts('classes', P), counts)
        self.assertEqual(api.send.call_args.args, ('POST', '/rest/v1/rpc/rr_deletion_counts'))

    def test_filter_injection_is_rejected_before_request(self):
        auth, api = signed_in()
        with self.assertRaises(CloudError): Archive(auth).list_projects(P + '&owner_id=eq.' + B)
        api.send.assert_not_called()


if __name__ == '__main__':
    unittest.main()
