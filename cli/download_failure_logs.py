from os import makedirs
from os.path import exists

import jsonlines
from click import option, argument
from utz import err, parallel, process

from .base import cli, DEFAULT_SINCE, REPO, since_opt

# Runs omitted due to unrelated failures:
# - 10113090142: all jobs failed: `No valid versions of tiledb-r found`
# - 10306622414: workflow file syntax error, no logs produced
DEFAULT_SKIPS = [
    10113090142,
    10306622414,
]


@cli.command("download-failure-logs")
@option('-f', '--overwrite', is_flag=True)
@option('-o', '--out-dir', default='log-failed')
@since_opt
@argument('runs-file', required=False)
def download_failure_logs(overwrite, out_dir, since, runs_file):
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
            and not since or run['createdAt'] > since
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

    parallel(runs, download_run_logs)
