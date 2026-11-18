"""Session-isolated navigation, account forms and private library screens."""
import hashlib
import json
import os
from uuid import uuid4

import streamlit as st
from archive import Archive, make_snapshot
from auth import Auth
from google_signin import google_button, google_client_id
from feedback_ui import render_feedback
from sample_library import SampleArchive
from supabase_api import CloudAPI, CloudConfig, CloudError

WORK_KEYS = ('instructions', 'draft', 'consent', 'originals', 'requirement_text', 'confirmed',
             'result', 'extract_meta', 'review_meta', 'rr_work_context', 'rr_baseline',
             'rr_save_token', 'rr_saved_token', 'rr_review_hash', 'project_name')


def setting(name, default=''):
    if name in os.environ:
        return os.environ[name]
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return default


def cloud_config():
    # Operator switch, not a replacement for RLS. Remains off until actual proof.
    if str(setting('RUBRIC_RADAR_ARCHIVE_ENABLED', 'false')).lower() != 'true':
        return None
    return CloudConfig.from_settings({key: setting(key) for key in ('SUPABASE_URL', 'SUPABASE_PUBLISHABLE_KEY')})


def clear_work():
    for key in WORK_KEYS:
        st.session_state.pop(key, None)


def transition(target):
    clear_work()
    for key in list(st.session_state):
        if key.startswith(('auth_', 'form_', 'delete_')) or key in ('rr_pending', 'rr_delete'):
            st.session_state.pop(key, None)
    st.session_state.rr_route = target


def dirty():
    baseline = st.session_state.get('rr_baseline', {'instructions': '', 'draft': '', 'project_name': ''})
    return (any(st.session_state.get(k, '') != baseline.get(k, '') for k in ('instructions', 'draft', 'project_name'))
            or bool(st.session_state.get('result') and st.session_state.get('rr_save_token') != st.session_state.get('rr_saved_token')))


def locked():
    return bool(st.session_state.get('rr_pending') or st.session_state.get('rr_delete'))


def navigate(target):
    if st.session_state.get('rr_route', {}).get('screen') == 'work' and dirty():
        st.session_state.rr_pending = target
    else:
        transition(target)


def discard_and_continue():
    transition(st.session_state.rr_pending)


def leave_account():
    auth = st.session_state.pop('rr_auth', None)
    # Clear every UI field and private record before remote logout, even on failure.
    st.session_state.clear()
    st.session_state.rr_route = {'screen': 'home'}
    if auth:
        try:
            auth.sign_out()
        except CloudError:
            st.session_state.rr_notice = 'Signed out locally. Remote sign-out could not be confirmed.'


def begin_guest():
    # Guest entry is an identity transition and must not carry account data.
    leave_account()
    st.session_state.rr_route = {'screen': 'work', 'guest': True}


def begin_sample():
    leave_account()
    st.session_state.rr_sample = True
    st.session_state.rr_route = {'screen': 'classes'}


def store():
    if st.session_state.get('rr_sample'):
        return SampleArchive()
    if not cloud_config():
        raise CloudError('The private library is not enabled yet. Continue as guest or explore the sample.')
    auth = st.session_state.get('rr_auth')
    if not auth:
        raise CloudError('Sign in to open your library.')
    return Archive(auth)


def writable():
    return not st.session_state.get('rr_sample') and not locked()


def nav_button(label, target, **kwargs):
    st.button(label, on_click=navigate, args=(target,), disabled=locked(), **kwargs)


def shell():
    route = st.session_state.get('rr_route', {'screen': 'home'})
    if st.session_state.get('rr_auth') and not st.session_state.get('rr_sample'):
        auth = st.session_state.rr_auth
        if route['screen'] != 'login':
            try:
                if not cloud_config():
                    raise CloudError('Library access is not enabled.')
                session = auth.verified_session()
                if session.user_id != st.session_state.get('rr_owner'):
                    raise CloudError('Account changed.')
            except CloudError:
                leave_account()
                st.session_state.rr_route = {'screen': 'login'}
                st.session_state.rr_notice = 'Your session could not be verified. Sign in again.'
                st.rerun()
    elif route['screen'] in ('classes', 'projects', 'saved') or (route['screen'] == 'work' and not route.get('guest')):
        if not st.session_state.get('rr_sample'):
            transition({'screen': 'login'})
            st.rerun()
    with st.container(key='rr_topbar'):
        brand, back, account = st.columns([4, 1.25, 1.75], vertical_alignment='center', wrap=False)
        with brand:
            with st.container(key='rr_brand'):
                st.markdown('**Rubric Radar**')
        with back:
            if route['screen'] != 'home':
                nav_button('Home', {'screen': 'home'}, key='nav_home', type='tertiary')
        with account:
            if st.session_state.get('rr_sample') or st.session_state.get('rr_owner'):
                st.button('Exit sample' if st.session_state.get('rr_sample') else 'Sign out',
                          on_click=leave_account, type='tertiary')
    if notice := st.session_state.pop('rr_notice', None):
        st.info(notice)
    if st.session_state.get('rr_sample'):
        st.caption('SAMPLE LIBRARY · Read-only example. No account, cloud saves or AI calls.')
    if st.session_state.get('rr_pending'):
        st.warning('You have unsaved work. Discard it to leave this review?')
        a, b = st.columns(2)
        a.button('Keep working', on_click=lambda: st.session_state.pop('rr_pending', None))
        b.button('Discard and continue', on_click=discard_and_continue)
    if st.session_state.get('rr_delete'):
        deletion_confirmation()
    return route


