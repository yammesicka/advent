from collections import Counter
import itertools
from typing import Any, Iterator


def get_input() -> Iterator[int]:
    with open('input.txt', 'r') as challenge_input:
        yield from map(str.strip, challenge_input)


def is_empty(iterator: Iterator[Any]) -> bool:
    try:
        next(iterator)
    except StopIteration:
        return True
    return False


# Part 1
def calculate_checksum(plates):
    twos, threes = 0, 0
    for plate in plates:
        twos += not is_empty(c for c in set(plate) if plate.count(c) == 2)
        threes += not is_empty(c for c in set(plate) if plate.count(c) == 3)
    return twos * threes


# Part 2
def closest_strings(plates: Iterator[int]) -> int:
    calculated_plates = []
    for plate in plates:
        current_plate = Counter(plate)
        for old_plate in calculated_plates:
            if sum((old_plate - current_plate).values()) == 1:
                common_characters = ''.join((current_plate - old_plate).keys())
                assert len(common_characters) == 1
                return plate.replace(common_characters, '', 1)
        calculated_plates.append(current_plate)


print(calculate_checksum(get_input()))
print(closest_strings(get_input()))