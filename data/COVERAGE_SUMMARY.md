# Coverage summary

Generated from the audited `data/benchmark_master_575.csv` and reconciled to `data/firm_level_benchmark.csv`.

## Coverage

- Frozen FY2024 firms: **575**
- Firms with first-pass search inventory: **575**
- Firms with a reviewed mapping record in the audited master: **302**
- Strict one-action archival benchmark: **9**
- Follow-up priority queue: **38**

## Benchmark status

| Status | Firms |
|---|---:|
| NO_REPORT_FOUND_AFTER_PASS1 | 346 |
| REPORT_NONCANONICAL_ACTION | 112 |
| REPORT_NO_ACTION | 71 |
| REVIEWED_NO_CANONICAL_MAPPING | 19 |
| STRICT_CANONICAL_ACTION | 9 |
| MAPPED_NOT_STRICT | 7 |
| PENDING_REVIEW | 4 |
| MULTI_NONCANONICAL | 3 |
| PENDING_SEARCH_REVIEW | 2 |
| NO_REPORT_FOUND_AFTER_PASS2 | 1 |
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

- `evidence/second_pass_batch_001.csv`: **20 firms** re-reviewed.
- **14** follow-up items reached a stable second-pass disposition and were closed from the priority queue.
- **6** remain because primary/full text could still change the action-bearing-source determination: 동국홀딩스, 한국석유공업, 고려아연, 디에스케이, 진코스텍, 레인보우로보틱스.
- The strict subset is unchanged at **9 firms**.

The archive is a contemporaneous 2024 human/expert benchmark, not a matched-information human-vs-LLM experiment. Search snippets and automated summaries remain discovery evidence only.
