import collections
import math
import numpy
from typing import Iterator, List, Set


def get_asteroids_indexes(space: List[str]):
    for i in range(len(space)):
        for j in range(len(space[i])):
            if space[i][j] == '#':
                yield complex(i, j)


def get_best_asteroid(asteroids: Set[complex]) -> Set[complex]:
    view = collections.defaultdict(set)
    for asteroid1 in asteroids:
        for asteroid2 in asteroids - {asteroid1}:
            distance = asteroid2 - asteroid1
            factor = math.gcd(int(distance.real), int(distance.imag))
            view[asteroid1].add(distance / factor)
    return max(view, key=lambda n: len(view.get(n)))  # Best asteroid
    # return len(max(view.values(), key=len))  # number of asteroids


def shoot(asteroids: Set[complex], center: complex) -> Iterator[complex]:
    asteroids = numpy.array(list(asteroids)) - center
    angles = (360 - (numpy.angle(asteroids, deg=True) - 90) % 360) % 360
    yield from sorted(zip(angles, asteroids))


def get_input() -> List[str]:
    with open('input.txt', 'r') as challenge_input:
        return list(map(str.strip, challenge_input.read().split()))


asteroids = set(get_asteroids_indexes(get_input()))
station = get_best_asteroid(asteroids)
print(station)

for i, asteroid in enumerate(shoot(asteroids, station), 1):
    print(i, asteroid)