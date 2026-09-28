# Action Mapping Codebook

This codebook maps explicit report statements to the frozen V4.3 nine-candidate action space.

| Action | Canonical meaning | Positive mapping evidence |
|---|---|---|
| A0 | Maintain / no intervention | Explicit statement that current financial policy should be maintained or no additional financial intervention is warranted |
| DL | Deleveraging / principal repayment | debt reduction, deleveraging, net-debt reduction, repayment, lowering interest-bearing debt |
| RF | Refinancing / maturity extension | refinance short-term debt, term out debt, extend maturities, replace short-term funding with long-term funding while preserving principal |
| CX | Growth CAPEX reduction | reduce, defer, postpone, prioritize or scale back discretionary/growth CAPEX; maintenance CAPEX preserved |
| WC1 | Inventory / receivables working-capital improvement | inventory reduction, inventory-turn improvement, faster receivable collection, reduction of receivable days |
| WC2 | Working-capital improvement using payables / supplier financing | WC1-type actions plus payment-term extension, accounts-payable financing, supplier financing |
| OE | Operating cost efficiency | cost reduction, COGS reduction, SG&A efficiency, structural operating expense reduction |
| MX1 | Deleveraging + cost efficiency | explicit combined program of debt reduction and OE-type cost efficiency |
| MX2 | Deleveraging + working-capital improvement | explicit combined program of debt reduction and WC1/WC2-type working-capital improvement |

## Non-canonical labels

Use these before forcing a canonical action:

- `NO_MAPPABLE_ACTION`: prospective action exists but does not correspond to the frozen action space.
- `MULTI_NONCANONICAL`: multiple explicit actions are present but the combination is not MX1 or MX2.
- `REPORT_NO_ACTION`: no prospective/recommended action appears in an otherwise eligible report.

## Mapping precedence

1. Preserve the original action concepts in `raw_action_tags`.
2. Apply a canonical action only when the report supplies affirmative evidence for that mapping.
3. Do not infer a combined action merely because two risks are discussed; both actions must be stated.
4. Do not convert a forecasted financial outcome into an action. Example: “net debt is expected to decline” is not DL unless the report attributes it to a debt-repayment/deleveraging policy.
5. Do not map investment advice (BUY/SELL) to any corporate action.
6. Do not map generic “improve profitability” to OE unless the mechanism is cost/expense efficiency.
7. Growth or revenue expansion is outside the frozen 8D managerial action space and should normally be `NO_MAPPABLE_ACTION`.

## Confidence

- `HIGH`: the action is explicit and directly matches the canonical definition.
- `MEDIUM`: the action is explicit but requires a small semantic interpretation within the same financial mechanism.
- `LOW`: the mapping is plausible but materially ambiguous; retain for review and exclude from a strict benchmark if necessary.

## Examples

- “차입금 상환을 통한 재무구조 개선” → DL / HIGH
- “단기성 차입을 장기차입으로 전환” → RF / HIGH
- “신규 증설 계획을 축소하고 필수 유지보수 투자만 집행” → CX / HIGH
- “재고 정상화와 매출채권 회수기간 단축” → WC1 / HIGH
- “재고축소 및 지급조건 연장으로 운전자본 부담 완화” → WC2 / HIGH
- “원가절감 및 판관비 효율화” → OE / HIGH
- “차입금 감축과 비용 구조조정을 병행” → MX1 / HIGH
- “차입금 상환과 재고/채권 회수 개선을 병행” → MX2 / HIGH
