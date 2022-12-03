from collections.abc import Iterable
import pathlib


FDU = Forward, Down, Up = 'forward', 'down', 'up'


def parse(f: pathlib.Path) -> Iterable[tuple[str, int]]:
    for line in f.read_text().splitlines():
        direction, _, distance = line.partition(' ')
        yield direction, int(distance)


def find_position(course: Iterable[tuple[str, int]]) -> int:
    horizontal = depth = 0
    for direction, distance in course:
        if direction == Forward:
            horizontal += distance
        elif direction == Up:
            depth -= distance
        elif direction == Down:
            depth += distance
    return depth * horizontal


def find_position_2(course: Iterable[tuple[str, int]]) -> int:
    horizontal = depth = aim = 0
    for direction, quantity in course:
        if direction == Forward:
            horizontal += quantity
            depth += aim * quantity
        elif direction == Up:
            aim -= quantity
        elif direction == Down:
            aim += quantity
    return depth * horizontal


if __name__ == '__main__':
    file = pathlib.Path(__file__).parent / 'input.txt'
    print(f'Part 1: {find_position(parse(file))}')
    print(f'Part 2: {find_position_2(parse(file))}')
