import os
import pathlib
from typing import Iterator, TextIO


def read_groups(path: pathlib.Path) -> Iterator[list[str]]:
    def read_next_group(f: TextIO) -> list[str]:
        lines = []
        while (line := f.readline()) and line != os.linesep:
            lines.append(line.rstrip())
        return lines

    with open(path) as f:
        while group := read_next_group(f):
            yield group


def count_answers_a(lines: list[str]) -> int:
    return len(set(''.join(lines)))


def count_answers_b(lines: list[str]) -> int:
    exists_in_all_lines = set(lines[0]).intersection(*lines[1:])
    return len(exists_in_all_lines)


if __name__ == '__main__':
    print(sum(map(count_answers_a, read_groups(pathlib.Path('input.txt')))))
    print(sum(map(count_answers_b, read_groups(pathlib.Path('input.txt')))))
