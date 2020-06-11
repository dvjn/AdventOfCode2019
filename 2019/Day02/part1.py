def run_intcode(intcode):
    intcode = intcode[:]
    for i in range(0, len(intcode), 4):
        if intcode[i] == 1:
            intcode[intcode[i + 3]] = intcode[intcode[i + 1]] + intcode[intcode[i + 2]]
        elif intcode[i] == 2:
            intcode[intcode[i + 3]] = intcode[intcode[i + 1]] * intcode[intcode[i + 2]]
        else:
            break
    return intcode[0]


if __name__ == "__main__":
    with open("input", "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        intcode[1:3] = 12, 2
        print(run_intcode(intcode))
