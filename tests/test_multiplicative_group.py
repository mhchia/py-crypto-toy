import binascii
import hashlib
import secrets
from typing import Sequence, Tuple

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


endian = "big"
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
modulus_int = int.from_bytes(modulus_bytes, endian)
q = (modulus_int - 1) // 2
g = MultiplicativeGroupElement(modulus_int, 2)
modulus_size = 1536 // 8  # bytes


def get_random_secret() -> int:
    return secrets.randbelow(modulus_int)


def hash_to_int(*args: Sequence[int]) -> int:
    # FIXME: Check how to serialize in the spec
    # Consider 192 = 1536 // 8

    serialized_inputs = tuple(i.to_bytes(modulus_size, endian) for i in args)
    concated_input = b"".join(serialized_inputs)
    h = hashlib.sha256(concated_input)
    return int.from_bytes(h.digest(), endian)


def gen_proof_knowledge_discrete_log(
    version: int, g: MultiplicativeGroupElement, x: int, random_value: int
) -> Tuple[int, int]:
    """
    Generate the proof of knowledge of the discrete log of an element.
    I.e. given `y` we know such `x` satisfying `y = g^x`.
    """
    c = hash_to_int(version, g.exponentiate(random_value).value)
    d = (random_value - x * c) % q
    return c, d


def verify_proof_knowledge_discrete_log(
    version: int,
    c: int,
    d: int,
    g: MultiplicativeGroupElement,
    y: MultiplicativeGroupElement,
) -> bool:
    """
    Verify the proof. Given `y`, `g`, `c`, and `d`, we verify whether the proof is correct.
    """
    return c == hash_to_int(version, g.exponentiate(d).operate(y.exponentiate(c)).value)


def gen_proof_equality_discrete_coordinates(
    *,
    version: int,
    g_0: MultiplicativeGroupElement,
    g_1: MultiplicativeGroupElement,
    g_2: MultiplicativeGroupElement,
    exponent_0: int,
    exponent_1: int,
    random_value_0: int,
    random_value_1: int,
) -> Tuple[int, int, int]:
    """
    Given `g_0`, `g_1`, `g_2`, generate a proof that we know `exponent_0` and `exponent_1` such that
    `y_0 = {g_0}^{exponent_0}` and `y_1 = ({g_1}^{exponent_0})*({g_2}^{exponent_1})`.
    """
    c = hash_to_int(
        version,
        g_0.exponentiate(random_value_0).value,
        g_1.exponentiate(random_value_0)
        .operate(g_2.exponentiate(random_value_1))
        .value,
    )
    d_0 = (random_value_0 - exponent_0 * c) % q
    d_1 = (random_value_1 - exponent_1 * c) % q
    return c, d_0, d_1


def verify_proof_equality_discrete_coordinates(
    *,
    version: int,
    g_0: MultiplicativeGroupElement,
    g_1: MultiplicativeGroupElement,
    g_2: MultiplicativeGroupElement,
    y_0: MultiplicativeGroupElement,
    y_1: MultiplicativeGroupElement,
    c: int,
    d_0: int,
    d_1: int,
) -> bool:
    return c == hash_to_int(
        version,
        g_0.exponentiate(d_0).operate(y_0.exponentiate(c)).value,
        g_1.exponentiate(d_0)
        .operate(g_2.exponentiate(d_1))
        .operate(y_1.exponentiate(c))
        .value,
    )


def gen_proof_equality_discrete_log(
    version: int,
    g_0: MultiplicativeGroupElement,
    g_1: MultiplicativeGroupElement,
    exponent: int,
    random_value: int,
) -> Tuple[int, int]:
    c = hash_to_int(
        version,
        g_0.exponentiate(random_value).value,
        g_1.exponentiate(random_value).value,
    )
    d = (random_value - exponent * c) % q
    return c, d


def verify_proof_equality_discrete_log(
    version: int,
    g_0: MultiplicativeGroupElement,
    g_1: MultiplicativeGroupElement,
    y_0: MultiplicativeGroupElement,
    y_1: MultiplicativeGroupElement,
    c: int,
    d: int,
) -> bool:
    return c == hash_to_int(
        version,
        g_0.exponentiate(d).operate(y_0.exponentiate(c)).value,
        g_1.exponentiate(d).operate(y_1.exponentiate(c)).value,
    )


def test_hash_to_int():
    assert (
        hash_to_int(1)
        == 3938873202533110169729565480406493056982423978045281570761196615900255145854
    )


