import sys
from collections import defaultdict
from dataclasses import dataclass
from math import ceil

from parse import parse  # pip install parse


@dataclass(frozen=True, eq=True)
class Matter:
    quantity: int
    chemical: str

    @classmethod
    def from_str(cls, string):
        return cls(*parse("{:d} {}", string.strip()).fixed)


def parse_reactions(reactions_file):
    reactions = {}
    for reaction in reactions_file:
        ingredients, product = reaction.strip().split(" => ")
        reactions[Matter.from_str(product)] = tuple(
            Matter.from_str(matter) for matter in ingredients.split(", ")
        )
    return reactions


def reduce_requirements(reactions, requirements, leftovers):
    new_requirements = defaultdict(int)
    for required_chemical, required_quantity in requirements.items():
        if required_chemical == "ORE":
            new_requirements[required_chemical] += required_quantity
            continue
        if required_chemical in leftovers and leftovers[required_chemical] > 0:
            if required_quantity < leftovers[required_chemical]:
                leftovers[required_chemical] -= required_quantity
                required_quantity = 0
            else:
                required_quantity -= leftovers[required_chemical]
                leftovers[required_chemical] = 0
        if required_quantity > 0:
            product, ingredients = next(
                reaction
                for reaction in reactions.items()
                if reaction[0].chemical == required_chemical
            )
            factor = ceil(required_quantity / product.quantity)
            if (generated_quantity := product.quantity * factor) > required_quantity:
                leftovers[required_chemical] += generated_quantity - required_quantity
            for ingredient in ingredients:
                new_requirements[ingredient.chemical] += ingredient.quantity * factor

    return new_requirements, leftovers


def get_ore_requirements(reactions, requirements):
    leftovers = defaultdict(int)

    while any(requirement != "ORE" for requirement in requirements.keys()):
        requirements, leftovers = reduce_requirements(
            reactions, requirements, leftovers
        )

    return requirements["ORE"]


def main():
    with open(sys.argv[1], "r") as reactions_file:
        reactions = parse_reactions(reactions_file)
        print(get_ore_requirements(reactions, {"FUEL": 1}))


if __name__ == "__main__":
    main()
