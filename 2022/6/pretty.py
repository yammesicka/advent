import pathlib


def solve(message: str, size: int) -> int | None:
    for i in range(size - 1, len(message) - size - 1):
        if len(set(message[i - size:i])) == size:
            return i


message = (pathlib.Path(__file__).parent / 'input.txt').read_text()
print(f"Part 1: {solve(message, 4)}")
print(f"Part 2: {solve(message, 14)}")
