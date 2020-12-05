import pathlib
from typing import Iterator


def read_lines(path: pathlib.Path) -> Iterator[str]:
    with open(path) as f:
        yield from map(str.strip, f)


def bin_from_text(text: str, on_bit: str) -> int:
    n = 0
    for i, char in enumerate(reversed(text)):
        bit = int(char == on_bit)
        n += (2 ** i) * bit
    return n


def get_seat_id(line: str) -> int:
    row = bin_from_text(text=line[:7], on_bit='B')
    col = bin_from_text(text=line[7:], on_bit='R')
    return row * 8 + col


if __name__ == '__main__':
    lines = read_lines(pathlib.Path('input.txt'))
    seats = set(map(get_seat_id, lines))
    print(max(seats))  # Part A
    print(set(range(min(seats), max(seats))) - seats)  # Part B
