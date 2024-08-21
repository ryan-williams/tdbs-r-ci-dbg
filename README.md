# [`r-ci.yml`] CI failure analysis

## Summary
Error logs, normalized and grouped:

<!-- summary -->
### "memory not mapped"
Seen 50x, most recently [#5785](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10456041903) (at 2024-08-19T15:12):
```
 *** caught segfault ***
address <ADDRESS>, cause 'memory not mapped'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

<details>
<summary>All runs</summary>

[#5419](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9569392325), [#5422](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9570984555), [#5423](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9572000964), [#5442](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9713375174), [#5444](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9715377508), [#5449](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9765104519), [#5451](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9766661484), [#5452](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9783707917), [#5464](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9814785558), [#5476](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9843704609), [#5486](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9881520849), [#5492](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9898053170), [#5512](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9943039058), [#5521](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9956624972), [#5523](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9959470218), [#5537](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10062825179), [#5538](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10064864542), [#5552](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10068043764), [#5559](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10114098472), [#5563](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10145229614), [#5571](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10154003557), [#5582](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10184466683), [#5586](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10185561956), [#5588](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10187783322), [#5602](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10220416866), [#5603](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10221334974), [#5604](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10222002953), [#5605](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10222392700), [#5618](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10256362597), [#5621](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10256549397), [#5623](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10256798425), [#5634](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10259083987), [#5635](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10266982650), [#5640](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10271470311), [#5641](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10271526049), [#5644](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10271742122), [#5646](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10273278390), [#5648](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10273437144), [#5686](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10322976724), [#5690](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10324940140), [#5693](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10325537082), [#5696](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10353181772), [#5698](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10354763678), [#5706](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10370712907), [#5711](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10377466816), [#5727](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10389017953), [#5736](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10395151073), [#5743](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10421656279), [#5784](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10456036061), [#5785](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10456041903)
</details>

### "invalid permissions"
Seen 12x, most recently [#5790](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10472816543) (at 2024-08-20T13:45):
```
 *** caught segfault ***
address <ADDRESS>, cause 'invalid permissions'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

<details>
<summary>All runs</summary>

[#5418](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9556822939), [#5459](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9797654194), [#5518](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9946090074), [#5556](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10086755545), [#5568](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10153626673), [#5616](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10255244523), [#5688](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10323602584), [#5714](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10378035547), [#5724](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10379617881), [#5729](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10389105432), [#5737](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10405130321), [#5790](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10472816543)
</details>

### "bad_function_call"
Seen 11x, most recently [#5786](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10456055740) (at 2024-08-19T15:13):
```
terminate called after throwing an instance of 'std::bad_function_call'
  what():  bad_function_call
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Aborted                 (core dumped)
##[error]Process completed with exit code 134.
```

<details>
<summary>All runs</summary>

[#5467](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9841072036), [#5527](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9977611518), [#5560](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10117378964), [#5615](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10255002395), [#5637](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10267534162), [#5654](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10277228833), [#5673](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10309133151), [#5707](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10371391793), [#5738](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10407106592), [#5764](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10434687662), [#5786](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10456055740)
</details>

### "address (nil), cause 'unknown'"
Seen 7x, most recently [#5787](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10457457425) (at 2024-08-19T16:45):
```
 *** caught segfault ***
address (nil), cause 'unknown'
An irrecoverable exception occurred. R is aborting now ...
/home/runner/work/_temp/<UUID>.sh: line <LINE>:  <ID> Segmentation fault      (core dumped)
##[error]Process completed with exit code 139.
```

<details>
<summary>All runs</summary>

[#5511](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/9941795268), [#5532](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10060281551), [#5550](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10066011138), [#5657](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10287520744), [#5746](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10421787401), [#5750](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10422557720), [#5787](https://github.com/single-cell-data/TileDB-SOMA/actions/runs/10457457425)
</details>

<!-- /summary -->

## Methods

Clone + Install:
```bash
git clone https://github.com/ryan-williams/tdbs-r-ci-dbg
pip install -e tdbs-r-ci-dbg
```

### Fetch metadata about [recent `r-ci.yml` `main` runs]
Fetch runs since 2024-06-18, save to [runs-since-20240618.jsonl](runs-since-20240618.jsonl):
```bash
dbg-r-ci fetch-runs
```

### Download failure logs (to [log-failed](log-failed))
```bash
dbg-r-ci download-failure-logs
```

### Extract error messages (to [err](err))
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
This updates the top of this README, as well as the "Breakdown by error message" details section of [TileDB-SOMA#2906].


[`r-ci.yml`]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml

[recent `r-ci.yml` `main` runs]: https://github.com/single-cell-data/TileDB-SOMA/actions/workflows/r-ci.yml?query=branch%3Amain

[TileDB-SOMA#2906]: https://github.com/single-cell-data/TileDB-SOMA/issues/2906
