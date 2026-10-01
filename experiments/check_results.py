"""Regenerate every checked-in output and verify the displayed tables."""

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tex_integer(value):
    return format(value, ',').replace(',', r'\,')


def results_table(summary):
    upper, lower = summary['q_plus'], summary['q_minus']
    count = tex_integer(summary['even_n_tested'])
    return '\n'.join([
        rf'Even inputs & ${count}$ & ${count}$\\',
        rf"Failures & {len(upper['failures'])} & {len(lower['failures'])}\\",
        rf"Largest minimum & {upper['maximum']} & {lower['maximum']}\\",
        rf"Center of largest minimum & ${tex_integer(upper['maximum_at'][0])}$ & ${tex_integer(lower['maximum_at'][0])}$\\",
        rf"Mean & {upper['mean']:.4f} & {lower['mean']:.4f}\\",
        rf"Median & {upper['median']:g} & {lower['median']:g}\\",
        rf"95th percentile & {upper['percentile_95_nearest_rank']} & {lower['percentile_95_nearest_rank']}\\",
    ])


def main():
    with tempfile.TemporaryDirectory() as folder:
        destination = Path(folder)
        for script, options in (('compute.py', ['--limit', '10000']),
                                ('experiments/local_counts.py', [])):
            subprocess.run([sys.executable, str(ROOT / script), *options,
                            '--output-dir', str(destination)], check=True, capture_output=True)
        for name in ('offsets.csv', 'records.csv', 'summary.json', 'local_counts.csv'):
            require((ROOT / 'results' / name).read_bytes() == (destination / name).read_bytes(),
                    'regeneration mismatch: ' + name)
        summary = json.loads((destination / 'summary.json').read_text())
        with (destination / 'local_counts.csv').open(newline='') as stream:
            local = list(csv.DictReader(stream))

    note = (ROOT / 'math' / 'note.tex').read_text(encoding='utf-8')
    expected = results_table(summary)
    actual = note.split('% BEGIN RESULTS TABLE\n')[1].split('\n% END RESULTS TABLE')[0]
    require(actual == expected, 'note results table differs from generated data')
    expected_local = '\n'.join(rf"{r['n']} & {r['upper']} & {r['lower']} & {r['both']}\\" for r in local)
    actual_local = note.split('% BEGIN LOCAL TABLE\n')[1].split('\n% END LOCAL TABLE')[0]
    require(actual_local == expected_local, 'note local table differs from generated data')

    upper, lower = summary['q_plus'], summary['q_minus']
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    expected_rows = [
        f"| Failures | {len(upper['failures'])} | {len(lower['failures'])} |",
        f"| Largest minimum | {upper['maximum']} | {lower['maximum']} |",
        f"| Center of largest minimum | {upper['maximum_at'][0]:,} | {lower['maximum_at'][0]:,} |",
        f"| Mean | {upper['mean']:.4f} | {lower['mean']:.4f} |",
        f"| Median | {upper['median']:g} | {lower['median']:g} |",
        f"| 95th percentile, nearest rank | {upper['percentile_95_nearest_rank']} | {lower['percentile_95_nearest_rank']} |",
    ]
    for row in expected_rows:
        require(row in readme, 'README table mismatch: ' + row)
    require(summary['limit'] == 10000 and summary['even_n_tested'] == 5000,
            'unexpected documented finite range')
    print('All four outputs reproduce byte for byte; both note tables and the README table agree.')


if __name__ == '__main__':
    main()
