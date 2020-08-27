import sys
from math import ceil
from part1 import parse_reactions, get_ore_requirements


def main():
    with open(sys.argv[1], "r") as reactions_file:
        reactions = parse_reactions(reactions_file)

        ore_quantity = 1e12

        ore_per_fuel = get_ore_requirements(reactions, {"FUEL": 1})
        base_fuel_generated = int(ore_quantity // ore_per_fuel)

        fuel_generated = base_fuel_generated
        previous_ore_quantity = used_ore_quantity = fuel_generated * ore_per_fuel

        jump = ceil(base_fuel_generated // 10)

        while True:
            previous_ore_quantity, used_ore_quantity = (
                used_ore_quantity,
                get_ore_requirements(reactions, {"FUEL": fuel_generated}),
            )
            if used_ore_quantity < ore_quantity:
                if previous_ore_quantity > ore_quantity and jump == 1:
                    break
                fuel_generated += jump
            elif used_ore_quantity > ore_quantity:
                if previous_ore_quantity < ore_quantity:
                    jump = ceil(jump // 2)
                fuel_generated -= jump
            else:
                break

        print(fuel_generated)


if __name__ == "__main__":
    main()
