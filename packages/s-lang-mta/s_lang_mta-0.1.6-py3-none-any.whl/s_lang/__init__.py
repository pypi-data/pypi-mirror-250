from s_lang.data_models import Code as _Code
from s_lang.parse import parse_code as _parse_code
from s_lang.runner import Runner as _Runner

__all__ = ["run"]


def run(code: str, inputs: list[int]) -> int:
    parsed_code: _Code = _parse_code(code)
    result: int = _Runner(parsed_code, inputs).run()

    return result
