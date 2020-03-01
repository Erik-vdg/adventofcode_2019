from intcode.IntcodeComputer import IntcodeComputer

if __name__ == '__main__':
    ic = IntcodeComputer.from_intcode_file('data/day_5_input.intcode')
    ic.process()
