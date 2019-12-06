#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest

from aoc.day6.part1 import parse_map, count_orbits, solve as part1
from aoc.day6.part2 import get_minimum_path, solve as part2


TEST1 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

TEST2 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""


@pytest.mark.parametrize(argnames=("orbits", "expected"), argvalues=[(TEST1, 42)])
def test_count_orbits(orbits, expected):
    assert count_orbits(parse_map(orbits)) == expected


def test_part1():
    assert part1() == 253104


@pytest.mark.parametrize(
    argnames=("a", "b", "orbits", "expected"),
    argvalues=[("YOU", "SAN", TEST2, {"E", "I", "K", "J", "D"})],
)
def test_get_minimum_path(a, b, orbits, expected):
    assert get_minimum_path(a, b, orbits) == expected


def test_part3():
    assert part2() == 499
