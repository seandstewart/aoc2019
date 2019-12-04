#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected
by a password. The Elves had written the password on a sticky note,
but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only
    ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).
"""
from typing import Union, List, Iterator, Generator, Callable, Any

PASSWORD_LEN = 6
INPUT = "387638-919123"

PasswordT = Union[str, List[int]]


def adjacent_repeats(password: PasswordT) -> bool:
    return any(a == b for a, b in zip(password[:-1], password[1:]))


def monotonic(password: PasswordT) -> bool:
    return not any(a > b for a, b in zip(password[:-1], password[1:]))


def check_password(password: PasswordT) -> bool:
    if not adjacent_repeats(password) or not monotonic(password):
        return False
    return True


def stream_valid_passes(
    start: int, stop: int, *, check: Callable[[PasswordT], bool] = check_password
) -> Generator[int, Any, None]:
    return (i for i in range(start, stop + 1) if check(str(i)))


def solve():
    start, stop = (int(x) for x in INPUT.split("-"))
    return [*stream_valid_passes(start, stop)]


if __name__ == "__main__":
    passwords = solve()
    print(
        "Day 4, Part 1:",
        f"Found {len(passwords)} possible combinations: {passwords}",
        sep="\n",
    )
