from .abc import GroupElement
from .math import extended_euclidean, is_coprime


class MultiplicativeGroupElement(GroupElement):
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
        return f"<MultiplicativeGroupElement {self.value} (mod {self.n})>"

    @property
    def identity(self) -> 'MultiplicativeGroupElement':
        return self.__class__(self.n, 1)

    def operate(self, other: "MultiplicativeGroupElement") -> "MultiplicativeGroupElement":
        new_value = (self.value * other.value) % self.n
        return self.__class__(self.n, new_value)

    def inverse(self) -> "MultiplicativeGroupElement":
        gcd, coeff = extended_euclidean(self.value, self.n)
        # Sanity check
        if gcd != 1:
            raise ValueError(f"value={self.value} must be coprime to n={self.n}")
        return self.__class__(self.n, coeff[0])

    def exponentiate(self, exponent: int) -> "MultiplicativeGroupElement":
        # Ref: https://en.wikipedia.org/wiki/Exponentiation_by_squaring#Basic_method
        cur_base = self
        y = self.identity
        if exponent < 0:
            cur_base = cur_base.inverse()
            exponent *= - 1
        if exponent == 0:
            return self.identity
        while exponent > 1:
            if exponent % 2 == 0:
                cur_base = cur_base.operate(cur_base)
                exponent //= 2
            else:
                y = cur_base.operate(y)
                cur_base = cur_base.operate(cur_base)
                exponent = (exponent - 1) // 2
        return y.operate(cur_base)
