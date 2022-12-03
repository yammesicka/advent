from collections.abc import Iterable, Iterator
import pathlib


PARAGRAPH_SIGN = '\n\n'
total_calories = sum


def get_elfs(f: pathlib.Path) -> Iterator[Iterable[int]]:
    for block in f.read_text().split(PARAGRAPH_SIGN):
        yield map(int, block.splitlines())


def max_elf(elfs_calories: Iterable[int], k: int = 1):
    if k == 1:  # More efficient
        return max(elfs_calories)
    return sum(sorted(elfs_calories)[-k:])


if __name__ == '__main__':
    input_file = pathlib.Path('input.txt')
    elfs_calories = [total_calories(elf) for elf in get_elfs(input_file)]
    print(f'Part 1: {max_elf(elfs_calories)}')
    print(f'Part 2: {max_elf(elfs_calories, k=3)}')
