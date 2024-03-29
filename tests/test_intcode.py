#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
from aoc.util.intcode import IntcodeOperator


@pytest.mark.parametrize(
    argnames=("ops", "input", "result"),
    argvalues=[
        ([1, 0, 0, 0, 99], None, [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], None, [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], None, [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], None, [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1101, 100, -1, 4, 0], None, [1101, 100, -1, 4, 99]),
        ([1002, 4, 3, 4, 33], None, [1002, 4, 3, 4, 99]),
    ],
)
def test_intcode_operator(ops, input, result):
    assert [
        *[*IntcodeOperator.from_iter(ops).run(input, debug=True)][-1].values()
    ] == result


long_prog = [
    3,
    21,
    1008,
    21,
    8,
    20,
    1005,
    20,
    22,
    107,
    8,
    21,
    20,
    1006,
    20,
    31,
    1106,
    0,
    36,
    98,
    0,
    0,
    1002,
    21,
    125,
    20,
    4,
    20,
    1105,
    1,
    46,
    104,
    999,
    1105,
    1,
    46,
    1101,
    1000,
    1,
    20,
    4,
    20,
    1105,
    1,
    46,
    98,
    99,
]


@pytest.mark.parametrize(
    argnames=("ops", "input", "output"),
    argvalues=[
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
        (long_prog, 7, 999),
        (long_prog, 8, 1000),
        (long_prog, 9, 1001),
    ],
)
def test_jump_flip(ops, input, output):
    computer = IntcodeOperator(ops)
    out = [*computer.run(input)]
    assert out[-1] == output
