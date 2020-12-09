from collections import defaultdict


def add_op(memory):
    memory["intcode"][memory["params"][2]] = (
        memory["intcode"][memory["params"][0]] + memory["intcode"][memory["params"][1]]
    )
    return memory


def mul_op(memory):
    memory["intcode"][memory["params"][2]] = (
        memory["intcode"][memory["params"][0]] * memory["intcode"][memory["params"][1]]
    )
    return memory


def in_op(memory):
    memory["intcode"][memory["params"][0]] = memory["input_buffer"]
    del memory["input_buffer"]
    return memory


def out_op(memory):
    memory["output_buffer"] = memory["intcode"][memory["params"][0]]
    return memory


def jump_if_true_op(memory):
    if memory["intcode"][memory["params"][0]] != 0:
        memory["ip"] = memory["intcode"][memory["params"][1]] - 3
    return memory


def jump_if_false_op(memory):
    if memory["intcode"][memory["params"][0]] == 0:
        memory["ip"] = memory["intcode"][memory["params"][1]] - 3
    return memory


def less_than_op(memory):
    memory["intcode"][memory["params"][2]] = (
        memory["intcode"][memory["params"][0]] < memory["intcode"][memory["params"][1]]
    )
    return memory


def equals_op(memory):
    memory["intcode"][memory["params"][2]] = (
        memory["intcode"][memory["params"][0]] == memory["intcode"][memory["params"][1]]
    )
    return memory


def change_relative_base_op(memory):
    memory["relative_base"] += int(memory["intcode"][memory["params"][0]])
    return memory


opcode_map = {
    1: {"name": "add", "length": 4, "macro": add_op},
    2: {"name": "mul", "length": 4, "macro": mul_op},
    3: {"name": "in", "length": 2, "macro": in_op, "requires_input": True},
    4: {"name": "out", "length": 2, "macro": out_op, "gives_output": True},
    5: {"name": "jump-if-true", "length": 3, "macro": jump_if_true_op},
    6: {"name": "jump-if-false", "length": 3, "macro": jump_if_false_op},
    7: {"name": "less-than", "length": 4, "macro": less_than_op},
    8: {"name": "equals", "length": 4, "macro": equals_op},
    9: {"name": "change-relative-base", "length": 2, "macro": change_relative_base_op},
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
            input_buffer = yield
            memory["input_buffer"] = int(input_buffer)
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
        memory = opcode_map[memory["opcode"]]["macro"](memory)
        if opcode_map[memory["opcode"]].get("gives_output", False):
            if debug:
                print("Output Buffer:", memory["output_buffer"])
            yield memory["output_buffer"]
            del memory["output_buffer"]
        memory["ip"] += opcode_map[memory["opcode"]]["length"]
        if debug:
            print("Next IP:", memory["ip"])

    return memory["intcode"][0]
