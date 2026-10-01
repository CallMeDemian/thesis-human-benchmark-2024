"""Build respondent material from the frozen H15 selection, without policy labels."""
from __future__ import annotations
import argparse, hashlib, html, json, math, subprocess, tempfile
from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw
import build_google_form_package as old

ASSET_BASE='https://raw.githubusercontent.com/CallMeDemian/thesis-human-benchmark-2024/refs/heads/analysis/human15-archival-expansion/analysis_outputs/human18/respondent/cards/'
ACTIONS=[
 ('A0','현 상태 유지','별도 개입 없이 현재 사업계획 유지'),
 ('DL','부채 상환','기초 총이자부부채의 약 35% 상환'),
 ('RF','차환','기초 단기차입금의 약 47%를 장기성 차입으로 전환'),
 ('CX','성장 CAPEX 축소','유지보수 투자는 유지하고 성장성 CAPEX 약 63% 축소'),
 ('WC1','운전자본 회수 개선','재고회전율 +0.70회, 매출채권회전율 +0.47회'),
 ('WC2','운전자본·지급조건 개선','재고회전율 +0.47회, 매출채권회전율 +0.31회, 매입채무회전율 −0.82회'),
 ('OE','비용 효율화','매출원가율 −1.34%p, 판매관리비율 −0.86%p'),
 ('MX1','부채상환 + 비용효율화','총이자부부채 약 17% 상환 + 원가율 −0.67%p + 판관비율 −0.43%p'),
 ('MX2','부채상환 + 운전자본 개선','총이자부부채 약 17% 상환 + 재고회전율 +0.28회 + 매출채권회전율 +0.19회 + 매입채무회전율 −0.25회')]
RULES='''각 사례에서는 제공된 2024년 재무정보를 보고 향후 약 1년의 재무건전성 개선에 가장 적절하다고 판단하는 관리행동 하나를 선택해 주세요. 목표는 실제 기업의 이후 행동이나 실적을 맞히는 것이 아니라, 제시된 정보만으로 당시의 판단을 내리는 것입니다.

9개 후보는 모두 연구에서 미리 정한 표준 프로그램입니다. 수치는 읽기 쉽게 반올림해 표시했습니다. 후보 하나를 고르되 강도나 조합은 제시된 형태 그대로 보아 주세요. A0는 별도 개입 없이 현재 사업계획을 이어가는 선택입니다.

총이자부부채는 단기차입금·유동성장기부채·비유동장기차입금·사채의 합계입니다. 부채상환은 회사의 가용 현금과 유동성 범위에서 실행되는 것으로 봅니다. 차환은 총원금을 유지한 채 단기차입 일부를 장기성 차입으로 바꾸는 행동입니다. CAPEX 축소는 유지보수 투자를 남겨두고 성장 목적의 신규투자를 줄이는 행동입니다.

재고회전율은 매출원가/재고, 매출채권회전율은 매출/매출채권, 매입채무회전율은 매출원가/매입채무입니다. 재고·채권 회전율 증가는 더 빠른 회수, 매입채무회전율 감소는 지급기간 연장 방향을 뜻합니다. 비용비율의 변화는 %p 단위입니다.

비-A0 후보는 연구상 같은 표준 강도로 비교하지만, 실제 비용이나 효과가 같다는 뜻은 아닙니다. 회사 상황에 따라 실행 가능한 크기는 달라질 수 있습니다.

기업명은 가려져 있으며 산업코드와 시장 구분은 원래 입력값을 그대로 표시합니다. '정보 없음'은 결측값으로 이해해 주세요. 화면에 제시된 정보만으로 판단해 주세요.'''
INTRO='''본 설문은 기업의 재무정보를 바탕으로 향후 약 1년의 재무건전성 개선을 위해 어떤 관리행동을 우선적으로 권고하는지 알아보기 위한 연구입니다. 응답 결과는 학위논문의 통계분석에 활용하며, 같은 정보를 바탕으로 생성된 모델의 판단과 비교합니다.

기업명이 가려진 18개 사례가 제시됩니다. 각 사례에서 9개 행동 중 하나를 고르고, 선택에 대한 확신 정도와 간단한 이유를 적어 주세요. 판단은 화면에 제시된 자료를 기준으로 해 주세요. 외부 검색이나 생성형 AI의 도움보다 본인의 판단을 기준으로 응답해 주세요.

설문은 익명으로 진행됩니다. 자유응답에는 개인정보나 직장 내부정보 대신 판단 근거만 적어 주세요. 참여는 자발적이며 중간에 그만두셔도 됩니다. 결과는 개인이 드러나지 않는 집계 형태로 제시합니다.'''
ROLES=['은행 기업금융·여신심사','신용평가·신용분석','금융기관 리스크관리','증권사·자산운용사 기업·산업분석','기업 재무·자금·기획','회계·감사·컨설팅','기업가치평가·투자분석','금융·재무 연구·교육','관련 경험 없음','기타']
EXP=['2년 미만','2년 이상 ~ 5년 미만','5년 이상 ~ 10년 미만','10년 이상 ~ 15년 미만','15년 이상']
MORE=['차입금 만기구조 및 금리','투자 및 CAPEX 계획','사업부문별 수익성','경영진의 사업계획','영업현금흐름 전망','산업 전망·경쟁상황','담보·보증·자금조달 가능성','정성적 신용평가 요소','기업명·사업이력','기타']

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,value): Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def label(key, fallback):
    return '기업규모(로그값)' if key=='log_assets' else fallback

