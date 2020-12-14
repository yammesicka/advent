import collections
import functools
import itertools
import math
import pathlib

from typing import Iterator


def read_lines(path: pathlib.Path) -> Iterator[int]:
    with open(path) as f:
        yield from map(int, f)





if __name__ == '__main__':
    lines = read_lines(pathlib.Path('input.txt'))
    print(

    )
