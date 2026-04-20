# RoboRAVE Korea — 공식 홈페이지

> **A Collaborative Robotics Program**
> 국제 로봇경진대회 RoboRAVE의 한국 공식 운영 기관 홈페이지.

## 개요

- **도메인**: [roborave-korea.co.kr](https://roborave-korea.co.kr)
- **공식 블로그**: [blog.naver.com/robot-league](https://blog.naver.com/robot-league)
- **이메일**: robot-league@naver.com
- **출범**: 2026년

RoboRAVE는 전 세계 60개국 6,000여 팀이 참가하는 국제 로봇경진대회이며,
RoboRAVE Korea는 국내 대회 운영과 국가대표 선발을 담당합니다.

## 파일 구조

```
.
├── index.html    # 단일 페이지 홈페이지 (HTML + CSS + JS 포함)
└── README.md
```

정적 HTML 한 파일로 구성되어 있어 별도 빌드 과정이 필요 없습니다.

## 로컬에서 미리보기

브라우저로 `index.html`을 열거나, 간단한 로컬 서버를 띄우면 됩니다.

```bash
# Python이 설치되어 있다면
python3 -m http.server 8000
# 이후 브라우저에서 http://localhost:8000 접속
```

## 배포

### GitHub Pages (무료)

1. 리포 **Settings → Pages** 로 이동
2. **Source**: `Deploy from a branch` 선택
3. **Branch**: `main` / `/ (root)` 선택 후 Save
4. 몇 분 뒤 `https://daewonlee81-glitch.github.io/RoboRAVE-Korea-WEP/` 로 접속 가능
5. 커스텀 도메인 연결: Pages 설정의 **Custom domain** 에 `roborave-korea.co.kr` 입력
6. 가비아 DNS에 아래 레코드 추가
   - `A` 레코드 4개: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` (www): `daewonlee81-glitch.github.io`

### Cloudflare Pages / Netlify / Vercel

이 리포를 연결(Connect Git) 하면 main 브랜치 커밋 시 자동 배포됩니다.

## 디자인 가이드

로고 색상과 통일된 팔레트를 사용합니다.

| 용도 | HEX | 설명 |
|---|---|---|
| Brand | `#C8102E` | 로고의 크림슨 레드 |
| Brand Dark | `#A00C20` | 호버/진한 강조 |
| Ink | `#0a0a0a` | 로고의 블랙 (본문 텍스트) |
| BG Soft | `#faf7f7` | 섹션 배경 |
| Line | `#ececec` | 구분선 |

## 수정 방법

`index.html` 파일을 직접 편집해서 커밋/푸시하면 됩니다.
주요 수정 포인트:

- 히어로 카피: `<section class="hero">` 내부
- 통계 숫자: `.stats` 블록
- 프로그램 카드 3개: `.cards` 블록
- 연락처 / 블로그: `.contact-info` 블록

## 라이선스

© 2026 RoboRAVE Korea. All rights reserved.
