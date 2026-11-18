"""Minimal Google Identity Services button. No Python/JS packages added."""
from pathlib import Path
import re

import streamlit.components.v1 as components
from supabase_api import CloudError

_button = components.declare_component('rr_google_signin', path=str(Path(__file__).parent / 'google_signin'))


def google_client_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,200}\.apps\.googleusercontent\.com', value):
        raise CloudError('Google sign-in is not configured yet. Continue as guest or explore the sample.')
    return value


def google_button(client_id, nonce):
    return _button(client_id=google_client_id(client_id), nonce=nonce,
                   key='auth_google_' + nonce, default=None)
