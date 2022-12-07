import pathlib
import re


text = pathlib.Path('input.txt').read_text()
assignments = re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", text, re.MULTILINE)
ranges = tuple(tuple(map(int, assignment)) for assignment in assignments)


fully_contained_ranges = sum(
    (start1 <= start2 and end1 >= end2) or (start2 <= start1 and end2 >= end1)
    for start1, end1, start2, end2 in ranges
)

overlapping_ranges = sum(
    start1 <= end2 and start2 <= end1
    for start1, end1, start2, end2 in ranges
)

print(f"{fully_contained_ranges=}, {overlapping_ranges=}")
