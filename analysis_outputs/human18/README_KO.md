# 18개 사례 Google Form 패키지 — H18-v1

## 가장 빠른 사용 방법
1. CREATE_GOOGLE_FORM.txt를 메모장으로 열어 전체 복사합니다.
2. Google Apps Script 새 프로젝트의 기본 코드를 지우고 붙여넣습니다.
3. createHuman15Survey 함수를 실행하고 권한을 승인합니다.
4. 실행 로그의 Draft edit URL을 엽니다. 설문과 응답 시트가 생성됩니다.
5. 연구 문의처·참여 안내와 기관의 연구 절차를 확인하고, 미리보기로 시험 응답을 한 뒤 게시합니다. 기본 생성 상태는 비공개 초안입니다.

이미지는 자동 삽입되며 해시로 버전을 확인합니다. 이미지 다운로드가 막히면 SETTINGS.useImages를 false로 바꿔 실행하십시오. 같은 27개 필드를 폼 안의 텍스트로 표시합니다. 오류 이전에 폼을 생성하지 않도록 이미지 검사를 먼저 합니다. 동일 설정 재실행은 기존 초안 URL을 반환합니다.

SETTINGS.order를 REVERSE로 바꾸면 순서가 반대인 별도 초안을 만들 수 있습니다. 참여자는 둘 중 한 버전만 응답합니다. 폼 전체의 질문 섞기는 켜지 마십시오. 18개 사례 소요시간은 실제 파일럿으로 확인해야 합니다.

## 구성
- respondent/cards: 사례 A~O 재무카드 15장과 행동 설명카드 1장
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
