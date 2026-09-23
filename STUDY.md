# Mathematical roadmap

The project proceeds from a precise prime-offset question to structural results and finite verification.

1. **Definitions and edge cases:** the strict offset bounds and the exceptional role of the prime 2.
2. **Connection to Legendre's conjecture:** the even/odd interval argument showing that the two offset conjectures jointly imply it.
3. **Divisibility obstructions:** prime divisors of the center and products of small primes rule out specified offsets.
4. **Residue restrictions:** congruence conditions filter candidates, with exceptions when a tested value equals the modulus.
5. **Finite local factors:** the Chinese remainder theorem combines exact residue counts for a fixed center.
6. **Heuristic interpretation:** typical offsets, record offsets, and the distinction between expected counts and existence.
7. **Exact computation:** an increasing-order search using a prime sieve, followed by a separate trial-division check of each minimum.
8. **Literature-based extension:** minimal Goldbach partitions yield a much larger verified range for the lower bound.

The proofs are in [NOTE.md](NOTE.md) and [LITERATURE_BOUND.md](LITERATURE_BOUND.md). The complete finite dataset accompanies the implementation.
