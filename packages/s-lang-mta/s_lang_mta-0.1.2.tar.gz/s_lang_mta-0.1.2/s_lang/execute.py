from collections import defaultdict
from dataclasses import dataclass, field

from s_lang.data_types import Code, Labels, Instruction
from s_lang.parse import parse_var, is_label_valid

Variable = tuple[str, int]


@dataclass
class Variables:
    x: dict[int, int] = field(default_factory=lambda: defaultdict(int))
    z: dict[int, int] = field(default_factory=lambda: defaultdict(int))
    y: int = 0


def init_input_vars(variables: Variables, input_vars: list[int]) -> None:
    for i, val in enumerate(input_vars):
        idx = i + 1
        variables.x[idx] = val


def create_run_variables(input_vars: list[int]) -> Variables:
    variables = Variables()
    init_input_vars(variables, input_vars)

    return variables


def inc_var(variables: Variables, var: Variable) -> None:
    ch, idx = var

    if ch == "X":
        variables.x[idx] += 1
    elif ch == "Z":
        variables.z[idx] += 1
    else:
        variables.y += 1


def dec_var(variables: Variables, var: Variable) -> None:
    ch, idx = var

    if ch == "X":
        variables.x[idx] = max(variables.x[idx] - 1, 0)
    elif ch == "Z":
        variables.z[idx] = max(variables.z[idx] - 1, 0)
    else:
        variables.y = max(variables.y - 1, 0)


def if_nez_goto(variables: Variables, labels: Labels, var: Variable, label: str, pc: int) -> int:
    ch, idx = var

    if ch == "X":
        val = variables.x[idx]
    elif ch == "Z":
        val = variables.z[idx]
    else:
        val = variables.y

    return labels.get(label, -1) if 0 < val else pc + 1


def exec_instruction(pc: int, inst: Instruction, labels: Labels, variables: Variables) -> int:
    match inst:
        case [v1, "<-", v2] if v1 == v2:
            return pc + 1

        case [v1, "<-", v2, "+", "1"] if v1 == v2:
            var = parse_var(v1)
            inc_var(variables, var)
            return pc + 1

        case [v1, "<-", v2, "-", "1"] if v1 == v2:
            var = parse_var(v1)
            dec_var(variables, var)
            return pc + 1

        case ["IF", v, "!=", "0", "GOTO", l]:
            if not is_label_valid(l):
                raise Exception(f"Syntax error at line {pc}: {' '.join(inst)}\ninvalid label")

            var = parse_var(v)
            return if_nez_goto(variables, labels, var, l, pc)

        case _:
            raise Exception(f"Syntax error at line {pc}: {' '.join(inst)}")


def exec_code(code: Code, input_vars: list[int]) -> int:
    instructions, labels = code
    variables = create_run_variables(input_vars)
    pc = 0
    prog_len = len(instructions)

    while 0 <= pc < prog_len:
        pc = exec_instruction(pc, instructions[pc], labels, variables)

    return variables.y
