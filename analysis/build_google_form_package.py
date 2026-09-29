from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from textwrap import wrap

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

PAYLOAD_REL = Path(
    "frozen/original_release/llm/final_plan3/"
    "2cf6d6d0e4250e66ce882ab95f9d641f2c73711ffbc6429e9a203dcc2ee680a2/"
    "firm_payload_source.parquet"
)
PROMPT_REL = Path("frozen/evidence/llm/prompt_contract.json")

SEED = 20260930

FIELD_GROUPS = [
    ("기업·시점", [
        ("fiscal_year", "기준연도", "year"),
        ("market", "시장", "text"),
        ("industry_class", "산업", "text"),
        ("log_assets", "기업규모 지표 log(총자산)", "raw3"),
    ]),
    ("안정성·유동성", [
        ("derived__debt_to_assets", "총부채 / 총자산", "pct"),
        ("derived__equity_to_assets", "자기자본 / 총자산", "pct"),
        ("derived__current_ratio", "유동비율", "ratio"),
        ("derived__cash_ratio", "현금 / 유동부채", "ratio"),
    ]),
    ("수익성·비용구조", [
        ("derived__operating_margin", "영업이익률", "pct"),
        ("derived__gross_margin", "매출총이익률", "pct"),
        ("derived__net_margin", "순이익률", "pct"),
        ("derived__roa_proxy", "ROA 대용치", "pct"),
        ("derived__cogs_to_revenue", "매출원가 / 매출", "pct"),
        ("derived__sga_to_revenue", "판매관리비 / 매출", "pct"),
        ("derived__financial_cost_to_revenue", "금융비용 / 매출", "pct"),
    ]),
    ("투자·자산", [
        ("derived__capex_to_revenue", "CAPEX / 매출", "pct"),
        ("derived__ppe_to_assets", "유형자산 / 총자산", "pct"),
    ]),
    ("차입구조", [
        ("derived__short_debt_to_total_debt", "단기차입 / 총이자부부채", "pct"),
        ("derived__long_debt_to_total_debt", "장기차입 / 총이자부부채", "pct"),
        ("derived__bond_to_total_debt", "사채 / 총이자부부채", "pct"),
    ]),
    ("운전자본", [
        ("derived__inventory_to_revenue", "재고 / 매출", "pct"),
        ("derived__receivables_to_revenue", "매출채권 / 매출", "pct"),
        ("derived__payables_to_revenue", "매입채무 / 매출", "pct"),
    ]),
    ("전년 대비 변화", [
        ("delta_1y__derived__operating_margin", "영업이익률 변화", "pp"),
        ("delta_1y__derived__debt_to_assets", "총부채 / 총자산 변화", "pp"),
        ("delta_1y__derived__current_ratio", "유동비율 변화", "ratio_signed"),
        ("delta_1y__derived__roa_proxy", "ROA 대용치 변화", "pp"),
    ]),
]

ACTIONS = [
    ("A0", "현 상태 유지", "별도 개입 없이 현재 사업계획 유지"),
    ("DL", "부채 상환", "총 이자부부채를 약 35% 상환"),
    ("RF", "차환", "단기차입금의 약 47%를 장기성 차입으로 전환"),
    ("CX", "성장 CAPEX 축소", "유지보수 투자는 유지하고 성장성 CAPEX를 약 63% 축소"),
    ("WC1", "운전자본 회수 개선", "재고회전율 약 +0.70회, 매출채권회전율 약 +0.47회"),
    ("WC2", "공급자금융 활용", "재고 약 +0.47회, 매출채권 약 +0.31회, 매입채무회전율 약 -0.82회"),
    ("OE", "비용 효율화", "매출원가율 약 -1.34%p, 판매관리비율 약 -0.86%p"),
    ("MX1", "부채상환 + 비용효율화", "부채 약 17% 상환 + 원가율 약 -0.67%p + 판관비율 약 -0.43%p"),
    ("MX2", "부채상환 + 운전자본 개선", "부채 약 17% 상환 + 재고 약 +0.28회 + 매출채권 약 +0.19회 + 매입채무회전율 약 -0.25회"),
]

ACTION_OPTIONS = [f"{a} — {b}" for a, b, _ in ACTIONS]

