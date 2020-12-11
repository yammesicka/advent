import collections
import math
import pathlib

from typing import Iterator


def read_lines(path: pathlib.Path) -> Iterator[int]:
    with open(path) as f:
        yield from map(int, f)


def dothis(lines, i):
    line = lines[i]
    n = 0
    if len(lines) - i >= 2 and line + 3 >= lines[i + 1]:
        n += 1
    if len(lines) - i >= 3 and line + 3 >= lines[i + 2]:
        n += 1
    if len(lines) - i >= 4 and line + 3 >= lines[i + 3]:
        n += 1
    return n


def calc(n):
    total = 0
    mul = 1
    i = 0
    while i < len(n):
        tail = i + 2
        while set(n[tail - 2:tail]) != set([1]):
            tail += 2
        else:
            pass


if __name__ == '__main__':
    lines = [0] + sorted(read_lines(pathlib.Path('input.txt')))
    print(lines)
    c = collections.Counter(lines[i + 1] - lines[i] for i in range(len(lines) - 1))
    print(c)
    print((c[3] + 1) * c[1])
    print([dothis(lines, i) for i in range(len(lines) - 1)])
    #print(calc([dothis(lines, i) for i in range(len(lines))]))
