"""Local Streamlit UI; assignment text lives only in the current session."""
from dotenv import load_dotenv
import streamlit as st
from radar import (extract, evaluate, confirmed_requirements, check_inputs, ReviewError,
                   INSTRUCTION_LIMIT, DRAFT_LIMIT)

load_dotenv()
st.set_page_config(page_title='Rubric Radar', page_icon='📡', layout='centered')
st.title('Rubric Radar')
st.subheader('Know what’s missing. Understand what matters. Submit stronger work.')
st.caption('A pre-submission coach for MBA written reports and projects. Feedback is not an official grade.')
st.info('Paste text only. Layout, course materials, factual accuracy, and source validity are not verified. '
        'You remain responsible for your work and your course’s AI rules.')
st.caption('Text is held in this browser session’s server memory, with no application storage or analytics. '
           'Live reviews send text to OpenRouter and a model provider using restricted privacy routing. '
           'Before real coursework, verify account logging settings and provider policies. '
           'Only share work you have permission to share.')


def invalidate_inputs():
    for key in ('originals', 'requirement_text', 'confirmed', 'result', 'extract_meta', 'review_meta'):
        st.session_state.pop(key, None)


def invalidate_confirmation():
    for key in ('confirmed', 'result', 'review_meta'):
        st.session_state.pop(key, None)


def clear():
    st.session_state.clear()


st.button('Clear this session', on_click=clear)
instructions = st.text_area('Assignment instructions or rubric', key='instructions', height=180,
                            help=f'Maximum {INSTRUCTION_LIMIT:,} characters. No silent truncation.',
                            on_change=invalidate_inputs)
draft = st.text_area('Your written draft', key='draft', height=260,
                     help=f'Maximum {DRAFT_LIMIT:,} characters. Separate paragraphs with blank lines.',
                     on_change=invalidate_inputs)
st.caption(f'Instructions: {len(instructions):,}/{INSTRUCTION_LIMIT:,} · Draft: {len(draft):,}/{DRAFT_LIMIT:,} characters')
allowed = st.checkbox('I am permitted to share this text and understand it will be sent to AI providers.', key='consent')
if st.button('1. Extract requirements', type='primary', disabled=not allowed):
    try:
        check_inputs(instructions, draft)
        invalidate_inputs()
        with st.spinner('Extracting requirements…'):
            originals, meta = extract(instructions, draft)
        st.session_state.originals = originals
        st.session_state.requirement_text = '\n'.join(r['text'] for r in originals)
        st.session_state.extract_meta = meta
    except ReviewError as exc:
        st.error(str(exc))

if 'originals' in st.session_state:
    st.header('2. Check the requirements')
    st.write('Correct, add, or remove requirements below. Use one requirement per line, up to 25. '
             'Changed and new items are marked as student-provided; confirm that they reflect the assignment.')
    with st.expander('Inspect extracted sources and ambiguities'):
        for i, r in enumerate(st.session_state.originals, 1):
            st.write(f'Requirement {i}')
            st.text(r['text'])
            st.text('Instruction excerpt: ' + r['source'])
            if r['ambiguity']:
                st.warning(r['ambiguity'])
    text = st.text_area('Requirements to confirm', key='requirement_text', height=220,
                        on_change=invalidate_confirmation)
    if st.button('Confirm requirements'):
        try:
            st.session_state.confirmed = confirmed_requirements(text, st.session_state.originals)
            st.session_state.pop('result', None)
        except ReviewError as exc:
            st.error(str(exc))

if 'confirmed' in st.session_state:
    st.success('Requirements confirmed. Ready to review your draft.')
    for r in st.session_state.confirmed:
        st.text(f"{r['id']}: {r['text']}" + (' [student-provided]' if r['student_added'] else ''))
    if st.button('3. Review my draft', type='primary', disabled=not allowed):
        st.session_state.pop('result', None)
        try:
            with st.spinner('Reviewing rubric coverage and reasoning…'):
                result, meta = evaluate(instructions, draft, st.session_state.confirmed)
            st.session_state.result = result
            st.session_state.review_meta = meta
        except ReviewError as exc:
            st.error(str(exc))

if 'result' in st.session_state:
    result = st.session_state.result
    st.header('Your review')
    st.caption('AI findings can be wrong. Check evidence before revising. Missing means evidence was not found.')
    lookup = {r['id']: r['text'] for r in st.session_state.confirmed}
    for f in result['findings']:
        with st.expander(f"{f['requirement_id']} · {f['status']}", expanded=True):
            st.text(lookup[f['requirement_id']])
            st.text(f['explanation'])
            if f['gap']:
                st.text('Gap: ' + f['gap'])
            for e in f['evidence']:
                st.caption(f"Draft paragraph {e['paragraph']}")
                st.text(e['quote'])
    st.header('Your revision priorities')
    if not result['recommendations']:
        st.write('No verified priorities returned. Review any unresolved requirements manually.')
    for i, rec in enumerate(result['recommendations'], 1):
        st.subheader(f"{i}. {rec['label']}")
        st.text(rec['action'])
        st.text('Why: ' + rec['why'])
        st.text('Approach: ' + rec['approach'])
        if rec['requirement_ids']:
            st.caption('Requirements: ' + ', '.join(rec['requirement_ids']))
    for limitation in result['limitations']:
        st.warning(limitation)
    st.write('Revise in your own editor, then paste your updated draft above for a fresh review. '
             'Reviews are not saved or automatically compared.')
    with st.expander('Run details (no assignment text)'):
        st.json({'extraction': st.session_state.extract_meta, 'evaluation': st.session_state.review_meta})
