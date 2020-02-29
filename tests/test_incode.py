import pytest
import sys
import os
from io import StringIO

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src.intcode.IntcodeComputer import IntcodeComputer # noqa E402
from src.intcode.IntcodeException import UnrecognizedOpcodeError, HaltExecutionError, InvalidIntcodeFormatError # noqa E402


def test_add():
    test_tape = [1, 0, 0, 3]
    ic = IntcodeComputer(test_tape)
    ic._process_at_head(advance_afterward=False)
    assert ic._tape == [1, 0, 0, 2]


def test_multiply():
    test_tape = [2, 0, 0, 3]
    ic = IntcodeComputer(test_tape)
    ic._process_at_head(advance_afterward=False)
    assert ic._tape == [2, 0, 0, 4]


def test_halt():
    with pytest.raises(HaltExecutionError):
        test_tape = [99]
        ic = IntcodeComputer(test_tape)
        ic._process_at_head(advance_afterward=False)


def test_unrecognized_opcode():
    with pytest.raises(UnrecognizedOpcodeError):
        test_tape = [98, 0, 0, 0]
        ic = IntcodeComputer(test_tape)
        ic._process_at_head(advance_afterward=False)


def test_integration_day2():
    test_tape = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    ic = IntcodeComputer(test_tape)
    ic.process()
    assert ic._tape == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]


def test_input(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('123\n'))

    test_tape = [3, 0, 99]
    ic = IntcodeComputer(test_tape)
    ic.process()
    assert ic._tape == [123, 0, 99]


def test_invalid_input(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('a\n'))

    with pytest.raises(InvalidIntcodeFormatError):
        test_tape = [3, 0, 99]
        ic = IntcodeComputer(test_tape)
        ic.process()


def test_output(capsys):
    test_tape = [4, 0, 99]
    ic = IntcodeComputer(test_tape)
    ic.process()
    out, err = capsys.readouterr()
    assert out == '4\n'


def test_parameter():
    test_tape = [1002, 4, 3, 4, 33]
    ic = IntcodeComputer(test_tape)
    ic.process()
    assert ic._tape == [1002, 4, 3, 4, 99]
