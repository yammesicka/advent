from itertools import count
import operator
from typing import Generator, List, Optional


OPCODE_SIZE = 4
OPCODES_FUNCTIONS = {
    1: operator.add,
    2: operator.mul,
}

Instructions = Generator[List[int], None, None]


def get_input() -> List[int]:
    with open('input.txt', 'r') as challenge_input:
        return list(map(int, challenge_input.read().strip().split(',')))


def instructions_generator(program: List[int]) -> Instructions:
    for i in count(0, OPCODE_SIZE):
        if program[i] == 99:
            return
        yield program[i:i + OPCODE_SIZE]


def get_output(program: List[int], a: int = 0, b: int = 0) -> Optional[int]:
    program[1:3] = a, b
    for opcode, src1, src2, dst in instructions_generator(program):
        if any(map(len(program).__le__, (dst, src1, src2))):
            return None
        function = OPCODES_FUNCTIONS[opcode]
        program[dst] = function(program[src1], program[src2])
    return program[0]


# Part 1
program = get_input()
print(get_output(list(program)))


# Part 2
MAX_GUESS = 1000
WANTED_OUTPUT = 19_690_720
print(next(
    noun * 100 + verb
    for noun in range(MAX_GUESS) for verb in range(MAX_GUESS)
    if get_output(list(program), noun, verb) == WANTED_OUTPUT
))
