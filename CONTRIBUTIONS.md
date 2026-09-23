# Methods and verification

## Project development

The project develops the prime-offset formulation in Mohammad Aldebbeh's March 2026 manuscript, *A Symmetrical Strengthening of Legendre's Conjecture Anchored on Even Squares*. The September version adds elementary structural results, a finite local-density calculation, and reproducible code and data.

## Evidence for the results

- **Elementary results:** complete proofs appear in the mathematical note.
- **Reproducible computation:** an exact sieve and a separate trial-division routine verify the minima for all 5,000 even inputs through 10,000.
- **Literature-based lower bound:** published minimal Goldbach-partition data provide the large-range input; the deduction and remaining small cases are documented in LITERATURE_BOUND.md.
- **Heuristics:** the local residue counts are exact. Their interpretation as a model of prime frequency is heuristic.

## Historical computation

The March manuscript reports a run through $10^8$, with record offsets 2,797 and 2,543. Its original code and raw output are unavailable, so that run is excluded from the reproducible dataset and is not used to establish the results in this repository.
