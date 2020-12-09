import sys


def parse_reverse_orbits():
    reverse_orbits = dict()
    with open(sys.argv[1], "r") as input_file:
        for line in input_file:
            stationary, orbiter = line.strip().split(")")
            reverse_orbits[orbiter] = stationary
        return reverse_orbits


def get_full_orbital_path(name, reverse_orbits):
    path = [name]
    while path[-1] != "COM":
        path.append(reverse_orbits[path[-1]])
    return path


def main():
    reverse_orbits = parse_reverse_orbits()
    san_path = get_full_orbital_path("SAN", reverse_orbits)
    you_path = get_full_orbital_path("YOU", reverse_orbits)
    meeting_point = next(
        space_entity for space_entity in you_path if space_entity in san_path
    )
    jumps = you_path.index(meeting_point) + san_path.index(meeting_point) - 2
    print(jumps)


if __name__ == "__main__":
    main()
