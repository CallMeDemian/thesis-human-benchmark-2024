#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from collections import defaultdict
from pathlib import Path

TERMS={
 "OE":["비용","원가","판관비","효율","수익성","마진","구조조정","고정비","인건비","절감"],
 "DL":["차입금","차입","부채","상환","재무구조","레버리지","순차입","순현금"],
 "RF":["차환","리파이낸","만기","장기차입","단기차입"],
 "CX":["투자 축소","투자 감소","투자 연기","투자 지연","보수적 투자","CAPEX","설비투자"],
 "WC":["재고","채권","매출채권","운전자본","회전율","회수","매입채무"],
}
NEGATIVE_TITLE_HINTS=["성장","수주","신제품","증설","확장","시장 확대","고객 확대"]

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--human",required=True);ap.add_argument("--input",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    h=Path(a.human); inp=Path(a.input);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=read_csv(inp)
    master={r["firm_key"]:r for r in read_csv(h/"data/firm_level_benchmark.csv")}
    strict={r["firm_key"] for r in read_csv(h/"outputs/strict_archival_benchmark.csv")}
    reviewed17=set()
    p=h/"analysis_outputs/human15/ARCHIVAL_PASS3_TARGETS.json"
    if p.exists():reviewed17={x["firm_key"] for x in json.loads(p.read_text(encoding="utf-8"))}
    agg=defaultdict(lambda:{"sources":[],"texts":[],"anchors":[]})
    for r in rows:
        fk=r["firm_key"]
        try: sn=json.loads(r.get("snippets_2024") or "[]")
        except: sn=[]
        try: an=json.loads(r.get("anchors_2024") or "[]")
        except: an=[]
        agg[fk]["sources"].append({"source":r["source_index"],"url":r["final_url"],"http":r["http_status"],"has2024":r["has_2024"]})
        agg[fk]["texts"].extend(sn)
        agg[fk]["anchors"].extend(an)
    scored=[]
    for fk,x in agg.items():
        if fk in strict: continue
        combined=" ".join(x["texts"]+[z.get("text","")+" "+z.get("context","") for z in x["anchors"]])
        termhits={}
        score=0
        for action,terms in TERMS.items():
            hits=sorted({t for t in terms if t.lower() in combined.lower()})
            if hits:
                termhits[action]=hits
                score+=len(hits)
        if not termhits:continue
        anchor_candidates=[]
        for z in x["anchors"]:
            ct=z.get("text","")+" "+z.get("context","")
            cats={a:[t for t in ts if t.lower() in ct.lower()] for a,ts in TERMS.items()}
            cats={a:v for a,v in cats.items() if v}
            if cats:
                anchor_candidates.append({"text":z.get("text",""),"href":z.get("href",""),"hits":cats,"context":z.get("context","")[:800]})
        m=master.get(fk,{})
        scored.append({
            "firm_key":fk,"stock_code":m.get("stock_code",""),"firm_name":m.get("firm_name",""),
            "prior_selection_status":m.get("selection_status",""),"reviewed_in_bounded_pass3":fk in reviewed17,
            "keyword_score":score,"action_keyword_hits":json.dumps(termhits,ensure_ascii=False),
            "candidate_links":json.dumps(anchor_candidates[:20],ensure_ascii=False),
            "source_pages":json.dumps(x["sources"],ensure_ascii=False),
        })
    scored.sort(key=lambda r:(r["reviewed_in_bounded_pass3"],-r["keyword_score"],r["stock_code"]))
    if scored:
        with (out/"broad_pass2_keyword_candidates.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(scored[0].keys()));w.writeheader();w.writerows(scored)
    summary={"candidate_firms":len(scored),"top20":[{k:r[k] for k in ("firm_key","firm_name","keyword_score","action_keyword_hits","reviewed_in_bounded_pass3")} for r in scored[:20]]}
    (out/"broad_pass2_keyword_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
