# Strict-9 checkpoint — 2026-09-30

This checkpoint freezes the work completed so far on the HB2024-v1.0 strict archival subset. It does **not** modify the frozen benchmark itself.

## Scope

- Benchmark: `HB2024-v1.0`
- Strict firms: 9
- Human action distribution: OE 7, CX 2
- Human benchmark source: `outputs/strict_archival_benchmark.csv`
- Downstream comparison surface:
  - candidate9
  - IC-b
  - B1
  - Run 1
  - Strict ITT
  - policies: C4, C4R, C6-E
  - models: GPT-5.4-mini, Gemini 3.1 Flash-Lite
  - generation regimes: BASELINE, HIGH
- Reference policy: frozen Candidate-IQL ensemble C3-E

## Completed analysis 1 — exact-action agreement

Exact-match rates against the frozen human-mapped action:

| Regime | Model | C4 | C4R | C6-E |
|---|---|---:|---:|---:|
| BASELINE | Gemini 3.1 Flash-Lite | 3/9 | 2/9 | 1/9 |
| BASELINE | GPT-5.4-mini | 3/9 | 3/9 | 3/9 |
| HIGH | Gemini 3.1 Flash-Lite | 3/9 | 3/9 | 3/9 |
| HIGH | GPT-5.4-mini | 2/9 | 2/9 | 2/9 |

C3-E exact agreement with the strict human action was **1/9**.

Important case-level pattern:

- The two human CX cases (대한해운, HMM) were never matched by the LLM candidate9 outputs across the evaluated model/regime/policy cells.
- Agreement was concentrated in OE cases.
- Some disagreements were stable at the firm level rather than random:
  - 스튜디오드래곤: OE matched across all 12 evaluated LLM cells.
  - 뉴로메카: human OE, LLM selected MX1 across all 12 evaluated cells.
  - 무림P&P: human OE, LLM selected RF across all 12 evaluated cells.

## Completed analysis 2 — C6-E reference uptake

C6-E adoption of the supplied C3-E reference:

| Regime | Model | C3-E reference adoption |
|---|---|---:|
| BASELINE | Gemini | 4/9 |
| BASELINE | GPT | 2/9 |
| HIGH | Gemini | 3/9 |
| HIGH | GPT | 3/9 |

C6-E did not mechanically copy the reference. There are cases where C3-E disagreed with the human archival action but C6-E rejected the reference and matched the human action.

## Completed analysis 3 — Oracle value comparison

The frozen human action for each firm was counterfactually applied to the **same FY2024 state** and scored on the same Simulator–Oracle substrate used for C4, C6-E, and C3-E.

The primary descriptive metric is no-op-adjusted Oracle value, `delta_R_score`.

### Common reference policies

| Policy | ΔAlpha | ΔBeta | ΔGamma |
|---|---:|---:|---:|
| Human-mapped | +0.6003 | +0.0944 | +0.1036 |
| C3-E | +0.8649 | -0.1557 | -0.1284 |

### LLM policies

| Regime | Model | Policy | ΔAlpha | ΔBeta | ΔGamma |
|---|---|---|---:|---:|---:|
| BASELINE | Gemini | C4 | +0.9385 | +0.0785 | +0.2118 |
| BASELINE | Gemini | C6-E | +0.5947 | +0.0869 | +0.1625 |
| BASELINE | GPT | C4 | +0.7979 | +0.0640 | +0.0886 |
| BASELINE | GPT | C6-E | +0.7979 | +0.0624 | +0.0960 |
| HIGH | Gemini | C4 | +0.9385 | +0.0800 | +0.2870 |
| HIGH | Gemini | C6-E | +0.8388 | +0.0942 | +0.2378 |
| HIGH | GPT | C4 | +0.5538 | +0.0513 | +0.0886 |
| HIGH | GPT | C6-E | +1.0245 | +0.0758 | +0.3244 |

For C3-E versus Human-mapped on Oracle-Alpha:

- mean gap: **+0.2646**
- firm-level W/T/L: **2 / 3 / 4**

Thus the Alpha mean advantage of C3-E is driven by a small number of large firm-level gains rather than broad dominance across the nine firms.

## Current interpretation

The strict-9 evidence separates three distinct concepts that should not be conflated:

1. **Human action agreement**
2. **Learned-reference uptake**
3. **Oracle policy value**

These are empirically different. A policy can disagree with the archival human action while obtaining an equal or higher Oracle score, and C3-E can score strongly on Oracle-Alpha while not retaining the same direction on Beta/Gamma.

The human-mapped policy is not an Alpha-maximizing policy, but its mean no-op-adjusted score is positive across all three Oracle backends in this subset.

## Interpretation boundary

- n=9 is a high-precision external anchor, not a representative sample.
- Human labels are OE 7 / CX 2, so action coverage is narrow and imbalanced.
- Human reports and model inputs are contemporaneous but not matched-information observations.
- Oracle scores are counterfactual evaluator outputs, not realized causal outcomes.
- No broad claim that “human”, “LLM”, or “C3-E” is globally superior is supported by this subset.

## Artifacts

- `analysis/strict9_external_anchor.py`
- `analysis/strict9_oracle_value.py`
- `analysis_outputs/strict9/STRICT9_REPORT.md`
- `analysis_outputs/strict9/STRICT9_ORACLE_VALUE_REPORT.md`
- `analysis_outputs/strict9/strict9_case_level.csv`
- `analysis_outputs/strict9/strict9_summary.csv`
- `analysis_outputs/strict9/strict9_reference_analysis.csv`
- `analysis_outputs/strict9/strict9_transitions.csv`
- `analysis_outputs/strict9/strict9_oracle_case_level.csv`
- `analysis_outputs/strict9/strict9_oracle_summary.csv`
- `analysis_outputs/strict9/strict9_oracle_pairwise_vs_human.csv`

## Next step

The next analysis is the 2025 realized-outcome follow-up:

`2024 archival human action -> 2025 actual firm action -> 2025 realized financial change -> observed credit-status change`

That follow-up is **not included as a finalized result in this checkpoint yet**. It should be added only after each firm's 2025 action, FY2025 financials, and comparable credit-rating evidence are source-audited and frozen.
