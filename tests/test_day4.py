#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest

from aoc.day4.part1 import check_password as check1, solve as part1
from aoc.day4.part2 import check_password as check2, solve as part2


@pytest.mark.parametrize(
    argnames=("password", "valid"),
    argvalues=[
        ("111111", True),
        ("122345", True),
        ("111123", True),
        ("135679", False),
        ("223450", False),
        ("123789", False),
    ]
)
def test_check1(password, valid):
    assert check1(password) is valid


def test_part1():
    assert len(part1()) == 466


@pytest.mark.parametrize(
    argnames=("password", "valid"),
    argvalues=[
        ("111111", False),
        ("122345", True),
        ("111123", False),
        ("135679", False),
        ("223450", False),
        ("123789", False),

    ]
)
def test_check2(password, valid):
    assert check2(password) is valid


def test_part2():
    assert len(part2()) == 292
