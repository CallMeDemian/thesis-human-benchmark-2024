# Search log

## Pilot 000 — first five firms

Date executed: 2026-09-29

The first five firms were used to stress-test the archival protocol before scaling to all 575.

### Findings

- Public web search does not reliably return a single comparable human recommendation report for every listed firm.
- Some hits are issuer IR rather than independent expert analysis.
- Some sell-side hits are only secondary summaries, not the original report.
- AI-generated securities material must be excluded from a human benchmark.
- A document can contain explicit management actions while remaining outside the frozen V4.3 action space. These are retained as `NO_MAPPABLE_ACTION`, not forced into the nine candidates.
- Credit-rating discovery may appear through secondary articles even when the original rating report is not directly indexed. Such items are leads, not yet primary evidence.

### Scaling implication

The 575-firm pass will retain distinct statuses for:

`ELIGIBLE_MAPPED`, `ELIGIBLE_NONMAPPABLE`, `REPORT_NO_ACTION`, `PENDING_FULLTEXT_REVIEW`, `SECONDARY_SUMMARY_ONLY`, `DATE_UNVERIFIED`, `EXCLUDED_AI_GENERATED`, and `NO_REPORT_FOUND`.

This prevents coverage pressure from turning silence, forecasts, or non-financial growth plans into fabricated canonical actions.


## 2026-09-29 continuation

### Repository migration
The benchmark work was moved from the temporary `human-benchmark-2024` branch of `thesis-reproduction-kit-v43` into the dedicated repository `CallMeDemian/thesis-human-benchmark-2024`.

The temporary branch was force-reset to the source repository's main commit so it no longer contains benchmark-specific commits. The connector used for this work does not expose a delete-ref operation, so the branch name itself may remain visible until manually deleted in GitHub.

### Protocol tightening
Before scaling collection, the schema was expanded to separate:
- explicit analyst recommendation,
- stated management policy,
- prospective action path,
- state/KMI threshold only,
- forecast only,
- no action statement.

This prevents CRA monitoring thresholds or analyst forecasts from being falsely presented as human recommendations.

### Reviewed full-text evidence
Two reviewed mapping batches are now stored:
- `reviewed_mappings_batch_001.csv`
- `reviewed_mappings_batch_002.csv`

These include full-text or primary-source review for examples such as CJ ENM, 서희건설, 금호타이어, CJ CGV, LIG넥스원, 현대글로비스, GST, 랩지노믹스, 뉴프렉스, 동국제약, 비엠티, 이수앱지스 and others.

### Discovery progress
The first-pass search queue has been advanced through approximately firm row 300. Discovery is not equivalent to final source exhaustion: firms without a 2024 sell-side hit still require CRA and/or issuer-IR searches before `NO_REPORT_FOUND` can be assigned.

Key methodological observation: a large share of public 2024 analyst reports concern product growth, market expansion, M&A, shareholder return, or capacity expansion. These are useful negative controls because they must remain `NO_MAPPABLE_ACTION` rather than being forced into the frozen 8D action space.

### Important interpretation boundary
KIS credit opinions explicitly describe their publications as credit opinions rather than financial advice. Accordingly, the strict archive should be described as an **archival human/expert financial-action benchmark**, with the `statement_type` field preserved. It should not be described wholesale as a set of human recommendations.
