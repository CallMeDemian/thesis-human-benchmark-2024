#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ORACLES = ("alpha","beta","gamma")
POLICIES = ("C4","C6-E")
REGIME_FILES = {
    "BASELINE": "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/BASELINE_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
    "HIGH": "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/HIGH_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(v):
    return "" if v is None else str(v).strip()


def fnum(v):
    try:
        return float(v)
    except Exception:
        return float("nan")


def firm_key(row):
    fk = norm(row.get("firm_key"))
    if fk:
        return fk
    year = norm(row.get("fiscal_year") or "2024")
    try:
        year = str(int(float(year)))
    except Exception:
        pass
    code = norm(row.get("stock_code") or row.get("firm_id") or "")
    try:
        code = str(int(float(code))).zfill(6)
    except Exception:
        code = "".join(ch for ch in code if ch.isdigit())[-6:].zfill(6)
    return f"{code}::{year}" if code else ""


def get_info(r):
    return norm(r.get("information_condition") or r.get("info"))


def mean(xs):
    vals=[x for x in xs if math.isfinite(x)]
    return sum(vals)/len(vals) if vals else float("nan")


def median(xs):
    vals=sorted(x for x in xs if math.isfinite(x))
    if not vals:
        return float("nan")
    n=len(vals)
    return vals[n//2] if n%2 else (vals[n//2-1]+vals[n//2])/2


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--human",type=Path,required=True)
    ap.add_argument("--repro",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)

    human_rows=read_csv(args.human/"outputs/strict_archival_benchmark.csv")
    if len(human_rows)!=9:
        raise RuntimeError(f"Expected strict n=9, got {len(human_rows)}")
    human={norm(r["firm_key"]):r for r in human_rows}

    case_rows=[]
    common_by_regime={}
    for regime,rel in REGIME_FILES.items():
        p=args.repro/rel
        if not p.exists():
            raise FileNotFoundError(p)

        # First pass: strict firm row_id mapping from canonical candidate9 C4 rows.
        key_to_rowid={}
        with p.open("r",encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                if norm(r.get("analysis_population")) not in {"","itt"}:
                    continue
                if norm(r.get("source"))!="stage8_llm":
                    continue
                if norm(r.get("policy"))!="C4" or norm(r.get("mode"))!="candidate9":
                    continue
                if norm(r.get("budget"))!="B1" or get_info(r)!="IC-b":
                    continue
                if norm(r.get("replicate")) not in {"","1","1.0"}:
                    continue
                fk=firm_key(r)
                if fk in human:
                    key_to_rowid[fk]=norm(r.get("row_id"))
        if len(key_to_rowid)!=9:
            raise RuntimeError(f"{regime}: strict row-id linkage failed: {len(key_to_rowid)}/9")
        rowid_to_key={v:k for k,v in key_to_rowid.items()}

        # Second pass: capture fixed human action, C3-E, C4, C6-E.
        fixed={}
        c3={}
        llm={}
        with p.open("r",encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                if norm(r.get("analysis_population")) not in {"","itt"}:
                    continue
                rid=norm(r.get("row_id"))
                if rid not in rowid_to_key:
                    continue
                fk=rowid_to_key[rid]
                source=norm(r.get("source"))
                policy=norm(r.get("policy"))
                if source=="stage6_fixed_action_surface" and policy==norm(human[fk]["mapped_action"]):
                    fixed[fk]=r
                elif source=="stage6_current_deployed_release" and policy=="C3-E":
                    c3[fk]=r
                elif source=="stage8_llm" and policy in POLICIES:
                    if norm(r.get("mode"))!="candidate9" or norm(r.get("budget"))!="B1" or get_info(r)!="IC-b":
                        continue
                    if norm(r.get("replicate")) not in {"","1","1.0"}:
                        continue
                    model=norm(r.get("model_key") or r.get("model"))
                    llm[(model,policy,fk)]=r

        if len(fixed)!=9 or len(c3)!=9:
            raise RuntimeError(f"{regime}: missing human fixed ({len(fixed)}) or C3-E ({len(c3)}) rows")

        models=sorted({k[0] for k in llm})
        for model in models:
            for pol in POLICIES:
                n=sum((model,pol,fk) in llm for fk in human)
                if n!=9:
                    raise RuntimeError(f"{regime}/{model}/{pol}: got {n}/9 LLM rows")

        # Assert common human and C3-E scores are invariant across regimes.
        common={}
        for fk in human:
            common[fk]={
                "human_action":norm(human[fk]["mapped_action"]),
                "c3e_action":norm(c3[fk].get("candidate_id")),
                **{f"human_R_{o}":fnum(fixed[fk].get(f"R_score_{o}")) for o in ORACLES},
                **{f"human_delta_{o}":fnum(fixed[fk].get(f"delta_R_score_{o}")) for o in ORACLES},
                **{f"c3e_R_{o}":fnum(c3[fk].get(f"R_score_{o}")) for o in ORACLES},
                **{f"c3e_delta_{o}":fnum(c3[fk].get(f"delta_R_score_{o}")) for o in ORACLES},
            }
        common_by_regime[regime]=common

        for model in models:
            for fk,h in human.items():
                row={
                    "regime":regime,
                    "model":model,
                    "firm_key":fk,
                    "firm_name":norm(h.get("firm_name")),
                    "human_action":norm(h.get("mapped_action")),
                    "c4_action":norm(llm[(model,"C4",fk)].get("candidate_id")),
                    "c6e_action":norm(llm[(model,"C6-E",fk)].get("candidate_id")),
                    "c3e_action":norm(c3[fk].get("candidate_id")),
                }
                for o in ORACLES:
                    row[f"human_R_{o}"]=fnum(fixed[fk].get(f"R_score_{o}"))
                    row[f"c4_R_{o}"]=fnum(llm[(model,"C4",fk)].get(f"R_score_{o}"))
                    row[f"c6e_R_{o}"]=fnum(llm[(model,"C6-E",fk)].get(f"R_score_{o}"))
                    row[f"c3e_R_{o}"]=fnum(c3[fk].get(f"R_score_{o}"))
                    row[f"human_delta_{o}"]=fnum(fixed[fk].get(f"delta_R_score_{o}"))
                    row[f"c4_delta_{o}"]=fnum(llm[(model,"C4",fk)].get(f"delta_R_score_{o}"))
                    row[f"c6e_delta_{o}"]=fnum(llm[(model,"C6-E",fk)].get(f"delta_R_score_{o}"))
                    row[f"c3e_delta_{o}"]=fnum(c3[fk].get(f"delta_R_score_{o}"))
                case_rows.append(row)

    # Common reference scores must agree across baseline/high.
    for fk in human:
        a=common_by_regime["BASELINE"][fk]
        b=common_by_regime["HIGH"][fk]
        for k in a:
            if k.endswith(("_action",)):
                if a[k]!=b[k]:
                    raise RuntimeError(f"Common action drift for {fk}/{k}")
            elif isinstance(a[k],float):
                if not (math.isfinite(a[k]) and math.isfinite(b[k]) and abs(a[k]-b[k])<1e-10):
                    raise RuntimeError(f"Common score drift for {fk}/{k}: {a[k]} vs {b[k]}")

    fields=list(case_rows[0].keys())
    with (args.out/"strict9_oracle_case_level.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(case_rows)

    # Summary: Human/C3-E once, LLM by regime/model.
    summary=[]
    base_common=common_by_regime["BASELINE"]
    for label,prefix in (("Human-mapped","human"),("C3-E","c3e")):
        rec={"regime":"REFERENCE","model":"common","policy":label,"n":9}
        for o in ORACLES:
            rec[f"mean_R_{o}"]=mean([x[f"{prefix}_R_{o}"] for x in base_common.values()])
            rec[f"median_R_{o}"]=median([x[f"{prefix}_R_{o}"] for x in base_common.values()])
            rec[f"mean_delta_{o}"]=mean([x[f"{prefix}_delta_{o}"] for x in base_common.values()])
            rec[f"median_delta_{o}"]=median([x[f"{prefix}_delta_{o}"] for x in base_common.values()])
        summary.append(rec)

    for (regime,model),grp in sorted(groupby:=defaultdict(list).items()):
        pass
    grouped=defaultdict(list)
    for r in case_rows:
        grouped[(r["regime"],r["model"])].append(r)
    for (regime,model),grp in sorted(grouped.items()):
        for policy,prefix in (("C4","c4"),("C6-E","c6e")):
            rec={"regime":regime,"model":model,"policy":policy,"n":len(grp)}
            for o in ORACLES:
                rec[f"mean_R_{o}"]=mean([x[f"{prefix}_R_{o}"] for x in grp])
                rec[f"median_R_{o}"]=median([x[f"{prefix}_R_{o}"] for x in grp])
                rec[f"mean_delta_{o}"]=mean([x[f"{prefix}_delta_{o}"] for x in grp])
                rec[f"median_delta_{o}"]=median([x[f"{prefix}_delta_{o}"] for x in grp])
            summary.append(rec)

    sfields=list(summary[0].keys())
    with (args.out/"strict9_oracle_summary.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=sfields);w.writeheader();w.writerows(summary)

    # Paired gaps against Human-mapped action.
    pairwise=[]
    for (regime,model),grp in sorted(grouped.items()):
        for policy,prefix in (("C4","c4"),("C6-E","c6e"),("C3-E","c3e")):
            for o in ORACLES:
                gaps=[x[f"{prefix}_R_{o}"]-x[f"human_R_{o}"] for x in grp]
                wins=sum(g>1e-12 for g in gaps); losses=sum(g<-1e-12 for g in gaps); ties=len(gaps)-wins-losses
                pairwise.append({
                    "regime":regime,"model":model,"policy":policy,"oracle":o,"n":len(gaps),
                    "mean_gap_vs_human":mean(gaps),"median_gap_vs_human":median(gaps),
                    "wins_vs_human":wins,"ties_vs_human":ties,"losses_vs_human":losses,
                    "mean_delta_score":mean([x[f"{prefix}_delta_{o}"] for x in grp]),
                    "human_mean_delta_score":mean([x[f"human_delta_{o}"] for x in grp]),
                })
    pfields=list(pairwise[0].keys())
    with (args.out/"strict9_oracle_pairwise_vs_human.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=pfields);w.writeheader();w.writerows(pairwise)

    # Compact Markdown.
    ref_h=summary[0]; ref_c3=summary[1]
    md=["# Strict-9 Oracle value comparison","",
        "Human means the frozen human archival action (OE/CX) applied counterfactually to the same FY2024 firm state and scored by the same Simulator–Oracle substrate. It is not the realized effect of the historical human recommendation.",
        "",
        "Primary descriptive metric below is no-op-adjusted Oracle score (Δ vs A0). Because all policies are scored on the same nine firms, absolute-score ordering and Δ-score ordering are equivalent within each Oracle.",
        "",
        "## Common reference policies","",
        "| Policy | ΔAlpha | ΔBeta | ΔGamma |","|---|---:|---:|---:|",
        f"| Human-mapped | {ref_h['mean_delta_alpha']:.4f} | {ref_h['mean_delta_beta']:.4f} | {ref_h['mean_delta_gamma']:.4f} |",
        f"| C3-E | {ref_c3['mean_delta_alpha']:.4f} | {ref_c3['mean_delta_beta']:.4f} | {ref_c3['mean_delta_gamma']:.4f} |",
        "",
        "## LLM C4 / C6-E by generation regime","",
        "| Regime | Model | Policy | ΔAlpha | Gap vs human (Alpha) | W/T/L vs human | ΔBeta | ΔGamma |",
        "|---|---|---|---:|---:|---:|---:|---:|"]
    lookup={(r["regime"],r["model"],r["policy"],r["oracle"]):r for r in pairwise}
    sl={(r["regime"],r["model"],r["policy"]):r for r in summary}
    for regime,model in sorted(grouped):
        for pol in ("C4","C6-E"):
            r=sl[(regime,model,pol)]
            p=lookup[(regime,model,pol,"alpha")]
            md.append(f"| {regime} | {model} | {pol} | {r['mean_delta_alpha']:.4f} | {p['mean_gap_vs_human']:+.4f} | {p['wins_vs_human']}/{p['ties_vs_human']}/{p['losses_vs_human']} | {r['mean_delta_beta']:.4f} | {r['mean_delta_gamma']:.4f} |")
    # C3 pairwise once.
    c3p=lookup[("BASELINE",sorted({r["model"] for r in case_rows if r["regime"]=="BASELINE"})[0],"C3-E","alpha")]
    md += ["","## C3-E versus Human-mapped","",
           f"- Alpha mean gap: **{c3p['mean_gap_vs_human']:+.4f}**; firm-level W/T/L = **{c3p['wins_vs_human']}/{c3p['ties_vs_human']}/{c3p['losses_vs_human']}**.",
           "",
           "## Interpretation boundary","",
           "This is a paired, same-substrate value comparison over only nine strict archival firms. It answers whether the mapped human action, C4, C6-E, or C3-E receives a higher counterfactual Oracle score on these firms. It does not establish that the higher-scoring policy would have produced the better realized credit outcome in the real world.",
           "",
           "Exact-action agreement and Oracle value are distinct outcomes: two policies can choose different actions yet receive similar or higher Oracle value, and a policy can match the human action while not maximize the evaluation substrate.",
           ""]
    (args.out/"STRICT9_ORACLE_VALUE_REPORT.md").write_text("\n".join(md),encoding="utf-8")

    manifest={
        "analysis_id":"HB2024_STRICT9_ORACLE_VALUE_V1",
        "strict_n":9,
        "human_definition":"frozen human archival action mapped to candidate9 and scored counterfactually on the same V4.3 Simulator-Oracle substrate",
        "comparison":["Human-mapped","C4","C6-E","C3-E"],
        "primary_oracle":"alpha",
        "robustness_oracles":["beta","gamma"],
        "primary_metric":"no-op-adjusted delta_R_score",
        "outputs":["strict9_oracle_case_level.csv","strict9_oracle_summary.csv","strict9_oracle_pairwise_vs_human.csv","STRICT9_ORACLE_VALUE_REPORT.md"],
    }
    (args.out/"STRICT9_ORACLE_VALUE_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","case_rows":len(case_rows),"summary_rows":len(summary),"pairwise_rows":len(pairwise)},ensure_ascii=False))


if __name__=="__main__":
    main()
