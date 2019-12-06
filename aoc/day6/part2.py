#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
--- Part Two ---

Now, you just need to figure out how many orbital transfers you (YOU)
need to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the
object SAN is orbiting. An orbital transfer lets you move from any
object to an object orbiting or orbited by that object.

For example, suppose you have the following map:

    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN

Visually, the above map of orbits looks like this:

                              YOU
                             /
            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around
I. To move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

Afterward, the map of orbits looks like this:

            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I - SAN
                     \
                      YOU

What is the minimum number of orbital transfers required to move from
the object YOU are orbiting to the object SAN is orbiting? (Between
the objects they are orbiting - not between YOU and SAN.)
"""
from typing import Iterator, Set

from aoc.day6.part1 import INPUT1, parse_map, stream_path


def stream_intersections(a: str, b: str, mapping: dict) -> Iterator[str]:
    """Manually iterate over the path streams for targets a & b.

    Yield any new intersections which are detected.
    """
    # Two forms of state, 'seen' & 'sent'
    # Everything we see is put in 'seen'
    # Only things yielded are put in 'sent'
    seen = set()
    sent = set()
    # We're also tracking when we exhaust the stream for each path.
    exhausted = set()
    # Create the streams.
    astream = stream_path(a, mapping)
    bstream = stream_path(b, mapping)
    while len(exhausted) < 2:
        for p, stream in ((a, astream), (b, bstream)):
            if p not in exhausted:
                try:
                    # Get the next set.
                    step = next(stream)
                    # If it's been seen but not yielded, send it out.
                    if step in seen and step not in sent:
                        sent.add(step)
                        yield step
                    # Add it to seen.
                    seen.add(step)
                # We've exhausted this path, ignore it on the next.
                except StopIteration:
                    exhausted.add(p)


def get_minimum_path(a: str, b: str, orbits: str) -> Set[str]:
    """Get the minimum number of *stops* between two points."""
    # Create the mapping
    mapping = parse_map(orbits)
    # Create the streaming path.
    istream = stream_intersections(a, b, mapping)
    try:
        # Get only the first intersection
        first = next(istream)
    except StopIteration:
        # These targets have no intersection.
        return set()
    print(f"First intersection: {first}")
    aipath = set()
    bipath = set()
    # Iterate over each path in turn and add the stops until we hit the intersection.
    for p, ipath in ((a, aipath), (b, bipath)):
        for s in stream_path(p, mapping):
            ipath.add(s)
            if s == first:
                break
    steps = aipath | bipath
    # The union of these two paths is the final result.
    return steps


def solve():
    stops = get_minimum_path("YOU", "SAN", INPUT1.read_text())
    # The question is the number of *steps*,
    # which is always the number of *stops* minus 1
    return len(stops) - 1


if __name__ == "__main__":
    print("Day 6, Part 2:", f"Minimum Jumps: {solve()}", sep="\n")
