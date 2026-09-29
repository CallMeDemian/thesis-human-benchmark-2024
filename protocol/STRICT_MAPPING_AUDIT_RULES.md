# Strict Mapping Audit Rules

This audit rule was added after the 575-firm first-pass discovery and **before** linking any archival action to C4, C6-E, C3-E, Simulator payoffs, or Oracle outcomes.

## Why this gate is needed

A public report often describes an upstream business action (asset sale, acquisition, plant expansion, vertical integration, restructuring) and then forecasts a downstream financial effect (lower leverage, lower unit cost, higher margin). The frozen V4.3 action space, however, represents a much narrower set of financial-management actions.

A downstream effect must therefore not be treated automatically as if the report had recommended the corresponding frozen action.

## Strict one-action adequacy gate

A canonical mapping may enter the **strict firm-level benchmark** only if all conditions hold:

1. **Prospective or ongoing action**: the source describes a future, ongoing, or explicitly recommended action. A purely realized historical action is not strict-eligible.
2. **Primary human evidence**: a primary report/full report (or sufficiently complete official analyst text) is available. Automated article summaries are discovery evidence only.
3. **Canonical mechanism is explicit**: the text explicitly identifies the financial mechanism represented by the frozen action.
4. **No material omitted co-action**: representing the source by one canonical action does not suppress a material simultaneous action that is orthogonal to, or opposite, another frozen axis.
5. **No outcome-only translation**: a forecasted lower debt ratio, lower cost, or higher margin is not enough when the actual stated managerial action is outside the action space and the canonical financial action itself is not stated.
6. **Source-layer label retained**: CRA, EQUITY, IR, and OTHER_EXPERT remain separate even when all other gates pass.

## Examples

- “추가 선박 투자를 미루는 것이 바람직하다” -> CX can be strict.
- “비용효율화 정책을 2024년에도 지속” -> OE can be strict.
- “공정 자동화를 해외공장에도 적용해 원가를 낮출 계획” -> OE can be strict when automation is the clearly stated cost-efficiency mechanism and no material contrary frozen action must be suppressed.
- “사업부 매각 후 연결부채가 감소할 전망” -> not strict DL unless debt repayment / principal reduction is itself stated; asset sale is an upstream noncanonical action.
- “제련소 인수로 원가경쟁력 개선” -> translated OE may be preserved for supplemental analysis, but acquisition is a material noncanonical investment and is not strict one-action-equivalent.
- “증설로 가동률 상승, 고정비 감소” -> not strict OE because growth-CAPEX expansion is a material simultaneous action and is opposite the CX direction.
- “지난 분기에 원가를 절감했다” -> realized action; not prospective strict benchmark.

## Audit output

Every previously strict-eligible record is re-reviewed under this gate. The audit decision is preserved in `evidence/strict_mapping_audit_v1.csv`.

The derived master table may be updated after this audit, but historical batch files remain immutable evidence of earlier coding decisions.
