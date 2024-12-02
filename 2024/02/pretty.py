from collections.abc import Callable, Iterable, Iterator
from itertools import pairwise
from pathlib import Path


INPUTS = Path(__file__).parent / "input.txt"
MIN_DIFF, MAX_DIFF = 1, 3


def read_reports(path: Path = INPUTS) -> Iterator[list[int]]:
    with path.open() as report:
        for line in report:
            yield [int(e) for e in line.strip().split()]


def is_safe(
    report: list[int],
    min_diff: int = MIN_DIFF,
    max_diff: int = MAX_DIFF,
) -> bool:
    if report[-1] - report[0] > 0:
        min_diff, max_diff = -max_diff, -min_diff
    return all(min_diff <= x - y <= max_diff for x, y in pairwise(report))


def is_safe_2(report: list[int]) -> bool:
    return any(is_safe(report[:i] + report[i + 1:]) for i in range(len(report)))


def count[T](
    iterator: Iterable[T],
    predicate: Callable[[T], bool] = lambda x: bool(x),
) -> int:
    return sum(1 for entry in iterator if predicate(entry))


print(count(read_reports(), is_safe))
print(count(read_reports(), is_safe_2))
