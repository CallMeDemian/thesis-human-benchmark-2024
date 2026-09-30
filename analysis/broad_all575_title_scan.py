#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests
from bs4 import BeautifulSoup

UA={"User-Agent":"Mozilla/5.0 (compatible; HB2024-academic-review/1.0)"}
DATE=re.compile(r"2024-\d{2}-\d{2}")
TERMS={
 "OE":("비용 효율","비용절감","비용 절감","원가 절감","판관비","구조조정","인력 효율","수익성 개선","효율화"),
 "DL":("차입금 상환","부채 상환","순차입금 감소","차입금 감소","부채 축소","재무구조 개선"),
 "RF":("차환","리파이낸싱","만기 연장","장기차입"),
 "CX":("CAPEX 축소","CAPEX 감소","투자 축소","투자 연기","투자 지연","보수적 투자"),
 "WC":("운전자본 개선","재고 축소","재고 정상화","채권 회수","매출채권 회수","회전율 개선"),
}

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def text_of(html):
    soup=BeautifulSoup(html,"html.parser")
    for x in soup(["script","style","noscript"]):x.decompose()
    return re.sub(r"\s+"," ",soup.get_text(" ",strip=True))

def fetch(code):
    url=f"https://m.irgo.co.kr/IR-COMP/{code}"
    try:
        r=requests.get(url,headers=UA,timeout=15,allow_redirects=True)
        txt=text_of(r.text)
        i=txt.find("리포트")
        if i<0:return r.status_code,r.url,""
        j=txt.find("공시",i+3)
        return r.status_code,r.url,txt[i:(j if j>=0 else min(len(txt),i+40000))]
    except Exception as e:
        return 0,url,""

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--human",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    h=Path(a.human);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    master=read_csv(h/"data/firm_level_benchmark.csv")
    strict={r["firm_key"] for r in read_csv(h/"outputs/strict_archival_benchmark.csv")}
    rows=[]
    def one(r):
        status,url,tail=fetch(r["stock_code"])
        matches=list(DATE.finditer(tail));wins=[]
        for m in matches:
            ctx=tail[max(0,m.start()-360):min(len(tail),m.end()+100)]
            hits={}
            for act,terms in TERMS.items():
                hh=sorted({t for t in terms if t.lower() in ctx.lower()})
                if hh:hits[act]=hh
            if hits:
                wins.append({"date":m.group(0),"hits":hits,"context":ctx})
        return {
            "firm_key":r["firm_key"],"stock_code":r["stock_code"],"firm_name":r["firm_name"],
            "already_strict":r["firm_key"] in strict,
            "prior_selection_status":r.get("selection_status",""),
            "prior_primary_status":r.get("primary_document_status",""),
            "http_status":status,"irgo_url":url,
            "action_title_windows":json.dumps(wins,ensure_ascii=False),
            "n_action_title_windows":len(wins)
        }
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs=[ex.submit(one,r) for r in master]
        for n,f in enumerate(as_completed(futs),1):
            rows.append(f.result())
            if n%100==0:print(f"done {n}/{len(master)}",flush=True)
    rows.sort(key=lambda r:(-r["n_action_title_windows"],r["stock_code"]))
    with (out/"all575_action_title_scan.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
    leads=[r for r in rows if r["n_action_title_windows"] and not r["already_strict"]]
    (out/"all575_action_title_scan_summary.json").write_text(json.dumps({
        "population":len(master),"non_strict_firms_with_action_term_windows":len(leads),
        "top":[{"firm_key":r["firm_key"],"firm_name":r["firm_name"],"prior_selection_status":r["prior_selection_status"],"windows":json.loads(r["action_title_windows"])} for r in leads[:80]]
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"population":len(master),"new_lead_firms":len(leads)},ensure_ascii=False))

if __name__=="__main__":main()
