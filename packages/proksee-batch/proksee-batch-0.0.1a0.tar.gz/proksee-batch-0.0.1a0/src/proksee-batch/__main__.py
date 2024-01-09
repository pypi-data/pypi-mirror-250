"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Proksee Batch."""
    print("Hello world, I am proksee-batch (prerelease)!")


if __name__ == "__main__":
    main(prog_name="proksee-batch")  # pragma: no cover
