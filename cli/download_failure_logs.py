from os import makedirs
from os.path import exists
from typing import Optional

import jsonlines
from click import option, argument
from utz import err, parallel, process, YMD

from .base import cli, DEFAULT_SINCE, REPO, since_opt, overwrite_opt, n_jobs_opt, out_dir_opt

# Runs omitted due to unrelated failures:
# - [10113090142]: all jobs failed: `No valid versions of tiledb-r found`
# - [10306622414]: workflow file syntax error, no logs produced
#
# [10113090142]: https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10113090142
# [10306622414]: https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10306622414
DEFAULT_SKIPS = [
    10113090142,
    10306622414,
]


FAIL_LOGS_DIR = 'log-failed'


@cli.command
@overwrite_opt
@n_jobs_opt
@out_dir_opt(FAIL_LOGS_DIR)
@since_opt
@argument('runs-file', required=False)
def download_failure_logs(
    overwrite: bool,
    n_jobs: int,
    out_dir: str,
    since: YMD,
    runs_file: Optional[str],
):
    """Download logs for failed runs since a given date."""
    if not runs_file:
        runs_file = f"runs-since-{DEFAULT_SINCE}.jsonl"

    with open(runs_file, "r") as f:
        with jsonlines.Reader(f) as lines:
            runs = list(lines)

    runs = [
        run
        for run in runs
        if (
            run['conclusion'] == 'failure'
            and run['databaseId'] not in DEFAULT_SKIPS
            and (not since or run['createdAt'] > since.str('-'))
        )
    ]
    makedirs(out_dir, exist_ok=True)

    def download_run_logs(run, overwrite=overwrite):
        db_id = run['databaseId']
        out_path = f"{out_dir}/{db_id}"

        if exists(out_path):
            if overwrite:
                err(f"Downloading {db_id} (overwriting)")
            else:
                err(f"Skipping {db_id} (already exists)")
                return
        else:
            err(f"Downloading {db_id}")

        with open(out_path, "w") as f:
            process.run(
                "gh", "run",
                "-R", REPO,
                "view", db_id,
                "--log-failed",
                stdout=f,
            )

    parallel(runs, download_run_logs, n_jobs=n_jobs)
