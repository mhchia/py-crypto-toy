import secrets
import binascii
from typing import Sequence

from cryptotoy.multiplicative_group import MultiplicativeElement


def gen_cyclic_group(g: MultiplicativeElement) -> Sequence[MultiplicativeElement]:
    cur = g
    identity = g.identity
    elements = [identity]
    while cur != identity:
        elements.append(cur)
        cur = cur.operate(g)
    return elements


def test_group_element():
    mg = MultiplicativeElement(35, 9)
    assert mg.inverse() == MultiplicativeElement(35, 4)
    assert mg == mg.operate(mg.identity)
    identity = mg.identity
    assert identity.operate(identity) == identity
    # TODO: More test for the group properties(closed, associative, id, and inverse)?


def test_generator():
    # 5 is a generator, which should be able to generate all elements
    g = MultiplicativeElement(23, 5)
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


def test_diffie_hellman():
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
    modulus_hex_str = modulus_repr.replace(' ', '').replace('\n', '')
    modulus_bytes = binascii.unhexlify(modulus_hex_str)
    modulus_int = int.from_bytes(modulus_bytes, 'big')
    g = MultiplicativeElement(modulus_int, 2)
    a = secrets.randbelow(modulus_int)
    b = secrets.randbelow(modulus_int)
    g_a = g.exponentiate(a)
    g_b = g.exponentiate(b)
    assert g_a.exponentiate(b) == g_b.exponentiate(a)
