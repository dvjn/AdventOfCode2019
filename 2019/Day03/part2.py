import sys

from part1 import Cell, get_intersections, get_visited_cells


def get_min_steps(wires):
    intersections = get_intersections(wires)

    steps_to_intersection_map = [[0 for _ in wires] for _ in intersections]

    for j, wire in enumerate(wires):
        wire_path = [Cell(0, 0)]
        visited_cells = set(wire_path)

        for move in wire:
            new_visited_cells = get_visited_cells(wire_path[-1], move)
            previously_visited_cell = next(
                (cell in visited_cells for cell in new_visited_cells), None
            )
            if previously_visited_cell:
                wire_path = wire_path[: wire_path.index(previously_visited_cell)]
                wire_path.extend(
                    new_visited_cells[
                        new_visited_cells.index(previously_visited_cell) :
                    ]
                )
            else:
                wire_path.extend(new_visited_cells)

            visited_cells.update(new_visited_cells)

            for i, intersection in enumerate(intersections):
                if intersection in new_visited_cells:
                    steps_to_intersection_map[i][j] = wire_path.index(intersection)

    return min(sum(steps) for steps in steps_to_intersection_map)


def main():
    with open(sys.argv[1], "r") as input_file:
        wires = [wire.split(",") for wire in input_file]
        print(get_min_steps(wires))


if __name__ == "__main__":
    main()