KOREAN_DEFS = {
    "derived__debt_to_assets": "총부채 ÷ 총자산. 총이자부부채 비율이 아님.",
    "derived__equity_to_assets": "자기자본 ÷ 총자산.",
    "derived__current_ratio": "유동자산 ÷ 유동부채.",
    "derived__cash_ratio": "현금및현금성자산 ÷ 유동부채.",
    "derived__operating_margin": "영업이익 ÷ 매출.",
    "derived__gross_margin": "매출총이익 ÷ 매출.",
    "derived__net_margin": "당기순이익 ÷ 매출.",
    "derived__roa_proxy": "당기순이익 ÷ 기말 총자산. 평균자산 ROA가 아님.",
    "derived__cogs_to_revenue": "매출원가 ÷ 매출.",
    "derived__sga_to_revenue": "판매관리비 ÷ 매출.",
    "derived__financial_cost_to_revenue": "광의의 금융비용 ÷ 매출. 순수 이자비용만을 의미하지 않음.",
    "derived__capex_to_revenue": "동결된 표준 CAPEX ÷ 매출.",
    "derived__ppe_to_assets": "순유형자산 ÷ 총자산.",
    "derived__short_debt_to_total_debt": "단기차입금 ÷ 총이자부부채.",
    "derived__long_debt_to_total_debt": "유동성장기부채와 비유동장기차입금 ÷ 총이자부부채.",
    "derived__bond_to_total_debt": "사채 ÷ 총이자부부채.",
    "derived__inventory_to_revenue": "재고자산 ÷ 매출.",
    "derived__receivables_to_revenue": "매출채권 ÷ 매출.",
    "derived__payables_to_revenue": "매입채무 ÷ 매출.",
    "delta_1y__derived__operating_margin": "당해 영업이익률 - 전년 영업이익률.",
    "delta_1y__derived__debt_to_assets": "당해 총부채/총자산 - 전년 값.",
    "delta_1y__derived__current_ratio": "당해 유동비율 - 전년 유동비율.",
    "delta_1y__derived__roa_proxy": "당해 ROA 대용치 - 전년 값.",
    "fiscal_year": "제공된 재무상태의 회계연도.",
    "log_assets": "총자산 규모를 로그 변환한 지표. 값이 클수록 기업 규모가 큼.",
    "market": "원천자료의 시장 구분.",
    "industry_class": "원천자료의 산업 구분.",
}

def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()

def fmt_value(v, kind: str) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "정보 없음"
    if kind == "text":
        s = str(v)
        return "정보 없음" if s in {"", "nan", "None", "UNKNOWN"} else s
    if kind == "year":
        try:
            return str(int(float(v)))
        except Exception:
            return str(v)
    try:
        x = float(v)
    except Exception:
        return str(v)
    if kind == "pct":
        return f"{x * 100:.1f}%"
    if kind == "pp":
        return f"{x * 100:+.1f}%p"
    if kind == "ratio":
        return f"{x:.2f}배"
    if kind == "ratio_signed":
        return f"{x:+.2f}배"
    if kind == "raw3":
        return f"{x:.2f}"
    return f"{x:.6g}"

def fit_lines(draw, text, fnt, max_width):
    text = str(text)
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines or [""]

def draw_card(row: pd.Series, alias: str, out: Path):
    W, H = 1600, 2200
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    f_title = font(54, True)
    f_sub = font(28, False)
    f_group = font(29, True)
    f_label = font(27, False)
    f_val = font(29, True)
    f_note = font(24, False)

    d.text((70, 55), f"Case {alias} — 2024년 재무상태", font=f_title, fill=(20,20,20))
    d.text((70, 128), "기업명은 비공개입니다. 제공된 정보만 사용하고 외부 검색은 하지 마십시오.", font=f_sub, fill=(70,70,70))

    y = 195
    left = 70
    right = W - 70
    label_x = 110
    value_x = 1030
    row_h = 48
    group_h = 48

    for group, fields in FIELD_GROUPS:
        d.rounded_rectangle((left, y, right, y + group_h), radius=8, fill=(238,240,244))
        d.text((90, y + 8), group, font=f_group, fill=(25,25,25))
        y += group_h + 4
        for key, label, kind in fields:
            val = fmt_value(row.get(key), kind)
            d.line((left, y + row_h - 1, right, y + row_h - 1), fill=(225,225,225), width=1)
            d.text((label_x, y + 8), label, font=f_label, fill=(35,35,35))
            # Long text values are wrapped.
            if kind == "text" and len(val) > 28:
                lines = fit_lines(d, val, f_label, right - value_x - 20)[:2]
                for j, line in enumerate(lines):
                    d.text((value_x, y + 5 + j*26), line, font=f_label, fill=(20,20,20))
                actual_h = max(row_h, 62)
            else:
                d.text((value_x, y + 7), val, font=f_val, fill=(20,20,20))
                actual_h = row_h
            y += actual_h
        y += 10

    d.text((70, H - 115), "목표: 향후 약 1년 동안 기업의 재무건전성·신용상태 개선을 위한 우선 관리행동 선택", font=f_note, fill=(55,55,55))
    d.text((70, H - 75), "주의: 값이 '정보 없음'인 항목을 0으로 간주하지 마십시오.", font=f_note, fill=(85,85,85))
    img.save(out, "PNG", optimize=True)

