from itertools import permutations

from part1 import run_intcode

if __name__ == "__main__":
    with open("input", "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]
        max_signal = 0
        for sequence in permutations(range(5, 10)):
            amps = tuple(run_intcode(intcode) for _ in range(5))
            amps_stopped = [False] * 5
            last_output = 0
            for amp, phase in zip(amps, sequence):
                next(amp)
                amp.send(phase)
            while not all(amps_stopped):
                for i, amp in enumerate(amps):
                    try:
                        last_output = amp.send(last_output)
                        next(amp)
                    except StopIteration:
                        amps_stopped[i] = True
            if last_output > max_signal:
                max_signal = last_output
        print(max_signal)
