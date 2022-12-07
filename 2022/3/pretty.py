from collections.abc import Iterator
import pathlib
import string


def parse(f: pathlib.Path) -> Iterator[str]:
    yield from f.read_text().splitlines()


def parse_line_blocks(f: pathlib.Path, block_size: int) -> Iterator[list[str]]:
    lines = f.read_text().splitlines()
    for chunk_offset in range(0, len(lines), block_size):
        yield lines[chunk_offset:chunk_offset + block_size]


def get_compartments(truck: str) -> tuple[str, str]:
    half_way = len(truck) // 2
    return truck[:half_way], truck[half_way:]


def get_shared(*args: str) -> str:
    shared = set.intersection(*map(set, args))
    return shared.pop()


def get_truck_shared_letter(truck: str) -> str:
    return get_shared(*get_compartments(truck))


def get_priority(char: str) -> int:
    return string.ascii_letters.index(char) + 1


def part_1(f: pathlib.Path) -> int:
    shared = map(get_truck_shared_letter, parse(f))
    return sum(map(get_priority, shared))


def part_2(f: pathlib.Path) -> int:
    truck_blocks = parse_line_blocks(f, block_size=3)
    return sum(get_priority(get_shared(*block)) for block in truck_blocks)


if __name__ == '__main__':
    input_file = pathlib.Path(__file__).parent / 'input.txt'
    print(f'Part 1: {part_1(input_file)}')
    print(f'Part 2: {part_2(input_file)}')
