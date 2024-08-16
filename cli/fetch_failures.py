from contextlib import contextmanager
from re import fullmatch
from sys import stdout

import jsonlines
from click import option, Choice, argument
from utz import process

from .base import cli


@contextmanager
def stdout_context():
    yield stdout


@cli.command("fetch-failures")
@option('-b', '--branch', default='main')
@option('-c', '--conclusion', type=Choice(['success', 'failure', '']), default='failure')
@option('-m', '--max-runs', type=int, default=200)
@option("-s", "--since", default="20240618")
@argument('out-path')
def fetch_failures(branch, conclusion, max_runs, since, out_path):
    if since:
        m = fullmatch(r'(?P<y>\d{4})-?(?P<m>\d{2})-?(?P<d>\d{2})', since)
        if not m:
            raise ValueError(f"Invalid date format: {since}")
        yyyy = m['y']
        mm = m['m'] or '01'
        dd = m['d'] or '01'
        since0 = f"{yyyy}{mm}{dd}"
        since1 = f"{yyyy}-{mm}-{dd}"
    else:
        since0 = since1 = None

    runs = process.json(
        "gh", "run",
        "-R", "single-cell-data/TileDB-SOMA",
        "list",
        "-w", "r-ci.yml",
        *(["-b", branch] if branch else []),
        "-L", max_runs,
        *(['-s', conclusion] if conclusion else []),
        "--json", "number,databaseId,conclusion,createdAt",
    )
    if since1:
        runs = [run for run in runs if run['createdAt'] > since1]

    if not out_path:
        out_path = f'failures-since'
        if since0:
            out_path += f'-{since0}'
        out_path += '.jsonl'
    with stdout_context() if out_path == '-' else open(out_path, 'w') as file:
        writer = jsonlines.Writer(file, compact=True)
        writer.write_all(runs)
        writer.close()
