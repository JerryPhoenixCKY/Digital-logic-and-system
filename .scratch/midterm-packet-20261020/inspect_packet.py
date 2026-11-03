"""Render the complete packet and measure text page boundaries."""
from pathlib import Path
import json
import re
from PIL import Image, ImageDraw, ImageFont
import pypdfium2 as pdfium
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
PDF=ROOT/"output/pdf/ECE2050_Midterm_Review.pdf"
TMP=ROOT/"tmp/pdfs/midterm"
PAGES=TMP/"pages"
PAGES.mkdir(parents=True, exist_ok=True)
doc=pdfium.PdfDocument(PDF)
font=ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf",22)
for i in range(len(doc)):
    im=doc[i].render(scale=1.35).to_pil().convert("RGB")
    im.save(PAGES/f"page-{i+1:02d}.png")
for first in range(0,len(doc),6):
    montage=Image.new("RGB",(1212,1788),"#dce5e9")
    draw=ImageDraw.Draw(montage)
    for j in range(6):
        idx=first+j
        if idx>=len(doc):break
        im=Image.open(PAGES/f"page-{idx+1:02d}.png")
        im.thumbnail((390,550))
        x=11+(j%3)*400
        y=36+(j//3)*880
        # Plenty of resolution for reading page structure in a compact grid.
        im=Image.open(PAGES/f"page-{idx+1:02d}.png")
        im.thumbnail((390,820))
        montage.paste(im,(x,y))
        draw.text((x,y-28),f"Page {idx+1}",font=font,fill="#20394b")
    # Crop unused bottom gap in the two-row contact sheet.
    montage=montage.crop((0,0,1212,1520))
    montage.save(TMP/f"contact-{first//6+1:02d}.png")

reader=PdfReader(PDF)
text=[p.extract_text() for p in reader.pages]
(TMP/"page-text.json").write_text(json.dumps(text,ensure_ascii=False),encoding="utf-8")
warnings=[]
with pdfplumber.open(PDF) as p:
    for i,page in enumerate(p.pages):
        for word in page.extract_words():
            if word["x0"]<35 or word["x1"]>page.width-30:
                warnings.append({"page":i+1,"word":word["text"],"x0":word["x0"],"x1":word["x1"]})
        if not page.chars:
            warnings.append({"page":i+1,"warning":"empty page"})
full="\n".join(text)
for expected in ["知识大纲","原理复习","公式与适用条件","自测与完整解析","0xC2358000","11010011010"]:
    if expected not in full:
        warnings.append({"warning":"text missing","value":expected})
report={"pages":len(doc),"contact_sheets":(len(doc)+5)//6,"boundary_warnings":warnings,
        "bookmarks":len(reader.outline),"answer_headers":full.count("答案与理由"),
        "part_pages":{m.group(0):i+1 for i,t in enumerate(text) for m in re.finditer(r"PART 0[1-4]",t)}}
(TMP/"qa-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
