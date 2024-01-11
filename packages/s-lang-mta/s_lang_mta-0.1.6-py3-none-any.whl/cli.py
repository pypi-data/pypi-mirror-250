from importlib import metadata

import typer

from s_lang import run as run_code


def read_file(path: str) -> str:
    with open(path, mode="r") as file:
        return file.read()


app = typer.Typer()
__version__ = metadata.version("s_lang_mta")


def version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def callback(
    _: bool = typer.Option(False, "--version", "-v", callback=version_callback)
) -> None:
    ...


@app.command()
def run(
    path: str = typer.Argument(help="Path to S lang code to run"),
    inputs: list[int] = typer.Option(None, "--input", "-i", help="Input variables"),
) -> None:
    inputs = inputs or []
    code = read_file(path)

    result: int = run_code(code, inputs)
    typer.echo(f">>> {result}")
