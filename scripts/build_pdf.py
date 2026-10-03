#!/usr/bin/env python3
"""회차 문제지(quiz.md)를 출력용 PDF로 변환.

usage: python scripts/build_pdf.py exercises/session-00-diagnostic/quiz.md
  -> 같은 폴더에 quiz.pdf 생성 (문항별 답/확신도 기입란 + 마지막 장 답안표)
requires: pip install weasyprint markdown
"""
import html
import re
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

CSS = """
@page { size: A4; margin: 16mm 16mm 18mm;
  @bottom-left { content: "%(title)s"; font-family: 'Noto Sans CJK KR'; font-size: 8pt; color: #888; }
  @bottom-right { content: counter(page) " / " counter(pages); font-family: 'Noto Sans CJK KR'; font-size: 8pt; color: #888; } }
body { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 10pt; line-height: 1.45; color: #111; }
h1 { font-size: 16pt; margin: 0 0 4pt; border-bottom: 2px solid #111; padding-bottom: 4pt; }
.meta { font-size: 9pt; margin: 8pt 0 8pt; white-space: nowrap; }
.meta span { border-bottom: 1px solid #999; width: 80pt; display: inline-block; margin: 0 14pt 0 4pt; }
.intro { font-size: 9pt; color: #333; background: #f3f3f3; padding: 6pt 8pt; border-radius: 3pt; }
.intro p { margin: 2pt 0; }
.q { break-inside: avoid; border: 1px solid #bbb; border-radius: 4pt; padding: 7pt 9pt 6pt; margin: 9pt 0; }
.qh { font-weight: 700; font-size: 10.5pt; margin-bottom: 3pt; }
.multi { font-weight: 700; color: #b00; font-size: 9pt; margin-left: 4pt; }
.q p { margin: 2pt 0 4pt; }
.q ul { list-style: none; padding-left: 4pt; margin: 3pt 0; }
.q li { margin: 2.5pt 0; padding-left: 18pt; text-indent: -18pt; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.6pt; background: #eee; padding: 0 2pt; }
.fill { display: flex; justify-content: space-between; border-top: 1px dashed #bbb; margin-top: 5pt; padding-top: 4pt; font-size: 9pt; }
.box { display: inline-block; width: 60pt; border-bottom: 1px solid #333; }
.conf span { display: inline-block; width: 13pt; height: 13pt; border: 1px solid #555; border-radius: 50%%;
  text-align: center; line-height: 12pt; font-size: 8pt; margin-left: 3pt; }
.notes { height: 20pt; border: 1px dotted #ccc; margin-top: 4pt; font-size: 7.5pt; color: #aaa; padding: 2pt 4pt; }
.sheet { break-before: page; }
table { border-collapse: collapse; width: 100%%; font-size: 9.5pt; }
th, td { border: 1px solid #999; padding: 4pt 5pt; text-align: center; }
th { background: #eee; }
td.l { text-align: left; }
.bub span { display: inline-block; width: 14pt; height: 14pt; border: 1px solid #555; border-radius: 50%%;
  line-height: 13pt; font-size: 8pt; margin: 0 1.5pt; }
"""


def inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def parse(md):
    head, *qs = re.split(r"^### ", md, flags=re.M)
    title = re.search(r"^# (.+)$", head, re.M).group(1)
    intro = re.sub(r"^# .+$", "", head, flags=re.M).replace("---", "").strip()
    items = []
    for block in qs:
        block = block.replace("\n---", "").strip()
        first, rest = block.split("\n", 1)
        qid = first.split()[0]
        multi = "(Choose" in first
        stem, opts = [], []
        for line in rest.strip().splitlines():
            m = re.match(r"- ([A-E])\. (.+)", line.strip())
            if m:
                opts.append(m.groups())
            elif line.strip():
                stem.append(line.strip())
        items.append(dict(id=qid, multi=multi, label=first[len(qid):].strip(), stem=" ".join(stem), opts=opts))
    return title, intro, items


def build(path):
    path = Path(path)
    title, intro, items = parse(path.read_text(encoding="utf-8"))
    out = [f"<h1>{inline(title)}</h1>",
           '<div class="meta">날짜 <span></span> 시작 <span></span> 종료 <span></span> 점수 <span></span></div>',
           f'<div class="intro">{markdown.markdown(intro)}</div>']
    conf = '<span class="conf">확신도' + "".join(f"<span>{i}</span>" for i in range(1, 6)) + "</span>"
    for q in items:
        multi = f'<span class="multi">{inline(q["label"])}</span>' if q["multi"] else ""
        opts = "".join(f"<li><b>{k}.</b>&nbsp; {inline(v)}</li>" for k, v in q["opts"])
        out.append(f'<div class="q"><div class="qh">{q["id"]}{multi}</div><p>{inline(q["stem"])}</p>'
                   f'<ul>{opts}</ul><div class="fill"><span>내 답 <span class="box"></span></span>{conf}</div>'
                   f'<div class="notes">판단 근거 메모</div></div>')
    rows = []
    for q in items:
        bub = "".join(f"<span>{k}</span>" for k, _ in q["opts"])
        rows.append(f'<tr><td>{q["id"]}{" ★" if q["multi"] else ""}</td><td class="bub">{bub}</td>'
                    f'<td class="bub">' + "".join(f"<span>{i}</span>" for i in range(1, 6)) + "</td><td></td></tr>")
    out.append('<div class="sheet"><h1>답안표</h1><p style="font-size:9pt">★ = 복수 정답(2개). '
               '다 푼 뒤 이 표를 보고 <code>results/</code> 답안지를 채우거나 채팅으로 전달.</p>'
               '<table><tr><th>문항</th><th>답</th><th>확신도</th><th>O/X</th></tr>' + "".join(rows) + "</table></div>")
    doc = f"<html><head><meta charset='utf-8'><style>{CSS % {'title': html.escape(title)}}</style></head><body>{''.join(out)}</body></html>"
    pdf = path.with_suffix(".pdf")
    HTML(string=doc).write_pdf(pdf)
    return pdf


if __name__ == "__main__":
    print(build(sys.argv[1]))
