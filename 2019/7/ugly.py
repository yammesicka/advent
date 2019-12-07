import itertools
import operator
from copy import copy
from typing import (
    Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple, Union,
)

from typing_extensions import TypedDict


Command = TypedDict(
    'Command',
    {
        'size': int, 'function': Callable[..., Any],
        'jump': bool, 'void': int, 'method': bool,
    },
    total=False,
)
ParsedCmds = Iterator[int]
vmethod = {'void': 1, 'method': True}


class IntcodeMachine:
    OPCODES: Dict[int, Command] = {
        1: {'size': 4, 'function': operator.add},
        2: {'size': 4, 'function': operator.mul},
        3: {'size': 2, 'function': lambda s: s.get_input(), 'method': True},
        4: {'size': 2, 'function': lambda s, v: s.add_output(v), **vmethod},
        5: {'size': 3, 'function': operator.truth, 'jump': True},
        6: {'size': 3, 'function': operator.not_, 'jump': True},
        7: {'size': 4, 'function': lambda x, y: bool(operator.lt(x, y))},
        8: {'size': 4, 'function': lambda x, y: bool(operator.eq(x, y))},
    }

    def __init__(self, code: List[int], inputs: Iterable[int]) -> None:
        self.eip = 0  # Instructions pointer
        self.code = code
        self._inputs = iter(inputs)
        self._outputs_index = 0
        self._outputs: List[int] = []

    @property
    def opcode(self) -> int:
        return self.code[self.eip] % 100

    @property
    def is_halt(self) -> bool:
        return self.opcode == 99

    @property
    def is_jump(self) -> bool:
        return self.opcode_get('jump', False)

    def add_inputs(self, inputs: Union[int, List[int]]) -> None:
        if not isinstance(inputs, (list, tuple)):
            inputs = [inputs]
        self._inputs = itertools.chain(self._inputs, inputs)

    def get_input(self) -> Optional[int]:
        try:
            return next(self._inputs)
        except StopIteration:
            return None

    def add_output(self, outputs: Union[int, List[int]]) -> None:
        if not isinstance(outputs, (list, tuple)):
            outputs = [outputs]
        self._outputs.extend(outputs)

    def get_outputs(self) -> List[int]:
        outputs = self._outputs[self._outputs_index:]
        self._outputs_index = len(self._outputs)
        return outputs

    @property
    def modes(self) -> Tuple[int, int, int]:
        modes_part = self.code[self.eip] // 100
        return modes_part % 10, modes_part // 10 % 10, modes_part // 100

    def opcode_get(self, prop: str, default: Any = None) -> Any:
        return self.OPCODES[self.opcode].get(prop, default)

    @property
    def argc(self) -> int:
        return self.opcode_get('size', 2) - 2

    @property
    def args(self) -> List[int]:
        offset = self.argc + self.opcode_get('void', 0)
        params = self.code[self.eip + 1:self.eip + 1 + offset]
        out = []
        for param, mode in zip(params, self.modes):
            out.append(param if mode else self.code[param])
        if self.opcode_get('method'):
            out.insert(0, self)
        return out

    @property
    def write_address(self) -> Optional[int]:
        if self.opcode_get('void'):
            return None

        write_to = self.code[self.eip + 1 + self.argc]
        is_relative_jump = self.is_jump and self.modes[self.argc] == 0
        return self.code[write_to] if is_relative_jump else write_to

    def __call__(self) -> List[int]:
        while self.opcode != 99:
            op_size = self.opcode_get('size')
            args, write_to = self.args, self.write_address
            returns = self.opcode_get('function')(*args)
            if returns is None and self.opcode == 3:
                return self.get_outputs()  # Halt until you get input
            if write_to is not None and not self.is_jump:
                self.code[write_to] = returns
            should_jump = self.is_jump and returns
            self.eip = write_to if should_jump else (self.eip + op_size)
        return self.get_outputs()


def get_input() -> List[int]:
    with open('input.txt', 'r') as challenge_input:
        return list(map(int, challenge_input.read().strip().split(',')))


# Part 1
program = get_input()
outputs = []
for phases in itertools.permutations(list(range(5))):
    current_input = 0
    for phase in phases:
        current_machine = IntcodeMachine(program, [phase, current_input])
        current_input = current_machine()[-1]
        program = current_machine.code
    outputs.append(current_input)
print(max(outputs))


# Part 2
program = get_input()
max_output = 0
for phases in itertools.permutations(list(range(5, 10))):
    machines = [IntcodeMachine(copy(get_input()), [phase]) for phase in phases]
    next_input = 0
    i = 0
    while not machines[-1].is_halt:
        machines[i].add_inputs(next_input)
        next_input = machines[i]()[-1]
        i = (i + 1) % len(machines)
    max_output = max(max_output, next_input)
print(max_output)
