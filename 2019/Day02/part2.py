import sys
from itertools import product

from part1 import run_intcode


def main():
    with open(sys.argv[1], "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]

        for noun, verb in product(range(100), range(100)):
            intcode[1:3] = noun, verb

            if run_intcode(intcode) == 19690720:
                print(100 * noun + verb)
                break


if __name__ == "__main__":
    main()
