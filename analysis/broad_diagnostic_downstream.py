#!/usr/bin/env python3
from __future__ import annotations

import argparse,csv,json,math,hashlib
from collections import Counter,defaultdict
from pathlib import Path

ACTIONS=("A0","DL","RF","CX","WC1","WC2","OE","MX1","MX2")
POLICIES=("C4","C4R","C6-E")
ORACLES=("alpha","beta","gamma")
FILES={
 "BASELINE":"frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/BASELINE_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
 "HIGH":"frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/HIGH_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
}

def read_csv(p):
    with Path(p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write_csv(p,rows):
    if not rows:return
    with Path(p).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
def norm(x):return "" if x is None else str(x).strip()
def num(x):
    try:return float(x)
    except:return float("nan")
def finite(x):return isinstance(x,(int,float)) and math.isfinite(x)
def mean(xs):
    a=[x for x in xs if finite(x)]
    return sum(a)/len(a) if a else float("nan")
def fkey(r):
    fk=norm(r.get("firm_key"))
    if fk:return fk
    code=norm(r.get("firm_id") or r.get("stock_code"))
    try:code=str(int(float(code))).zfill(6)
    except:pass
    year=norm(r.get("fiscal_year") or "2024")
    try:year=str(int(float(year)))
    except:pass
    return f"{code}::{year}"
def info(r):return norm(r.get("information_condition") or r.get("info"))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--human",required=True)
    ap.add_argument("--repro",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    h=Path(a.human);repro=Path(a.repro);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    diag=read_csv(h/"analysis_outputs/broad_archival/supplementary_archival_diagnostics_v2.csv")
    if len(diag)!=3:raise RuntimeError(f"expected 3 diagnostics, got {len(diag)}")
    by={r["firm_key"]:r for r in diag}
    target=set(by)
    all_long=[]
    common={}
    manifests={}
    baseline_c3_rows={}
    for regime,rel in FILES.items():
        p=repro/rel
        if not p.exists():raise FileNotFoundError(p)
        manifests[regime]={"path":rel,"sha256":sha(p),"size":p.stat().st_size}
        rowids={}
        llm={}
        with p.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                if norm(r.get("analysis_population")) not in {"","itt"}:continue
                if norm(r.get("source"))!="stage8_llm":continue
                if norm(r.get("mode"))!="candidate9" or norm(r.get("budget"))!="B1" or info(r)!="IC-b":continue
                if norm(r.get("replicate")) not in {"","1","1.0"}:continue
                if norm(r.get("phase")) not in {"","MAIN"}:continue
                pol=norm(r.get("policy"))
                if pol not in POLICIES:continue
                fk=fkey(r)
                if fk not in target:continue
                rid=norm(r.get("row_id"))
                if pol=="C4":rowids[fk]=rid
                model=norm(r.get("model_key") or r.get("model"))
                llm[(model,pol,fk)]=r
        if set(rowids)!=target:raise RuntimeError(f"{regime} row linkage mismatch")
        rev={v:k for k,v in rowids.items()}
        fixed=defaultdict(dict);c3={}
        with p.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                rid=norm(r.get("row_id"))
                if rid not in rev:continue
                fk=rev[rid];src=norm(r.get("source"));pol=norm(r.get("policy"))
                if src=="stage6_fixed_action_surface" and pol in ACTIONS:fixed[fk][pol]=r
                if src=="stage6_current_deployed_release" and pol=="C3-E":c3[fk]=r
        models=sorted({k[0] for k in llm})
        for fk in target:
            if set(fixed[fk])!=set(ACTIONS):raise RuntimeError(f"incomplete fixed surface {regime}/{fk}")
            if fk not in c3:raise RuntimeError(f"missing C3-E {regime}/{fk}")
        if regime=="BASELINE":baseline_c3_rows=c3
        for fk in target:
            d=by[fk];comp=d["canonical_component"]
            if regime=="BASELINE":
                ceiling={}
                for o in ORACLES:
                    vals={act:num(fixed[fk][act].get(f"delta_R_score_{o}")) for act in ACTIONS}
                    best=max(vals.values());bacts=sorted(k for k,v in vals.items() if abs(v-best)<=1e-12)
                    ceiling[o]=(best,bacts)
                common[fk]={
                    "diagnostic_id":d["diagnostic_id"],"firm_key":fk,"stock_code":d["stock_code"],"firm_name":d["firm_name"],
                    "canonical_component":comp,"blocking_reason":d["blocking_reason"],"source_url":d["source_url"],
                    "C3E_action":norm(c3[fk].get("candidate_id")),
                    **{f"component_delta_{o}":num(fixed[fk][comp].get(f"delta_R_score_{o}")) for o in ORACLES},
                    **{f"ceiling_delta_{o}":ceiling[o][0] for o in ORACLES},
                    **{f"ceiling_actions_{o}":";".join(ceiling[o][1]) for o in ORACLES},
                }
        for model in models:
            for pol in POLICIES:
                for fk in target:
                    r=llm[(model,pol,fk)];act=norm(r.get("candidate_id"));d=by[fk]
                    rec={
                        "diagnostic_id":d["diagnostic_id"],"firm_key":fk,"firm_name":d["firm_name"],
                        "regime":regime,"model":model,"policy":pol,"action":act,
                        "canonical_component":d["canonical_component"],
                        "equals_canonical_component":int(act==d["canonical_component"]),
                        "C3E_action":norm(c3[fk].get("candidate_id")),
                        "equals_C3E":int(act==norm(c3[fk].get("candidate_id"))),
                    }
                    for o in ORACLES:rec[f"delta_{o}"]=num(r.get(f"delta_R_score_{o}"))
                    all_long.append(rec)
        manifests[regime]["models"]=models

    for fk,c in common.items():
        rr=baseline_c3_rows[fk]
        rec={"diagnostic_id":c["diagnostic_id"],"firm_key":fk,"firm_name":c["firm_name"],
             "regime":"REFERENCE","model":"Candidate-IQL ensemble","policy":"C3-E","action":c["C3E_action"],
             "canonical_component":c["canonical_component"],
             "equals_canonical_component":int(c["C3E_action"]==c["canonical_component"]),
             "C3E_action":c["C3E_action"],"equals_C3E":1}
        for o in ORACLES:rec[f"delta_{o}"]=num(rr.get(f"delta_R_score_{o}"))
        all_long.append(rec)

    write_csv(out/"broad_diagnostic_model_side_long.csv",all_long)
    case_rows=[]
    for fk,c in sorted(common.items(),key=lambda kv:kv[1]["diagnostic_id"]):
        rec=dict(c)
        for regime in FILES:
            for model in manifests[regime]["models"]:
                short="Gemini" if "gemini" in model.lower() else "GPT"
                for pol in POLICIES:
                    rr=next(x for x in all_long if x["firm_key"]==fk and x["regime"]==regime and x["model"]==model and x["policy"]==pol)
                    rec[f"{regime}_{short}_{pol}_action"]=rr["action"]
                    rec[f"{regime}_{short}_{pol}_delta_alpha"]=rr["delta_alpha"]
        case_rows.append(rec)
    write_csv(out/"broad_diagnostic_case_table.csv",case_rows)

    summary=[]
    for regime in ["REFERENCE","BASELINE","HIGH"]:
        rows=[x for x in all_long if x["regime"]==regime]
        groups=defaultdict(list)
        for x in rows:groups[(x["model"],x["policy"])].append(x)
        for (model,pol),xs in sorted(groups.items()):
            summary.append({
                "regime":regime,"model":model,"policy":pol,"n":len(xs),
                "action_distribution":json.dumps(dict(sorted(Counter(x["action"] for x in xs).items())),ensure_ascii=False),
                "canonical_component_convergence":mean([float(x["equals_canonical_component"]) for x in xs]),
                "c3e_convergence":mean([float(x["equals_C3E"]) for x in xs]),
                "mean_delta_alpha":mean([x["delta_alpha"] for x in xs]),
                "mean_delta_beta":mean([x["delta_beta"] for x in xs]),
                "mean_delta_gamma":mean([x["delta_gamma"] for x in xs]),
            })
    write_csv(out/"broad_diagnostic_summary.csv",summary)

    lines=[
      "# Broad-search diagnostic cases — downstream model-side analysis","",
      "These cases are not additions to the frozen strict-9 independent-expert benchmark. They are retained because the broad Pass-2/Pass-3 audit exposed an OE-like component together with a source-hierarchy or action-space reason that blocks a strict one-action label.","",
      "| Firm | OE-like component | C3-E | Alpha candidate ceiling | Baseline Gemini C4/C4R/C6-E | Baseline GPT | High Gemini | High GPT |",
      "|---|---|---|---|---|---|---|---|"
    ]
    for r in case_rows:
        def trip(reg,m):return "/".join(r[f"{reg}_{m}_{p}_action"] for p in POLICIES)
        lines.append(f"| {r['firm_name']} | {r['canonical_component']} | {r['C3E_action']} | {r['ceiling_actions_alpha']} | {trip('BASELINE','Gemini')} | {trip('BASELINE','GPT')} | {trip('HIGH','Gemini')} | {trip('HIGH','GPT')} |")
    lines += ["","## Interpretation boundary","",
      "- Canonical-component convergence is descriptive, not accuracy, because these firms do not have a valid strict single-action expert label.",
      "- Candidate ceiling is internal to the frozen Simulator–Oracle evaluation substrate and is not real-world ground truth.",
      "- The three cases are useful survey diagnostics for whether matched-information humans also experience action-space ambiguity.",
      ""
    ]
    (out/"BROAD_DIAGNOSTIC_DOWNSTREAM_REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    manifest={"status":"PASS","analysis_id":"BROAD_DIAGNOSTIC_MODEL_SIDE_V1","strict_extension_n":0,"diagnostic_n":3,
              "comparison_contract":{"mode":"candidate9","information_condition":"IC-b","budget":"B1","replicate":1,"analysis_population":"itt","policies":list(POLICIES)},
              "stage9":manifests,"outputs":["broad_diagnostic_model_side_long.csv","broad_diagnostic_case_table.csv","broad_diagnostic_summary.csv","BROAD_DIAGNOSTIC_DOWNSTREAM_REPORT.md"]}
    (out/"BROAD_DIAGNOSTIC_DOWNSTREAM_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","diagnostic_n":3,"long_rows":len(all_long)},ensure_ascii=False))

if __name__=="__main__":main()
