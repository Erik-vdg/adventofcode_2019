from math import floor


def calc_fuel(mass: int) -> int:
    return floor(mass / 3.0) - 2


def calc_fuel_recurse(mass: int) -> int:
    if mass < 0:
        return 0
    else:
        return mass + calc_fuel_recurse(calc_fuel(mass))

def main(inputfile: str, recurse: bool):
    with open(inputfile, 'r') as infile:
        if recurse:
            print(sum(calc_fuel_recurse(int(row)) - int(row) for row in infile))
        else:
            print(sum(calc_fuel(int(row)) for row in infile))


if __name__ == '__main__':
    file = 'data/day_1_input.txt'
    main(file, True)

    # Should return 2
    #print(calc_fuel_recurse(14) - 14)
    # Should return 966
    #print(calc_fuel_recurse(1969) - 1969)
    # Should return 50346
    #print(calc_fuel_recurse(100756) - 100756)
        