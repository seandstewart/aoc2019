#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from aoc.day5.part1 import solve as part1
from aoc.day5.part2 import solve as part2


def test_part1():
    assert part1() == 5577461


def test_part2():
    assert part2() == 7161591
