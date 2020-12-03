import functools
import operator
import pathlib
from typing import Iterable, Tuple


def read_lines(path: pathlib.Path) -> Iterable[str]:
    with open(path) as f:
        yield from f


def vertical_jumper(lines: Iterable[str], jumps: int) -> Iterable[str]:
    for place, line in enumerate(lines):
        if place % jumps == 0:
            yield line


def slide(map_lines: Iterable[str], jumps: Tuple[int, int]) -> Iterable[bool]:
    place = 0
    lines = vertical_jumper(map_lines, jumps[1])
    for line in lines:
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
    slider = functools.partial(slide, trees_map)
    jumps = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    trees = (count_trees(slider(jump)) for jump in jumps)
    print(functools.reduce(operator.mul, trees, 1))


if __name__ == '__main__':
    part_2()
