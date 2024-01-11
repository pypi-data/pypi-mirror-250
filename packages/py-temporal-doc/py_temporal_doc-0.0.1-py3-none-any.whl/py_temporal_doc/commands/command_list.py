import click
from click import MultiCommand, Path
from dependency_injector.wiring import Provide, inject

from py_temporal_doc.commands.container import Container
from py_temporal_doc.commands.generate_json.core import GenerateJSON


@click.group()
def generate_json() -> None:
    """
    Click group for generate json
    """
    pass


@generate_json.command(name="generate-json")
@click.argument("source", type=Path(exists=True))
@click.argument("destination", default=".", type=Path(exists=True))
@inject
def generate_json_execute(
    source: Path, destination: Path, cls: GenerateJSON = Provide[Container.generate_json]
) -> None:
    """
    Execution of generate diagram CLI command

    Args:
        path: Folder/File path
        cls: Target class of the command

    Returns:
        None
    """
    cls.execute(source=source, destination=destination)


command_list: list[MultiCommand] = [generate_json]  # List of valid commands for CLI
