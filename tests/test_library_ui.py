"""Exercise actual Streamlit navigation using synthetic in-memory test doubles."""
from copy import deepcopy
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from test_app import button, META
from test_radar import INSTRUCTIONS, DRAFT, ORIGINALS, REPORT
from test_cloud import signed_in, USER, A, B, P, R, snapshot
from sample_library import CLASS_ID, PROJECT_ID
from supabase_api import CloudError


class FakeArchive:
    def __init__(self):
        self.classes = {CLASS_ID: dict(id=CLASS_ID, name='Synthetic class', professor='', semester='')}
        self.projects = {P: dict(id=P, class_id=CLASS_ID, name='Synthetic project', instructions=INSTRUCTIONS)}
        self.reviews = {}; self.writes = []; self.fail_save = False; self.changed_counts = False

    def list_classes(self, offset=0): return list(self.classes.values())[offset:offset+100]
    def get_class(self, record_id): return deepcopy(self.classes[record_id])
    def list_projects(self, class_id, offset=0): return [deepcopy(r) for r in self.projects.values() if r['class_id'] == class_id][offset:offset+100]
    def get_project(self, record_id): return deepcopy(self.projects[record_id])
    def list_reviews(self, project_id, offset=0): return [deepcopy(r) for r in self.reviews.values() if r['project_id'] == project_id][offset:offset+100]
    def load_review(self, record_id): return deepcopy(self.reviews[record_id])
    def create_class(self, name, professor='', semester=''):
        self.writes.append('create_class'); self.classes[B] = dict(id=B, name=name, professor=professor, semester=semester)
        return self.get_class(B)
    def save_project(self, class_id, name, instructions, project_id=None):
        self.writes.append('save_project'); project_id = project_id or B
        self.projects[project_id] = dict(id=project_id, class_id=class_id, name=name, instructions=instructions)
        return self.get_project(project_id)
    def save_review(self, project_id, token, value):
        if self.fail_save: raise CloudError('Synthetic storage unavailable.')
        self.writes.append(('save_review', token))
        self.reviews[R] = dict(id=R, project_id=project_id, created_at='Synthetic date', snapshot=deepcopy(value))
        return self.load_review(R)
    def deletion_counts(self, kind, record_id):
        return {'classes': int(kind == 'classes'), 'projects': int(kind != 'reviews'), 'reviews': int(bool(self.reviews)) + int(self.changed_counts)}
    def delete(self, kind, record_id, confirmed=False):
        assert confirmed
        self.writes.append(('delete', kind, record_id))
        if kind == 'reviews': return self.reviews.pop(record_id)
        if kind == 'projects': return self.projects.pop(record_id)
        return self.classes.pop(record_id)


