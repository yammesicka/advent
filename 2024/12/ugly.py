from collections import defaultdict
from pathlib import Path


TEXT = (Path(__file__).parent / "input.txt").read_text().splitlines()
GRID = {complex(i, j): c for i, row in enumerate(TEXT) for j, c in enumerate(row)}
W, H = len(TEXT[0]), len(TEXT)
DIRS = UP, DOWN, LEFT, RIGHT = (-1j, 1j, -1, 1)
PERP = {
    UP:    (LEFT, RIGHT),
    DOWN:  (LEFT, RIGHT),
    LEFT:  (UP, DOWN),
    RIGHT: (UP, DOWN),
}


def neighbors(p: complex) -> set[complex]:
    return {p + d for d in DIRS}

def perimeter(area):
    return sum(4 - len(neighbors(p) & area) for p in area)


class Grouper:
    def __init__(self):
        self.groups: defaultdict[str, list[set[complex]]] = defaultdict(list)

    def _new_group(self, c: str, p: complex) -> set[complex]:
        self.groups[c].append({p})
        return self.groups[c][-1]

    def _add_to_group_with_neighbors(self, c: str, p: complex) -> set[complex] | None:
        groups_found = [group for group in self.groups[c] if neighbors(p) & group]
        for group in groups_found:
            group.add(p)
        self._consolidate_groups(groups_found)
        return groups_found[0] if groups_found else None

    def add(self, c: str, p: complex) -> set[complex]:
        return self._add_to_group_with_neighbors(c, p) or self._new_group(c, p)

    def _consolidate_groups(self, groups: list[set[complex]]) -> None:
        if len(groups) <= 1:
            return
        for group in groups[1:]:
            groups[0].update(group)
            self.groups[c].remove(group)

    def __iter__(self):
        return iter((c, group) for c, groups in self.groups.items() for group in groups)


def get_number_of_sides(area: set[complex]) -> int:
    calculated = set()
    sides = 0
    for p in area:
        for move in DIRS:
            if (move, p) not in calculated:
                line = []
                for perp_move in PERP[move]:
                    cur = p
                    while cur in area and (cur + move) not in area:
                        line.append((move, cur))
                        cur += perp_move
                if line:
                    sides += 1
                    calculated |= frozenset(line)
    return sides


areas = Grouper()
for p, c in GRID.items():
    areas.add(c, p)

# Part 1
print(sum(len(area) * perimeter(area) for _, area in areas))

# Part 2
print(sum(len(area) * get_number_of_sides(area) for _, area in areas))
