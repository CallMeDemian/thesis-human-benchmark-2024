# Thesis Human Benchmark 2024

Archival human/expert benchmark for the 575 FY2024 firms in the V4.3 thesis.

## Current status

- First-pass discovery: **575 / 575 complete**
- Reviewed document/mapping records: **303**
- Strict one-action subset: **9 firms**
- Remaining follow-up queue: **3 firms**
- Second-pass batches completed: **60 firms**

Use `data/firm_level_benchmark.csv` as the audited one-row-per-firm source of truth and `outputs/strict_archival_benchmark.csv` as the strict subset. The hierarchy is frozen as **action-bearing-source priority**. A known source whose primary text remains inaccessible after two searches is preserved as `PRIMARY_UNAVAILABLE_AFTER_PASS2`, not silently converted to no-action.
