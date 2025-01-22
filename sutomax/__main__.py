import click
from .funcmodule import session


@click.command()
def main():
    """This is a normal script. The design is very human."""
    session()


if __name__ == '__main__':
    main()