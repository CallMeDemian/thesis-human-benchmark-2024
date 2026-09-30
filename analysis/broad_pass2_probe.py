#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, re, time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

URLS={
 "IRGO":"https://m.irgo.co.kr/IR-COMP/{code}",
 "ALPHASQUARE":"https://alphasquare.co.kr/home/stock-issue?code={code}&type=report",
 "STOCKREPORT":"https://stockreport.kr/stocks/{code}",
}
UA={"User-Agent":"Mozilla/5.0 (compatible; HB2024-academic-review/1.0)"}

def read_csv(p):
    with open(p,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))

def clean_text(html):
    soup=BeautifulSoup(html,"html.parser")
    for x in soup(["script","style","noscript"]): x.decompose()
    return re.sub(r"\s+"," ",soup.get_text(" ",strip=True))

def fetch(url):
    try:
        r=requests.get(url,headers=UA,timeout=15,allow_redirects=True)
        return r.status_code,r.url,clean_text(r.text)[:250000]
    except Exception as e:
        return 0,url,"ERROR "+repr(e)

def snippets(txt, needles=("2024","2024-","2024.","2024/")):
    spans=[]
    for n in needles:
        start=0
        while True:
            i=txt.find(n,start)
            if i<0: break
            spans.append(txt[max(0,i-220):min(len(txt),i+550)])
            start=i+len(n)
            if len(spans)>=20: break
        if len(spans)>=20: break
    # dedupe
    out=[]
    for s in spans:
        if s not in out: out.append(s)
    return out[:12]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--human",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--probe",action="store_true")
    args=ap.parse_args()
    h=Path(args.human); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    rows=read_csv(h/"data/firm_level_benchmark.csv")
    statuses={"NO_REVIEWED_MAPPING_RECORD","NO_REPORT_FOUND_AFTER_PASS1","NO_REPORT_FOUND_AFTER_PASS2"}
    q=[r for r in rows if r.get("selection_status") in statuses]
    if args.probe:
        wanted={"042000","063080","253590","129890","214180","104830"}
        q=[r for r in rows if r["stock_code"] in wanted]
    recs=[]
    for j,r in enumerate(q,1):
        code=r["stock_code"]; name=r["firm_name"]
        for src,tpl in URLS.items():
            status,final,text=fetch(tpl.format(code=code))
            recs.append({
                "firm_key":r["firm_key"],"stock_code":code,"firm_name":name,
                "source_index":src,"http_status":status,"final_url":final,
                "has_2024":("2024" in text),"text_len":len(text),
                "snippets_2024":json.dumps(snippets(text),ensure_ascii=False),
            })
        if j%25==0: print(f"done {j}/{len(q)}",flush=True)
        time.sleep(0.03)
    with (out/"broad_pass2_probe.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(recs[0].keys()));w.writeheader();w.writerows(recs)
    positives=[x for x in recs if x["has_2024"]]
    (out/"broad_pass2_probe_summary.json").write_text(json.dumps({
        "queue_n":len(q),"request_n":len(recs),"positive_2024_source_pages":len(positives),
        "by_source":{s:{"requests":sum(x["source_index"]==s for x in recs),"http200":sum(x["source_index"]==s and x["http_status"]==200 for x in recs),"has2024":sum(x["source_index"]==s and x["has_2024"] for x in recs)} for s in URLS},
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"queue":len(q),"requests":len(recs),"positive":len(positives)},ensure_ascii=False))

if __name__=="__main__": main()
