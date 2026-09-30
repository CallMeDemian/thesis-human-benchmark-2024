#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ACTIONS = ("A0","DL","RF","CX","WC1","WC2","OE","MX1","MX2")
POLICIES = ("C4","C4R","C6-E")
ORACLES = ("alpha","beta","gamma")
REGIME_FILES = {
    "BASELINE": "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/BASELINE_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
    "HIGH": "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage9/HIGH_STRICT_ITT/llm_stage9_llm_rl_comparison.csv",
}

def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def norm(v):
    return "" if v is None else str(v).strip()

def fnum(v):
    try:
        return float(v)
    except Exception:
        return float("nan")

def finite(v):
    return isinstance(v,(int,float)) and math.isfinite(v)

def mean(xs):
    vals=[x for x in xs if finite(x)]
    return sum(vals)/len(vals) if vals else float("nan")

def median(xs):
    vals=sorted(x for x in xs if finite(x))
    if not vals:
        return float("nan")
    n=len(vals)
    return vals[n//2] if n%2 else (vals[n//2-1]+vals[n//2])/2

def sha256(path: Path):
    import hashlib
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def get_info(r):
    return norm(r.get("information_condition") or r.get("info"))

def firm_key(r):
    fk=norm(r.get("firm_key"))
    if fk:
        return fk
    code=norm(r.get("firm_id") or r.get("stock_code") or "")
    if code:
        try:
            code=str(int(float(code))).zfill(6)
        except Exception:
            digits="".join(x for x in code if x.isdigit())
            code=digits[-6:].zfill(6) if digits else code
    year=norm(r.get("fiscal_year") or "2024")
    try:
        year=str(int(float(year)))
    except Exception:
        pass
    return f"{code}::{year}" if code else ""

def panel_keys(case_rows):
    original={r["firm_key"] for r in case_rows if r["panel"]=="ARCHIVAL_ANCHOR_9"}
    extra={r["firm_key"] for r in case_rows if r["panel"]=="ADDITIONAL_STATE_6"}
    return {
        "ARCHIVAL_ANCHOR_9": original,
        "ADDITIONAL_STATE_6": extra,
        "ALL_15": {r["firm_key"] for r in case_rows},
    }

def action_dist(actions):
    return json.dumps(dict(sorted(Counter(actions).items())), ensure_ascii=False)

def fmt(x,d=4):
    return "NA" if not finite(x) else f"{x:.{d}f}"

def pct(x):
    return "NA" if not finite(x) else f"{100*x:.1f}%"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--human",type=Path,required=True)
    ap.add_argument("--repro",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)

    cases=read_csv(args.human/"analysis_outputs/human15/RESEARCHER_ONLY_case_key.csv")
    if len(cases)!=15:
        raise RuntimeError(f"Expected 15 cases, got {len(cases)}")
    aliases=[r["case_alias"] for r in cases]
    if aliases != list("ABCDEFGHIJKLMNO"):
        raise RuntimeError(f"Unexpected alias order: {aliases}")
    by_fk={r["firm_key"]:r for r in cases}
    if len(by_fk)!=15:
        raise RuntimeError("Duplicate human15 firm key")
    panels=panel_keys(cases)
    if len(panels["ARCHIVAL_ANCHOR_9"])!=9 or len(panels["ADDITIONAL_STATE_6"])!=6:
        raise RuntimeError("Panel size mismatch")

    strict=read_csv(args.human/"outputs/strict_archival_benchmark.csv")
    human_action={r["firm_key"]:r["mapped_action"] for r in strict}
    if set(human_action)!=panels["ARCHIVAL_ANCHOR_9"]:
        raise RuntimeError("Frozen strict-9 keys do not equal preserved A-I keys")

    issuer_path=args.human/"analysis_outputs/human15/ISSUER_POLICY_EXTENSION.csv"
    issuer_rows=read_csv(issuer_path) if issuer_path.exists() else []
    issuer_map={norm(r.get("firm_key")):r for r in issuer_rows if norm(r.get("mapped_action")) in ACTIONS}

    diagnostics={"analysis_id":"HUMAN15_DOWNSTREAM_PRE_SURVEY_V1","stage9":{}}
    fixed_by_regime={}
    c3_by_regime={}
    llm_by_regime={}

    for regime,rel in REGIME_FILES.items():
        p=args.repro/rel
        if not p.exists():
            raise FileNotFoundError(p)
        diagnostics["stage9"][regime]={"path":rel,"sha256":sha256(p),"size_bytes":p.stat().st_size}

        key_to_rowid={}
        llm={}
        with p.open("r",encoding="utf-8-sig",newline="") as f:
            rd=csv.DictReader(f)
            diagnostics["stage9"][regime]["columns"]=rd.fieldnames
            for r in rd:
                if norm(r.get("analysis_population")) not in {"","itt"}:
                    continue
                if norm(r.get("source"))!="stage8_llm":
                    continue
                if norm(r.get("mode"))!="candidate9" or norm(r.get("budget"))!="B1" or get_info(r)!="IC-b":
                    continue
                if norm(r.get("replicate")) not in {"","1","1.0"}:
                    continue
                if norm(r.get("phase")) not in {"","MAIN"}:
                    continue
                pol=norm(r.get("policy"))
                if pol not in POLICIES:
                    continue
                fk=firm_key(r)
                if fk not in by_fk:
                    continue
                rid=norm(r.get("row_id"))
                if pol=="C4" and rid:
                    key_to_rowid[fk]=rid
                model=norm(r.get("model_key") or r.get("model"))
                key=(model,pol,fk)
                if key in llm:
                    raise RuntimeError(f"Duplicate LLM row: {regime}/{key}")
                llm[key]=r

        if len(key_to_rowid)!=15:
            raise RuntimeError(f"{regime}: row-id map {len(key_to_rowid)}/15; missing={sorted(set(by_fk)-set(key_to_rowid))}")
        rid_to_fk={v:k for k,v in key_to_rowid.items()}
        models=sorted({k[0] for k in llm})
        if len(models)!=2:
            raise RuntimeError(f"{regime}: expected 2 models, got {models}")
        for model in models:
            for pol in POLICIES:
                if sum((model,pol,fk) in llm for fk in by_fk)!=15:
                    raise RuntimeError(f"{regime}/{model}/{pol}: incomplete 15-case LLM slice")

        fixed=defaultdict(dict)
        c3={}
        with p.open("r",encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                if norm(r.get("analysis_population")) not in {"","itt"}:
                    continue
                rid=norm(r.get("row_id"))
                if rid not in rid_to_fk:
                    continue
                fk=rid_to_fk[rid]
                source=norm(r.get("source"))
                pol=norm(r.get("policy"))
                if source=="stage6_fixed_action_surface" and pol in ACTIONS:
                    fixed[fk][pol]=r
                elif source=="stage6_current_deployed_release" and pol=="C3-E":
                    c3[fk]=r

        for fk in by_fk:
            if set(fixed[fk])!=set(ACTIONS):
                raise RuntimeError(f"{regime}: fixed action surface incomplete for {fk}")
        if len(c3)!=15:
            raise RuntimeError(f"{regime}: C3-E {len(c3)}/15")

        fixed_by_regime[regime]=fixed
        c3_by_regime[regime]=c3
        llm_by_regime[regime]=llm
        diagnostics["stage9"][regime]["models"]=models
        diagnostics["stage9"][regime]["matched_n"]=15

    for fk in by_fk:
        if norm(c3_by_regime["BASELINE"][fk].get("candidate_id")) != norm(c3_by_regime["HIGH"][fk].get("candidate_id")):
            raise RuntimeError(f"C3-E action drift for {fk}")
        for act in ACTIONS:
            for o in ORACLES:
                a=fnum(fixed_by_regime["BASELINE"][fk][act].get(f"delta_R_score_{o}"))
                b=fnum(fixed_by_regime["HIGH"][fk][act].get(f"delta_R_score_{o}"))
                if not (finite(a) and finite(b) and abs(a-b)<1e-10):
                    raise RuntimeError(f"Fixed surface drift: {fk}/{act}/{o}")

    fixed=fixed_by_regime["BASELINE"]
    c3=c3_by_regime["BASELINE"]

    ceiling={}
    ceiling_rows=[]
    for case in cases:
        fk=case["firm_key"]
        rec={"case_alias":case["case_alias"],"panel":case["panel"],"selection_stratum":case["selection_stratum"],
             "firm_key":fk,"stock_code":case["stock_code"],"firm_name":case["firm_name"]}
        ceiling[fk]={}
        for o in ORACLES:
            vals={a:fnum(fixed[fk][a].get(f"delta_R_score_{o}")) for a in ACTIONS}
            best=max(vals.values())
            best_actions=sorted(a for a,v in vals.items() if abs(v-best)<=1e-12)
            rec[f"ceiling_delta_{o}"]=best
            rec[f"ceiling_actions_{o}"]=";".join(best_actions)
            ceiling[fk][o]=(best,best_actions)
        ceiling_rows.append(rec)
    write_csv(args.out/"downstream_candidate_ceiling.csv",ceiling_rows)

    long_rows=[]
    for case in cases:
        fk=case["firm_key"]
        rr=c3[fk]
        act=norm(rr.get("candidate_id"))
        rec={"case_alias":case["case_alias"],"panel":case["panel"],"selection_stratum":case["selection_stratum"],
             "firm_key":fk,"stock_code":case["stock_code"],"firm_name":case["firm_name"],
             "regime":"REFERENCE","model":"Candidate-IQL ensemble","policy":"C3-E","action":act,
             "reference_candidate_id":"","adopts_reference":"","human_archival_action":human_action.get(fk,"")}
        for o in ORACLES:
            d=fnum(rr.get(f"delta_R_score_{o}"))
            best,bacts=ceiling[fk][o]
            rec[f"delta_{o}"]=d
            rec[f"regret_to_candidate_ceiling_{o}"]=best-d
            rec[f"hits_candidate_ceiling_{o}"]=int(act in bacts)
        long_rows.append(rec)

    for regime in REGIME_FILES:
        for model in diagnostics["stage9"][regime]["models"]:
            for pol in POLICIES:
                for case in cases:
                    fk=case["firm_key"]
                    rr=llm_by_regime[regime][(model,pol,fk)]
                    act=norm(rr.get("candidate_id"))
                    ref=norm(rr.get("reference_candidate_id"))
                    rec={"case_alias":case["case_alias"],"panel":case["panel"],"selection_stratum":case["selection_stratum"],
                         "firm_key":fk,"stock_code":case["stock_code"],"firm_name":case["firm_name"],
                         "regime":regime,"model":model,"policy":pol,"action":act,
                         "reference_candidate_id":ref,
                         "adopts_reference":int(act==ref) if pol=="C6-E" and ref else "",
                         "human_archival_action":human_action.get(fk,"")}
                    for o in ORACLES:
                        d=fnum(rr.get(f"delta_R_score_{o}"))
                        best,bacts=ceiling[fk][o]
                        rec[f"delta_{o}"]=d
                        rec[f"regret_to_candidate_ceiling_{o}"]=best-d
                        rec[f"hits_candidate_ceiling_{o}"]=int(act in bacts)
                    long_rows.append(rec)
    write_csv(args.out/"downstream_case_level_long.csv",long_rows)

    summary=[]
    for panel,pkeys in panels.items():
        subset=[r for r in long_rows if r["firm_key"] in pkeys]
        grouped=defaultdict(list)
        for r in subset:
            grouped[(r["regime"],r["model"],r["policy"])].append(r)
        for (regime,model,pol),rows in sorted(grouped.items()):
            rec={"panel":panel,"regime":regime,"model":model,"policy":pol,"n":len(rows),
                 "action_distribution":action_dist([r["action"] for r in rows]),
                 "non_A0_rate":sum(r["action"]!="A0" for r in rows)/len(rows)}
            for o in ORACLES:
                rec[f"mean_delta_{o}"]=mean([r[f"delta_{o}"] for r in rows])
                rec[f"median_delta_{o}"]=median([r[f"delta_{o}"] for r in rows])
                rec[f"mean_regret_{o}"]=mean([r[f"regret_to_candidate_ceiling_{o}"] for r in rows])
                rec[f"median_regret_{o}"]=median([r[f"regret_to_candidate_ceiling_{o}"] for r in rows])
                rec[f"ceiling_hit_rate_{o}"]=mean([float(r[f"hits_candidate_ceiling_{o}"]) for r in rows])
            summary.append(rec)
    write_csv(args.out/"downstream_policy_summary.csv",summary)

    idx={(r["regime"],r["model"],r["policy"],r["firm_key"]):r for r in long_rows if r["regime"]!="REFERENCE"}
    transitions=[]
    reference=[]
    for panel,pkeys in panels.items():
        for regime in REGIME_FILES:
            for model in diagnostics["stage9"][regime]["models"]:
                for new,old in (("C4R","C4"),("C6-E","C4"),("C6-E","C4R")):
                    pairs=[(idx[(regime,model,old,fk)],idx[(regime,model,new,fk)]) for fk in pkeys]
                    rec={"panel":panel,"regime":regime,"model":model,"comparison":f"{new}_vs_{old}",
                         "n":len(pairs),"action_changed":sum(a["action"]!=b["action"] for a,b in pairs)}
                    rec["action_change_rate"]=rec["action_changed"]/len(pairs)
                    for o in ORACLES:
                        rec[f"mean_delta_change_{o}"]=mean([b[f"delta_{o}"]-a[f"delta_{o}"] for a,b in pairs])
                    transitions.append(rec)
                c4=[idx[(regime,model,"C4",fk)] for fk in pkeys]
                c4r=[idx[(regime,model,"C4R",fk)] for fk in pkeys]
                c6=[idx[(regime,model,"C6-E",fk)] for fk in pkeys]
                refacts={fk:norm(c3[fk].get("candidate_id")) for fk in pkeys}
                reference.append({
                    "panel":panel,"regime":regime,"model":model,"n":len(pkeys),
                    "c4_matches_c3e":sum(r["action"]==refacts[r["firm_key"]] for r in c4),
                    "c4r_matches_c3e":sum(r["action"]==refacts[r["firm_key"]] for r in c4r),
                    "c6e_matches_c3e":sum(r["action"]==refacts[r["firm_key"]] for r in c6),
                    "c6e_reference_adoption_rate":sum(r["action"]==refacts[r["firm_key"]] for r in c6)/len(c6),
                })
        for model in diagnostics["stage9"]["BASELINE"]["models"]:
            for pol in POLICIES:
                pairs=[(idx[("BASELINE",model,pol,fk)],idx[("HIGH",model,pol,fk)]) for fk in pkeys]
                rec={"panel":panel,"regime":"HIGH_vs_BASELINE","model":model,"comparison":pol,
                     "n":len(pairs),"action_changed":sum(a["action"]!=b["action"] for a,b in pairs)}
                rec["action_change_rate"]=rec["action_changed"]/len(pairs)
                for o in ORACLES:
                    rec[f"mean_delta_change_{o}"]=mean([b[f"delta_{o}"]-a[f"delta_{o}"] for a,b in pairs])
                transitions.append(rec)
    write_csv(args.out/"downstream_policy_transitions.csv",transitions)
    write_csv(args.out/"downstream_reference_behavior.csv",reference)

    wide=[]
    for case in cases:
        fk=case["firm_key"]
        crow=next(x for x in ceiling_rows if x["firm_key"]==fk)
        rec={"case_alias":case["case_alias"],"panel":case["panel"],"selection_stratum":case["selection_stratum"],
             "firm_key":fk,"firm_name":case["firm_name"],"human_archival_action":human_action.get(fk,""),
             "C3E_action":norm(c3[fk].get("candidate_id")),
             "ceiling_alpha_actions":crow["ceiling_actions_alpha"],"ceiling_alpha_delta":crow["ceiling_delta_alpha"]}
        for regime in REGIME_FILES:
            for model in diagnostics["stage9"][regime]["models"]:
                mshort="Gemini" if "gemini" in model.lower() else "GPT"
                for pol in POLICIES:
                    rr=llm_by_regime[regime][(model,pol,fk)]
                    rec[f"{regime}_{mshort}_{pol}_action"]=norm(rr.get("candidate_id"))
                    rec[f"{regime}_{mshort}_{pol}_delta_alpha"]=fnum(rr.get("delta_R_score_alpha"))
        wide.append(rec)
    write_csv(args.out/"downstream_case_table_wide.csv",wide)

    regression={"status":"NOT_RUN","reason":"strict9_summary.csv missing"}
    old_path=args.human/"analysis_outputs/strict9/strict9_summary.csv"
    if old_path.exists():
        old=read_csv(old_path)
        expected={(norm(r["regime"]),norm(r["model"]),norm(r["policy"])):int(float(r["exact_matches"]))
                  for r in old if norm(r["regime"]) in REGIME_FILES}
        observed={}
        for regime in REGIME_FILES:
            for model in diagnostics["stage9"][regime]["models"]:
                for pol in POLICIES:
                    observed[(regime,model,pol)]=sum(
                        norm(llm_by_regime[regime][(model,pol,fk)].get("candidate_id"))==human_action[fk]
                        for fk in panels["ARCHIVAL_ANCHOR_9"]
                    )
        mismatches=[{"cell":"|".join(k),"expected":v,"observed":observed.get(k)}
                    for k,v in expected.items() if observed.get(k)!=v]
        if mismatches:
            raise RuntimeError(f"Strict9 regression mismatch: {mismatches}")
        regression={"status":"PASS","checked_cells":len(expected),"mismatches":[]}
    (args.out/"downstream_strict9_regression_check.json").write_text(
        json.dumps(regression,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )

    issuer_out=[]
    for fk,h in issuer_map.items():
        mapped=norm(h.get("mapped_action"))
        for regime,rel in REGIME_FILES.items():
            p=args.repro/rel
            c4rid=""
            llmrows=[]
            with p.open("r",encoding="utf-8-sig",newline="") as f:
                for rr in csv.DictReader(f):
                    if firm_key(rr)!=fk:
                        continue
                    if norm(rr.get("analysis_population")) not in {"","itt"}:
                        continue
                    if norm(rr.get("source"))=="stage8_llm" and norm(rr.get("mode"))=="candidate9" and norm(rr.get("budget"))=="B1" and get_info(rr)=="IC-b" and norm(rr.get("replicate")) in {"","1","1.0"} and norm(rr.get("phase")) in {"","MAIN"} and norm(rr.get("policy")) in POLICIES:
                        llmrows.append(rr)
                        if norm(rr.get("policy"))=="C4":
                            c4rid=norm(rr.get("row_id"))
            if not c4rid:
                continue
            c3r=None
            fixeds={}
            with p.open("r",encoding="utf-8-sig",newline="") as f:
                for rr in csv.DictReader(f):
                    if norm(rr.get("row_id"))!=c4rid:
                        continue
                    source=norm(rr.get("source"))
                    pol=norm(rr.get("policy"))
                    if source=="stage6_current_deployed_release" and pol=="C3-E":
                        c3r=rr
                    elif source=="stage6_fixed_action_surface" and pol in ACTIONS:
                        fixeds[pol]=rr
            if c3r is None or len(fixeds)!=9:
                continue
            best=max(fnum(fixeds[a].get("delta_R_score_alpha")) for a in ACTIONS)
            bacts=sorted(a for a in ACTIONS if abs(fnum(fixeds[a].get("delta_R_score_alpha"))-best)<=1e-12)
            if regime=="BASELINE":
                issuer_out.append({
                    "firm_key":fk,"firm_name":norm(h.get("firm_name")),"source_type":norm(h.get("source_type")),
                    "regime":"REFERENCE","model":"issuer/C3-E","policy":"issuer-mapped vs C3-E",
                    "issuer_mapped_action":mapped,"issuer_mapped_delta_alpha":fnum(fixeds[mapped].get("delta_R_score_alpha")),
                    "selected_action":norm(c3r.get("candidate_id")),"selected_delta_alpha":fnum(c3r.get("delta_R_score_alpha")),
                    "candidate_ceiling_alpha_actions":";".join(bacts),"candidate_ceiling_alpha_delta":best,
                    "note":"Issuer-policy layer only; not independent expert strict benchmark",
                })
            for rr in llmrows:
                issuer_out.append({
                    "firm_key":fk,"firm_name":norm(h.get("firm_name")),"source_type":norm(h.get("source_type")),
                    "regime":regime,"model":norm(rr.get("model_key")),"policy":norm(rr.get("policy")),
                    "issuer_mapped_action":mapped,"issuer_mapped_delta_alpha":fnum(fixeds[mapped].get("delta_R_score_alpha")),
                    "selected_action":norm(rr.get("candidate_id")),"selected_delta_alpha":fnum(rr.get("delta_R_score_alpha")),
                    "candidate_ceiling_alpha_actions":";".join(bacts),"candidate_ceiling_alpha_delta":best,
                    "note":"Issuer-policy layer only; not independent expert strict benchmark",
                })
    write_csv(args.out/"downstream_issuer_policy_extension.csv",issuer_out)

    md=[
        "# Human-15 확장 패널 — 기존 분석의 downstream 확장",
        "",
        "## 분석 범위",
        "",
        "기존 strict-9 결과는 수정하지 않는다. A-I는 frozen archival expert anchor이고, J-O는 인간 설문을 위해 재무상태만으로 사전 선정한 6개 추가 사례다. 추가 6개에는 아직 human action label이 없으므로 human-vs-LLM exact agreement를 계산하지 않는다.",
        "",
        "이번 확장은 동일한 frozen V4.3 candidate9 / IC-b / B1 / Run1 / Strict ITT 결과에서 C4, C4R, C6-E, C3-E의 행동과 Oracle alpha/beta/gamma 값을 15개 사례에 대해 결합한다. Candidate ceiling은 같은 firm의 9개 frozen candidate 중 평가기반 점수가 가장 높은 값이며 현실의 정답이 아니다.",
        "",
        "## 추가 6개 사례의 model-side 결과",
        "",
        "| Case | 선정층 | C3-E | Alpha ceiling | Baseline Gemini C4/C4R/C6-E | Baseline GPT C4/C4R/C6-E | High Gemini C4/C4R/C6-E | High GPT C4/C4R/C6-E |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in wide:
        if r["panel"]!="ADDITIONAL_STATE_6":
            continue
        def trip(reg,model):
            return "/".join(str(r[f"{reg}_{model}_{p}_action"]) for p in POLICIES)
        md.append(f"| {r['case_alias']} | {r['selection_stratum']} | {r['C3E_action']} | {r['ceiling_alpha_actions']} | {trip('BASELINE','Gemini')} | {trip('BASELINE','GPT')} | {trip('HIGH','Gemini')} | {trip('HIGH','GPT')} |")

    md += [
        "",
        "## Panel별 Oracle alpha 요약",
        "",
        "| Panel | Regime | Model | Policy | n | mean dAlpha | median dAlpha | mean regret to ceiling | ceiling hit rate |",
        "|---|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for panel in ("ARCHIVAL_ANCHOR_9","ADDITIONAL_STATE_6","ALL_15"):
        for r in [x for x in summary if x["panel"]==panel]:
            md.append(f"| {panel} | {r['regime']} | {r['model']} | {r['policy']} | {r['n']} | {fmt(float(r['mean_delta_alpha']))} | {fmt(float(r['median_delta_alpha']))} | {fmt(float(r['mean_regret_alpha']))} | {pct(float(r['ceiling_hit_rate_alpha']))} |")

    md += [
        "",
        "## C6-E reference uptake",
        "",
        "| Panel | Regime | Model | C4=C3-E | C4R=C3-E | C6-E=C3-E | C6-E adoption |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for r in reference:
        md.append(f"| {r['panel']} | {r['regime']} | {r['model']} | {r['c4_matches_c3e']}/{r['n']} | {r['c4r_matches_c3e']}/{r['n']} | {r['c6e_matches_c3e']}/{r['n']} | {pct(float(r['c6e_reference_adoption_rate']))} |")

    md += [
        "",
        "## 해석 경계",
        "",
        "- A-I의 archival human-action agreement와 Human-mapped Oracle value는 기존 strict-9 결과가 권위 있는 결과이며 이 분석에서 다시 정의하지 않았다.",
        "- J-O는 아직 인간 응답이 없으므로 현재 표는 model-side pre-survey baseline이다. 설문 수집 후 human modal action, 선택분포, confidence, rationale 및 LLM agreement를 추가해야 한다.",
        "- 추가 6개는 재무상태 다양성을 위한 목적표본이며 575개 모집단의 대표표본이 아니다.",
        "- Candidate ceiling과 Oracle regret는 평가기반 내부 비교량이다. 실제 기업행동이나 신용등급 변화의 ground truth가 아니다.",
        "- 인터엠 기업 자체 경영정책 확장은 독립 전문가 strict benchmark와 분리한다.",
        "",
    ]
    (args.out/"HUMAN15_DOWNSTREAM_REPORT.md").write_text("\n".join(md),encoding="utf-8")

    manifest={
        "analysis_id":"HUMAN15_DOWNSTREAM_PRE_SURVEY_V1",
        "status":"PASS",
        "n_cases":15,
        "panels":{"ARCHIVAL_ANCHOR_9":9,"ADDITIONAL_STATE_6":6,"ALL_15":15},
        "comparison_contract":{"mode":"candidate9","information_condition":"IC-b","budget":"B1","replicate":1,"analysis_population":"itt","phase":"MAIN","policies":list(POLICIES),"regimes":list(REGIME_FILES)},
        "strict9_regression":regression,
        "human_response_status":"NOT_COLLECTED",
        "outputs":[
            "downstream_candidate_ceiling.csv","downstream_case_level_long.csv","downstream_policy_summary.csv",
            "downstream_policy_transitions.csv","downstream_reference_behavior.csv","downstream_case_table_wide.csv",
            "downstream_strict9_regression_check.json","downstream_issuer_policy_extension.csv","HUMAN15_DOWNSTREAM_REPORT.md"
        ],
        "diagnostics":diagnostics,
    }
    (args.out/"HUMAN15_DOWNSTREAM_MANIFEST.json").write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps({"status":"PASS","case_rows":len(long_rows),"summary_rows":len(summary),"transition_rows":len(transitions),"reference_rows":len(reference),"issuer_rows":len(issuer_out)},ensure_ascii=False))

if __name__=="__main__":
    main()
