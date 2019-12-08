#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
--- Part Two ---

Now you're ready to decode the image. The image is rendered by
stacking the layers and aligning the pixels with the same positions in
each layer. The digits indicate the color of the corresponding pixel:
0 is black, 1 is white, and 2 is transparent.

The layers are rendered with the first layer in front and the last
layer in back. So, if a given position has a transparent pixel in the
first and second layers, a black pixel in the third layer, and a white
pixel in the fourth layer, the final image would have a black pixel at
that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image
data 0222112222120000 corresponds to the following image layers:

    Layer 1: 02
             22

    Layer 2: 11
             22

    Layer 3: 22
             12

    Layer 4: 00
             00

Then, the full image can be found by determining the top visible pixel
in each position:

- The top-left pixel is black because the top layer is 0.
- The top-right pixel is white because the top layer is 2
  (transparent), but the second layer is 1.
- The bottom-left pixel is white because the top two layers are 2, but
  the third layer is 1.
- The bottom-right pixel is black because the only visible pixel in
  that position is 0 (from layer 4).

So, the final image looks like this:

    01
    10

What message is produced after decoding your image?
"""
import dataclasses
import enum
from typing import Mapping, Tuple

from aoc.day8.part1 import INPUT1, stream_chunks


class Pixel(enum.IntEnum):
    """A single pixel in an ascii-art image."""

    BLACK = 0
    WHITE = 1
    CLEAR = 2

    def __str__(self) -> str:
        return PMAP[self]


PMAP: Mapping[Pixel, str] = {Pixel.CLEAR: " ", Pixel.WHITE: "█", Pixel.BLACK: "░"}


@dataclasses.dataclass
class BitMap:
    """Translate an 'encoded' string into an ascii-art image."""

    width: int
    height: int
    data: str
    delim: str = "\n"

    def __post_init__(self):
        self.bitmap = self.get_bitmap(self.data, self.width, self.height)

    @staticmethod
    def get_bitmap(string: str, w: int, h: int) -> Tuple[Pixel]:
        n = w * h
        layers = [*stream_chunks(*string, n=n)]
        bitmap = []
        for i in range(n):
            for layer in layers:
                c = Pixel(int(layer[i]))
                if c != Pixel.CLEAR:
                    bitmap.append(c)
                    break
        return (*bitmap,)

    def __str__(self):
        return "\n".join(
            "".join(map(str, x)) for x in stream_chunks(*self.bitmap, n=self.width)
        )


def solve():
    return BitMap(25, 6, INPUT1.read_text().strip())


if __name__ == "__main__":
    print("Day 6, Part 2:", "Bitmap:", f"{solve()}", sep="\n")