def draw_action_card(out: Path):
    W, H = 1600, 1860
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f_title = font(50, True)
    f_head = font(28, True)
    f_code = font(30, True)
    f_text = font(26, False)
    f_note = font(23, False)

    d.text((70, 50), "9개 표준 관리행동", font=f_title, fill=(20,20,20))
    d.text((70, 120), "각 Case에서 아래 후보 중 정확히 하나를 선택합니다. 후보를 수정하거나 결합하지 않습니다.", font=f_text, fill=(65,65,65))

    y = 190
    for code, name, desc in ACTIONS:
        d.rounded_rectangle((70, y, 1530, y+152), radius=12, fill=(246,247,249), outline=(220,220,220))
        d.text((95, y+24), code, font=f_code, fill=(25,25,25))
        d.text((215, y+20), name, font=f_head, fill=(25,25,25))
        lines = fit_lines(d, desc, f_text, 1220)[:3]
        for j, line in enumerate(lines):
            d.text((215, y+62+j*30), line, font=f_text, fill=(65,65,65))
        y += 164

    d.text((70, H-105), "모든 비-A0 후보는 연구에서 사전에 동결한 표준 강도(B1 nominal intensity 1)입니다.", font=f_note, fill=(70,70,70))
    d.text((70, H-70), "A0는 무개입 기준입니다. '더 큰 행동이 항상 더 좋다'고 가정하지 마십시오.", font=f_note, fill=(70,70,70))
    img.save(out, "PNG", optimize=True)

def draw_action_semantics(out: Path):
    W, H = 1600, 1180
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f_title = font(48, True)
    f_head = font(28, True)
    f_text = font(25, False)
    d.text((70, 48), "행동 선택 시 참고사항", font=f_title, fill=(20,20,20))
    rules = [
        ("부채 상환", "실제 상환은 회사의 가용 현금과 유동성 범위 안에서 가능하다고 가정합니다."),
        ("차환", "총 차입원금은 늘리지 않고 단기차입 일부를 장기성 차입으로 바꾸는 행동입니다."),
        ("CAPEX 축소", "유지보수 투자는 유지하고 성장 목적의 신규 투자를 줄이는 행동입니다."),
        ("운전자본", "재고·매출채권 회전율 증가는 더 빠른 회수, 매입채무회전율 감소는 지급기간 연장 방향입니다."),
        ("비용 효율화", "매출원가율과 판매관리비율을 낮추는 행동입니다."),
        ("후보 선택", "9개 후보 중 가장 적절하다고 생각하는 하나를 고르십시오. 숫자의 미세한 차이보다 행동 방향을 중심으로 판단해 주십시오."),
    ]
    y = 140
    for head, body in rules:
        d.rounded_rectangle((70, y, 1530, y+130), radius=8, fill=(248,249,250), outline=(225,225,225))
        d.text((92, y+18), head, font=f_head, fill=(35,35,35))
        lines = fit_lines(d, body, f_text, 1120)[:3]
        for j, line in enumerate(lines):
            d.text((360, y+18+j*31), line, font=f_text, fill=(55,55,55))
        y += 145
    img.save(out, "PNG", optimize=True)

