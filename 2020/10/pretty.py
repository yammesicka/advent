import collections
import functools
import pathlib

from typing import Iterator


def read_lines(path: pathlib.Path) -> Iterator[int]:
    with open(path) as f:
        yield from map(int, f)


def get_legit_jumps(lines: list[int], from_line: int) -> Iterator[int]:
    def is_legit_jump(to_line: int) -> bool:
        in_bounds = to_line < len(lines)
        return in_bounds and (lines[from_line] + 3) >= lines[to_line]

    destination_lines = (from_line + i for i in range(1, 4))
    yield from filter(is_legit_jump, destination_lines)


def count_paths(numbers: list[int]) -> int:
    @functools.lru_cache(maxsize=1024)
    def count_number_paths(from_line: int) -> int:
        next_lines = get_legit_jumps(numbers, from_line)
        return max(1, sum(map(count_number_paths, next_lines)))
    return count_number_paths(from_line=0)


if __name__ == '__main__':
    lines = sorted(read_lines(pathlib.Path('input.txt')))
    lines = [0] + lines + [lines[-1] + 3]
    jumps = (lines[i + 1] - lines[i] for i in range(len(lines) - 1))
    jumps_of = collections.Counter(jumps)
    print(jumps_of[3] * jumps_of[1])
    print(count_paths(lines))
