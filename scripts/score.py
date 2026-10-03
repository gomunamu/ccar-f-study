#!/usr/bin/env python3
"""회차 채점 + 숙련도 갱신.

usage: python scripts/score.py 00
  reads  keys/session-00.yaml, results/session-00.yaml, concepts.yaml, mastery.json
  writes results/session-00-report.md, mastery.json
"""
import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALPHA = 0.4  # 개념 숙련도 EMA 가중치 (최근 결과 반영 비율)
PRIOR = 0.5  # 처음 보는 개념의 초기 숙련도


def load_yaml(p):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def norm(ans):
    return "".join(sorted(str(ans or "").upper().replace(",", "").replace(" ", "")))


def main(sid):
    concepts = load_yaml(ROOT / "concepts.yaml")["domains"]
    key = load_yaml(ROOT / f"keys/session-{sid}.yaml")["questions"]
    sub = load_yaml(ROOT / f"results/session-{sid}.yaml")
    answers = sub.get("answers", {})
    mpath = ROOT / "mastery.json"
    mastery = json.loads(mpath.read_text()) if mpath.exists() else {"sessions": [], "concepts": {}}

    rows, by_domain = [], {}
    for qid, k in key.items():
        a = answers.get(qid, {}) or {}
        given, correct = norm(a.get("answer")), norm("".join(k["answer"]))
        ok = given == correct and given != ""
        conf = a.get("confidence") or 0
        dom = k["concepts"][0].split(".")[0]
        by_domain.setdefault(dom, []).append(ok)
        rows.append((qid, dom, k["concepts"], given or "-", correct, ok, conf, k["why"]))
        for c in k["concepts"]:
            m = mastery["concepts"].setdefault(c, {"attempts": 0, "correct": 0, "p": PRIOR, "last_seen": None})
            m["attempts"] += 1
            m["correct"] += int(ok)
            m["p"] = round((1 - ALPHA) * m["p"] + ALPHA * (1.0 if ok else 0.0), 3)
            m["last_seen"] = sid

    total_ok = sum(r[5] for r in rows)
    dom_acc = {d: sum(v) / len(v) for d, v in by_domain.items()}
    est = sum(concepts[d]["weight"] * dom_acc.get(d, 0) for d in concepts) / sum(
        concepts[d]["weight"] for d in concepts if d in dom_acc) * 1000
    mastery["sessions"].append({"session": sid, "date": sub.get("date") or str(date.today()),
                                "score": f"{total_ok}/{len(rows)}",
                                "domain_acc": {d: round(v, 2) for d, v in dom_acc.items()},
                                "weighted_estimate": round(est)})
    mpath.write_text(json.dumps(mastery, ensure_ascii=False, indent=2), encoding="utf-8")

    misconceptions = [r for r in rows if not r[5] and r[6] >= 4]
    lucky = [r for r in rows if r[5] and 0 < r[6] <= 2]
    weak = sorted(dom_acc.items(), key=lambda x: x[1])

    out = [f"# Session {sid} Report", "",
           f"- 점수: **{total_ok}/{len(rows)}** ({total_ok / len(rows):.0%})",
           f"- 도메인 비중 가중 추정치: **{est:.0f} / 1000** (합격선 720, 참고용)", "",
           "## 도메인별", "", "| 도메인 | 정답률 | 비중 |", "|---|---|---|"]
    for d, acc in weak:
        out.append(f"| {d} {concepts[d]['name']} | {acc:.0%} ({sum(by_domain[d])}/{len(by_domain[d])}) | {concepts[d]['weight']:.0%} |")
    out += ["", "## 확신했는데 틀림 (최우선 복습 — 오개념)", ""]
    out += [f"- {r[0]} `{', '.join(r[2])}` 내 답 {r[3]} → 정답 {r[4]}: {r[7]}" for r in misconceptions] or ["- 없음"]
    out += ["", "## 맞았지만 찍음 (복습 필요)", ""]
    out += [f"- {r[0]} `{', '.join(r[2])}`: {r[7]}" for r in lucky] or ["- 없음"]
    out += ["", "## 전체 문항", "", "| Q | 개념 | 내 답 | 정답 | 확신 | 결과 |", "|---|---|---|---|---|---|"]
    out += [f"| {r[0]} | {', '.join(r[2])} | {r[3]} | {r[4]} | {r[6] or '-'} | {'O' if r[5] else 'X'} |" for r in rows]
    out += ["", "## 오답 해설", ""]
    out += [f"- **{r[0]}** ({r[4]}) {r[7]}" for r in rows if not r[5]] or ["- 없음"]
    rp = ROOT / f"results/session-{sid}-report.md"
    rp.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(rp.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "00")
