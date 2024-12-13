from functools import cache
from pathlib import Path


STONES = list(map(int, (Path(__file__).parent / "input.txt").read_text().split()))


@cache
def count(stone: int, steps: int) -> int:
    if steps == 1:
        return 2 if len(str(stone)) % 2 == 0 else 1

    if stone == 0:
        return count(1, steps - 1)
    if len(s := str(stone)) % 2 == 0:
        left, right = int(s[:len(s) // 2]), int(s[len(s) // 2:])
        return count(left, steps - 1) + count(right, steps - 1)
    return count(stone * 2024, steps - 1)


print(sum(count(stone, 25) for stone in STONES))
print(sum(count(stone, 75) for stone in STONES))
