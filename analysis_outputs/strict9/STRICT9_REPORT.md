# Strict-9 human benchmark external-anchor analysis

This analysis links the frozen HB2024-v1.0 strict one-action archival subset to the frozen V4.3 candidate9/B1/IC-b outputs and the C3-E reference policy. The human archive is not modified.

- Strict firms: **9** (대한해운, 무림P&P, HMM, 더존비즈온, 카페24, 랩지노믹스, 율촌, 스튜디오드래곤, 뉴로메카)
- Human action distribution: **OE 7, CX 2**
- LLM comparison surface: candidate9 / IC-b / B1 / Run 1 / Strict ITT
- Conditions: C4, C4R, C6-E; models analyzed separately; BASELINE and HIGH reported separately
- C3-E: Candidate-IQL ensemble reference, evaluated once because its firm actions are invariant to LLM generation regime

## Exact-action agreement

| Regime | Model | Policy | Exact | Rate | Wilson 95% CI | Kappa | Macro recall (OE/CX) |
|---|---|---|---:|---:|---:|---:|---:|
| BASELINE | google_gemini31flashlite | C4 | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| BASELINE | google_gemini31flashlite | C4R | 2/9 | 22.2% | [6.3%, 54.7%] | 0.060 | 14.3% |
| BASELINE | google_gemini31flashlite | C6-E | 1/9 | 11.1% | [2.0%, 43.5%] | 0.027 | 7.1% |
| BASELINE | openai_gpt54mini | C4 | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| BASELINE | openai_gpt54mini | C4R | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| BASELINE | openai_gpt54mini | C6-E | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| HIGH | google_gemini31flashlite | C4 | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| HIGH | google_gemini31flashlite | C4R | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| HIGH | google_gemini31flashlite | C6-E | 3/9 | 33.3% | [12.1%, 64.6%] | 0.100 | 21.4% |
| HIGH | openai_gpt54mini | C4 | 2/9 | 22.2% | [6.3%, 54.7%] | 0.060 | 14.3% |
| HIGH | openai_gpt54mini | C4R | 2/9 | 22.2% | [6.3%, 54.7%] | 0.060 | 14.3% |
| HIGH | openai_gpt54mini | C6-E | 2/9 | 22.2% | [6.3%, 54.7%] | 0.060 | 14.3% |
| REFERENCE | Candidate-IQL ensemble | C3-E | 1/9 | 11.1% | [2.0%, 43.5%] | -0.286 | 7.1% |

## Revision / generation-regime transitions

| Regime | Model | Comparison | Wrong→Correct | Correct→Wrong | Net match change | McNemar exact p |
|---|---|---|---:|---:|---:|---:|
| BASELINE | google_gemini31flashlite | C4R vs C4 | 0 | 1 | -11.1%p | 1.0000 |
| BASELINE | google_gemini31flashlite | C6-E vs C4 | 0 | 2 | -22.2%p | 0.5000 |
| BASELINE | google_gemini31flashlite | C6-E vs C4R | 0 | 1 | -11.1%p | 1.0000 |
| BASELINE | openai_gpt54mini | C4R vs C4 | 0 | 0 | +0.0%p | 1.0000 |
| BASELINE | openai_gpt54mini | C6-E vs C4 | 0 | 0 | +0.0%p | 1.0000 |
| BASELINE | openai_gpt54mini | C6-E vs C4R | 0 | 0 | +0.0%p | 1.0000 |
| HIGH | google_gemini31flashlite | C4R vs C4 | 0 | 0 | +0.0%p | 1.0000 |
| HIGH | google_gemini31flashlite | C6-E vs C4 | 0 | 0 | +0.0%p | 1.0000 |
| HIGH | google_gemini31flashlite | C6-E vs C4R | 0 | 0 | +0.0%p | 1.0000 |
| HIGH | openai_gpt54mini | C4R vs C4 | 0 | 0 | +0.0%p | 1.0000 |
| HIGH | openai_gpt54mini | C6-E vs C4 | 0 | 0 | +0.0%p | 1.0000 |
| HIGH | openai_gpt54mini | C6-E vs C4R | 0 | 0 | +0.0%p | 1.0000 |
| HIGH_vs_BASELINE | google_gemini31flashlite | C4 | 1 | 1 | +0.0%p | 1.0000 |
| HIGH_vs_BASELINE | google_gemini31flashlite | C4R | 1 | 0 | +11.1%p | 1.0000 |
| HIGH_vs_BASELINE | google_gemini31flashlite | C6-E | 2 | 0 | +22.2%p | 0.5000 |
| HIGH_vs_BASELINE | openai_gpt54mini | C4 | 0 | 1 | -11.1%p | 1.0000 |
| HIGH_vs_BASELINE | openai_gpt54mini | C4R | 0 | 1 | -11.1%p | 1.0000 |
| HIGH_vs_BASELINE | openai_gpt54mini | C6-E | 0 | 1 | -11.1%p | 1.0000 |

