# Prime offsets around even squares

A number-theory investigation by **Mohammad Aldebbeh** of prime displacements from an even square. The project asks for small prime offsets on each side, proves elementary obstructions and exact residue counts, and records an independently checked finite search. Its emphasis is the bounded witness problem: which offsets work, which are ruled out, and what can be concluded from finite verification.

Read the [mathematical note (PDF)](math/note.pdf) or its [LaTeX source](math/note.tex). The [claim-status page](math/claims.md) separates proofs, computations and heuristics.

## The question

For even $n\ge2$, define

$$Q_+(n)=\min\{q:q\text{ prime},\ q<2n+1,\ n^2+q\text{ prime}\},$$
$$Q_-(n)=\min\{q:q\text{ prime},\ q<2n-1,\ n^2-q\text{ prime}\}.$$

An empty set has minimum $\infty$. The two conjectures assert finiteness for every even $n$. Each direction may use a different prime offset. The strict bounds place the shifted primes in the adjacent square gaps. At $n=2$, the minima are 3 and 2; the even-prime exception is retained.

## Proved mathematics

- Both universal offset conjectures together imply Legendre's conjecture, by treating even and odd square gaps separately. This is a conditional implication.
- For even $n\ge4$, every prime offset dividing $n$ fails on both sides. Products of small primes show that no fixed finite collection of offsets covers all even squares.
- If $3\nmid n$ and $q>3$, upper witnesses require $q\equiv1\pmod3$, lower witnesses $q\equiv2\pmod3$.
- For fixed $n$, the Chinese remainder theorem gives exact counts of locally admissible offset residues. The simultaneous count excludes $0,n^2,-n^2$ at each modulus. In particular, when $3\nmid n$, a common bounded prime witness on both sides must be $q=3$.

The note gives all proofs. The residue counts concern integer classes in a complete period; they are not counts of prime witnesses.

## Finite results

The search covers **all 5,000 even inputs $2\le n\le10\,000$**, checking existence and minimality by a sieve followed by independent trial division.

| Statistic | Upper | Lower |
|---|---:|---:|
| Failures | 0 | 0 |
| Largest minimum | 397 | 467 |
| Center of largest minimum | 6,046 | 8,968 |
| Mean | 27.8088 | 22.3494 |
| Median | 13 | 11 |
| 95th percentile, nearest rank | 97 | 83 |

The [full dataset](results/offsets.csv) retains every input, together with [records](results/records.csv), [summary and hash](results/summary.json), and [exact local counts](results/local_counts.csv).

**External computational input:** the minimal Goldbach-partition verification of Oliveira e Silva, Herzog and Pardi supplies a smaller prime summand at most 9781 for every even $4<E\le4\cdot10^{18}$. Applying it to $n^2$ for $n\ge4892$, and checking smaller even centers here, verifies the **lower** assertion through $n=2\cdot10^9$. This larger range uses their published exhaustive computation; it is not regenerated here and gives no upper-side bound. See the note, Section 6, and [data provenance](results/README.md).

The universal offset conjectures and asymptotic growth laws remain unproved. The frequency model in the note is heuristic. Earlier references to a run through $10^8$ lack reproducible code and output and are excluded from the release results.

## Reproduce

Run from the repository root with **Python 3.10 or newer** (tested with 3.12.14). No third-party Python packages or external datasets are required.

```sh
python -m unittest discover -s tests -v
python compute.py --limit 10000
python experiments/local_counts.py
python experiments/check_results.py
```

The last command regenerates both experiments in a temporary directory, compares every output byte, and checks the displayed tables. The computation keeps trial-division verification enabled even under `python -O`.

`compute.py` accepts limits from 2 to 20,000; an odd limit is rounded down. The sieve array uses about 100 MB at 10,000, with extra temporary allocations, and memory grows quadratically. Default runs overwrite the generated files in `results/`. Use `--output-dir PATH` for separate runs; both experiments accept this option. There are no random choices or timestamp-dependent outputs.

## Repository guide

| Path | Contents |
|---|---|
| `math/` | Self-contained note, PDF and claim status |
| `src/prime_offsets.py` | Sieve, bounded search, independent verifier and residue counts |
| `compute.py` | Main experiment and deterministic output writer |
| `experiments/` | Local-count experiment and reproduction/table checker |
| `tests/` | Independent finite checks and failure/edge cases |
| `results/` | Complete finite outputs and external-source provenance |

To rebuild the PDF with an existing LaTeX installation, run `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=math math/note.tex` twice. The source is standalone and uses standard LaTeX packages.

Reference: T. Oliveira e Silva, S. Herzog and S. Pardi, *Empirical verification of the even Goldbach conjecture and computation of prime gaps up to $4\cdot10^{18}$*, **Mathematics of Computation 83** (2014), 2033–2060, Section 2.1 and Table 4, p. 2043. [DOI](https://doi.org/10.1090/S0025-5718-2013-02787-1).
