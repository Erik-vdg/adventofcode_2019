from math import floor


def calc_fuel(mass: int) -> int:
    return floor(mass / 3.0) - 2


def calc_fuel_recurse(mass: int) -> int:
    if mass < 0:
        return 0
    else:
        return mass + calc_fuel_recurse(calc_fuel(mass))


def main(inputfile: str):
    with open(inputfile, 'r') as infile:
        part_1 = sum(calc_fuel(int(row)) for row in infile)
        print(f'Part 1 Answer: {part_1}')
        part_2 = sum(calc_fuel_recurse(int(row)) - int(row) for row in infile)
        print(f'Part 2 Answer: {part_2}')


if __name__ == '__main__':
    file = 'data/day_1_input.txt'
    main(file)
