#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually
need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach
each intersection; choose the intersection where the sum of both
wires' steps is lowest. If a wire visits a position on the grid
multiple times, use the steps value from the first time it visits that
position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares
the wire has entered to get to that location, including the
intersection being considered. Again consider the example from above:

    ...........
    .+-----+...
    .|.....|...
    .|..+--X-+.
    .|..|..|.|.
    .|.-X--+.|.
    .|..|....|.
    .|.......|.
    .o-------+.
    ...........

In the above example, the intersection closest to the central port is
reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20
steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes
only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of
15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an
intersection?
"""
from typing import Dict, Tuple, Set

from aoc.day3.part1 import get_intersections, stream_points, Point, _distgetter, INPUT1
from aoc.util.helpers import timer


def get_steps(string: str, inter: Set[Point]) -> Dict[Point, int]:
    """Step over the path for the given string and count.

    Return a mapping of the intersecting points and their distance from start.
    """
    steps: int = 0
    dists: Dict[Point, int] = {}
    for p in stream_points(string):
        if p in inter and p not in dists:
            dists[p] = steps
        steps += 1
    return dists


def get_min_intersection(a: str, b: str) -> Tuple[Point, int]:
    """Get the minimum intersection.

    For this we mean the least combined steps to an intersection from the origin on
    each path.
    """
    inters = get_intersections(a, b)
    asteps = get_steps(a, inters)
    bsteps = get_steps(b, inters)
    steps = ((k, asteps[k] + bsteps[k]) for k in asteps.keys() & bsteps.keys())
    return min(steps, key=_distgetter)


@timer
def solve():
    a, b = INPUT1.read_text().splitlines()
    return get_min_intersection(a, b)


if __name__ == "__main__":
    point, dist = solve()
    print(
        "Day 3, Part 2:",
        f"Shortest distance to intersection @ {point}: {dist}",
        sep="\n",
    )