def page_buttons(route, length):
    offset = route.get('offset', 0)
    a, b = st.columns(2)
    if offset:
        with a: nav_button('Previous page', {**route, 'offset': max(0, offset - 100)})
    if length == 100:
        with b: nav_button('Next page', {**route, 'offset': offset + 100})


def home():
    st.html('''<section class="rr-hero">
      <h1>Know what to fix next.</h1>
      <p class="rr-intro">Turn your rubric into a clear review.<br>Find the gaps. Focus your next revision.</p>
    </section>''')
    with st.container(key='home_actions'):
        a, b = st.columns(2, vertical_alignment='center')
        a.button('Continue as guest', type='primary', on_click=begin_guest, width='stretch')
        with b:
            nav_button('Open my library', {'screen': 'classes'} if st.session_state.get('rr_owner') else {'screen': 'login'},
                       type='tertiary', width='stretch')
        st.button('Explore sample library', on_click=begin_sample, type='tertiary', width='stretch')
        st.caption('No account needed for a guest review.')
    with st.container(key='home_steps'):
        for column, number, title, description in zip(st.columns(3, gap='large'),
                ('01', '02', '03'), ('Bring your rubric.', 'Check the evidence.', 'Revise with focus.'),
                ('Paste your instructions and draft.', 'Confirm requirements. See what is covered.', 'Leave with up to three revision priorities.')):
            with column:
                st.caption(number)
                st.subheader(title)
                st.caption(description)
    st.caption('For MBA reports and projects. Feedback is guidance, not an official grade.')


def login():
    st.header('Your private review library')
    try:
        config = cloud_config()
    except CloudError as exc:
        st.error(str(exc)); config = None
    enabled = config is not None
    if not enabled:
        st.info('Private accounts are not available yet. Try the sample library or continue as guest.')
    if enabled:
        try:
            client_id = google_client_id(setting('GOOGLE_CLIENT_ID'))
            auth = st.session_state.get('rr_auth')
            if not auth:
                auth = Auth(CloudAPI(config)); st.session_state.rr_auth = auth
            response = google_button(client_id, auth.google_challenge())
            if response is not None:
                if not isinstance(response, dict) or response.get('error'):
                    auth.cancel_google()
                    raise CloudError('Google sign-in could not finish. Try again or continue as guest.')
                session = auth.sign_in_google(response.get('credential'), response.get('challenge_id'))
                clear_work()
                st.session_state.rr_owner = session.user_id
                transition({'screen': 'classes'}); st.rerun()
        except CloudError as exc:
            st.error(str(exc))
        st.button('Try Google sign-in again', on_click=retry_google)
        st.caption('If you close the Google window, you can try again or continue as guest.')
    else:
        st.button('Continue with Google', disabled=True)
    st.button('Explore sample library', on_click=begin_sample)
    st.button('Continue as guest', on_click=begin_guest)
    st.caption('Google and Supabase process your sign-in identity. No Gmail or Drive access is requested. '
               'This app does not collect a password. Sign out ends this app session; it does not sign you out of Google.')


def retry_google():
    auth = st.session_state.get('rr_auth')
    if auth:
        auth.cancel_google()


def class_accent(class_id):
    # UUID-derived presentation only: stable across renames, sorting and sessions.
    return ('blue', 'mint', 'violet', 'peach', 'rose', 'sand')[int(class_id.replace('-', ''), 16) % 6]


def course_label(text, class_id):
    with st.container(key='course_identity_tone_' + class_accent(class_id)):
        st.text(text)


