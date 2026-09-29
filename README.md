# Thesis Human Benchmark 2024

Archival human/expert benchmark for the 575 FY2024 firms in the V4.3 thesis.

## Frozen status

**HB2024-v1.0 is frozen for downstream linkage.**

- Data snapshot commit: `bd6e6ab005ce9d7e810621aa3e29fc7799651824`
- First-pass public-web discovery: **575 / 575 complete**
- Reviewed document/mapping records: **303**
- Priority follow-up queue: **0**
- Strict one-action archival subset: **9 firms**
- Second-pass batches completed: **63 firms**
- Deterministic final audit: **PASS**

Use `data/firm_level_benchmark.csv` as the audited one-row-per-firm source of truth, `outputs/firm_level_benchmark_final.csv` as the frozen output copy, and `outputs/strict_archival_benchmark.csv` as the high-precision strict subset. `outputs/BENCHMARK_DISTRIBUTIONS.md` contains the final distributions, while `outputs/FINAL_AUDIT.md` and `outputs/FREEZE_MANIFEST.json` define the frozen release.

The source hierarchy is frozen as **action-bearing-source priority**. A known source whose primary text remains inaccessible after two searches is preserved as `PRIMARY_UNAVAILABLE_AFTER_PASS2`, not silently converted to no-action.

Downstream C4 / C6-E / C3-E and payoff data are joined in new keyed artifacts against this frozen snapshot.
