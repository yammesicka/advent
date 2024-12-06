from pathlib import Path
import re


INPUT = (Path(__file__).parent / "input.txt").read_text().splitlines()


# Part 1
only_digits = (re.findall(r"\d", line) for line in INPUT)
print(sum(int(line[0] + line[-1]) for line in only_digits))


# Part 2
DIGITS = "zero one two three four five six seven eight nine".split()
ANY_WORDY_DIGIT = "|".join(DIGITS)
FIRST_DIGIT = re.compile(rf"(\d|{ANY_WORDY_DIGIT}).*")
LAST_DIGIT = re.compile(rf".*(\d|{ANY_WORDY_DIGIT})")
WORD_TO_DIGIT = {word: i for i, word in enumerate(DIGITS)}


def line_to_number(line: str) -> int:
    def translate_digit(digit: str) -> int:
        return int(WORD_TO_DIGIT.get(digit, digit))

    first = FIRST_DIGIT.search(line).group(1)
    last = LAST_DIGIT.search(line).group(1)
    return translate_digit(first) * 10 + translate_digit(last)


print(sum(map(line_to_number, INPUT)))
