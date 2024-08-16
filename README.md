# [`r-ci.yml`] CI failure analysis

## Summary
Error logs, normalized and grouped:

### "memory not mapped"
Seen 48x, most recently at [2024-08-16T14:34](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10421656279):
```
 *** caught segfault ***
address <ADDRESS>, cause 'memory not mapped'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

### "invalid permissions"
Seen 11x, most recently at [2024-08-15T14:09](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10405130321):
```
 *** caught segfault ***
address <ADDRESS>, cause 'invalid permissions'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

### "address (nil), cause 'unknown'"
Seen 5x, most recently at [2024-08-16T14:44](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10421787401):
```
 *** caught segfault ***
address (nil), cause 'unknown'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

### "bad_function_call"
Seen 9x, most recently at [2024-08-15T16:31](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10407106592):
```
terminate called after throwing an instance of 'std::bad_function_call'
  what():  bad_function_call
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Aborted                 (core dumped)
##[error]Process completed with exit code 134.
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
dbg-r-ci extract-errors
```
- Strip lines' metadata prefixes (workflow/job names, timestamps)
- Drop lines up to and including the first occurrence of `70 | ScalarMap`
- Drop empty lines

### Normalize: elide memory addresses, UUIDs
```bash
dbg-r-ci normalize-errors
```

### Group by hash, summarize groups
```bash
dbg-r-ci summarize
```

[`r-ci.yml`]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml

[recent `r-ci.yml` `main` runs]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml?query=branch%3Amain
