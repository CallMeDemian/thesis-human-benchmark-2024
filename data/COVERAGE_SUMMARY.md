# Coverage summary

Generated from the audited `data/benchmark_master_575.csv` and reconciled to `data/firm_level_benchmark.csv`.

## Coverage

- Frozen FY2024 firms: **575**
- Firms with first-pass search inventory: **575**
- Firms with a reviewed mapping record in the audited master: **303**
- Strict one-action archival benchmark: **9**
- Follow-up priority queue: **23**

## Benchmark status

| Status | Firms |
|---|---:|
| NO_REPORT_FOUND_AFTER_PASS1 | 346 |
| REPORT_NONCANONICAL_ACTION | 117 |
| REPORT_NO_ACTION | 72 |
| REVIEWED_NO_CANONICAL_MAPPING | 13 |
| STRICT_CANONICAL_ACTION | 9 |
| PENDING_REVIEW | 4 |
| MAPPED_NOT_STRICT | 4 |
| MULTI_NONCANONICAL | 4 |
| NO_REPORT_FOUND_AFTER_PASS2 | 3 |
| PENDING_SEARCH_REVIEW | 2 |
| EXCLUDED_AI_ONLY | 1 |

## Strict canonical action distribution

| Action | Firms |
|---|---:|
| OE | 7 |
| CX | 2 |

## Strict-source distribution

| Source type | Firms |
|---|---:|
| EQUITY | 8 |
| CRA | 1 |

## Second-pass progress

- Batch 001: **20 firms** re-reviewed; 14 queue items closed.
- Batch 002: **20 firms** re-reviewed; **15** additional queue items closed.
- Remaining follow-up queue: **23**.
- The strict subset remains **9 firms**.

Batch 002 applies the frozen action-bearing-source hierarchy and corrects several semantic/source-selection issues: debt-equity setoff is not DL; growth-CAPEX expansion is not CX or downstream OE; rating withdrawal/no-action permits descent to EQUITY; an action-bearing CRA blocks cherry-picking a lower-layer canonical action.

The archive is a contemporaneous 2024 human/expert benchmark, not a matched-information human-vs-LLM experiment. Search snippets and automated summaries remain discovery evidence only.
