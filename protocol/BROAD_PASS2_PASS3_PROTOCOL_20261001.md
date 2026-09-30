# Broad archival Pass-2/Pass-3 expansion protocol — 2026-10-01

Status: prospective rule for this broad extension. HB2024-v1.0 and all previously inspected downstream results remain frozen.

## Objective

Expand the 2024 archival expert-action anchor without relaxing the frozen strict mapping rules and without selecting firms from LLM/Oracle agreement or payoff.

## Search population

Start from the frozen 575-firm population. The broad Pass-2 queue is the union of firms still lacking a reviewed primary human mapping after the previous workflow:
- selection_status = NO_REVIEWED_MAPPING_RECORD;
- selection_status = NO_REPORT_FOUND_AFTER_PASS1;
- selection_status = NO_REPORT_FOUND_AFTER_PASS2, retained as negative controls / search-completeness checks.

The 17 firms already covered by the bounded 2026-10-01 Pass-3 audit remain separately logged and are not silently recoded.

## Pass 2 — systematic discovery

For every firm in the queue, query public report indexes using stock code and firm name. Record positive and negative discovery results. Prefer:
1. CRA opinion/report indexes,
2. human-authored securities research indexes,
3. issuer IR indexes only as a separate management-policy layer.

Automated/AI summaries are discovery leads only. A report title or snippet cannot establish a strict canonical action.

No C3-E/C4/C4R/C6-E action, Simulator/Oracle score, 2025 outcome, or prior human-vs-model agreement may be read by the selection script.

## Pass 3 recovery queue — previously identified but incomplete primary evidence

In addition to newly discovered Pass-2 reports, re-open every frozen record for which a 2024 human report was already identified but the primary evidence was incomplete. This includes SECONDARY_SUMMARY_ONLY, PRIMARY_INDEX_AVAILABLE, DISCOVERY_INDEX_ONLY, PENDING_FULLTEXT_REVIEW, PRIMARY_REPORT_IDENTIFIED, PRIMARY_DOCUMENT_IDENTIFIED, PRIMARY_TEXT_REVIEW_PENDING, SECONDARY_SUMMARY_ACTION_CANDIDATE, PRIMARY_LATER_REPORT_PENDING, and INDEX_ONLY.

This recovery queue is evaluated under the same source hierarchy and strict gate. Recovering the primary report can change an earlier provisional/no-action disposition only when the primary text itself supplies new evidence. A secondary summary is not retroactively promoted merely because its wording resembles a canonical action.

## Pass 3 — action-bearing primary review

Any 2024 report discovered in Pass 2 that may contain a corporate financial/managerial action is reviewed using the existing source hierarchy and strict gate:
- publication date 2024-01-01 to 2024-12-31;
- primary human-authored report or sufficiently complete official analyst/CRA text;
- prospective or ongoing action;
- canonical mechanism explicit;
- no material omitted co-action;
- no outcome-only translation;
- latest action-bearing source hierarchy retained (CRA -> EQUITY -> IR).

Earlier/lower-priority documents cannot be chosen merely because they map to candidate9 if a later/higher-priority action-bearing source is noncanonical or materially multi-action.

## Outputs

Do not overwrite HB2024-v1.0. Emit:
- broad_pass2_discovery.csv
- broad_pass3_review.csv
- strict_archival_extension_v2.csv (independent expert cases only)
- issuer_policy_extension_v2.csv (separate source layer)
- search audit / manifest.

Only newly verified independent expert strict cases may extend the archival human-action comparison. New survey cases receive anonymized IC-b states and no answer key.

## Downstream analysis

For every newly verified independent expert strict case, join the already frozen candidate9 / IC-b / B1 / Run1 / Strict ITT outputs and compute the same external-anchor statistics used for strict-9:
- C4/C4R/C6-E exact action agreement,
- C3-E action agreement,
- reference uptake,
- same-substrate Oracle alpha/beta/gamma values and pairwise gaps.

Report strict-9, extension-only, and combined expert anchor separately.

## Survey

Add newly verified strict expert firms to the current matched-information survey after the existing A-O cases. Respondents see only the same 27 IC-b fields and candidate9/B1 action definitions, with human-readable rounding. Company identity, archival expert action, model output, Oracle payoff and later outcomes remain hidden.

Create a fresh form build ID rather than changing a fielded form.
