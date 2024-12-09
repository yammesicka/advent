from collections import defaultdict
import itertools
from pathlib import Path
from typing import Callable


TEXT = (Path(__file__).parent / "input.txt").read_text().splitlines()
HEIGHT, WIDTH = len(TEXT), len(TEXT[0])
EMPTY = "."
GRID = {complex(i, j): c for i, row in enumerate(TEXT) for j, c in enumerate(row)}

type Grid = dict[complex, str]


def get_antennas(grid: Grid = GRID) -> defaultdict[str, list[complex]]:
    antennas = defaultdict(list)
    for xy, c in grid.items():
        if c != EMPTY:
            antennas[c].append(xy)
    return antennas


def jump_once(a: complex, b: complex, distance: complex, grid: Grid) -> set[complex]:
    return {p for p in (a + distance, b - distance) if p in grid}


def jump_infinitely(a: complex, b: complex, distance: complex, grid: Grid) -> set[complex]:
    jumps = {a, b}
    while (a := a + distance) in grid:
        jumps.add(a)
    while (b := b - distance) in grid:
        jumps.add(b)
    return jumps


def find_antennas(jump: Callable[..., set[complex]], grid: Grid = GRID) -> set[complex]:
    jumps = set()
    for coords in get_antennas(grid).values():
        for a, b in itertools.combinations(coords, r=2):
            jumps |= jump(a, b, distance=a - b, grid=grid)
    return jumps


print(f"Part 1: {len(find_antennas(jump_once))}")
print(f"Part 2: {len(find_antennas(jump_infinitely))}")
