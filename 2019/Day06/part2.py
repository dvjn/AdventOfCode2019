reverse_orbits = dict()


def parse_reverse_orbits():
    with open("input", "r") as input_file:
        global orbits
        for line in input_file:
            stationary, orbiter = line.strip().split(")")
            reverse_orbits[orbiter] = stationary


def get_full_orbital_path(name):
    path = [name]
    while path[-1] != "COM":
        path.append(reverse_orbits[path[-1]])
    return path


if __name__ == "__main__":
    parse_reverse_orbits()
    san_path = get_full_orbital_path("SAN")
    you_path = get_full_orbital_path("YOU")
    meeting_point = next(
        space_entity for space_entity in you_path if space_entity in san_path
    )
    jumps = you_path.index(meeting_point) + san_path.index(meeting_point) - 2
    print(jumps)
