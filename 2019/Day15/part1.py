import os
import sys
from collections import defaultdict, deque
from dataclasses import dataclass

from intcode import run_intcode

UNEXPLORED = 0
DROID = 1
EMPTY = 2
WALL = 3
TARGET = 4
cell_map = {UNEXPLORED: " ", DROID: "◉", EMPTY: "░", WALL: "█", TARGET: "▢"}


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def get_boundaries(cells):
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    for cell in cells:
        if cell.x < min_x:
            min_x = cell.x
        if cell.x > max_x:
            max_x = cell.x

        if cell.y < min_y:
            min_y = cell.y
        if cell.y > max_y:
            max_y = cell.y

    return min_x, max_x, min_y, max_y


def parse_image(cells):
    min_x, max_x, min_y, max_y = get_boundaries(cells.keys())
    if isinstance(cells, defaultdict):
        safe_cells = cells
    else:
        safe_cells = defaultdict(int)
        safe_cells.update(cells)
    return [
        [safe_cells[Cell(i, j)] for i in range(min_x, max_x + 1)]
        for j in range(min_y, max_y + 1)
    ]


def draw_image(image):
    processed_image = "\n".join("".join(str(pixel) for pixel in row) for row in image)
    for i, pixel in cell_map.items():
        processed_image = processed_image.replace(str(i), pixel)
    cls()
    print(processed_image)


@dataclass(frozen=True)
class Cell:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Cell(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Cell(self.x - other.x, self.y - other.y)


move_codes = {Cell(0, -1): 1, Cell(0, 1): 2, Cell(1, 0): 3, Cell(-1, 0): 4}


def get_neighbours(cell):
    return tuple(cell + move for move in move_codes.keys())


def explore_world(droid, pretty=True):
    world_map = defaultdict(int)
    droid_position = Cell(0, 0)
    world_map[droid_position] = 2
    path = deque([droid_position])
    dead_ends = set()
    while not all(cell in dead_ends for cell in path):
        dead_neighbours = 0
        eligibility = True
        for neighbour in get_neighbours(droid_position):
            if neighbour in dead_ends:
                dead_neighbours += 1
            elif eligibility:
                if not (len(path) > 1 and path[-2] == neighbour):
                    eligibility = False
                eligible_neighbour = neighbour
        if dead_neighbours == 4:
            break
        if dead_neighbours == 3:
            dead_ends.add(droid_position)
            next(droid)
            droid.send(move_codes[eligible_neighbour - droid_position])
            droid_position = eligible_neighbour
            path.pop()
        else:
            next(droid)
            ret_status = droid.send(move_codes[eligible_neighbour - droid_position])
            if ret_status == 0:
                world_map[eligible_neighbour] = WALL
                dead_ends.add(eligible_neighbour)
            else:
                droid_position = eligible_neighbour
                world_map[droid_position] = EMPTY if ret_status == 1 else TARGET
                path.append(droid_position)
        if pretty:
            draw_image(parse_image({**world_map, droid_position: 1}))

    world_map[Cell(0, 0)] = DROID
    return world_map


def get_available_neighbours(grid, cell):
    for neighbour in get_neighbours(cell):
        if grid[neighbour] in (EMPTY, TARGET):
            yield neighbour


def get_shortest_path(grid):
    path_length = 0
    active_cells = [next(cell for cell, value in grid.items() if value == DROID)]
    explored = set()
    while not any(grid[cell] == TARGET for cell in active_cells):
        new_active_cells = set()
        for cell in active_cells:
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
        print("Shortest Path:", get_shortest_path(world_map))


if __name__ == "__main__":
    main()
