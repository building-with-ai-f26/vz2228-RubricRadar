"""Render validated current or saved feedback without model calls."""
import streamlit as st


def render_feedback(result, confirmed, extract_meta=None, review_meta=None):
    st.header('Your review')
    st.caption('AI findings can be wrong. Check evidence before revising. Missing means evidence was not found.')
    counts = {status: sum(f['status'] == status for f in result['findings'])
              for status in ('Met', 'Partially Met', 'Missing', 'Needs Review')}
    with st.container(border=True, key='feedback_summary'):
        st.subheader('Review summary')
        for column, (status, count) in zip(st.columns(4), counts.items()):
            column.metric(status, count)
        gaps = counts['Partially Met'] + counts['Missing']
        st.write(f"{gaps} of {len(result['findings'])} requirements have identified gaps. "
                 f"{counts['Needs Review']} need manual review.")
        st.caption('Open the details on any card to inspect the feedback and evidence.')

    st.subheader('Your revision priorities')
    if not result['recommendations']:
        st.write('No verified priorities returned. Review any unresolved requirements manually.')
    for i, rec in enumerate(result['recommendations'], 1):
        with st.container(border=True, key=f'priority_{i}'):
            st.caption(f"Priority {i} · {rec['label']}")
            st.write(rec['action'])
            if rec['requirement_ids']:
                st.caption('Requirements: ' + ', '.join(rec['requirement_ids']))
            with st.expander('Why this matters and how to approach it'):
                st.write('Why: ' + rec['why'])
                st.write('Approach: ' + rec['approach'])

    status_colors = {'Met': 'met', 'Partially Met': 'partial',
                     'Missing': 'missing', 'Needs Review': 'review'}
    st.subheader('Requirement details')
    lookup = {r['id']: r for r in confirmed}
    for f in result['findings']:
        requirement = lookup[f['requirement_id']]
        with st.container(border=True, key=f"finding_{status_colors[f['status']]}_{f['requirement_id']}"):
            st.write(f"**{f['requirement_id']} · {f['status']}**")
            with st.container(key='finding_title_' + f['requirement_id']):
                st.write(requirement['text'])
            st.write(f['explanation'])
            with st.expander('View gaps, evidence, and rubric source'):
                if f['gap']:
                    st.write('Gap: ' + f['gap'])
                if not f['evidence']:
                    st.caption('No verified draft quotes are available for this finding.')
                for e in f['evidence']:
                    st.caption(f"Draft paragraph {e['paragraph']}")
                    st.write(e['quote'])
                if requirement['source']:
                    st.caption('Assignment source')
                    st.write(requirement['source'])
                if requirement['student_added']:
                    st.caption('Student-provided requirement; check it against the assignment.')

    if result['limitations']:
        with st.expander('Limitations and items to check'):
            for limitation in result['limitations']:
                st.write(limitation)
    st.write('Revise in your own editor, then start a fresh review with your updated draft. '
             'Save explicitly to keep a review; revisions are not automatically compared.')
    with st.expander('Run details (no assignment text)'):
        st.json({'extraction': extract_meta, 'evaluation': review_meta})
