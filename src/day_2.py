from intcode.IntcodeComputer import IntcodeComputer
import sys


if __name__ == '__main__':
    ic = IntcodeComputer.from_intcode_file('data/day_2_input.intcode')
    ic[1] = 12
    ic[2] = 2
    ic.process()
    print(f'Part 1 Answer: {ic[0]}')

    desired_result = 19690720
    combinations = [(noun, verb) for noun in range(100) for verb in range(100)]
    for (noun, verb) in combinations:
        ic = IntcodeComputer.from_intcode_file('data/day_2_input.intcode')
        ic[1] = noun
        ic[2] = verb
        ic.process()
        if ic[0] == desired_result:
            print(f'Part 2 Answer: {noun*100 + verb}')
            break
