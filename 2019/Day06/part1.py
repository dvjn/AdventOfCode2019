import sys
from collections import defaultdict


def count_orbits_recursive(stationary, orbiter, orbits, orbit_counts=None):
    if not orbit_counts:
        orbit_counts = {"COM": 0}
    stationary_count = orbit_counts.get(stationary)
    orbit_counts[orbiter] = stationary_count + 1
    if orbiter in orbits:
        for sub_orbiter in orbits[orbiter]:
            orbit_counts = count_orbits_recursive(
                orbiter, sub_orbiter, orbits, orbit_counts
            )
    return orbit_counts


def parse_orbits():
    orbits = defaultdict(set)
    with open(sys.argv[1], "r") as input_file:
        for line in input_file:
            stationary, orbiter = line.strip().split(")")
            orbits[stationary].add(orbiter)
        return orbits


def main():
    orbits = parse_orbits()
    for orbiter in orbits["COM"]:
        orbit_counts = count_orbits_recursive("COM", orbiter, orbits)
    print(sum(orbit_counts.values()))


if __name__ == "__main__":
    main()
