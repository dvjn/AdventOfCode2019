def is_valid_password(number):
    number_str = str(number)
    previous_digit = "0"
    same_adjacent_digits = False
    for digit in number_str:
        if digit < previous_digit:
            return False
        if digit == previous_digit:
            same_adjacent_digits = True
        previous_digit = digit

    return same_adjacent_digits


with open("input", "r") as input_file:
    lower, upper = map(int, input_file.read().split("-"))

    possibilities = 0
    number = lower
    while number <= upper:
        if is_valid_password(number):
            possibilities += 1
        number += 1

    print(possibilities)
