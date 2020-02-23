from collections import MutableSequence
from typing import List, Optional, Iterable, Union
from pathlib import Path

from .IntcodeException import HaltExecutionError, InvalidIntcodeFormatError
from .OpcodeFactory import OpcodeFactory


class IntcodeComputer(MutableSequence):
    __slots__ = ['_tape', '_head', '_opcode_factory']

    def __init__(self, tape: List[int], head: int = 0):
        self._tape = tape
        self.head = head
        self._opcode_factory = OpcodeFactory()

    @property
    def head(self) -> int:
        return self._head

    @head.setter
    def head(self, index: int) -> None:
        if 0 <= index < len(self._tape):
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
        if path.suffix != '.intcode': # type: ignore
            raise InvalidIntcodeFormatError(f'{str(path)} not an intcode file!')
        intcode_list = []
        with open(path, mode='r') as intcode_file:
            for line in intcode_file.readlines():
                intcode_list.extend([int(item) for item in line.split(',')])
        return cls(list(intcode_list), head)

    def __getitem__(self, index: Union[int, slice]):
        return self._tape[index]

    def __setitem__(self, index: Union[int, slice], value):
        self._tape[index] = value

    def __delitem__(self, index: Union[int, slice]):
        raise NotImplementedError('Delete not yet implemented')

    def __len__(self) -> int:
        return len(self._tape)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self._tape == other._tape
        else:
            return NotImplemented

    def insert(self, item, index):
        raise NotImplementedError('Insert not yet implemented')

    def __repr__(self) -> str:
        return(f'IntcodeComputer(tape={repr(self._tape)}, head={self._head})')

    def __str__(self) -> str:
        return str(self._tape)

    # TODO Make this look much better
    # def pretty_print(self) -> str:
    #    out_arr = []
        # thing = zip_longest(*[iter(self._tape)]*self._stride, fillvalue='x')
        # for grouping in thing:
        #    out_arr.append('  '.join([str(thing) for thing in grouping]))
    #    return '\n'.join(out_arr)

    def _process_at_head(self, advance_afterward: bool = True) -> Optional[int]:
        opcode_function = self._opcode_factory.create(self._tape[self.head])
        new_head, result = opcode_function.process(self._tape, self.head)
        if advance_afterward:
            self.head = new_head
        return result

    def process(self) -> None:
        try:
            while True:
                result = self._process_at_head()
                if result is not None:
                    # Right now we are just printing, but maybe we can do something else?
                    # i.e. save to a file
                    print(result)
        except HaltExecutionError:
            pass
