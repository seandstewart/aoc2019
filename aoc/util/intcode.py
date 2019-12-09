#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import dataclasses
import enum
import operator
from typing import List, Callable, Mapping, Tuple, Iterator, Union, Optional
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

FLIP: Mapping[OpCode, OpConfig] = {
    OpCode.FLT: {"op": operator.lt, "adix": 3},
    OpCode.FEQ: {"op": operator.eq, "adix": 3},
}

JUMP: Mapping[OpCode, OpConfig] = {
    OpCode.JIT: {"op": bool, "adix": 3},
    OpCode.JIF: {"op": lambda x: not x, "adix": 3},
}

OPERATIONS = {**COMPUTE, **IO, **FLIP, **JUMP}

HandlerT = Callable[[int, List[int], int], Tuple[int, int]]


@dataclasses.dataclass
class Instruction:
    code: OpCode
    C: ParamMode = ParamMode.POS
    B: ParamMode = ParamMode.POS
    A: ParamMode = ParamMode.POS

    def __post_init__(self):
        self.index = (self.C, self.B, self.A)
        self.operate: Optional[Callable] = OPERATIONS[self.code].get("op")
        self.adix = OPERATIONS[self.code].get("adix", 1)
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

    def get_args(self, pos: int, array: List[int]) -> Tuple[int, int, Iterator[int]]:
        start, stop = pos + 1, pos + self.adix
        argspos = array[start:stop]
        args = (array[p] if i == ParamMode.POS else p for p, i in zip(argspos, self))
        return start, stop, args

    def compute(
        self, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[Optional[int], int]:
        start, stop, (a, b) = self.get_args(pos, array)
        store = array[stop]
        val = self.operate(a, b)
        array[store] = val
        return None, stop + 1

    def io(
        self, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[Optional[int], int]:
        stop = pos + self.adix
        start = pos + 1
        if self.code == OpCode.IN:
            target = array[start]
            if input is None:
                raise RuntimeError(f"{self.code}: can't proceed without input.")
            array[target] = input
            res = None
        else:
            res = array[start] if self.C == ParamMode.IMM else array[array[start]]
        return res, stop + 1

    def jump(
        self, pos: int, array: List[int], *, input: int = None
    ) -> Tuple[Optional[int], int]:
        start, stop, (a, b) = self.get_args(pos, array)
        pos = b if self.operate(a) else stop
        return None, pos

    def flip(self, pos: int, array: List[int], *, input: int = None) -> Tuple[int, int]:
        start, stop, (a, b) = self.get_args(pos, array)
        target = array[stop]
        array[target] = int(self.operate(a, b))
        return 0, stop + 1

    def execute(self, pos: int, array: List[int], *, input: int = None):
        return self.handlers[self.code](pos, array, input=input)


@dataclasses.dataclass
class IntcodeOperator:
    array: List[int]

    @staticmethod
    def execute(pos: int, array: List[int], *, input: int = None) -> Tuple[int, int]:
        instruction = Instruction.from_str(str(array[pos]))
        return instruction.execute(pos, array, input=input)

    def run(
        self, *, debug: bool = False, input: int = None
    ) -> Iterator[Union[int, List[int]]]:
        """Run the program defined by the array of ints and output any results.

        If ``debug`` is True, the final output is the state of the working memory on exit.
        """
        array = self.array.copy()
        pos = 0
        try:
            while pos < len(array) and array[pos] != OpCode.STOP:
                res, pos = self.execute(pos, array, input=input)
                if res is not None:
                    yield res
        except (ValueError, KeyError, IndexError) as err:
            print(err)
        if debug:
            yield array
