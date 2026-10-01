# Human-18 확장 패널 — broad-search diagnostics 통합

## 분석 범위

기존 strict-9 결과는 수정하지 않는다. A-I는 frozen archival expert anchor, J-O는 재무상태 다양성 6개, P-R은 broad Pass-2/Pass-3에서 확보한 action-space diagnostic 3개다. J-R에는 strict human action label이 없으므로 human-vs-LLM exact agreement를 계산하지 않는다.

이번 확장은 동일한 frozen V4.3 candidate9 / IC-b / B1 / Run1 / Strict ITT 결과에서 C4, C4R, C6-E, C3-E의 행동과 Oracle alpha/beta/gamma 값을 18개 사례에 대해 결합한다. Candidate ceiling은 같은 firm의 9개 frozen candidate 중 평가기반 점수가 가장 높은 값이며 현실의 정답이 아니다.

## 추가 9개 사례의 model-side 결과

| Case | 선정층 | C3-E | Alpha ceiling | Baseline Gemini C4/C4R/C6-E | Baseline GPT C4/C4R/C6-E | High Gemini C4/C4R/C6-E | High GPT C4/C4R/C6-E |
|---|---|---|---|---|---|---|---|
| J | LEVERAGE | RF | MX1;OE | MX1/MX1/MX1 | WC1/WC1/RF | CX/CX/CX | MX1/MX1/RF |
| K | LIQUIDITY | OE | OE | MX1/MX1/MX1 | WC1/WC1/OE | MX1/MX1/MX1 | MX1/MX1/OE |
| L | SHORT_DEBT | RF | RF | MX2/MX2/MX2 | MX1/MX1/RF | OE/MX1/RF | RF/RF/RF |
| M | WORKING_CAPITAL | WC1 | DL | MX2/MX2/MX2 | MX2/MX2/MX2 | OE/OE/OE | MX1/MX1/WC1 |
| N | CAPEX | OE | WC1 | WC2/WC2/WC2 | WC1/WC1/WC1 | DL/DL/MX1 | WC1/WC1/OE |
| O | STRONG_BALANCE_SHEET | OE | OE | RF/RF/RF | WC1/WC1/OE | OE/OE/OE | OE/OE/A0 |
| P | ARCHIVAL_ACTION_SPACE_DIAGNOSTIC | MX2 | A0;CX;DL;MX1;MX2;OE;RF;WC1;WC2 | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 |
| Q | ARCHIVAL_ACTION_SPACE_DIAGNOSTIC | OE | CX;OE;WC1 | OE/MX1/OE | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 |
| R | ARCHIVAL_ACTION_SPACE_DIAGNOSTIC | RF | DL | RF/RF/RF | RF/RF/RF | RF/RF/RF | RF/RF/RF |

## Panel별 Oracle alpha 요약

