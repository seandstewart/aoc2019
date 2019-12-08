#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools
import time
from typing import Tuple


@functools.lru_cache(maxsize=5000)
def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def timer(func):
    @functools.wraps(func)
    def _timer(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        finish = time.time()
        print(f"Took {(finish - start) * 1000:.4f}ms")
        return res

    return _timer