def classes(route):
    st.header('My classes')
    st.caption('Your projects, with a place for everything.')
    records = store().list_classes(offset=route.get('offset', 0))
    st.caption(f"{len(records)} {'class' if len(records) == 1 else 'classes'} on this page")
    columns = st.columns(2, gap='medium')
    for index, row in enumerate(records):
        with columns[index % 2], st.container(border=True, key='class_card_' + row['id'] + '_tone_' + class_accent(row['id'])):
            with st.container(key='item_title_' + row['id']):
                st.text(row['name'])
            details = ' · '.join(x for x in (row.get('professor'), row.get('semester')) if x)
            if details: st.caption(details)
            nav_button('Open class', {'screen': 'projects', 'class_id': row['id']},
                       key='open_class_' + row['id'], type='tertiary')
    if not records: st.info('No classes on this page. Create your first class below.')
    page_buttons(route, len(records))
    with st.expander('Create a class', expanded=not records):
        with st.form('create_class', clear_on_submit=False):
            name = st.text_input('Class name', max_chars=200, key='form_class_name', disabled=not writable())
            professor = st.text_input('Professor (optional)', max_chars=200, key='form_professor', disabled=not writable())
            semester = st.text_input('Semester (optional)', max_chars=200, key='form_semester', disabled=not writable())
            submitted = st.form_submit_button('Create class', disabled=not writable())
        if submitted:
            row = store().create_class(name, professor, semester)
            transition({'screen': 'projects', 'class_id': row['id']}); st.rerun()


def projects(route):
    archive = store(); course = archive.get_class(route['class_id'])
    st.header('Class projects'); course_label(course['name'], course['id'])
    nav_button('Back to classes', {'screen': 'classes'}, type='tertiary')
    records = archive.list_projects(course['id'], offset=route.get('offset', 0))
    columns = st.columns(2, gap='medium')
    for index, row in enumerate(records):
        with columns[index % 2], st.container(border=True, key='project_card_' + row['id'] + '_tone_' + class_accent(course['id'])):
            with st.container(key='item_title_' + row['id']):
                st.text(row['name'])
            nav_button('Open project', {'screen': 'work', 'project_id': row['id']},
                       key='open_project_' + row['id'], type='tertiary')
    if not records: st.info('No projects on this page. Add a project and its instructions below.')
    page_buttons(route, len(records))
    with st.expander('Create a project', expanded=not records):
        with st.form('create_project'):
            name = st.text_input('Project name', max_chars=200, key='form_project_name', disabled=not writable())
            instructions = st.text_area('Project instructions or rubric', max_chars=12000, key='form_project_instructions', disabled=not writable())
            st.caption('Creating a project explicitly saves its name and instructions to your cloud library.')
            submitted = st.form_submit_button('Create project', disabled=not writable())
        if submitted:
            row = archive.save_project(course['id'], name, instructions)
            transition({'screen': 'work', 'project_id': row['id']}); st.rerun()
    delete_button('Delete class', 'classes', course, {'screen': 'classes'})


def work_context(route):
    if route.get('guest'):
        st.caption('Guest review · no coursework archive writes')
        if 'rr_baseline' not in st.session_state:
            st.session_state.rr_baseline = {'instructions': '', 'draft': '', 'project_name': ''}
        return None
    archive = store(); project = archive.get_project(route['project_id']); course = archive.get_class(project['class_id'])
    course_label(course['name'] + ' / ' + project['name'], course['id'])
    nav_button('Back to projects', {'screen': 'projects', 'class_id': course['id']}, type='tertiary')
    if st.session_state.get('rr_work_context') != project['id']:
        clear_work()
        st.session_state.rr_work_context = project['id']
        st.session_state.instructions = project['instructions']
        st.session_state.project_name = project['name']
        st.session_state.rr_baseline = {'instructions': project['instructions'], 'draft': '', 'project_name': project['name']}
    st.text_input('Project name', key='project_name', max_chars=200, disabled=not writable())
    if st.session_state.get('rr_sample'):
        st.caption('Read-only sample. Open the saved review below to inspect example feedback.')
    return project


def input_hash():
    return hashlib.sha256(json.dumps([st.session_state.get('instructions', ''), st.session_state.get('draft', ''),
                                      st.session_state.get('confirmed', [])], sort_keys=True).encode()).hexdigest()


def record_result():
    st.session_state.rr_save_token = str(uuid4())
    st.session_state.rr_review_hash = input_hash()
    st.session_state.pop('rr_saved_token', None)


