import sys
from part1 import run_intcode, opcode_map

new_opcodes = {
    5: {
        "name": "jump-if-true",
        "length": 3,
        "macro": "if intcode[params[0]] != 0: ip = intcode[params[1]] - 3",
    },
    6: {
        "name": "jump-if-false",
        "length": 3,
        "macro": "if intcode[params[0]] == 0: ip = intcode[params[1]] - 3",
    },
    7: {
        "name": "less-than",
        "length": 4,
        "macro": "intcode[params[2]] = int(intcode[params[0]] < intcode[params[1]])",
    },
    8: {
        "name": "equals",
        "length": 4,
        "macro": "intcode[params[2]] = int(intcode[params[0]] == intcode[params[1]])",
    },
}

opcode_map.update(new_opcodes)


def main():
    with open(sys.argv[1], "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        run_intcode(intcode, opcode_map)


if __name__ == "__main__":
    main()
