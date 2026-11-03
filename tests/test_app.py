"""Exercise the real UI with synthetic provider responses, never real API calls."""
import copy
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from test_radar import INSTRUCTIONS, DRAFT, ORIGINALS, REPORT
from radar import ReviewError

META = {'model': 'synthetic-test', 'seconds': 0, 'cost_usd': 0}


def button(app, label):
    return next(b for b in app.button if b.label == label)


class AppTests(unittest.TestCase):
    def fill(self):
        app = AppTest.from_file('../app.py').run()
        app.text_area(key='instructions').input(INSTRUCTIONS)
        app.text_area(key='draft').input(DRAFT)
        app.checkbox(key='consent').check().run()
        return app

    @patch('radar.extract', return_value=(ORIGINALS, META))
    @patch('radar.evaluate', return_value=(copy.deepcopy(REPORT), META))
    def test_review_edit_invalidation_and_clear(self, evaluate, extract):
        app = self.fill()
        button(app, '1. Extract requirements').click().run()
        button(app, 'Confirm requirements').click().run()
        button(app, '3. Review my draft').click().run()
        self.assertFalse(app.exception)
        self.assertIn('result', app.session_state)
        app.text_area(key='requirement_text').input('Discuss risks.').run()
        self.assertNotIn('confirmed', app.session_state)
        self.assertNotIn('result', app.session_state)
        app.text_area(key='draft').input('New draft').run()
        self.assertNotIn('originals', app.session_state)
        button(app, 'Clear this session').click().run()
        self.assertEqual(app.text_area(key='draft').value, '')
        self.assertFalse(app.exception)

    @patch('radar.extract', return_value=(ORIGINALS, META))
    @patch('radar.evaluate', side_effect=ReviewError('Token limit.', diagnostics={
        'requested_max_tokens': 16000, 'output_tokens': 16000, 'reasoning_tokens': None}))
    def test_review_failure_displays_diagnostics_and_preserves_inputs(self, evaluate, extract):
        app = self.fill()
        button(app, '1. Extract requirements').click().run()
        button(app, 'Confirm requirements').click().run()
        button(app, '3. Review my draft').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.text_area(key='draft').value, DRAFT)
        self.assertIn('confirmed', app.session_state)
        self.assertNotIn('result', app.session_state)
        self.assertTrue(app.json)
        self.assertIn('16000', app.json[0].value)

    @patch('radar.extract', side_effect=ReviewError('Provider unavailable.'))
    def test_failure_preserves_inputs(self, extract):
        app = self.fill()
        button(app, '1. Extract requirements').click().run()
        self.assertEqual(app.text_area(key='draft').value, DRAFT)
        self.assertTrue(app.error)
        self.assertNotIn('originals', app.session_state)
        self.assertFalse(app.exception)


if __name__ == '__main__': unittest.main()
