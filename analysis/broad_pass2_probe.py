#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, re, time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        r=requests.get(url,headers=UA,timeout=12,allow_redirects=True)
        return r.status_code,r.url,r.text
    except Exception as e:
        return 0,url,"ERROR "+repr(e)

def anchor_inventory(html, base_url):
    if html.startswith("ERROR "):
        return []
    soup=BeautifulSoup(html,"html.parser")
    out=[]
    for a in soup.find_all("a", href=True):
        txt=re.sub(r"\s+"," ",a.get_text(" ",strip=True))
        href=a.get("href","")
        parent_txt=re.sub(r"\s+"," ",a.parent.get_text(" ",strip=True)) if a.parent else txt
        context=(txt+" "+parent_txt)[:1200]
        if "2024" not in context:
            continue
        if href.startswith("//"): href="https:"+href
        elif href.startswith("/"):
            from urllib.parse import urljoin
            href=urljoin(base_url,href)
        out.append({"text":txt[:500],"context":context,"href":href})
    # deterministic de-duplication
    seen=set(); ded=[]
    for x in out:
        key=(x["text"],x["href"])
        if key in seen: continue
        seen.add(key); ded.append(x)
    return ded[:100]

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
    tasks=[]
    for r in q:
        for src,tpl in URLS.items():
            tasks.append((r,src,tpl.format(code=r["stock_code"])))
    def one(task):
        r,src,url=task
        status,final,html=fetch(url)
        text=clean_text(html)[:250000] if not html.startswith("ERROR ") else html
        return {
            "firm_key":r["firm_key"],"stock_code":r["stock_code"],"firm_name":r["firm_name"],
            "source_index":src,"http_status":status,"final_url":final,
            "has_2024":("2024" in text),"text_len":len(text),
            "snippets_2024":json.dumps(snippets(text),ensure_ascii=False),
            "anchors_2024":json.dumps(anchor_inventory(html,final),ensure_ascii=False),
        }
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs=[ex.submit(one,t) for t in tasks]
        for j,fut in enumerate(as_completed(futs),1):
            recs.append(fut.result())
            if j%100==0: print(f"done {j}/{len(tasks)}",flush=True)
    recs.sort(key=lambda x:(x["stock_code"],x["source_index"]))
    with (out/"broad_pass2_probe.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(recs[0].keys()));w.writeheader();w.writerows(recs)
    positives=[x for x in recs if x["has_2024"]]
    (out/"broad_pass2_probe_summary.json").write_text(json.dumps({
        "queue_n":len(q),"request_n":len(recs),"positive_2024_source_pages":len(positives),
        "by_source":{s:{"requests":sum(x["source_index"]==s for x in recs),"http200":sum(x["source_index"]==s and x["http_status"]==200 for x in recs),"has2024":sum(x["source_index"]==s and x["has_2024"] for x in recs)} for s in URLS},
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"queue":len(q),"requests":len(recs),"positive":len(positives)},ensure_ascii=False))

if __name__=="__main__": main()
