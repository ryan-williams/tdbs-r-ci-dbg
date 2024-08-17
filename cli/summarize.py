from contextlib import contextmanager, nullcontext
from functools import partial
from hashlib import sha256
from io import StringIO
from os import environ as env

import jsonlines
from click import option
from utz import process, singleton, now, err

from .base import cli, load_db_ids, DEFAULT_RUNS_FILE, REPO, GH_ISSUE_NUM
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
@option('-i', '--update-issue', type=int, default=GH_ISSUE_NUM, help="Issue number to update. Summary goes between `<!-- summary -->` and `<!-- /summary -->` \"tags\", if present.")
@option('-l', '--level', type=int, default=3, help='Markdown heading level for each error message group')
@option('-u', '--update-readme', is_flag=True)
def summarize(update_issue, level, update_readme):
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

    summary_io = StringIO()
    with readme_sub_ctx() if update_readme else nullcontext() as readme:
        def write(line="", **kwargs):
            print(line, file=summary_io, **kwargs)
            if readme:
                print(line, file=readme, **kwargs)

        heading_prefix = "#" * level
        for sha, db_ids in shas.items():
            db_ids.sort()
            name = NAMES[sha]
            last_id = db_ids[-1]
            last_run = runs_by_id[last_id]
            last_number = last_run["number"]
            last_run_dt = last_run["createdAt"][:-4]
            write(f"{heading_prefix} \"{name}\"")
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

    summary_str = summary_io.getvalue()
    print(summary_str)

    if update_issue:
        body = singleton(
            process.json(
                'gh', 'issue',
                '-R', REPO,
                'view', update_issue,
                '--json', 'body',
            ).values()
        )
        lines = (line.rstrip('\r') for line in body.split("\n"))
        new_lines = []
        found = False
        for line in lines:
            new_lines.append(line)
            if line == "<!-- summary -->":
                found = True
                break
        if found:
            now_str = f'{now()}'
            new_lines.append("<details>")
            new_lines.append("<summary><h2>Breakdown by error message</h2></summary>")
            new_lines.append("")
            run_number = env.get('GITHUB_RUN_NUMBER')
            run_id = env.get('GITHUB_RUN_ID')
            if run_id and run_number:
                url = f"https://github.com/{REPO}/actions/runs/{run_id}"
                new_lines.append(f"*Updated at {now_str}, by [#{run_number}]({url})*")
            else:
                new_lines.append(f"*Updated at {now_str}*")
            new_lines.append(summary_str)
            new_lines.append("</details>")
            for line in lines:
                if line == "<!-- /summary -->":
                    new_lines.append(line)
                    break
            for line in lines:
                new_lines.append(line)

        print()
        new_body = "\n".join(new_lines)
        if new_body == body:
            err(f"#{update_issue} body unchanged")
            return
        print("new body:")
        print(new_body)
        body_path = f"{update_issue}.md"
        with open(body_path, "w") as f:
            f.write(new_body)

        process.run(
            'gh', 'issue',
            '-R', REPO,
            'edit', update_issue,
            '--body-file', body_path,
        )