class LibraryUITests(unittest.TestCase):
    def setUp(self):
        # Disable actual cloud configuration irrespective of a developer's .env.
        self.config_patch = patch('library_ui.cloud_config', return_value=None)
        self.config_patch.start(); self.addCleanup(self.config_patch.stop)
        # AppTest cannot drive Google's browser popup; test that protocol in Node.
        self.google_patch = patch('library_ui.google_button', return_value=None)
        self.google_patch.start(); self.addCleanup(self.google_patch.stop)

    def app(self):
        return AppTest.from_file('../app.py').run()

    def private_app(self, archive, screen='work'):
        self.config_patch.stop()
        configured = patch('library_ui.cloud_config', return_value=object()); configured.start(); self.addCleanup(configured.stop)
        storage = patch('library_ui.store', return_value=archive); storage.start(); self.addCleanup(storage.stop)
        auth, api = signed_in(); api.send.return_value = USER
        app = AppTest.from_file('../app.py')
        app.session_state['rr_auth'] = auth; app.session_state['rr_owner'] = A
        app.session_state['rr_route'] = {'screen': screen, **({'project_id': P} if screen in ('project', 'work') else {})}
        return app.run()

    def complete_review(self, app):
        app.text_area(key='draft').input(DRAFT)
        app.checkbox(key='consent').check().run()
        button(app, 'Extract requirements').click().run()
        button(app, 'Confirm & review my draft').click().run()
        self.assertFalse(app.exception)

    @patch('supabase_api.CloudAPI.send')
    @patch('radar.call_model')
    def test_sample_browsing_is_read_only_and_makes_no_cloud_or_model_calls(self, model, cloud):
        app = self.app(); button(app, 'Explore sample library').click().run()
        button(app, 'Open class').click().run()
        self.assertTrue(button(app, 'Create project').disabled)
        button(app, 'Open project').click().run()
        self.assertTrue(button(app, 'New review').disabled)
        self.assertEqual(app.selectbox[0].options, ['Market entry · sample project · Draft 1'])
        self.assertFalse(app.text_area)
        app.selectbox[0].select_index(0).run()
        button(app, 'Open saved review').click().run()
        self.assertTrue(button(app, 'Check a revised draft').disabled)
        self.assertTrue(button(app, 'Delete review').disabled)
        self.assertFalse(app.exception)
        cloud.assert_not_called(); model.assert_not_called()

    @patch('supabase_api.CloudAPI.send')
    def test_unconfigured_sign_in_is_disabled_guest_remains_available(self, cloud):
        app = self.app(); button(app, 'Open my library').click().run()
        self.assertTrue(next(b for b in app.button if b.label == 'Continue with Google').disabled)
        button(app, 'Continue as guest').click().run()
        self.assertIn('draft', app.session_state)
        cloud.assert_not_called(); self.assertFalse(app.exception)

    def google_login_app(self):
        archive = FakeArchive(); app = self.private_app(archive, screen='classes')
        button(app, 'Sign out').click().run()
        self.google_id = patch('library_ui.google_client_id', return_value='synthetic.apps.googleusercontent.com')
        self.google_id.start(); self.addCleanup(self.google_id.stop)
        button(app, 'Open my library').click().run()
        return app

    def test_google_sign_in_opens_library_and_clears_old_work_and_credentials(self):
        app = self.google_login_app()
        auth, api = signed_in()
        from test_cloud import TOKEN
        auth.session = None
        app.session_state['instructions'] = 'Old synthetic work'
        api.send.side_effect = lambda method, path, **kwargs: TOKEN if 'token?' in path else USER
        def response(client_id, nonce): return {'credential': 'synthetic-id-token', 'challenge_id': nonce}
        with patch('library_ui.Auth', return_value=auth), patch('library_ui.google_button', side_effect=response):
            app.session_state['rr_auth'] = auth
            app.run()
        self.assertEqual(app.session_state['rr_route']['screen'], 'classes')
        self.assertEqual(app.session_state['rr_owner'], A)
        for key in ('instructions', 'draft', 'auth_password', 'auth_email'):
            self.assertNotIn(key, app.session_state)
        self.assertFalse(app.exception)

    @patch('supabase_api.CloudAPI.send')
    def test_cancelled_google_login_has_no_identity_or_network_call(self, cloud):
        app = self.google_login_app()
        with patch('library_ui.google_button', return_value=None): app.run()
        self.assertNotIn('rr_owner', app.session_state)
        self.assertEqual(app.session_state['rr_route']['screen'], 'login')
        self.assertEqual(len(app.text_input), 0)
        self.assertEqual(len(app.selectbox), 0)
        button(app, 'Continue as guest').click().run()
        self.assertNotIn('rr_auth', app.session_state)
        self.assertIn('draft', app.session_state)
        cloud.assert_not_called(); self.assertFalse(app.exception)

    @patch('supabase_api.CloudAPI.send')
    def test_google_load_failure_shows_safe_retry_and_no_private_session(self, cloud):
        app = self.google_login_app()
        with patch('library_ui.google_button', return_value={'error': 'unavailable'}): app.run()
        self.assertTrue(app.error)
        self.assertNotIn('rr_owner', app.session_state)
        with patch('library_ui.google_button', return_value=None):
            button(app, 'Try Google sign-in again').click().run()
        self.assertFalse(app.error)
        cloud.assert_not_called(); self.assertFalse(app.exception)

    def test_unsaved_navigation_can_keep_or_discard_inputs(self):
        app = self.app(); button(app, 'Continue as guest').click().run()
        app.text_area(key='draft').input('Synthetic unsaved draft').run()
        button(app, 'Home').click().run()
        self.assertEqual(app.text_area(key='draft').value, 'Synthetic unsaved draft')
        button(app, 'Keep working').click().run()
        self.assertEqual(app.text_area(key='draft').value, 'Synthetic unsaved draft')
        button(app, 'Home').click().run(); button(app, 'Discard and continue').click().run()
        button(app, 'Continue as guest').click().run()
        self.assertEqual(app.text_area(key='draft').value, '')
        self.assertFalse(app.exception)

    def test_create_class_and_project_are_explicit_saves(self):
        archive = FakeArchive(); app = self.private_app(archive, screen='classes')
        self.assertEqual(archive.writes, [])
        app.text_input(key='form_class_name').input('New synthetic class')
        button(app, 'Create class').click().run()
        self.assertEqual(archive.writes, ['create_class'])
        app.text_input(key='form_project_name').input('New synthetic project')
        app.text_area(key='form_project_instructions').input(INSTRUCTIONS)
        button(app, 'Create project').click().run()
        button(app, 'New review').click().run()
        self.assertEqual(app.text_area(key='instructions').value, INSTRUCTIONS)
        self.assertEqual(archive.writes, ['create_class', 'save_project'])
        self.assertFalse(app.exception)

    @patch('radar.extract', return_value=(ORIGINALS, META))
    @patch('radar.evaluate', return_value=(deepcopy(REPORT), META))
    def test_review_save_is_explicit_idempotent_and_edits_invalidate_it(self, evaluate, extract):
        archive = FakeArchive(); app = self.private_app(archive)
        self.complete_review(app)
        self.assertEqual(archive.writes, [])
        button(app, 'Save review').click().run()
        self.assertEqual(len(archive.writes), 1)
        self.assertTrue(button(app, 'Save review').disabled)
        saved = deepcopy(archive.reviews[R])
        app.text_area(key='draft').input('Changed synthetic draft').run()
        self.assertTrue(button(app, 'Save review').disabled)
        self.assertNotIn('rr_save_token', app.session_state)
        self.assertEqual(saved, archive.reviews[R])
        button(app, 'Back to project').click().run()
        button(app, 'Discard and continue').click().run()
        self.assertEqual(app.selectbox[0].options, ['Synthetic project · Draft 1'])
        app.selectbox[0].select_index(0).run()
        button(app, 'Open saved review').click().run()
        self.assertEqual(app.session_state['rr_route']['review_id'], R)
        evaluate.assert_called_once()
        extract.assert_called_once()
        self.assertFalse(app.exception)

    @patch('radar.extract', return_value=(ORIGINALS, META))
    @patch('radar.evaluate', return_value=(deepcopy(REPORT), META))
    def test_storage_failure_preserves_feedback_and_retry_token(self, evaluate, extract):
        archive = FakeArchive(); app = self.private_app(archive); self.complete_review(app)
        token = app.session_state['rr_save_token']; archive.fail_save = True
        button(app, 'Save review').click().run()
        self.assertEqual(app.session_state['rr_save_token'], token)
        self.assertIn('result', app.session_state)
        self.assertEqual(app.text_area(key='draft').value, DRAFT)
        self.assertTrue(app.error); self.assertFalse(app.exception)
        archive.fail_save = False
        button(app, 'Save review').click().run()
        self.assertEqual(archive.writes[0], ('save_review', token))

    @patch('radar.call_model')
    def test_open_and_revise_saved_review_requires_fresh_consent_and_extraction(self, model):
        archive = FakeArchive(); archive.reviews[R] = dict(id=R, project_id=P, created_at='Synthetic date', snapshot=snapshot())
        archive.reviews[B] = dict(id=B, project_id=P, created_at='Later synthetic date', snapshot=snapshot())
        app = self.private_app(archive, screen='project')
        self.assertEqual(app.selectbox[0].options, ['Synthetic project · Draft 1', 'Synthetic project · Draft 2'])
        app.selectbox[0].select_index(1).run()
        button(app, 'Open saved review').click().run()
        self.assertEqual(app.session_state['rr_route']['screen'], 'saved')
        self.assertEqual(app.session_state['rr_route']['review_id'], B)
        self.assertIn('Synthetic project · Draft 2', [item.value for item in app.text])
        button(app, 'Check a revised draft').click().run()
        self.assertEqual(app.text_area(key='draft').value, DRAFT)
        self.assertFalse(app.checkbox(key='consent').value)
        self.assertNotIn('result', app.session_state); self.assertNotIn('originals', app.session_state)
        model.assert_not_called(); self.assertFalse(app.exception)

    def test_logout_clears_work_and_forms_even_when_remote_logout_fails(self):
        archive = FakeArchive(); app = self.private_app(archive)
        app.text_area(key='draft').input('Synthetic private draft').run()
        app.session_state['rr_auth'].api.send.side_effect = CloudError('Network failure')
        button(app, 'Sign out').click().run()
        self.assertNotIn('draft', app.session_state); self.assertNotIn('rr_auth', app.session_state)
        self.assertNotIn('rr_owner', app.session_state); self.assertNotIn('rr_pending', app.session_state)
        self.assertEqual(app.session_state['rr_route']['screen'], 'home')
        self.assertFalse(app.exception)

    def test_identity_change_clears_private_state_before_render(self):
        archive = FakeArchive(); app = self.private_app(archive)
        app.text_area(key='draft').input('Synthetic private draft').run()
        app.session_state['rr_auth'].api.send.return_value = {**USER, 'id': B}
        app.run()
        self.assertNotIn('draft', app.session_state)
        self.assertEqual(app.session_state['rr_route']['screen'], 'login')
        self.assertFalse(app.exception)

    def test_delete_cancellation_and_changed_counts_require_reconfirmation(self):
        archive = FakeArchive(); app = self.private_app(archive, screen='project')
        button(app, 'Delete project').click().run(); button(app, 'Cancel deletion').click().run()
        self.assertEqual(archive.writes, [])
        button(app, 'Delete project').click().run(); archive.changed_counts = True
        button(app, 'Confirm deletion').click().run()
        self.assertEqual(archive.writes, [])
        button(app, 'Confirm deletion').click().run()
        self.assertEqual(archive.writes, [('delete', 'projects', P)])
        self.assertFalse(app.exception)

    def test_guest_entry_from_account_clears_identity(self):
        archive = FakeArchive(); app = self.private_app(archive)
        button(app, 'Home').click().run(); button(app, 'Continue as guest').click().run()
        self.assertNotIn('rr_auth', app.session_state); self.assertNotIn('rr_owner', app.session_state)
        self.assertTrue(app.session_state['rr_route']['guest'])
        self.assertEqual(archive.writes, [])


if __name__ == '__main__': unittest.main()
