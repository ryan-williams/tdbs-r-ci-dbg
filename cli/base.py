import click
from click import option
from utz import YMD


@click.group()
def cli():
    pass


DEFAULT_SINCE = "20240618"
REPO = "single-cell-data/TileDB-SOMA"


def parse_ymd(ctx, param, value: str) -> YMD:
    return YMD(value) if value else None


overwrite_opt = option('-f', '--overwrite', is_flag=True)
njobs_opt = option('-j', '--n-jobs', type=int, default=0, help="Number of parallel jobs; \"1\" to disable parallelism")
since_opt = option("-S", "--since", default=DEFAULT_SINCE, callback=parse_ymd, help="Only consider runs since this date")
