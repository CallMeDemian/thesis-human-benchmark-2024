# Downstream Linkage Contract — HB2024 v1.0 × V4.3

Frozen before inspecting strict-nine model outcomes.

## Authorities

- Human archival labels: HB2024-v1.0 frozen snapshot `bd6e6ab005ce9d7e810621aa3e29fc7799651824`.
- Human release manifest: `outputs/FREEZE_MANIFEST.json`.
- V4.3 model evidence: frozen release `thesis-v43-reproduction-kit-v1.0.4`.
- Join key: `firm_key`; `row_id` is used only after its one-to-one crosswalk to `firm_key` is verified.

Archival source selection and action mapping are never revised after inspecting model actions or payoffs.

## Analysis population

Primary external-anchor population is the **nine strict archival firms** only.

This is a deliberately high-precision, selected subset. It is not treated as a representative sample of the 575 firms and it is not a matched-information human experiment.

## Primary action-agreement analysis

The human action is the frozen candidate ID in `outputs/strict_archival_benchmark.csv`.

Compare exact candidate-ID agreement against:

1. C3-E reference action.
2. LLM C4 under `candidate9 / IC-b / B1 / MAIN / replicate 1 / Strict ITT`.
3. LLM C6-E under the same candidate9 conditions.

LLM foundation models are analyzed separately.

The **BASELINE generation regime is primary** because it is the main V4.3 campaign. HIGH is a robustness analysis.

Report:
- exact agreement count / 9 and proportion;
- agreement separately for the seven human OE cases and two human CX cases;
- the full 9×policy action table.

Do not use Cohen's kappa, rank models by agreement, or perform population-level hypothesis tests: n=9, severe class imbalance, and purposive strict-subset selection make those summaries easy to overinterpret.

## Primary payoff linkage

Use the V4.3 Stage6 575×9 candidate payoff surface to evaluate the frozen human candidate action on the same FY2024 evaluation state.

For each strict firm and Oracle α / β / γ:

`human_delta = score(human_action) - score(A0)`

For C3-E:

`c3e_delta = score(C3E_action) - score(A0)`

For candidate9 C4 and C6-E, use the frozen Stage8 `delta_R_score_alpha/beta/gamma` values directly.

For each comparator, report on the nine-firm strict subset:
- mean and median delta;
- firm-level human-minus-comparator paired differences;
- win / tie / loss counts, with a numerical tie tolerance of `1e-12`;
- the complete firm-level table.

Do not present these as estimates of general human-vs-LLM superiority. They are descriptive comparisons within a selected contemporaneous archival anchor.

## Secondary diagnostics

Descriptive only:
- whether C6-E candidate ID equals its C3-E reference candidate ID;
- whether C6-E moves toward or away from the frozen human action relative to C4;
- differences between BASELINE and HIGH in exact action agreement and payoffs.

Free8 nearest-candidate projection is **not** part of the primary archival comparison. Any later free8 projection analysis must be separately preregistered because projection itself changes the estimand.

## Information-vintage limitation

Human source documents were published during calendar 2024 and may use FY2023, interim-2024, market, qualitative, or management information available on each publication date. The V4.3 policies are evaluated on the frozen FY2024 policy state. Therefore the linkage is an external archival validity anchor, not a randomized or information-matched contest.

## Freeze rule

If any downstream result is surprising, the archival action labels remain unchanged. Any correction to an archival label would require a separately documented source/protocol error and a new benchmark version, not an outcome-driven edit.
