#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import dataclasses
import enum
import operator
from collections import defaultdict
from typing import (
    List,
    Callable,
    Mapping,
    Tuple,
    Iterator,
    Union,
    Optional,
    DefaultDict,
    Iterable,
    TypeVar,
    Type,
)
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

HandlerT = Callable[[int, DefaultDict[int, int], int], Tuple[int, int]]


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

    def get_args(
        self, pos: int, array: DefaultDict[int, int]
    ) -> Tuple[int, int, Iterator[int]]:
        """Get the args for an instruction."""
        start, stop = pos + 1, pos + self.adix
        argspos = [array[x] for x in range(start, stop)]
        args = (array[p] if i == ParamMode.POS else p for p, i in zip(argspos, self))
        return start, stop, args

    def compute(
        self, pos: int, array: DefaultDict[int, int], *, input: List[int] = None
    ) -> Tuple[Optional[int], int]:
        """'compute' a new value from the parameters and store it."""
        start, stop, (a, b) = self.get_args(pos, array)
        store = array[stop]
        val = self.operate(a, b)
        array[store] = val
        return None, stop + 1

    def io(
        self, pos: int, array: DefaultDict[int, int], *, input: List[int] = None
    ) -> Tuple[Optional[int], int]:
        """Store an input or send a value."""
        stop = pos + self.adix
        start = pos + 1
        if self.code == OpCode.IN:
            target = array[start]
            if not input:
                raise RuntimeError(f"{self.code}: can't proceed without input.")
            array[target] = input.pop()
            res = None
        else:
            res = array[start] if self.C == ParamMode.IMM else array[array[start]]
        return res, stop + 1

    def jump(
        self, pos: int, array: DefaultDict[int, int], *, input: List[int] = None
    ) -> Tuple[Optional[int], int]:
        """Move the pointer to a new position if a condition is met."""
        start, stop, (a, b) = self.get_args(pos, array)
        pos = b if self.operate(a) else stop
        return None, pos

    def flip(
        self, pos: int, array: DefaultDict[int, int], *, input: List[int] = None
    ) -> Tuple[int, int]:
        """Store a tiny-int of the result of a logical operation."""
        start, stop, (a, b) = self.get_args(pos, array)
        target = array[stop]
        array[target] = int(self.operate(a, b))
        return 0, stop + 1

    def execute(
        self, pos: int, array: DefaultDict[int, int], *, input: List[int] = None
    ):
        return self.handlers[self.code](pos, array, input=input)


T = TypeVar("T")


@dataclasses.dataclass
class IntcodeOperator:
    array: DefaultDict[int, int]

    @classmethod
    def from_iter(cls: Type[T], iterable: Iterable[int]) -> T:
        array = defaultdict(int, dict([*enumerate(iterable)]))
        return cls(array)

    @classmethod
    def from_str(cls: Type[T], string: str) -> T:
        return cls.from_iter((int(x) for x in string.strip().split(",")))

    @staticmethod
    def execute(
        pos: int, array: DefaultDict[int, int], *, input: List[int] = None
    ) -> Tuple[int, int]:
        instruction = Instruction.from_str(str(array[pos]))
        return instruction.execute(pos, array, input=input)

    def run(self, *input: int, debug: bool = False) -> Iterator[Union[int, List[int]]]:
        """Run the program defined by the array of ints and output any results.

        If ``debug`` is True, the final output is the state of the working memory on exit.
        """
        array = self.array.copy()
        input = [*input]
        pos = 0
        while array[pos] != OpCode.STOP:
            res, pos = self.execute(pos, array, input=input)
            if res is not None:
                yield res
        if debug:
            yield array
