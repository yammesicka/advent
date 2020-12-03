import pathlib
import re
from typing import Dict, Iterator, Union


LINE_TYPE = Dict[str, Union[str, int]]
LINE_REGEX = re.compile(
    r'(?P<low>\d+)-'
    r'(?P<high>\d+)\s+'
    r'(?P<char>\w+)'
    r'\s*:\s+'
    r'(?P<password>\w+)',
)


def read_lines(path: pathlib.Path) -> Iterator[str]:
    with open(path) as f:
        yield from f


def extract_line(line: str) -> LINE_TYPE:
    line_match = LINE_REGEX.match(line)
    if line_match is None:
        raise ValueError('Bad line pattern', line)

    line_parts: LINE_TYPE = line_match.groupdict()
    line_parts['low'] = int(line_parts['low'])
    line_parts['high'] = int(line_parts['high'])
    return line_parts


def check_pass(low: int, high: int, char: str, password: str) -> bool:
    return low <= password.count(char) <= high


def check_pass_2(low: int, high: int, char: str, password: str) -> bool:
    return (
        (len(password) >= max(low, high)) and
        (password[low - 1] == char) ^ (password[high - 1] == char)
    )


if __name__ == '__main__':
    lines = list(map(extract_line, read_lines(pathlib.Path('input.txt'))))
    print(sum(check_pass(**line) for line in lines))
    print(sum(check_pass_2(**line) for line in lines))
