"""Deterministic supplementary case selection; never reads policy results/payoffs."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import pandas as pd

PAYLOAD = 'frozen/original_release/llm/final_plan3/2cf6d6d0e4250e66ce882ab95f9d641f2c73711ffbc6429e9a203dcc2ee680a2/firm_payload_source.parquet'
EXPECTED = '10e78a84a1fdcd8af80b4057795214c896a20c4c1a7444a9cd01c7eab4dd3d56'
ACTIONS = {'A0','DL','RF','CX','WC1','WC2','OE','MX1','MX2'}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--human', required=True); p.add_argument('--repro', required=True); args=p.parse_args()
    h,r=Path(args.human),Path(args.repro); out=h/'analysis_outputs/human15'; out.mkdir(parents=True,exist_ok=True)
    assert sha(r/PAYLOAD)==EXPECTED, 'Frozen payload checksum mismatch'
    contract=json.loads((r/'frozen/evidence/llm/prompt_contract.json').read_text(encoding='utf-8'))
    fields=[x['field'] for x in contract['information_conditions']['IC-b']['visible_dictionary']]
    assert len(fields)==27 and 'firm_name' not in fields
    # Immediately discard all columns outside the public IC-b state and join key.
    states=pd.read_parquet(r/PAYLOAD, columns=['firm_key']+fields)
    states['firm_key']=states['firm_key'].astype(str)
    assert len(states)==575 and states.firm_key.nunique()==575
    assert pd.to_numeric(states.fiscal_year).eq(2024).all()
    oldpath=h/'analysis_outputs/google_form_matched_human/RESEARCHER_ONLY_case_key.csv'
    old=pd.read_csv(oldpath,dtype=str).sort_values('case_alias')
    assert list(old.case_alias)==list('ABCDEFGHI') and old.firm_key.nunique()==9
    pool=states.set_index('firm_key').copy()
    names={'debt':'derived__debt_to_assets','current':'derived__current_ratio','short':'derived__short_debt_to_total_debt','capex':'derived__capex_to_revenue','margin':'derived__operating_margin'}
    numeric={k:pd.to_numeric(pool[v],errors='coerce').replace([float('inf'),float('-inf')],float('nan')) for k,v in names.items()}
    numeric['wc']=pd.to_numeric(pool['derived__inventory_to_revenue'],errors='coerce')+pd.to_numeric(pool['derived__receivables_to_revenue'],errors='coerce')
    numeric['wc']=numeric['wc'].replace([float('inf'),float('-inf')],float('nan'))
    q={k:{'q25':float(v.dropna().quantile(.25,interpolation='linear')),'q75':float(v.dropna().quantile(.75,interpolation='linear')),'nonmissing':int(v.notna().sum())} for k,v in numeric.items()}
    specs=[
        ('LEVERAGE',numeric['debt']>=q['debt']['q75']),
        ('LIQUIDITY',numeric['current']<=q['current']['q25']),
        ('SHORT_DEBT',numeric['short']>=q['short']['q75']),
        ('WORKING_CAPITAL',numeric['wc']>=q['wc']['q75']),
        ('CAPEX',numeric['capex']>=q['capex']['q75']),
        ('STRONG_BALANCE_SHEET',(numeric['debt']<=q['debt']['q25'])&(numeric['current']>=q['current']['q75'])&(numeric['margin']>0))]
    used=set(old.firm_key); audit=[]; chosen=[]
    for alias,(stratum,mask) in zip('JKLMNO',specs):
        candidates=sorted(k for k in pool.index[mask.fillna(False)] if k not in used)
        assert candidates, f'Empty pool: {stratum}'
        scored=[(hashlib.sha256(f'H15-v1|20261001|{stratum}|{k}'.encode()).hexdigest(),k) for k in candidates]
        scored.sort(); digest,key=scored[0]; used.add(key)
        audit.append({'case_alias':alias,'stratum':stratum,'pool_size_after_exclusion':len(candidates),'selection_hash':digest,'firm_key':key,'candidate_pool':candidates})
        chosen.append({'case_alias':alias,'firm_key':key,'panel':'ADDITIONAL_STATE_6','selection_stratum':stratum})
    keyrows=[{'case_alias':x.case_alias,'firm_key':x.firm_key,'panel':'ARCHIVAL_ANCHOR_9','selection_stratum':'PRESERVED_ORIGINAL'} for x in old.itertuples()]+chosen
    cross=pd.DataFrame(keyrows)
    assert len(cross)==15 and cross.firm_key.nunique()==15
    # Name and archival metadata are linked AFTER the selection is fully determined.
    master=pd.read_csv(h/'data/firm_level_benchmark.csv',dtype=str).fillna('')
    cross=cross.merge(master[['firm_key','firm_name','stock_code']],on='firm_key',validate='one_to_one')
    cross.to_csv(out/'RESEARCHER_ONLY_case_key.csv',index=False,encoding='utf-8-sig')
    selected=cross[['case_alias','firm_key']].merge(states,on='firm_key',validate='one_to_one').sort_values('case_alias')
    selected[['case_alias']+fields].to_csv(out/'case_states_ICb.csv',index=False,encoding='utf-8-sig')
    save_json(out/'SELECTION_AUDIT.json',{'protocol':'protocol/EXPANSION_PROTOCOL_20261001.md','payload_sha256':EXPECTED,'thresholds':q,'selection':audit,'policy_columns_used':[],'outcome_columns_used':[],'original_cases_preserved':True,'population':575,'initial_eligible_pool':566,'n_cases':15,'design':'purposive financial-state coverage; not a representative random sample'})
    summary=[]
    for rec in chosen:
        k=rec['firm_key']; name=cross.loc[cross.firm_key.eq(k),'firm_name'].iloc[0]
        vals={f:None if pd.isna(numeric[f].loc[k]) else float(numeric[f].loc[k]) for f in numeric}
        summary.append(dict(rec,firm_name=name,selection_metrics=vals))
    save_json(out/'ADDITIONAL_SIX_SUMMARY.json',summary)
    targets=master[(master.selection_status=='PRIMARY_UNAVAILABLE_AFTER_PASS2')|((master.mapped_action.isin(ACTIONS))&(master.strict_eligible.str.upper()!='TRUE'))]
    cols=['firm_key','firm_name','source_type','report_date','report_title','url','discovery_url','statement_type','evidence_summary','mapped_action','selection_status','notes']
    save_json(out/'ARCHIVAL_PASS3_TARGETS.json',targets[cols].to_dict('records'))
    save_json(out/'ACTION_CATALOG_EXACT.json',contract['action_contract']['catalog'])
    save_json(out/'FROZEN_INPUT_FINGERPRINTS.json',{'protocol_sha256':sha(h/'protocol/EXPANSION_PROTOCOL_20261001.md'),'original_strict_csv_sha256':sha(h/'outputs/strict_archival_benchmark.csv'),'original_case_key_sha256':sha(oldpath),'payload_sha256':EXPECTED,'prompt_contract_sha256':sha(r/'frozen/evidence/llm/prompt_contract.json')})
    print(json.dumps({'selected':summary,'archive_target_count':len(targets),'status':'SELECTION_PASS'},ensure_ascii=False))

if __name__=='__main__': main()
