from collections import defaultdict


class VariablesStore:
    def __init__(self, inputs: list[int] | None = None):
        self.x: dict[int, int] = defaultdict(int)
        self.z: dict[int, int] = defaultdict(int)
        self.y: int = 0

        inputs = inputs or []

        for idx, val in enumerate(inputs, start=1):
            self.x[idx] = val

    def __getitem__(self, var: str) -> int:
        v_type, v_idx = self._parse_var(var)

        if v_type == "Y":
            return self.y

        return self._get_var_type(v_type)[v_idx]

    def __setitem__(self, var: str, value: int) -> None:
        v_type, v_idx = self._parse_var(var)

        if v_type == "Y":
            self.y = value
        else:
            self._get_var_type(v_type)[v_idx] = value

    def _get_var_type(self, v_type: str) -> dict[int, int] | None:
        if v_type == "X":
            return self.x
        elif v_type == "Z":
            return self.z

    @staticmethod
    def _parse_var(string: str) -> tuple[str, int]:
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
