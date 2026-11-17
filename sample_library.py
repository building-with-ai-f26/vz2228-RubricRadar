"""Read-only synthetic library for a local UI walkthrough; never a cloud client."""
from copy import deepcopy
from archive import make_snapshot
from supabase_api import CloudError

# Separate intentionally incomplete example for live demo checks.
DEMO_INSTRUCTIONS = (
    'Write a recommendation for an MBA campus coffee shop choosing a growth initiative. '
    'Compare two options: a student loyalty program and extended evening hours. '
    'Recommend one option and explain why. Identify one implementation risk. '
    'Include a measurable success criterion for a four-week pilot.'
)
DEMO_DRAFT = (
    'The coffee shop could introduce a student loyalty program or extend evening hours. '
    'A loyalty program rewards repeat visits with a free drink after ten purchases and '
    'would use the existing checkout system. Extended hours could reach students leaving '
    'late classes, but would require additional staffing and utility expenses.\n\n'
    'I recommend the loyalty program because it encourages repeat visits while keeping '
    'staffing costs stable. The shop could promote it with a sign at checkout and an '
    'announcement in the student newsletter.'
)

CLASS_ID = '10000000-0000-0000-0000-000000000001'
PROJECT_ID = '20000000-0000-0000-0000-000000000001'
REVIEW_ID = '30000000-0000-0000-0000-000000000001'
INSTRUCTIONS = 'Compare two options. Recommend one option.'
DRAFT = 'Option A costs less. Option B reaches more customers.\n\nI recommend A because our budget is limited.'
ORIGINALS = [{'text': 'Compare two options.', 'source': 'Compare two options.'},
             {'text': 'Recommend one option.', 'source': 'Recommend one option.'}]
CONFIRMED = [dict(id=f'R{i}', text=r['text'], source=r['source'], student_added=False)
             for i, r in enumerate(ORIGINALS, 1)]
RESULT = {'findings': [dict(requirement_id=f'R{i}', status='Met', explanation=explanation, gap='',
                           evidence=[{'quote': quote, 'paragraph': i}])
                       for i, explanation, quote in [
                           (1, 'The draft compares cost and reach.', DRAFT.split('\n\n')[0]),
                           (2, 'The recommendation connects to the budget.', DRAFT.split('\n\n')[1])]],
          'recommendations': [], 'limitations': []}


SAMPLE_CLASSES = [
    dict(id=CLASS_ID, name='Strategy · sample class', professor='Sample professor', semester='Fall 2026'),
    dict(id='10000000-0000-0000-0000-000000000002', name='Marketing · sample class', professor='Sample professor', semester='Fall 2026'),
    dict(id='10000000-0000-0000-0000-000000000003', name='Finance · sample class', professor='Sample professor', semester='Fall 2026'),
]
SAMPLE_PROJECTS = [dict(id=f'20000000-0000-0000-0000-{index:012d}', class_id=course['id'], name=name,
                        instructions=INSTRUCTIONS)
                   for index, (course, name) in enumerate(zip(SAMPLE_CLASSES,
                       ('Market entry · sample project', 'Brand launch · sample project', 'Investment case · sample project')), 1)]


class SampleArchive:
    """No authentication bypass or mutating methods; fixed synthetic records only."""
    def list_classes(self, offset=0):
        return deepcopy(SAMPLE_CLASSES[offset:offset+100])

    def get_class(self, class_id):
        for course in SAMPLE_CLASSES:
            if course['id'] == class_id: return deepcopy(course)
        raise CloudError('Sample class unavailable.')

    def list_projects(self, class_id, offset=0):
        self.get_class(class_id)
        return deepcopy([p for p in SAMPLE_PROJECTS if p['class_id'] == class_id][offset:offset+100])

    def get_project(self, project_id):
        for project in SAMPLE_PROJECTS:
            if project['id'] == project_id: return deepcopy(project)
        raise CloudError('Sample project unavailable.')

    def list_reviews(self, project_id, offset=0):
        self.get_project(project_id)
        review_id = '3' + project_id[1:]
        return [] if offset else [dict(id=review_id, project_id=project_id, created_at='Synthetic example')]

    def load_review(self, review_id):
        project_id = '2' + review_id[1:]
        self.get_project(project_id)
        if not review_id.startswith('3'): raise CloudError('Sample review unavailable.')
        return dict(id=review_id, project_id=project_id, created_at='Synthetic example',
                    snapshot=make_snapshot(INSTRUCTIONS, DRAFT, deepcopy(ORIGINALS), deepcopy(CONFIRMED), deepcopy(RESULT)))
