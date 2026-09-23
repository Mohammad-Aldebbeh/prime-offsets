# A finite-range corollary for the lower prime-offset conjecture

## Published input

Oliveira e Silva, Herzog, and Pardi computed minimal Goldbach partitions for all even integers up to $4\times10^{18}$. Section 2.1 and Table 4 of their paper record 9,781 as the largest minimal smaller summand in that range.

Reference: T. Oliveira e Silva, S. Herzog, S. Pardi, *Empirical verification of the even Goldbach conjecture and computation of prime gaps up to $4\cdot10^{18}$*, Mathematics of Computation **83** (2014), 2033–2060, DOI [10.1090/S0025-5718-2013-02787-1](https://doi.org/10.1090/S0025-5718-2013-02787-1). See [the authors' publication record](https://sweet.ua.pt/tos/bib/4.12.html) and [a readable copy of the published paper](https://denisevellachemla.eu/empirical-verification-of-the-even-CG.pdf), Table 4 on printed page 2043.

## Deduction

**Finite-range corollary, using the published computation.** For every even integer $2\le n\le2\times10^9$, there is a prime $q<2n-1$ such that $n^2-q$ is prime.

**Proof.** If $4892\le n\le2\times10^9$, then $n^2\le4\times10^{18}$. The published minimal-partition result supplies primes $q,p$ with $n^2=q+p$ and $q\le9781$. Since $2n-1\ge9783>9781$, the required strict bound holds. All remaining even integers $2\le n\le4890$ are covered by the repository's exact calculation through 10,000, independently checked by trial division. $\square$

The corollary combines the published exhaustive computation of Oliveira e Silva, Herzog, and Pardi with the exact small cases in this repository.

## Why this does not settle the upper conjecture

The upper question asks for $p-q=n^2$ with prime $q<2n+1$. A sum representation $p+q=n^2$ does not give this difference representation. Nor does merely finding a prime in $(n^2,(n+1)^2)$ ensure that its difference from $n^2$ is prime.

This project independently verifies the upper bound only through 10,000. The original manuscript reports a larger computation, but its code is unavailable. No matching literature-based upper range has been established in this revision. The verified ranges are therefore different: through 10,000 for the upper bound and through two billion for the lower bound.
