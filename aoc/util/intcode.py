#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import dataclasses
import enum
import operator
from typing import List, Callable, Mapping
from typing_extensions import TypedDict


class OpCode(enum.IntEnum):
    ADD = 1
    MUL = 2
    STOP = 99


class OpReg(TypedDict):
    op: Callable[..., int]
    adix: int


OPS: Mapping[OpCode, OpReg] = {
    OpCode.ADD: {"op": operator.add, "adix": 3},
    OpCode.MUL: {"op": operator.mul, "adix": 3},
}


@dataclasses.dataclass
class IntcodeOperator:
    array: List[int]

    @staticmethod
    def operate(pos: int, array: List[int]) -> int:
        code = array[pos]
        reg = OPS[OpCode(code)]
        op = reg["op"]
        stop = pos + reg["adix"]
        store = array[stop]
        argspos = array[pos + 1:stop]
        res = op(*(array[i] for i in argspos))
        array[store] = res
        return stop + 1

    def run(self) -> List[int]:
        array = self.array.copy()
        pos = 0
        try:
            while pos < len(array) and array[pos] != OpCode.STOP:
                pos = self.operate(pos, array)
        except (ValueError, KeyError, IndexError) as err:
            print(err)
        return array