| Panel | Regime | Model | Policy | n | mean dAlpha | median dAlpha | mean regret to ceiling | ceiling hit rate |
|---|---|---|---|---:|---:|---:|---:|---:|
| ARCHIVAL_ANCHOR_9 | BASELINE | google_gemini31flashlite | C4 | 9 | 0.9385 | 0.0000 | 0.4624 | 77.8% |
| ARCHIVAL_ANCHOR_9 | BASELINE | google_gemini31flashlite | C4R | 9 | 0.9807 | 0.0000 | 0.4203 | 66.7% |
| ARCHIVAL_ANCHOR_9 | BASELINE | google_gemini31flashlite | C6-E | 9 | 0.5947 | 0.0000 | 0.8063 | 55.6% |
| ARCHIVAL_ANCHOR_9 | BASELINE | openai_gpt54mini | C4 | 9 | 0.7979 | 0.0000 | 0.6030 | 77.8% |
| ARCHIVAL_ANCHOR_9 | BASELINE | openai_gpt54mini | C4R | 9 | 0.7979 | 0.0000 | 0.6030 | 77.8% |
| ARCHIVAL_ANCHOR_9 | BASELINE | openai_gpt54mini | C6-E | 9 | 0.7979 | 0.0000 | 0.6030 | 77.8% |
| ARCHIVAL_ANCHOR_9 | HIGH | google_gemini31flashlite | C4 | 9 | 0.9385 | 0.0000 | 0.4624 | 77.8% |
| ARCHIVAL_ANCHOR_9 | HIGH | google_gemini31flashlite | C4R | 9 | 0.9385 | 0.0000 | 0.4624 | 77.8% |
| ARCHIVAL_ANCHOR_9 | HIGH | google_gemini31flashlite | C6-E | 9 | 0.8388 | 0.0000 | 0.5622 | 66.7% |
| ARCHIVAL_ANCHOR_9 | HIGH | openai_gpt54mini | C4 | 9 | 0.5538 | 0.0000 | 0.8471 | 66.7% |
| ARCHIVAL_ANCHOR_9 | HIGH | openai_gpt54mini | C4R | 9 | 1.0245 | 0.0000 | 0.3765 | 77.8% |
| ARCHIVAL_ANCHOR_9 | HIGH | openai_gpt54mini | C6-E | 9 | 1.0245 | 0.0000 | 0.3765 | 77.8% |
| ARCHIVAL_ANCHOR_9 | REFERENCE | Candidate-IQL ensemble | C3-E | 9 | 0.8649 | 0.0000 | 0.5361 | 55.6% |
| ADDITIONAL_STATE_6 | BASELINE | google_gemini31flashlite | C4 | 6 | 0.5331 | 0.4750 | 1.4728 | 16.7% |
| ADDITIONAL_STATE_6 | BASELINE | google_gemini31flashlite | C4R | 6 | 0.5331 | 0.4750 | 1.4728 | 16.7% |
| ADDITIONAL_STATE_6 | BASELINE | google_gemini31flashlite | C6-E | 6 | 0.5331 | 0.4750 | 1.4728 | 16.7% |
| ADDITIONAL_STATE_6 | BASELINE | openai_gpt54mini | C4 | 6 | 0.5805 | 0.2372 | 1.4254 | 16.7% |
| ADDITIONAL_STATE_6 | BASELINE | openai_gpt54mini | C4R | 6 | 0.5805 | 0.2372 | 1.4254 | 16.7% |
| ADDITIONAL_STATE_6 | BASELINE | openai_gpt54mini | C6-E | 6 | 1.6046 | 1.5044 | 0.4014 | 66.7% |
| ADDITIONAL_STATE_6 | HIGH | google_gemini31flashlite | C4 | 6 | 0.1838 | 0.0915 | 1.8222 | 16.7% |
| ADDITIONAL_STATE_6 | HIGH | google_gemini31flashlite | C4R | 6 | 0.1838 | 0.0915 | 1.8222 | 16.7% |
| ADDITIONAL_STATE_6 | HIGH | google_gemini31flashlite | C6-E | 6 | 0.7580 | 0.2608 | 1.2480 | 33.3% |
| ADDITIONAL_STATE_6 | HIGH | openai_gpt54mini | C4 | 6 | 1.0259 | 0.6271 | 0.9801 | 66.7% |
| ADDITIONAL_STATE_6 | HIGH | openai_gpt54mini | C4R | 6 | 1.0259 | 0.6271 | 0.9801 | 66.7% |
| ADDITIONAL_STATE_6 | HIGH | openai_gpt54mini | C6-E | 6 | 1.3854 | 0.9385 | 0.6205 | 33.3% |
| ADDITIONAL_STATE_6 | REFERENCE | Candidate-IQL ensemble | C3-E | 6 | 1.4159 | 0.9385 | 0.5900 | 50.0% |
| BROAD_DIAGNOSTIC_3 | BASELINE | google_gemini31flashlite | C4 | 3 | 2.5606 | 2.9705 | 0.1850 | 66.7% |
| BROAD_DIAGNOSTIC_3 | BASELINE | google_gemini31flashlite | C4R | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | BASELINE | google_gemini31flashlite | C6-E | 3 | 2.5606 | 2.9705 | 0.1850 | 66.7% |
| BROAD_DIAGNOSTIC_3 | BASELINE | openai_gpt54mini | C4 | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | BASELINE | openai_gpt54mini | C4R | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | BASELINE | openai_gpt54mini | C6-E | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | google_gemini31flashlite | C4 | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | google_gemini31flashlite | C4R | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | google_gemini31flashlite | C6-E | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | openai_gpt54mini | C4 | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | openai_gpt54mini | C4R | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | openai_gpt54mini | C6-E | 3 | 1.5704 | -0.0000 | 1.1751 | 33.3% |
| BROAD_DIAGNOSTIC_3 | REFERENCE | Candidate-IQL ensemble | C3-E | 3 | 2.5606 | 2.9705 | 0.1850 | 66.7% |
| ALL_18 | BASELINE | google_gemini31flashlite | C4 | 18 | 1.0737 | 0.2372 | 0.7530 | 55.6% |
| ALL_18 | BASELINE | google_gemini31flashlite | C4R | 18 | 0.9298 | 0.2372 | 0.8969 | 44.4% |
| ALL_18 | BASELINE | google_gemini31flashlite | C6-E | 18 | 0.9018 | 0.0000 | 0.9249 | 44.4% |
| ALL_18 | BASELINE | openai_gpt54mini | C4 | 18 | 0.8542 | 0.0000 | 0.9725 | 50.0% |
| ALL_18 | BASELINE | openai_gpt54mini | C4R | 18 | 0.8542 | 0.0000 | 0.9725 | 50.0% |
| ALL_18 | BASELINE | openai_gpt54mini | C6-E | 18 | 1.1956 | 0.3293 | 0.6312 | 66.7% |
| ALL_18 | HIGH | google_gemini31flashlite | C4 | 18 | 0.7922 | 0.0000 | 1.0345 | 50.0% |
| ALL_18 | HIGH | google_gemini31flashlite | C4R | 18 | 0.7922 | 0.0000 | 1.0345 | 50.0% |
| ALL_18 | HIGH | google_gemini31flashlite | C6-E | 18 | 0.9338 | 0.0000 | 0.8929 | 50.0% |
| ALL_18 | HIGH | openai_gpt54mini | C4 | 18 | 0.8806 | 0.0915 | 0.9461 | 61.1% |
| ALL_18 | HIGH | openai_gpt54mini | C4R | 18 | 1.1159 | 0.0915 | 0.7108 | 66.7% |
| ALL_18 | HIGH | openai_gpt54mini | C6-E | 18 | 1.2358 | 0.0000 | 0.5909 | 55.6% |
| ALL_18 | REFERENCE | Candidate-IQL ensemble | C3-E | 18 | 1.3312 | 0.2608 | 0.4955 | 55.6% |

