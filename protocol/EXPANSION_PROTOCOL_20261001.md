# Expansion protocol — 2026-10-01

Status: prospective rule for this extension, NOT a preregistration of the original study. Existing strict-9 results have already been inspected. Freeze these extension rules before computing the six additional survey cases or inspecting their policy outcomes.

## Two distinct populations

1. HB2024-v1.0 strict-9 stays byte-for-byte unchanged. An archival extension requires NEW source evidence passing the EXISTING inclusion, source-layer, temporal, canonical-mechanism and no-material-omitted-co-action rules. Do not rename a larger human survey as strict-15.
2. H15-v1 is a supplemental matched-information human judgment panel: the existing nine cases A–I plus six financial-state-selected cases J–O. A new survey case does not need an archival expert recommendation. It receives no expert label until respondents provide judgments.

## Archival Pass 3

Re-review all 13 records with selection_status PRIMARY_UNAVAILABLE_AFTER_PASS2 and all four canonical-but-not-strict records in the frozen firm-level CSV. Preserve discovery metadata and failures. Original 2024 primary reports and additional verifiable 2024 primary documents for these same firms are eligible. Do not promote from titles, snippets, later financial outcomes or model agreement. IR remains a management-plan layer, not an independent expert baseline. Preserve v1 and record additional eligible cases separately, including the exact primary document, publication date, statement type, canonical mechanism, relevant page, co-actions, and limitations. Outcome-blinding is limited: earlier strict-9 results are known; no new model outputs/payoffs are consulted in re-audit. Do not claim that the original mappings were independently re-coded by a new human reviewer.

## Six-case survey extension: fixed algorithm

Source: frozen FY2024 firm_payload_source.parquet, release tag thesis-v43-reproduction-kit-v1.0.4, campaign 2cf6d6d0e4250e66ce882ab95f9d641f2c73711ffbc6429e9a203dcc2ee680a2. Expected SHA256: 10e78a84a1fdcd8af80b4057795214c896a20c4c1a7444a9cd01c7eab4dd3d56. Use ONLY firm_key and the 27 IC-b visible fields; use names only AFTER selection to construct the researcher crosswalk. No C3-E reference, LLM action, Oracle score, historical expert action, or FY2025 result may enter the selection function.

Thresholds: pandas quantile with linear interpolation, computed from finite values among all 575 unique FY2024 firms. Working-capital burden = inventory/revenue + receivables/revenue, requiring both components finite. Derived sums are used for selection only, not added to respondent input.

In this fixed order, draw one non-overlapping case from each pool after excluding the original nine and earlier draws:

J LEVERAGE: debt_to_assets >= its Q75.
K LIQUIDITY: current_ratio <= its Q25.
L SHORT_DEBT: short_debt_to_total_debt >= its Q75.
M WORKING_CAPITAL: working-capital burden >= its Q75.
N CAPEX: capex_to_revenue >= its Q75.
O STRONG_BALANCE_SHEET: debt_to_assets <= Q25, current_ratio >= Q75, operating_margin > 0.

Within each pool choose the minimum SHA256 of UTF-8 string H15-v1|20261001|<STRATUM>|<firm_key>, with firm_key as tie-breaker. Record pool size, threshold, chosen hash and raw state. Empty pools FAIL; do not substitute an outcome-selected case or silently relax a threshold. Preserve the old A–I crosswalk.

These are coverage-oriented, purposive strata, not estimates of the prevalence of an optimal action. High leverage does not imply that DL is a ground-truth answer. The six strata may overlap conceptually although selected firms must be distinct. The combined 15 are not a representative sample of the 575.

## Survey constraints

Keep IC-b fields, company-name blinding, candidate9/B1, one initial action without an external reference, confidence and short reason. Primary matched-process comparator is C4; C4R/C6-E have additional review/reference procedures and are secondary comparisons, not fully matched human conditions. Keep human-readable rounded presentation; preserve exact underlying vectors/data for scoring and audit. Mark unavailable data as unavailable, not zero. Keep industry codes as originally supplied; do not silently add industry-name lookup or analyst context. No financial outcomes or archival action labels on respondent pages. No answer key in public respondent materials.

Fifteen cases may impose more burden. Use two counterbalanced orders (A–O and reverse) as optional equivalent forms; do not randomize questions away from case data. Let each participant complete only one version. No claims about sufficient sample size or completion time before a pilot. Do not alter an already fielded form: create a new version, preserve prior responses separately.

## Analysis boundary

Report old nine, new six, and combined fifteen separately. Human choice distributions and support for each policy are not causal ground truth. Score selected human candidate IDs using exact frozen vectors on the same substrate. Treat repeated choices within respondents and firms as dependent; do not call 15 times respondents independent firms. This extension does not identify the causal effect of an unchosen action.

## Publication and reproducibility

Archive source hashes, selection pools, audit decisions, deterministic generated materials, and validation results. Do not commit copyrighted full PDFs or respondent data. Create an unpublished Google Form draft by default; researcher verifies consent/contact wording, institutional requirements and preview before publishing. Existing HB2024-v1.0 source files must be unchanged.
