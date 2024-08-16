# [`r-ci.yml`] CI failure analysis

## Summary
Error log lines, normalized and grouped:
```
SHA e859ef999150e001b7b08ae2d1e73180a3f1f8de, seen 38x, e.g. run 10062825179:
 *** caught segfault ***
address <ADDRESS>, cause 'memory not mapped'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.

SHA 5330f593509a898c2847642bacb277170e107e25, seen 6x, e.g. run 10117378964:
terminate called after throwing an instance of 'std::bad_function_call'
  what():  bad_function_call
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Aborted                 (core dumped)
##[error]Process completed with exit code 134.

SHA 00ab001a8d3acf1b34cb6486d31b4ad9c14c64f9, seen 6x, e.g. run 10086755545:
 *** caught segfault ***
address <ADDRESS>, cause 'invalid permissions'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.

SHA 50a96d9e82b26845bcab5d6ed0bcfc68aae655e5, seen 4x, e.g. run 10060281551:
 *** caught segfault ***
address (nil), cause 'unknown'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

## Methods

Clone + Install:
```bash
git clone https://github.com/ryan-williams/tdbs-r-ci-dbg
pip install -e tdbs-r-ci-dbg
```

### Fetch metadata about [recent `r-ci.yml` `main` runs]
Since 2024-06-18, save to [runs-since-20240618.jsonl](runs-since-20240618.jsonl):
```bash
dbg-r-ci fetch-runs
```

### Download failure logs to [log-failed/](log-failed/)
```bash
dbg-r-ci download-failure-logs
```

### Extract error messages to [err/](err/)
```bash
mkdir -p err
ls log-failed/ \
| parallel 'cat log-failed/{} \
| cut -f3- \
| cut -d" " -f2- \
| sed -e "1,/70 | ScalarMap/ d" \
| sed "/^\s*$/d" \
> err/{}'
```
- Strip lines' metadata prefixes (workflow/job names, timestamps)
- Drop lines up to and including the first occurrence of `70 | ScalarMap`
- Drop empty lines

### Normalize: elide memory addresses, UUIDs
```bash
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
```

### Group by hash
```bash
rm -rf shas && mkdir -p shas
ls normalized/ \
| parallel --env PATH 'sha="$(shasum normalized/{} | cut -d" " -f1)"; echo {} >> shas/$sha'
```

### Summarize groups
```bash
wc -l shas/* \
| head -n-1 \
| sort -nr \
| perl -pe 's/^ +//g' \
| parallel -k --env PATH --colsep ' ' 'sha={2/}; first="$(head -1 shas/$sha)"; echo "SHA $sha, seen {1}x, e.g. run $first:"; cat normalized/$first; echo'
```

[`r-ci.yml`]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml

[recent `r-ci.yml` `main` runs]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml?query=branch%3Amain
