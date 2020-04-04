import math
from typing import Tuple


def extended_euclidean(
    a: int, b: int, coeff_a: Tuple[int, int] = (1, 0), coeff_b: Tuple[int, int] = (0, 1)
) -> Tuple[int, Tuple[int, int]]:
    if b > a:
        a, b = b, a
        coeff_a, coeff_b = coeff_b, coeff_a
    if b == 0:
        return a, coeff_a
    r = a % b
    if r == 0:
        return b, coeff_b
    q = a // b
    coeff_r = (coeff_a[0] - q * coeff_b[0], coeff_a[1] - q * coeff_b[1])
    return extended_euclidean(b, r, coeff_b, coeff_r)


def is_coprime(a: int, b: int) -> bool:
    return 1 == math.gcd(a, b)


# A naive implementation
def is_prime(n: int) -> bool:
    if n <= 0:
        # In some definition `0` is a natural number though
        raise ValueError("n should be a natural number")
    # Quick checks
    if n == 1:
        return False
    if n in (2, 3):
        return True
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True
