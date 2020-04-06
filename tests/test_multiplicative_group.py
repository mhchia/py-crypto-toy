from typing import Sequence

from crypto_toy.multiplicative_group import MultiplicativeGroupElement


def gen_cyclic_group(
    g: MultiplicativeGroupElement,
) -> Sequence[MultiplicativeGroupElement]:
    cur = g
    identity = g.identity
    elements = [identity]
    while cur != identity:
        elements.append(cur)
        cur = cur.operate(g)
    return elements


def test_group_element():
    mg = MultiplicativeGroupElement(35, 9)
    assert mg.inverse() == MultiplicativeGroupElement(35, 4)
    assert mg == mg.operate(mg.identity)
    identity = mg.identity
    assert identity.operate(identity) == identity
    # TODO: More test for the group properties(closed, associative, id, and inverse)?


def test_generator():
    # 5 is a generator, which should be able to generate all elements
    g = MultiplicativeGroupElement(23, 5)
    elements = gen_cyclic_group(g)
    # euler totient function
    assert len(elements) == (23 - 1)

    # Test: exponentiate
    for idx, value in enumerate(elements):
        assert g.exponentiate(idx) == value
    # negative exponentiation
    assert g.exponentiate(-3) == g.inverse().exponentiate(3)
    # 0 exponentiation
    assert g.exponentiate(0) == g.identity
