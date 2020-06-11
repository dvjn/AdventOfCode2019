from part1 import calculate_fuel_requirement

if __name__ == "__main__":
    total_fuel_requirement = 0
    with open("input", "r") as masses:
        for mass in masses:
            new_fuel_requirement = calculate_fuel_requirement(int(mass))
            while new_fuel_requirement > 0:
                total_fuel_requirement += new_fuel_requirement
                new_fuel_requirement = calculate_fuel_requirement(new_fuel_requirement)

    print(total_fuel_requirement)
