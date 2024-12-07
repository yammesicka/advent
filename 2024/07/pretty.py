import operator
import re
from collections.abc import Callable, Sequence
from functools import reduce
from itertools import product
from pathlib import Path


type BinaryOperators = Sequence[Callable[[int, int], int]]
type Operands = tuple[int, ...]

TEXT = (Path(__file__).parent / "input.txt").read_text()
LINES: list[tuple[Operands, int]] = [
    (tuple(map(int, numbers.split())), int(result))
    for result, numbers in re.findall(r"(\d+):\s+((?:\d+[ \t]*)+)", TEXT)
]


def solver(numbers: Operands, solution: int, allowed_operators: BinaryOperators) -> int:
    for operators in product(allowed_operators, repeat=len(numbers) - 1):
        actions = iter(operators)
        if solution == reduce(lambda x, y: next(actions)(x, y), numbers):
            return solution
    return 0


# Part 1
ALLOWED_OPERATORS = (operator.add, operator.mul)
print(sum(solver(*line, ALLOWED_OPERATORS) for line in LINES))

# Part 2
ALLOWED_OPERATORS = (operator.add, operator.mul, lambda a, b: int(str(a) + str(b)))
print(sum(solver(*line, ALLOWED_OPERATORS) for line in LINES))
