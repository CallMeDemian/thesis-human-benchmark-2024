#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path

DATE_RE=re.compile(r"(20\d{2})-(\d{2})-(\d{2})")
BROKER_HINTS=("증권","투자증권","신용평가","Ratings","평가")
CANON_HINTS=("비용","원가","효율","절감","구조조정","차입","상환","차환","재무구조","운전자본","재고","채권","CAPEX","설비투자","투자 축소","투자 연기","투자 지연","마진")

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    rows=read_csv(a.input);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    found=[]
    for r in rows:
        if r.get("source_index")!="IRGO":continue
        tail=r.get("report_tail","")
        if not tail:continue
        # The rendered IRGO report list follows repeated title / org-author / date segments.
        # Split around dates and retain local context; this is discovery evidence only.
        matches=list(DATE_RE.finditer(tail))
        for m in matches:
            if m.group(1)!="2024":continue
            context=tail[max(0,m.start()-260):min(len(tail),m.end()+40)]
            context=re.sub(r"\s+"," ",context).strip()
            # Drop obvious issuer-only events unless there is a broker/rater marker.
            human_expert=any(x in context for x in BROKER_HINTS) and "해당기업 IR팀" not in context[-130:]
            hits=sorted({x for x in CANON_HINTS if x.lower() in context.lower()})
            found.append({
                "firm_key":r["firm_key"],"stock_code":r["stock_code"],"firm_name":r["firm_name"],
                "date":m.group(0),"human_expert_hint":human_expert,
                "canonical_keyword_hits":";".join(hits),
                "context":context,
                "irgo_url":r["final_url"],
            })
    # dedupe overlapping date contexts
    ded=[];seen=set()
    for x in found:
        key=(x["firm_key"],x["date"],x["context"])
        if key in seen:continue
        seen.add(key);ded.append(x)
    ded.sort(key=lambda x:(x["stock_code"],x["date"],x["context"]))
    if ded:
        with (out/"broad_pass2_2024_report_windows.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(ded[0].keys()));w.writeheader();w.writerows(ded)
    leads=[x for x in ded if x["human_expert_hint"] and x["canonical_keyword_hits"]]
    leads.sort(key=lambda x:(-len(x["canonical_keyword_hits"].split(";")),x["stock_code"],x["date"]))
    if leads:
        with (out/"broad_pass3_leads.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(leads[0].keys()));w.writeheader();w.writerows(leads)
    (out/"broad_pass3_leads_summary.json").write_text(json.dumps({
        "2024_windows":len(ded),"human_expert_windows":sum(x["human_expert_hint"] for x in ded),
        "canonical_keyword_leads":len(leads),
        "top30":[{k:x[k] for k in ("firm_key","firm_name","date","canonical_keyword_hits","context")} for x in leads[:30]]
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"windows":len(ded),"leads":len(leads)},ensure_ascii=False))

if __name__=="__main__":main()
