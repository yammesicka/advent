from pathlib import Path


type Grid = dict[complex, str]

ROBOT, OBSTACLE, EMPTY, BOX_L, BOX_R = "@#.[]"
DIRS = {"<" : -1j, ">" : 1j, "^" : -1, "v" : 1}

map_, steps_ = (Path(__file__).parent / 'input.txt').read_text().split("\n\n")
map_ = map_.translate(str.maketrans({"#": "##", ".": "..", "O": "[]", "@": "@."}))
grid = {complex(x, y): cell for x, r in enumerate(map_.splitlines()) for y, cell in enumerate(r)}
STEPS = [DIRS[s] for s in steps_.replace("\n", "")]
robot = next(k for k, v in grid.items() if v == ROBOT)


def move(start: complex, step: complex, g: Grid = grid) -> Grid | None:
    current = start + step
    if any((
        g[current] == BOX_L and move(current + 1j, step, g) and move(current, step, g),
        g[current] == BOX_R and move(current - 1j, step, g) and move(current, step, g),
        g[current] == EMPTY,
    )):
        g[start], g[current] = g[current], g[current - step]
        return g
    

for step in STEPS:
    if grid_after_move := move(robot, step, grid.copy()):
        robot += step
        grid = grid_after_move


print(int(sum(k.real * 100 + k.imag for k, v in grid.items() if v == BOX_L)))
