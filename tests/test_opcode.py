import pytest
import sys
import os
from io import StringIO

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src.intcode.IntcodeComputer import IntcodeComputer # noqa E402
from src.intcode.IntcodeException import UnrecognizedOpcodeError, HaltExecutionError, InvalidIntcodeFormatError # noqa E402
from src.intcode.OpcodeFactory import OpcodeFactory, OpcodeType


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_invalid_opcode():
    with pytest.raises(UnrecognizedOpcodeError):
        OpcodeFactory.register_opcode(opcode_value=0, opcode=None)
