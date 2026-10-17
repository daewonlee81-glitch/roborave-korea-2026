#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RoboRAVE Taiwan Open 2026 · 초청장 발급용 명단(roster.js) 생성기

사용법:
  python3 make_roster.py participants.csv            # → roster.js (같은 폴더)
  python3 make_roster.py participants.csv -o roster.js

participants.csv (UTF-8, 엑셀에서 'CSV UTF-8'로 저장) 열:
  name_kr   성명(국문)            * 필수 — 조회 키
  birth     생년월일 YYYY-MM-DD   * 필수 — 조회 키
  name_en   여권상 영문 성명      (선택) 예: LEE YEON SOO
  gender    M / F                 (선택)
  school    학교·소속             (선택, 발급 시 참가자가 직접 입력 가능)
  grade     학년/반               (선택, 비우면 생년월일로 자동 계산)
  team      팀명                  (선택)
  event     참가 종목             (선택)
  role      참가 자격             (선택, 기본 '선수 (Student Competitor)')
  adult     1 이면 인솔자·보호자 → 학교 제출용 문서 발급 안 함
  passport  여권번호              (선택, 입국 참고용 문서에 기본값으로 사용)
  depart    대만 입국 예정일      (선택, 기본 2026-12-11)
  ret       대만 출국 예정일      (선택, 기본 2026-12-14)
  stay      체류 예정지           (선택)
  doc_no    문서번호              (선택, 비우면 RRK-TW2026-0001 부터 순번)

* 원본 CSV에는 개인정보가 있으므로 절대 깃허브에 올리지 마세요. roster.js 만 올립니다.
* 같은 사람을 다시 생성해도 문서번호·확인코드가 유지되도록, 이전 roster.js 가 있으면 번호를 이어받습니다.
"""
import base64, csv, hashlib, json, os, re, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 150000
PREFIX = "RRK-TW2026-"
EVENT = {
  "kr": "RoboRAVE Taiwan Open 2026",
  "en": "RoboRAVE Taiwan Open 2026",
  "start": "2026-12-12", "end": "2026-12-13",
  "venue": "국립중앙대학교 이런관 (National Central University, Yiren Hall)",
  "addr": "No. 300, Zhongda Rd., Zhongli District, Taoyuan City 320317, Taiwan",
  "city_kr": "대만 타오위안", "city_en": "Taoyuan, Taiwan",
  "country_kr": "대만", "country_en": "Taiwan",
  "badge": "TAIWAN OPEN 2026", "badge_sub": "TAOYUAN, TAIWAN",
  "organizer": "RoboRAVE Taiwan · 국립중앙대학교 (National Central University)",
  "note": "12/12(토) 11:00 개시 · 12/13(일) 16:00 종료",
  "depart": "2026-12-11", "ret": "2026-12-14",
  "stay": "타오위안 중리(中壢) 지역 호텔 (Zhongli District, Taoyuan, Taiwan)",
  "org1": "로보레이브 코리아", "org2": "국제로봇교육협의회", "signer": "국제로봇교육협의회장",
  "base": "https://roborave-korea.co.kr/invitation/taiwan-2026/",
}

def norm_name(s): return re.sub(r"\s+", "", s or "").lower()
def sha16(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
def b64(b): return base64.b64encode(b).decode()

def derive(pw, salt):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode("utf-8"))

def enc(obj, pw, salt):
    key = derive(pw, salt); iv = secrets.token_bytes(12)
    ct = AESGCM(key).encrypt(iv, json.dumps(obj, ensure_ascii=False).encode("utf-8"), None)
    return b64(iv + ct)

def mask(name):
    n = name.strip()
    if len(n) <= 2: return n[0] + "*"
    return n[0] + "*" * (len(n) - 2) + n[-1]

def gender_kr(g):
    g = (g or "").strip().upper()
    return {"M": "남 (M)", "F": "여 (F)", "남": "남 (M)", "여": "여 (F)"}.get(g, g)

def load_prev(path):
    """이전 roster.js 에서 idx→(doc_no, key) 를 읽어 번호를 이어받는다."""
    if not os.path.exists(path): return {}, 0
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"window\.ROSTER=(\{.*\});?\s*$", txt, re.S)
    if not m: return {}, 0
    d = json.loads(m.group(1)); prev = {}; mx = 0
    for r in d.get("records", []):
        prev[r["i"]] = (r["n"], r["k"])
        mm = re.search(r"(\d+)$", r["n"])
        if mm: mx = max(mx, int(mm.group(1)))
    return prev, mx

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"): print(__doc__); sys.exit(0)
    src = args[0]
    out = args[args.index("-o") + 1] if "-o" in args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "roster.js")
    prev, seq = load_prev(out)
    salt = secrets.token_bytes(16)
    records, verify, seen, skipped = [], [], set(), []
    with open(src, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            row = {k.strip(): (v or "").strip() for k, v in row.items() if k}
            name, birth = row.get("name_kr", ""), row.get("birth", "")
            if not name: continue
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", birth):
                skipped.append(f"{name}: 생년월일 형식 오류 '{birth}' (YYYY-MM-DD 필요)"); continue
            pw = norm_name(name) + "|" + birth
            idx = sha16(pw)
            if idx in seen: skipped.append(f"{name} {birth}: 중복 행 — 두 번째 행 무시"); continue
            seen.add(idx)
            if row.get("doc_no"): no, key = row["doc_no"], None
            elif idx in prev: no, key = prev[idx]
            else: seq += 1; no, key = f"{PREFIX}{seq:04d}", None
            if not key:
                key = "".join(secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(8))
            adult = row.get("adult", "") in ("1", "y", "Y", "true", "TRUE")
            person = {
                "nameKr": name, "nameEn": row.get("name_en", ""), "birth": birth,
                "gender": gender_kr(row.get("gender")), "school": row.get("school", ""),
                "grade": row.get("grade", ""), "team": row.get("team", ""), "event": row.get("event", ""),
                "role": row.get("role", "") or ("인솔자 · 보호자 (Chaperone / Guardian)" if adult else "선수 (Student Competitor)"),
                "adult": adult, "nationality": "대한민국 (Republic of Korea)",
                "passport": row.get("passport", ""), "depart": row.get("depart", "") or EVENT["depart"],
                "ret": row.get("ret", "") or EVENT["ret"], "stay": row.get("stay", "") or EVENT["stay"],
            }
            records.append({"i": idx, "n": no, "k": key, "d": enc(person, pw, salt)})
            vpw = no + "|" + key
            verify.append({"h": sha16(vpw), "d": enc({"name": mask(name), "school": row.get("school", ""),
                                                      "team": row.get("team", ""), "event": row.get("event", "")}, vpw, salt)})
    data = {"v": 1, "iter": ITER, "salt": b64(salt), "event": EVENT, "records": records, "verify": verify}
    with open(out, "w", encoding="utf-8") as f:
        f.write("/* RoboRAVE Korea · Taiwan Open 2026 초청장 명단 (암호화됨) — make_roster.py 로 자동 생성, 직접 수정하지 마세요 */\n")
        f.write("window.ROSTER=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"OK  {len(records)}명 → {out}")
    for s in skipped: print("SKIP", s)

if __name__ == "__main__":
    main()
