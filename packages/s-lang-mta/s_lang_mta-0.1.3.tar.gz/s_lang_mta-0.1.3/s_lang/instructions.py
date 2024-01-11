from s_lang.data_models import Labels, Instruction
from s_lang.variables_store import VariablesStore
from s_lang.parse import is_label_valid


def inc_var(variables: VariablesStore, var: str, pc: int) -> int:
    variables[var] += 1

    return pc + 1


def dec_var(variables: VariablesStore, var: str, pc: int) -> int:
    variables[var] = max(variables[var] - 1, 0)

    return pc + 1


def if_nez_goto(variables: VariablesStore, labels: Labels, var: str, label: str, pc: int) -> int:
    if not is_label_valid(label):
        raise ValueError(f"invalid label")

    val = variables[var]
    labels_target = labels.get(label, -1)

    return labels_target if 0 < val else pc + 1


def add_k(variables: VariablesStore, var: str, k: int, pc: int) -> int:
    if k < 1:
        raise ValueError("invalid const")

    variables[var] += k

    return pc + 1


def sub_k(variables: VariablesStore, var: str, k: int, pc: int) -> int:
    if k < 1:
        raise ValueError("invalid const")

    variables[var] -= k

    return pc + 1


def if_ez_goto(variables: VariablesStore, labels: Labels, var: str, label: str, pc: int) -> int:
    if not is_label_valid(label):
        raise ValueError(f"invalid label")

    val = variables[var]
    labels_target = labels.get(label, -1)

    return labels_target if 0 == val else pc + 1


def goto(labels: Labels, label: str) -> int:
    if not is_label_valid(label):
        raise ValueError(f"invalid label")

    labels_target = labels.get(label, -1)

    return labels_target


def exec_instruction(pc: int, inst: Instruction, labels: Labels, variables: VariablesStore) -> int:
    try:
        match inst:
            # basic syntax:

            case [v1, "<-", v2] if v1 == v2:
                return pc + 1

            case [v1, "<-", v2, "+", "1"] if v1 == v2:
                return inc_var(variables, v1, pc)

            case [v1, "<-", v2, "-", "1"] if v1 == v2:
                return dec_var(variables, v1, pc)

            case ["IF", v, "!=", "0", "GOTO", l]:
                return if_nez_goto(variables, labels, v, l, pc)

            # syntactic sugars:

            case [v1, "<-", v2, "+", k] if v1 == v2 and isinstance(k, str) and k.isnumeric():
                return add_k(variables, v1, int(k), pc)

            case [v1, "<-", v2, "-", k] if v1 == v2 and isinstance(k, str) and k.isnumeric():
                return sub_k(variables, v1, int(k), pc)

            case ["IF", v, "=", "0", "GOTO", l]:
                return if_ez_goto(variables, labels, v, l, pc)

            case ["GOTO", l]:
                return goto(labels, l)

            case _:
                raise ValueError("unknown command")

    except Exception as err:
        raise Exception(f"Syntax error at line {pc}: {' '.join(inst)}\n{err}")
