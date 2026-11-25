"""Private archive API; UI integration is gated until database verification.

Database RLS is the security boundary. Owner filters are defense in depth, not
proof of isolation. No service-role client, coursework logging or guest writes.
"""
from copy import deepcopy
import math
from urllib.parse import urlencode

from jsonschema import validate, ValidationError

from auth import valid_id
from radar import (check_inputs, confirmed_requirements, validate_requirements,
                   validate_evaluation, ReviewError, EVALUATION, obj, arr)
from supabase_api import CloudError

META = obj({
    'model': {'type': ['string', 'null'], 'maxLength': 200},
    'prompt_version': {'type': ['string', 'null'], 'maxLength': 50},
    'seconds': {'type': ['number', 'null'], 'minimum': 0},
    'input_tokens': {'type': ['integer', 'null'], 'minimum': 0},
    'output_tokens': {'type': ['integer', 'null'], 'minimum': 0},
    'cost_usd': {'type': ['number', 'null'], 'minimum': 0},
})
SNAPSHOT = obj({
    'schema_version': {'const': 1},
    'instructions': {'type': 'string', 'minLength': 1, 'maxLength': 12000},
    'draft': {'type': 'string', 'minLength': 1, 'maxLength': 30000},
    'originals': {**arr(obj({'text': {'type': 'string', 'minLength': 1, 'maxLength': 4000},
                            'source': {'type': 'string', 'minLength': 1, 'maxLength': 4000}})), 'minItems': 1},
    'confirmed': {**arr(obj({'id': {'type': 'string'}, 'text': {'type': 'string', 'minLength': 1, 'maxLength': 2000},
                            'source': {'type': 'string', 'maxLength': 4000},
                            'student_added': {'type': 'boolean'}})), 'minItems': 1},
    'result': EVALUATION,
    'extract_meta': META,
    'review_meta': META,
})


def metadata(value):
    """Only operational fields; never persist arbitrary provider diagnostics."""
    value = value if isinstance(value, dict) else {}
    selected = {key: value.get(key) for key in META['properties']}
    for key, item in selected.items():
        if isinstance(item, float) and not math.isfinite(item):
            selected[key] = None
    return selected


def validate_snapshot(value):
    try:
        validate(value, SNAPSHOT)
        check_inputs(value['instructions'], value['draft'])
        originals = validate_requirements({'requirements': deepcopy(value['originals'])}, value['instructions'])
        confirmed = confirmed_requirements('\n'.join(r['text'] for r in value['confirmed']), originals)
        if originals != value['originals'] or confirmed != value['confirmed']:
            raise ValueError
        checked = validate_evaluation(deepcopy(value['result']), confirmed, value['draft'])
        if checked != value['result']:
            raise ValueError  # Do not silently repair an archived review.
        for meta in (value['extract_meta'], value['review_meta']):
            if any(isinstance(x, float) and not math.isfinite(x) for x in meta.values()):
                raise ValueError
        return deepcopy(value)
    except (ValidationError, ReviewError, KeyError, TypeError, ValueError):
        raise CloudError('This review snapshot is incomplete or invalid. Run a fresh review before saving.') from None


def make_snapshot(instructions, draft, originals, confirmed, result, extract_meta=None, review_meta=None):
    return validate_snapshot(dict(schema_version=1, instructions=instructions, draft=draft,
                                  originals=originals, confirmed=confirmed, result=result,
                                  extract_meta=metadata(extract_meta), review_meta=metadata(review_meta)))


def short_text(value, label, *, optional=False):
    if not isinstance(value, str) or len(value.strip()) > 200 or (not optional and not value.strip()):
        raise CloudError(f'{label} must be {"at most" if optional else "1–"}200 characters.')
    return value.strip()


