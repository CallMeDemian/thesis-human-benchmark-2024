# Coverage summary

Generated from `data/benchmark_master_575.csv`.

## Coverage

- Frozen FY2024 firms: **575**
- Firms with first-pass search inventory: **575**
- Firms with a reviewed mapping record in the canonical master: **291**
- Strict canonical archival actions currently available: **17**
- Strict canonical actions excluding issuer IR/management evidence: **16**
- Follow-up priority queue: **52**

## Benchmark status

| Status | Firms |
|---|---:|
| NO_REPORT_FOUND_AFTER_PASS1 | 347 |
| REPORT_NONCANONICAL_ACTION | 97 |
| REPORT_NO_ACTION | 71 |
| REVIEWED_NO_CANONICAL_MAPPING | 24 |
| STRICT_CANONICAL_ACTION | 17 |
| PENDING_REVIEW | 11 |
| MAPPED_NOT_STRICT | 3 |
| MULTI_NONCANONICAL | 2 |
| PENDING_SEARCH_REVIEW | 2 |
| EXCLUDED_AI_ONLY | 1 |

## Strict canonical action distribution

| Action | Firms |
|---|---:|
| OE | 13 |
| CX | 2 |
| WC1 | 1 |
| DL | 1 |

## Strict-source distribution

| Source type | Firms |
|---|---:|
| EQUITY | 12 |
| CRA | 4 |
| IR | 1 |

## Interpretation

The first-pass internet search covers all 575 firms, but the benchmark must not be described as 575 human recommendations. Many firms have no eligible 2024 public expert report, reports without a prospective financial action, or actions outside the frozen 8D/9-candidate space.

`data/canonical_mapping_overrides.csv` records reviewed evidence that was omitted from the row-batched mapping files or corrected under the frozen action-contract boundary. In particular, an asset sale is not treated as DL unless principal debt reduction itself is the identified managerial action/path.

The archival benchmark is contemporaneous rather than information-matched: calendar-2024 reports can use FY2023 or interim-2024 information, whereas the thesis LLM policy is evaluated on the frozen FY2024 state.