## C6-E reference behavior

| Regime | Model | C3-E matches human | C6-E matches human | C6-E adopts C3-E | Adoption rate |
|---|---|---:|---:|---:|---:|
| BASELINE | google_gemini31flashlite | 1/9 | 1/9 | 4/9 | 44.4% |
| BASELINE | openai_gpt54mini | 1/9 | 3/9 | 2/9 | 22.2% |
| HIGH | google_gemini31flashlite | 1/9 | 3/9 | 3/9 | 33.3% |
| HIGH | openai_gpt54mini | 1/9 | 2/9 | 3/9 | 33.3% |

## Interpretation boundary

The strict-9 set is a high-precision external anchor, not a representative human sample. With n=9 and a 7/2 OE/CX label mix, estimates are necessarily imprecise and action coverage is narrow. Exact-match rates and transition counts are therefore descriptive. McNemar p-values are included only as small-sample diagnostics, not as evidence for broad population claims.

The benchmark is also contemporaneous rather than matched-information: 2024 human reports may use information vintages that differ from the FY2024 state supplied to the model. Agreement is therefore evidence of action-direction convergence under different information processes, not a randomized human-vs-LLM accuracy test.

## Next analysis boundary

Do not broaden the strict set post hoc. Any later 13-case canonical sensitivity or 113-case action-space coverage analysis should be emitted as a separate layer and must not overwrite HB2024-v1.0.
## Extension note — 2026-10-01 broad Pass-2 / Pass-3 and Human-18

The strict-9 result above remains the authoritative independent-expert archival anchor. A substantially broader follow-up search was completed without relaxing the frozen source hierarchy or strict one-action gate:

- 341 unresolved / previously negative firms entered broad Pass-2;
- 1,023 public report-index requests were executed;
- all 575 firms were additionally screened through report-title windows;
- 32 non-strict action-term leads were taken to terminal Pass-3 review;
- unresolved leads after completion: **0**;
- newly eligible independent-expert strict cases: **0**.

Accordingly, the independent-expert archival anchor remains **strict-9** rather than being post-hoc enlarged.

The extension adds two separate layers that must not be pooled into strict-9:

1. six financial-state diversity cases for matched-information human judgment (`ADDITIONAL_STATE_6`);
2. three broad-search action-space diagnostic cases (`BROAD_DIAGNOSTIC_3`: 하나투어, 비투엔, 휠라홀딩스).

The matched-information survey therefore contains **18 anonymized cases (A-R)** under the same `IC-b / candidate9 / B1` information/action contract. Model-side C4/C4R/C6-E/C3-E and Oracle Alpha/Beta/Gamma outputs have been joined for all 18 cases. The original strict-9 regression check remains **PASS: 12 cells checked, 0 mismatches**.

See:
- `analysis_outputs/HUMAN18_FINAL_HANDOFF.md`
- `analysis_outputs/broad_archival/BROAD_PASS3_FINAL_REVIEW.md`
- `analysis_outputs/human18/downstream/HUMAN18_DOWNSTREAM_REPORT.md`

This extension does not convert Human-18 into an archival human benchmark. Only A-I carry frozen archival expert actions; J-R receive human labels only from the prospective matched-information survey.

