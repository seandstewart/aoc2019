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
        ([1103, 3, 1, 0, 99], 2, [1103, 3, 1, 2, 99]),
        ([4, 3, 1, 0, 99], None, [4, 3, 1, 0, 99]),
        ([1101, 100, -1, 4, 0], None, [1101, 100, -1, 4, 99]),
        ([1002, 4, 3, 4, 33], None, [1002, 4, 3, 4, 99]),
    ],
)
def test_intcode_operator(ops, input, result):
    assert [*IntcodeOperator(ops).run(input=input)][-1] == result
