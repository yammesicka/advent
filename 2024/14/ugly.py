from collections import Counter
from dataclasses import dataclass
import math
from pathlib import Path
import re


@dataclass
class Robot:
    position: complex
    velocity: complex

    def step(self, steps: int = 1) -> complex:
        pos = self.position + self.velocity * steps
        return complex(pos.real % SIZE.real, pos.imag % SIZE.imag)


TEXT = (Path(__file__).parent / "input.txt").read_text()
SIZE = 101 + 103j
CX, CY = SIZE.real / 2, SIZE.imag / 2
ROBOTS_TEXT = re.findall(r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)", TEXT)
ROBOTS_INTS = [tuple(map(int, r)) for r in ROBOTS_TEXT]
ROBOTS = [Robot(complex(x, y), complex(vx, vy)) for x, y, vx, vy in ROBOTS_INTS]


def quadrant(p: complex) -> tuple[bool, bool] | None:
    if p.real == CX or p.imag == CY:
        return None
    return p.real < CX, p.imag < CY


# Part 1
final_positions = [robot.step(100) for robot in ROBOTS]
quads = Counter(filter(None, map(quadrant, final_positions)))
print(math.prod(quads.values()))

# Part 2
robots = [Robot(robot.position, robot.velocity) for robot in ROBOTS]
best = (0, 0)
for i in range(1, 10000):
    h, w = Counter(), Counter()
    for robot in robots:
        robot.position = robot.step()
    h = Counter(r.position.real for r in robots)
    w = Counter(r.position.imag for r in robots)
    # Kinda odd way to check it but not gonna start
    # using the Chinese Reminder Theorem for this
    score = h.most_common(1)[0][1] * w.most_common(1)[0][1]
    best = max(best, (score, i))
print(best[1])

# Bonus: print it
final_positions = [robot.step(7055) for robot in ROBOTS]
for w in range(int(CY)):
    row = "".join("#" if complex(x, w) in final_positions else "." for x in range(int(CX)))
    print(row)
