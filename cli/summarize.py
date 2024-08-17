import json
import re
from contextlib import contextmanager, nullcontext
from functools import partial
from hashlib import sha256
from io import StringIO
from os import environ as env

import jsonlines
from click import option
from utz import process, err, singleton

from .base import cli, load_db_ids, DEFAULT_RUNS_FILE, TDBS, GH_ISSUE_NUM, DEFAULT_METADATA_FILE, REPO
from .normalize_errors import NORMALIZED_DIR

NAMES = {
    "d6cfe842dc246ac67c8b8fb341c4d09a24e05e01e0f05bb9a1f7366aa55240e5": "memory not mapped",
    "cbfb6cc1965c610935cfb56476ac66eb1e10db7f79b54238e85453ac11caa267": "invalid permissions",
    "12898a26fbbae699e8555eeda71f5dd25f6aecc56664eea2aa690cf2d190b4c7": "address (nil), cause 'unknown'",
    "67c6c7e284af1c81625ba210bd9de40c4571c0bf7479ea87ede16c5726d585a1": "bad_function_call",
}


@contextmanager
def readme_sub_ctx():
    with open("README.md", "r") as readme_ctx:
        readme_lines = iter([ line.rstrip("\n") for line in readme_ctx.readlines() ])
    file = open("README.md", "w")
    write = partial(print, file=file)
    try:
        for line in readme_lines:
            write(line)
            if line == "<!-- summary -->":
                yield file
                break
    finally:
        for line in readme_lines:
            if line == "<!-- /summary -->":
                write(line)
                break
        for line in readme_lines:
            write(line)


def update_issue(
    issue: int,
    summary_str: str,
    fetched_at: str,
    header_level: int,
    runs_since_5442: list[dict],
    quiet: bool,
    dry_run: bool,
):
    body = singleton(
        process.json(
            'gh', 'issue',
            '-R', TDBS,
            'view', issue,
            '--json', 'body',
        ).values()
    )
    lines = (line.rstrip('\r') for line in body.split("\n"))
    body_io = StringIO()

    def write(line="", **kwargs):
        print(line, file=body_io, **kwargs)
    found = False
    all_failures_since_5442 = all(run['conclusion'] == 'failure' for run in runs_since_5442)
    if not all_failures_since_5442:
        err("Not all runs since #5442 have failed")

    run_number = env.get('GITHUB_RUN_NUMBER')
    run_id = env.get('GITHUB_RUN_ID')
    if run_id and run_number:
        run_url = f"https://github.com/{REPO}/actions/runs/{run_id}"
        run_link = f"[#{run_number}]({run_url})"
    else:
        run_link = None

    for line in lines:
        if all_failures_since_5442:
            sub = f'Since [#5442] (Jun 28), all {len(runs_since_5442)} runs have failed (as of {fetched_at}'
            if run_link:
                sub += f": {run_link}"
            sub += ")"
            line = re.sub(
                r'Since \[#5442] \(Jun 28\), all \d+ runs have failed \(as of \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z(?:: \[#\d+]\([^)]+\))?\)',
                sub,
                line,
            )
        write(line)
        if line == "<!-- summary -->":
            found = True
            break
    if found:
        assert header_level >= 1
        heading = f"h{header_level}"
        write("<details>")
        write(f"<summary><{heading}>Breakdown by error message</{heading}></summary>")
        write()
        updated_str = f"Updated at {fetched_at}"
        if run_link:
            updated_str += f" (by {run_link})"
        write(f"*{updated_str}*")
        write()
        write(summary_str)
        write("</details>")
        for line in lines:
            if line == "<!-- /summary -->":
                write(line)
                break
        for line in lines:
            write(line)

    print()
    new_body = body_io.getvalue()
    if new_body == body:
        err(f"#{issue} body unchanged")
        return
    if not quiet:
        print("new body:")
        print(new_body)
    body_path = f"{issue}.md"
    with open(body_path, "w") as f:
        f.write(new_body)

    process.run(
        'gh', 'issue',
        '-R', TDBS,
        'edit', issue,
        '--body-file', body_path,
        dry_run=dry_run,
    )


@cli.command
@option('-i', '--issue', type=int, default=GH_ISSUE_NUM, help="Issue number to update. Summary goes between `<!-- summary -->` and `<!-- /summary -->` \"tags\", if present.")
@option('-I', '--no-update-issue', 'no_update_issue', is_flag=True)
@option('-l', '--level', type=int, default=3, help='Markdown heading level for each error message group')
@option('-n', '--dry-run', is_flag=True, help="Update local files, but don't actually edit the issue")
@option('-q', '--quiet', is_flag=True, help=f"Don't print the \"summary\" that's being written to README.md and/or #{GH_ISSUE_NUM}; useful e.g. because GitHub Actions mistakenly detects error messages in the summary as applying to the current job")
@option('-U', '--no-update-readme', is_flag=True)
def summarize(issue, no_update_issue, level, dry_run, quiet, no_update_readme):
    """Group normalized error logs, summarize."""
    db_ids = load_db_ids(NORMALIZED_DIR)
    shas = {}
    for db_id in db_ids:
        with open(f"{NORMALIZED_DIR}/{db_id}", "rb") as f:
            sha = sha256(f.read()).hexdigest()
            if sha not in shas:
                shas[sha] = []
            shas[sha].append(db_id)

    with open(DEFAULT_RUNS_FILE, "r") as f:
        with jsonlines.Reader(f) as lines:
            runs = list(lines)
            runs_by_id = {
                run["databaseId"]: run
                for run in runs
            }

    with open(DEFAULT_METADATA_FILE, "r") as f:
        metadata = json.load(f)
        fetched_at = metadata["fetched_at"]

    summary_io = StringIO()
    with nullcontext() if no_update_readme else readme_sub_ctx() as readme:
        def write(line="", **kwargs):
            print(line, file=summary_io, **kwargs)
            if readme:
                print(line, file=readme, **kwargs)

        heading_prefix = "#" * level
        for sha, db_ids in sorted(shas.items(), key=lambda item: len(item[1]), reverse=True):
            db_ids.sort()
            name = NAMES[sha]
            last_id = db_ids[-1]
            last_run = runs_by_id[last_id]
            last_number = last_run["number"]
            last_run_dt = last_run["createdAt"][:-4]
            write(f"{heading_prefix} \"{name}\"")
            url = f"https://github.com/{TDBS}/actions/runs/{last_id}"
            write(f"Seen {len(db_ids)}x, most recently [#{last_number}]({url}) (at {last_run_dt}):")
            write(f"```")
            with open(f"{NORMALIZED_DIR}/{last_id}", "r") as f:
                write(f.read(), end="")
            write(f"```")
            write()
            write("<details>")
            write("<summary>All runs</summary>")
            write()
            for idx, db_id in enumerate(db_ids):
                run = runs_by_id[db_id]
                number = run["number"]
                url = f"https://github.com/{TDBS}/actions/runs/{db_id}"
                if idx > 0:
                    write(", ", end="")
                write(f"[#{number}]({url})", end="")
            write()
            write("</details>")
            write()

    summary_str = summary_io.getvalue()
    if not quiet:
        print(summary_str)

    if not no_update_issue:
        runs_since_5442 = [
            run
            for run in runs
            if run['number'] >= 5442
        ]
        update_issue(
            issue=issue,
            summary_str=summary_str,
            fetched_at=fetched_at,
            header_level=level - 1,
            runs_since_5442=runs_since_5442,
            quiet=quiet,
            dry_run=dry_run,
        )
