import pytest

from crypto_toy.math import extended_euclidean, is_coprime, is_prime


def test_extended_euclidean():
    assert (3, (5, -8)) == extended_euclidean(135, 84)
    assert (3, (-8, 5)) == extended_euclidean(84, 135)
    assert (2, (1, 0)) == extended_euclidean(2, 0)


def test_is_coprime():
    assert is_coprime(35, 9)
    assert is_coprime(3, 5)
    assert is_coprime(5, 1)

    assert not is_coprime(3, 3)
    assert not is_coprime(15, 12)


@pytest.mark.parametrize(
    "number",
    (
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
    ),
)
def test_is_prime_true(number):
    assert is_prime(number)


@pytest.mark.parametrize(
    "number", (-1, 0,),
)
def test_is_prime_raise(number):
    with pytest.raises(ValueError):
        is_prime(number)


@pytest.mark.parametrize(
    "number", (1, 4, 6, 8, 9, 10, 12),
)
def test_is_prime_false(number):
    assert not is_prime(number)
