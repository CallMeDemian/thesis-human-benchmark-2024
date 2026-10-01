# Broad Pass-2 / Pass-3 final review — 2026-10-01

## Result

The broad extension does **not** enlarge the frozen independent-expert strict-9.

The search was materially broader than the bounded 17-firm re-review:

- 341 unresolved / previously negative firms entered the broad Pass-2 queue.
- 1,023 public report-index requests were executed across IRGO, AlphaSquare, and StockReport.
- A separate all-575 IRGO title scan was also run.
- The all-575 action-term screen surfaced 32 non-strict firms for focused review.
- Primary-text recovery and source-hierarchy checks were then applied to the strongest apparent canonical-action leads.

No newly reviewed firm satisfied all existing strict gates simultaneously. The most common failure modes were: (i) outcome-only language such as “profitability improvement”; (ii) a customer/industry investment being misread as the firm's CX; (iii) an upstream business exit, acquisition, spin-off, or channel expansion producing an OE-like financial effect; (iv) a later action-bearing source that is noncanonical; and (v) primary full text not being recoverable.

This is a substantive negative result. The strict gate is intentionally high-precision and must not be relaxed merely to increase n.

## High-value diagnostic cases retained outside strict-9

### 하나투어 (039130::2024)

A primary Leading Investment & Securities report dated 2024-06-18 contains a clear OE-like mechanism: expansion of online sales, continuing personnel efficiency, and limited fixed-cost growth are linked to profitability improvement. However, a later primary Hyundai Motor Securities report dated 2024-11-22 states a 2025 plan for aggressive marketing and free-travel market-share expansion. That later action-bearing source is a material noncanonical growth/marketing action. Under the frozen firm aggregation rule, the earlier OE-like document cannot be selected simply because it maps to candidate9.

Decision: `SUPPLEMENTARY_DIAGNOSTIC_ONLY`; canonical component = OE; firm-level strict label = none.

Primary sources:
- Leading Investment & Securities, 2024-06-18, “중고가 패키지상품은 잘 팔리고~효율성도 증가하고!”
  https://www.leading.co.kr/board/EquityResearch/detail/3028
- Hyundai Motor Securities, 2024-11-22, “Not only 패키지, But also 자유여행”
  https://www.hmsec.com/documents/research/20241121163905170_ko.pdf

### 비투엔 (307870::2024)

The latest identified 2024 analyst report is SangSangIn Securities, 2024-11-18, “비용 효율화로 체질 개선 기대.” The report index is verified. Available report-derived coverage describes personnel reduction together with a spin-off of a loss-making business. The latter is a material noncanonical co-action, and a complete primary report was not recovered in this extension.

Decision: `SUPPLEMENTARY_DIAGNOSTIC_ONLY`; OE component is visible, but no single strict candidate is assigned.

Sources:
- IRGO report index: https://m.irgo.co.kr/IR-COMP/307870/
- Discovery coverage: https://www.newspim.com/news/view/20241118000093

### 휠라홀딩스 (081660::2024)

A primary Hanwha Investment & Securities report dated 2024-11-06 explicitly links the shutdown of FILA USA wholesale operations to long-run fixed-cost reduction, loss-structure removal, and cash-flow improvement. The stated managerial act, however, is a material business shutdown/restructuring. The frozen strict gate does not translate an upstream business exit into OE solely because fixed costs fall.

Decision: `SUPPLEMENTARY_DIAGNOSTIC_ONLY`; OE financial effect is present, but firm-level strict label = none.

Primary source:
- Hanwha Investment & Securities, 2024-11-06, “FILA USA 구조조정 발표”
  https://www.hanwhawm.com/main/research/main/view.cmd?depth3_id=anls1&seq=63030&templet=default

## Other screened patterns

- 원익머트리얼즈: “원가 절감/수익성 개선” is primarily described through product mix and raw-material cost conditions; no explicit clean ongoing OE intervention was established from the latest eligible 2024 material.
- 유니셈: “보수적 투자” hits referred to customer / industry investment context rather than the firm's own CX action.
- 교촌에프앤비: direct-operation conversion is the stated business mechanism; it is not automatically the frozen OE intervention.
- SAMG엔터: cost control is accompanied by business cleanup and inventory disposal; existing primary review remains multi/noncanonical.
- 효성티앤씨: financing commentary and acquisition/business-transfer actions remain noncanonical.
- 동성화인텍, 에스원, 보령, 빙그레 and many other title-screen hits were forecasts, business conditions, or profitability descriptions rather than a canonical managerial action.

## Survey implication

The three diagnostic cases above are useful for the matched-information human survey because they probe precisely the action-space boundary that the archival audit exposed. They may be appended as anonymized cases after A–O, but their archival labels must not be shown to respondents and they must not be pooled into the strict-9 human-expert accuracy benchmark.

Survey panels therefore become:

- A–I: frozen independent-expert strict anchor (9)
- J–O: financial-state diversity cases (6)
- P–R: broad-search action-space diagnostic cases (3)

Total survey cases: 18.

## Analysis implication

Keep three result layers separate:

1. strict-9 independent expert anchor — authoritative historical external-anchor result;
2. broad-search diagnostic archive — action-space / source-hierarchy failure cases, not a performance baseline;
3. matched-information human survey — once collected, human choices on all 18 cases can be compared with model outputs under IC-b / candidate9 / B1.

No causal-ground-truth interpretation is added.
