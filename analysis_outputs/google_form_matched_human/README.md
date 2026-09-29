# Matched-condition human Google Form package

This package is generated from the frozen strict-9 archival subset and the frozen V4.3 FY2024 IC-b LLM payload.

Files:
- COPY_PASTE_FORM_TEXT.md: exact Google Form section/question text.
- CREATE_GOOGLE_FORM.gs: optional Apps Script skeleton that creates the form after you upload the PNG cards to Drive and fill in their file IDs.
- cards/: two metric-guide images, one action-catalog image, and nine anonymized case cards.
- case_states_ICb_full_precision.csv: respondent-visible IC-b values at full stored precision.
- RESEARCHER_ONLY_case_key.csv: confidential alias-to-firm mapping and archival human action. Do not give this file to respondents.
- MANIFEST.json: frozen package metadata.

Design:
- Human condition: IC-b / candidate9 / B1.
- Firm names and stock codes are hidden.
- Market, industry, fiscal year and all 23 financial fields visible under IC-b are retained.
- Values are re-formatted for human readability but no diagnostic interpretation is added.
- Each respondent chooses one candidate action, reports confidence, and gives a short rationale for all nine firms.

Before deployment, confirm the university's human-subject research / IRB or exemption requirements and replace the consent text if an approved template is required.
