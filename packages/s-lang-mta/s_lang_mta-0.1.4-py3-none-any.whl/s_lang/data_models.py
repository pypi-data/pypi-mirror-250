from dataclasses import dataclass

Instruction = list[str]
Labels = dict[str, int]


@dataclass
class Code:
    instructions: list[Instruction]
    labels: Labels
