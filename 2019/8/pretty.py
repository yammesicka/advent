import itertools
from typing import Tuple


HEIGHT, WIDTH = 6, 25
PICTURE_SIZE = HEIGHT * WIDTH


with open('input.txt') as picture_format:
    picture = picture_format.read().strip()

layer_starts = range(0, len(picture), PICTURE_SIZE)
layers = [picture[i:i + PICTURE_SIZE] for i in layer_starts]


# Part 1
fewest_zeros = min(layers, key=lambda layer: layer.count('0'))
print(fewest_zeros.count('1') * fewest_zeros.count('2'))


# Part 2
def parse_pixel_from_layers(layers: Tuple[str, ...]) -> str:
    try:
        return next(itertools.dropwhile('2'.__eq__, layers))
    except StopIteration:
        return '2'


msg = ''.join(map(parse_pixel_from_layers, zip(*layers)))
for i in range(0, PICTURE_SIZE, WIDTH):
    print(msg[i: i+WIDTH].replace('0', ' '))
