import click

from py_temporal_doc.commands import container as CommandContainer
from py_temporal_doc.commands.command_list import command_list


def setup_containers():
    # Initialize containers
    command_container = CommandContainer.Container()


def startup_cli():
    # Initialize Command
    cli = click.CommandCollection(sources=command_list)
    cli()


# For running the non compiled version
if __name__ == "__main__":
    setup_containers()
    startup_cli()


# For compiled version
def main():
    setup_containers()
    startup_cli()
