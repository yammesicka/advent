import operator
from typing import Any, Callable, Dict, Iterator, List, Optional

from typing_extensions import TypedDict


Command = TypedDict(
    'Command',
    {'size': int, 'function': Callable[..., Any], 'void': int},
    total=False,
)
ParsedCmds = Iterator[int]

INPUTS = iter([1])
OPCODES: Dict[int, Command] = {
    1: {'size': 4, 'function': operator.add},
    2: {'size': 4, 'function': operator.mul},
    3: {'size': 2, 'function': lambda: next(INPUTS)},
    4: {'size': 2, 'function': print, 'void': 1},
    5: {'size': 3, 'function': operator.truth},
    6: {'size': 3, 'function': operator.not_},
    7: {'size': 4, 'function': lambda x, y: bool(operator.lt(x, y))},
    8: {'size': 4, 'function': lambda x, y: bool(operator.eq(x, y))},
}
JUMP_OPCODES = {5, 6}


def get_input() -> List[int]:
    with open('input.txt', 'r') as challenge_input:
        return list(map(int, challenge_input.read().strip().split(',')))


def parse_command(code: List[int], instruction: int, *args: int) -> ParsedCmds:
    padded_opcode = str(instruction).zfill(5)
    modes, op = padded_opcode[2::-1], int(padded_opcode[3:])
    yield op

    argc = OPCODES[op]['size'] - 2
    for param in range(argc + OPCODES[op].get('void', 0)):
        yield code[args[param]] if modes[param] == '0' else args[param]

    write_to = args[-1] if not OPCODES[op].get('void', False) else None
    is_relative_jump = (op in JUMP_OPCODES and modes[argc] == '0')
    yield code[args[-1]] if is_relative_jump else write_to


def get_output(program: List[int]) -> Optional[int]:
    i = 0
    while program[i] != 99:
        op_size = OPCODES[program[i] % 100]['size']
        opcode, *command = program[i:i + op_size]
        opcode, *args, write_to = parse_command(program, opcode, *command)
        returns = OPCODES[opcode]['function'](*args)
        if returns is not None and opcode not in JUMP_OPCODES:
            program[write_to] = returns
        i = write_to if opcode in JUMP_OPCODES and returns else (i + op_size)
    return program[0]


program = get_input()
get_output(program)
