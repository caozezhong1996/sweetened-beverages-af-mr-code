# -*- coding: utf-8 -*-
"""One-shot renumber for v4.5.6: insert position for new ref 7 (AHA 2026
scientific statement). Every existing citation/ref numbered >= 7 becomes n+1.

Rules:
  - Only lines containing 'T`' (docx text template lines) are touched, so JS
    code arrays like [2350, 2850, ...] or T2.header[0] are never matched.
  - Citation groups [n], [n,m] -> each number n>=7 incremented.
  - Reference-list leading numbers 'T`N. ' with N>=7 incremented.
The new ref 7 line and new [7] citations are inserted AFTER this script runs.
"""
import re
import sys

PATH = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_manuscript_v45.js"

src = open(PATH, encoding="utf-8").read()
lines = src.split("\n")

cite_re = re.compile(r"\[(\d{1,2}(?:,\d{1,2})*)\]")
ref_re = re.compile(r"^(\s*T`)(\d{1,2})(\.\s)")

bump = lambda n: n + 1 if n >= 7 else n


def fix_cite(m):
    return "[" + ",".join(str(bump(int(x))) for x in m.group(1).split(",")) + "]"


n_cite_lines = n_ref_lines = 0
out = []
for ln in lines:
    if "T`" in ln:
        new = cite_re.sub(fix_cite, ln)
        m = ref_re.match(new)
        if m and int(m.group(2)) >= 7:
            new = m.group(1) + str(int(m.group(2)) + 1) + m.group(3) + new[m.end():]
            n_ref_lines += 1
        if new != ln:
            n_cite_lines += 1
        out.append(new)
    else:
        out.append(ln)

open(PATH, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"lines changed: {n_cite_lines} (incl. {n_ref_lines} reference-list lines)")
