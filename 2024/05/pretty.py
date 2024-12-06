from itertools import combinations, starmap
from pathlib import Path
import re


TEXT = (Path(__file__).parent / "input.txt").read_text()
RULES = set(re.findall(r"(\d+)\|(\d+)", TEXT))
UPDATES = [r.split(",") for r in re.findall(r"\d+,(?:\d+,?)+", TEXT)]


def middle(pages: list[str]) -> int:
    return int(pages[len(pages) // 2])


def follow_rules(former_page: str, latter_page: str, rules: set[tuple[str, str]] = RULES) -> bool:
    return (latter_page, former_page) not in rules


def is_valid_order(pages: list[str]) -> bool:
    page_pairs = combinations(pages, r=2)
    return all(starmap(follow_rules, page_pairs))


# Part 1
print(sum(middle(pages) for pages in UPDATES if is_valid_order(pages)))


# Part 2:
def bubble_sort(pages: list[str], rules: set[tuple[str, str]] = RULES) -> list[str]:
    i = j = 0
    while i < len(pages):
        j = i + 1
        while j < len(pages):
            if not follow_rules(pages[i], pages[j], rules):
                pages[i], pages[j] = pages[j], pages[i]
                j = i
            j += 1
        i += 1
    return pages


print(sum(middle(bubble_sort(pages)) for pages in UPDATES if not is_valid_order(pages)))
