import math
import operator
import pathlib
from typing import Iterable, Tuple


def read_lines(path: pathlib.Path) -> Iterable[str]:
    with open(path) as f:
        yield from f


def jump_lines(lines: Iterable[str], jumps: int) -> Iterable[str]:
    yield from (line for place, line in enumerate(lines) if place % jumps == 0)


def slide(map_lines: Iterable[str], jumps: Tuple[int, int]) -> Iterable[str]:
    place = 0
    for line in jump_lines(map_lines, jumps=jumps[1]):
        yield line[place]
        place = (place + jumps[0]) % (len(line) - 1)


def count_trees(slider: Iterable[str]) -> int:
    def is_tree(char: str) -> bool:
        return char == '#'

    return sum(map(is_tree, slider))


def part_1():
    trees_map = read_lines(pathlib.Path('input.txt'))
    slider = slide(trees_map, jumps=(3, 1))
    print(count_trees(slider))


def part_2():
    trees_map = list(read_lines(pathlib.Path('input.txt')))
    jumps = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    trees = (count_trees(slide(trees_map, jump)) for jump in jumps)
    print(math.prod(trees))


if __name__ == '__main__':
    part_1()
    part_2()
