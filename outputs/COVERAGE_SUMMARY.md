# Coverage and Strict Benchmark Status

Updated: 2026-09-29

## Current collection state

- Frozen FY2024 target firms: **575 / 575**
- First-pass public-web discovery: **575 / 575 complete**
- Rows with a reviewed mapping record: **292 / 575**
- Strict one-action archival benchmark after mapping audits: **9 firms**
- Strict source mix: **1 CRA, 8 EQUITY**
- Strict action mix: **2 CX, 7 OE**

The strict subset is intentionally conservative. Coverage pressure is not allowed to convert forecasts, state thresholds, growth strategies, asset sales, acquisitions, capacity expansion, already-realized actions, or multi-action restructuring into a frozen canonical action without adequate semantic fit.

## Strict firms

| Row | Firm | Source | Date | Statement type | Action |
|---:|---|---|---|---|---|
| 50 | 대한해운 | 한국신용평가 (CRA) | 2024-12-26 | STATED_MANAGEMENT_POLICY | CX |
| 72 | 무림P&P | 교보증권 (EQUITY) | 2024-12-10 | STATED_MANAGEMENT_POLICY | OE |
| 82 | HMM | KB증권 (EQUITY) | 2024-10-18 | EXPLICIT_RECOMMENDATION | CX |
| 89 | 더존비즈온 | 미래에셋증권 (EQUITY) | 2024-11-27 | PROSPECTIVE_ACTION_PATH | OE |
| 183 | 카페24 | 미래에셋증권 (EQUITY) | 2024-03-11 | STATED_MANAGEMENT_POLICY | OE |
| 267 | 랩지노믹스 | 대신증권 (EQUITY) | 2024-10-29 | PROSPECTIVE_ACTION_PATH | OE |
| 368 | 율촌 | 유안타증권 (EQUITY) | 2024-12-20 | PROSPECTIVE_ACTION_PATH | OE |
| 448 | 스튜디오드래곤 | 미래에셋증권 (EQUITY) | 2024-11-18 | PROSPECTIVE_ACTION_PATH | OE |
| 515 | 뉴로메카 | 유진투자증권 (EQUITY) | 2024-06-24 | STATED_MANAGEMENT_POLICY | OE |

## Audit history

The repository preserves three explicit mapping audits:

1. `evidence/strict_mapping_audit_v1.csv`
2. `evidence/provisional_action_audit_v1.csv`
3. `evidence/strict_candidate_audit_v2.csv`

These audits demote translated downstream effects, realized-only actions, and mappings that omit material noncanonical or opposite-direction co-actions.

## Important boundary

This archive is not a 575-firm human experiment with matched information. It is a **2024 contemporaneous archival human/expert benchmark**. Reports may use FY2023, interim-2024, market, management, or qualitative information available on their publication dates.

The strict subset must therefore be compared with C4/C6-E as an external archival anchor, not as a randomized or information-matched estimate of human superiority.

## Next gate

Before any Oracle/Simulator or LLM outcome linkage:

- recover primary text for remaining high-value provisional candidates;
- complete second-pass CRA/issuer searches for high-priority `NO_REPORT_FOUND_AFTER_PASS1` firms;
- freeze a versioned firm-level benchmark snapshot;
- only then merge in C4 / C6-E / C3-E action and payoff data.
