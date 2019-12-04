from typing import Generator


def get_input() -> Generator[str, None, None]:
    with open('input.txt', 'r') as challenge_input:
        yield from map(str.strip, challenge_input)


def calculate_total_fuel(fuel: int) -> int:
    if fuel <= 0:
        return 0
    fuel_needed = fuel // 3 - 2
    return fuel_needed + calculate_total_fuel(fuel_needed)


# Part 1
print(sum(fuel // 3 - 2 for fuel in map(int, get_input())))

# Part 2
print(sum(map(calculate_total_fuel, map(int, get_input()))))
