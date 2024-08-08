# [`r-ci.yml`] CI failure analysis

## Fetch metadata about [failed `r-ci.yml` `main` runs][r-ci main failures]
Since 2024-06-18, to [failures-since-20240618.jsonl](failures-since-20240618.jsonl:
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

## Download failure logs to [log-failed/](log-failed/)
```bash
mkdir -p log-failed
cat failures-since-20240618.jsonl \
| jq -r .databaseId \
| grep -v  -e 10113090142 -e 10306622414 \
| parallel 'f=log-failed/{}; if ! [ -f $f ]; then echo "Downloading {}"; gh run view {} --log-failed > $f; fi'
```
Runs omitted due to unrelated failures:
- [10113090142]: all jobs failed: `No valid versions of tiledb-r found`
- [10306622414]: workflow file syntax error, no logs produced

## Extract error messages to [err/](err/)
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

## Normalize: elide memory addresses, UUIDs
```bash
mkdir -p normalized
ls err/ \
| parallel --env PATH 'h="[\\da-f]"; h4="$h$h$h$h"; cat err/{} \
| perl -pe "s/address 0x$h+/address <ADDRESS>/" \
| perl -pe "s/$h4$h4-$h4-$h4-$h4-$h4$h4$h4/<UUID>/" \
| perl -pe "s/:  \d+ (Segmentation fault|Aborted)/:  <ID> \$1/" \
| sed -e "/##\[debug\]Finishing: Test/ d" \
> normalized/{}'
```

## Group by hash
```bash
mkdir -p shas
ls normalized/ \
| parallel --env PATH 'sha="$(shasum normalized/{} | cut -d" " -f1)"; echo {} >> shas/$sha'
```

[`r-ci.yml`]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml
[10113090142]: https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10113090142
[10306622414]: https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10306622414

[r-ci main failures]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml?query=branch%3Amain+is%3Afailure