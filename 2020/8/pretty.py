from enum import IntEnum
from itertools import chain
from typing import (
    Any, Callable, Dict, Iterable, List, NamedTuple, Optional, Set, Union,
)

from typing_extensions import TypedDict


Command = TypedDict(
    'Command',
    {'func': Callable[..., Any], 'void': bool, 'method': bool},
    total=False,
)
VOID_METHOD = {'void': True, 'method': True}


class Operation(NamedTuple):
    name: str
    params: List[int]


CodeType = List[Operation]


class ConsoleFunc:
    @staticmethod
    def jump(machine: 'GameConsole', jump_to: int) -> None:
        return machine.jump_if(bool, True, jump_to, relative=True)

    @staticmethod
    def add(machine: 'GameConsole', *params: int) -> int:
        return sum([machine.read_output(), *params])

    @staticmethod
    def sub(machine: 'GameConsole', *params: int) -> int:
        return machine.read_output() - params[0]


class GameConsole:
    OPCODES: Dict[str, Command] = {
        'acc': Command(func=ConsoleFunc.add, method=True),
        'jmp': Command(func=ConsoleFunc.jump, **VOID_METHOD),
        'nop': Command(func=lambda *_: 0, void=True),
    }

    def __init__(self, code: Iterable[str], inputs: Iterable[int]) -> None:
        self.eip = 0  # Instructions pointer
        self.code: CodeType = []
        self._preparsed_code = code
        self._inputs = iter(inputs)
        self._outputs_index = -1
        self._outputs: List[int] = []
        self._jumped = False
        self._visited: Set[int] = set()
        if code:
            self.parse_code()

    def parse_code(self) -> None:
        for line in self._preparsed_code:
            name, _, preparsed_params = line.partition(' ')
            params = [int(param) for param in preparsed_params.split()]
            self.code.append(Operation(name, params))

    @property
    def command(self):
        return self.code[self.eip]

    @property
    def opcode(self) -> str:
        return self.command.name

    @property
    def is_halt(self) -> bool:
        return self.eip in self._visited or self.eip >= len(self.code)

    @property
    def is_ok(self) -> bool:
        return self.eip >= len(self.code)

    def add_inputs(self, inputs: Union[int, List[int]]) -> None:
        inputs = [inputs] if isinstance(inputs, int) else inputs
        self._inputs = chain(self._inputs, inputs)

    def get_input(self) -> Optional[int]:
        try:
            return next(self._inputs)
        except StopIteration:
            return None

    def read_output(self, index: Optional[int] = None) -> int:
        read_from = index if index is not None else self._outputs_index
        return self._outputs[read_from]

    def add_output(self, outputs: Union[int, List[int]]) -> None:
        outputs = [outputs] if isinstance(outputs, int) else outputs
        self._outputs.extend(outputs)
        self._outputs_index += len(outputs)

    def write_value(self, output: int):
        output_shortage = self._outputs_index - len(self._outputs) + 1
        if output_shortage > 0:
            self.add_output([0] * output_shortage)
        self._outputs[self._outputs_index] = output

    def jump_if(
        self,
        predicate: Callable[..., bool], arg: int,
        jump_address: int, relative: bool = True,
    ) -> None:
        if relative:
            jump_address += self.eip

        if predicate(arg):
            self.eip = jump_address
            self._jumped = True

    def opcode_get(self, prop: str, default: Any = None) -> Any:
        return self.OPCODES[self.opcode].get(prop, default)

    def resize_to_index(self, index: int) -> None:
        nop = Operation(name='nop', params=[0])
        self.code.extend([nop] * (index - len(self.code) + 1))

    @property
    def args(self) -> List[Union[int]]:
        params = self.command.params
        if self.opcode_get('method', False):
            params = [self, *params]
        return params

    @property
    def argc(self) -> int:
        return len(self.args)

    @property
    def act(self) -> Callable:
        return self.opcode_get('func')

    def flip_instruction(self, between: Set[str], start: int) -> int:
        for index, operation in enumerate(self.code[start:], start):
            if operation.name in between:
                swapped_op = (between ^ set([operation.name])).pop()
                self.code[index] = Operation(swapped_op, operation.params)
                return index + 1
        return -1

    def next_instruction(self) -> int:
        self.eip = self.eip + 1
        return self.eip

    def debug(self, return_value=None):
        print('-' * 40)
        print(f'Address:         0x{self.eip}')
        print(f'Opcode:          {self.opcode}')
        print(f'Args:            {self.args}')
        print(f'Write address:   {self._outputs_index}')
        if return_value is not None:
            print(f'Return value:    {return_value}')
        print(self._outputs)
        print('-' * 40)

    def __call__(self) -> List[int]:
        self.add_output(0)
        while not self.is_halt:
            self._jumped = False
            self._visited.add(self.eip)
            return_value = self.act(*self.args)
            if not self._jumped:
                if not self.opcode_get('void', False):
                    self.write_value(return_value)
                self.next_instruction()
        return self._outputs


def get_input() -> Iterable[str]:
    with open('input.txt', 'r') as challenge_input:
        yield from challenge_input


# Part A
program = get_input()
current_machine = GameConsole(program, [])
print(current_machine())

# Part B
program = list(get_input())
flip_between = {'jmp', 'nop'}
is_ok = False
next_change = 0
while not is_ok:
    try_console = GameConsole(program, [])
    next_change = try_console.flip_instruction(flip_between, start=next_change)
    output = try_console()
    is_ok = try_console.is_ok

print(output)
