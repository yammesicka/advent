import pathlib
import re
from typing import TypeAlias


CARGO_SIZE = 4
Crane: TypeAlias = list[str]
Instruction: TypeAlias = tuple[int, int, int]


def parse_cranes(cranes_text: str) -> list[Crane]:
    lines = cranes_text.splitlines()[-2::-1]
    crane_indexes = range(1, len(lines[0]), CARGO_SIZE)
    return [
        [cargo for line in lines if (cargo := line[crane_idx].strip())]
        for crane_idx in crane_indexes
    ]


def parse_instructions(instructions) -> tuple[Instruction]:
    raw_moves = re.findall(r"move (\d+) from (\d+) to (\d+)", instructions)
    return tuple(tuple(map(int, line)) for line in raw_moves)


def parse(manual: pathlib.Path) -> tuple[list[Crane], tuple[Instruction]]:
    cranes_text, _, instructions = manual.read_text().partition('\n\n')
    return parse_cranes(cranes_text), parse_instructions(instructions)


def move_cranes(
    cranes_: list[Crane], moves: tuple[Instruction], flip: bool = False,
) -> list[Crane]:
    cranes = [crane.copy() for crane in cranes_]
    for count, from_crane, to_crane in moves:
        src, dst = cranes[from_crane - 1], cranes[to_crane - 1]
        cargo = (None, -count - 1, -1) if flip else (-count, None)
        dst.extend(src[slice(*cargo)])
        del src[slice(*cargo)]
    return cranes


def lasts(iterable: list[Crane]) -> str:
    return ''.join(crane[-1] for crane in iterable)


cranes, moves = parse(pathlib.Path(__file__).parent / 'input.txt')
print(f"Part 1: {lasts(move_cranes(cranes, moves, flip=True))}")
print(f"Part 2: {lasts(move_cranes(cranes, moves, flip=False))}")
