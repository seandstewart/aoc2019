#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from aoc.day2.part1 import reproduce_1202
from aoc.day2.part2 import locate_instruction


def test_part1():
    assert reproduce_1202()[0] == 3790645


def test_part2():
    assert locate_instruction(19690720) == 6577
