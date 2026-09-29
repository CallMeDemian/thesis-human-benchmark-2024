# Firm-level source hierarchy and aggregation rule

This rule is frozen before completion of the 575-firm search.

## Objective

The archive may contain multiple 2024 documents per firm. Document-level evidence is never discarded, but a deterministic rule is needed for the firm-level benchmark used against C4 and C6-E.

## Strict firm-level benchmark

For each firm:

1. **CRA first.** Review the latest eligible, firm-specific 2024 credit-rating agency opinion/report.
   - If that CRA document contains a **material prospective managerial action or stated management financial policy**, it governs the strict firm-level selection even when the action is `NO_MAPPABLE_ACTION` or `MULTI_NONCANONICAL`. Do not descend to a lower source merely to obtain a canonical action.
   - If the CRA document contains only `FORECAST_ONLY`, `STATE_THRESHOLD_ONLY`, or `NO_ACTION_STATEMENT` evidence, CRA has not supplied an action to select; proceed to EQUITY.
2. **EQUITY second.** Apply the same rule to the latest eligible 2024 human-authored sell-side report for which full text or sufficient primary-source text is available.
   - A material prospective noncanonical or multi-action EQUITY policy blocks substitution by IR for the strict one-action benchmark.
   - If the EQUITY evidence is only a forecast, state threshold, or no-action statement, proceed to IR.
3. **IR third.** Use the latest eligible 2024 issuer IR / value-up / management-plan document containing a prospective managerial action. IR is labelled separately as a management-plan benchmark and is not described as independent expert judgment.
4. If the selected highest-priority **action-bearing** document cannot be represented by one frozen canonical action, the firm has no strict canonical archival action. Preserve the reason as `NO_MAPPABLE_ACTION` or `MULTI_NONCANONICAL`. If no action-bearing document exists at any layer, preserve `REPORT_NO_ACTION`.
5. Lower-priority mapped evidence may be retained for supplemental analysis, but it never overrides a higher-priority material action-bearing source. All source-layer descents and overrides must be logged.

## Date ordering

"Latest" means the latest **publication date inside 2024**, not the newest web crawl date.

## Source-hierarchy clarification

The hierarchy is therefore **action-bearing-source priority**, not “canonical-action priority.” A higher-priority report that merely forecasts outcomes does not block lower-layer action evidence, while a higher-priority report that actually states a material managerial action does block cherry-picking a lower-layer canonical action. This distinction is frozen before any C4 / C6-E / C3-E / Oracle payoff linkage.

## Multiple actions in the selected document

- Use MX1 only for an explicit deleveraging + cost-efficiency combination.
- Use MX2 only for an explicit deleveraging + working-capital combination.
- Other multi-action combinations remain `MULTI_NONCANONICAL` in the strict benchmark.
- A single primary action may be used only when the text itself clearly prioritizes it; coder preference is not enough.

## Evidence sufficiency

Strict mapping requires a primary document or sufficiently complete source text to establish the action. Search snippets, automated summaries, and secondary paraphrases are discovery evidence only.

## Information-vintage limitation

The V4.3 LLM evaluates FY2024 firm states, whereas reports published during calendar 2024 may rely on FY2023, quarterly 2024, market, qualitative, and issuer-provided information available at their publication date.

Therefore this archive is a **contemporaneous 2024 archival benchmark**, not a matched-information randomized human-vs-LLM experiment. Any thesis comparison must state this limitation explicitly.

## Mapping freeze

Document selection and action mapping are frozen before loading the firm's C4, C6-E, C3-E, Simulator payoff, Oracle payoff, or candidate ceiling values.
