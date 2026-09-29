# Final archival benchmark audit

Freeze date: 2026-09-29  
Data snapshot commit: `bd6e6ab005ce9d7e810621aa3e29fc7799651824`

## Deterministic invariants

All checks passed.

| Check | Result |
|---|---|
| Frozen roster rows | 575 / 575 |
| Unique firm_key in roster | 575 |
| Firm-level benchmark rows / unique keys | 575 / 575 |
| Benchmark master rows / unique keys | 575 / 575 |
| Final firm-level output rows / unique keys | 575 / 575 |
| Canonical shards combined rows / unique keys | 575 / 575 |
| Follow-up queue | 0 |
| Strict output vs firm-level strict keys | exact match |
| Strict noncanonical actions | 0 |
| Strict weak-confidence mappings | 0 |
| Silence mapped to A0 | 0 |
| Master mapping drift vs firm-level source of truth | 0 |

## Frozen strict subset

| Row | Firm | Source | Action | Confidence |
|---:|---|---|---|---|
| 50 | 대한해운 | CRA | CX | HIGH |
| 72 | 무림P&P | EQUITY | OE | HIGH |
| 82 | HMM | EQUITY | CX | HIGH |
| 89 | 더존비즈온 | EQUITY | OE | HIGH |
| 183 | 카페24 | EQUITY | OE | HIGH |
| 267 | 랩지노믹스 | EQUITY | OE | HIGH |
| 368 | 율촌 | EQUITY | OE | HIGH |
| 448 | 스튜디오드래곤 | EQUITY | OE | HIGH |
| 515 | 뉴로메카 | EQUITY | OE | HIGH |

## Freeze boundary

Archival source selection, semantic mapping, strict eligibility, and firm-level aggregation are frozen at the data snapshot commit above. Downstream model actions and payoff data are added by firm_key in separate artifacts so the archival labels remain an independent external benchmark.

## Interpretation boundary

This is a contemporaneous archival benchmark rather than a matched-information human experiment. The nine-firm strict subset is a high-precision external anchor, not a representative sample of all 575 firms.
