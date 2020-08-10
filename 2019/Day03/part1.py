import sys
from collections import defaultdict, namedtuple


Cell = namedtuple("Cell", ["x", "y"])

move_map = {"R": Cell(1, 0), "L": Cell(-1, 0), "U": Cell(0, 1), "D": Cell(0, -1)}


def move(cell, move_key):
    move_delta = move_map[move_key]
    return Cell(cell.x + move_delta.x, cell.y + move_delta.y)


def get_visited_cells(start_point, move_code):
    visited_cells = [start_point]
    for _ in range(int(move_code[1:])):
        visited_cells.append(move(visited_cells[-1], move_code[0]))
    return visited_cells[1:]


def get_intersections(wires):
    wires_visited = defaultdict(lambda: [False] * len(wires))

    for i, wire in enumerate(wires):
        current_position = Cell(0, 0)
        for move_code in wire:
            visited_cells = get_visited_cells(current_position, move_code)
            current_position = visited_cells[-1]
            for visited_cell in visited_cells:
                wires_visited[visited_cell][i] = True

    return [cell for cell, visited in wires_visited.items() if all(visited)]


def get_distance(cell1, cell2=Cell(0, 0)):
    return abs(cell1.x - cell2.x) + abs(cell1.y + cell2.y)


def main():
    with open(sys.argv[1], "r") as input_file:
        wires = [wire.split(",") for wire in input_file]
        intersections = get_intersections(wires)
        closest_intersection = min(intersections, key=get_distance)
        print(get_distance(closest_intersection))


if __name__ == "__main__":
    main()
