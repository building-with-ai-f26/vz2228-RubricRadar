"""Small Supabase HTTP transport. No auth state, logging, redirects or retries."""
from dataclasses import dataclass, field
import json
import os
import re
import ssl
from urllib import error, request

import certifi


class CloudError(Exception):
    """Fixed, student-safe message; never includes a remote body or credential."""

    def __init__(self, message, *, status=None):
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class CloudConfig:
    url: str
    publishable_key: str = field(repr=False)

    def __post_init__(self):
        # Only hosted Supabase origins for this first version. No custom proxy URLs.
        if not re.fullmatch(r'https://[a-z0-9-]+\.supabase\.co', self.url):
            raise CloudError('Configure a hosted SUPABASE_URL (https://<project>.supabase.co).')
        if not re.fullmatch(r'sb_publishable_[A-Za-z0-9_-]+', self.publishable_key):
            raise CloudError('Configure SUPABASE_PUBLISHABLE_KEY with a publishable key, never a secret/service-role key.')

    @classmethod
    def from_settings(cls, settings=None):
        """Accept environment or a flat st.secrets mapping; do not read .env here."""
        settings = os.environ if settings is None else settings
        return cls(settings.get('SUPABASE_URL', '').rstrip('/'),
                   settings.get('SUPABASE_PUBLISHABLE_KEY', ''))


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward a password, key or user bearer to a redirect destination.
        return None


class CloudAPI:
    def __init__(self, config):
        self.config = config

    def send(self, method, path, *, token=None, body=None, prefer=None):
        if not path.startswith(('/auth/v1/', '/rest/v1/')) or '\n' in path:
            raise CloudError('Unsupported cloud operation.')
        headers = {'apikey': self.config.publishable_key, 'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        if prefer:
            headers['Prefer'] = prefer
        try:
            payload = None if body is None else json.dumps(body, allow_nan=False).encode()
            req = request.Request(self.config.url + path, data=payload, method=method, headers=headers)
            opener = request.build_opener(NoRedirect(), request.HTTPSHandler(
                context=ssl.create_default_context(cafile=certifi.where())))
            with opener.open(req, timeout=20) as response:
                raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise CloudError('The cloud response was too large. Narrow the selection and retry.')
            return json.loads(raw) if raw else None
        except error.HTTPError as exc:
            status = exc.code
            exc.close()
            messages = {400: 'The cloud request was refused. Check your details and try again.',
                        401: 'Sign-in expired or credentials were refused. Sign in again.',
                        403: 'Access to this action was refused.',
                        409: 'This save conflicts with an existing record. Reload and retry.',
                        422: 'Those details could not be accepted. Check them and retry.',
                        429: 'Too many requests. Wait before trying again.'}
            raise CloudError(messages.get(status, 'The cloud service could not complete this action.'),
                             status=status) from None
        except (error.URLError, TimeoutError, OSError):
            raise CloudError('The cloud service could not connect. Your working inputs are preserved.') from None
        except (ValueError, TypeError):
            raise CloudError('The cloud service returned an unreadable response.') from None
