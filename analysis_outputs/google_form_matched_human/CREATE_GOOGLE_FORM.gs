// Google Apps Script — generated survey skeleton
// 1) Upload all PNG files in the cards folder to Google Drive.
// 2) Replace CARD_FILE_IDS values below with the corresponding Drive file IDs.
// 3) Run createMatchedHumanSurvey() in script.google.com.
// Apps Script Forms supports ImageItem.setImage(BlobSource).

const CARD_FILE_IDS = {
  "metric1": "PUT_DRIVE_FILE_ID_FOR_00_metric_guide_1_png",
  "metric2": "PUT_DRIVE_FILE_ID_FOR_00_metric_guide_2_png",
  "actions": "PUT_DRIVE_FILE_ID_FOR_01_action_catalog_png",
  "A": "PUT_DRIVE_FILE_ID_FOR_case_A_png",
  "B": "PUT_DRIVE_FILE_ID_FOR_case_B_png",
  "C": "PUT_DRIVE_FILE_ID_FOR_case_C_png",
  "D": "PUT_DRIVE_FILE_ID_FOR_case_D_png",
  "E": "PUT_DRIVE_FILE_ID_FOR_case_E_png",
  "F": "PUT_DRIVE_FILE_ID_FOR_case_F_png",
  "G": "PUT_DRIVE_FILE_ID_FOR_case_G_png",
  "H": "PUT_DRIVE_FILE_ID_FOR_case_H_png",
  "I": "PUT_DRIVE_FILE_ID_FOR_case_I_png"
};

const ACTION_OPTIONS = ["A0 — 현 상태 유지", "DL — 부채 상환", "RF — 차환", "CX — 성장 CAPEX 축소", "WC1 — 운전자본 회수 개선", "WC2 — 공급자금융 활용", "OE — 비용 효율화", "MX1 — 부채상환 + 비용효율화", "MX2 — 부채상환 + 운전자본 개선"];
const CASE_ALIASES = ["A", "B", "C", "D", "E", "F", "G", "H", "I"];

function addDriveImage(form, key, title) {
  const blob = DriveApp.getFileById(CARD_FILE_IDS[key]).getBlob();
  form.addImageItem().setTitle(title).setImage(blob).setWidth(700);
}

function createMatchedHumanSurvey() {
  const form = FormApp.create('기업 신용상태 개선을 위한 재무행동 판단 연구');
  form.setDescription(
    '2024년 재무정보·시장·산업정보만을 이용해 향후 약 1년의 재무건전성·신용상태 개선을 위한 관리행동을 판단하는 연구입니다. ' +
    '기업명은 제공하지 않으며 외부 검색이나 데이터 조회는 하지 마십시오.'
  );
  form.setConfirmationMessage('응답해 주셔서 감사합니다.');

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
  addDriveImage(form, 'metric1', '재무지표 읽는 법 1/2');
  addDriveImage(form, 'metric2', '재무지표 읽는 법 2/2');
  addDriveImage(form, 'actions', '9개 표준 관리행동');
  form.addSectionHeaderItem().setTitle('유의사항').setHelpText(
    '각 사례에서 9개 후보 중 하나만 선택하십시오. 정보 없음은 0이 아닙니다. 기업을 추정하더라도 외부 검색이나 기억에 의존한 구체적 사건·수치를 추가하지 마십시오.'
  );

  CASE_ALIASES.forEach(alias => {
    form.addPageBreakItem().setTitle('Case ' + alias);
    addDriveImage(form, alias, 'Case ' + alias + ' 재무정보');
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
  });

  form.addPageBreakItem().setTitle('정보 충분성 및 오염 점검');
  form.addCheckboxItem().setTitle('실제 기업 신용개선 권고를 내린다면 추가로 확인하고 싶은 정보를 모두 선택해 주십시오.')
    .setChoiceValues(['구체적인 차입금 만기구조 및 금리','향후 투자계획 및 CAPEX 계획','사업부문별 수익성','경영진의 사업계획','영업현금흐름 전망','산업 전망 및 경쟁상황','담보·보증 및 자금조달 가능성','신용평가사의 정성적 평가요소','기업명 및 과거 사업이력','기타']);
  form.addCheckboxItem().setTitle('실제 기업이 어떤 회사인지 알아보았거나 강하게 추정한 사례가 있습니까?')
    .setChoiceValues(['없음'].concat(CASE_ALIASES.map(x => 'Case ' + x)));
  form.addMultipleChoiceItem().setTitle('응답 과정에서 인터넷 검색, 외부 데이터 조회 또는 생성형 AI 도구를 사용했습니까?')
    .setChoiceValues(['아니오','예']).setRequired(true);
  form.addParagraphTextItem().setTitle('9개 표준 행동으로는 충분히 표현하기 어렵다고 느낀 사례가 있다면 Case와 원하는 행동을 적어 주십시오.');
  form.addParagraphTextItem().setTitle('설문 판단 과정에서 어렵거나 애매했던 점이 있다면 자유롭게 작성해 주십시오.');

  Logger.log('Edit URL: ' + form.getEditUrl());
  Logger.log('Responder URL: ' + form.getPublishedUrl());
}
