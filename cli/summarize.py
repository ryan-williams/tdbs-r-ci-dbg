from contextlib import contextmanager, nullcontext
from functools import partial
from hashlib import sha256

import jsonlines
from click import option

from .base import cli, load_db_ids, DEFAULT_RUNS_FILE, REPO
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


@cli.command
@option('-u', '--update-readme', is_flag=True)
def summarize(update_readme):
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

    with readme_sub_ctx() if update_readme else nullcontext() as readme:
        def write(line="", **kwargs):
            print(line, **kwargs)
            if readme:
                print(line, file=readme, **kwargs)

        for sha, db_ids in shas.items():
            db_ids.sort()
            name = NAMES[sha]
            last_id = db_ids[-1]
            last_run = runs_by_id[last_id]
            last_number = last_run["number"]
            last_run_dt = last_run["createdAt"][:-4]
            write(f"### \"{name}\"")
            url = f"https://github.com/{REPO}/actions/runs/{last_id}"
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
                url = f"https://github.com/{REPO}/actions/runs/{db_id}"
                if idx > 0:
                    write(", ", end="")
                write(f"[#{number}]({url})", end="")
            write()
            write("</details>")
            write()
