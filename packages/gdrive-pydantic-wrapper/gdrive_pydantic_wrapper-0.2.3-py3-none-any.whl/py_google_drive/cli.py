"""Console script for py_google_drive."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("py-google-drive")
    click.echo("=" * len("py-google-drive"))
    click.echo("Skeleton project created by Cookiecutter PyPackage")


if __name__ == "__main__":
    main()  # pragma: no cover
