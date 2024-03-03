from typing import Union, cast

from directives import Org, Label, Directive, Equ, MemoryDirective, AddressDirective
from expression import ExprContext, Expression
from z80.instructions import Instruction
from z80.instructions.instruction_def import MemoryDetail


def to_int(s: str, negative: bool = False) -> int:
    if s.endswith("h"):
        value = int(s[:-1], 16)
    elif s.startswith("0x"):
        value = int(s[2:], 16)
    elif s.startswith("$-"):
        value = int(s[2:], 16)
    elif s.startswith("$"):
        value = int(s[1:], 16)
    else:
        try:
            value = int(s)
        except ValueError:
            raise ValueError(f"Cannot convert to it '{s}'")

    if negative:
        value = - value

    return value


def second_pass(instructions: list[Union[Instruction, Directive]]) -> None:
    context = ExprContext()

    pc = 0
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        if isinstance(instruction, MemoryDetail):
            instruction.address = pc
            pc += instruction.size()
        elif isinstance(instruction, Org):
            instruction.second_pass(context)
            pc = instruction.address
        elif isinstance(instruction, Label):
            if i + 1 < len(instructions) and isinstance(instructions[i + 1], Equ):
                pass
            else:
                context.add_label(instruction.label, pc)
                instruction.address = pc
        i += 1

    for name in context.labels:
        value = context.labels[name]
        if isinstance(value, Expression):
            context.labels[name] = value.evaluate(context)

    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        if isinstance(instruction, Equ):
            if i == 0:
                raise ValueError(f"EQU without label at line {instruction.line}")

            if isinstance(instructions[i - 1], Label):
                label: Label = cast(Label, instructions[i - 1])
                instruction.label = label.label
                del instructions[i - 1]
                instruction.second_pass(context)
            else:
                raise ValueError(f"EQU without label at line {instruction.line}")
        elif isinstance(instruction, MemoryDirective):
            instruction.second_pass(context)
            i += 1
        elif isinstance(instruction, Directive):
            instruction.second_pass(context)
            i += 1
        else:
            i += 1

    for instruction in instructions:
        context.current_instruction = instruction
        if isinstance(instruction, Instruction):
            for p_key in instruction.params:
                expr = instruction.params[p_key]
                if isinstance(expr, Expression):
                    instruction.params[p_key] = expr.evaluate(context)

            params = instruction.params
            for element in instruction.addr_mode.addr_mode_elements:
                if element.relative():
                    params[element.param_name()] = params[element.param_name()] - (instruction.address + instruction.size())


def assembler_output(instructions: list[Instruction]) -> None:
    has_label = False
    for instruction in instructions:
        if isinstance(instruction, Label):
            label = cast(Label, instruction)
            print(f"0x{instruction.address:04x} {label.label:12} ", end="")
            has_label = True
        elif isinstance(instruction, Instruction):
            if has_label:
                print(f"{instruction.to_str(2).strip()}")
                has_label = False
            else:
                print(f"0x{instruction.address:04x}              {instruction.to_str(2).strip()}")
        elif isinstance(instruction, MemoryDirective):
            if has_label:
                print(f"{instruction.to_str(2).strip()}")
                has_label = False
            else:
                print(f"0x{instruction.address:04x}              {instruction.to_str(2).strip()}")
        elif isinstance(instruction, Equ):
            equ = cast(Equ, instruction)
            print(f"       {equ.label:12} {equ.to_str(2)}")
        elif isinstance(instruction, AddressDirective):
            if has_label:
                print(f"{instruction.to_str(2)}")
                has_label = False
            else:
                print(f"0x{instruction.address:04x}              {instruction.to_str(2)}")
        else:
            print(f"                    {instruction.to_str(2)}")
    print()


def populate_memory(instructions: list[Instruction], memory: bytes) -> tuple[int, int]:
    mem_min = 65536
    mem_max = 0
    for instruction in instructions:
        if isinstance(instruction, Instruction):
            p = instruction.address
            s = instruction.addr_mode.size()

        elif isinstance(instruction, MemoryDirective):
            if has_label:
                print(f"{instruction.to_str(2).strip()}")
                has_label = False
            else:
                print(f"0x{instruction.address:04x}              {instruction.to_str(2).strip()}")
        elif isinstance(instruction, Equ):
            equ = cast(Equ, instruction)
            print(f"       {equ.label:12} {equ.to_str(2)}")
        elif isinstance(instruction, AddressDirective):
            if has_label:
                print(f"{instruction.to_str(2)}")
                has_label = False
            else:
                print(f"0x{instruction.address:04x}              {instruction.to_str(2)}")
        else:
            print(f"                    {instruction.to_str(2)}")
    return mem_min, mem_max
