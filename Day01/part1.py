import sys


def calculate_fuel_requirement(mass):
    return (mass // 3) - 2


def main():
    with open(sys.argv[1], "r") as masses:
        total_fuel_requirement = sum(
            calculate_fuel_requirement(int(mass)) for mass in masses
        )

    print(total_fuel_requirement)


if __name__ == "__main__":
    main()
