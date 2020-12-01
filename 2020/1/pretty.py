import operator
import pathlib
from typing import Iterator, Optional, Set, Tuple


def read_lines(path: pathlib.Path) -> Iterator[int]:
    with open(path) as f:
        yield from (int(str.strip(line)) for line in f)


def get_two_candidates_by_sum(
    numbers: Set[int], total: int,
) -> Optional[Tuple[int, int]]:
    for candidate in numbers:
        if total - candidate in numbers:
            return (candidate, total - candidate)
    return None


def part_a(numbers: Set[int], total: int) -> Optional[int]:
    valid_two = get_two_candidates_by_sum(numbers, total)
    if valid_two:
        return operator.mul(*valid_two)
    return None


if __name__ == '__main__':
    TARGET_SUM = 2020
    numbers = set(read_lines(pathlib.Path('input.txt')))

    # A
    print(part_a(numbers, TARGET_SUM))

    # B
    for num in numbers:
        mul_of_two = part_a(numbers, TARGET_SUM - num)
        if mul_of_two:
            print(mul_of_two * num)
