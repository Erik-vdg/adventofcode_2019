class IntcodeException(Exception):
    pass

class UnrecognizedOpcodeError(IntcodeException):
    pass

class HaltExecutionError(IntcodeException):
    pass

class InvalidIntcodeFormatError(IntcodeException):
    pass