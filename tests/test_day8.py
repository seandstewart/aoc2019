#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from aoc.day8.part1 import solve as part1
from aoc.day8.part2 import BitMap, solve as part2


@pytest.mark.parametrize(
    argnames=("string", "size", "expected"),
    argvalues=[("0222112222120000", (2, 2), "░█\n█░")],
)
def test_get_bitmap(string, size, expected):
    assert str(BitMap(*size, data=string)) == expected


def test_part1():
    assert part1() == 2159


PART2 = """░██░░░░██░████░█░░█░███░░
█░░█░░░░█░░░░█░█░░█░█░░█░
█░░░░░░░█░░░█░░████░█░░█░
█░░░░░░░█░░█░░░█░░█░███░░
█░░█░█░░█░█░░░░█░░█░█░█░░
░██░░░██░░████░█░░█░█░░█░"""


def test_part2():
    assert str(part2()) == PART2
