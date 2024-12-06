from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple


def positions(lines: list[str], char: str) -> Iterator[complex]:
    yield from (
        complex(i, j)
        for i, row in enumerate(lines)
        for j, c in enumerate(row)
        if c == char
    )


Walked = NamedTuple("Walked", [("visited", set[complex]), ("is_loop", bool)])


GUARD_SIGN, OBSTACLE_SIGN, BLANK_SIGN = "^", "#", "."
GRID = (Path(__file__).parent / "input.txt").read_text().splitlines()
OBSTACLES = set(positions(GRID, OBSTACLE_SIGN))
BLANKS = set(positions(GRID, BLANK_SIGN))
GUARD = next(positions(GRID, GUARD_SIGN))
MAP = OBSTACLES.union(BLANKS).union([GUARD])


def walk(
    map_: set[complex] = MAP,
    guard: complex = GUARD,
    obstacles: set[complex] = OBSTACLES,
) -> Walked:
    step = -1
    visited = set()
    while guard in map_ and (guard, step) not in visited:
        visited.add((guard, step))
        if guard + step in obstacles:
            step *= -1j
        else:
            guard += step
    return Walked(visited={v for v, _ in visited}, is_loop=(guard, step) in visited)


# Part 1
print(len(squares_visited := walk().visited))

# Part 2
print(sum(
    walk(obstacles=OBSTACLES | {new_obstacle}).is_loop
    for new_obstacle in squares_visited
))
