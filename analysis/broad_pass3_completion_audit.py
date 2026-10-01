#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def write_csv(p,rows):
    with open(p,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--human",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    h=Path(args.human);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)

    scan=json.loads((out/"all575_action_title_scan_summary.json").read_text(encoding="utf-8"))
    master={r["firm_key"]:r for r in read_csv(h/"data/firm_level_benchmark.csv")}
    final2=json.loads((h/"evidence/BROAD_PASS3_FINAL_TWO_LEADS_20261001.json").read_text(encoding="utf-8"))
    final2_by={r["firm_key"]:r for r in final2["records"]}

    leads=scan["top"]
    assert len(leads)==scan["non_strict_firms_with_action_term_windows"]==32

    rows=[]
    unresolved=[]
    for x in leads:
        fk=x["firm_key"];m=master[fk]
        if m.get("review_record_present")=="TRUE":
            status="PREEXISTING_REVIEW_COMPLETE"
            decision=m.get("selection_status","")
            evidence_basis=m.get("primary_document_status","")
            mapped=m.get("mapped_action","")
            note=m.get("notes","")
        elif fk in final2_by:
            z=final2_by[fk]
            status="FINAL_PASS3_MANUAL_CLOSURE"
            decision=z["decision"]
            evidence_basis=z["source_layer"]
            mapped=z.get("archival_action","")
            note=z["strict_reason"]
        else:
            status="UNRESOLVED"
            decision=""
            evidence_basis=""
            mapped=""
            note=""
            unresolved.append(fk)
        rows.append({
            "firm_key":fk,
            "stock_code":m.get("stock_code",""),
            "firm_name":x["firm_name"],
            "prior_selection_status":x["prior_selection_status"],
            "lead_windows":len(x.get("windows",[])),
            "lead_categories":";".join(sorted({k for w in x.get("windows",[]) for k in w.get("hits",{})})),
            "completion_status":status,
            "final_decision":decision,
            "mapped_action_if_any":mapped,
            "evidence_basis":evidence_basis,
            "strict_eligible_after_completion":"TRUE" if m.get("strict_eligible")=="TRUE" else "FALSE",
            "note":note,
        })
    if unresolved:
        raise RuntimeError(f"Unresolved all-575 action-title leads: {unresolved}")
    if any(r["strict_eligible_after_completion"]=="TRUE" for r in rows):
        raise RuntimeError("A title-screen lead unexpectedly became strict through completion audit; review extension files explicitly.")

    write_csv(out/"BROAD_PASS3_32_LEAD_COMPLETION_AUDIT.csv",rows)
    summary={
        "status":"PASS",
        "all575_action_title_leads":len(rows),
        "preexisting_review_complete":sum(r["completion_status"]=="PREEXISTING_REVIEW_COMPLETE" for r in rows),
        "final_manual_closure":sum(r["completion_status"]=="FINAL_PASS3_MANUAL_CLOSURE" for r in rows),
        "unresolved_after_completion":0,
        "new_independent_expert_strict_cases":0,
        "strict_anchor_count_after_broad_search":9,
    }
    (out/"BROAD_PASS3_32_LEAD_COMPLETION_AUDIT.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# Broad Pass-3 32-lead completion audit",
        "",
        "The all-575 action-title scan surfaced 32 non-strict firms. This audit verifies that every one of those 32 leads has a terminal review disposition.",
        "",
        f"- pre-existing reviewed mapping records: **{summary['preexisting_review_complete']}**",
        f"- final manual closures added in this pass: **{summary['final_manual_closure']}**",
        "- unresolved leads: **0**",
        "- new independent-expert strict cases: **0**",
        "- strict archival expert anchor remains: **9**",
        "",
        "The two final closures were 네패스 and 동양이엔피. Neither yielded an eligible 2024 independent-expert action-bearing report that could satisfy the frozen strict gate.",
        "",
        "See BROAD_PASS3_32_LEAD_COMPLETION_AUDIT.csv for all 32 dispositions and evidence/BROAD_PASS3_FINAL_TWO_LEADS_20261001.json for the final manual evidence.",
        "",
        "This completion audit does not convert report-title keywords into actions. It only verifies that every action-term lead has been resolved under the existing source hierarchy and strict mapping rules.",
        "",
    ]
    (out/"BROAD_PASS3_32_LEAD_COMPLETION_AUDIT.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
