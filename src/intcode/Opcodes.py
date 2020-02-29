from abc import ABC, abstractmethod, abstractproperty
from typing import Iterable, Tuple, Optional, Type
from collections import Mapping
from .IntcodeException import HaltExecutionError, UnrecognizedOpcodeError, InvalidIntcodeFormatError


class Opcode(ABC):
    @abstractproperty
    def stride(self) -> int:
        return 0

    @abstractmethod
    def process(self, IntcodeTape: Iterable, head: int) -> Optional[Tuple[int, Optional[int]]]:
        return (head + self.stride, None)


class AddOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 4

    def process(self, IntcodeTape: Iterable, head: int) -> Tuple[int, None]:
        x_idx, y_idx, result_idx = IntcodeTape[head + 1: head + self.stride]
        IntcodeTape[result_idx] = IntcodeTape[x_idx] + IntcodeTape[y_idx]
        return (head + self.stride, None)


class MultiplyOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 4

    def process(self, IntcodeTape: Iterable, head: int) -> Tuple[int, None]:
        x_idx, y_idx, result_idx = IntcodeTape[head + 1: head + self.stride]
        IntcodeTape[result_idx] = IntcodeTape[x_idx] * IntcodeTape[y_idx]
        return (head + self.stride, None)


class InputOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 2

    def process(self, IntcodeTape: Iterable, head: int) -> Tuple[int, None]:
        result_idx = IntcodeTape[head + 1]
        try:
            input_val = input(f"Input required from position {head}: ")
            IntcodeTape[result_idx] = int(input_val)
        except ValueError:
            raise InvalidIntcodeFormatError(f'{input_val} cannot be converted to an Integer!')
        return (head + self.stride, None)


class OutputOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 2

    def process(self, IntcodeTape: Iterable, head: int) -> Tuple[int, int]:
        read_idx = IntcodeTape[head + 1]
        return (head + self.stride, IntcodeTape[read_idx])


class HaltOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 0

    def process(self, IntcodeTape: Iterable, head: int) -> None:
        raise HaltExecutionError('Halting execution due to instruction')


class OpcodeRegistry(Mapping):
    __slots__ = ['_opcode_map']

    def __init__(self):
        self._opcode_map = {
            1: AddOpcode(),
            2: MultiplyOpcode(),
            3: InputOpcode(),
            4: OutputOpcode(),
            99: HaltOpcode(),
        }

    def __getitem__(self, opcode: int) -> Type[Opcode]:
        try:
            return self._opcode_map[opcode]
        except KeyError:
            raise UnrecognizedOpcodeError(f'Unrecognized Opcode: {opcode}')

    def __iter__(self):
        return iter(self._opcode_map)

    def __len__(self):
        return len(self._opcode_map)
