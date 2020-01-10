from abc import ABC, abstractmethod, abstractproperty
from typing import Callable, Iterable
from .IntcodeException import HaltExecutionError

class Opcode(ABC):
    @abstractproperty
    def stride(self) -> int:
        return -1

    @abstractmethod
    def process(self, IntcodeTape: Iterable, *args: ...) -> Callable:
        pass


class AddOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 4
    
    def process(self, IntcodeTape: Iterable, x_idx: int, y_idx: int) -> int:
        return IntcodeTape[x_idx] + IntcodeTape[y_idx]


class MultiplyOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 4

    def process(self, IntcodeTape: Iterable, x_idx: int, y_idx: int) -> int:
        return IntcodeTape[x_idx] * IntcodeTape[y_idx]

class HaltOpcode(Opcode):
    @property
    def stride(self) -> int:
        return 1
    
    def process(self, IntcodeTape: Iterable) -> None:
        raise HaltExecutionError('Halting execution due to instruction')