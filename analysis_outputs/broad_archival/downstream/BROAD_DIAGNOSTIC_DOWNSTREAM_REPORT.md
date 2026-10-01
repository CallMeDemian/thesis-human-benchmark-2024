# Broad-search diagnostic cases — downstream model-side analysis

These cases are not additions to the frozen strict-9 independent-expert benchmark. They are retained because the broad Pass-2/Pass-3 audit exposed an OE-like component together with a source-hierarchy or action-space reason that blocks a strict one-action label.

| Firm | OE-like component | C3-E | Alpha candidate ceiling | Baseline Gemini C4/C4R/C6-E | Baseline GPT | High Gemini | High GPT |
|---|---|---|---|---|---|---|---|
| 하나투어 | OE | MX2 | A0;CX;DL;MX1;MX2;OE;RF;WC1;WC2 | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 |
| 비투엔 | OE | OE | CX;OE;WC1 | OE/MX1/OE | MX1/MX1/MX1 | MX1/MX1/MX1 | MX1/MX1/MX1 |
| 휠라홀딩스 | OE | RF | DL | RF/RF/RF | RF/RF/RF | RF/RF/RF | RF/RF/RF |

## Interpretation boundary

- Canonical-component convergence is descriptive, not accuracy, because these firms do not have a valid strict single-action expert label.
- Candidate ceiling is internal to the frozen Simulator–Oracle evaluation substrate and is not real-world ground truth.
- The three cases are useful survey diagnostics for whether matched-information humans also experience action-space ambiguity.
