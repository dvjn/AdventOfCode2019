import os
import sys
from collections import defaultdict


def cls():
    os.system("cls" if os.name == "nt" else "clear")


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


def run_intcode(
    intcode, input_device, output_device, opcode_map=opcode_map, debug=False
):
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
            memory["input_buffer"] = next(input_device)
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
            if debug:
                print("Output Buffer:", memory["output_buffer"])
            output_device.send(memory["output_buffer"])
            del memory["output_buffer"]
        memory["ip"] += opcode_map[memory["opcode"]]["length"]
        if debug:
            print("Next IP:", memory["ip"])

    return memory["intcode"][0]


class Monitor:
    pixel_map = {0: " ", 1: "█", 2: "▒", 3: "▔", 4: "●"}

    @staticmethod
    def get_boundaries(tiles):
        min_x, max_x = float("inf"), float("-inf")
        min_y, max_y = float("inf"), float("-inf")

        for x, y in tiles:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        return min_x, max_x, min_y, max_y

    def __init__(self):
        self.screen = defaultdict(int)

    def show(self):
        min_x, max_x, min_y, max_y = Monitor.get_boundaries(self.screen.keys())
        image = "\n".join(
            "".join(str(self.screen[(i, j)]) for i in range(min_x, max_x + 1))
            for j in range(min_y, max_y + 1)
        )
        for i, pixel in Monitor.pixel_map.items():
            image = image.replace(str(i), pixel)
        cls()
        print(image)

    def set_pixel(self, x, y, value):
        self.screen[(x, y)] = value


class ScoreBoard:
    def __init__(self):
        self.score = None

    def show(self):
        print(f"Score: {self.score}" if self.score else "No Score")

    def set_score(self, score):
        self.score = score


def make_joystick(monitor):
    while True:
        ball_x = next(
            (coords[0] for coords, value in monitor.screen.items() if value == 4)
        )
        paddle_x = next(
            (coords[0] for coords, value in monitor.screen.items() if value == 3)
        )
        yield 0 if ball_x == paddle_x else -1 if ball_x < paddle_x else 1


def make_mux_output(monitor, score_board):
    while True:
        x = yield
        y = yield
        z = yield
        if x == -1 and y == 0:
            score_board.set_score(z)
        else:
            monitor.set_pixel(x, y, z)
        monitor.show()
        score_board.show()


def play_game(intcode):
    monitor = Monitor()
    score_board = ScoreBoard()
    joystick = make_joystick(monitor)
    mux_output = make_mux_output(monitor, score_board)
    next(mux_output)
    run_intcode(intcode, joystick, mux_output)


def main():
    with open(sys.argv[1], "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        intcode[0] = 2
        play_game(intcode)


if __name__ == "__main__":
    main()
