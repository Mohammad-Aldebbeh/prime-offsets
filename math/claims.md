# Mathematical status

The [note](note.pdf) is the main exposition; its [source](note.tex) contains the full proofs. The following inventory also records the status of claims in the earlier repository writeup.

| Claim | Status | Where and scope |
|---|---|---|
| Offset bounds put the primes in adjacent square gaps | Proved algebra | Section 1; strict inequalities |
| The two universal assertions imply Legendre's conjecture | Proved conditional implication | Proposition 1; no unconditional prime-existence conclusion |
| Offset 2 fails except for the lower witness at $n=2$ | Proved parity restriction | Section 1 |
| Prime offsets dividing an even $n\ge4$ fail | Proved | Proposition 2 |
| No fixed finite offset set works for all even squares | Proved | Corollary 3; does not assert existence of larger witnesses |
| Modulo-3 restrictions | Proved | Proposition 4; excludes $q=3$ from its hypotheses |
| One-sided local counts and equal complete-period counts | Proved finite formula | Proposition 5; fixed center, variable integer residue |
| Simultaneous local counts and the common-witness restriction | Proved elementary extension | Proposition 6 and Corollary 7 |
| Finite local correction factors | Proved algebra | Section 3; prime-frequency interpretation is heuristic |
| Bézout's identity, CRT and square-root trial-division criterion | Standard elementary facts, with arguments included | Sections 2, 3 and 5 |
| Both bounded minima through 10,000 | Reproducible computation | Section 5; every even input, every minimum independently checked |
| Means, quantiles and records | Exact finite data summaries | Section 5 and `results/`; not asymptotic estimates |
| Lower assertion through two billion | Deduction using external computation | Proposition 8; published Goldbach bound plus local small cases |
| Expected-count and first-offset scales | Heuristic | Section 7; no proved probability model or growth law |
| Poisson zero-count formula | Additional modeling assumption | Section 7; not used to establish any result |
| Universal upper/lower existence, converse of the Legendre implication, asymptotic bounds | Unresolved here | No proof is claimed |
| Historical run through $10^8$ and its reported records | Unsupported by available reproducible artifacts | Excluded from current results; earlier text remains in Git history |
| Attribution to an earlier March manuscript | Not independently verifiable from this repository | The manuscript is not supplied; it is not used as mathematical or computational evidence |

The unavailable manuscript and historical computation are not sources for any current result. The finite correction factors are obtained by elementary residue counts; no advanced singular-series theorem is used.

The universal conjectures require more than finding an ordinary prime in each square gap: the displacement itself must be prime. Goldbach existence alone also lacks the required small-summand bound.
