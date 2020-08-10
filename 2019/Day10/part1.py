import sys
from math import degrees, atan2
from collections import namedtuple

VisibleAsteroid = namedtuple("VisibleAsteroid", ["sq_distance", "asteroid"])


class Asteriod:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visible_asteroids = dict()
        self.num_visible_asteroids = 0

    def get_angle(self, other):
        ang = degrees(atan2(self.row - other.row, self.col - other.col))
        return (ang + 270) % 360

    def get_sq_distance(self, other):
        return pow(self.row - other.row, 2) + pow(self.col - other.col, 2)

    def add_visible_asteroid(self, other):
        sq_distance = self.get_sq_distance(other)
        angle = self.get_angle(other)

        if angle in self.visible_asteroids:
            if self.visible_asteroids[angle].sq_distance < sq_distance:
                return
        else:
            self.num_visible_asteroids += 1

        self.visible_asteroids[angle] = VisibleAsteroid(sq_distance, other)

    def __repr__(self):
        return (
            "<Asteroid "
            f"row={self.row} col={self.col} "
            f"num_visible_asteroids={self.num_visible_asteroids}>"
        )


def find_best_asteroid(asteroids):
    return max(asteroids, key=lambda asteroid: asteroid.num_visible_asteroids)


def load_asteroids(space_map):
    asteroids = set(
        Asteriod(i, j)
        for i, row in enumerate(space_map)
        for j, col in enumerate(row)
        if col == "#"
    )
    for asteroid in asteroids:
        for other_asteroid in asteroids:
            if asteroid == other_asteroid:
                continue
            asteroid.add_visible_asteroid(other_asteroid)
    return asteroids


def main():
    with open(sys.argv[1], "r") as input_file:
        space_map = input_file.read().strip().split("\n")
        asteroids = load_asteroids(space_map)
        best_asteroid = find_best_asteroid(asteroids)
        print(best_asteroid.num_visible_asteroids)


if __name__ == "__main__":
    main()
