import collections
from itertools import islice
import pathlib

from typing import Iterator


def read_lines(path: pathlib.Path) -> Iterator[int]:
    with open(path) as f:
        yield from map(int, f)


"""
This one was a nice idea, but turned out to be inefficient:

class SearchableDeque(collections.deque):
    def __init__(self, items, *args, **kwargs):
        items = tuple(items)
        self.search_bag = collections.Counter(items)
        super().__init__(items, *args, **kwargs)

    def append(self, to_append, *args, **kwargs):
        if len(self) == self.maxlen:
            self.search_bag[self[0]] -= 1
        self.search_bag[to_append] += 1

        super().append(to_append, *args, **kwargs)

    def __contains__(self, item):
        return self.search_bag[item] > 0
"""


def search_sublist_of_sum(sublist: list[int], sum_to_search: int) -> list[int]:
    tail = 0
    total = 0
    for head, num in enumerate(sublist):
        if total < sum_to_search:
            total += num
        while total > sum_to_search:
            total -= sublist[tail]
            tail += 1
        if total == sum_to_search:
            return sublist[tail:head]
    raise ValueError(f'Sum {sum_to_search} was not found as a sublist.')


def part_a(lines: Iterator[int]) -> int:
    numbers = collections.deque(islice(lines, 25), maxlen=25)
    for number in islice(lines, 25, None):
        if all(number - a not in numbers for a in numbers):
            return number
        numbers.append(number)
    raise ValueError("Can't find the special number.")


if __name__ == '__main__':
    lines = read_lines(pathlib.Path('input.txt'))
    solution = part_a(lines)
    print(solution)

    lines: list[int] = list(read_lines(pathlib.Path('input.txt')))
    sublist = search_sublist_of_sum(lines, solution)
    print(min(sublist) + max(sublist))
