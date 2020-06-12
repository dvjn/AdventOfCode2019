def is_valid_password(number):
    number_str = "0" + str(number) + "a"
    same_adjacent_digits = False
    for i in range(1, len(number_str)):
        if number_str[i] < number_str[i - 1]:
            return False

        if (
            i > 2
            and number_str[i] != number_str[i - 1]
            and number_str[i - 1] == number_str[i - 2]
            and number_str[i - 2] != number_str[i - 3]
        ):
            same_adjacent_digits = True

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
