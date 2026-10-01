"""Finite checks of the implementation; mathematical proofs are in the note."""

import copy
import csv
import hashlib
import json
from math import gcd, prod
from pathlib import Path
import tempfile
import unittest

from compute import statistics, write_results
from src.prime_offsets import (allowed_residues, local_count, minimum_offset,
                               passes_filter, search, sieve, trial_prime,
                               verify_rows)

ROOT = Path(__file__).resolve().parents[1]


def direct_prime(x):
    return x >= 2 and not any(x % d == 0 for d in range(2, x))


class PrimalityTests(unittest.TestCase):
    def test_sieve_boundaries(self):
        self.assertEqual(sieve(0), bytearray([0]))
        self.assertEqual(sieve(1), bytearray([0, 0]))
        self.assertEqual(sieve(2), bytearray([0, 0, 1]))
        with self.assertRaises(ValueError):
            sieve(-1)

    def test_three_primality_methods(self):
        flags = sieve(1000)
        for x in range(-3, 1001):
            self.assertEqual(trial_prime(x), direct_prime(x), x)
            if x >= 0:
                self.assertEqual(bool(flags[x]), direct_prime(x), x)


class SearchTests(unittest.TestCase):
    def test_minima_by_direct_enumeration(self):
        rows = search(60)
        for row in rows:
            for sign, key in ((1, 'q_plus'), (-1, 'q_minus')):
                witnesses = [q for q in range(2, 2*row['n'] + sign)
                             if direct_prime(q) and direct_prime(row['n']**2 + sign*q)]
                self.assertEqual(row[key], min(witnesses) if witnesses else None)

    def test_filtered_and_unfiltered_search(self):
        top = 400
        flags = sieve((top + 1)**2)
        primes = [q for q in range(2, 2*top + 1) if flags[q]]
        for n in range(2, top + 1, 2):
            for sign in (1, -1):
                self.assertEqual(minimum_offset(n, sign, primes, flags),
                                 minimum_offset(n, sign, primes, flags, filtered=False))

    def test_equal_modulus_exceptions(self):
        self.assertTrue(passes_filter(2, 2, -1))  # shifted prime is 2
        self.assertTrue(passes_filter(2, 3, 1))   # shifted prime is 7
        self.assertEqual(search(2), [{'n': 2, 'q_plus': 3, 'q_minus': 2}])

    def test_strict_boundary_and_failure(self):
        flags = sieve(50)
        self.assertIsNone(minimum_offset(2, -1, [3], flags))
        self.assertIsNone(minimum_offset(4, 1, [2, 3, 5, 7], bytearray(50)))

    def test_parameters(self):
        self.assertEqual(search(11), search(10))
        for limit in (-1, 0, 1, 20001):
            with self.assertRaises(ValueError):
                search(limit)
        with self.assertRaises(ValueError):
            minimum_offset(3, 1, [], bytearray())
        with self.assertRaises(ValueError):
            minimum_offset(4, 0, [], bytearray())

    def test_verifier_detects_false_witness_and_false_failure(self):
        rows = search(4)
        verify_rows(rows, 4)
        for field, value in (('q_plus', None), ('q_plus', 2), ('q_minus', 3)):
            broken = copy.deepcopy(rows)
            broken[0][field] = value
            with self.assertRaises(ValueError):
                verify_rows(broken, 4)

    def test_verifier_detects_nonminimal_witness(self):
        rows = search(4)
        rows[1]['q_plus'] = 7  # 23 is prime, but 19 already comes from q=3
        with self.assertRaises(ValueError):
            verify_rows(rows, 4)

    def test_verifier_detects_missing_or_duplicate_center(self):
        rows = search(6)
        for broken in (rows[:-1], [rows[0], rows[0], rows[2]], list(reversed(rows))):
            with self.assertRaises(ValueError):
                verify_rows(broken, 6)


class ArithmeticTests(unittest.TestCase):
    def test_prime_divisor_obstruction(self):
        for n in range(4, 100, 2):
            for q in range(2, n + 1):
                if trial_prime(q) and n % q == 0:
                    self.assertFalse(trial_prime(n*n + q))
                    self.assertFalse(trial_prime(n*n - q))

    def test_modulo_three_and_common_witness(self):
        for n in range(4, 200, 2):
            if n % 3 == 0:
                continue
            for q in range(2, 2*n - 1):
                if not trial_prime(q):
                    continue
                upper, lower = trial_prime(n*n + q), trial_prime(n*n - q)
                if q > 3 and upper:
                    self.assertEqual(q % 3, 1)
                if q > 3 and lower:
                    self.assertEqual(q % 3, 2)
                if upper and lower:
                    self.assertEqual(q, 3)
        self.assertTrue(trial_prime(4**2 + 3) and trial_prime(4**2 - 3))

    def test_crt_products_and_symmetry(self):
        for moduli in ((), (2,), (3,), (2, 3), (2, 3, 5), (2, 3, 5, 7)):
            for n in range(2, 64, 2):
                period, upper = allowed_residues(n, moduli, (1,))
                _, lower = allowed_residues(n, moduli, (-1,))
                _, both = allowed_residues(n, moduli, (1, -1))
                self.assertEqual(period, prod(moduli))
                self.assertEqual(len(upper), local_count(n, moduli))
                self.assertEqual(len(lower), local_count(n, moduli))
                self.assertEqual(len(both), local_count(n, moduli, both=True))
                self.assertEqual(set(lower), {(-a) % period for a in upper})
                self.assertEqual(set(both), set(upper) & set(lower))
                self.assertEqual(upper, [a for a in range(period)
                                         if gcd(a*(n*n+a), period) == 1])

    def test_modulus_validation(self):
        for moduli in ((2, 2), (4,), (0,), (-3,)):
            with self.assertRaises(ValueError):
                local_count(4, moduli)
        with self.assertRaises(ValueError):
            allowed_residues(4, (2, 3), ())

    def test_goldbach_threshold_arithmetic(self):
        self.assertEqual(2*4891 - 1, 9781)  # equality does not meet the strict bound
        self.assertLess(2*4890 - 1, 9781)
        self.assertGreater(2*4892 - 1, 9781)
        self.assertEqual((2*10**9)**2, 4*10**18)
        self.assertGreater((2*10**9 + 2)**2, 4*10**18)


class OutputTests(unittest.TestCase):
    def test_failure_statistics(self):
        rows = [{'n': 2, 'q_plus': None, 'q_minus': None}]
        summary = statistics(rows, 'q_plus')
        self.assertEqual(summary['failures'], [2])
        self.assertEqual(summary['maximum_at'], [])
        self.assertIsNone(summary['mean'])

    def test_deterministic_output(self):
        rows = search(30)
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder)
            write_results(rows, dest)
            first = {p.name: p.read_bytes() for p in dest.iterdir()}
            write_results(rows, dest)
            self.assertEqual(first, {p.name: p.read_bytes() for p in dest.iterdir()})
            self.assertNotIn(b'\r', first['offsets.csv'])

    def test_complete_checked_in_dataset(self):
        path = ROOT / 'results' / 'offsets.csv'
        with path.open(newline='', encoding='utf-8') as stream:
            rows = [{key: int(value) if value else None for key, value in row.items()}
                    for row in csv.DictReader(stream)]
        verify_rows(rows, 10000)
        summary = json.loads((path.parent / 'summary.json').read_text())
        self.assertEqual(summary['even_n_tested'], len(rows))
        self.assertEqual(summary['csv_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        for key in ('q_plus', 'q_minus'):
            self.assertEqual(summary[key], statistics(rows, key))


if __name__ == '__main__':
    unittest.main()
