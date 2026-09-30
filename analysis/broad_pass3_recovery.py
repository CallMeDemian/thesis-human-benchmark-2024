#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

PRIMARY_RECOVERY={
 "SECONDARY_SUMMARY_ONLY","PRIMARY_INDEX_AVAILABLE","DISCOVERY_INDEX_ONLY",
 "PENDING_FULLTEXT_REVIEW","PRIMARY_REPORT_IDENTIFIED","PRIMARY_DOCUMENT_IDENTIFIED",
 "PRIMARY_TEXT_REVIEW_PENDING","SECONDARY_SUMMARY_ACTION_CANDIDATE",
 "PRIMARY_LATER_REPORT_PENDING","INDEX_ONLY"
}
CANON={
 "OE":("비용","원가","판관비","효율","절감","구조조정","고정비","인건비","마진"),
 "DL":("차입금","부채","상환","재무구조","레버리지","순차입"),
 "RF":("차환","리파이낸","만기","장기차입","단기차입"),
 "CX":("CAPEX","설비투자","투자 축소","투자 감소","투자 연기","투자 지연","보수적"),
 "WC":("운전자본","재고","매출채권","회전율","회수","매입채무"),
}
UA={"User-Agent":"Mozilla/5.0 (compatible; HB2024-academic-review/1.0)"}
DATE=re.compile(r"2024-\d{2}-\d{2}")

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def text_of(html):
    soup=BeautifulSoup(html,"html.parser")
    for x in soup(["script","style","noscript"]):x.decompose()
    return re.sub(r"\s+"," ",soup.get_text(" ",strip=True))

def fetch(url):
    try:
        r=requests.get(url,headers=UA,timeout=15,allow_redirects=True)
        return r.status_code,r.url,r.text
    except Exception as e:
        return 0,url,"ERROR "+repr(e)

def report_section(html):
    if html.startswith("ERROR "):return ""
    txt=text_of(html)
    i=txt.find("리포트")
    if i<0:return ""
    j=txt.find("공시",i+3)
    return txt[i:(j if j>=0 else min(len(txt),i+30000))]

def windows(tail):
    out=[]
    for m in DATE.finditer(tail):
        out.append(re.sub(r"\s+"," ",tail[max(0,m.start()-360):min(len(tail),m.end()+120)]).strip())
    # exact de-dupe
    return list(dict.fromkeys(out))

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--human",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    h=Path(a.human);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    master=read_csv(h/"data/firm_level_benchmark.csv")
    strict={r["firm_key"] for r in read_csv(h/"outputs/strict_archival_benchmark.csv")}
    queue=[r for r in master if r.get("primary_document_status") in PRIMARY_RECOVERY and r["firm_key"] not in strict]
    tasks=[(r,f"https://m.irgo.co.kr/IR-COMP/{r['stock_code']}") for r in queue]
    rows=[]
    def one(t):
        r,url=t;status,final,html=fetch(url);tail=report_section(html);wins=windows(tail)
        return r,status,final,wins
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs=[ex.submit(one,t) for t in tasks]
        for n,f in enumerate(as_completed(futs),1):
            r,status,final,wins=f.result()
            if not wins:
                rows.append({
                    "firm_key":r["firm_key"],"stock_code":r["stock_code"],"firm_name":r["firm_name"],
                    "prior_primary_status":r.get("primary_document_status",""),"prior_selection_status":r.get("selection_status",""),
                    "http_status":status,"irgo_url":final,"date":"","canonical_keyword_hits":"","report_window":""
                })
            else:
                for w in wins:
                    date=(DATE.search(w).group(0) if DATE.search(w) else "")
                    hits={}
                    for act,terms in CANON.items():
                        hh=sorted({x for x in terms if x.lower() in w.lower()})
                        if hh:hits[act]=hh
                    rows.append({
                        "firm_key":r["firm_key"],"stock_code":r["stock_code"],"firm_name":r["firm_name"],
                        "prior_primary_status":r.get("primary_document_status",""),"prior_selection_status":r.get("selection_status",""),
                        "http_status":status,"irgo_url":final,"date":date,
                        "canonical_keyword_hits":json.dumps(hits,ensure_ascii=False) if hits else "",
                        "report_window":w
                    })
            if n%50==0:print(f"done {n}/{len(tasks)}",flush=True)
    rows.sort(key=lambda x:(x["stock_code"],x["date"],x["report_window"]))
    with (out/"pass3_recovery_windows.csv").open("w",encoding="utf-8-sig",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0].keys()));wr.writeheader();wr.writerows(rows)
    leads=[x for x in rows if x["date"] and x["canonical_keyword_hits"]]
    # One row per firm summary, preserving all 2024 windows for manual/full-text recovery.
    by={}
    for x in leads:
        by.setdefault(x["firm_key"],[]).append(x)
    summary=[]
    for fk,xs in by.items():
        summary.append({
            "firm_key":fk,"stock_code":xs[0]["stock_code"],"firm_name":xs[0]["firm_name"],
            "prior_primary_status":xs[0]["prior_primary_status"],"lead_windows":len(xs),
            "canonical_keyword_hits":json.dumps(sorted({k for x in xs for k in json.loads(x["canonical_keyword_hits"]).keys()}),ensure_ascii=False),
            "windows":json.dumps([{"date":x["date"],"hits":json.loads(x["canonical_keyword_hits"]),"context":x["report_window"]} for x in xs],ensure_ascii=False)
        })
    summary.sort(key=lambda x:(-x["lead_windows"],x["stock_code"]))
    if summary:
        with (out/"pass3_recovery_leads.csv").open("w",encoding="utf-8-sig",newline="") as f:
            wr=csv.DictWriter(f,fieldnames=list(summary[0].keys()));wr.writeheader();wr.writerows(summary)
    (out/"pass3_recovery_summary.json").write_text(json.dumps({
        "queue_n":len(queue),"window_rows":len(rows),"firms_with_canonical_keyword_leads":len(summary),
        "lead_firms":[{"firm_key":x["firm_key"],"firm_name":x["firm_name"],"lead_windows":x["lead_windows"],"canonical_keyword_hits":json.loads(x["canonical_keyword_hits"])} for x in summary]
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"queue":len(queue),"lead_firms":len(summary)},ensure_ascii=False))

if __name__=="__main__":main()
