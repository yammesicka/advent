from collections.abc import Iterator
from pathlib import Path


TEXT = (Path(__file__).parent / "input.txt").read_text().splitlines()
GRID = {complex(i, j): int(c) for i, row in enumerate(TEXT) for j, c in enumerate(row)}
STARTS = [xy for xy, c in GRID.items() if c == 0]
DIRECTIONS = (1, 1j, -1, -1j)


def next_valid_steps(xy: complex, slope: int) -> Iterator[complex]:
    for step in DIRECTIONS:
        if xy + step in GRID and GRID[xy + step] - slope == 1:
            yield xy + step


def peaks(xy: complex, slope: int) -> set[complex]:
    if GRID[xy] == 9:
        return {xy}
    return set().union(
        *(peaks(next_xy, slope + 1) for next_xy in next_valid_steps(xy, slope))
    )


def routes(xy: complex, slope: int) -> int:
    if GRID[xy] == 9:
        return 1
    return sum(routes(next_xy, slope + 1) for next_xy in next_valid_steps(xy, slope))


print(sum(len(peaks(start, slope=0)) for start in STARTS))
print(sum(routes(start, slope=0) for start in STARTS))
