#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
--- Part Two ---

An Elf just remembered one more important detail: the two adjacent
matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule,
the following are now true:

    112233 meets these criteria because the digits never decrease
        and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a
        larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than
        twice, it still contains a double 22).

How many different passwords within the range given in your puzzle
input meet all of the criteria?
"""
from collections import defaultdict

from aoc.day4.part1 import INPUT, stream_valid_passes, monotonic, PasswordT


def even_grouped_repeats(password: PasswordT) -> bool:
    """Check for at least one pair of identical digits that are not part of a larger."""
    counts = defaultdict(lambda: 1)
    prev = password[0]
    for c in password[1:]:
        if c == prev:
            counts[c] += 1
        prev = c
    return any((y for x, y in counts.items() if y == 2))


def check_password(password: PasswordT) -> bool:
    """Validate this password."""
    if not monotonic(password):
        return False
    if not even_grouped_repeats(password):
        return False

    return True


def solve():
    start, stop = (int(x) for x in INPUT.split("-"))
    return [*stream_valid_passes(start, stop, check=check_password)]


if __name__ == '__main__':
    passwords = solve()
    print(
        "Day 4, Part 2:",
        f"Found {len(passwords)} possible combinations: {passwords}",
        sep="\n"
    )
