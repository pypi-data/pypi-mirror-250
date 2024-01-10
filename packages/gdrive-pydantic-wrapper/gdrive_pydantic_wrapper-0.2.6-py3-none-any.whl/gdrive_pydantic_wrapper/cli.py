"""Console script for gdrive_pydantic_wrapper."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("gdrive-pydantic-wrapper")
    click.echo("=" * len("gdrive-pydantic-wrapper"))
    click.echo("Skeleton project created by Cookiecutter PyPackage")


if __name__ == "__main__":
    main()  # pragma: no cover
