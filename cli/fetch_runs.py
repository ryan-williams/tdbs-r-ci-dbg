import json
from contextlib import contextmanager
from sys import stdout
from typing import Optional

import jsonlines
from click import option, argument
from utz import process, YMD, now

from .base import cli, since_opt, REPO


@contextmanager
def stdout_context():
    yield stdout


@cli.command
@option('-b', '--branch', default='main')
@option('-m', '--max-runs', type=int, default=200)
@option('-r', '--reverse-chron', is_flag=True)
@option('-s', '--status', 'statuses', multiple=True, default=('success', 'failure'))
@since_opt
@argument('out-path', required=False)
def fetch_runs(branch, max_runs, reverse_chron, statuses, since, out_path):
    """Fetch runs of the r-ci.yml workflow."""
    if since:
        since = YMD(since)

    if statuses == ('',):
        statuses = ()

    def fetch_for_status(status: Optional[str] = None) -> list[dict]:
        return process.json(
            "gh", "run",
            "-R", REPO,
            "list",
            "-w", "r-ci.yml",
            *(["-b", branch] if branch else []),
            "-L", max_runs,
            *(['-s', status] if status else []),
            "--json", "number,databaseId,conclusion,createdAt",
        )

    now_str = f'{now()}'
    if statuses:
        runs = []
        for status in statuses:
            runs.extend(fetch_for_status(status))
    else:
        runs = fetch_for_status()

    runs.sort(key=lambda run: run['createdAt'], reverse=reverse_chron)

    if since:
        runs = [ run for run in runs if run['createdAt'] > since.str('-') ]

    if not out_path:
        prefix = "failures" if statuses == ('failure',) else "successes" if statuses == ('success',) else "runs"
        out_path = f'{prefix}-since'
        if since:
            out_path += f'-{since}'
        out_path += '.jsonl'

    with stdout_context() if out_path == '-' else open(out_path, 'w') as file:
        writer = jsonlines.Writer(file, compact=True)
        writer.write_all(runs)
        writer.close()

    if out_path != '-':
        assert out_path.endswith('.jsonl')
        metadata_path = out_path[:-1]
        with open(metadata_path, 'w') as f:
            json.dump({ 'fetched_at': now_str }, f, indent=2)
