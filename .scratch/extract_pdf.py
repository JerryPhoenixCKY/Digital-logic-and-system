# -*- coding: utf-8 -*-
"""Extract text from a PDF into a workspace .txt file for reading."""
import sys
import pdfplumber

src = sys.argv[1]
out = sys.argv[2]

with pdfplumber.open(src) as pdf:
    n = len(pdf.pages)
    with open(out, "w", encoding="utf-8") as f:
        f.write("### PAGES: %d\n" % n)
        for i, page in enumerate(pdf.pages, 1):
            f.write("\n\n========== PAGE %d ==========\n" % i)
            txt = page.extract_text(x_tolerance=1.5, y_tolerance=2.5) or ""
            f.write(txt)
print("pages:", n, "->", out)
