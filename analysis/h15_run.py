"""H15 package entrypoint: selection is separate; configure readable presentation and attach audit."""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
import h15_build as build

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--human',required=True);p.add_argument('--repro',required=True);a=p.parse_args()
    h=Path(a.human);out=h/'analysis_outputs/human15'
    build.main()
    audit=json.loads((h/'evidence/ARCHIVAL_PASS3_REVIEW_20261001.json').read_text())
    targets=json.loads((out/'ARCHIVAL_PASS3_TARGETS.json').read_text())
    assert len(audit['records'])==17
    assert {r['firm_key'] for r in audit['records']}=={r['firm_key'] for r in targets}
    assert sum(r['primary_full_text_rechecked'] for r in audit['records'])==4
    additions=[r for r in audit['records'] if r['decision']=='ADD_SEPARATE_ISSUER_ONGOING_POLICY_LAYER']
    assert len(additions)==1 and additions[0]['source_layer']=='IR'
    shutil.copy2(h/'evidence/ARCHIVAL_PASS3_REVIEW_20261001.json',out/'ARCHIVAL_PASS3_REVIEW.json')
    shutil.copy2(h/'analysis_outputs/archival_pass3/ISSUER_POLICY_EXTENSION.csv',out/'ISSUER_POLICY_EXTENSION.csv')
    shutil.copy2(h/'protocol/EXPANSION_PROTOCOL_20261001.md',out/'EXPANSION_PROTOCOL.md')
    report='''# 확장 검토 결과 — 2026-10-01

## 실제로 확장한 두 범위

- 문헌 기반: 원래 외부 전문가 문서 strict-9는 그대로 보존. 별도 기업 자체 경영정책(IR) 1건 추가. 서로 다른 출처 층을 나란히 세면 10개이지만 독립 전문가 strict-10이라고 부르지 않는다.
- 설문 기반: 원래 사례 A–I + 재무상태 기준 신규 사례 J–O = 15개. 새 6개에 정답 행동은 부여하지 않았다.

## 문헌 재검토 범위와 결과

고정된 17개 후보(원문 미확보 13개, mapping은 있지만 strict 탈락 4개)를 대상으로 검색·원문 접근을 재시도했다. 4개는 원문 서술을 직접 다시 확인했고, 13개는 충분한 원문 미확보 상태를 유지했다. 이 결과는 전체 575개에 대해 가능한 모든 원문을 소진했다는 뜻이 아니다.

인터엠: 2024-11-12 회사 제공 보도자료 말미에 비용 효율화에 현재 주력하고 있다는 문장이 있다. 앞선 검토에서 이미 끝난 원가절감만 있다고 본 시간성 판단은 불충분했다. 현재 진행 중인 OE라는 근거는 인정하되, 회사 자체 발표이므로 별도 IR 층으로 추가한다. 2025 실행 규모나 실제 신용개선 효과를 증명하지는 않는다.

서희건설: 한국신용평가 2024-12-23 보고서 5·7쪽은 과거 공사미수금 정산과 현금 축적, 향후 현금흐름·사업비 분산을 설명한다. 특정한 미래 회수속도 개선 행동을 확인하지 못하여 WC1 strict로 승격하지 않는다.

동국제약: LS증권 2024-10-25 보고서 1쪽의 미래 제조원가 절감은 리봄화장품 인수·생산시설 통합과 연결된다. 해당 co-action을 지우고 OE 단독으로 처리하지 않는다.

이수앱지스: 대신증권 2024-05-31 보고서 4쪽은 배양기 변경·생산성 개선과 전환비용 반영이 이미 이뤄졌다고 설명한다. 이익 개선이 계속된다는 전망만으로 새 행동을 만들지 않는다. 2024-07-23 한국투자 보고서의 자동 요약도 원문 대체로 쓰지 않는다.

BGF리테일(2024-12-02 하나), 에스피시스템스(2024-06-04 한국투자), 퓨런티어(2024-12-10 신한)는 구체적 추가 원문 탐색 경로를 기록했다. 충분한 원문이 확보되지 않았으므로 새 strict 사례로 세지 않았다. 모든 기업의 판정·접근 URL·제약은 ARCHIVAL_PASS3_REVIEW.json에 보존했다.

## 설문 신규 사례

| 사례 | 기업 | 사전 선정 층 | 참고 수치(동결 FY2024 입력) |
|---|---|---|---|
| J | 와이엠티 | 총부채/자산 상위 25% | 총부채/자산 56.1%, CAPEX/매출 46.7% |
| K | 금호건설 | 유동비율 하위 25% | 유동비율 0.90배, 총부채/자산 83.7% |
| L | 타이거일렉 | 단기차입 비중 상위 25% | 총이자부부채 중 단기차입 100.0% |
| M | 황금에스티 | 재고·채권/매출 상위 25% | 재고와 매출채권 합계/매출 65.8% |
| N | 주성엔지니어링 | CAPEX/매출 상위 25% | CAPEX/매출 7.6% |
| O | 대정화금 | 저부채·고유동성·흑자 | 총부채/자산 14.4%, 유동비율 3.97배 |

임계값은 575개 전체의 2024년 입력으로 계산했다. 각 층에서 원래 9개와 이전 추출 기업을 제외하고 사전 고정한 해시 순서로 한 개씩 선정했다. 모델 행동·점수·2025년 결과는 선택 함수에 입력하지 않았다. 선정 층과 기업명은 응답 화면에 표시하지 않는다.

## 사용·해석 주의

고부채라는 이유만으로 DL이 정답인 것은 아니다. 15개는 재무상태의 다양한 조합을 보려는 목적표본이지 전체 기업에 대한 대표표본이 아니다. 인간 응답의 최빈값도 인과적 정답이 아니다. 기존 9개, 신규 6개, 전체 15개를 구분하여 제시한다.

사람용 표기는 반올림했지만 정확한 채점 벡터는 ACTION_CATALOG_EXACT.json을 사용한다. MX2는 총이자부부채 약 17% 상환, 재고회전율 +0.28회, 매출채권회전율 +0.19회, 매입채무회전율 −0.25회로 표시한다.

자동 검증은 자료 결합·필드 수·후보 벡터·텍스트 누출·이미지 경계·스크립트 구문까지다. Google 계정 실제 실행과 브라우저 화면 확인은 수행하지 않았다. 생성되는 폼은 비공개 초안이며 사용자가 배포 전 확인한다.
'''
    (out/'REVIEW_REPORT_KO.md').write_text(report,encoding='utf-8')
    validation=json.loads((out/'VALIDATION.json').read_text())
    validation['archival_target_coverage']=17;validation['new_independent_expert_cases']=0;validation['separate_issuer_policy_cases']=1
    build.dump(out/'VALIDATION.json',validation)
    print('H15_RELEASE_PASS; survey 15; independent expert archive 9 preserved; issuer extension 1.')
