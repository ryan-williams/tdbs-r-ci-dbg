import click
from click import option


@click.group()
def cli():
    pass


DEFAULT_SINCE = "20240618"
REPO = "single-cell-data/TileDB-SOMA"


since_opt = option("-S", "--since", default=DEFAULT_SINCE)