def save_controls(project):
    if not project: return
    archive = store()
    st.caption('Save project keeps its name and rubric defaults. Save review keeps the exact draft and feedback snapshot. Nothing is saved automatically.')
    if st.button('Save project', disabled=not writable()):
        archive.save_project(project['class_id'], st.session_state.project_name, st.session_state.get('instructions', ''), project_id=project['id'])
        st.session_state.rr_baseline['instructions'] = st.session_state.instructions
        st.session_state.rr_baseline['project_name'] = st.session_state.project_name
        st.success('Project defaults saved. Your draft has not been saved by this action.')
    current = (bool(st.session_state.get('result')) and st.session_state.get('rr_review_hash') == input_hash()
               and bool(st.session_state.get('rr_save_token')))
    already = current and st.session_state.get('rr_saved_token') == st.session_state.get('rr_save_token')
    if st.button('Save review', disabled=not writable() or not current or already):
        snapshot = make_snapshot(*(st.session_state[k] for k in ('instructions', 'draft', 'originals', 'confirmed', 'result')),
                                 st.session_state.get('extract_meta'), st.session_state.get('review_meta'))
        archive.save_review(project['id'], st.session_state.rr_save_token, snapshot)
        st.session_state.rr_saved_token = st.session_state.rr_save_token
        st.session_state.rr_baseline = dict(instructions=st.session_state.instructions, draft=st.session_state.draft,
                                            project_name=st.session_state.project_name)
        st.success('Review saved. It is now available in this project’s history.')
        st.rerun()
    if already: st.success('This review is saved.')
    st.subheader('Saved reviews')
    offset = st.session_state.get('rr_route', {}).get('offset', 0)
    rows = archive.list_reviews(project['id'], offset=offset)
    for row in rows:
        with st.container(border=True):
            st.text(str(row['created_at']))
            nav_button('Open saved review', {'screen': 'saved', 'review_id': row['id'], 'project_id': project['id']}, key='open_review_' + row['id'])
    if not rows: st.caption('No saved reviews on this page yet.')
    page_buttons(st.session_state.rr_route, len(rows))
    delete_button('Delete project', 'projects', project, {'screen': 'projects', 'class_id': project['class_id']})


def saved(route):
    archive = store(); row = archive.load_review(route['review_id']); project = archive.get_project(row['project_id'])
    st.header('Saved review'); course_label(project['name'], project['class_id']); st.text(str(row['created_at']))
    st.caption('Read-only snapshot. Opening it makes no AI calls.')
    nav_button('Back to project', {'screen': 'work', 'project_id': project['id']}, type='tertiary')
    if st.button('Check a revised draft', disabled=not writable()):
        snapshot = row['snapshot']
        transition({'screen': 'work', 'project_id': project['id']})
        st.session_state.rr_work_context = project['id']
        st.session_state.instructions = snapshot['instructions']; st.session_state.draft = snapshot['draft']
        st.session_state.project_name = project['name']
        # Fresh consent/extraction required; original history remains unchanged.
        st.session_state.rr_baseline = {'instructions': project['instructions'], 'draft': '', 'project_name': project['name']}
        st.rerun()
    snapshot = row['snapshot']
    with st.container(key='snapshot_text'), st.expander('Instructions and draft in this snapshot'):
        st.text(snapshot['instructions']); st.text(snapshot['draft'])
    render_feedback(snapshot['result'], snapshot['confirmed'], snapshot['extract_meta'], snapshot['review_meta'])
    delete_button('Delete review', 'reviews', {'id': row['id'], 'name': 'Review from ' + str(row['created_at'])},
                  {'screen': 'work', 'project_id': project['id']})


def delete_button(label, kind, row, back):
    if st.button(label, disabled=not writable()):
        st.session_state.rr_delete = dict(kind=kind, id=row['id'], name=row['name'], back=back,
                                         counts=store().deletion_counts(kind, row['id']))
        st.rerun()


def deletion_confirmation():
    selected = st.session_state.rr_delete
    st.warning('Permanently delete this item and its saved descendants? This cannot be undone.')
    st.text(selected['name'])
    counts = selected['counts']
    st.write(f"{counts['classes']} classes · {counts['projects']} projects · {counts['reviews']} reviews")
    a, b = st.columns(2)
    if a.button('Cancel deletion'):
        st.session_state.pop('rr_delete', None); st.rerun()
    if b.button('Confirm deletion', type='primary'):
        archive = store(); fresh = archive.deletion_counts(selected['kind'], selected['id'])
        if fresh != counts:
            st.session_state.rr_delete['counts'] = fresh
            st.session_state.rr_notice = 'Affected records changed. Review the updated counts and confirm again.'
        else:
            archive.delete(selected['kind'], selected['id'], confirmed=True)
            transition(selected['back']); st.session_state.rr_notice = 'Deleted from your active library.'
        st.rerun()


def render_page(route):
    if route['screen'] == 'home':
        home()
    elif route['screen'] == 'login':
        login()
    else:
        {'classes': classes, 'projects': projects, 'saved': saved}[route['screen']](route)


def cloud_error(exc):
    auth = st.session_state.get('rr_auth')
    if auth and auth.session is None:
        leave_account(); st.session_state.rr_route = {'screen': 'login'}
        st.session_state.rr_notice = 'Your session ended. Sign in again.'; st.rerun()
    st.error(str(exc))
    nav_button('Return to classes', {'screen': 'classes'}, key='error_back')
