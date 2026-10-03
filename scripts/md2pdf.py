#!/usr/bin/env python3
"""학습자료 마크다운을 출력용 A4 PDF로 변환.

usage: python scripts/md2pdf.py materials/easy-guide.md   -> materials/easy-guide.pdf
requires: pip install weasyprint markdown
"""
import html
import re
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

CSS = """
@page { size: A4; margin: 17mm 16mm 18mm;
  @bottom-left { content: string(chap); font-family: 'Noto Sans CJK KR'; font-size: 8pt; color: #888; }
  @bottom-right { content: counter(page); font-family: 'Noto Sans CJK KR'; font-size: 8pt; color: #888; } }
@page :first { @bottom-left { content: none; } }
body { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 10pt; line-height: 1.6; color: #1a1a1a; }
h1 { font-size: 24pt; margin: 30mm 0 6pt; border-bottom: 3px solid #c2410c; padding-bottom: 6pt; }
h2 { font-size: 15pt; color: #fff; background: #1f2937; padding: 6pt 10pt; border-radius: 4pt;
     margin: 0 0 10pt; break-before: page; string-set: chap content(); }
h2.first { break-before: auto; margin-top: 14pt; }
h3 { font-size: 11.5pt; color: #c2410c; margin: 14pt 0 4pt; border-left: 4px solid #c2410c; padding-left: 6pt;
     break-after: avoid; }
p { margin: 4pt 0 6pt; }
ul, ol { margin: 3pt 0 6pt; padding-left: 16pt; }
li { margin: 1.5pt 0; }
li.task { list-style: none; margin-left: -14pt; }
.box { display: inline-block; width: 9pt; height: 9pt; border: 1.2px solid #444; margin-right: 6pt; vertical-align: -1pt; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; background: #fff7ed; border-left: 4px solid #fdba74; color: #444; font-size: 9pt; }
blockquote p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9pt; break-inside: avoid; }
th { background: #f3f4f6; font-weight: 700; }
th, td { border: 1px solid #c8c8c8; padding: 4pt 6pt; vertical-align: top; text-align: left; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; background: #f1f1f1; padding: 0 2pt; border-radius: 2pt; }
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 6pt 8pt; border-radius: 3pt; font-size: 8.5pt; white-space: pre-wrap; }
pre code { background: none; padding: 0; }
hr { display: none; }
strong { color: #111; }
"""


def build(path):
    path = Path(path)
    md = path.read_text(encoding="utf-8")
    # python-markdown은 목록 앞에 빈 줄이 없으면 목록으로 인식하지 않으므로 보정
    md = re.sub(r"(?m)^((?![-*\d]|\s|\|)[^\n]+)\n(?=(- |\d+\. ))", r"\1\n\n", md)
    body = markdown.markdown(md, extensions=["tables", "fenced_code"])
    body = re.sub(r"<li>\[ \]\s*", '<li class="task"><span class="box"></span>', body)
    body = body.replace("<h2>", '<h2 class="first">', 1)
    title = re.search(r"^# (.+)$", md, re.M).group(1)
    doc = (f"<html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
           f"<style>{CSS}</style></head><body>{body}</body></html>")
    out = path.with_suffix(".pdf")
    HTML(string=doc).write_pdf(out)
    return out


if __name__ == "__main__":
    print(build(sys.argv[1]))
