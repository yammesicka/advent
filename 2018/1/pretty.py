import itertools
from typing import Iterator


def get_input() -> Iterator[int]:
    with open('input.txt', 'r') as challenge_input:
        yield from (int(line.strip()) for line in challenge_input)


# Part 1
print(sum(get_input()))


# Part 2
def first_repeating_frequency(frequencies: Iterator[int]) -> int:
    calculated_frequencies = set()
    current_frequency = 0
    for frequency in itertools.cycle(frequencies):
        current_frequency += frequency
        if current_frequency in calculated_frequencies:
            return current_frequency
        calculated_frequencies.add(current_frequency)


print(first_repeating_frequency(get_input()))