# Prime offsets around even squares: elementary structure and computation

Mohammad Aldebbeh — September 2026. This note develops the prime-offset formulation of the March 2026 manuscript through elementary proofs, local residue calculations, and an exact computational experiment. See CONTRIBUTIONS.md for methods and verification.

## 1. The question

For an even integer $n\ge2$, consider two questions:

1. Is there a prime $q<2n+1$ such that $n^2+q$ is prime?
2. Is there a prime $q<2n-1$ such that $n^2-q$ is prime?

Call these the upper and lower prime-offset conjectures. Each direction may use a different prime $q$. The two bounds place the resulting primes in the intervals immediately above and below $n^2$.

Define bounded minima

$$Q_+(n)=\min\{q:q\text{ prime},\ q<2n+1,\ n^2+q\text{ prime}\},$$

$$Q_-(n)=\min\{q:q\text{ prime},\ q<2n-1,\ n^2-q\text{ prime}\}.$$

Set the value to $\infty$ if the set is empty. Thus the conjectures assert that both quantities are finite for every even $n\ge2$. This convention avoids silently assuming the existence we are investigating.

For $n=2$, the upper witness is $q=3$, giving 7, and the lower witness is $q=2$, giving 2. This exceptional role of the even prime must be retained in implementations. For even $n\ge4$, $q=2$ fails in both directions because $n^2\pm2$ is an even number greater than 2.

## 2. A conditional implication for Legendre's conjecture

**Proposition 1.** If both prime-offset conjectures hold, every interval $(m^2,(m+1)^2)$ with integer $m\ge1$ contains a prime.

**Proof.** If $m$ is even, apply the upper conjecture at $n=m$. Its prime lies strictly between $m^2$ and $m^2+2m+1=(m+1)^2$. If $m$ is odd, apply the lower conjecture at the even integer $n=m+1$. Its prime lies strictly between $n^2-(2n-1)=(n-1)^2=m^2$ and $n^2=(m+1)^2$. This includes $m=1$ through the lower witness at $n=2$. $\square$

This proves an implication between conjectures, not an unconditional prime-existence theorem. The converse has not been established here: Legendre's conjecture does not specify that the displacement from the even square must itself be prime.

The equations $p-q=n^2$ and $p+q=n^2$ also connect the questions to prime differences and Goldbach representations. Such connections do not supply the required small offset. In particular, an unrestricted representation of $n^2$ as a sum of two primes need not put either summand below $2n-1$. Throughout, Goldbach and prime-pair assertions remain conjectural. The term Polignac's conjecture usually adds the requirement that the two primes be consecutive, whereas this project imposes no such requirement.

## 3. Elementary obstructions

**Proposition 2.** Let $n\ge4$ be even and $q$ a prime divisor of $n$. Then neither $n^2+q$ nor $n^2-q$ is prime.

**Proof.** Both expressions are divisible by $q$. Moreover, $q\le n$ and $n^2-q\ge n^2-n>n\ge q$, so both are strictly greater than $q$. $\square$

This gives a simple justified optimization: discard prime offsets dividing $n$, after treating $n=2$ separately.

**Proposition 3.** For every real $B\ge2$, there are infinitely many even integers $n$ for which every prime offset $q\le B$ fails in both directions.

**Proof.** Let $P$ be the product of all primes at most $B$. Choose any positive multiple $n=kP$ with $n\ge4$. Every prime $q\le B$ divides $n$, so Proposition 2 applies. There are infinitely many such multiples. $\square$

Consequently, no fixed finite collection of prime offsets works for all even squares. Under the prime-offset conjectures, both finite minima are simultaneously larger than $B$ at these $n$. Without those conjectures, the unconditional conclusion is that every offset at most $B$ fails; it does not prove that a larger successful offset exists. This distinction matters when describing the observed minima as "bounded."

For example, $n=30$ rules out $q=2,3,5$. This construction concerns the absolute size of the offset. It does not contradict a bound that grows with $n$, such as $2n\pm1$.

**Proposition 4.** Suppose $n\ge4$ is even, $3\nmid n$, and $q>3$ lies in the relevant conjectured interval. An upper success requires $q\equiv1\pmod3$; a lower success requires $q\equiv2\pmod3$.

**Proof.** We have $n^2\equiv1\pmod3$. In the upper case, $q\equiv2$ makes $n^2+q$ divisible by 3. In the lower case, $q\equiv1$ makes $n^2-q$ divisible by 3. The resulting numbers exceed 3 within the stated intervals, so they are composite. $\square$

If $3\mid n$, neither nonzero residue class of $q$ is eliminated modulo 3, but $q=3$ is eliminated by Proposition 2. Thus the factorization of $n$ changes the local search landscape. The upper and lower directions have different permissible classes for a given $n$; a pooled plot can hide this.

## 4. A finite local-density calculation

This calculation uses modular arithmetic and finite products; no spectral theory is needed. Fix $n$ and an odd prime $\ell$. As a residue variable $a$ runs modulo $\ell$, ask that neither $a$ nor $n^2+a$ be divisible by $\ell$. The forbidden residues are $0$ and $-n^2$. They coincide if $\ell\mid n$ and are distinct otherwise. For the lower expression they are $0$ and $n^2$, with the same count.

Thus the number of forbidden residues is

