import copy
import itertools
import pathlib

from typing import Callable, Iterator, Optional


MOVES = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1),
)
EMPTY_SEAT, TAKEN_SEAT, FLOOR = 'L', '#', '.'
SOME_SEAT = {EMPTY_SEAT, TAKEN_SEAT}


MATRIX = list[list[str]]
SEARCHER = Callable[[MATRIX, int, int], Iterator[Optional[str]]]


def read_lines(path: pathlib.Path) -> Iterator[list[str]]:
    with open(path) as f:
        yield from (list(n.strip()) for n in f)


def is_in_bounds(matrix: MATRIX, x: int, y: int) -> bool:
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])


def get_seats(seats: MATRIX) -> Iterator[tuple[str, int, int]]:
    for i, line in enumerate(seats):
        for j, seat in enumerate(line):
            yield (seat, i, j)


def get_adjacents(seats: MATRIX, x0: int, y0: int) -> Iterator[Optional[str]]:
    yield from (
        seats[x0 + x1][y0 + y1]
        for x1, y1 in MOVES
        if is_in_bounds(seats, x0 + x1, y0 + y1)
    )


def get_viewables(seats: MATRIX, x0: int, y0: int) -> Iterator[Optional[str]]:
    def get_view_in_direction(x1, y1):
        x, y = x0, y0
        while is_in_bounds(seats, (x := x + x1), (y := y + y1)):
            if seats[x][y] in SOME_SEAT:
                return seats[x][y]

    yield from itertools.starmap(get_view_in_direction, MOVES)


def stabalize(seats: MATRIX, searcher: SEARCHER, max_neighbors: int) -> MATRIX:
    def get_updated_seat(seat: str, nearby: list[Optional[str]]) -> str:
        taken_seats = nearby.count(TAKEN_SEAT)
        seat_condition = {
            seat == EMPTY_SEAT and not taken_seats:              TAKEN_SEAT,
            seat == TAKEN_SEAT and taken_seats >= max_neighbors: EMPTY_SEAT,
        }
        return seat_condition.get(True, seat)

    matrix_copy = copy.deepcopy(seats)
    seats = [[]]
    while seats != matrix_copy:
        seats = copy.deepcopy(matrix_copy)
        for seat, i, j in get_seats(seats):
            nearby = list(searcher(seats, i, j)) if seat != '.' else []
            matrix_copy[i][j] = get_updated_seat(seat, nearby)
    return matrix_copy


def count_occupied_seats(matrix: MATRIX) -> int:
    return sum(line.count(TAKEN_SEAT) for line in matrix)


if __name__ == '__main__':
    matrix = list(read_lines(pathlib.Path('input.txt')))
    print(count_occupied_seats(stabalize(matrix, get_adjacents, 4)))
    print(count_occupied_seats(stabalize(matrix, get_viewables, 5)))
