from pathlib import Path
import re


CODE = (Path(__file__).parent / "input.txt").read_text()

# Part 1
MUL_NUMBERS = (
    r"mul\("
    r"(\d{1,3}),(\d{1,3})"
    r"\)"
)

muls = re.findall(MUL_NUMBERS, CODE)
print(sum(int(a) * int(b) for a, b in muls))

# Part 2
cleaned = re.sub(r"don't\(\).*?do\(\)", " ", CODE, flags=re.DOTALL)
cleaned = re.sub(r"don't\(\).*", " ", cleaned, flags=re.DOTALL)

muls = re.findall(MUL_NUMBERS, cleaned)
print(sum(int(a) * int(b) for a, b in muls))