$$\nu_\ell(n)=\begin{cases}1,&\ell\mid n,\\2,&\ell\nmid n.\end{cases}$$

The exact fraction of allowed residues at this modulus is $1-\nu_\ell(n)/\ell$. Relative to a model treating the two divisibility tests independently, the finite correction factor is

$$c_\ell(n)=\frac{1-\nu_\ell(n)/\ell}{(1-1/\ell)^2}=\begin{cases}\ell/(\ell-1),&\ell\mid n,\\\ell(\ell-2)/(\ell-1)^2,&\ell\nmid n.\end{cases}$$

At $\ell=2$, even $n$ gives a factor of 2. For a cutoff $y\ge2$, define

$$C_y(n)=2\prod_{\substack{3\le\ell\le y\\\ell\ \mathrm{prime}}}c_\ell(n).$$

By the Chinese remainder theorem, the allowed fraction among all residues modulo the product of these primes is exactly the product of the allowed fractions. This is an exact statement about residue classes. It does not establish equidistribution of prime candidates in a short interval, independence of primality events, or an asymptotic formula for the number of successful offsets. Also, actual primes equal to one of the small moduli are exceptions to a divisibility-based filter and must be handled separately.

This calculation varies the offset $q$ with $n$ fixed. It is distinct from fixing $q$ and counting solutions of $n^2\equiv\mp q\pmod\ell$ as $n$ varies. Both are useful, but they answer different counting questions.

## 5. What a heuristic can and cannot say

Let $H$ be a candidate offset cutoff small relative to $n^2$. There are roughly $H/\log H$ prime offsets below $H$. Ignoring congruence effects, a rough model assigns a shifted value near $n^2$ prime density $1/(2\log n)$, giving

$$\lambda_0(n,H)\approx\frac{H}{2\log n\log H}.$$

This baseline ignores parity. For odd prime $q$ and even $n$, the shifted number is already odd; the parity-adjusted baseline doubles the expression. The finite factors in Section 4 provide a transparent way to explore additional local corrections, but they do not turn the model into a theorem.

Setting a modeled expected count near one suggests a *typical first-offset scale* of order $\log n\log\log n$, up to local and constant factors. The maximum over many $n$ is a different statistic and can be much larger. A finite record plot alone cannot establish $O((\log n)^2)$ growth, a limiting law, or a surprising failure of a random model. A defensible experiment reports means, quantiles, and records separately.

Taking $H$ near $2n$ gives a modeled expected count growing roughly like $n/(\log n)^2$. This is motivation for the conjectures, not a proof. A growing expectation alone does not imply that the probability of zero tends to zero: a random variable equal to 0 with probability one half and $2n$ with probability one half has expectation $n$ but a fixed zero probability. An estimate such as $e^{-\lambda}$ for no successes requires an additional independence or Poisson assumption, which is not proved here. Even a vanishing modeled failure probability would not establish the claim for every even integer.

## 6. Reproducible computation

The supplied program performs an exact sieve up to $(10000+1)^2$, then searches the bounded prime offsets for every even $n$ from 2 through 10,000. An independently implemented trial-division routine checks all resulting witnesses and all smaller prime offsets, validating minimality as well as existence.

| Statistic | Upper offsets | Lower offsets |
|---|---:|---:|
| Even inputs checked | 5,000 | 5,000 |
| Failures in the bounded search | 0 | 0 |
| Maximum minimum offset | 397 | 467 |
| Input attaining that maximum | 6,046 | 8,968 |
| Mean minimum offset | 27.8088 | 22.3494 |
| Median minimum offset | 13 | 11 |
| 95th percentile (nearest rank) | 97 | 83 |

The full data and successive records accompany the code. The source manuscript reports a much larger run to $10^8$, with maxima 2,797 and 2,543. The original implementation and raw output are unavailable; those historical figures are excluded from the reproducible dataset and the results established here.

## 7. A larger lower-side range from published computations

The lower conjecture holds for every even $n\le2\times10^9$ as a corollary of the published minimal Goldbach-partition computation of Oliveira e Silva, Herzog, and Pardi, together with our small-case check. For $n\ge4892$, their bound supplies $q\le9781<2n-1$; their range covers $n^2\le4\times10^{18}$. See [the full deduction and source](LITERATURE_BOUND.md). This conclusion uses their computation, not the missing historical code. It gives no analogous upper-side bound.

## 8. Next mathematical questions

Useful further experiments include grouping offsets by $n\bmod30$, separating typical values from record values, and comparing candidate counts with and without the finite correction $C_y(n)$. Such comparisons would quantify deviations from the heuristic model. Scaling to $10^8$ would require a memory-efficient implementation with a justified primality test, restartable batches, and saved outputs.

The contribution of this project is a precise question, elementary structural analysis, and a transparent finite experiment. The universal prime-offset conjectures and asymptotic growth of their minima remain open.

## References and provenance

- Mohammad Aldebbeh, *A Symmetrical Strengthening of Legendre's Conjecture Anchored on Even Squares*, March 21, 2026, five-page manuscript.
- János Pintz, [On the singular series in the prime k-tuple conjecture](https://arxiv.org/abs/1004.1084), 2010. Advanced background on singular series, not a prerequisite or a claimed source of a bound for the present problem.
- All propositions and finite local calculations above include their complete arguments. The finite correction is an instance of standard prime-pair local-density reasoning, applied here to the offset variable.
