from s_lang.data_types import Code as _Code
from s_lang.parse import parse_code as _parse_code
from s_lang.execute import exec_code as _exec_code

__all__ = ["run"]


def run(code: str, inputs: list[int]) -> int:
    parsed_code: _Code = _parse_code(code)
    result: int = _exec_code(parsed_code, inputs)

    return result
