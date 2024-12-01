from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Counter, TypeAlias


Locations: TypeAlias = tuple[Iterable[int], Iterable[int]]

INPUT_FILE = Path(__file__).parent / "input.txt"


def read(file: Path) -> Iterator[str]:
    yield from file.read_text().splitlines()


def _ints(strings: list[str]) -> Iterator[int]:
    return map(int, strings)


def parse(locations: Iterator[str]) -> Locations:
    left, right = zip(*(line.split() for line in locations), strict=True)
    return _ints(left), _ints(right)


def sort(locations: Locations) -> Locations:
    left, right = map(sorted, locations)
    return left, right


def calc_1(locations: Locations) -> int:
    return sum(abs(x - y) for x, y in zip(*locations))


def calc_2(locations: Locations) -> int:
    left, right = locations
    counter = Counter(right)
    return sum(counter[item] * item for item in left)


print(calc_1(sort(parse(read(INPUT_FILE)))))
print(calc_2(parse(read(INPUT_FILE))))
