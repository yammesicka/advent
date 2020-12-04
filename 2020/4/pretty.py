import os
import pathlib
import re
from typing import Iterator


PASSPORT_MANDATORY_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
VALID_HAIR_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def read_lines(path: pathlib.Path) -> Iterator[str]:
    with open(path) as f:
        yield from f


def get_passport_as_line(lines_iterator: Iterator[str]) -> str:
    passport = ""
    while (line := next(lines_iterator, None)) and line != os.linesep:
        passport += line.strip() + ' '
    return passport


def dictify_passport(passport: str) -> dict[str, str]:
    return dict(re.findall(r"(\w+):((?:\w|#)+)", passport))


def is_fields_valid(passport: dict[str, str]) -> bool:
    def is_number_in_range(number: str, start: int, end: int) -> bool:
        return number.isdigit() and int(number) in range(start, end + 1)

    def is_height_valid(height: str) -> bool:
        return (
            (height.endswith('cm') and 150 <= int(height[:-2]) <= 193)
            or (height.endswith('in') and 59 <= int(height[:-2]) <= 76)
        )

    return (
        is_number_in_range(passport['byr'], 1920, 2002)
        and is_number_in_range(passport['iyr'], 2010, 2020)
        and is_number_in_range(passport['eyr'], 2020, 2030)
        and is_height_valid(passport['hgt'])
        and bool(re.fullmatch('#[0-9a-f]{6}', passport['hcl'], re.IGNORECASE))
        and passport['ecl'] in VALID_HAIR_COLORS
        and passport['pid'].isdigit() and len(passport['pid']) == 9
    )


def is_passport_valid(passport: dict[str, str]) -> bool:
    return (
        PASSPORT_MANDATORY_FIELDS <= set(passport)
        and is_fields_valid(passport)  # Only in part 2
    )


if __name__ == '__main__':
    lines = read_lines(pathlib.Path('input.txt'))
    count = 0
    while (passport := get_passport_as_line(lines)):
        count += is_passport_valid(dictify_passport(passport))
    print(count)
