#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from aoc.day1.part1 import Module as P1Module, get_total_fuel as p1_get_total_fuel
from aoc.day1.part2 import Module as P2Module, get_total_fuel as p2_get_total_fuel

import pytest


@pytest.mark.parametrize(
    argnames=("mass", "fuel"),
    argvalues=[
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ]
)
def test_p1module_fuel(mass: int, fuel: int):
    assert P1Module(mass).fuel == fuel


def test_p1_total():
    assert p1_get_total_fuel() == 3488702


@pytest.mark.parametrize(
    argnames=("mass", "fuel"),
    argvalues=[
        (12, 2),
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ]
)
def test_p2module_fuel(mass: int, fuel: int):
    assert P2Module(mass).fuel == fuel


def test_p2_total():
    assert p2_get_total_fuel() == 5230169
