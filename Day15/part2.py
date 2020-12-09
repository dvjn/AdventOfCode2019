import sys

from intcode import run_intcode
from part1 import (
    TARGET,
    draw_image,
    explore_world,
    get_available_neighbours,
    parse_image,
)


def get_longest_path(grid):
    path_length = 0
    active_cells = [next(cell for cell, value in grid.items() if value == TARGET)]
    explored = set()
    while len(active_cells) > 0:
        new_active_cells = set()
        for cell in active_cells:
            explored.add(cell)
            for neighbour in get_available_neighbours(grid, cell):
                if not (neighbour in explored or neighbour in active_cells):
                    new_active_cells.add(neighbour)
        active_cells = new_active_cells
        path_length += 1

    return path_length


def main():
    with open(sys.argv[1], "r") as intcode_file:
        intcode = [int(code) for code in intcode_file.read().split(",")]

        droid = run_intcode(intcode)
        world_map = explore_world(droid)
        draw_image(parse_image(world_map))
        print("Minutes to fill:", get_longest_path(world_map) - 1)


if __name__ == "__main__":
    main()
