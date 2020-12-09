import pathlib
import re
from typing import Iterator

import networkx as nx


BagCanInclude = dict[str, dict[str, int]]

TARGET_BAG = 'shiny gold'
LINE_BAG = re.compile(
    r'(?P<count>\d)\s+'
    r'(?P<color>\w+\s+\w+)'
)


def read_lines(path: pathlib.Path) -> Iterator[str]:
    with open(path) as f:
        yield from f


def extract_bags(line: str) -> BagCanInclude:
    color = ' '.join(line.split()[:2])
    can_contain = LINE_BAG.finditer(line)
    return {
        color: {bag['color']: int(bag['count']) for bag in can_contain}
    }


def get_bags_options(lines: Iterator[BagCanInclude]) -> BagCanInclude:
    bags_options: BagCanInclude = {}
    for line in lines:
        bags_options.update(line)
    return bags_options


def create_bags_graph(bags: BagCanInclude) -> nx.Graph:
    graph = nx.DiGraph()
    for color, bags_included in bags.items():
        for color_included, number_included in bags_included.items():
            graph.add_edge(color, color_included, weight=number_included)
    return graph


def count_shiny_options(bags_options: nx.Graph) -> int:
    return sum(
        nx.has_path(bags_options, bag, TARGET_BAG)
        for bag in bags_options.nodes
    ) - 1  # The shiny gold bag itself


def get_shiny_include_capacity(bags: nx.Graph, source: str) -> int:
    def count_bags(src: str, bags_until_now: int = 1) -> int:
        total_bags = 0
        for bag, props in bags[src].items():
            weight = bags_until_now * props['weight']
            total_bags += weight + count_bags(bag, weight)
        return total_bags

    return count_bags(source)


if __name__ == '__main__':
    bags = map(extract_bags, read_lines(pathlib.Path('input.txt')))
    bags_graph = create_bags_graph(get_bags_options(bags))
    print(count_shiny_options(bags_graph))
    print(get_shiny_include_capacity(bags_graph, TARGET_BAG))
