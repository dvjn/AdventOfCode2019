import sys
from itertools import accumulate


def main():
    with open(sys.argv[1], "r") as signal_file:
        signal_string = signal_file.read().strip()
        signal = (list(map(int, signal_string)) * 10000)[int(signal_string[:7]) :]

        for _ in range(100):
            signal = [abs(i) % 10 for i in accumulate(signal[::-1])][::-1]

        print("".join([str(x) for x in signal[:8]]))


if __name__ == "__main__":
    main()
