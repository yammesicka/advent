import pathlib
import re


COMPESS = 'ESWN'
DIRECTIONS = dict(zip(COMPESS, (1, -1j, -1, 1j)))


def get_manhattan_distance(x: complex, y: complex) -> int:
    return int(abs(y.real - x.real) + abs(y.imag - x.imag))


def rotate_head(head: str, direction: str, angle: int) -> str:
    current = COMPESS.index(head)
    ticks = angle // (90 if direction == 'R' else -90)
    return COMPESS[(current + ticks) % 4]


def sail_ship(moves: list[tuple[str, str]]) -> complex:
    ship = 0 + 0j
    head = 'E'
    for move, steps in moves:
        move = head if move == 'F' else move
        if move in 'NESW':
            ship += DIRECTIONS[move] * int(steps)
        elif move in 'RL':
            head = rotate_head(head, move, angle=int(steps))
    return ship


def rotate_waypoint(waypoint: complex, direction: str, angle: int) -> complex:
    direction_sign = -1 if direction == 'R' else 1
    change = (direction_sign * 1j) ** (int(angle) // 90)
    return waypoint * change


def sail_waypoints(moves: list[tuple[str, str]]) -> complex:
    ship = 0 + 0j
    waypoint = 10 + 1j
    for move, steps in moves:
        if move == 'F':
            ship += waypoint * int(steps)
        elif move in 'NESW':
            waypoint += DIRECTIONS[move] * int(steps)
        elif move in 'RL':
            waypoint = rotate_waypoint(waypoint, move, int(steps))
    return ship


if __name__ == '__main__':
    moves = re.findall(r'(\w)(\d+)', pathlib.Path('input.txt').read_text())
    print(get_manhattan_distance(0 + 0j, sail_ship(moves)))
    print(get_manhattan_distance(0 + 0j, sail_waypoints(moves)))
