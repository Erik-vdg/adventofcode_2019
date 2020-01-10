import pytest
import sys
import os

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src.intcode.IntcodeComputer import IntcodeComputer
from src.intcode.IntcodeException import UnrecognizedOpcodeError, HaltExecutionError
from src.intcode.Opcodes import AddOpcode


def test_add():
    test_tape = [1,0,0,3]
    ic = IntcodeComputer(test_tape)
    ic._process_at_head(advance_afterward=False)
    assert ic._tape == [1,0,0,2]


def test_multiply():
    test_tape = [2,0,0,3]
    ic = IntcodeComputer(test_tape)
    ic._process_at_head(advance_afterward=False)
    assert ic._tape == [2,0,0,4]


def test_halt():
    with pytest.raises(HaltExecutionError):
        test_tape = [99,0]
        ic = IntcodeComputer(test_tape)
        ic._process_at_head(advance_afterward=False)


def test_unrecognized_opcode():
    with pytest.raises(UnrecognizedOpcodeError):
        test_tape = [-1,0,0,0]
        ic = IntcodeComputer(test_tape)
        ic._process_at_head(advance_afterward=False)


def test_integration_day2():
    test_tape = [1,9,10,3,2,3,11,0,99,30,40,50]
    ic = IntcodeComputer(test_tape)
    ic.process()
    assert ic._tape == [3500,9,10,70,2,3,11,0,99,30,40,50]


if __name__ == '__main__':
    test_add_opcode()
