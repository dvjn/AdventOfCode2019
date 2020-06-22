from part1 import run_intcode

if __name__ == "__main__":
    with open("input", "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        runner = run_intcode(intcode)
        next(runner)
        print(runner.send("2"))