## C6-E reference uptake

| Panel | Regime | Model | C4=C3-E | C4R=C3-E | C6-E=C3-E | C6-E adoption |
|---|---|---|---:|---:|---:|---:|
| ARCHIVAL_ANCHOR_9 | BASELINE | google_gemini31flashlite | 2/9 | 3/9 | 4/9 | 44.4% |
| ARCHIVAL_ANCHOR_9 | BASELINE | openai_gpt54mini | 2/9 | 2/9 | 2/9 | 22.2% |
| ARCHIVAL_ANCHOR_9 | HIGH | google_gemini31flashlite | 2/9 | 2/9 | 3/9 | 33.3% |
| ARCHIVAL_ANCHOR_9 | HIGH | openai_gpt54mini | 2/9 | 3/9 | 3/9 | 33.3% |
| ADDITIONAL_STATE_6 | BASELINE | google_gemini31flashlite | 0/6 | 0/6 | 0/6 | 0.0% |
| ADDITIONAL_STATE_6 | BASELINE | openai_gpt54mini | 0/6 | 0/6 | 4/6 | 66.7% |
| ADDITIONAL_STATE_6 | HIGH | google_gemini31flashlite | 1/6 | 1/6 | 2/6 | 33.3% |
| ADDITIONAL_STATE_6 | HIGH | openai_gpt54mini | 2/6 | 2/6 | 5/6 | 83.3% |
| BROAD_DIAGNOSTIC_3 | BASELINE | google_gemini31flashlite | 2/3 | 1/3 | 2/3 | 66.7% |
| BROAD_DIAGNOSTIC_3 | BASELINE | openai_gpt54mini | 1/3 | 1/3 | 1/3 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | google_gemini31flashlite | 1/3 | 1/3 | 1/3 | 33.3% |
| BROAD_DIAGNOSTIC_3 | HIGH | openai_gpt54mini | 1/3 | 1/3 | 1/3 | 33.3% |
| ALL_18 | BASELINE | google_gemini31flashlite | 4/18 | 4/18 | 6/18 | 33.3% |
| ALL_18 | BASELINE | openai_gpt54mini | 3/18 | 3/18 | 7/18 | 38.9% |
| ALL_18 | HIGH | google_gemini31flashlite | 4/18 | 4/18 | 6/18 | 33.3% |
| ALL_18 | HIGH | openai_gpt54mini | 5/18 | 6/18 | 9/18 | 50.0% |

## 해석 경계

- A-I의 archival human-action agreement와 Human-mapped Oracle value는 기존 strict-9 결과가 권위 있는 결과이며 이 분석에서 다시 정의하지 않았다.
- J-R은 아직 인간 응답이 없으므로 현재 표는 model-side pre-survey baseline이다. 설문 수집 후 human modal action, 선택분포, confidence, rationale 및 LLM agreement를 추가해야 한다.
- J-O는 재무상태 다양성을 위한 목적표본이고 P-R은 broad-search diagnostic 사례다. 전체 18개는 575개 모집단의 대표표본이 아니다.
- Candidate ceiling과 Oracle regret는 평가기반 내부 비교량이다. 실제 기업행동이나 신용등급 변화의 ground truth가 아니다.
- 인터엠 기업 자체 경영정책 확장은 독립 전문가 strict benchmark와 분리한다.