def test_diffie_hellman():
    a = get_random_secret()
    b = get_random_secret()
    g_a = g.exponentiate(a)
    g_b = g.exponentiate(b)
    assert g_a.exponentiate(b) == g_b.exponentiate(a)


@pytest.mark.parametrize(
    "x, y", ((5566, 7788), (5566, 5566),),
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
    # zk proofs
    r_2a, r_3a = get_random_secret(), get_random_secret()

    c_2a, d_2a = gen_proof_knowledge_discrete_log(1, g_1, a_2, r_2a)
    c_3a, d_3a = gen_proof_knowledge_discrete_log(2, g_1, a_3, r_3a)

    # Bob
    # TODO: "Check that both g2a and g3a are >= 2 and <= modulus-2", what is the "modulus" here?
    assert g_2a.value >= 2
    assert g_3a.value >= 2

    # Verify zk proofs
    assert verify_proof_knowledge_discrete_log(1, c_2a, d_2a, g_1, g_2a)
    assert verify_proof_knowledge_discrete_log(2, c_3a, d_3a, g_1, g_3a)

    b_2, b_3 = get_random_secret(), get_random_secret()
    g_2b = g_1.exponentiate(b_2)
    g_3b = g_1.exponentiate(b_3)
    g_2 = g_2a.exponentiate(b_2)
    g_3 = g_3a.exponentiate(b_3)

    r_2b, r_3b, r_4b, r_5b, r_6b = (
        get_random_secret(),
        get_random_secret(),
        get_random_secret(),
        get_random_secret(),
        get_random_secret(),
    )
    c_2b, d_2b = gen_proof_knowledge_discrete_log(3, g_1, b_2, r_2b)
    c_3b, d_3b = gen_proof_knowledge_discrete_log(4, g_1, b_3, r_3b)

    p_b = g_3.exponentiate(r_4b)
    q_b = g_1.exponentiate(r_4b).operate(g_2.exponentiate(y))
    c_pqb, d_pq0b, d_pq1b = gen_proof_equality_discrete_coordinates(
        version=5,
        g_0=g_3,
        g_1=g_1,
        g_2=g_2,
        exponent_0=r_4b,
        exponent_1=y,
        random_value_0=r_5b,
        random_value_1=r_6b,
    )

    # Alice
    # Checks
    assert g_2b.value >= 2
    assert g_3b.value >= 2
    assert p_b.value >= 2
    assert q_b.value >= 2
    # Check DH first
    assert g_2b.exponentiate(a_2) == g_2
    assert g_3b.exponentiate(a_3) == g_3
    # Verify zk-proofs
    assert verify_proof_knowledge_discrete_log(3, c_2b, d_2b, g_1, g_2b)
    assert verify_proof_knowledge_discrete_log(4, c_3b, d_3b, g_1, g_3b)
    assert verify_proof_equality_discrete_coordinates(
        version=5,
        g_0=g_3,
        g_1=g_1,
        g_2=g_2,
        y_0=p_b,
        y_1=q_b,
        c=c_pqb,
        d_0=d_pq0b,
        d_1=d_pq1b,
    )

    r_4a, r_5a, r_6a, r_7a = (
        get_random_secret(),
        get_random_secret(),
        get_random_secret(),
        get_random_secret(),
    )
    p_a = g_3.exponentiate(r_4a)
    q_a = g_1.exponentiate(r_4a).operate(g_2.exponentiate(x))
    r_a = q_a.operate(q_b.inverse()).exponentiate(a_3)
    # NOTE: Omit the proof for `p_a` and `q_a` here, since they are generated and verified
    #   in the same way as `p_b` and `q_b`.
    c_ra, d_ra = gen_proof_equality_discrete_log(
        7, g_1, q_a.operate(q_b.inverse()), a_3, r_7a,
    )

    # Bob
    # Verify zk-proofs
    assert verify_proof_equality_discrete_log(
        7, g_1, q_a.operate(q_b.inverse()), g_3a, r_a, c_ra, d_ra,
    )

    r_b = q_a.operate(q_b.inverse()).exponentiate(b_3)
    r_ab = r_a.exponentiate(b_3)

    # Alice
    assert r_b.exponentiate(a_3) == r_ab

    if x == y:
        assert r_ab == p_a.operate(p_b.inverse())
    else:
        assert r_ab != p_a.operate(p_b.inverse())
