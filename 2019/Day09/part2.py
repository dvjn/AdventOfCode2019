import sys
from part1 import run_intcode


def main():
    with open(sys.argv[1], "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        runner = run_intcode(intcode)
        next(runner)
        print(runner.send("2"))


if __name__ == "__main__":
    main()
