import itertools
from typing import List, Tuple


HEIGHT, WIDTH = 6, 25
PICTURE_SIZE = HEIGHT * WIDTH


def parse_pixel_from_layers(layers: Tuple[str, ...]) -> str:
    try:
        return next(itertools.dropwhile('2'.__eq__, layers))
    except StopIteration:
        return '2'


def get_input() -> str:
    with open('input.txt') as picture_format:
        return picture_format.read().strip()


def get_layers(image_blob: str) -> List[str]:
    layer_starts = range(0, len(image_blob), PICTURE_SIZE)
    return [image_blob[i:i + PICTURE_SIZE] for i in layer_starts]


# Part 1
layers = get_layers(get_input())
fewest_zeros = min(layers, key=lambda layer: layer.count('0'))
print(fewest_zeros.count('1') * fewest_zeros.count('2'))

# Part 2
msg = ''.join(map(parse_pixel_from_layers, zip(*layers)))
for i in range(0, PICTURE_SIZE, WIDTH):
    print(msg[i: i+WIDTH].replace('0', ' '))
