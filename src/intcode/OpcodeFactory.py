from abc import ABC, abstractmethod
from enum import IntEnum, unique
from typing import Type, Iterable, Tuple, List, MutableSequence, Dict, TypeVar
from .IntcodeException import UnrecognizedOpcodeError, HaltExecutionError, InvalidIntcodeFormatError

@unique
class OpcodeType(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    HALT = 99


class OpcodeBase(ABC):
    # All Opcodes subclass from this Base Opcode
    # The __init_subclass__ method automatically registers each subclassed opcode to the OpcodeFactory

    def __init_subclass__(cls, opcode_value: OpcodeType, **kwargs):
        super().__init_subclass__(**kwargs) # type: ignore
        OpcodeFactory.register_opcode(opcode_value, cls)

    @abstractmethod
    def __init__(self, params: List[int]):
        pass

    @abstractmethod
    def process(self, tape: MutableSequence, head: int):
        pass

class OpcodeFactory(object):

    _opcode_registry: Dict[OpcodeType, Type[OpcodeBase]] = {}

    @classmethod
    def register_opcode(cls, opcode_value: OpcodeType, opcode: Type[OpcodeBase]) -> None:
        if opcode_value in OpcodeType and opcode_value not in cls._opcode_registry.keys():
            cls._opcode_registry[opcode_value] = opcode
        else:
            raise UnrecognizedOpcodeError(f'Opcode Value of {opcode_value} is not recognized!')

    @classmethod
    def create(cls, opcode_value: int) -> OpcodeBase:
        val, params = split_into_opcode_and_parameters(opcode_value)
        try:
            opcode = cls._opcode_registry[val]
            return opcode(params=params)
        except KeyError as err:
            raise UnrecognizedOpcodeError(f'Opcode Value of {opcode_value} is not recognized!') from err


class AddOpcode(OpcodeBase, opcode_value=OpcodeType.ADD):
    stride = 4

    def __init__(self, params=None):
        if params is None:
            params = [0, 0, 0]
        elif len(params) < 3:
            params += [0] * (3 - len(params))
        self.params = params

    def process(self, tape: MutableSequence, head: int) -> Tuple[int, None]:
        x_idx, y_idx, result_idx = tape[head + 1: head + AddOpcode.stride]
        if self.params[0] == 0:
            x_val = tape[x_idx]
        elif self.params[0] == 1:
            x_val = x_idx
        if self.params[1] == 0:
            y_val = tape[y_idx]
        elif self.params[1] == 1:
            y_val = y_idx
        tape[result_idx] = x_val + y_val
        return (head + self.stride, None)


class MultiplyOpcode(OpcodeBase, opcode_value=OpcodeType.MULTIPLY):
    stride = 4

    def __init__(self, params=None):
        if params is None:
            params = [0, 0, 0]
        elif len(params) < 3:
            params += [0] * (3 - len(params))
        self.params = params

    def process(self, tape: MutableSequence, head: int) -> Tuple[int, None]:
        x_idx, y_idx, result_idx = tape[head + 1: head + MultiplyOpcode.stride]
        if self.params[0] == 0:
            x_val = tape[x_idx]
        elif self.params[0] == 1:
            x_val = x_idx
        if self.params[1] == 0:
            y_val = tape[y_idx]
        elif self.params[1] == 1:
            y_val = y_idx
        tape[result_idx] = x_val * y_val
        return (head + self.stride, None)


class InputOpcode(OpcodeBase, opcode_value=OpcodeType.INPUT):
    stride = 2

    def __init__(self, params=None):
        if params is None:
            params = [0]
        self.params = params

    def process(self, tape: MutableSequence, head: int) -> Tuple[int, None]:
        result_idx = tape[head + 1]
        try:
            input_val = input(f"Input required from position {head}: ")
            tape[result_idx] = int(input_val)
        except ValueError as err:
            raise InvalidIntcodeFormatError(f'{input_val} cannot be converted to an Integer!') from err
        return (head + self.stride, None)


class OutputOpcode(OpcodeBase, opcode_value=OpcodeType.OUTPUT):
    stride = 2

    def __init__(self, params=None):
        if params is None:
            params = [0]
        self.params = params

    def process(self, tape: MutableSequence, head: int) -> Tuple[int, int]:
        if self.params[0] == 0:
            read_val = tape[tape[head + 1]]
        elif self.params[0] == 1:
            read_val = tape[head + 1]
        return (head + self.stride, read_val)


class HaltOpcode(OpcodeBase, opcode_value=OpcodeType.HALT):
    stride = 0

    def __init__(self, params=None):
        if params is None:
            params = [0]
        self.params = params
    
    def process(self, tape: MutableSequence, head:int) -> None:
        raise HaltExecutionError('Halting execution due to instruction')

def split_into_opcode_and_parameters(opcode_val: int) -> Tuple[OpcodeType, List[int]]:
    opcode = OpcodeType(opcode_val % 100)
    parameters = [int(p) for p in str(opcode_val // 100)][::-1]
    return (opcode, parameters)