def draw_metric_guides(out1: Path, out2: Path):
    label_by_key = {key: label for _, fields in FIELD_GROUPS for key, label, _ in fields}
    items = [(k, label_by_key.get(k, k), v) for k, v in KOREAN_DEFS.items()]
    halves = [items[:14], items[14:]]
    for out, subset, idx in [(out1, halves[0], 1), (out2, halves[1], 2)]:
        W, H = 1600, 1500
        img = Image.new("RGB", (W,H), "white")
        d = ImageDraw.Draw(img)
        f_title = font(48, True)
        f_key = font(23, True)
        f_desc = font(24, False)
        d.text((70, 48), f"재무지표 읽는 법 ({idx}/2)", font=f_title, fill=(20,20,20))
        y=130
        for key, label, desc in subset:
            d.rounded_rectangle((70,y,1530,y+82), radius=8, fill=(248,249,250), outline=(225,225,225))
            d.text((92,y+12), label, font=f_key, fill=(45,45,45))
            lines=fit_lines(d, desc, f_desc, 930)[:2]
            for j,line in enumerate(lines):
                d.text((590,y+10+j*29), line, font=f_desc, fill=(55,55,55))
            y += 94
        img.save(out, "PNG", optimize=True)

def build_copy_paste(alias_order):
    action_lines = "\n".join(f"- {a} — {b}" for a,b,_ in ACTIONS)
    cases = []
    for alias in alias_order:
        cases.append(f"""## Case {alias}

상단 이미지: cards/case_{alias}.png

Q1. 이 기업의 향후 약 1년 동안의 재무건전성·신용상태 개선을 위해 가장 우선적으로 권고할 관리행동 하나를 선택해 주십시오.
- 유형: 객관식
- 필수: 예
{action_lines}

Q2. 위 선택에 대한 확신 정도는 어느 정도입니까?
- 유형: 선형배율 1~5
- 1: 매우 불확실
- 5: 매우 확신
- 필수: 예

Q3. 위 행동을 선택한 가장 중요한 이유를 1~3문장으로 작성해 주십시오.
- 유형: 장문형
- 필수: 예
""")
    return f"""# Google Form 복붙용 원고

## 폼 제목
기업 신용상태 개선을 위한 재무행동 판단 연구

## 폼 설명
본 설문은 기업의 재무정보를 바탕으로 향후 약 1년의 재무건전성·신용상태 개선을 위해 어떤 관리행동을 우선적으로 권고할 것인지 조사하기 위한 연구입니다.

각 사례에는 2024년 기업 재무정보, 시장 및 산업정보가 제공됩니다. 기업명은 제공하지 않습니다. 제공된 정보만 이용하여 판단해 주시고 인터넷 검색, 외부 데이터 조회 또는 동료와의 상의는 하지 말아 주십시오.

각 사례에서는 사전에 정의된 9개의 관리행동 가운데 가장 적절하다고 판단하는 행동 하나를 선택합니다. 정답이 정해진 시험이 아니며 현재 제공된 정보에 기초한 전문적 판단을 응답해 주시면 됩니다.

개인의 이름과 소속기관명은 수집하지 않습니다.

예상 소요시간: 약 15~25분

※ 실제 배포 전 소속 대학의 인간대상연구/IRB 또는 심의면제 요건을 확인하고 필요한 승인·문구로 교체하십시오.

## 섹션 1 — 참여 동의
Q. 위 연구설명을 확인하였으며 자발적으로 연구 참여에 동의합니다.
- 동의합니다
- 동의하지 않습니다
- 유형: 객관식 / 필수
- 권장 분기: '동의하지 않습니다' 선택 시 설문 제출

## 섹션 2 — 응답자 배경
Q1. 현재 또는 과거에 경험한 업무를 모두 선택해 주십시오.
- 은행 기업금융·여신심사
- 신용평가·신용분석
- 금융기관 리스크관리
- 증권사·자산운용사 기업/산업분석
- 기업 재무·자금·기획
- 회계·감사·컨설팅
- 기업가치평가·투자분석
- 금융·재무 관련 연구/교육
- 기타
유형: 체크박스 / 필수

Q2. 기업 재무 또는 신용분석 관련 실무·연구 경험은 얼마나 됩니까?
- 2년 미만
- 2년 이상 ~ 5년 미만
- 5년 이상 ~ 10년 미만
- 10년 이상 ~ 15년 미만
- 15년 이상
유형: 객관식 / 필수

Q3. 기업의 재무상태 및 신용도를 평가하는 업무에 대한 본인의 경험 수준은 어느 정도입니까?
- 선형배율 1~5
- 1: 경험이 거의 없음
- 5: 매우 익숙함
- 필수

## 섹션 3 — 판단 규칙
이미지 1: cards/00_metric_guide_1.png
이미지 2: cards/00_metric_guide_2.png
이미지 3: cards/01_action_catalog.png\n이미지 4: cards/02_action_semantics.png

설명:
- 기업명은 제공되지 않습니다.
- 산업 및 시장정보는 제공된 정보의 일부입니다.
- '정보 없음'을 0으로 해석하지 마십시오.
- 각 사례에서 9개 후보 가운데 하나만 선택하십시오.
- 기업을 알아보았다고 생각하더라도 외부 검색이나 기억에 의존한 구체적 수치·사건을 추가하지 마십시오.
- 목표는 주가상승이나 기업가치 극대화가 아니라 향후 약 1년의 재무건전성·신용상태 개선입니다.

{chr(10).join(cases)}

## 마지막 섹션 — 정보 충분성 및 오염 점검
Q1. 실제 기업 신용개선 권고를 내린다면 추가로 확인하고 싶은 정보를 모두 선택해 주십시오.
- 구체적인 차입금 만기구조 및 금리
- 향후 투자계획 및 CAPEX 계획
- 사업부문별 수익성
- 경영진의 사업계획
- 영업현금흐름 전망
- 산업 전망 및 경쟁상황
- 담보·보증 및 자금조달 가능성
- 신용평가사의 정성적 평가요소
- 기업명 및 과거 사업이력
- 기타
유형: 체크박스

Q2. 실제 기업이 어떤 회사인지 알아보았거나 강하게 추정한 사례가 있습니까?
- 없음
- Case A
- Case B
- Case C
- Case D
- Case E
- Case F
- Case G
- Case H
- Case I
유형: 체크박스

Q3. 응답 과정에서 인터넷 검색, 외부 데이터 조회 또는 생성형 AI 도구를 사용했습니까?
- 아니오
- 예
유형: 객관식 / 필수

Q4. 9개 표준 행동으로는 충분히 표현하기 어렵다고 느낀 사례가 있다면 Case와 원하는 행동을 적어 주십시오.
유형: 장문형 / 선택

Q5. 설문 판단 과정에서 어렵거나 애매했던 점이 있다면 자유롭게 작성해 주십시오.
유형: 장문형 / 선택
"""

