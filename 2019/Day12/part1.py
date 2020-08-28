import sys
from dataclasses import dataclass
from itertools import combinations

from parse import parse  # pip install parse


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return n


@dataclass
class Vec3D:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Vec3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __pos__(self):
        return Vec3D(sign(self.x), sign(self.y), sign(self.z))

    def __abs__(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Moon:
    def __init__(self, x, y, z):
        self.position = Vec3D(x, y, z)
        self.velocity = Vec3D()

    @staticmethod
    def from_position_str(string):
        return Moon(*parse("<x={:d}, y={:d}, z={:d}>", string).fixed)

    @property
    def total_energy(self):
        return abs(self.position) * abs(self.velocity)

    def __repr__(self):
        return f"<Moon position={self.position} velocity={self.velocity}>"


def increment_time_step(moons):
    gravities = {moon: Vec3D() for moon in moons}
    for moon1, moon2 in combinations(moons, 2):
        gravity = +(moon2.position - moon1.position)
        gravities[moon1] += gravity
        gravities[moon2] -= gravity
    for moon, gravity in gravities.items():
        moon.velocity += gravity
        moon.position += moon.velocity


def main():
    with open(sys.argv[1], "r") as initial_positions_file:
        moons = list(
            Moon.from_position_str(initial_position.strip())
            for initial_position in initial_positions_file
        )
        for _ in range(1000):
            increment_time_step(moons)

        print(sum(moon.total_energy for moon in moons))


if __name__ == "__main__":
    main()
