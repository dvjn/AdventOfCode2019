from functools import reduce
from part1 import Moon, increment_time_step

axes = ("x", "y", "z")


def get_axis_state(moons, state, axis):
    return tuple(getattr(getattr(moon, state), axis) for moon in moons)


def compute_gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def compute_lcm(x, y):
    lcm = (x * y) // compute_gcd(x, y)
    return lcm


if __name__ == "__main__":
    with open("input", "r") as initial_positions_file:
        moons = list(
            Moon.from_position_str(initial_position.strip())
            for initial_position in initial_positions_file
        )
        initial_positions = {
            axis: get_axis_state(moons, "position", axis) for axis in axes
        }
        axes_periodicity = {axis: None for axis in axes}

        i = 0
        while not all(axes_periodicity.values()):
            i += 1
            increment_time_step(moons)
            for axis in axes:
                if (
                    not axes_periodicity[axis]
                    and get_axis_state(moons, "velocity", axis) == (0, 0, 0, 0)
                    and get_axis_state(moons, "position", axis)
                    == initial_positions[axis]
                ):
                    print(f"Axis {axis} repeated at {i}")
                    axes_periodicity[axis] = i

        print(reduce(compute_lcm, axes_periodicity.values()))
