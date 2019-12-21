from typing import Iterable, List, Union, Optional
from collections import MutableSequence
from itertools import islice


class IntcodeTape(MutableSequence):
    _tape = []
    _stride = 4

    def _list_to_tape(raw_list: List, stride: int = self._stride) -> Iterable[IntcodeItem]:
        ret_array = []
        for i in range(0, len(raw_list), stride):
            ret_array.append(IntcodeItem(islice(raw_list, i, stride)))
        return ret_array

    def __init__(self, raw_list: List, stride: int = 4):
        


    # Number of IntcodeTape Items
    def __len__(self):
        return len(self._tape)

    # Get Intcode Item at location
    def __getitem__(self, index: int) -> IntcodeItem:
        return self._tape[index]

    # Set item at location
    def __setitem__(self, index: int, value: Union[IntcodeItem, List]):
        if isinstance(value, IntcodeItem):
            self._tape[index] = Value
        else:
            self._tape[index] = IntcodeItem.from_list(value)


    def __delitem__(self, index: int):
        del self._tape[index]

    def insert(self, value: Union[IntcodeItem, List], index: int):
        if isinstance(value, IntcodeItem):
            self._tape.insert(index, value)
        else:
            self._tape.insert(index, IntcodeItem.from_list(value)

    def __repr__:


class IntcodeItem(MutableMapping):
    __slots__ = ['opcode', 'input_positions', 'output_position']

    def __init__(self, opcode: int, input_positons: Optional[List[int]], output_position: Optional[int]):
        self.opcode = opcode
        self.input_positions = input_positons
        self.output_position = output_position

    @classmethod
    def from_list(self, input_list: List):
        try:
            if len(input_list == 1):
                self.__init__(opcode = input_list[0], input_positons = None, output_position = None)
            elif len(input_list == 2):
                self.__init__(opcode = input_list[0], input_positons = None, output_position = input_list[-1])
            elif len(input_list > 2):
                self.__init__(opcode = input_list[0], input_positons = input_list[1:-1], output_position = input_list[-1])
            else:
                raise ValueError('Expected an Iterable of length 1 or more')
            

    def __len__(self):
        return len(self.input_positions)

    def __get