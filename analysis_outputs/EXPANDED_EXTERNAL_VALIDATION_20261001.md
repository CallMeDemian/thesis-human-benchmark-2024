# Expanded external validation checkpoint — 2026-10-01

## Status

**BROAD SEARCH COMPLETE / STRICT EXPERT ANCHOR UNCHANGED / HUMAN-18 SURVEY PREPARED**

This checkpoint integrates the broad Pass-2/Pass-3 archival search, the frozen strict-9 external anchor, the six financial-state survey additions, three broad-search diagnostic cases, and the corresponding model-side downstream analysis.

## 1. Broad Pass-2 / Pass-3 coverage

The extension rules were frozen before inspecting newly generated downstream policy results.

Search coverage:
- frozen FY2024 population: 575 firms;
- broad unresolved/negative Pass-2 queue: 341 firms;
- public report-index requests: 1,023 across IRGO, AlphaSquare and StockReport;
- pages containing 2024 material: 344;
- separate all-575 IRGO title/window scan: completed;
- non-strict firms surfaced by action-term title/window screen: 32;
- previously incomplete-primary records and the strongest apparent canonical-action leads were then re-reviewed under the existing source hierarchy and strict one-action adequacy gate.

The search did not use C3-E/C4/C4R/C6-E actions, Oracle/Simulator payoffs, FY2025 outcomes, or prior model-human agreement to choose extension cases.

## 2. Strict expert extension result: zero

No new firm passed all original strict requirements simultaneously.

Therefore:

- frozen independent-expert anchor remains **n=9**;
- strict_archival_extension_v2.csv contains no additional firm;
- HB2024-v1.0 is unchanged.

This is a negative search result, not permission to relax the gate.

The repeated exclusion mechanisms were:
1. forecast or outcome language without an explicit managerial intervention;
2. customer/industry investment incorrectly resembling the firm's own CX;
3. business exit, acquisition, spin-off, channel conversion or other upstream action producing a downstream OE-like effect;
4. material co-actions that cannot be represented by one frozen candidate;
5. later/higher-priority action-bearing evidence that is noncanonical;
6. insufficient primary text.

## 3. Broad-search diagnostic archive

Three high-information cases are retained separately as **action-space/source-hierarchy diagnostics**, not as strict expert labels.

| ID | Firm | Canonical component visible in archive | Why strict mapping is blocked |
|---|---|---|---|
| BROAD-DIAG-01 | 하나투어 | OE | An earlier primary report contains online/personnel efficiency, but a later 2024 action-bearing report plans aggressive marketing/free-travel expansion. The later material noncanonical action governs the frozen hierarchy. |
| BROAD-DIAG-02 | 비투엔 | OE | Cost-efficiency language is accompanied by loss-making-business spin-off; full primary text was not recovered in the broad extension. |
| BROAD-DIAG-03 | 휠라홀딩스 | OE-like fixed-cost effect | The actual managerial act is U.S. wholesale business shutdown/restructuring. The gate does not translate a business exit into OE solely because fixed costs fall. |

Primary/source locators are preserved in supplementary_archival_diagnostics_v2.csv and BROAD_PASS3_FINAL_REVIEW.md.

## 4. Existing Human-15 model-side results retained

A-I remain the frozen strict archival anchor.

J-O remain six policy-blind financial-state coverage cases:
- J leverage,
- K liquidity,
- L short debt,
- M working capital,
- N CAPEX,
- O strong balance sheet.

Their earlier downstream results are preserved. No human label is assigned before survey collection.

## 5. Human-18 survey design

The matched-information survey now contains:

- **A-I: ARCHIVAL_ANCHOR_9** — 9 frozen strict archival firms;
- **J-O: ADDITIONAL_STATE_6** — 6 financial-state diversity cases;
- **P-R: BROAD_DIAGNOSTIC_3** — 3 broad-search action-space diagnostics.

Total: **18 cases**.

P-R mapping:
- P = 하나투어
- Q = 비투엔
- R = 휠라홀딩스

The researcher crosswalk is private. Respondents receive:
- the same 27 IC-b information fields;
- anonymized firm identity;
- candidate9/B1 action definitions;
- human-readable rounded values;
- one action choice, confidence and short rationale.

Respondents do not receive the archival component, model output, Oracle payoff, source document, company identity, or later outcome.

The broad diagnostic cases are included to test matched-information human decisions at precisely the points where free-form archival evidence does not fit cleanly into the frozen candidate space. They are **not** given an answer key.

## 6. Integrated 18-case model-side downstream analysis

Contract:
- candidate9
- IC-b
- B1
- Run1 / replicate 1
- Strict ITT
- C4, C4R, C6-E
- GPT-5.4-mini and Gemini 3.1 Flash-Lite
- BASELINE and HIGH
- C3-E frozen Candidate-IQL ensemble

The original strict-9 regression check remains **PASS: 12 cells checked, 0 mismatches**.

### Broad diagnostic three

| Case | Firm | C3-E | Alpha candidate ceiling | Baseline Gemini C4/C4R/C6-E | Baseline GPT | High Gemini | High GPT |
|---|---|---|---|---|---|---|---|
| P | 하나투어 | MX2 | all nine tied at 0 | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 |
| Q | 비투엔 | OE | CX/OE/WC1 | OE/MX1/OE | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 |
| R | 휠라홀딩스 | RF | DL | RF/RF/RF | RF/RF/RF | RF/RF/RF | RF/RF/RF |

The archival OE-like component agrees with C3-E in 1/3 cases. This is **component convergence only**, not accuracy.

### Combined 18-case mean Delta Alpha

| Regime | Model | C4 | C4R | C6-E |
|---|---|---:|---:|---:|
| BASELINE | Gemini 3.1 Flash-Lite | 1.0737 | 0.9298 | 0.9018 |
| BASELINE | GPT-5.4-mini | 0.8542 | 0.8542 | 1.1956 |
| HIGH | Gemini 3.1 Flash-Lite | 0.7922 | 0.7922 | 0.9338 |
| HIGH | GPT-5.4-mini | 0.8806 | 1.1159 | 1.2358 |

C3-E mean Delta Alpha over all 18 = **1.3312**.

These combined values are descriptive for the purposively assembled survey panel. They are not population estimands for the 575 firms.

### C6-E reference uptake over 18

- BASELINE Gemini: 6/18 = 33.3%
- BASELINE GPT: 7/18 = 38.9%
- HIGH Gemini: 6/18 = 33.3%
- HIGH GPT: 9/18 = 50.0%

The result continues to show that C6-E is not mechanically identical to C3-E.

## 7. Interpretation boundary

Keep the following objects separate:

1. strict archival expert action (A-I only);
2. broad-search OE-like component (P-R diagnostic only);
3. matched-information human survey choice (A-R after collection);
4. LLM/C3-E selected action;
5. Oracle/Simulator policy value;
6. realized FY2025 action/outcome.

Only A-I currently support archival expert-vs-model exact-action agreement.

J-R currently support model-side pre-survey analysis only.

After survey collection, the primary human comparison should be: Human(IC-b, candidate9, B1) vs C4(IC-b, candidate9, B1).

C4R and C6-E remain secondary because they add a review/reference procedure that human respondents do not receive in the initial matched decision.

Human modal choice remains a human baseline, not causal ground truth.
