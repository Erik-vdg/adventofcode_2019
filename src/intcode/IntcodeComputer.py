from collections import MutableSequence, Mapping
from typing import List, Optional, Callable, Iterable, Union
from itertools import zip_longest
import logging
from pathlib import Path

from .IntcodeException import UnrecognizedOpcodeError, HaltExecutionError, InvalidIntcodeFormatError
from . import Opcodes

class IntcodeComputer(MutableSequence):
    _stride = 4
    __slots__ = ['_tape', '_head', '_opcodes']


    def __init__(self, tape: List[int], head: int=0):
        self._tape = tape
        self.head = head
        self._opcodes = NewOpcodeRegistry()


    @property
    def head(self) -> int:
        return self._head


    @head.setter
    def head(self, index: int) -> None:
        if index % self._stride != 0:
            raise IndexError('Detached Head')
        elif 0 <= index < len(self._tape):
            self._head = index
        else:
            raise IndexError('Attemted to move outside of tape') 


    @classmethod
    def from_iterable(cls, iterable: Iterable[int], head: int = 0):
        return cls(list(iterable), head)


    @classmethod
    def from_intcode_file(cls, path: Union[Path, str], head: int = 0):
        if type(path) is str:
            path = Path(path)
        if path.suffix != '.intcode':
            raise InvalidIntcodeFormatError(f'{str(path)} not an intcode file!')
        intcode_list = []
        with open(path, mode='r') as intcode_file:
            for line in intcode_file.readlines():
                intcode_list.extend([int(item) for item in line.split(',')])
        return cls(list(intcode_list), head)
    
    def __getitem__(self, index: int) -> int:
        return self._tape[index]
    

    def __setitem__(self, index: int, value: int) -> None:
        self._tape[index] = value


    def __delitem__(self, index: int) -> None:
        raise NotImplementedError('Delete not yet implemented')


    def __len__(self) -> int:
        return len(self._tape)


    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self._tape == other._tape
        else:
            return NotImplemented


    def insert(self, item: int, index: int) -> None:
        raise NotImplementedError('Insert not yet implemented')


    def __repr__(self) -> str:
        return(f'IntcodeComputer(tape={repr(self._tape)}, head={self._head})')


    def __str__(self) -> str:
        return str(self._tape)


    #TODO Make this look much better
    def pretty_print(self) -> str:
        out_arr = []
        thing = zip_longest(*[iter(self._tape)]*self._stride, fillvalue='x')
        for grouping in thing:
            out_arr.append('  '.join([str(thing) for thing in grouping]))
        return '\n'.join(out_arr)


    def _process_at_head(self, advance_afterward: bool = True) -> None:
        opcode_function = self._opcodes[self._tape[self.head]]
        stride = opcode_function.stride
        operating_section = self._tape[self.head: self.head + stride]

        self._tape[operating_section[-1]] = opcode_function.process(self._tape, *operating_section[1:-1])
        if advance_afterward:
            self.head += stride

        
    def process(self, single_step: bool = False) -> None:
        try:
            while True:
                self._process_at_head()
                if single_step:
                    print(self)
                    input()
        except HaltExecutionError as e:
            pass


class NewOpcodeRegistry(Mapping):
    __slots__ = ['_opcode_map']

    def __init__(self):
        self._opcode_map = {
            1: Opcodes.AddOpcode(),
            2: Opcodes.MultiplyOpcode(),
            99: Opcodes.HaltOpcode(),
        }

    def __getitem__(self, opcode) -> Callable[[IntcodeComputer, int, int], int]:
        try:
            return self._opcode_map[opcode]
        except KeyError:
            raise UnrecognizedOpcodeError(f'Unrecognized Opcode: {opcode}')

    def __iter__(self):
        return iter(self._opcode_map)

    def __len__(self):
        return len(self._opcode_map)
