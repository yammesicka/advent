from collections.abc import Iterable
import itertools
import pathlib


def read(file: pathlib.Path) -> Iterable[int]:
    yield from map(int, file.read_text().strip().splitlines())


def count_increases(depths: Iterable[int]) -> int:
    return sum(i < j for i, j in itertools.pairwise(depths))


def count_sum_increases(depths: Iterable[int], window_size: int) -> int:
    head, tail = itertools.tee(depths)
    for _ in range(window_size):
        next(tail, None)
    return sum(i < j for i, j in zip(head, tail))


# Stage 1
print(count_increases(read(pathlib.Path('input.txt'))))
# Stage 2
print(count_sum_increases(read(pathlib.Path('input.txt')), 3))
