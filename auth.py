"""Supabase email auth foundation; create one Auth object per Streamlit session.

No cookies, local files, shared caches, or automatic background refresh. UI wiring
and clearing of coursework on account changes are handled by library_ui.py.
"""
from dataclasses import dataclass, field
import re
import time
from uuid import UUID

from supabase_api import CloudError


def valid_id(value):
    try:
        return str(UUID(value))
    except (ValueError, TypeError, AttributeError):
        raise CloudError('The selected record is invalid. Reload and try again.') from None


def email_address(value):
    if not isinstance(value, str) or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', value.strip()) or len(value) > 254:
        raise CloudError('Enter a valid email address.')
    return value.strip()


def password_value(value):
    if not isinstance(value, str) or not 12 <= len(value) <= 128:
        raise CloudError('Use a password between 12 and 128 characters.')
    return value


@dataclass(repr=False)
class AuthSession:
    user_id: str
    access_token: str = field(repr=False)
    refresh_token: str = field(repr=False)
    expires_at: float
    recovery: bool = False


class Auth:
    def __init__(self, api):
        self.api = api
        self.session = None

    def sign_up(self, email, password):
        # Do not log in automatically, even if server confirmation is misconfigured.
        self.session = None
        self.api.send('POST', '/auth/v1/signup',
                      body={'email': email_address(email), 'password': password_value(password)})
        return 'If registration is available, check your email for a confirmation code.'

    def sign_in(self, email, password):
        self.session = None
        if not isinstance(password, str) or not password or len(password) > 128:
            raise CloudError('Enter your password.')
        return self._accept(self.api.send('POST', '/auth/v1/token?grant_type=password',
                            body={'email': email_address(email), 'password': password}))

    def verify_code(self, email, code, *, recovery=False):
        self.session = None
        if not isinstance(code, str) or not re.fullmatch(r'[0-9]{6}', code):
            raise CloudError('Enter the six-digit code from your email.')
        data = self.api.send('POST', '/auth/v1/verify', body={
            'email': email_address(email), 'token': code, 'type': 'recovery' if recovery else 'email'})
        return self._accept(data, recovery=recovery)

    def request_password_reset(self, email):
        self.api.send('POST', '/auth/v1/recover', body={'email': email_address(email)})
        return 'If an account exists, check your email for a recovery code.'

    def _accept(self, data, *, recovery=False, expected_user=None):
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
            self.session = AuthSession(user_id, access, refresh, time.time() + expires, recovery)
            return self.session
        except (KeyError, TypeError, ValueError):
            raise CloudError('A verified email session was not returned. Confirm your email and sign in again.') from None

    def verified_session(self):
        """Fail closed; verify with Auth before each storage operation, refresh near expiry."""
        current = self.session
        if current is None or current.recovery:
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

    def reset_password(self, password):
        password = password_value(password)
        current = self.session
        if not current or not current.recovery or current.expires_at <= time.time():
            self.session = None
            raise CloudError('Request and verify a new recovery code first.')
        # Forget locally before either network call. Recovery never becomes a
        # normal coursework session, including on a failed password change.
        self.session = None
        try:
            self.api.send('PUT', '/auth/v1/user', token=current.access_token, body={'password': password})
        except CloudError:
            try:
                self.api.send('POST', '/auth/v1/logout?scope=local', token=current.access_token)
            except CloudError:
                pass
            raise
        try:
            self.api.send('POST', '/auth/v1/logout?scope=local', token=current.access_token)
        except CloudError:
            return 'Your password changed. Local sign-out is complete; remote sign-out could not be confirmed. Sign in again.'
        return 'Your password changed. Sign in again.'

    def sign_out(self):
        current, self.session = self.session, None
        if current:
            self.api.send('POST', '/auth/v1/logout?scope=local', token=current.access_token)
