from collections.abc import Iterator
from pathlib import Path


def positions(lines: list[str], char: str) -> Iterator[complex]:
    yield from (complex(i, j) for i, row in enumerate(lines) for j, c in enumerate(row) if c == char)


type VISITED = set[complex]
type IS_LOOP = bool
SQUARES_VISITED = 0
IS_STUCK_IN_LOOP = 1

TEXT = (Path(__file__).parent / "input.txt").read_text()
GUARD_SIGN, OBSTACLE_SIGN, BLANK_SIGN = "^", "#", "."
GRID = TEXT.splitlines()
OBSTACLES = set(positions(GRID, OBSTACLE_SIGN))
BLANKS = set(positions(GRID, BLANK_SIGN))
GUARD = next(positions(GRID, GUARD_SIGN))
MAP = OBSTACLES.union(BLANKS).union([GUARD])


def walk(
    map_: set[complex] = MAP,
    guard: complex = GUARD,
    obstacles: set[complex] = OBSTACLES,
) -> tuple[VISITED, IS_LOOP]:
    step = -1
    visited = set()
    while guard in map_ and (guard, step) not in visited:
        visited.add((guard, step))
        if guard + step in obstacles:
            step *= -1j
        else:
            guard += step
    return {v for v, _ in visited}, (guard, step) in visited


# Part 1
squares_visited = walk()[SQUARES_VISITED]
print(len(squares_visited))

# Part 2
print(sum(
    walk(obstacles=OBSTACLES | {new_obstacle})[IS_STUCK_IN_LOOP]
    for new_obstacle in squares_visited
))
