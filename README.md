# Prime offsets around even squares

A mathematical and computational project by Mohammad Aldebbeh investigating primes of the form $n^2+q$ and $n^2-q$, where $n$ is even and $q$ is prime.

The project combines elementary proofs, congruence obstructions, local-density heuristics, and reproducible computation. The two prime-offset conjectures jointly imply Legendre's conjecture; their universal validity remains open.

## Results

- Elementary proofs establish the implication for Legendre's conjecture, divisibility obstructions, and the failure of every fixed finite set of prime offsets to cover all even squares.
- An exact computation verifies both conjectured bounds for all 5,000 even inputs $2\le n\le10000$. Every minimum is cross-checked by trial division. The largest minimum upper offset is 397 at $n=6046$; the largest minimum lower offset is 467 at $n=8968$.
- A deduction from published minimal Goldbach-partition data, together with the local computation, establishes the lower bound for every even $2\le n\le2\times10^9$. This larger range applies to the lower bound only.

## Contents

- [Mathematical note](NOTE.md): definitions, proofs, congruence restrictions, and heuristics.
- [Literature-based lower bound](LITERATURE_BOUND.md): statement, proof, and source.
- [Reference computation](compute.py), [complete data](offsets.csv), [record offsets](records.csv), and [summary](summary.json).
- [Methods and verification](CONTRIBUTIONS.md).
- [Mathematical roadmap](STUDY.md).

## Reproduce

```sh
python compute.py --limit 10000
```

Python's standard library is sufficient. The program searches allowed prime offsets in increasing order, records the first success or a failure, and independently checks both the returned primes and all earlier prime offsets by trial division.

The sieve's memory use grows quadratically with the limit: its main array uses roughly 100 MB at 10,000, with additional temporary allocations. The implementation caps the limit at 20,000. Running it again overwrites the generated data.

The repository's reproducible dataset covers inputs through 10,000. Historical computations in the March 2026 manuscript are described separately in the methods note.
