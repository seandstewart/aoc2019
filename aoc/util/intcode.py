#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import dataclasses
import enum
import operator
from typing import List, Callable, Mapping, Tuple
from typing_extensions import TypedDict


class OpCode(enum.IntEnum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    JIT = 5
    JIF = 6
    FLT = 7
    FEQ = 8
    STOP = 99


class ParamMode(enum.IntEnum):
    POS = 0
    IMM = 1


@dataclasses.dataclass
class Instruction:
    code: OpCode
    C: ParamMode = ParamMode.POS
    B: ParamMode = ParamMode.POS
    A: ParamMode = ParamMode.POS

    def __post_init__(self):
        self.index = (self.C, self.B, self.A)

    @classmethod
    def from_str(cls, string: str) -> "Instruction":
        """Take an instruction written right -> left and parse it."""
        return cls(
            OpCode(int(string[-2:])),
            *(ParamMode(int(i)) for i in reversed(string[:-2])),
        )

    def __iter__(self):
        return iter(self.index)

    def __getitem__(self, item: int) -> ParamMode:
        return self.index[item]


class OpConfig(TypedDict, total=False):
    op: Callable[..., int]
    adix: int


COMPUTE: Mapping[OpCode, OpConfig] = {
    OpCode.ADD: {"op": operator.add, "adix": 3},
    OpCode.MUL: {"op": operator.mul, "adix": 3},
}

IO: Mapping[OpCode, OpConfig] = {
    OpCode.IN: {"adix": 1},
    OpCode.OUT: {"adix": 1},
}


HandlerT = Callable[[Instruction, int, List[int], int], Tuple[int, int]]


@dataclasses.dataclass
class IntcodeOperator:
    array: List[int]

    def __post_init__(self):
        self.handlers: Mapping[OpCode, HandlerT] = {
            OpCode.OUT: self.io,
            OpCode.IN: self.io,
            OpCode.MUL: self.compute,
            OpCode.ADD: self.compute,
            OpCode.FLT: self.flip,
            OpCode.FEQ: self.flip,
            OpCode.JIF: self.jump,
            OpCode.JIT: self.jump,
        }

    @staticmethod
    def compute(
        instr: Instruction, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[int, int]:
        reg = COMPUTE[instr.code]
        op = reg["op"]
        stop = pos + reg["adix"]
        start = pos + 1
        store = array[stop]
        argspos = array[start:stop]
        val = op(
            *(array[p] if i == ParamMode.POS else p for p, i in zip(argspos, instr))
        )
        array[store] = val
        return 0, stop + 1

    @staticmethod
    def io(
        instr: Instruction, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[int, int]:
        reg = IO[instr.code]
        stop = pos + reg["adix"]
        start = pos + 1
        target = array[start]
        if instr.code == OpCode.IN:
            if input is None:
                raise RuntimeError(f"{instr.code}: can't proceed without input.")
            array[target] = input
            res = 0
        else:
            res = array[target]
        return res, stop + 1

    @staticmethod
    def jump(
        instr: Instruction, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[int, int]:
        a, b = (
            y if x == ParamMode.IMM else array[y]
            for x, y in zip(instr, array[pos + 1 : pos + 3])
        )
        if instr.code == OpCode.JIT and a:
            pos = b
        elif instr.code == OpCode.JIF and not a:
            pos = b
        return 0, pos

    @staticmethod
    def flip(instr: Instruction, pos: int, array: List[int], *, input: int = None):
        a, b, t = (
            y if x == ParamMode.IMM else array[y]
            for x, y in zip(instr, array[pos + 1 : pos + 4])
        )
        if instr.code == OpCode.FEQ:
            array[t] = 1 if a == b else 0
        elif instr.code == OpCode.FLT:
            array[t] = 1 if a < b else 0
        return 0, pos + 4

    def operate(
        self, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[int, int]:
        instruction = Instruction.from_str(str(array[pos]))
        return self.handlers[instruction.code](instruction, pos, array, input=input)

    def run(self, *, input: int = None) -> List[int]:
        array = self.array.copy()
        pos = 0
        try:
            while pos < len(array) and array[pos] != OpCode.STOP:
                res, pos = self.operate(pos, array, input=input)
                yield res
        except (ValueError, KeyError, IndexError) as err:
            print(err)
        yield array
