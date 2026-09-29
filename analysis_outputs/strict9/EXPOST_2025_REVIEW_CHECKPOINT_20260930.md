# Strict-9 2025 ex-post review checkpoint — 2026-09-30

## Status

**PROVISIONAL REVIEW CHECKPOINT — NOT A FROZEN RESULT**

This file records the analysis reviewed on 2026-09-30 so that the reasoning is preserved in version control. It does **not** modify the frozen `HB2024-v1.0` archival benchmark and does **not** yet promote the 2025 follow-up to a source-audited thesis result.

The 2025 action / financial / credit-status evidence must still be source-audited and frozen before any thesis claim is finalized.

## 1. Existing strict-9 anchor retained

The strict archival subset remains:

- 대한해운
- 무림P&P
- HMM
- 더존비즈온
- 카페24
- 랩지노믹스
- 율촌
- 스튜디오드래곤
- 뉴로메카

Frozen human action distribution:

- OE: 7
- CX: 2

Existing downstream comparison surface:

- candidate9
- IC-b
- B1
- Run 1
- Strict ITT
- LLM policies: C4, C4R, C6-E
- models: GPT-5.4-mini, Gemini 3.1 Flash-Lite
- generation regimes: BASELINE, HIGH
- reference policy: frozen Candidate-IQL ensemble C3-E

Existing exact-action agreement against the frozen human archival action:

| Regime | Model | C4 | C4R | C6-E |
|---|---|---:|---:|---:|
| BASELINE | Gemini 3.1 Flash-Lite | 3/9 | 2/9 | 1/9 |
| BASELINE | GPT-5.4-mini | 3/9 | 3/9 | 3/9 |
| HIGH | Gemini 3.1 Flash-Lite | 3/9 | 3/9 | 3/9 |
| HIGH | GPT-5.4-mini | 2/9 | 2/9 | 2/9 |

C3-E exact agreement with the frozen human action remains **1/9**.

Existing same-substrate Oracle-value comparison:

| Policy / condition | ΔAlpha | ΔBeta | ΔGamma |
|---|---:|---:|---:|
| Human-mapped | +0.6003 | +0.0944 | +0.1036 |
| C3-E | +0.8649 | -0.1557 | -0.1284 |
| BASELINE Gemini C4 | +0.9385 | +0.0785 | +0.2118 |
| BASELINE Gemini C6-E | +0.5947 | +0.0869 | +0.1625 |
| BASELINE GPT C4 | +0.7979 | +0.0640 | +0.0886 |
| BASELINE GPT C6-E | +0.7979 | +0.0624 | +0.0960 |
| HIGH Gemini C4 | +0.9385 | +0.0800 | +0.2870 |
| HIGH Gemini C6-E | +0.8388 | +0.0942 | +0.2378 |
| HIGH GPT C4 | +0.5538 | +0.0513 | +0.0886 |
| HIGH GPT C6-E | +1.0245 | +0.0758 | +0.3244 |

These results already show that **human-action agreement, C3-E reference uptake, and Oracle policy value are distinct validation targets**.

## 2. Preliminary 2025 realized-action follow-up

The current review added a provisional fourth layer:

`2024 archival expert action -> 2025 actual firm action -> 2025 realized financial change -> observed credit-status change`

The current case-level review is summarized below.

| Firm | 2024 archival action | Preliminary 2025 realized action reading | Canonical reading | Current interpretation |
|---|---|---|---|---|
| 대한해운 | CX | vessel-sale / restrained newbuild investment with debt reduction | CX + DL co-action | human CX direction realized; financial burden also reduced |
| 무림P&P | OE | high-efficiency recovery-boiler / energy-cost reduction program | OE | action realized, but accounting benefit has timing lag |
| HMM | CX | material vessel / green-equipment investment expansion | growth CAPEX expansion; outside candidate9 and opposite to CX | strongest counterexample to human CX and a limitation of one-sided CX action semantics |
| 더존비즈온 | OE | AI/cloud/process efficiency and lower outsourcing cost | OE | direct realization of OE direction |
| 카페24 | OE | continued cost-efficiency / restructuring effects | OE | realized direction consistent with archival OE |
| 랩지노믹스 | OE | LDT implementation and testing-cost reduction | OE | OE realized, but other losses dominated 2025 accounting outcome |
| 율촌 | OE | automation continued while Poland growth investment also continued | OE + material growth-CAPEX co-action | not clean OE-only realization |
| 스튜디오드래곤 | OE | production-cost efficiency / AI / casting diversification | OE | OE realized; annual outcome also affected by content-lineup conditions |
| 뉴로메카 | OE | component internalization | OE | OE realized; operating loss improved but overall financial condition remained weak |

### Preliminary realization count

If each company is forced to one **primary** canonical action, the archival human action is directionally concordant with the observed 2025 primary action in **8/9** firms, with HMM as the clear contradiction.

A more conservative representation is:

- **7 exact**
- **1 partial / material co-action**: 율촌
- **1 contradiction / out-of-space**: HMM

This is the preferred wording until the 2025 evidence is fully audited.

Because eight of the nine preliminary 2025 primary mappings are the same as the frozen archival human label, the already-computed candidate9 action-match counts for C4/C6-E/C3-E remain approximately the same on this tiny follow-up set. However, HMM exposes an important structural issue: the realized action is growth-CAPEX expansion, which the frozen candidate9 action space cannot represent as a positive growth-investment action. Therefore, no candidate9 policy could exactly match that realized decision.

