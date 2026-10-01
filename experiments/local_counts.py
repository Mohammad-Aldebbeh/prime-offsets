"""Check CRT counts by direct enumeration modulo 210 for selected centers."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compute import ROOT, write_csv
from src.prime_offsets import allowed_residues, local_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'results')
    args = parser.parse_args()
    rows = []
    for n in (2, 4, 6, 10, 14, 30, 42, 210):
        counts = []
        for directions in ((1,), (-1,), (1, -1)):
            period, residues = allowed_residues(n, (2, 3, 5, 7), directions)
            predicted = local_count(n, (2, 3, 5, 7), both=len(directions) == 2)
            if predicted != len(residues):
                raise ValueError(f'CRT mismatch at n={n}, directions={directions}')
            counts.append(predicted)
        rows.append(dict(zip(('n', 'period', 'upper', 'lower', 'both'), (n, period, *counts))))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / 'local_counts.csv', ['n', 'period', 'upper', 'lower', 'both'], rows)
    print('All 24 CRT counts agree with direct enumeration modulo 210.')


if __name__ == '__main__':
    main()
