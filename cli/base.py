import re
from os import listdir

import click
from click import option
from utz import YMD


@click.group()
def cli():
    pass


DEFAULT_SINCE = "20240618"
DEFAULT_RUNS_FILE = f"runs-since-{DEFAULT_SINCE}.jsonl"
REPO = "single-cell-data/TileDB-SOMA"


def parse_ymd(ctx, param, value: str) -> YMD:
    return YMD(value) if value else None


overwrite_opt = option('-f', '--overwrite', is_flag=True)
n_jobs_opt = option('-j', '--n-jobs', type=int, default=0, help="Number of parallel jobs; \"1\" to disable parallelism")


def out_dir_opt(default: str):
    return option('-o', '--out-dir', default=default)


since_opt = option("-S", "--since", default=DEFAULT_SINCE, callback=parse_ymd, help="Only consider runs since this date")


def load_db_ids(dir: str) -> list[int]:
    return [
        int(re.match(r"(\d+)$", path).group(1))
        for path in listdir(dir)
    ]
