from itertools import starmap
from pathlib import Path
import re


TEXT = (Path(__file__).parent / "input.txt").read_text()
MACHINES_TEXT = re.findall(
    r"Button\s+A:\s+X\+(\d+),\s+Y\+(\d+)\n+"
    r"Button\s+B:\s+X\+(\d+),\s+Y\+(\d+)\n+"
    r"Prize:\s+X=(\d+),\s+Y=(\d+)",
    TEXT,
)
MACHINES = [tuple(map(int, m)) for m in MACHINES_TEXT]


def cost_to_win(x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> int:
    """Practically, the solution to a system of linear equations."""
    y = round((z2 - x2 * (z1 / x1)) / (x2 * -y1 / x1 + y2))
    x = round((z1 - y1 * y) / x1)
    if x * x1 + y * y1 == z1 and x * x2 + y * y2 == z2:
        return x * 3 + y
    return 0


print(sum(starmap(cost_to_win, MACHINES)))
print(sum(
    cost_to_win(x1, x2, y1, y2, z1 + 10_000_000_000_000, z2 + 10_000_000_000_000)
    for x1, x2, y1, y2, z1, z2 in MACHINES
))
