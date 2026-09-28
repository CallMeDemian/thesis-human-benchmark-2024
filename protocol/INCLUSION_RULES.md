# Inclusion Rules

## 1. Population

The target population is the frozen set of 575 firms used in the FY2024 V4.3 policy evaluation.

The firm identifier is `firm_key = {6-digit stock code}::2024`.

## 2. Eligible publication dates

Inclusive window:

- start: 2024-01-01
- end: 2024-12-31

Use the document's stated publication date. If the date cannot be verified, mark `DATE_UNVERIFIED` and exclude it from the primary benchmark.

## 3. Eligible source classes

### CRA — preferred primary source
Public material from a recognized credit-rating agency that identifies the firm and discusses rating drivers, outlook, leverage, liquidity, debt service, refinancing, investment burden, working capital, cost efficiency, or other credit-relevant financial policy.

### EQUITY — secondary external-expert source
A securities analyst report may be used only when it contains an explicit corporate financial-policy/action statement. Investment opinions such as BUY/HOLD/SELL, target prices, or earnings forecasts alone are not actions.

### IR — separate management-plan source
Issuer IR presentations, earnings materials, or public management plans may be coded when management explicitly states a future financial action. These are not independent expert judgments and must remain a separate benchmark layer.

### OTHER_EXPERT
Other identifiable professional research may be retained for exploratory use, with organization and author/provenance recorded.

## 4. Inclusion at document level

A document is eligible for action coding when all are true:

1. target firm is identifiable;
2. publication date is inside the window;
3. source is attributable;
4. the relevant statement concerns a future or recommended financial/managerial action, or a stated financial-policy plan;
5. the evidence can be summarized without reconstructing the mapping from Oracle/Simulator outcomes.

## 5. Exclusions

Exclude or retain as non-mappable when the document contains only:

- investment recommendation / target price;
- descriptive historical performance;
- earnings forecast without managerial action;
- generic industry discussion not specific to the firm;
- already-realized action with no prospective recommendation or plan;
- ambiguous wording that cannot be assigned to an action axis;
- document date outside the 2024 window.

## 6. No-report and no-action handling

These states are distinct:

- `NO_REPORT_FOUND`: no eligible 2024 report identified after the documented search.
- `REPORT_NO_ACTION`: eligible report found but no explicit action statement.
- `NO_MAPPABLE_ACTION`: action-like statement exists but cannot be mapped to the frozen action contract.
- `A0`: use only when the source explicitly supports maintaining the current financial policy / no additional intervention.

Silence is never coded as A0.

## 7. Multiple reports per firm

Keep every eligible report as a document-level observation. Do not overwrite earlier reports.

Firm-level summaries are derived later using a frozen aggregation rule. Until that rule is fixed, preserve all document-level mappings.

## 8. Evidence capture

Store:

- firm_key
- stock code and firm name
- report date
- source organization
- source type
- title
- author when available
- canonical URL
- short paraphrased evidence summary
- mapped action
- mapping confidence
- mapping rationale
- retrieval date

Do not commit full copyrighted report PDFs unless redistribution rights are clear.

## 9. Independence from model outcomes

Researchers performing the archival mapping should not consult the firm's C4, C6-E, C3-E, Oracle payoff, or candidate ceiling when deciding the report mapping.

Any later comparison with model policies is downstream of the frozen archival mapping.
