"""Run from repository root: .venv/bin/python tests/smoke_live.py.
Uses only synthetic assignment text; incurs two provider requests. No draft logging.
This is a feasibility check, not the required 10-case quality evaluation.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
from radar import extract, evaluate, confirmed_requirements, ReviewError

INSTRUCTIONS = ('Compare two expansion alternatives. Justify your recommendation. '
                'Discuss implementation risks.')
DRAFT = ('A regional launch costs less but reaches fewer customers. A national launch '
         'has greater reach but higher upfront costs.\n\n'
         'I recommend a regional launch because the company has a limited budget.')

if __name__ == '__main__':
    load_dotenv(Path(__file__).resolve().parents[1] / '.env')
    try:
        originals, extraction_meta = extract(INSTRUCTIONS, DRAFT)
        confirmed = confirmed_requirements('\n'.join(r['text'] for r in originals), originals)
        report, evaluation_meta = evaluate(INSTRUCTIONS, DRAFT, confirmed)
        print(json.dumps({'extraction': extraction_meta, 'evaluation': evaluation_meta,
                          'requirements': len(confirmed),
                          'statuses': [{'requirement_id': f['requirement_id'], 'status': f['status']}
                                       for f in report['findings']],
                          'recommendations': len(report['recommendations'])}, indent=2))
        print('Inspect quality separately: comparison and justification should be addressed; '
              'implementation risks are intentionally absent. Structural success is not proof of accuracy.')
    except ReviewError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
