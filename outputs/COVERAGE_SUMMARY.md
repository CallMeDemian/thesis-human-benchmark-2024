# Coverage summary

Generated from the audited `data/benchmark_master_575.csv` and reconciled to `data/firm_level_benchmark.csv`.

## Coverage

- Frozen FY2024 firms: **575**
- First-pass search inventory: **575 / 575**
- Reviewed document/mapping records: **303**
- Strict one-action archival benchmark: **9**
- Follow-up priority queue: **3**

## Benchmark status

| Status | Firms |
|---|---:|
| NO_REPORT_FOUND_AFTER_PASS1 | 345 |
| REPORT_NONCANONICAL_ACTION | 119 |
| REPORT_NO_ACTION | 71 |
| PRIMARY_UNAVAILABLE_AFTER_PASS2 | 13 |
| STRICT_CANONICAL_ACTION | 9 |
| NO_REPORT_FOUND_AFTER_PASS2 | 4 |
| MAPPED_NOT_STRICT | 4 |
| MULTI_NONCANONICAL | 4 |
| REVIEWED_NO_CANONICAL_MAPPING | 3 |
| PENDING_SEARCH_REVIEW | 2 |
| EXCLUDED_AI_ONLY | 1 |

## Second-pass progress

- Batch 001: 20 firms reviewed; 14 queue items closed.
- Batch 002: 20 firms reviewed; 15 queue items closed.
- Batch 003: 20 firms reviewed; 20 queue items closed using either primary evidence or the frozen PRIMARY_UNAVAILABLE_AFTER_PASS2 terminal state.
- Remaining queue: **3 firms**.
- Strict subset remains **9 firms**.

PRIMARY_UNAVAILABLE_AFTER_PASS2 prevents a known but inaccessible human report from being mislabeled as REPORT_NO_ACTION and prevents search snippets/automated summaries from becoming final canonical mappings.
