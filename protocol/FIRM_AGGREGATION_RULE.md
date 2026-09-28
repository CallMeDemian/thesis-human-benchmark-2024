# Firm-level source hierarchy and aggregation rule

This rule is frozen before completion of the 575-firm search.

## Objective

The archive may contain multiple 2024 documents per firm. Document-level evidence is never discarded, but a deterministic rule is needed for the firm-level benchmark used against C4 and C6-E.

## Strict firm-level benchmark

For each firm:

1. **CRA first.** Use the latest eligible, firm-specific 2024 credit-rating agency opinion/report that contains an explicit prospective managerial action, stated management financial policy, or an action-linked credit condition that can be mapped under the frozen action codebook.
2. **EQUITY second.** If no mappable CRA action exists, use the latest eligible 2024 human-authored sell-side report for which full text or sufficient primary-source text is available and contains an explicit mappable corporate financial action.
3. **IR third.** If neither CRA nor EQUITY yields a mappable action, use the latest eligible 2024 issuer IR / value-up / management-plan document containing an explicit mappable action. IR is labelled separately as a management-plan benchmark and is not described as independent expert judgment.
4. If an eligible document exists but no canonical action can be justified, the firm has no strict canonical archival action. Preserve the reason as `REPORT_NO_ACTION`, `NO_MAPPABLE_ACTION`, or `MULTI_NONCANONICAL`.
5. Never replace a non-mappable higher-priority source with a lower-priority source merely because the lower-priority source happens to map to a high-scoring action. Lower-priority mapped evidence may be retained for supplemental analysis, but the strict selection rule and all overrides must be logged.

## Date ordering

"Latest" means the latest **publication date inside 2024**, not the newest web crawl date.

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
