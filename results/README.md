# Results and provenance

## Repository computations

`offsets.csv` contains one row for each even $2\le n\le10000$. Columns `q_plus` and `q_minus` are the least prime offsets meeting the strict bounds $q<2n+1$ and $q<2n-1$. Empty fields would mean the corresponding bounded search failed. No inputs or failures are omitted.

`records.csv` lists successive strict record minima, separately by direction. `summary.json` reports the number tested, successes, complete failure lists, maxima and their centers, means, medians, and nearest-rank 95th percentiles. Statistics would be over successes only. The SHA-256 applies to the exact UTF-8, LF-terminated bytes of `offsets.csv`.

`local_counts.csv` counts all admissible integer offset residues modulo 210 for eight stated centers. It is generated both by CRT products and by direct enumeration. `both` is the intersection of the upper and lower residue sets, not a count of prime witnesses.

Reproduction commands are in the [README](../README.md). `experiments/check_results.py` regenerates every generated file and checks the note and README tables. The complete 5,000-row dataset is small enough to retain in full. Its numerical rows are unchanged from the original repository; line endings and the summary schema have been made deterministic.

## External Goldbach input

T. Oliveira e Silva, S. Herzog and S. Pardi, *Empirical verification of the even Goldbach conjecture and computation of prime gaps up to $4\cdot10^{18}$*, **Mathematics of Computation 83** (2014), no. 288, 2033–2060.

- [DOI and publisher record](https://doi.org/10.1090/S0025-5718-2013-02787-1)
- [Author's publication record](https://sweet.ua.pt/tos/bib/4.12.html)
- [Readable copy of the published paper](https://denisevellachemla.eu/empirical-verification-of-the-even-CG.pdf)

The introduction defines the minimal Goldbach partition; Section 2.1 and Table 4 on printed page 2043 list record smaller summands over the exhaustive range. The final record is 9781. The input used here is:

> For each even $4<E\le4\cdot10^{18}$, there are primes $r,p$ with $E=r+p$ and $r\le9781$.

At an even center $4892\le n\le2\cdot10^9$, set $E=n^2$ and $q=r$. Then $n^2-q$ is prime and $q\le9781<2n-1$. Local verification covers the remaining even centers through 4890. The deduction is in Proposition 8 of the note.

The repository uses these two published summary bounds, not downloaded Goldbach data. It does not re-host the paper or third-party datasets and does not independently repeat the large verification. No external parsing code or dataset dependency is needed. The larger range is lower-side only.
