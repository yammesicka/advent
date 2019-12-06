from typing import Dict, List, Tuple


DIRECTIONS = dict(zip('UDLR', (1j, -1j, 1, -1)))


def manhattan_distance(number: complex) -> float:
    return abs(number.real) + abs(number.imag)


def get_input() -> Tuple[List[str], ...]:
    with open('input.txt', 'r') as challenge_input:
        return tuple(line.strip().split(',') for line in challenge_input)


def get_travel(instructions: List[str]) -> Dict[complex, int]:
    src = 0j
    total_steps_taken = 0
    steps = (DIRECTIONS[i[0]] * int(i[1:]) for i in instructions)
    points: Dict[complex, int] = {}
    for step in steps:
        dst = src + step
        direction = (dst - src) / abs(dst - src)
        while src != dst:
            src += direction
            total_steps_taken += 1
            # Remember only the distance to the first visit
            points[src] = points.get(src, total_steps_taken)
    return points


# Part 1
inputs = get_input()
visited1, visited2 = get_travel(inputs[0]), get_travel(inputs[1])
intersections = set(visited1) & set(visited2)
closest = min(intersections, key=manhattan_distance)
print(manhattan_distance(closest))


# Part 2
distances = ((visited1[k], visited2[k]) for k in intersections)
print(sum(min(distances, key=sum)))
