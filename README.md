
Fetch metadata about [failed `r-ci.yml` `main` runs][r-ci main failures] since 2024-06-18:
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

Produces: [failures-since-20240618.jsonl](failures-since-20240618.jsonl).

[r-ci main failures]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml?query=branch%3Amain+is%3Afailure