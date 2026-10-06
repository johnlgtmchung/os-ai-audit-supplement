"""Recompute descriptive counts from returned labels, not inter-rater reliability."""
import csv
import json
from pathlib import Path


def summarize(rows):
    if len({r['item_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate item ID')
    for row in rows:
        for role in ('colleague', 'author'):
            state, score = row[f'{role}_state'], row[f'{role}_score']
            if state == 'SCORED':
                if score not in {'0', '1', '2', '3'}:
                    raise ValueError('SCORED requires a numeric label')
            elif state in {'UD', 'ADJ', 'N/A'}:
                if score != '':
                    raise ValueError('Scope status must not have a numeric label')
            else:
                raise ValueError('Missing or unknown scope state')
    paired = [r for r in rows if r['colleague_state'] == r['author_state'] == 'SCORED']
    confusion = {}
    for r in rows:
        key = r['colleague_state'] + ' / ' + r['author_state']
        confusion[key] = confusion.get(key, 0) + 1
    return {
        'items': len(rows), 'case_clusters': len({r['case_id'] for r in rows}),
        'state_matches': sum(r['colleague_state'] == r['author_state'] for r in rows),
        'state_confusion_colleague_author': confusion,
        'jointly_numeric': len(paired),
        'equal_numeric_labels': sum(r['colleague_score'] == r['author_score'] for r in paired),
        'excluded_from_numeric_comparison': len(rows) - len(paired),
        'discrepant_items': [r['item_id'] for r in rows if
                            (r['colleague_state'], r['colleague_score']) !=
                            (r['author_state'], r['author_score'])],
        'interpretation': 'Descriptive record correspondence; not a controlled reliability estimate.',
    }


if __name__ == '__main__':
    with Path(__file__).with_name('review_comparison.csv').open(newline='') as f:
        print(json.dumps(summarize(list(csv.DictReader(f))), indent=2))
