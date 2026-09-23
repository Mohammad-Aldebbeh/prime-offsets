"""Exact, bounded experiment. Python standard library only.

Run: python compute.py --limit 10000
Memory grows quadratically: this transparent reference implementation is
intentionally limited to 20000. It cannot reproduce a run to 100 million.
September 2026 revision.
"""
import argparse
import csv
import hashlib
import json
from math import isqrt, ceil
from pathlib import Path
import platform
from statistics import mean, median


def sieve(limit):
    flags = bytearray(b'\x01') * (limit + 1)
    flags[0:2] = b'\x00\x00'
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p*p:limit+1:p] = b'\x00' * ((limit-p*p)//p + 1)
    return flags


def trial_prime(value):
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % d for d in range(3, isqrt(value) + 1, 2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=10000)
    args = parser.parse_args()
    if not 2 <= args.limit <= 20000:
        parser.error('limit must be between 2 and 20000 (quadratic memory use)')
    top = args.limit - args.limit % 2
    flags = sieve((top+1)**2)
    primes = [q for q in range(2, 2*top+1) if flags[q]]
    rows = []
    for n in range(2, top+1, 2):
        found = []
        for sign in (1, -1):
            answer = None
            for q in primes:
                if q >= 2*n + sign:
                    break
                if flags[n*n+sign*q]:
                    answer = q
                    break
            found.append(answer)
        rows.append({'n': n, 'q_plus': found[0], 'q_minus': found[1]})

    # Independent primality routine checks ALL outputs and ALL earlier
    # prime-offset candidates, verifying minimality, not only witnesses.
    candidates = [q for q in range(2, 2*top+1) if trial_prime(q)]
    assert candidates == primes
    for row in rows:
        n = row['n']
        for sign, key in ((1, 'q_plus'), (-1, 'q_minus')):
            q = row[key]
            stop = q if q is not None else 2*n+sign
            for earlier in candidates:
                if earlier >= stop:
                    break
                assert not trial_prime(n*n+sign*earlier), (n, sign, earlier)
            if q is not None:
                assert trial_prime(q) and trial_prime(n*n+sign*q)
                assert q < 2*n+sign
    assert rows[0] == {'n': 2, 'q_plus': 3, 'q_minus': 2}

    dest = Path(__file__).resolve().parent
    dest.mkdir(exist_ok=True)
    csv_path = dest / 'offsets.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['n', 'q_plus', 'q_minus'])
        writer.writeheader()
        writer.writerows(rows)
    summary = {'limit': top, 'even_n_tested': len(rows),
               'method': 'Exact Eratosthenes sieve; all minima independently checked by trial division',
               'python': platform.python_version(),
               'csv_sha256': hashlib.sha256(csv_path.read_bytes()).hexdigest()}
    records = []
    for key in ('q_plus', 'q_minus'):
        vals = sorted(r[key] for r in rows if r[key] is not None)
        maximum = max(vals) if vals else None
        summary[key] = {'failures': [r['n'] for r in rows if r[key] is None],
                        'maximum': maximum,
                        'maximum_at': [r['n'] for r in rows if r[key] == maximum],
                        'mean': mean(vals) if vals else None,
                        'median': median(vals) if vals else None,
                        'percentile_95_nearest_rank': vals[ceil(.95*len(vals))-1] if vals else None}
        record = -1
        for r in rows:
            if r[key] is not None and r[key] > record:
                record = r[key]
                records.append({'direction': key, 'n': r['n'], 'q': record})
    with (dest/'records.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['direction', 'n', 'q'])
        writer.writeheader()
        writer.writerows(records)
    (dest/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
