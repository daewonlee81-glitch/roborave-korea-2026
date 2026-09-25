# 수상실적증명 발급 (roborave-korea.co.kr/certificate/)

worldrobotleague.net/certificate/ 와 같은 구조의 정적 페이지입니다.

- `index.html` — 조회(성명+학교명) → 국문/영문 증명서 출력(인쇄/PDF 저장), 발급번호·QR 진위 확인
- `awards.csv` — 수상 데이터 (엑셀에서 편집 후 **CSV UTF-8** 로 저장)
- `seal.png` — IREA 직인, `qrcode.min.js` — QR 생성

## 데이터 추가
`awards.csv` 에 한 줄씩 추가합니다. 수상자 1명당 1행, `cert_no` 는 고유해야 합니다.
- 발급번호 규칙: `RK26-종목코드-순번` (Korea Open 2026), `RO26-종목코드-순번` (오사카 2026)
- `birth` 칸을 채우면 해당 행은 학교명 대신 생년월일(YYYY-MM-DD)로도 조회됩니다.
- `name_en`, `school_en` 을 채우면 영문 증명서에 영문으로 표시됩니다(비우면 한글 표시).
