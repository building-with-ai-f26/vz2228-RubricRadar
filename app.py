"""Streamlit review UI with guest mode and gated private-library integration."""
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import library_ui as library
from feedback_ui import render_feedback
from supabase_api import CloudError
from sample_library import DEMO_INSTRUCTIONS, DEMO_DRAFT
from radar import (extract, evaluate, confirmed_requirements, check_inputs, ReviewError,
                   INSTRUCTION_LIMIT, DRAFT_LIMIT)

load_dotenv()
st.set_page_config(page_title='Rubric Radar', page_icon='📡', layout='centered')
# Trusted static code only; st.html executes in the app document, not an iframe.
analytics = (Path(__file__).parent / 'docs' / 'posthog.js').read_text()
st.html('<script>window.RUBRIC_RADAR_SURFACE = "local_app";\n' + analytics + '</script>',
        unsafe_allow_javascript=True)
st.html('<style>' + (Path(__file__).parent / 'app_style.css').read_text() + '</style>')


def invalidate_inputs():
    for key in ('originals', 'requirement_text', 'confirmed', 'result', 'extract_meta', 'review_meta', 'rr_save_token', 'rr_saved_token', 'rr_review_hash'):
        st.session_state.pop(key, None)


def invalidate_confirmation():
    for key in ('confirmed', 'result', 'review_meta', 'rr_save_token', 'rr_saved_token', 'rr_review_hash'):
        st.session_state.pop(key, None)


def show_request_error(exc):
    st.error(str(exc))
    if exc.diagnostics:
        with st.expander('Request diagnostics (no assignment text)', expanded=True):
            st.json(exc.diagnostics)
            st.caption('Null means the provider did not report a usable value. '
                       'Output tokens may include reasoning; counts do not establish answer length.')


def clear():
    library.clear_work()


def load_demo():
    invalidate_inputs()
    st.session_state.instructions = DEMO_INSTRUCTIONS
    st.session_state.draft = DEMO_DRAFT
    st.session_state.consent = False


def review(route):
    project = library.work_context(route)
    readonly = library.locked() or bool(st.session_state.get('rr_sample'))
    a, b = st.columns(2)
    a.button('Clear this session', on_click=clear, disabled=readonly)
    b.button('Load demo example', on_click=load_demo, disabled=readonly,
             help='Replace both working text fields with a synthetic example. Nothing is saved or sent; sharing consent resets.')
    instructions = st.text_area('Assignment instructions or rubric', key='instructions', height=180,
                                help=f'Maximum {INSTRUCTION_LIMIT:,} characters. No silent truncation.',
                                on_change=invalidate_inputs, disabled=readonly)
    draft = st.text_area('Your written draft', key='draft', height=260,
                         help=f'Maximum {DRAFT_LIMIT:,} characters. Separate paragraphs with blank lines.',
                         on_change=invalidate_inputs, disabled=readonly)
    st.caption(f'Instructions: {len(instructions):,}/{INSTRUCTION_LIMIT:,} · Draft: {len(draft):,}/{DRAFT_LIMIT:,} characters')
    allowed = st.checkbox('I am permitted to share this text and understand it will be sent to AI providers.', key='consent', disabled=readonly)
    if st.button('Extract requirements', type='primary', disabled=not allowed or readonly):
        try:
            check_inputs(instructions, draft)
            invalidate_inputs()
            with st.spinner('Extracting requirements…'):
                originals, meta = extract(instructions, draft)
            st.session_state.originals = originals
            st.session_state.requirement_text = '\n'.join(r['text'] for r in originals)
            st.session_state.extract_meta = meta
        except ReviewError as exc:
            show_request_error(exc)

    if 'originals' in st.session_state:
        st.header('Check requirements & review')
        st.write('Correct, add, or remove requirements below. Use one requirement per line, up to 25. '
                 'Then confirm and review your draft in one step. Changed and new items are marked as student-provided.')
        with st.expander('Inspect extracted sources'):
            for i, r in enumerate(st.session_state.originals, 1):
                st.write(f'Requirement {i}')
                st.text(r['text'])
                st.text('Instruction excerpt: ' + r['source'])
        text = st.text_area('Requirements to confirm', key='requirement_text', height=220,
                            on_change=invalidate_confirmation, disabled=readonly)
        if st.button('Confirm & review my draft', type='primary', disabled=not allowed or readonly):
            st.session_state.pop('result', None)
            st.session_state.pop('review_meta', None)
            try:
                check_inputs(instructions, draft)
                st.session_state.confirmed = confirmed_requirements(text, st.session_state.originals)
                with st.spinner('Checking your draft against the requirements…'):
                    result, meta = evaluate(instructions, draft, st.session_state.confirmed)
                st.session_state.result = result
                st.session_state.review_meta = meta
                library.record_result()
            except ReviewError as exc:
                show_request_error(exc)


    if 'result' in st.session_state:
        render_feedback(st.session_state.result, st.session_state.confirmed,
                        st.session_state.get('extract_meta'), st.session_state.get('review_meta'))
    library.save_controls(project)


try:
    route = library.shell()
    if route['screen'] == 'work':
        review(route)
    else:
        library.render_page(route)
except CloudError as exc:
    library.cloud_error(exc)


with st.container(key='review_privacy'), st.expander('Privacy and review limits'):
    st.info('Paste text only. Layout, course materials, factual accuracy, and source validity are not verified. '
            'You remain responsible for your work and your course’s AI rules.')
    st.caption('Guest text stays in this browser session’s server memory without archive writes. '
               'When enabled, private library saves explicitly store selected coursework in Supabase cloud storage. '
               'Clearing this session leaves saved records intact. Active-record deletion does not erase backups. '
               'PostHog measures pageviews and named button clicks and records a masked session replay. '
               'Replay text and inputs are masked; coursework is not included in click events. '
               'Live reviews send text to OpenRouter and a model provider using restricted privacy routing. '
               'Before real coursework, verify account logging settings and provider policies. '
               'Only share work you have permission to share.')
