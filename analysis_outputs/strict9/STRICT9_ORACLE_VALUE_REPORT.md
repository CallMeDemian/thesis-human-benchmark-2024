# Strict-9 Oracle value comparison

Human means the frozen human archival action (OE/CX) applied counterfactually to the same FY2024 firm state and scored by the same Simulator–Oracle substrate. It is not the realized effect of the historical human recommendation.

Primary descriptive metric below is no-op-adjusted Oracle score (Δ vs A0). Because all policies are scored on the same nine firms, absolute-score ordering and Δ-score ordering are equivalent within each Oracle.

## Common reference policies

| Policy | ΔAlpha | ΔBeta | ΔGamma |
|---|---:|---:|---:|
| Human-mapped | 0.6003 | 0.0944 | 0.1036 |
| C3-E | 0.8649 | -0.1557 | -0.1284 |

## LLM C4 / C6-E by generation regime

| Regime | Model | Policy | ΔAlpha | Gap vs human (Alpha) | W/T/L vs human | ΔBeta | ΔGamma |
|---|---|---|---:|---:|---:|---:|---:|
| BASELINE | google_gemini31flashlite | C4 | 0.9385 | +0.3382 | 1/7/1 | 0.0785 | 0.2118 |
| BASELINE | google_gemini31flashlite | C6-E | 0.5947 | -0.0056 | 1/5/3 | 0.0869 | 0.1625 |
| BASELINE | openai_gpt54mini | C4 | 0.7979 | +0.1977 | 1/7/1 | 0.0640 | 0.0886 |
| BASELINE | openai_gpt54mini | C6-E | 0.7979 | +0.1977 | 1/7/1 | 0.0624 | 0.0960 |
| HIGH | google_gemini31flashlite | C4 | 0.9385 | +0.3382 | 1/7/1 | 0.0800 | 0.2870 |
| HIGH | google_gemini31flashlite | C6-E | 0.8388 | +0.2385 | 1/6/2 | 0.0942 | 0.2378 |
| HIGH | openai_gpt54mini | C4 | 0.5538 | -0.0464 | 1/6/2 | 0.0513 | 0.0886 |
| HIGH | openai_gpt54mini | C6-E | 1.0245 | +0.4242 | 2/5/2 | 0.0758 | 0.3244 |

## C3-E versus Human-mapped

- Alpha mean gap: **+0.2646**; firm-level W/T/L = **2/3/4**.

## Interpretation boundary

This is a paired, same-substrate value comparison over only nine strict archival firms. It answers whether the mapped human action, C4, C6-E, or C3-E receives a higher counterfactual Oracle score on these firms. It does not establish that the higher-scoring policy would have produced the better realized credit outcome in the real world.

Exact-action agreement and Oracle value are distinct outcomes: two policies can choose different actions yet receive similar or higher Oracle value, and a policy can match the human action while not maximize the evaluation substrate.
