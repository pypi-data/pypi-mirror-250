from s_lang.data_models import Code
from s_lang.variables_store import VariablesStore
from s_lang.instructions import exec_instruction


class Runner:
    def __init__(self, code: Code, inputs: list[int]):
        self.code: Code = code
        self.variables: VariablesStore = VariablesStore(inputs)
        self.pc: int = 0

    def run(self) -> int:
        prog_len = len(self.code.instructions)

        while 0 <= self.pc < prog_len:
            self.pc = exec_instruction(
                pc=self.pc,
                inst=self.code.instructions[self.pc],
                labels=self.code.labels,
                variables=self.variables
            )

        return self.variables.y
