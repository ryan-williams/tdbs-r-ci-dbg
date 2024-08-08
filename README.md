
Fetch metadata about [failed `r-ci.yml` `main` runs][r-ci main failures], since 2024-06-18, to [failures-since-20240618.jsonl](failures-since-20240618.jsonl):
```bash
since=2024-06-18
yyyymmdd=$(echo $since | sed 's/-//g')
max=100
gh run list -w r-ci.yml -b main --json number,databaseId,conclusion,createdAt -L $max \
| jq -c "
    .[]
    | select(
        .conclusion == \"failure\" and
        .createdAt > \"$since\"
    )
" | tee failures-since-$yyyymmdd.jsonl
```

Download failure logs to [log-failed/](log-failed/):
```bash
mkdir -p log-failed
cat failures-since-20240618.jsonl \
| jq -r .databaseId \
| grep -v 10306622414 \
| parallel 'f=log-failed/{}; if ! [ -f $f ]; then echo "Downloading {}"; gh run view {} --log-failed > $f; fi'
```

([10306622414] is omitted because it failed with a syntax error in the workflow file, and didn't produce any logs)

Extract error messages to [err/](err/):
```bash
mkdir -p err
ls log-failed/ \
| parallel 'cat log-failed/{} \
| cut -f3- \
| cut -d" " -f2- \
| sed -e "1,/70 | ScalarMap/ d" \
| sed '/^\s*$/d' \
> err/{}'
```
- Strip lines' leading metadata (workflow/job names, timestamps)
- Drop lines up to and including the first occurrence of `70 | ScalarMap`
- Drop empty lines


[10306622414]: https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10306622414

[r-ci main failures]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml?query=branch%3Amain+is%3Afailure