# Coverage summary

Generated from the audited `data/benchmark_master_575.csv` and reconciled to `data/firm_level_benchmark.csv`.

## Coverage

- Frozen FY2024 firms: **575**
- Firms with first-pass search inventory: **575**
- Firms with a reviewed mapping record in the audited master: **292**
- Strict one-action archival benchmark: **9**
- Follow-up priority queue: **52**

## Benchmark status

| Status | Firms |
|---|---:|
| NO_REPORT_FOUND_AFTER_PASS1 | 346 |
| REPORT_NONCANONICAL_ACTION | 102 |
| REPORT_NO_ACTION | 71 |
| REVIEWED_NO_CANONICAL_MAPPING | 23 |
| PENDING_REVIEW | 11 |
| STRICT_CANONICAL_ACTION | 9 |
| MAPPED_NOT_STRICT | 7 |
| MULTI_NONCANONICAL | 3 |
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

## Source of truth

- `data/firm_level_benchmark.csv`: audited one-row-per-firm mapping state.
- `outputs/strict_archival_benchmark.csv`: current strict archival subset.
- `evidence/strict_mapping_audit_v1.csv`, `evidence/strict_candidate_audit_v2.csv`, and `evidence/provisional_action_audit_v1.csv`: preserved audit trail.
- `data/benchmark_master_575.csv` and the canonical shards are reconciled to the audited firm-level state in this revision.

The archive is a contemporaneous 2024 human/expert benchmark, not a matched-information human-vs-LLM experiment. Search snippets and automated summaries remain discovery evidence only.
