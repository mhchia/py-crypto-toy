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


def test_multiplicative_group_generator():
    g = MultiplicativeElement(23, 2)
    assert g.is_cyclic()
    cur = g
    identity = g.identity
    elements = [identity]
    while cur != identity:
        print(cur)
        elements.append(cur)
        cur = cur.operate(g)
    print(elements)
