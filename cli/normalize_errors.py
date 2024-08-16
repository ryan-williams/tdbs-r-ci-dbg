import re
from os import listdir
from os.path import exists
from re import sub

from utz import parallel

from .base import cli, out_dir_opt, n_jobs_opt, overwrite_opt
from .extract_errors import ERR_DIR

NORMALIZED_DIR = "normalized"


@cli.command
@overwrite_opt
@n_jobs_opt
@out_dir_opt(NORMALIZED_DIR)
def normalize_errors(overwrite, n_jobs, out_dir):
    """Normalize error logs: substitute memory addresses and UUIDs with placeholders.

    mkdir -p normalized
    ls err/ \
    | parallel --env PATH 'h="[\\da-f]"; h4="$h$h$h$h"; cat err/{} \
    | perl -pe "s/address 0x$h+/address <ADDRESS>/" \
    | perl -pe "s/$h4$h4-$h4-$h4-$h4-$h4$h4$h4/<UUID>/" \
    | perl -pe "s/<UUID>.sh: line (1|4):/<UUID>.sh: line <LINE>:/" \
    | perl -pe "s/:  \d+ (Segmentation fault|Aborted)/:  <ID> \$1/" \
    | perl -pe "s/( \(core dumped\)) Rscript .*/\$1/" \
    | sed -e "/##\[debug\]Finishing: Test/d" \
    | sed -e "/0 | SCEOutgest/d" \
    > normalized/{}'
    """

    def normalize_err_logs(db_id):
        in_path = f"{ERR_DIR}/{db_id}"
        out_path = f"{out_dir}/{db_id}"
        if exists(out_path):
            if overwrite:
                print(f"Normalizing {db_id}: overwriting {out_path}")
            else:
                print(f"Normalizing {db_id}: skipping ({out_path} exists)")
                return
        else:
            print(f"Normalizing {db_id}: writing to {out_path}")

        with (
            open(in_path, "r") as r,
            open(out_path, "w") as w,
        ):
            for line in r:
                line = sub(r"address 0x[\da-f]+", "address <ADDRESS>", line)
                line = sub(r"[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}", "<UUID>", line)
                line = sub(r"<UUID>.sh: line (1|4):", "<UUID>.sh: line <LINE>:", line)
                line = sub(r":  \d+ (Segmentation fault|Aborted)", ":  <ID> \\1", line)
                line = sub(r"( \(core dumped\)) Rscript .*", "\\1", line)
                if "##[debug]Finishing: Test" in line:
                    continue
                if "0 | SCEOutgest" in line:
                    continue
                w.write(line)

    db_ids = [
        re.match(r"(\d+)$", path).group(1)
        for path in listdir(ERR_DIR)
    ]
    parallel(db_ids, normalize_err_logs, n_jobs=n_jobs)
