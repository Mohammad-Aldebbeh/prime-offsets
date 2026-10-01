"""Reproduce the exact bounded search and independent verification."""

import argparse
import csv
import hashlib
import json
from math import ceil
from pathlib import Path
from statistics import mean, median

from src.prime_offsets import MAX_LIMIT, SIGNS, search, verify_rows

ROOT = Path(__file__).resolve().parent


def write_csv(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def statistics(rows, key):
    values = sorted(r[key] for r in rows if r[key] is not None)
    maximum = max(values) if values else None
    return {'successes': len(values),
            'failures': [r['n'] for r in rows if r[key] is None],
            'maximum': maximum,
            'maximum_at': [r['n'] for r in rows if maximum is not None and r[key] == maximum],
            'mean': mean(values) if values else None,
            'median': median(values) if values else None,
            'percentile_95_nearest_rank': values[ceil(.95*len(values))-1] if values else None}


def write_results(rows, destination):
    destination.mkdir(parents=True, exist_ok=True)
    csv_path = destination / 'offsets.csv'
    write_csv(csv_path, ['n', 'q_plus', 'q_minus'], rows)
    records = []
    for _, key in SIGNS:
        record = -1
        for row in rows:
            if row[key] is not None and row[key] > record:
                record = row[key]
                records.append({'direction': key, 'n': row['n'], 'q': record})
    write_csv(destination / 'records.csv', ['direction', 'n', 'q'], records)
    summary = {'limit': rows[-1]['n'], 'even_n_tested': len(rows),
               'method': 'Exact Eratosthenes sieve; all minima independently checked by trial division',
               'csv_sha256': hashlib.sha256(csv_path.read_bytes()).hexdigest(),
               **{key: statistics(rows, key) for _, key in SIGNS}}
    (destination / 'summary.json').write_bytes((json.dumps(summary, indent=2) + '\n').encode())
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=10000)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'results',
                        help='destination; defaults to results/ beside this script')
    args = parser.parse_args()
    if not 2 <= args.limit <= MAX_LIMIT:
        parser.error(f'limit must be between 2 and {MAX_LIMIT} (quadratic memory use)')
    rows = search(args.limit)
    verify_rows(rows, args.limit)
    print(json.dumps(write_results(rows, args.output_dir), indent=2))


if __name__ == '__main__':
    main()
