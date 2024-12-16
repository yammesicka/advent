from pathlib import Path
from itertools import count, takewhile


ROBOT, OBSTACLE, BOX, EMPTY_SPACE = "@#O."
DIRS = {"<" : -1j, ">" : 1j, "^" : -1, "v" : 1}

map_, steps_ = (Path(__file__).parent / 'input.txt').read_text().split("\n\n")
grid = {complex(x, y): cell for x, r in enumerate(map_.splitlines()) for y, cell in enumerate(r)}
STEPS = [DIRS[s] for s in steps_.replace("\n", "")]
robot = next(k for k, v in grid.items() if v == ROBOT)


def push(start: complex, step: complex, grid: dict[complex, str] = grid) -> complex:
    robot_place = start - step
    boxes: list[complex] = list(takewhile(lambda c: grid[c] == BOX, count(start, step)))
    push_from, push_to = boxes[0], boxes[-1] + step
    if grid[push_to] != EMPTY_SPACE:
        return robot_place

    grid[robot_place], grid[push_from], grid[push_to] = EMPTY_SPACE, ROBOT, BOX
    return push_from


for step in STEPS:
    next_step = robot + step
    if grid[next_step] == EMPTY_SPACE:
        grid[robot], grid[next_step] = EMPTY_SPACE, ROBOT
        robot = next_step
    elif grid[next_step] == BOX:
        robot = push(next_step, step)

print(int(sum(k.real * 100 + k.imag for k, v in grid.items() if v == BOX)))
