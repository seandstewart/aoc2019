#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the
Venus refuelling station. During the rush back on Earth, the fuel
management system wasn't completely installed, so that's next on the
priority list.

Opening the front panel reveals a jumble of wires. Specifically, two
wires are connected to a central port and extend outward on a grid.
You trace the path each wire takes as it leaves the central port, one
wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths.
To fix the circuit, you need to find the intersection point closest to
the central port. Because the wires are on a grid, use the Manhattan
distance for this measurement. While the wires do technically cross
right at the central port where they both start, this point does not
count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting
from the central port (o), it goes right 8, up 5, left 5, and finally
down 3:

    ...........
    ...........
    ...........
    ....+----+.
    ....|....|.
    ....|....|.
    ....|....|.
    .........|.
    .o-------+.
    ...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6,
down 4, and left 4:

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

These wires cross at two locations (marked X), but the lower-left one
is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159

    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
"""
import dataclasses
import enum
import operator
import pathlib
import re
from collections import defaultdict
from typing import Type, TypeVar, NamedTuple, Dict, Set, Tuple

import typic

from aoc.util.helpers import manhattan_distance

DIR = pathlib.Path(__file__).parent
INPUT1: pathlib.Path = DIR / "input1.txt"


class Direction(str, enum.Enum):
    DOWN = "D"
    UP = "U"
    LEFT = "L"
    RIGHT = "R"

    def op(self, a: int, b: int) -> int:
        return OPS[self](a, b)


OPS = {
    Direction.DOWN: operator.sub,
    Direction.UP: operator.add,
    Direction.LEFT: operator.sub,
    Direction.RIGHT: operator.add,
}


V = TypeVar("V")


class Point(NamedTuple):
    x: int
    y: int


@typic.al
@dataclasses.dataclass
class Vector:
    PATTERN = re.compile(r"^(?P<direction>[UDLR])(?P<distance>\d+)$")
    direction: Direction
    distance: int

    @classmethod
    def from_str(cls: Type[V], string: str) -> V:
        match = cls.PATTERN.match(string)
        if match:
            return cls(**match.groupdict())
        raise ValueError(f"{string!r} is not a valid vector.")

    def move(self, start: Point) -> Point:
        if self.direction in {Direction.UP, Direction.DOWN}:
            return start._replace(y=self.direction.op(start.y, self.distance))
        return start._replace(x=self.direction.op(start.x, self.distance))


P = TypeVar("P")


PathT = Dict[int, Set[int]]


def path_from_str(string: str) -> PathT:
    """For our purposes a "path" is a Mapping of x-index -> y-indices."""
    start: Point = Point(0, 0)
    path: PathT = defaultdict(set)
    for vstr in string.split(","):
        # create the vector object
        v = Vector.from_str(vstr)
        # move the 'cursor'
        end = v.move(start)
        # map the values in the range between the start cursor and end cursor
        if v.direction in {Direction.UP, Direction.DOWN}:
            # For moves on the y-plane, update the y-indices for the x-index it resides
            pth = (
                range(start.y, end.y + 1)
                if v.direction == Direction.UP
                else range(end.y, start.y + 1)
            )
            path[end.x].update(pth)
        else:
            # For moves on the x-plane, add the y-index to the x-indices it resides.
            pth = (
                range(start.x, end.x + 1)
                if v.direction == Direction.RIGHT
                else range(end.x, start.x + 1)
            )
            for i in pth:
                path[i].add(end.y)
        start = end

    return path


def get_intersections(a: PathT, b: PathT) -> PathT:
    return {
        x: y for x, y in {
            k: a[k] & b[k] for k in a.keys() & b.keys()
        }.items() if y
    }


_distgetter = operator.itemgetter(1)


def get_min_intersection_from_target(
    target: Point, a: PathT, b: PathT
) -> Tuple[Point, int]:
    intersection = get_intersections(a, b)
    dists: Set[Tuple[Point, int]] = set()
    for x, ys in intersection.items():
        for y in (z for z in ys if (x, z) != target):
            p = Point(x, y)
            dists.add((p, manhattan_distance(p, target)))
    return min(dists, key=_distgetter)


def get_closest_intersection(a: str, b: str) -> Tuple[Point, int]:
    target = Point(0, 0)
    patha = path_from_str(a)
    pathb = path_from_str(b)
    intersection = get_min_intersection_from_target(target, patha, pathb)
    return intersection


def solve():
    a, b = INPUT1.read_text().splitlines()
    return get_closest_intersection(a, b)


if __name__ == '__main__':
    point, dist = solve()
    print(
        "Day 3, Part 1:",
        f"Closest intersection to (0, 0) @ {dist}: {point}",
        sep="\n"
    )
