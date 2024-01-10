# s-lang
s-lang interpreter

Basic usage:
```python
from s_lang import run


def main() -> None:
    inputs = [5]
    code = """
Z <- Z + 1
[A] IF X != 0 GOTO B
IF Z != 0 GOTO E
[B] Y <- Y + 1
X <- X - 1
IF Z != 0 GOTO A
"""

    result: int = run(code, inputs)
    print(result) 


if __name__ == "__main__":
    main()

```
