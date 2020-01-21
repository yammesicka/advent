import operator
from enum import IntEnum
from itertools import chain, starmap
from typing import (
    Any, Callable, Dict, Iterable, List, Optional, Tuple, Union,
)

from typing_extensions import TypedDict


Command = TypedDict(
    'Command',
    {
        'size': int, 'function': Callable[..., Any], 'void': bool,
        'method': bool,
    },
    total=False,
)
VOID_METHOD = {'void': True, 'method': True}


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class IntcodeFunc:
    @staticmethod
    def get_input(machine: 'IntcodeMachine') -> Optional[int]:
        return machine.get_input()

    @staticmethod
    def add_output(machine: 'IntcodeMachine', outputs: int) -> None:
        return machine.add_output(outputs)

    @staticmethod
    def jump_if(machine: 'IntcodeMachine', verdict: int, jump_to: int) -> None:
        return machine.jump_if(operator.truth, verdict, jump_to)

    @staticmethod
    def jump_if_not(
            machine: 'IntcodeMachine', verdict: int, jump_to: int,
    ) -> None:
        return machine.jump_if(operator.not_, verdict, jump_to)

    @staticmethod
    def int_lt(a: int, b: int) -> int:
        return int(a < b)

    @staticmethod
    def int_eq(a: int, b: int) -> int:
        return int(a == b)

    @staticmethod
    def relative(machine: 'IntcodeMachine', offset: int) -> None:
        return machine.update_relative(offset)


class IntcodeMachine:
    OPCODES: Dict[int, Command] = {
        1: Command(size=4, function=operator.add),
        2: Command(size=4, function=operator.mul),
        3: Command(size=2, function=IntcodeFunc.get_input, method=True),
        4: Command(size=2, function=IntcodeFunc.add_output, **VOID_METHOD),
        5: Command(size=3, function=IntcodeFunc.jump_if, **VOID_METHOD),
        6: Command(size=3, function=IntcodeFunc.jump_if_not, **VOID_METHOD),
        7: Command(size=4, function=IntcodeFunc.int_lt),
        8: Command(size=4, function=IntcodeFunc.int_eq),
        9: Command(size=2, function=IntcodeFunc.relative, **VOID_METHOD),
        99: Command(size=1, function=lambda: 0, void=True),
    }

    def __init__(self, code: List[int], inputs: Iterable[int]) -> None:
        self.eip = 0  # Instructions pointer
        self.code = code
        self._relative = 0
        self._inputs = iter(inputs)
        self._outputs_index = 0
        self._outputs: List[int] = []
        self._jumped = False

    @property
    def opcode(self) -> int:
        return self.code[self.eip] % 100

    @property
    def is_halt(self) -> bool:
        return self.opcode == 99

    def add_inputs(self, inputs: Union[int, List[int]]) -> None:
        inputs = [inputs] if isinstance(inputs, int) else inputs
        self._inputs = chain(self._inputs, inputs)

    def get_input(self) -> Optional[int]:
        try:
            return next(self._inputs)
        except StopIteration:
            return None

    def add_output(self, outputs: Union[int, List[int]]) -> None:
        outputs = [outputs] if isinstance(outputs, int) else outputs
        self._outputs.extend(outputs)

    def get_outputs(self) -> List[int]:
        outputs = self._outputs[self._outputs_index:]
        self._outputs_index = len(self._outputs)
        return outputs

    def jump_if(
            self, predicate: Callable[..., bool], arg: int, jump_address: int,
    ) -> None:
        if predicate(arg):
            self.eip = jump_address
            self._jumped = True

    @property
    def modes(self) -> Tuple[int, int, int]:
        modes_part = self.code[self.eip] // 100
        return modes_part % 10, modes_part // 10 % 10, modes_part // 100

    def opcode_get(self, prop: str, default: Any = None) -> Any:
        return self.OPCODES[self.opcode].get(prop, default)

    @property
    def argc(self) -> int:
        return self.opcode_get('size', 2) - 2

    def update_relative(self, offset: int) -> None:
        self._relative += offset

    def resize_to_index(self, index: int) -> None:
        self.code.extend([0] * (index - len(self.code) + 1))

    def parse_read_args(self, param: int, mode: int) -> int:
        if mode == Mode.IMMEDIATE:
            return param

        elif mode == Mode.POSITION:
            index = param
        elif mode == Mode.RELATIVE:
            index = param + self._relative

        self.resize_to_index(index)
        return self.code[index]

    def parse_write_args(self, write_address: int, mode: int) -> int:
        if mode == Mode.RELATIVE:
            write_address = write_address + self._relative

        self.resize_to_index(write_address)
        return write_address

    @property
    def args(self) -> List[int]:
        # In void function the last parameter is not write address
        offset = self.argc + int(self.opcode_get('void', False))
        params = self.code[self.eip + 1:self.eip + 1 + offset]
        out = [self] if self.opcode_get('method') else []
        out.extend(starmap(self.parse_read_args, zip(params, self.modes)))
        return out

    @property
    def write_address(self) -> Optional[int]:
        if self.opcode_get('void'):
            return None

        write_to = self.code[self.eip + 1 + self.argc]
        mode = self.modes[self.argc]
        return self.parse_write_args(write_to, mode)

    def write(self, value: int) -> None:
        if self.write_address is None:
            return
        self.resize_to_index(self.write_address)
        self.code[self.write_address] = value

    def next_instruction(self, return_value: int) -> int:
        self.eip = self.eip + self.opcode_get('size')
        return self.eip

    def debug(self, return_value=None):
        print('-' * 40)
        print(f'Address:         0x{self.eip}')
        full_code = self.code[self.eip:self.opcode_get('size') + self.eip]
        print(f'Full code:       {full_code}')
        print(f'Opcode:          {self.opcode}')
        print(f'Args:            {self.args}')
        print(f'Write address:   {self.write_address}')
        if return_value is not None:
            print(f'Return value:    {return_value}')
        print(f'Relative status: {self._relative}')
        print(self._outputs)
        print('-' * 40)

    def __call__(self) -> List[int]:
        while not self.is_halt:
            self._jumped = False
            return_value = self.opcode_get('function')(*self.args)
            if not self._jumped:
                if return_value is None and self.opcode == 3:
                    return self.get_outputs()  # Halt until you get input
                self.write(return_value)
                self.next_instruction(return_value)
        return self.get_outputs()


def get_input() -> List[int]:
    with open('input.txt', 'r') as challenge_input:
        return list(map(int, challenge_input.read().strip().split(',')))


program = get_input()
current_machine = IntcodeMachine(program, [2])
print(current_machine())
