# 초청장 발급 (roborave-korea.co.kr/invitation/taiwan-2026/)

RoboRAVE Taiwan Open 2026 한국 참가단용 초청장 발급 페이지. `/invitation/`(오사카 2026)과 같은 구조입니다.

- `index.html` — 성명+생년월일 조회 → 문서 생성(인쇄/PDF 저장) → 하단 QR로 진위 확인
  - 학교 제출용: 참가 확인 및 출석인정 협조 요청서 (학생만)
  - 대만 입국 참고용: 참가 초청 확인서 (국·영문, 여권번호·체류기간 포함 / 인솔자·보호자도 발급 가능)
- `roster.js` — 암호화된 참가자 명단 (**`make_roster.py`로 생성, 직접 편집 금지**)
- `make_roster.py` — 명단 생성기
- 직인·QR 라이브러리는 `/certificate/seal.png`, `/certificate/qrcode.min.js`를 공용으로 씁니다.

## 명단 추가·갱신 방법

1. `participants.csv`(개인정보 포함 — **깃허브에 올리지 말 것**)를 엑셀에서 편집 후 *CSV UTF-8*로 저장
   열: `name_kr, birth(YYYY-MM-DD), name_en, gender(M/F), school, grade, team, event, role, adult(1=인솔자·보호자), passport, depart, ret, stay, doc_no`
   필수는 `name_kr`, `birth` 두 개뿐이며 나머지는 비워도 됩니다(발급 시 참가자가 입력).
2. 이 폴더에서 실행 (Python 3 + `pip install cryptography`)
   ```bash
   python3 make_roster.py participants.csv
   ```
   기존 `roster.js`가 있으면 같은 사람의 문서번호·확인코드를 그대로 이어받습니다(이미 발급된 문서의 QR 진위확인 유지).
3. 생성된 `roster.js`만 커밋/업로드

## 조회 방식·보안
- 참가자 레코드는 `성명+생년월일`을 키로 PBKDF2(15만회)+AES-GCM 으로 암호화되어 있어, 본인 정보 없이는 명단을 열람할 수 없습니다.
- 발급 시 입력한 학교명·여권정보는 브라우저 안에서만 쓰이며 서버로 전송되지 않습니다.
- 문서번호 규칙: `RRK-TW2026-0001` 부터 순번.
