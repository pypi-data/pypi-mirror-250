import re

from s_lang.data_types import Instruction, Code, Labels


def is_label_valid(label: str) -> bool:
    ch = label[0]
    idx = label[1:]
    idx = idx or "1"

    if not ch.isalpha() or not ch.isupper():
        return False

    if not idx.isnumeric():
        return False

    return 0 < int(idx)


def parse_var(string: str) -> tuple[str, int]:
    var_char: str = string[0]
    var_idx_str: str = string[1:]

    if var_char not in ("X", "Z", "Y") or (var_char == "Y" and var_idx_str):
        raise ValueError("Invalid variable name")

    var_idx_str = var_idx_str or "1"

    if not var_idx_str.isnumeric():
        raise ValueError("Invalid variable name")

    var_idx = int(var_idx_str)

    if var_idx <= 0:
        raise ValueError("Invalid variable name")

    return var_char, var_idx


def read_lines(code: str) -> list[str]:
    return [line.rstrip() for line in code.split("\n")]


def parse_code(code: str) -> Code:
    code = code.strip()
    code_lines: list[str] = read_lines(code)
    instructions: list[Instruction] = []
    labels: Labels = {}

    for i, line in enumerate(code_lines):
        line = line.strip()
        parts = re.split(r"^\[([A-Z]\d*)\] ", line, maxsplit=1)

        if 1 < len(parts):
            inst = parts[2]
            labels[parts[1]] = i
        else:
            inst = parts[0]

        inst_parts = re.split(r"\s+", inst)
        instructions.append(inst_parts)

    return instructions, labels