class Archive:
    TABLES = {'classes': 'rr_classes', 'projects': 'rr_projects', 'reviews': 'rr_reviews'}

    def __init__(self, auth):
        self.auth = auth

    def _rows(self, session, kind, method='GET', *, filters=None, body=None, prefer=None, extra=None):
        query = {'owner_id': 'eq.' + session.user_id, **(filters or {}), **(extra or {})}
        rows = self.auth.api.send(method, '/rest/v1/' + self.TABLES[kind] + '?' + urlencode(query),
                                  token=session.access_token, body=body, prefer=prefer)
        if not isinstance(rows, list) or any(not isinstance(r, dict) or r.get('owner_id') != session.user_id for r in rows):
            raise CloudError('The archive returned an invalid response. Reload and try again.')
        return rows

    def _one(self, rows):
        if len(rows) != 1:
            raise CloudError('The selected record was not available. Reload and try again.')
        return rows[0]

    def _page(self, offset):
        if type(offset) is not int or offset < 0:
            raise CloudError('Invalid archive page.')
        return {'order': 'created_at.desc,id.desc', 'limit': '100', 'offset': str(offset)}

    def get_class(self, class_id):
        session = self.auth.verified_session()
        return self._one(self._rows(session, 'classes', filters={'id': 'eq.' + valid_id(class_id)}, extra={'select': '*'}))

    def get_project(self, project_id):
        session = self.auth.verified_session()
        return self._one(self._rows(session, 'projects', filters={'id': 'eq.' + valid_id(project_id)}, extra={'select': '*'}))

    def list_classes(self, offset=0):
        session = self.auth.verified_session()
        return self._rows(session, 'classes', extra={'select': '*', **self._page(offset)})

    def create_class(self, name, professor='', semester=''):
        body = dict(name=short_text(name, 'Class name'), professor=short_text(professor, 'Professor', optional=True),
                    semester=short_text(semester, 'Semester', optional=True))
        session = self.auth.verified_session()
        return self._one(self._rows(session, 'classes', 'POST', body={**body, 'owner_id': session.user_id},
                                    prefer='return=representation'))

    def list_projects(self, class_id, offset=0):
        class_id = valid_id(class_id)
        session = self.auth.verified_session()
        return self._rows(session, 'projects', filters={'class_id': 'eq.' + class_id},
                          extra={'select': '*', **self._page(offset)})

    def save_project(self, class_id, name, instructions, *, project_id=None):
        class_id = valid_id(class_id)
        name = short_text(name, 'Project name')
        if not isinstance(instructions, str) or not instructions.strip() or len(instructions) > 12000:
            raise CloudError('Project instructions must contain 1–12,000 characters.')
        session = self.auth.verified_session()
        # Composite foreign key + RLS enforce parent ownership even via direct API.
        body = {'class_id': class_id, 'name': name, 'instructions': instructions}
        if project_id:
            return self._one(self._rows(session, 'projects', 'PATCH', filters={'id': 'eq.' + valid_id(project_id)},
                                        body=body, prefer='return=representation'))
        return self._one(self._rows(session, 'projects', 'POST', body={**body, 'owner_id': session.user_id},
                                    prefer='return=representation'))

    def list_reviews(self, project_id, offset=0):
        project_id = valid_id(project_id)
        session = self.auth.verified_session()
        return self._rows(session, 'reviews', filters={'project_id': 'eq.' + project_id},
                          extra={**self._page(offset), 'order': 'created_at.asc,id.asc',
                                 'select': 'id,owner_id,project_id,created_at'})

    def load_review(self, review_id):
        review_id = valid_id(review_id)
        session = self.auth.verified_session()
        row = self._one(self._rows(session, 'reviews', filters={'id': 'eq.' + review_id}, extra={'select': '*'}))
        row['snapshot'] = validate_snapshot(row.get('snapshot'))
        return row

    def save_review(self, project_id, save_token, snapshot):
        project_id, save_token = valid_id(project_id), valid_id(save_token)
        snapshot = validate_snapshot(snapshot)
        session = self.auth.verified_session()
        rows = self._rows(session, 'reviews', 'POST', body={
            'owner_id': session.user_id, 'project_id': project_id, 'save_token': save_token, 'snapshot': snapshot},
            extra={'on_conflict': 'owner_id,save_token'}, prefer='resolution=ignore-duplicates,return=representation')
        # A rerun may encounter the DB's unique token. Fetch, never overwrite history.
        if not rows:
            rows = self._rows(session, 'reviews', filters={'save_token': 'eq.' + save_token}, extra={'select': '*'})
        row = self._one(rows)
        if row.get('project_id') != project_id or row.get('snapshot') != snapshot:
            raise CloudError('This save token belongs to a different review. Start a fresh save.')
        return row

    def deletion_counts(self, kind, record_id):
        """For confirmation UI; counts must be shown again if concurrent data changes."""
        if kind not in self.TABLES:
            raise CloudError('Unsupported archive item.')
        record_id = valid_id(record_id)
        session = self.auth.verified_session()
        self._one(self._rows(session, kind, filters={'id': 'eq.' + record_id}, extra={'select': 'id,owner_id'}))
        # PostgREST count-only responses would need separate transport support. Use
        # exact server-side RPC instead, so counts are not truncated by row limits.
        result = self.auth.api.send('POST', '/rest/v1/rpc/rr_deletion_counts', token=session.access_token,
                                    body={'item_kind': kind, 'item_id': record_id})
        if (not isinstance(result, dict) or set(result) != {'classes', 'projects', 'reviews'}
                or any(type(n) is not int or n < 0 for n in result.values())):
            raise CloudError('Deletion counts could not be loaded. Retry before deleting.')
        return result

    def delete(self, kind, record_id, *, confirmed=False):
        if not confirmed:
            raise CloudError('Confirm the selected item and its affected records before deleting.')
        if kind not in self.TABLES:
            raise CloudError('Unsupported archive item.')
        record_id = valid_id(record_id)
        session = self.auth.verified_session()
        return self._one(self._rows(session, kind, 'DELETE', filters={'id': 'eq.' + record_id},
                                    prefer='return=representation'))
