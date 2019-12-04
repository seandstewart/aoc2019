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
import copy
import dataclasses
import enum
import operator
import pathlib
import re
from typing import Type, TypeVar, NamedTuple, Set, Tuple, Iterator

import typic

from aoc.util.helpers import manhattan_distance

DIR = pathlib.Path(__file__).parent
INPUT1: pathlib.Path = DIR / "input1.txt"


class Point(NamedTuple):
    """A single point in the path. Overloads addition for easy moves."""
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return type(self)(self.x + other.x, self.y + other.y)


class Direction(str, enum.Enum):
    DOWN = "D"
    UP = "U"
    LEFT = "L"
    RIGHT = "R"

    def move(self, p: Point) -> Point:
        return MOVES[self] + p


MOVES = {
    Direction.DOWN: Point(0, -1),
    Direction.UP: Point(0, 1),
    Direction.LEFT: Point(-1, 0),
    Direction.RIGHT: Point(1, 0),
}


V = TypeVar("V")


CENTER = Point(0, 0)


@typic.al
@dataclasses.dataclass
class Vector:
    """A representation of direction and distance."""
    PATTERN = re.compile(r"^(?P<direction>[UDLR])(?P<distance>\d+)$")
    direction: Direction
    distance: int

    @classmethod
    def from_str(cls: Type[V], string: str) -> V:
        """Extract a vector from an instruction string."""
        match = cls.PATTERN.match(string)
        if match:
            return cls(**match.groupdict())
        raise ValueError(f"{string!r} is not a valid vector.")

    def move(self, p: Point) -> Iterator[Point]:
        """Generate a series of points along this vector from a given start."""
        current = p
        for i in range(1, self.distance + 1):
            current = self.direction.move(current)
            yield current


P = TypeVar("P")


def stream_points(move_string: str) -> Iterator[Point]:
    """Stream the new points for every move in the path."""
    current = copy.copy(CENTER)
    yield current
    for vstr in move_string.split(","):
        v = Vector.from_str(vstr)
        for p in v.move(current):
            current = p
            yield current


def get_intersections(a: str, b: str) -> Set[Point]:
    """Get the intersecting points of two paths as defined by instructions."""
    intersects = {*stream_points(a)} & {*stream_points(b)}
    return intersects - {CENTER}


_distgetter = operator.itemgetter(1)


def get_closest_intersection(a: str, b: str) -> Tuple[Point, int]:
    """Find the intersection which is closest to center."""
    intersects = get_intersections(a, b)
    dists = ((x, manhattan_distance(CENTER, x)) for x in intersects)
    return min(dists, key=_distgetter)


def solve():
    """Solve part 1."""
    a, b = INPUT1.read_text().splitlines()
    return get_closest_intersection(a, b)


if __name__ == '__main__':
    point, dist = solve()
    print(
        "Day 3, Part 1:",
        f"Closest intersection to (0, 0) @ {dist}: {point}",
        sep="\n"
    )
