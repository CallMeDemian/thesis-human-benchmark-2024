/* Human-15 Google Forms builder. Generated data replaces the marker below.
 * Paste the generated CREATE_GOOGLE_FORM.gs into a standalone Apps Script project.
 * Run createHuman15Survey(). No respondent data is sent to GitHub.
 * A draft (unpublished) Form and a private response spreadsheet are created.
 */
const SURVEY = __DATA_JSON__;
const SETTINGS = {
  order: 'FORWARD', // Optional second version: REVERSE. Each person completes only one.
  researcherContact: '', // Before publishing, enter your research contact details here or in the Form.
  useImages: true // false builds a native-text equivalent if GitHub image retrieval is blocked.
};
function hexSha256(bytes) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, bytes)
    .map(function(x) { return ('0' + ((x + 256) % 256).toString(16)).slice(-2); }).join('');
}
function preparedImages() {
  if (!SETTINGS.useImages) return {};
  const entries = SURVEY.images;
  const replies = UrlFetchApp.fetchAll(entries.map(function(e) {
    return {url: SURVEY.assetBase + e.file, muteHttpExceptions: true, followRedirects: true};
  }));
  const result = {};
  entries.forEach(function(e, i) {
    const reply = replies[i];
    if (reply.getResponseCode() !== 200) throw new Error('Image retrieval failed: ' + e.file + '. No form was created. Set useImages=false for native text.');
    if (hexSha256(reply.getBlob().getBytes()) !== e.sha256) throw new Error('Image version mismatch: ' + e.file + '. Use the complete matching package, or set useImages=false.');
    result[e.file] = reply.getBlob().setContentType('image/png').setName(e.file);
  });
  return result;
}
function createHuman15Survey() {
  if (SETTINGS.order !== 'FORWARD' && SETTINGS.order !== 'REVERSE') throw new Error('order must be FORWARD or REVERSE');
  const blobs = preparedImages(); // Fail before creating a partial Form if any asset is unavailable.
  const props = PropertiesService.getScriptProperties();
  const idKey = 'H15_FORM_' + SURVEY.buildId + '_' + SETTINGS.order + '_' + SETTINGS.useImages;
  const previous = props.getProperty(idKey);
  if (previous) {
    Logger.log('Existing draft: ' + FormApp.openById(previous).getEditUrl());
    return;
  }
  const form = FormApp.create(SURVEY.title + ' [H15-v1 ' + SETTINGS.order + ']', false);
  form.setCollectEmail(false).setLimitOneResponsePerUser(false).setPublishingSummary(false);
  form.setProgressBar(true).setShuffleQuestions(false).setShowLinkToRespondAgain(false);
  form.setIsQuiz(false).setAllowResponseEdits(false);
  const contact = SETTINGS.researcherContact.trim();
  form.setDescription(SURVEY.intro + (contact ? '\n\n연구 문의: ' + contact : '\n\n[배포 전 연구자 확인: 연구 문의처와 필요한 참여 안내를 입력하십시오.]'));
  form.setConfirmationMessage('응답해 주셔서 감사합니다.');
  const sheet = SpreadsheetApp.create('기업 재무행동 설문 응답 H15-v1 ' + SETTINGS.order);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());
  const consent = form.addMultipleChoiceItem().setTitle('연구 설명을 읽었으며 자발적으로 참여에 동의합니다.').setRequired(true);
  consent.setChoices([
    consent.createChoice('동의합니다', FormApp.PageNavigationType.CONTINUE),
    consent.createChoice('동의하지 않습니다', FormApp.PageNavigationType.SUBMIT)
  ]);
  form.addPageBreakItem().setTitle('응답자 배경');
  form.addCheckboxItem().setTitle('현재 또는 과거에 경험한 업무를 선택해 주십시오.').setChoiceValues(SURVEY.backgroundRoles).setRequired(true);
  form.addMultipleChoiceItem().setTitle('기업 재무·신용분석 관련 실무 또는 연구 경험').setChoiceValues(SURVEY.experience).setRequired(true);
  form.addScaleItem().setTitle('기업의 재무상태·신용도 평가에 얼마나 익숙합니까?').setBounds(1,5).setLabels('경험이 거의 없음','매우 익숙함').setRequired(true);
  form.addPageBreakItem().setTitle('판단 방법');
  form.addSectionHeaderItem().setTitle('공통 안내').setHelpText(SURVEY.rules);
  form.addSectionHeaderItem().setTitle('행동별 의미와 강도').setHelpText(SURVEY.actions.join('\n\n'));
  form.addSectionHeaderItem().setTitle('재무지표 정의').setHelpText(SURVEY.dictionary);
  let cases = SURVEY.cases.slice();
  if (SETTINGS.order === 'REVERSE') cases.reverse();
  cases.forEach(function(c, index) {
    form.addPageBreakItem().setTitle('사례 ' + c.alias + ' (' + (index+1) + '/' + cases.length + ')');
    if (SETTINGS.useImages) {
      form.addImageItem().setTitle('사례 ' + c.alias + ' — 재무정보').setImage(blobs['case_' + c.alias + '.png']).setWidth(700);
    } else {
      c.groups.forEach(function(g) { form.addSectionHeaderItem().setTitle(g.title).setHelpText(g.lines.join('\n')); });
    }
    form.addMultipleChoiceItem().setTitle('[' + c.alias + '] 향후 약 1년의 재무건전성 개선을 위해 우선적으로 권고할 행동 하나를 선택해 주십시오.')
      .setHelpText('표시된 수치는 읽기 쉽게 반올림한 표준 프로그램입니다. 후보를 수정하거나 서로 결합하지 마십시오.')
      .setChoiceValues(SURVEY.actions).setRequired(true);
    form.addScaleItem().setTitle('[' + c.alias + '] 선택에 대한 확신 정도').setBounds(1,5).setLabels('매우 불확실','매우 확신').setRequired(true);
    form.addParagraphTextItem().setTitle('[' + c.alias + '] 선택 이유').setHelpText('핵심 재무상태와 고려한 상충관계를 1~3문장으로 적어 주십시오. 이름·기관명 등 개인정보는 적지 마십시오.').setRequired(true);
  });
  form.addPageBreakItem().setTitle('마지막 확인');
  form.addCheckboxItem().setTitle('실무에서 추가로 확인하고 싶은 정보').setChoiceValues(SURVEY.additionalInformation);
  form.addCheckboxItem().setTitle('실제 기업을 알아보았거나 강하게 추정한 사례').setHelpText('해당하는 사례만 선택하십시오. 없으면 선택하지 않아도 됩니다.').setChoiceValues(SURVEY.cases.map(function(c) { return '사례 ' + c.alias; }));
  form.addMultipleChoiceItem().setTitle('응답 중 인터넷 검색·외부 데이터 조회·생성형 AI를 사용했습니까?').setChoiceValues(['아니오','예']).setRequired(true);
  form.addParagraphTextItem().setTitle('선택지에 없는 행동을 권고하고 싶었다면 사례와 내용을 적어 주십시오.');
  form.addParagraphTextItem().setTitle('판단하기 어렵거나 불명확했던 점');
  props.setProperty(idKey, form.getId());
  Logger.log('Draft edit URL: ' + form.getEditUrl());
  Logger.log('Responder URL (publish after review): ' + form.getPublishedUrl());
  Logger.log('Response sheet: ' + sheet.getUrl());
  Logger.log('Created unpublished draft. Verify consent/contact, preview, and respondent access before publishing.');
}
