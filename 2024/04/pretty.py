import functools
from pathlib import Path
import itertools


type XY = tuple[int, int]

TEXT = (Path(__file__).parent / "input.txt").read_text().splitlines()
WIDTH, HEIGHT = len(TEXT), len(TEXT[0])
DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)
DIAGONALS = ((-1, -1), (-1, 1), (1, -1), (1, 1))


def step(start_point: XY, direction: XY, magnitude: int) -> XY:
    return (
        start_point[0] + direction[0] * magnitude,
        start_point[1] + direction[1] * magnitude,
    )


def slice2d(start: XY, direction: XY, word_size: int, text: list[str] = TEXT) -> str:
    def get_letter_by_offset(offset: int) -> str:
        x, y = step(start, direction, offset)
        is_valid_index = 0 <= x < len(text) and 0 <= y < len(text[0])
        return text[x][y] if is_valid_index else ""

    return "".join(get_letter_by_offset(offset) for offset in range(word_size))


def is_word(start: XY, direction: XY, word: str, text: list[str] = TEXT) -> bool:
    return slice2d(start, direction, len(word), text) == word


# Part one
is_xmas = functools.partial(is_word, word="XMAS", text=TEXT)

all_xy_positions = itertools.product(range(WIDTH), range(HEIGHT))
potential_words = itertools.product(all_xy_positions, DIRECTIONS)
print(sum(itertools.starmap(is_xmas, potential_words)))

# Part two
def is_x_mas(start_point: XY, directions: tuple[XY, ...] = DIAGONALS) -> int:
    count = 0
    for direction in directions:
        start = step(start_point, direction, -1)
        if is_word(start, direction, "MAS", TEXT):
            count += 1
        if count == 2:
            return True
    return False

start_positions = itertools.product(range(WIDTH), range(HEIGHT))
print(sum(map(is_x_mas, start_positions)))
