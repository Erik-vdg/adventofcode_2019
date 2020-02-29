

def is_elligible(number: int) -> bool:
    # is 6-digit number
    if not (100000 <= number <= 999999):
        return False
    numstr = str(number)

    # two adjacent digits are the same
    # from left to right, digits never decrease
    adjacent_match = False
    ascending = True
    for i in range(5):
        if numstr[i] == numstr[i+1]:
            adjacent_match = True
        if numstr[i] > numstr[i+1]:
            ascending = False
    return adjacent_match and ascending


def is_elligible_2(number: int) -> bool:
    # is 6-digit number
    if not (100000 <= number <= 999999):
        return False
    numstr = str(number)

    # two adjacent digits are the same
    # from left to right, digits never decrease
    adjacent_match = False
    ascending = True
    for i in range(5):
        if numstr[i] > numstr[i+1]:
            ascending = False
    for i in range(10):
        if str(i)*2 in numstr and str(i)*3 not in numstr:
            adjacent_match = True
    return adjacent_match and ascending


def main():
    lower_bound = 372304
    upper_bound = 847060

    valid_passwords = [x for x in range(lower_bound, upper_bound) if is_elligible(x)]
    print(f'Part 1 answer: {len(valid_passwords)}')

    valid_passwords_2 = [x for x in valid_passwords if is_elligible_2(x)]
    print(f'Part 2 answer: {len(valid_passwords_2)}')


if __name__ == '__main__':
    main()