def display(value,kind):
    if value is None or pd.isna(value): return '정보 없음'
    if kind=='text': return '정보 없음' if str(value) in {'UNKNOWN','','None','nan'} else str(value)
    if kind=='year': return str(int(value))
    x=float(value)
    if not math.isfinite(x): return '정보 없음'
    if kind in {'pct','pp'}:
        y=x*100; suffix='%' if kind=='pct' else '%p'
        return (f'{y:+.1f}' if kind=='pp' else f'{y:.1f}')+suffix
    return (f'{x:+.2f}' if kind=='ratio_signed' else f'{x:.2f}')+('배' if 'ratio' in kind else '')

class Canvas:
    def __init__(self,w=1100):
        self.w=w; self.y=36; self.parts=[]; self.probe=ImageDraw.Draw(Image.new('RGB',(w,50))); self.max_right=0
    def text(self,text,x,y,size=27,bold=False):
        f=old.font(size,bold); width=self.probe.textlength(text,font=f)
        assert x+width<=self.w-25, (text,x+width,self.w)
        self.max_right=max(self.max_right,x+width)
        self.parts.append(('text',text,x,y,size,bold))
    def wrap(self,text,width,size=27,bold=False):
        f=old.font(size,bold); lines=[]
        for para in str(text).split('\n'):
            cur=''
            for char in para:
                if cur and self.probe.textlength(cur+char,font=f)>width:
                    lines.append(cur); cur=char
                else: cur+=char
            lines.append(cur)
        return lines
    def paragraph(self,text,size=27,gap=12):
        for line in self.wrap(text,self.w-84,size):
            self.text(line,42,self.y,size); self.y+=size+12
        self.y+=gap
    def heading(self,text):
        self.parts.append(('rect',36,self.y,self.w-36,self.y+48))
        self.text(text,48,self.y+7,27,True); self.y+=57
    def row(self,name,value):
        left=self.wrap(name,590,27); right=self.wrap(value,350,27)
        for j,t in enumerate(left): self.text(t,48,self.y+j*36,27)
        for j,t in enumerate(right): self.text(t,690,self.y+j*36,27,True)
        self.y+=max(len(left),len(right))*36+12
    def save(self,path):
        height=self.y+30; img=Image.new('RGB',(self.w,height),'white'); d=ImageDraw.Draw(img)
        for p in self.parts:
            if p[0]=='rect': d.rectangle(p[1:],fill=(238,240,243))
            else:
                _,t,x,y,s,b=p; d.text((x,y),t,font=old.font(s,b),fill=(25,25,25))
                box=d.textbbox((x,y),t,font=old.font(s,b)); assert box[3]<height and box[2]<self.w
        img.save(path,optimize=True)
        with Image.open(path) as check: check.verify()
        return {'width':self.w,'height':height,'max_text_right':round(self.max_right,2),'render_bounds_check':'PASS','sha256':sha(path)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--human',required=True);p.add_argument('--repro',required=True);args=p.parse_args()
    h,r=Path(args.human),Path(args.repro);out=h/'analysis_outputs/human18'; public=out/'respondent';cards=public/'cards';cards.mkdir(parents=True,exist_ok=True)
    data=pd.read_csv(out/'case_states_ICb.csv',dtype={'case_alias':str,'market':str,'industry_class':str})
    cross=pd.read_csv(out/'RESEARCHER_ONLY_case_key.csv',dtype=str)
    contract=json.loads((r/'frozen/evidence/llm/prompt_contract.json').read_text())
    fields=[x['field'] for x in contract['information_conditions']['IC-b']['visible_dictionary']]
    assert data.shape==(18,28) and list(data.case_alias)==list('ABCDEFGHIJKLMNOPQR')
    assert set(data.columns)=={'case_alias',*fields}
    assert [a[0] for a in ACTIONS]==contract['action_contract']['candidate_order']
    assert json.loads((out/'ACTION_CATALOG_EXACT.json').read_text())==contract['action_contract']['catalog']
    docs=[]; renders={}; cases=[]
    for row in data.to_dict('records'):
        alias=row['case_alias']; canvas=Canvas();canvas.text('사례 '+alias+'  |  2024년 재무정보',42,canvas.y,38,True);canvas.y+=64
        canvas.paragraph('제공된 정보만으로 판단해 주십시오. 정보 없음은 0이 아닙니다.',24)
        groups=[]; seen=[]; md=['## 사례 '+alias,'']
        for title,fs in old.FIELD_GROUPS:
            canvas.heading(title); lines=[]; md+=['### '+title,'']
            for key,nm,kind in fs:
                name=label(key,nm);value=display(row[key],kind);seen.append(key);canvas.row(name,value);lines.append(name+': '+value);md.append('- '+name+': '+value)
            groups.append({'title':title,'lines':lines});canvas.y+=5;md.append('')
        assert len(seen)==27 and set(seen)==set(fields)
        canvas.paragraph('비율은 소수 1자리, 배수·로그값은 소수 2자리로 표시합니다.',22)
        path=cards/f'case_{alias}.png';renders[path.name]=canvas.save(path)
        cases.append({'alias':alias,'groups':groups})
        md+=['질문 1. 향후 약 1년의 재무건전성 개선을 위해 우선 권고할 행동 하나를 선택해 주십시오.','유형: 객관식 / 필수','']
        md+=['- '+a+' — '+b+' | '+c for a,b,c in ACTIONS]
        md+=['','질문 2. 선택에 대한 확신 정도: 1(매우 불확실)~5(매우 확신). / 필수','질문 3. 선택 이유를 1~3문장으로 적어 주십시오. / 필수','']
        docs+=md
    cv=Canvas();cv.text('9개 표준 관리행동',42,cv.y,38,True);cv.y+=64
    cv.paragraph('수치는 읽기 쉽게 반올림한 값입니다. 후보 하나만 선택합니다.',24)
    for a,b,c in ACTIONS: cv.heading(a+' — '+b);cv.paragraph(c,27)
    cv.paragraph('부채는 총이자부부채입니다. 회전율 변화는 가산 변화, 비용비율 변화는 %p입니다. 상세 의미는 폼의 공통 안내를 참고하십시오.',24)
    renders['action_catalog.png']=cv.save(cards/'action_catalog.png')
    dictionary=[]
    for group,fs in old.FIELD_GROUPS:
        for key,nm,kind in fs:
            definition=old.KOREAN_DEFS[key]
            if key=='log_assets': definition='원래 입력에 포함된 총자산의 부호 보존 로그 변환값. sign(총자산) × ln(1+|총자산|). 원액으로 역변환하거나 다른 단위로 바꾸지 않았습니다.'
            if key=='derived__long_debt_to_total_debt': definition='(유동성장기부채 + 비유동장기차입금) ÷ 총이자부부채.'
            dictionary.append(label(key,nm)+': '+definition)
    spec={'title':'기업 재무행동 판단 연구','buildId':'H18-v2-20261001','assetBase':ASSET_BASE,'intro':INTRO,'rules':RULES,'actions':[a+' — '+b+' | '+c for a,b,c in ACTIONS],'dictionary':'\n'.join(dictionary),'backgroundRoles':ROLES,'experience':EXP,'additionalInformation':MORE,'cases':cases,'images':[{'file':f'case_{c["alias"]}.png','sha256':renders[f'case_{c["alias"]}.png']['sha256']} for c in cases]}
    raw=json.dumps(spec,ensure_ascii=False,allow_nan=False)
    for name in cross.firm_name:
        assert name not in raw, 'Company identity leaked to respondent specification'
    assert 'mapped_action' not in raw and 'selection_stratum' not in raw
    template=(h/'analysis/h15_form.gs').read_text(encoding='utf-8'); assert template.count('__DATA_JSON__')==1
    template=template.replace('createHuman15Survey','createHuman18Survey').replace('Human-15 Google Forms builder','Human-18 Google Forms builder')
    script=template.replace('__DATA_JSON__',raw)
    (out/'CREATE_GOOGLE_FORM.gs').write_text(script,encoding='utf-8'); (out/'CREATE_GOOGLE_FORM.txt').write_text(script,encoding='utf-8')
    with tempfile.NamedTemporaryFile(mode='w',suffix='.js',encoding='utf-8') as tmp:
        tmp.write(script);tmp.flush();subprocess.run(['node','--check',tmp.name],check=True)
    md=['# Google Form 수동 작성 원고 — H18-v2','',INTRO,'','## 응답자 배경','업무: '+', '.join(ROLES),'경력: '+', '.join(EXP),'익숙함: 1~5','', '## 공통 안내',RULES,'','## 재무지표 정의',*dictionary,'',*docs,'## 마지막 확인','추가로 필요한 정보: '+', '.join(MORE),'기업을 알아본 사례: A~R 중 해당 사례 선택(없으면 빈칸)','외부 검색·데이터·생성형 AI 사용 여부: 아니오/예','선택지에 없는 행동 및 불명확했던 점: 자유응답']
    (public/'COPY_PASTE_FORM_TEXT.md').write_text('\n\n'.join(md),encoding='utf-8')
    preview=['<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>H15 설문 미리보기</title><style>body{font:17px/1.65 sans-serif;max-width:860px;margin:30px auto;padding:0 18px}img{max-width:100%;height:auto}section{margin:42px 0;padding:24px;border:1px solid #ddd;border-radius:12px}label{display:block;margin:8px 0}p{white-space:pre-wrap}textarea{width:96%;min-height:80px}</style><body><h1>기업 재무행동 판단 연구</h1><p>오프라인 검토용. 응답을 수집하거나 전송하지 않습니다.</p><p>'+html.escape(INTRO)+'</p><h2>공통 안내</h2><p>'+html.escape(RULES)+'</p>']
    for c in cases:
        a=c['alias'];preview+=['<section><h2>사례 '+a+'</h2><img src="cards/case_'+a+'.png" alt="사례 '+a+' 재무정보">']
        preview+=['<label><input type="radio" name="action_'+a+'"> '+html.escape(t)+'</label>' for t in spec['actions']]
        preview+=['<p>확신 정도 1~5</p><select><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select><p>선택 이유</p><textarea></textarea></section>']
    preview+=['</body></html>'];(public/'PREVIEW.html').write_text('\n'.join(preview),encoding='utf-8')
    report={'status':'BUILD_AND_STATIC_VALIDATION_PASS','n_cases':18,'preserved_original_aliases':list('ABCDEFGHI'),'state_diversity_aliases':list('JKLMNO'),'broad_diagnostic_aliases':list('PQR'),'fields_per_case':27,'no_company_names_in_respondent_spec':True,'exact_catalog_matches_prompt':True,'script_node_syntax_check':'PASS','google_account_execution':'NOT_RUN','browser_visual_check':'NOT_RUN','image_render_checks':renders,'response_collection':'NOT_STARTED','original_strict_archive_modified':False}
    dump(out/'VALIDATION.json',report);dump(out/'respondent_spec.json',spec)
    (out/'README_KO.md').write_text('''# 18개 사례 Google Form 패키지 — H18-v2

## 가장 빠른 사용 방법
1. CREATE_GOOGLE_FORM.txt를 메모장으로 열어 전체 복사합니다.
2. Google Apps Script 새 프로젝트의 기본 코드를 지우고 붙여넣습니다.
3. createHuman18Survey 함수를 실행하고 권한을 승인합니다.
4. 실행 로그의 Draft edit URL을 엽니다. 설문과 응답 시트가 생성됩니다.
5. 연구 문의처·참여 안내와 기관의 연구 절차를 확인하고, 미리보기로 시험 응답을 한 뒤 게시합니다. 기본 생성 상태는 비공개 초안입니다.

이미지는 자동 삽입되며 해시로 버전을 확인합니다. 이미지 다운로드가 막히면 SETTINGS.useImages를 false로 바꿔 실행하십시오. 같은 27개 필드를 폼 안의 텍스트로 표시합니다. 오류 이전에 폼을 생성하지 않도록 이미지 검사를 먼저 합니다. 동일 설정 재실행은 기존 초안 URL을 반환합니다.

SETTINGS.order를 REVERSE로 바꾸면 순서가 반대인 별도 초안을 만들 수 있습니다. 참여자는 둘 중 한 버전만 응답합니다. 폼 전체의 질문 섞기는 켜지 마십시오. 18개 사례 소요시간은 실제 파일럿으로 확인해야 합니다.

## 구성
- respondent/cards: 사례 A~R 재무카드 18장과 행동 설명카드 1장
- respondent/PREVIEW.html: 오프라인 검토 화면(응답 전송 없음)
- respondent/COPY_PASTE_FORM_TEXT.md: 수동 작성용 실제 재무값과 문항
- CREATE_GOOGLE_FORM.gs / .txt: 동일한 자동 생성 코드
- RESEARCHER_ONLY_case_key.csv: 연구자용 기업 대응표. 응답자에게 보내지 마십시오.
- case_states_ICb.csv / ACTION_CATALOG_EXACT.json: 재현·채점용 원값
- SELECTION_AUDIT.json: 후보풀·층화 기준·선정 해시
- VALIDATION.json: 자동 검증 범위와 미실행 항목

## 해석 범위
기존 strict-9는 그대로입니다. A–I는 strict anchor, J–O는 재무상태 다양성 사례, P–R은 broad Pass-2/Pass-3에서 확인된 action-space diagnostic 사례입니다. P–R도 정답 행동을 지정하지 않으며 strict expert benchmark에 합치지 않습니다. 분석에서는 기존 9개, 재무상태 6개, diagnostic 3개, 전체 18개를 구분해 제시하십시오. 초기 단일 판단 비교의 주 비교조건은 C4이며 C6-E는 외부 참조가 있어 절차까지 동일한 비교가 아닙니다.

수치는 사람이 읽기 좋게 반올림했습니다. 회사명·종목코드·전문가 권고·모델 답·점수·2025년 결과는 응답 화면에 넣지 않았습니다. 산업코드는 원래 IC-b 값 그대로이며 산업명 해설을 새로 붙이지 않았습니다.

기존 9개 설문을 이미 배포했다면 응답을 보존하고 별도 버전으로 운영하십시오. 문항과 반올림 표시가 일부 정돈되어 있으므로 기존 응답과 무조건 합치지 마십시오. Google 계정의 실제 생성·로그아웃 접속·화면 검증은 연구자가 마지막으로 확인해야 합니다.
''',encoding='utf-8')
    print('H15_BUILD_PASS: 18 cases, 27 fields each; images verified; script syntax checked; Google runtime not executed.')

if __name__=='__main__': main()
