"""Exact arithmetic for bounded prime offsets. Standard library only."""

from math import isqrt, prod

MAX_LIMIT = 20000
SIGNS = ((1, 'q_plus'), (-1, 'q_minus'))


def sieve(limit):
    """Return primality flags for the inclusive interval [0, limit]."""
    if not isinstance(limit, int) or limit < 0:
        raise ValueError('sieve limit must be a nonnegative integer')
    flags = bytearray(b'\x01') * (limit + 1)
    flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p*p:limit+1:p] = b'\x00' * ((limit-p*p)//p + 1)
    return flags


def trial_prime(value):
    """Deterministic trial division, independent of the sieve."""
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % d for d in range(3, isqrt(value) + 1, 2))


def validate_center(n):
    if not isinstance(n, int) or n < 2 or n % 2:
        raise ValueError('n must be an even integer at least 2')


def validate_sign(sign):
    if sign not in (-1, 1):
        raise ValueError('sign must be +1 or -1')


def passes_filter(n, q, sign, moduli=(2, 3, 5, 7)):
    """Reject a shifted value only when a modulus is a proper divisor.

    The caller supplies prime q and prime moduli. Equality with a modulus
    is deliberately retained, including the lower witness at n=2.
    """
    value = n*n + sign*q
    return value >= 2 and all(value == p or value % p for p in moduli)


def minimum_offset(n, sign, primes, flags, filtered=True):
    """Search sorted prime candidates under the strict bound 2*n+sign."""
    validate_center(n)
    validate_sign(sign)
    for q in primes:
        if q >= 2*n + sign:
            break
        if filtered and not passes_filter(n, q, sign):
            continue
        if flags[n*n + sign*q]:
            return q
    return None


def search(limit):
    """Both bounded minima for every even n <= limit; round odd limits down."""
    if not isinstance(limit, int) or not 2 <= limit <= MAX_LIMIT:
        raise ValueError(f'limit must be between 2 and {MAX_LIMIT}')
    top = limit - limit % 2
    flags = sieve((top + 1)**2)
    primes = [q for q in range(2, 2*top + 1) if flags[q]]
    return [{'n': n, **{key: minimum_offset(n, sign, primes, flags)
                       for sign, key in SIGNS}}
            for n in range(2, top + 1, 2)]


def verify_rows(rows, limit):
    """Check coverage, witnesses, minimality and failures by trial division.

    No assertions: verification also runs under python -O.
    """
    top = limit - limit % 2
    if [r['n'] for r in rows] != list(range(2, top + 1, 2)):
        raise ValueError('missing, duplicated or unordered centers')
    candidates = [q for q in range(2, 2*top + 1) if trial_prime(q)]
    for row in rows:
        n = row['n']
        for sign, key in SIGNS:
            q = row[key]
            bound = 2*n + sign
            if q is not None:
                if not (isinstance(q, int) and 2 <= q < bound
                        and trial_prime(q) and trial_prime(n*n + sign*q)):
                    raise ValueError(f'invalid witness at n={n}, {key}: {q}')
            stop = q if q is not None else bound
            for earlier in candidates:
                if earlier >= stop:
                    break
                if trial_prime(n*n + sign*earlier):
                    raise ValueError(f'missed smaller witness at n={n}, {key}: {earlier}')


def validate_moduli(moduli):
    moduli = tuple(moduli)
    if len(set(moduli)) != len(moduli) or any(not isinstance(p, int) or
                                             not trial_prime(p) for p in moduli):
        raise ValueError('moduli must be distinct primes')
    return moduli


def allowed_residues(n, moduli, directions=(1,)):
    """Enumerate residues a with a and selected n^2 +/- a coprime to M."""
    validate_center(n)
    moduli = validate_moduli(moduli)
    directions = tuple(directions)
    if directions not in ((1,), (-1,), (1, -1), (-1, 1)):
        raise ValueError('choose one direction or both directions')
    period = prod(moduli)
    allowed = [a for a in range(period)
               if all(a % p and all((n*n + s*a) % p for s in directions)
                      for p in moduli)]
    return period, allowed


def local_count(n, moduli, both=False):
    """CRT product count, without enumerating a full period."""
    validate_center(n)
    moduli = validate_moduli(moduli)
    return prod(p - (1 if n % p == 0 else (3 if both else 2))
                for p in moduli)
