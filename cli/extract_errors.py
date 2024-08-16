import re
from os import makedirs, listdir
from os.path import exists

from click import option
from utz import parallel

from .base import cli, overwrite_opt, njobs_opt
from .download_failure_logs import FAIL_LOGS_DIR

ERR_DIR = 'err'


@cli.command("extract-errors")
@overwrite_opt
@njobs_opt
@option('-o', '--out-dir', default=ERR_DIR)
def extract_errors(overwrite, n_jobs, out_dir):
    """Remove failed runs' logs that precede the failure, strip metadata/timestamps, drop empty lines.
    - Strip lines' metadata prefixes (workflow/job names, timestamps)
    - Drop lines up to and including the first occurrence of `70 | ScalarMap`
    - Drop empty lines
    """
    makedirs(out_dir, exist_ok=True)

    def extract_run_errors(db_id):
        in_path = f"{FAIL_LOGS_DIR}/{db_id}"
        out_path = f"{out_dir}/{db_id}"
        if exists(out_path):
            if overwrite:
                print(f"Extracting {db_id}: overwriting {out_path}")
            else:
                print(f"Extracting {db_id}: skipping ({out_path} exists)")
                return
        else:
            print(f"Extracting {db_id}: writing to {out_path}")

        with (
            open(in_path, "r") as r,
            open(out_path, "w") as w,
        ):
            lines_iter = iter(r.readlines())
            for line in lines_iter:
                if re.search(r"70 \| ScalarMap", line):
                    break

            for line in lines_iter:
                line = line.rstrip('\n')
                line = '\t'.join(line.split('\t')[2:])
                line = ' '.join(line.split(' ')[1:])
                if line.strip():
                    print(line, file=w)

    db_ids = [
        re.match(r"(\d+)$", path).group(1)
        for path in listdir("log-failed")
    ]
    parallel(db_ids, extract_run_errors, n_jobs=n_jobs)
