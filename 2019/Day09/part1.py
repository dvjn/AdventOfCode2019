from collections import defaultdict

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
    3: {
        "name": "in",
        "length": 2,
        "macro": "intcode[params[0]] = int(input_buffer); del input_buffer",
        "requires_input": True,
    },
    4: {
        "name": "out",
        "length": 2,
        "macro": "output_buffer = intcode[params[0]]",
        "gives_output": True,
    },
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
    9: {
        "name": "change-relative-base",
        "length": 2,
        "macro": "relative_base += int(intcode[params[0]])",
    },
}


def resolve_parameter_address(intcode, i, mode, relative_base):
    if mode == 0:
        return intcode[i]
    elif mode == 1:
        return i
    else:
        return relative_base + intcode[i]


def run_intcode(intcode, opcode_map=opcode_map, debug=False):
    memory = {
        "intcode": defaultdict(int),
        "ip": 0,
        "relative_base": 0,
    }
    memory["intcode"].update(enumerate(intcode))
    while memory["intcode"][memory["ip"]] != 99:
        memory["full_opcode"] = str(memory["intcode"][memory["ip"]]).zfill(5)
        memory["opcode"] = int(memory["full_opcode"][-2:])
        memory["n_params"] = opcode_map[memory["opcode"]]["length"] - 1
        memory["params"] = tuple(
            resolve_parameter_address(
                memory["intcode"],
                memory["ip"] + j + 1,
                int(memory["full_opcode"][-3 - j]),
                memory["relative_base"],
            )
            for j in range(memory["n_params"])
        )
        if opcode_map[memory["opcode"]].get("requires_input", False):
            memory["input_buffer"] = yield
        if debug:
            print()
            print("Opcode:", memory["full_opcode"])
            print("Params", memory["params"])
            print("Operation:", opcode_map[memory["opcode"]]["name"])
            print(
                "Param Values:",
                tuple(memory["intcode"][param] for param in memory["params"]),
            )
            if "input_buffer" in memory:
                print("Input Buffer:", memory["input_buffer"])
        exec(opcode_map[memory["opcode"]]["macro"], None, memory)
        if opcode_map[memory["opcode"]].get("gives_output", False):
            yield memory["output_buffer"]
            del memory["output_buffer"]
        if debug:
            if "output_buffer" in memory:
                print("Output Buffer:", memory["output_buffer"])
        memory["ip"] += opcode_map[memory["opcode"]]["length"]
        if debug:
            print("Next IP:", memory["ip"])

    return memory["intcode"][0]


if __name__ == "__main__":
    with open("input", "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        runner = run_intcode(intcode)
        next(runner)
        print(runner.send("1"))
