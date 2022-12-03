import functools
import pathlib


def read(file: pathlib.Path):
    return file.read_text()


def get_count(item: tuple[int, int]):
    return item[1], item[0]


def get_most_common_bit_at(binaries: list[str], i: int) -> str:
    how_many_ones = sum(int(binary[i]) for binary in binaries)
    half_of_all_binaries = len(binaries) / 2
    return str(int(how_many_ones >= half_of_all_binaries))


def invert_bits(number: int, max_size: int) -> int:
    return 2 ** max_size - number - 1


def part_1(binaries: list[str]) -> int:
    _bit_at = functools.partial(get_most_common_bit_at, binaries)
    common_bits = ''.join(_bit_at(i) for i in range(len(binaries[0])))
    number = int(common_bits, 2)
    not_number = invert_bits(number, len(common_bits))
    return number * not_number


def part_2(binaries):
    def _reduce_using_bit(numbers, bit_to_match, index):
        if len(numbers) == 1:
            return numbers
        return [number for number in numbers if number[index] == bit_to_match]

    oxygen = binaries.copy()
    co2 = binaries.copy()
    i = 0
    while len(oxygen) != 1 or len(co2) != 1:
        common_bit = get_most_common_bit_at(oxygen, i)
        uncommon_bit = str(1 - int(get_most_common_bit_at(co2, i)))
        oxygen = _reduce_using_bit(oxygen, common_bit, i)
        co2 = _reduce_using_bit(co2, uncommon_bit, i)
        i += 1
    return int(oxygen.pop(), 2) * int(co2.pop(), 2)


text = read(pathlib.Path(__file__).parent / 'input.txt')
print(part_1(text.split()))
print(part_2(text.split()))