## 3. What this does and does not say

### Supported descriptive conclusion

The current evidence separates at least four concepts:

1. Oracle policy value
2. archival expert action
3. learned-reference uptake / LLM policy action
4. realized corporate action

They are not interchangeable.

A policy may score highly on the Oracle substrate while disagreeing with both the archival expert action and the firm's later realized action.

### Not supported

Do **not** state:

- "human experts are 8/9 accurate"
- "humans outperform LLMs"
- "the human recommendation caused the 2025 financial / rating outcome"
- "C3-E or LLM was wrong because the company chose another action"
- "2025 rating changes are caused by 2025 actions"

The realized firm action is not the counterfactual optimal action, and the observed outcome does not identify the causal effect of unchosen alternatives.

## 4. Human benchmark is not a matched-condition human baseline

The strict-9 archival expert records are **not** an apples-to-apples human-vs-LLM experiment.

Important asymmetries:

### Information-set asymmetry

Archival experts often had access to:

- firm identity
- issuer-specific business context
- management plans
- investment plans
- projects already underway
- industry / competitive context beyond the IC-b schema

The main LLM comparison surface instead uses the thesis-defined structured input, principally IC-b on candidate9/B1.

### Response-process asymmetry

The human experts did not solve a pre-specified nine-action classification task.

The actual process was:

`real firm analysis -> free-form expert report -> post-hoc mapping to candidate9`

whereas the evaluated LLM candidate9 condition was:

`thesis-defined structured input -> direct choice inside candidate9`

Therefore the strict-9 archive must be described as an **archival expert-action external anchor**, not as a matched human performance control group.

## 5. Ground truth and human baseline must be separated

A human survey would **not** create causal ground truth.

Multiple experts may disagree while all remain plausible. Their answers would estimate a human decision distribution / human baseline under specified conditions, not reveal the true counterfactual action that maximizes future credit quality.

For the current thesis:

- **formal policy baselines** remain C0 / heuristic references / C3-E / other frozen comparison policies;
- **external ecological anchor** is the strict-9 archival expert-action set;
- **ex-post observational anchor** is the 2025 realized-action / financial / credit-status follow-up;
- **true causal ground truth** remains unobserved.

A matched-condition human study becomes necessary only if the thesis is changed to make a direct claim such as:

> under the same information and action schema, human experts outperform / match / underperform the LLM policy.

That is a different estimand from the current validation-first policy-harness question.

## 6. Implication for whether a human survey is required

Current review conclusion:

**A new human-subject survey is not methodologically required for the existing thesis estimand, provided that the strict-9 evidence is framed as an external archival anchor rather than a human-vs-LLM accuracy benchmark.**

If a supervisor explicitly requires a matched human baseline, the smallest defensible extension would be a separate strict-9 matched-condition study using:

- the same IC-b information package,
- the same candidate9 definitions,
- the same B1 rule,
- expert respondents,
- action choice plus short rationale,
- inter-rater agreement reported explicitly.

That extension should be treated as a separate validation layer rather than silently redefining the archival benchmark.

## 7. Preferred low-cost next analysis before any human survey

Before recruiting human participants, test the most important identified confound directly with a strict-9 LLM sensitivity.

### Condition A — current structured information

`financials + industry + year -> candidate9`

### Condition B — matched richer firm context

`financials + industry + firm-specific 2024 context -> candidate9`

The richer context must redact the expert's final recommendation/action sentence so that the model cannot simply copy the archival answer.

### Optional Condition C — richer context + free-form recommendation

`same redacted richer context -> free-form recommendation -> same post-hoc mapping rule`

This can separate, descriptively:

- information-set effect
- response-space / schema effect
- remaining policy-choice disagreement

This sensitivity is much closer to the thesis's existing RQ5 / policy-harness logic than immediately launching a new human-subject experiment.

## 8. HMM as a key external-validity counterexample

HMM should be preserved as a focused case rather than forced into A0.

The frozen action space defines CX as restraint / reduction of growth CAPEX. A realized decision to expand vessel investment is therefore not no-action; it is a direction that the current candidate9 space cannot represent.

This case highlights two separate limitations:

1. **action-space coverage**: candidate9 is asymmetric for growth CAPEX;
2. **simulator semantics**: near-term cash / leverage effects of CAPEX may not capture longer-run operating-cost or competitive benefits from new assets.

The 2025 credit-rating evidence must still be date-aligned carefully. A rating action issued during 2025 may rely mainly on FY2024 information and therefore cannot automatically be interpreted as an outcome caused by a 2025 investment decision.

## 9. Source-audit requirements before promotion

Before this checkpoint becomes a thesis result, freeze for each firm:

- 2025 action evidence source
- source date
- exact action evidence summary
- canonical mapping and co-action flag
- FY2024 and FY2025 financial values used
- rating agency
- rating type / instrument
- rating date
- information period underlying the rating
- whether 2024 -> 2025 rating comparison is truly comparable
- any agency change or instrument change
- source URL / document hash where possible

Until that audit is complete, all realized-outcome findings in this file remain **PROVISIONAL**.

## Bottom line

The review to date supports adding a small ex-post external-validation layer, but it does **not** justify converting strict-9 into a matched human benchmark.

The most defensible thesis framing remains:

> Oracle policy value, archival expert recommendations, realized corporate actions, and subsequent credit outcomes are different validation objects. The strict-9 evidence is useful precisely because it shows that these objects can diverge.