def build_apps_script(alias_order):
    action_js = json.dumps(ACTION_OPTIONS, ensure_ascii=False)
    aliases_js = json.dumps(alias_order, ensure_ascii=False)
    return f'''// Google Apps Script — one-run survey builder
// Paste this file into https://script.google.com and run createMatchedHumanSurvey().
// The case-card images are fetched from the public research repository and embedded into the Form.
// After creation, the script logs the edit URL, responder URL, and response-spreadsheet URL.

const CARD_BASE_URL =
  'https://github.com/CallMeDemian/thesis-human-benchmark-2024/raw/refs/heads/analysis/strict9-human-anchor/' +
  'analysis_outputs/google_form_matched_human/cards/';

const ACTION_OPTIONS = {action_js};
const CASE_ALIASES = {aliases_js};

function addRepoImage(form, filename, title) {{
  const response = UrlFetchApp.fetch(CARD_BASE_URL + filename);
  if (response.getResponseCode() !== 200) {{
    throw new Error('Failed to fetch image: ' + filename + ' / HTTP ' + response.getResponseCode());
  }}
  form.addImageItem()
    .setTitle(title)
    .setImage(response.getBlob())
    .setWidth(700);
}}

function createMatchedHumanSurvey() {{
  const form = FormApp.create('기업 신용상태 개선을 위한 재무행동 판단 연구', true);
  form.setCollectEmail(false);
  form.setProgressBar(true);
  form.setDescription(
    '본 설문은 2024년 재무정보·시장·산업정보를 바탕으로 향후 약 1년의 재무건전성·신용상태 개선을 위한 관리행동을 판단하는 연구입니다. ' +
    '기업명은 제공하지 않습니다. 제공된 정보만 이용하여 판단하고 인터넷 검색, 외부 데이터 조회, 생성형 AI 사용 또는 동료와의 상의는 하지 마십시오.'
  );
  form.setConfirmationMessage('응답해 주셔서 감사합니다.');

  const responseSheet = SpreadsheetApp.create('기업 신용상태 개선 재무행동 설문 응답');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, responseSheet.getId());

  const consent = form.addMultipleChoiceItem()
    .setTitle('위 연구설명을 확인하였으며 자발적으로 연구 참여에 동의합니다.')
    .setRequired(true);
  consent.setChoices([
    consent.createChoice('동의합니다', FormApp.PageNavigationType.CONTINUE),
    consent.createChoice('동의하지 않습니다', FormApp.PageNavigationType.SUBMIT)
  ]);

  form.addPageBreakItem().setTitle('응답자 배경');
  form.addCheckboxItem().setTitle('현재 또는 과거에 경험한 업무를 모두 선택해 주십시오.')
    .setChoiceValues(['은행 기업금융·여신심사','신용평가·신용분석','금융기관 리스크관리','증권사·자산운용사 기업/산업분석','기업 재무·자금·기획','회계·감사·컨설팅','기업가치평가·투자분석','금융·재무 관련 연구/교육','기타'])
    .setRequired(true);
  form.addMultipleChoiceItem().setTitle('기업 재무 또는 신용분석 관련 실무·연구 경험은 얼마나 됩니까?')
    .setChoiceValues(['2년 미만','2년 이상 ~ 5년 미만','5년 이상 ~ 10년 미만','10년 이상 ~ 15년 미만','15년 이상'])
    .setRequired(true);
  form.addScaleItem().setTitle('기업의 재무상태 및 신용도를 평가하는 업무에 대한 본인의 경험 수준은 어느 정도입니까?')
    .setBounds(1,5).setLabels('경험이 거의 없음','매우 익숙함').setRequired(true);

  form.addPageBreakItem().setTitle('판단 규칙');
  addRepoImage(form, '00_metric_guide_1.png', '재무지표 읽는 법 1/2');
  addRepoImage(form, '00_metric_guide_2.png', '재무지표 읽는 법 2/2');
  addRepoImage(form, '01_action_catalog.png', '9개 표준 관리행동');
  addRepoImage(form, '02_action_semantics.png', '관리행동 해석 규칙');
  form.addSectionHeaderItem().setTitle('유의사항').setHelpText(
    '각 사례에서 9개 후보 중 하나만 선택하십시오. 정보 없음은 0이 아닙니다. ' +
    '기업을 추정하더라도 외부 검색이나 기억에 의존한 구체적 사건·수치를 추가하지 마십시오. ' +
    '목표는 주가상승이나 기업가치 극대화가 아니라 향후 약 1년의 재무건전성·신용상태 개선입니다.'
  );

  CASE_ALIASES.forEach(alias => {{
    form.addPageBreakItem().setTitle('Case ' + alias);
    addRepoImage(form, 'case_' + alias + '.png', 'Case ' + alias + ' 재무정보');
    form.addMultipleChoiceItem()
      .setTitle('이 기업의 향후 약 1년 동안의 재무건전성·신용상태 개선을 위해 가장 우선적으로 권고할 관리행동 하나를 선택해 주십시오.')
      .setChoiceValues(ACTION_OPTIONS)
      .setRequired(true);
    form.addScaleItem()
      .setTitle('위 선택에 대한 확신 정도는 어느 정도입니까?')
      .setBounds(1,5).setLabels('매우 불확실','매우 확신').setRequired(true);
    form.addParagraphTextItem()
      .setTitle('위 행동을 선택한 가장 중요한 이유를 1~3문장으로 작성해 주십시오.')
      .setRequired(true);
  }});

  form.addPageBreakItem().setTitle('정보 충분성 및 오염 점검');
  form.addCheckboxItem().setTitle('실제 기업 신용개선 권고를 내린다면 추가로 확인하고 싶은 정보를 모두 선택해 주십시오.')
    .setChoiceValues(['구체적인 차입금 만기구조 및 금리','향후 투자계획 및 CAPEX 계획','사업부문별 수익성','경영진의 사업계획','영업현금흐름 전망','산업 전망 및 경쟁상황','담보·보증 및 자금조달 가능성','신용평가사의 정성적 평가요소','기업명 및 과거 사업이력','기타']);
  form.addCheckboxItem().setTitle('실제 기업이 어떤 회사인지 알아보았거나 강하게 추정한 사례가 있습니까?')
    .setChoiceValues(['없음'].concat(CASE_ALIASES.map(x => 'Case ' + x)));
  form.addMultipleChoiceItem().setTitle('응답 과정에서 인터넷 검색, 외부 데이터 조회 또는 생성형 AI 도구를 사용했습니까?')
    .setChoiceValues(['아니오','예']).setRequired(true);
  form.addParagraphTextItem().setTitle('9개 표준 행동으로는 충분히 표현하기 어렵다고 느낀 사례가 있다면 Case와 원하는 행동을 적어 주십시오.');
  form.addParagraphTextItem().setTitle('설문 판단 과정에서 어렵거나 애매했던 점이 있다면 자유롭게 작성해 주십시오.');

  Logger.log('Form edit URL: ' + form.getEditUrl());
  Logger.log('Responder URL: ' + form.getPublishedUrl());
  Logger.log('Response spreadsheet: ' + responseSheet.getUrl());
}}
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", required=True)
    ap.add_argument("--repro", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    human = Path(args.human)
    repro = Path(args.repro)
    out = Path(args.out)
    cards = out / "cards"
    cards.mkdir(parents=True, exist_ok=True)

    strict = pd.read_csv(human / "outputs/strict_archival_benchmark.csv", dtype={"stock_code": str, "firm_key": str})
    strict = strict[["firm_key","stock_code","firm_name","mapped_action"]].drop_duplicates("firm_key").copy()
    if len(strict) != 9:
        raise RuntimeError(f"Expected 9 strict firms, found {len(strict)}")

    prompt = json.loads((repro / PROMPT_REL).read_text(encoding="utf-8"))
    exact_catalog = prompt["action_contract"]["catalog"]
    exact_catalog_by_id = {x["candidate_id"]: x["action"] for x in exact_catalog}
    expected_mx2 = {
        "growth_capex_reduction_pct": 0.0,
        "deleveraging_total_debt_pct": 0.17347746621389504,
        "refinancing_short_debt_pct": 0.0,
        "inv_turnover_chg": 0.27967522463998157,
        "ar_turnover_chg": 0.18682078088911175,
        "ap_turnover_chg": -0.2453574198113573,
        "cogs_ratio_chg": 0.0,
        "sga_ratio_chg": 0.0,
    }
    if exact_catalog_by_id.get("MX2") != expected_mx2:
        raise RuntimeError(f"Frozen MX2 contract mismatch: {exact_catalog_by_id.get('MX2')}")
    (out / "ACTION_CATALOG_EXACT.json").write_text(
        json.dumps(exact_catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    icb_fields = [x["field"] for x in prompt["information_conditions"]["IC-b"]["visible_dictionary"]]
    if len(icb_fields) != 27:
        raise RuntimeError(f"Expected 27 IC-b fields, found {len(icb_fields)}")

    payload = pd.read_parquet(repro / PAYLOAD_REL)
    if "firm_key" not in payload.columns:
        # Fallback to the frozen row-id crosswalk already produced by strict-9 analysis.
        cross = pd.read_csv(human / "analysis_outputs/strict9/strict9_case_level.csv", dtype={"firm_key": str})
        cross = cross[["row_id","firm_key"]].drop_duplicates()
        if "row_id" not in payload.columns:
            raise RuntimeError("Payload has neither firm_key nor row_id")
        payload = payload.merge(cross, on="row_id", how="left", validate="many_to_one")

    payload["firm_key"] = payload["firm_key"].astype(str)
    keys = set(strict["firm_key"].astype(str))
    states = payload[payload["firm_key"].isin(keys)].copy()

    if "fiscal_year" in states.columns:
        fy = pd.to_numeric(states["fiscal_year"], errors="coerce")
        if (fy == 2024).any():
            states = states[fy == 2024].copy()

    missing = [f for f in icb_fields if f not in states.columns]
    if missing:
        raise RuntimeError(f"IC-b fields missing from payload: {missing}")

    counts = states.groupby("firm_key").size()
    bad = counts[counts != 1]
    if not bad.empty:
        raise RuntimeError(f"Expected one payload row per strict firm: {bad.to_dict()}")
    if states["firm_key"].nunique() != 9:
        got = set(states["firm_key"])
        raise RuntimeError(f"Missing strict firm payloads: {sorted(keys-got)}")

    strict_sorted = strict.sort_values("firm_key").reset_index(drop=True)
    order = list(strict_sorted["firm_key"])
    random.Random(SEED).shuffle(order)
    aliases = list("ABCDEFGHI")
    alias_map = dict(zip(order, aliases))

    key = strict_sorted.copy()
    key["case_alias"] = key["firm_key"].map(alias_map)
    key = key.sort_values("case_alias")[["case_alias","firm_key","stock_code","firm_name","mapped_action"]]
    key.to_csv(out / "RESEARCHER_ONLY_case_key.csv", index=False, encoding="utf-8-sig")

    states = states.merge(key[["firm_key","case_alias"]], on="firm_key", how="left", validate="one_to_one")
    public_cols = ["case_alias"] + icb_fields
    states[public_cols].sort_values("case_alias").to_csv(out / "case_states_ICb_full_precision.csv", index=False, encoding="utf-8-sig")

    draw_metric_guides(cards / "00_metric_guide_1.png", cards / "00_metric_guide_2.png")
    draw_action_card(cards / "01_action_catalog.png")
    draw_action_semantics(cards / "02_action_semantics.png")

    by_key = states.set_index("firm_key")
    for _, r in key.iterrows():
        draw_card(by_key.loc[r["firm_key"]], r["case_alias"], cards / f"case_{r['case_alias']}.png")

    (out / "COPY_PASTE_FORM_TEXT.md").write_text(build_copy_paste(aliases), encoding="utf-8")
    (out / "CREATE_GOOGLE_FORM.gs").write_text(build_apps_script(aliases), encoding="utf-8")

    manifest = {
        "status": "MATCHED_HUMAN_FORM_PACKAGE",
        "seed": SEED,
        "strict_firms": 9,
        "information_condition": "IC-b",
        "action_mode": "candidate9",
        "budget": "B1",
        "icb_field_count": len(icb_fields),
        "case_aliases": aliases,
        "payload_source": str(PAYLOAD_REL),
        "prompt_contract": str(PROMPT_REL),
        "human_source": "outputs/strict_archival_benchmark.csv",
        "respondent_visible_firm_identity": False,
        "researcher_only_key": "RESEARCHER_ONLY_case_key.csv",
        "notes": [
            "Images use the same 27 IC-b information fields, but values are rounded to a human-readable precision for expert judgment. Full-precision values remain in case_states_ICb_full_precision.csv.",
            "Respondent-facing action magnitudes are rounded for readability; ACTION_CATALOG_EXACT.json preserves the exact frozen eight-dimensional vectors for audit.",
            "Do not distribute the researcher-only case key to respondents.",
            "Verify institutional human-subject/IRB requirements before fielding."
        ]
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme = """# Matched-condition human Google Form package

This package is generated from the frozen strict-9 archival subset and the frozen V4.3 FY2024 IC-b LLM payload.

Files:
- COPY_PASTE_FORM_TEXT.md: exact Google Form section/question text.
- CREATE_GOOGLE_FORM.gs: one-run Apps Script that creates the Form, embeds the frozen public case-card images, and links a response spreadsheet.
- cards/: two metric-guide images, one exact action-catalog image, one action-semantics image, and nine anonymized case cards.
- case_states_ICb_full_precision.csv: the 27 IC-b values at full stored precision.\n- ACTION_CATALOG_EXACT.json: exact frozen candidate9 eight-dimensional vectors from the LLM prompt contract.
- RESEARCHER_ONLY_case_key.csv: confidential alias-to-firm mapping and archival human action. Do not give this file to respondents.
- MANIFEST.json: frozen package metadata.

Design:
- Human condition: IC-b / candidate9 / B1.
- Firm names and stock codes are hidden.
- Market, industry, fiscal year and all 23 financial fields visible under IC-b are retained.
- Values are re-formatted for human readability but no diagnostic interpretation is added.
- Each respondent chooses one candidate action, reports confidence, and gives a short rationale for all nine firms.

Before deployment, confirm the university's human-subject research / IRB or exemption requirements and replace the consent text if an approved template is required.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")

if __name__ == "__main__":
    main()

# Package protocol revision: explicit external-tool contamination check.
