import click
from ttracker.cli_factory import command_factory


def main():
    c = command_factory()
    try:
        c()
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red")
