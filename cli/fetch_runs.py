from contextlib import contextmanager
from re import fullmatch
from sys import stdout
from typing import Optional

import jsonlines
from click import option, argument
from utz import process

from .base import cli


@contextmanager
def stdout_context():
    yield stdout


DEFAULT_SINCE = "20240618"


@cli.command("fetch-runs")
@option('-b', '--branch', default='main')
@option('-m', '--max-runs', type=int, default=200)
@option('-r', '--reverse-chron', is_flag=True)
@option('-s', '--status', 'statuses', multiple=True, default=('success', 'failure'))
@option("-S", "--since", default=DEFAULT_SINCE)
@argument('out-path', required=False)
def fetch_runs(branch, max_runs, reverse_chron, statuses, since, out_path):
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

    if statuses == ('',):
        statuses = ()

    def fetch_for_status(status: Optional[str] = None) -> list[dict]:
        return process.json(
            "gh", "run",
            "-R", "single-cell-data/TileDB-SOMA",
            "list",
            "-w", "r-ci.yml",
            *(["-b", branch] if branch else []),
            "-L", max_runs,
            *(['-s', status] if status else []),
            "--json", "number,databaseId,conclusion,createdAt",
        )

    if statuses:
        runs = []
        for status in statuses:
            runs.extend(fetch_for_status(status))
    else:
        runs = fetch_for_status()

    runs.sort(key=lambda run: run['createdAt'], reverse=reverse_chron)

    if since1:
        runs = [run for run in runs if run['createdAt'] > since1]

    if not out_path:
        prefix = "failures" if statuses == ('failure',) else "successes" if statuses == ('success',) else "runs"
        out_path = f'{prefix}-since'
        if since0:
            out_path += f'-{since0}'
        out_path += '.jsonl'
    with stdout_context() if out_path == '-' else open(out_path, 'w') as file:
        writer = jsonlines.Writer(file, compact=True)
        writer.write_all(runs)
        writer.close()
