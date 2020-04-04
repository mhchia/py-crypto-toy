import binascii
import secrets
from typing import Sequence

import pytest

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


modulus_repr = """
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF
"""
modulus_hex_str = modulus_repr.replace(" ", "").replace("\n", "")
modulus_bytes = binascii.unhexlify(modulus_hex_str)
modulus_int = int.from_bytes(modulus_bytes, "big")
g = MultiplicativeGroupElement(modulus_int, 2)


def get_random_secret() -> int:
    return secrets.randbelow(modulus_int)


def test_diffie_hellman():
    a = get_random_secret()
    b = get_random_secret()
    g_a = g.exponentiate(a)
    g_b = g.exponentiate(b)
    assert g_a.exponentiate(b) == g_b.exponentiate(a)


@pytest.mark.parametrize(
    "x, y",
    (
        (5566, 7788),
        (5566, 5566),
    ),
)
def test_smp(x, y):
    # TODO: Add zk proofs
    # FIXME: Sometimes there are `RecursionError: maximum recursion depth exceeded in comparison`
    #   when running `extended_euclidean`.
    g_1 = g

    # Alice
    a_2, a_3 = get_random_secret(), get_random_secret()
    g_2a = g_1.exponentiate(a_2)
    g_3a = g_1.exponentiate(a_3)

    # Bob
    b_2, b_3 = get_random_secret(), get_random_secret()
    g_2b = g_1.exponentiate(b_2)
    g_3b = g_1.exponentiate(b_3)

    g_2 = g_2a.exponentiate(b_2)
    g_3 = g_3a.exponentiate(b_3)
    r = get_random_secret()
    p_b = g_3.exponentiate(r)
    q_b = g_1.exponentiate(r).operate(g_2.exponentiate(y))

    # Alice
    assert g_2b.exponentiate(a_2) == g_2
    assert g_3b.exponentiate(a_3) == g_3
    s = get_random_secret()
    p_a = g_3.exponentiate(s)
    q_a = g_1.exponentiate(s).operate(g_2.exponentiate(x))
    r_a = q_a.operate(q_b.inverse()).exponentiate(a_3)

    # Bob
    r_b = q_a.operate(q_b.inverse()).exponentiate(b_3)
    r_ab = r_a.exponentiate(b_3)

    # Alice
    assert r_b.exponentiate(a_3) == r_ab

    if x == y:
        assert r_ab == p_a.operate(p_b.inverse())
    else:
        assert r_ab != p_a.operate(p_b.inverse())
