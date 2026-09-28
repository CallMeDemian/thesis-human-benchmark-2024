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
