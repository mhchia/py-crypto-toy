from .abc import GroupElement
from .math import extended_euclidean, is_coprime, is_prime


class MultiplicativeElement(GroupElement):
    n: int  # mod `n`
    value: int  # the integer value of the element

    def __init__(self, n: int, value: int) -> None:
        if not is_coprime(n, value):
            raise ValueError(f"value={value} must be coprime to n={n}")
        self.n = n
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.n == other.n and self.value == other.value

    def __repr__(self) -> str:
        return f"<MultiplicativeElement {self.value} (mod {self.n})>"

    def is_cyclic(self) -> bool:
        # This could be really slow when `n` is large
        return is_prime(self.n)

    @property
    def identity(self) -> 'MultiplicativeElement':
        return self.__class__(self.n, 1)

    def operate(self, other: "MultiplicativeElement") -> "MultiplicativeElement":
        new_value = (self.value * other.value) % self.n
        print(f"!@# new_value={new_value}")
        return self.__class__(self.n, new_value)

    def inverse(self) -> "MultiplicativeElement":
        gcd, coeff = extended_euclidean(self.value, self.n)
        # Sanity check
        if gcd != 1:
            raise ValueError(f"value={self.value} must be coprime to n={self.n}")
        return self.__class__(self.n, coeff[0])

    # TODO: How to pick a random element?
    # TODO: How to calculate k*G faster? (Probably through k = 2^0+2^1+...)
