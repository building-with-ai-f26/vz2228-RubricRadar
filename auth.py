"""Google-to-Supabase auth; create one Auth object per Streamlit session.

No cookies, local files, shared caches, or automatic background refresh. UI wiring
and clearing of coursework on account changes are handled by library_ui.py.
"""
from dataclasses import dataclass, field
import hashlib
import hmac
import secrets
import time
from uuid import UUID

from supabase_api import CloudError


def valid_id(value):
    try:
        return str(UUID(value))
    except (ValueError, TypeError, AttributeError):
        raise CloudError('The selected record is invalid. Reload and try again.') from None


@dataclass(repr=False)
class AuthSession:
    user_id: str
    access_token: str = field(repr=False)
    refresh_token: str = field(repr=False)
    expires_at: float


@dataclass(repr=False)
class GoogleChallenge:
    nonce: str = field(repr=False)
    expires_at: float

    @property
    def public_nonce(self):
        # Google receives the hash; Supabase receives the original server nonce.
        return hashlib.sha256(self.nonce.encode()).hexdigest()


class Auth:
    def __init__(self, api):
        self.api = api
        self.session = None
        self._google = None

    def google_challenge(self):
        if self._google is None or self._google.expires_at <= time.monotonic():
            self._google = GoogleChallenge(secrets.token_urlsafe(32), time.monotonic() + 300)
        return self._google.public_nonce

    def cancel_google(self):
        self._google = None

    def sign_in_google(self, credential, challenge_id):
        self.session = None
        pending, self._google = self._google, None  # One attempt, even on refusal.
        if (pending is None or pending.expires_at <= time.monotonic()
                or not isinstance(challenge_id, str) or len(challenge_id) != 64
                or not hmac.compare_digest(pending.public_nonce.encode(), challenge_id.encode())
                or not isinstance(credential, str) or not 1 <= len(credential) <= 16384):
            raise CloudError('Google sign-in expired or was invalid. Try signing in again.')
        data = self.api.send('POST', '/auth/v1/token?grant_type=id_token', body={
            'provider': 'google', 'id_token': credential, 'nonce': pending.nonce})
        return self._accept(data, require_google=True)

    def _accept(self, data, *, expected_user=None, require_google=False):
        self.session = None
        try:
            access, refresh, expires = data['access_token'], data['refresh_token'], data['expires_in']
            if (not isinstance(access, str) or not access or not isinstance(refresh, str) or not refresh
                    or type(expires) is not int or not 0 < expires <= 604800):
                raise ValueError
            # Supabase verifies the token. Do not trust decoded JWTs or client user IDs.
            user = self.api.send('GET', '/auth/v1/user', token=access)
            user_id = valid_id(user['id'])
            if not user.get('email_confirmed_at') or (expected_user and user_id != expected_user):
                raise ValueError
            if require_google and not any(isinstance(identity, dict) and identity.get('provider') == 'google'
                                          for identity in (user.get('identities') or [])):
                raise ValueError
            self.session = AuthSession(user_id, access, refresh, time.time() + expires)
            return self.session
        except (KeyError, TypeError, ValueError):
            raise CloudError('A verified account session was not returned. Try signing in again.') from None

    def verified_session(self):
        """Fail closed; verify with Auth before each storage operation, refresh near expiry."""
        current = self.session
        if current is None:
            raise CloudError('Sign in to access your saved coursework.')
        try:
            if current.expires_at <= time.time() + 60:
                data = self.api.send('POST', '/auth/v1/token?grant_type=refresh_token',
                                     body={'refresh_token': current.refresh_token})
                return self._accept(data, expected_user=current.user_id)
            user = self.api.send('GET', '/auth/v1/user', token=current.access_token)
            if valid_id(user['id']) != current.user_id or not user.get('email_confirmed_at'):
                raise CloudError('Your account session changed. Sign in again.')
            return current
        except (CloudError, KeyError, TypeError):
            self.session = None
            raise CloudError('Your session could not be verified. Sign in again.') from None

    def sign_out(self):
        self.cancel_google()
        current, self.session = self.session, None
        if current:
            self.api.send('POST', '/auth/v1/logout?scope=local', token=current.access_token)
