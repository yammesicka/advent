import functools
from collections import defaultdict
from typing import Dict, Iterable, List


def get_input() -> Iterable[str]:
    with open('input.txt', 'r') as challenge_input:
        return map(str.strip, challenge_input.readlines())


def parse_input(inputs: Iterable[str]) -> Dict[str, List[str]]:
    planets: Dict[str, List[str]] = defaultdict(list)
    for line in inputs:
        planet, _, orbiter = line.partition(')')
        planets[orbiter].append(planet)
    return planets


def map_flatter(starmap: Dict[str, List[str]]) -> Dict[str, List[str]]:
    @functools.lru_cache(maxsize=None)
    def flat_map(start: str) -> List[str]:
        if start not in starmap:
            return []
        stars = [s for star in starmap[start] for s in flat_map(star)]
        return starmap[start] + stars
    return {star: flat_map(star) for star in starmap}


# Part 1
data = parse_input(get_input())
flat_orbiters = map_flatter(data)
print(sum(map(len, flat_orbiters.values())))

# Part 2
print(len(set(flat_orbiters['YOU']) ^ set(flat_orbiters['SAN'])))
