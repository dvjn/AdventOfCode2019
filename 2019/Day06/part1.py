from collections import defaultdict

orbits = defaultdict(lambda: set())
orbit_counts = {"COM": 0}


def count_orbits_recursive(stationary, orbiter):
    stationary_count = orbit_counts.get(stationary)
    orbit_counts[orbiter] = stationary_count + 1
    if orbiter in orbits:
        for sub_orbiter in orbits[orbiter]:
            count_orbits_recursive(orbiter, sub_orbiter)


def parse_orbits():
    with open("input", "r") as input_file:
        global orbits
        for line in input_file:
            stationary, orbiter = line.strip().split(")")
            orbits[stationary].add(orbiter)


if __name__ == "__main__":
    parse_orbits()
    for orbiter in orbits["COM"]:
        count_orbits_recursive("COM", orbiter)
    print(sum(orbit_counts.values()))
