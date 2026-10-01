#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,hashlib
from pathlib import Path
import pandas as pd

PAYLOAD=Path("frozen/original_release/llm/final_plan3/2cf6d6d0e4250e66ce882ab95f9d641f2c73711ffbc6429e9a203dcc2ee680a2/firm_payload_source.parquet")
PROMPT=Path("frozen/evidence/llm/prompt_contract.json")

def read_csv(p):
    with Path(p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--human",required=True);ap.add_argument("--repro",required=True);a=ap.parse_args()
    h=Path(a.human);r=Path(a.repro);out=h/"analysis_outputs/human18";out.mkdir(parents=True,exist_ok=True)
    old=read_csv(h/"analysis_outputs/human15/RESEARCHER_ONLY_case_key.csv")
    if len(old)!=15 or [x["case_alias"] for x in old]!=list("ABCDEFGHIJKLMNO"):
        raise RuntimeError("Human-15 base is not frozen A-O")
    diag=read_csv(h/"analysis_outputs/broad_archival/supplementary_archival_diagnostics_v2.csv")
    if len(diag)!=3:raise RuntimeError("Expected 3 broad diagnostics")
    diag=sorted(diag,key=lambda x:x["diagnostic_id"])
    ext=[]
    for alias,row in zip("PQR",diag):
        ext.append({
            "case_alias":alias,"firm_key":row["firm_key"],"panel":"BROAD_DIAGNOSTIC_3",
            "selection_stratum":"ARCHIVAL_ACTION_SPACE_DIAGNOSTIC",
            "firm_name":row["firm_name"],"stock_code":row["stock_code"],
        })
    rows=[{k:x.get(k,"") for k in ("case_alias","firm_key","panel","selection_stratum","firm_name","stock_code")} for x in old]+ext
    if len(rows)!=18 or len({x["firm_key"] for x in rows})!=18:raise RuntimeError("Human-18 key invalid")
    with (out/"RESEARCHER_ONLY_case_key.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

    contract=json.loads((r/PROMPT).read_text(encoding="utf-8"))
    fields=[x["field"] for x in contract["information_conditions"]["IC-b"]["visible_dictionary"]]
    states=pd.read_parquet(r/PAYLOAD,columns=["firm_key"]+fields)
    states["firm_key"]=states["firm_key"].astype(str)
    key=pd.DataFrame(rows)[["case_alias","firm_key"]]
    selected=key.merge(states,on="firm_key",how="left",validate="one_to_one").sort_values("case_alias")
    if selected.shape!=(18,29):raise RuntimeError(f"Unexpected selected shape {selected.shape}")
    if selected[fields].isna().all(axis=1).any():raise RuntimeError("Missing diagnostic IC-b state")
    selected[["case_alias"]+fields].to_csv(out/"case_states_ICb.csv",index=False,encoding="utf-8-sig")
    (out/"ACTION_CATALOG_EXACT.json").write_text(json.dumps(contract["action_contract"]["catalog"],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    audit={
      "build_id":"H18-v3-20261001","n_cases":18,
      "panels":{"ARCHIVAL_ANCHOR_9":9,"ADDITIONAL_STATE_6":6,"BROAD_DIAGNOSTIC_3":3},
      "base_h15_key_sha256":sha(h/"analysis_outputs/human15/RESEARCHER_ONLY_case_key.csv"),
      "broad_diagnostic_source_sha256":sha(h/"analysis_outputs/broad_archival/supplementary_archival_diagnostics_v2.csv"),
      "payload_sha256":sha(r/PAYLOAD),"prompt_contract_sha256":sha(r/PROMPT),
      "policy_or_oracle_used_for_case_selection":False,
      "respondent_identity_fields":False,
      "note":"P-R are survey diagnostics, not additions to the strict-9 expert benchmark."
    }
    (out/"SELECTION_AUDIT.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"H18_SELECTION_PASS","n":18,"new_aliases":["P","Q","R"]},ensure_ascii=False))
if __name__=="__main__":main()
