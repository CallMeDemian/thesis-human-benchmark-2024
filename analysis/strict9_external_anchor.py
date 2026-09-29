#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ACTIONS = ("A0","DL","RF","CX","WC1","WC2","OE","MX1","MX2")
POLICIES = ("C4","C4R","C6-E")
REGIME_FILES = {
    "BASELINE": "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/BASELINE_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
    "HIGH": "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/HIGH_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(v):
    return "" if v is None else str(v).strip()


def is_truthy(v):
    return norm(v).upper() in {"TRUE","1","YES","Y"}


def norm_year(v):
    s = norm(v)
    try:
        return str(int(float(s)))
    except Exception:
        return s


def norm_code(v):
    s = norm(v)
    if not s:
        return ""
    if "::" in s:
        s = s.split("::", 1)[0]
    try:
        return str(int(float(s))).zfill(6)
    except Exception:
        digits = "".join(ch for ch in s if ch.isdigit())
        return digits[-6:].zfill(6) if digits else s


def human_key(row):
    fk = norm(row.get("firm_key"))
    if fk:
        return fk
    return f"{norm_code(row.get('stock_code'))}::2024"


def stage_firm_key(row):
    fk = norm(row.get("firm_key"))
    if fk:
        return fk
    year = norm_year(row.get("fiscal_year") or row.get("year") or "2024")
    code = norm_code(row.get("stock_code") or row.get("firm_id") or row.get("corp_code"))
    return f"{code}::{year}" if code else ""


def get_info(row):
    return norm(row.get("information_condition") or row.get("info"))


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z*z/n
    center = (p + z*z/(2*n)) / den
    half = z * math.sqrt((p*(1-p)/n) + z*z/(4*n*n)) / den
    return max(0.0, center-half), min(1.0, center+half)


def cohen_kappa(human, pred):
    if not human:
        return float("nan")
    n = len(human)
    po = sum(a == b for a,b in zip(human,pred)) / n
    hc, pc = Counter(human), Counter(pred)
    pe = sum((hc[a]/n)*(pc[a]/n) for a in set(hc)|set(pc))
    if abs(1-pe) < 1e-15:
        return float("nan")
    return (po-pe)/(1-pe)


def macro_recall_observed(human, pred):
    labels = sorted(set(human))
    vals = []
    for lab in labels:
        idx = [i for i,x in enumerate(human) if x == lab]
        vals.append(sum(pred[i] == lab for i in idx)/len(idx))
    return sum(vals)/len(vals) if vals else float("nan")


def exact_mcnemar_p(b, c):
    n = b + c
    if n == 0:
        return 1.0
    m = min(b,c)
    tail = sum(math.comb(n,k) for k in range(m+1)) / (2**n)
    return min(1.0, 2*tail)


def fmt_pct(x):
    return "NA" if not math.isfinite(x) else f"{100*x:.1f}%"


def fmt_num(x, d=3):
    return "NA" if not math.isfinite(x) else f"{x:.{d}f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", type=Path, required=True)
    ap.add_argument("--repro", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    human_path = args.human / "outputs/strict_archival_benchmark.csv"
    human_rows = read_csv(human_path)
    if len(human_rows) != 9:
        raise RuntimeError(f"Expected frozen strict benchmark n=9, got {len(human_rows)}")
    if any(norm(r.get("mapped_action")) not in ACTIONS for r in human_rows):
        raise RuntimeError("Human strict benchmark contains noncanonical action")
    human = {human_key(r): r for r in human_rows}
    if len(human) != 9:
        raise RuntimeError("Human strict firm_key is not unique")

    case_rows = []
    diagnostics = {
        "human_strict_n": len(human_rows),
        "human_action_distribution": dict(Counter(norm(r["mapped_action"]) for r in human_rows)),
        "regimes": {},
    }
    c3e_by_regime = {}

    for regime, rel in REGIME_FILES.items():
        p = args.repro / rel
        if not p.exists():
            raise FileNotFoundError(p)
        diagnostics["regimes"][regime] = {"path": rel, "sha256": sha256(p), "size_bytes": p.stat().st_size}

        strict_rowids = {}
        candidate_rows = []
        c3e_rows = []

        with p.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            diagnostics["regimes"][regime]["columns"] = reader.fieldnames
            for r in reader:
                pop = norm(r.get("analysis_population"))
                if pop and pop != "itt":
                    continue

                fk = stage_firm_key(r)
                if fk in human:
                    rid = norm(r.get("row_id"))
                    if rid:
                        strict_rowids[fk] = rid

                source = norm(r.get("source"))
                policy = norm(r.get("policy"))
                mode = norm(r.get("mode"))
                if source == "stage8_llm" and policy in POLICIES:
                    if mode != "candidate9":
                        continue
                    if norm(r.get("budget")) != "B1":
                        continue
                    if get_info(r) != "IC-b":
                        continue
                    rep = norm(r.get("replicate"))
                    if rep not in {"","1","1.0"}:
                        continue
                    if fk in human:
                        candidate_rows.append(r)
                elif policy == "C3-E" and source != "stage8_llm":
                    c3e_rows.append(r)

        diagnostics["regimes"][regime]["matched_firm_keys"] = sorted(strict_rowids)
        diagnostics["regimes"][regime]["matched_strict_n"] = len(strict_rowids)
        if len(strict_rowids) != 9:
            missing = sorted(set(human) - set(strict_rowids))
            raise RuntimeError(f"{regime}: failed to map all strict firms; missing={missing}")

        # Candidate9 rows: expect each regime x model x policy to contain all 9 firms.
        seen = set()
        for r in candidate_rows:
            fk = stage_firm_key(r)
            pred = norm(r.get("candidate_id"))
            model = norm(r.get("model_key") or r.get("model"))
            policy = norm(r.get("policy"))
            key = (regime, model, policy, fk)
            if key in seen:
                raise RuntimeError(f"Duplicate strict candidate row: {key}")
            seen.add(key)
            h = human[fk]
            human_action = norm(h["mapped_action"])
            case_rows.append({
                "regime": regime,
                "model": model,
                "policy": policy,
                "firm_key": fk,
                "row_id": norm(r.get("row_id")),
                "stock_code": norm(h.get("stock_code")),
                "firm_name": norm(h.get("firm_name")),
                "human_action": human_action,
                "predicted_action": pred,
                "exact_match": int(pred == human_action),
                "reference_candidate_id": norm(r.get("reference_candidate_id")),
                "reference_match_human": int(norm(r.get("reference_candidate_id")) == human_action) if policy == "C6-E" else "",
                "c6e_adopted_reference": int(pred == norm(r.get("reference_candidate_id"))) if policy == "C6-E" else "",
                "statement_type": norm(h.get("statement_type")),
                "source_type": norm(h.get("source_type")),
                "source_org": norm(h.get("source_org")),
            })

        combos = defaultdict(set)
        for x in case_rows:
            if x["regime"] == regime:
                combos[(x["model"],x["policy"])].add(x["firm_key"])
        diagnostics["regimes"][regime]["candidate9_cells"] = {
            f"{m}|{pol}": len(keys) for (m,pol),keys in sorted(combos.items())
        }
        expected_models = sorted({x["model"] for x in case_rows if x["regime"] == regime})
        for m in expected_models:
            for pol in POLICIES:
                n = len(combos.get((m,pol),set()))
                if n != 9:
                    raise RuntimeError(f"{regime}/{m}/{pol}: expected 9 strict rows, got {n}")

        # C3-E reference: join via the strict firms' row_id.
        rid_to_fk = {rid: fk for fk,rid in strict_rowids.items()}
        c3_unique = {}
        for r in c3e_rows:
            rid = norm(r.get("row_id"))
            if rid not in rid_to_fk:
                continue
            action = norm(r.get("candidate_id"))
            c3_unique[rid] = action
        if len(c3_unique) != 9:
            raise RuntimeError(f"{regime}: expected 9 C3-E rows, got {len(c3_unique)}")
        c3e_by_regime[regime] = {rid_to_fk[rid]: act for rid,act in c3_unique.items()}

    # C3-E must be identical across generation regimes.
    base_c3 = c3e_by_regime["BASELINE"]
    high_c3 = c3e_by_regime["HIGH"]
    if base_c3 != high_c3:
        raise RuntimeError("C3-E strict-firm actions differ between BASELINE and HIGH stage9 artifacts")

    # Add a single C3-E reference row per firm.
    for fk, pred in base_c3.items():
        h = human[fk]
        case_rows.append({
            "regime": "REFERENCE",
            "model": "Candidate-IQL ensemble",
            "policy": "C3-E",
            "firm_key": fk,
            "row_id": "",
            "stock_code": norm(h.get("stock_code")),
            "firm_name": norm(h.get("firm_name")),
            "human_action": norm(h["mapped_action"]),
            "predicted_action": pred,
            "exact_match": int(pred == norm(h["mapped_action"])),
            "reference_candidate_id": "",
            "reference_match_human": "",
            "c6e_adopted_reference": "",
            "statement_type": norm(h.get("statement_type")),
            "source_type": norm(h.get("source_type")),
            "source_org": norm(h.get("source_org")),
        })

    case_fields = [
        "regime","model","policy","firm_key","row_id","stock_code","firm_name",
        "human_action","predicted_action","exact_match","reference_candidate_id",
        "reference_match_human","c6e_adopted_reference","statement_type","source_type","source_org"
    ]
    with (out/"strict9_case_level.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=case_fields); w.writeheader(); w.writerows(case_rows)

    # Summary.
    grouped = defaultdict(list)
    for r in case_rows:
        grouped[(r["regime"],r["model"],r["policy"])].append(r)
    summary_rows=[]
    for (regime,model,policy), rows in sorted(grouped.items()):
        human_actions=[r["human_action"] for r in rows]
        preds=[r["predicted_action"] for r in rows]
        k=sum(int(r["exact_match"]) for r in rows); n=len(rows)
        lo,hi=wilson(k,n)
        summary_rows.append({
            "regime":regime,"model":model,"policy":policy,"n":n,
            "exact_matches":k,"exact_match_rate":k/n if n else float("nan"),
            "wilson95_low":lo,"wilson95_high":hi,
            "cohen_kappa":cohen_kappa(human_actions,preds),
            "macro_recall_observed_labels":macro_recall_observed(human_actions,preds),
            "predicted_action_distribution":json.dumps(dict(sorted(Counter(preds).items())),ensure_ascii=False),
        })
    summary_fields=list(summary_rows[0].keys())
    with (out/"strict9_summary.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=summary_fields);w.writeheader();w.writerows(summary_rows)

    # Within-regime transitions in human agreement.
    index={(r["regime"],r["model"],r["policy"],r["firm_key"]):r for r in case_rows if r["regime"] in REGIME_FILES}
    trans_rows=[]
    for regime in REGIME_FILES:
        models=sorted({r["model"] for r in case_rows if r["regime"]==regime})
        for model in models:
            for new,old in (("C4R","C4"),("C6-E","C4"),("C6-E","C4R")):
                states=[]
                for fk in human:
                    a=index[(regime,model,old,fk)]["exact_match"]
                    b=index[(regime,model,new,fk)]["exact_match"]
                    states.append((a,b))
                cc=sum(a==1 and b==1 for a,b in states)
                cw=sum(a==1 and b==0 for a,b in states)
                wc=sum(a==0 and b==1 for a,b in states)
                ww=sum(a==0 and b==0 for a,b in states)
                trans_rows.append({
                    "regime":regime,"model":model,"comparison":f"{new} vs {old}","n":len(states),
                    "correct_to_correct":cc,"correct_to_wrong":cw,"wrong_to_correct":wc,"wrong_to_wrong":ww,
                    "net_exact_match_change":(wc-cw)/len(states),
                    "mcnemar_exact_p":exact_mcnemar_p(cw,wc),
                })

    # High vs baseline on same model/policy.
    models=sorted({r["model"] for r in case_rows if r["regime"]=="BASELINE"})
    for model in models:
        for pol in POLICIES:
            states=[]
            for fk in human:
                a=index[("BASELINE",model,pol,fk)]["exact_match"]
                b=index[("HIGH",model,pol,fk)]["exact_match"]
                states.append((a,b))
            cc=sum(a==1 and b==1 for a,b in states)
            cw=sum(a==1 and b==0 for a,b in states)
            wc=sum(a==0 and b==1 for a,b in states)
            ww=sum(a==0 and b==0 for a,b in states)
            trans_rows.append({
                "regime":"HIGH_vs_BASELINE","model":model,"comparison":pol,"n":len(states),
                "correct_to_correct":cc,"correct_to_wrong":cw,"wrong_to_correct":wc,"wrong_to_wrong":ww,
                "net_exact_match_change":(wc-cw)/len(states),
                "mcnemar_exact_p":exact_mcnemar_p(cw,wc),
            })
    with (out/"strict9_transitions.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(trans_rows[0].keys()));w.writeheader();w.writerows(trans_rows)

    # C6-E reference behavior.
    ref_rows=[]
    for regime in REGIME_FILES:
        models=sorted({r["model"] for r in case_rows if r["regime"]==regime})
        for model in models:
            rows=[index[(regime,model,"C6-E",fk)] for fk in human]
            adopted=sum(int(r["c6e_adopted_reference"]) for r in rows)
            human_match=sum(int(r["exact_match"]) for r in rows)
            ref_match=sum(int(r["reference_match_human"]) for r in rows)
            ref_correct_c6_correct=sum(int(r["reference_match_human"])==1 and int(r["exact_match"])==1 for r in rows)
            ref_wrong_c6_correct=sum(int(r["reference_match_human"])==0 and int(r["exact_match"])==1 for r in rows)
            ref_rows.append({
                "regime":regime,"model":model,"n":len(rows),
                "c3e_reference_matches_human":ref_match,
                "c6e_matches_human":human_match,
                "c6e_adopts_reference":adopted,
                "c6e_adoption_rate":adopted/len(rows),
                "reference_correct_and_c6e_correct":ref_correct_c6_correct,
                "reference_wrong_but_c6e_correct":ref_wrong_c6_correct,
            })
    with (out/"strict9_reference_analysis.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(ref_rows[0].keys()));w.writeheader();w.writerows(ref_rows)

    # Markdown report.
    strict_names=", ".join(r["firm_name"] for r in human_rows)
    md=[]
    md.append("# Strict-9 human benchmark external-anchor analysis")
    md.append("")
    md.append("This analysis links the frozen HB2024-v1.0 strict one-action archival subset to the frozen V4.3 candidate9/B1/IC-b outputs and the C3-E reference policy. The human archive is not modified.")
    md.append("")
    md.append(f"- Strict firms: **9** ({strict_names})")
    md.append(f"- Human action distribution: **OE 7, CX 2**")
    md.append("- LLM comparison surface: candidate9 / IC-b / B1 / Run 1 / Strict ITT")
    md.append("- Conditions: C4, C4R, C6-E; models analyzed separately; BASELINE and HIGH reported separately")
    md.append("- C3-E: Candidate-IQL ensemble reference, evaluated once because its firm actions are invariant to LLM generation regime")
    md.append("")
    md.append("## Exact-action agreement")
    md.append("")
    md.append("| Regime | Model | Policy | Exact | Rate | Wilson 95% CI | Kappa | Macro recall (OE/CX) |")
    md.append("|---|---|---|---:|---:|---:|---:|---:|")
    for r in summary_rows:
        md.append(f"| {r['regime']} | {r['model']} | {r['policy']} | {r['exact_matches']}/{r['n']} | {fmt_pct(float(r['exact_match_rate']))} | [{fmt_pct(float(r['wilson95_low']))}, {fmt_pct(float(r['wilson95_high']))}] | {fmt_num(float(r['cohen_kappa']))} | {fmt_pct(float(r['macro_recall_observed_labels']))} |")
    md.append("")
    md.append("## Revision / generation-regime transitions")
    md.append("")
    md.append("| Regime | Model | Comparison | Wrong→Correct | Correct→Wrong | Net match change | McNemar exact p |")
    md.append("|---|---|---|---:|---:|---:|---:|")
    for r in trans_rows:
        md.append(f"| {r['regime']} | {r['model']} | {r['comparison']} | {r['wrong_to_correct']} | {r['correct_to_wrong']} | {100*float(r['net_exact_match_change']):+.1f}%p | {float(r['mcnemar_exact_p']):.4f} |")
    md.append("")
    md.append("## C6-E reference behavior")
    md.append("")
    md.append("| Regime | Model | C3-E matches human | C6-E matches human | C6-E adopts C3-E | Adoption rate |")
    md.append("|---|---|---:|---:|---:|---:|")
    for r in ref_rows:
        md.append(f"| {r['regime']} | {r['model']} | {r['c3e_reference_matches_human']}/{r['n']} | {r['c6e_matches_human']}/{r['n']} | {r['c6e_adopts_reference']}/{r['n']} | {fmt_pct(float(r['c6e_adoption_rate']))} |")
    md.append("")
    md.append("## Interpretation boundary")
    md.append("")
    md.append("The strict-9 set is a high-precision external anchor, not a representative human sample. With n=9 and a 7/2 OE/CX label mix, estimates are necessarily imprecise and action coverage is narrow. Exact-match rates and transition counts are therefore descriptive. McNemar p-values are included only as small-sample diagnostics, not as evidence for broad population claims.")
    md.append("")
    md.append("The benchmark is also contemporaneous rather than matched-information: 2024 human reports may use information vintages that differ from the FY2024 state supplied to the model. Agreement is therefore evidence of action-direction convergence under different information processes, not a randomized human-vs-LLM accuracy test.")
    md.append("")
    md.append("## Next analysis boundary")
    md.append("")
    md.append("Do not broaden the strict set post hoc. Any later 13-case canonical sensitivity or 113-case action-space coverage analysis should be emitted as a separate layer and must not overwrite HB2024-v1.0.")
    (out/"STRICT9_REPORT.md").write_text("\n".join(md)+"\n",encoding="utf-8")

    manifest={
        "analysis_id":"HB2024_STRICT9_EXTERNAL_ANCHOR_V1",
        "human_benchmark":"HB2024-v1.0",
        "human_input":str(human_path.relative_to(args.human)),
        "human_input_sha256":sha256(human_path),
        "strict_n":9,
        "human_action_distribution":diagnostics["human_action_distribution"],
        "comparison_contract":{
            "analysis_population":"itt",
            "mode":"candidate9",
            "information_condition":"IC-b",
            "budget":"B1",
            "replicate":1,
            "policies":list(POLICIES),
            "generation_regimes":["BASELINE","HIGH"],
            "c3e_reference":"frozen Candidate-IQL ensemble",
        },
        "diagnostics":diagnostics,
        "outputs":[
            "strict9_case_level.csv","strict9_summary.csv","strict9_transitions.csv",
            "strict9_reference_analysis.csv","STRICT9_REPORT.md","STRICT9_MANIFEST.json"
        ],
        "interpretation":"descriptive high-precision external anchor; not representative; no post-hoc broadening",
    }
    (out/"STRICT9_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    print(json.dumps({
        "status":"PASS",
        "strict_n":9,
        "case_rows":len(case_rows),
        "summary_rows":len(summary_rows),
        "output_dir":str(out),
    },ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
