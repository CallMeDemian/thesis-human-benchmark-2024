# Human-18 / Broad Pass-2·Pass-3 Final Handoff

Date: 2026-10-01

## Final state

The frozen independent-expert archival anchor remains **strict-9**. The broad Pass-2 / Pass-3 expansion did not add a new independent-expert strict case under the existing high-precision gate.

The extension nevertheless materially broadened the audit and produced two additional validation layers:

- **state-diversity matched survey cases**: J-O (6 cases)
- **broad-search action-space diagnostics**: P-R (3 cases)

The matched-information human survey therefore has **18 cases (A-R)**.

## Search expansion completed

Broad Pass-2:
- unresolved / previously negative queue: **341 firms**
- report-index requests: **1,023**
- report-index sources: IRGO, AlphaSquare, StockReport
- source pages containing 2024 references: **344**

Additional screens:
- all-575 report-title scan: completed
- non-strict firms surfaced by action-term title windows: **32**
- incomplete-primary recovery queue: **147 firms**
- firms with canonical-keyword recovery leads: **32**

Focused Pass-3 review preserved the original source hierarchy and strict mapping gate. No strict rule was relaxed after downstream results were observed.

## Why strict-9 did not expand

The dominant rejection patterns were:

1. outcome-only wording (for example, profitability improvement without a managerial mechanism);
2. customer/industry CAPEX being mistaken for the firm's own CX action;
3. upstream business actions (business exit, acquisition, spin-off, restructuring, channel expansion) creating an OE-like financial effect without being equivalent to the frozen OE intervention;
4. later/higher-priority action-bearing evidence being materially noncanonical;
5. insufficient primary text.

The empty `strict_archival_extension_v2.csv` is therefore an intentional negative result, not a failed search.

## Broad-search diagnostic cases

Three cases were retained outside the strict benchmark:

| Alias | Firm | Diagnostic |
|---|---|---|
| P | 하나투어 | Earlier OE-like personnel/fixed-cost efficiency is superseded at firm level by a later material noncanonical growth/marketing action. |
| Q | 비투엔 | Explicit cost-efficiency language coexists with a loss-making-business spin-off; clean one-action OE mapping is not justified. |
| R | 휠라홀딩스 | FILA USA restructuring produces fixed-cost savings, but the managerial act is an upstream business shutdown/restructuring rather than the frozen OE intervention. |

These cases are **not** human answer keys. They are included in the survey because they probe the boundary between a financial effect and the actual managerial action.

## Human survey structure

- A-I: `ARCHIVAL_ANCHOR_9`
- J-O: `ADDITIONAL_STATE_6`
- P-R: `BROAD_DIAGNOSTIC_3`
- total: **18**

Respondents receive:
- FY2024 IC-b only;
- the same 27 visible information fields;
- candidate9 / B1;
- anonymized firm identities;
- one initial action choice, confidence and short rationale.

They do not receive:
- firm names or stock codes;
- archival expert actions;
- model outputs;
- Oracle / Simulator scores;
- FY2025 outcomes.

## Downstream integration completed

The existing downstream pipeline has been re-run for all 18 cases against the frozen V4.3 results:

- C4
- C4R
- C6-E
- C3-E
- Oracle Alpha / Beta / Gamma
- candidate ceiling
- regret to candidate ceiling
- reference uptake
- policy transitions

The output is partitioned by:
- `ARCHIVAL_ANCHOR_9`
- `ADDITIONAL_STATE_6`
- `BROAD_DIAGNOSTIC_3`
- `ALL_18`

The preserved strict-9 regression check is **PASS: 12 cells checked, 0 mismatches**.

Human responses have not yet been collected, so J-R are currently model-side pre-survey baselines only.

## Key interpretation boundary

Do not relabel this result as strict-18.

The valid structure is:

1. **strict-9 independent expert archival anchor**;
2. **broad-search diagnostic archive**;
3. **18-case matched-information human survey**.

A future human modal action is a human judgment baseline, not causal ground truth.

## Final artifacts

Core archival expansion:
- `analysis_outputs/broad_archival/BROAD_PASS3_FINAL_REVIEW.md`
- `analysis_outputs/broad_archival/strict_archival_extension_v2.csv`
- `analysis_outputs/broad_archival/supplementary_archival_diagnostics_v2.csv`

Human-18:
- `analysis_outputs/human18/CREATE_GOOGLE_FORM.txt`
- `analysis_outputs/human18/RESEARCHER_ONLY_case_key.csv`
- `analysis_outputs/human18/case_states_ICb.csv`
- `analysis_outputs/human18/respondent/`

Downstream:
- `analysis_outputs/human18/downstream/HUMAN18_DOWNSTREAM_REPORT.md`
- `analysis_outputs/human18/downstream/HUMAN18_DOWNSTREAM_MANIFEST.json`
- case-level, policy-summary, transition and reference-behavior CSVs in the same directory.

## Reproducibility status

- Human-18 survey static build: PASS
- 18 cases: PASS
- 27 IC-b fields per case: PASS
- company-name leakage check: PASS
- candidate9 exact-catalog check: PASS
- Apps Script syntax check: PASS
- case-card render-bounds checks: PASS
- Human-18 downstream join: PASS
- strict-9 regression: PASS

Still requiring researcher-side execution:
- Google account Form creation;
- browser/mobile visual inspection;
- pilot completion-time check;
- institutional human-subject / ethics procedure as applicable;
- response collection and post-survey human-vs-model analysis.
