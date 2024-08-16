from hashlib import sha256
from sys import stdout

import jsonlines

from .base import cli, load_db_ids, DEFAULT_RUNS_FILE, REPO
from .normalize_errors import NORMALIZED_DIR

NAMES = {
    "d6cfe842dc246ac67c8b8fb341c4d09a24e05e01e0f05bb9a1f7366aa55240e5": "memory not mapped",
    "cbfb6cc1965c610935cfb56476ac66eb1e10db7f79b54238e85453ac11caa267": "invalid permissions",
    "12898a26fbbae699e8555eeda71f5dd25f6aecc56664eea2aa690cf2d190b4c7": "address (nil), cause 'unknown'",
    "67c6c7e284af1c81625ba210bd9de40c4571c0bf7479ea87ede16c5726d585a1": "bad_function_call",
}


@cli.command
def summarize():
    """Group normalized error logs, summarize.

    rm -rf shas && mkdir -p shas
    ls normalized/ \
    | parallel --env PATH 'sha="$(shasum normalized/{} | cut -d" " -f1)"; echo {} >> shas/$sha'
    wc -l shas/* \
    | head -n-1 \
    | sort -nr \
    | perl -pe 's/^ +//g' \
    | parallel -k --env PATH --colsep ' ' 'sha={2/}; first="$(head -1 shas/$sha)"; echo "SHA $sha, seen {1}x, e.g. run $first:"; cat normalized/$first; echo'
    """
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

    for sha, db_ids in shas.items():
        db_ids.sort()
        name = NAMES[sha]
        last_id = db_ids[-1]
        last_run = runs_by_id[last_id]
        last_run_dt = last_run["createdAt"][:-4]
        print(f"### \"{name}\"")
        url = f"https://github.com/{REPO}/actions/runs/{last_id}"
        print(f"Seen {len(db_ids)}x, most recently at [{last_run_dt}]({url}):")
        print(f"```")
        with open(f"{NORMALIZED_DIR}/{last_id}", "r") as f:
            stdout.write(f.read())
        print(f"```")
        print()
