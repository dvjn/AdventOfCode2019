import sys
from itertools import chain, cycle, islice, repeat, starmap
from operator import mul

base_pattern = [1, 0, -1, 0]


def pattern_generator(i):
    for _ in range(i):
        yield 0
    for x in cycle(chain.from_iterable(repeat(x, i + 1) for x in base_pattern)):
        yield x


def get_pattern(n, i):
    return list(islice(pattern_generator(i), n))


def get_fft_digit(signal, pattern):
    return abs(sum(starmap(mul, zip(signal, pattern)))) % 10


def fft(signal, n):
    signal_len = len(signal)
    patterns = [get_pattern(signal_len, i) for i in range(signal_len)]

    for _ in range(n):
        signal = [get_fft_digit(signal, pattern) for pattern in patterns]

    return signal


def main():
    with open(sys.argv[1], "r") as signal_file:
        signal = [int(digit) for digit in signal_file.read().strip()]
        print("".join(map(str, fft(signal, 100)[:8])))


if __name__ == "__main__":
    main()
