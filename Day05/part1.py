import sys

opcode_map = {
    1: {
        "name": "add",
        "length": 4,
        "macro": "intcode[params[2]] = intcode[params[0]] + intcode[params[1]]",
    },
    2: {
        "name": "mul",
        "length": 4,
        "macro": "intcode[params[2]] = intcode[params[0]] * intcode[params[1]]",
    },
    3: {"name": "in", "length": 2, "macro": "intcode[params[0]] = int(input('in: '))"},
    4: {"name": "out", "length": 2, "macro": "print('out:', intcode[params[0]])"},
}


def resolve_parameter_address(intcode, i, mode):
    return i if int(mode) else intcode[i]


def run_intcode(intcode, opcode_map=opcode_map, debug=False):
    memory = {"intcode": intcode[:], "ip": 0}
    while memory["intcode"][memory["ip"]] != 99:
        memory["full_opcode"] = str(memory["intcode"][memory["ip"]]).zfill(5)
        memory["opcode"] = int(memory["full_opcode"][-2:])
        memory["n_params"] = opcode_map[memory["opcode"]]["length"] - 1
        memory["params"] = tuple(
            resolve_parameter_address(
                memory["intcode"], memory["ip"] + j + 1, memory["full_opcode"][-3 - j]
            )
            for j in range(memory["n_params"])
        )
        if debug:
            print()
            print("Opcode:", memory["full_opcode"])
            print("Params", memory["params"])
            print("Operation:", opcode_map[memory["opcode"]]["name"])
            print(
                "Param Values:",
                tuple(memory["intcode"][param] for param in memory["params"]),
            )
        exec(opcode_map[memory["opcode"]]["macro"], None, memory)
        memory["ip"] += opcode_map[memory["opcode"]]["length"]
        if debug:
            print("Next IP:", memory["ip"])

    return memory["intcode"][0]


def main():
    with open(sys.argv[1], "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        run_intcode(intcode)


if __name__ == "__main__":
    main()
