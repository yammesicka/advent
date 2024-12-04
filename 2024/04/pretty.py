import functools
import itertools
from pathlib import Path


type XY = tuple[int, int]

TEXT = (Path(__file__).parent / "input.txt").read_text().splitlines()
HEIGHT, WIDTH = len(TEXT), len(TEXT[0])
DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)
DIAGONALS = ((-1, -1), (-1, 1), (1, -1), (1, 1))


def new_point(start: XY, direction: XY, steps: int) -> XY:
    return (
        start[0] + direction[0] * steps,
        start[1] + direction[1] * steps,
    )


def extract_word(point: XY, direction: XY, word_length: int, text: list[str] = TEXT) -> str:
    def get_letter_by_offset(offset: int) -> str:
        line, char = new_point(point, direction, offset)
        is_valid_position = 0 <= line < len(text) and 0 <= char < len(text[0])
        return text[line][char] if is_valid_position else ""

    return "".join(get_letter_by_offset(offset) for offset in range(word_length))


def matches_word(start: XY, direction: XY, word: str, text: list[str] = TEXT) -> bool:
    return extract_word(start, direction, len(word), text) == word


# Part one
is_xmas = functools.partial(matches_word, word="XMAS", text=TEXT)

start_coordinates = itertools.product(range(HEIGHT), range(WIDTH))
potential_word_positions = itertools.product(start_coordinates, DIRECTIONS)
print(sum(itertools.starmap(is_xmas, potential_word_positions)))

# Part two
def is_x_mas(start_point: XY, diagonals: tuple[XY, ...] = DIAGONALS) -> int:
    diagonals_around_found = 0
    for diagonal in diagonals:
        adjusted_start = new_point(start_point, diagonal, steps=-1)
        if matches_word(adjusted_start, diagonal, "MAS", TEXT):
            diagonals_around_found += 1
        if diagonals_around_found == 2:
            return True
    return False

start_coordinates = itertools.product(range(HEIGHT), range(WIDTH))
print(sum(map(is_x_mas, start_coordinates)))
