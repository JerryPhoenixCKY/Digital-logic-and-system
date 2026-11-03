"""Package the checked course notes as a self-contained HTML / printable PDF."""
from pathlib import Path
import html
import io
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
TMP = ROOT / "tmp" / "pdfs" / "midterm"
OUT.mkdir(exist_ok=True)
(OUT / "pdf").mkdir(exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
PANDOC = Path(r"D:\anaconda\Library\bin\pandoc.exe")
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
HTML_PATH = OUT / "ECE2050_Midterm_Review.html"
PDF_PATH = OUT / "pdf" / "ECE2050_Midterm_Review.pdf"
RAW_PDF = TMP / "packet-unpaginated.pdf"
DOCS = [
    ("Midterm Knowledge Outline", "outline", "01", "知识大纲", "Knowledge outline"),
    ("Midterm Review Guide", "principles", "02", "原理复习", "Principles and reasoning"),
    ("Midterm Formula Sheet", "formulas", "03", "公式与适用条件", "Formula reference"),
    ("Midterm Practice and Answers", "practice", "04", "自测与完整解析", "Practice and answers"),
]
DOC_IDS = {x[0]: x[1] for x in DOCS}
ANCHORS = {}

CSS = """
:root{--ink:#172a3b;--muted:#567083;--teal:#086e75;--line:#d6e1e5;--soft:#edf5f5;--gold:#a66022}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:"Microsoft YaHei","Segoe UI",sans-serif;color:var(--ink);font-size:14px;line-height:1.8;margin:0;background:#e7edf0}
a{color:var(--teal);text-decoration:none;overflow-wrap:anywhere}
a:hover{text-decoration:underline}
main{max-width:1020px;background:white;margin:32px auto;padding:60px 72px;box-shadow:0 7px 36px #162e4120}
.cover{min-height:820px;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-size:12px;letter-spacing:3px;color:var(--teal);font-weight:700}
.cover h1{font-size:48px;letter-spacing:-1px;line-height:1.35;margin:18px 0;color:var(--ink)}
.cover .subtitle{font-size:20px;color:var(--muted);margin:0 0 26px}
.cover .intro{max-width:660px;font-size:16px}
.scope{margin:30px 0 20px;padding:14px 20px;background:var(--soft);border-left:4px solid var(--teal)}
.toc{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:28px 0}
.toc a{border:1px solid var(--line);border-radius:4px;padding:18px;display:block;color:var(--ink)}
.toc b{color:var(--teal);font-size:14px;margin-right:12px}
.toc small{display:block;margin-left:34px;color:var(--muted)}
.cover .meta{font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px;margin-top:30px}
.toolbar{position:sticky;top:0;z-index:2;background:#172a3bef;color:white;padding:10px 20px;display:flex;gap:24px;align-items:center;justify-content:center}
.toolbar a,.toolbar button{color:white;font:inherit;font-size:13px}
.toolbar button{border:1px solid #ffffff60;border-radius:4px;background:transparent;padding:3px 12px;cursor:pointer}
.part{padding-top:44px}
.part>header{border-top:4px solid var(--teal);padding-top:15px;margin-bottom:24px}
.part>header .part-num{color:var(--teal);font-size:12px;font-weight:700;letter-spacing:2px}
.part>header h1{font-size:30px;margin:4px 0;line-height:1.4}
.part>header p{color:var(--muted);font-size:13px;margin:0}
h2{font-size:20px;line-height:1.5;margin:30px 0 13px;border-bottom:1px solid var(--line);padding-bottom:7px;color:#0c626a}
h3{font-size:16px;line-height:1.5;margin:24px 0 10px;color:#1b4057}
h4{font-size:14px;margin:20px 0 8px}
p{margin:9px 0}
ul,ol{margin:9px 0;padding-left:1.6em}
li{margin:4px 0}
li>p{margin:4px 0}
blockquote{margin:15px 0;padding:12px 18px;border-left:3px solid #50a2a5;background:#f0f6f6;color:#234351}
blockquote p:first-child{margin-top:0}
blockquote p:last-child{margin-bottom:0}
details{margin:12px 0 19px;padding:9px 16px 12px;background:#f3f6f8;border:1px solid #e0e7eb;border-radius:3px}
details summary{font-weight:700;color:#38626e;cursor:pointer}
details>div{margin-top:8px}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:12.6px;line-height:1.65}
thead{background:#e7f0f2}
th,td{border:1px solid var(--line);padding:7px 9px;vertical-align:top;overflow-wrap:anywhere}
th{font-weight:700;text-align:left}
tr:nth-child(even) td{background:#f9fbfc}
pre{font-size:11.5px;line-height:1.5;background:#f3f6f8;padding:12px;white-space:pre-wrap;overflow-wrap:anywhere}
code{font-family:Consolas,"Microsoft YaHei",monospace;font-size:.92em;background:#f0f3f5;padding:.1em .2em;border-radius:2px}
pre code{padding:0;background:transparent}
math{font-family:"Cambria Math","STIX Two Math",serif}
math[display="block"]{font-size:1.05em;margin:14px 0;overflow:visible}
.math.display{display:block;text-align:center;margin:12px 0;break-inside:avoid}
.math.inline{white-space:nowrap}
.map{margin:18px 0;padding:16px;background:var(--soft);border:1px solid var(--line);text-align:center}
.map .row{display:flex;justify-content:center;align-items:center;gap:12px;margin:8px 0;flex-wrap:wrap}
.map span.node{border:1px solid #94bbbf;background:white;padding:7px 12px;border-radius:3px;font-weight:600}
.map .branch{font-size:12px;color:var(--muted)}
.section-links{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12px;margin:15px 0 20px}
.section-links a{border-bottom:1px dotted #94bbbf}
.reader-note{font-size:12px;color:var(--muted)}
input[type="checkbox"]{width:12px;height:12px;margin:0 5px 0 0}
hr{border:0;border-top:1px solid var(--line);margin:20px 0}
@page{size:A4;margin:18mm 17mm 19mm}
@media print{
 html{scroll-behavior:auto}
 body{background:white;font-size:10.3pt;line-height:1.6}
 main{max-width:none;margin:0;padding:0;box-shadow:none}
 .toolbar{display:none}
 .cover{height:253mm;min-height:0;break-after:page}
 .cover h1{font-size:37pt}
 .cover .subtitle{font-size:16pt}
 .cover .intro{font-size:11.5pt}
 .cover .meta{font-size:9pt}
 .toc{gap:10px}
 .toc a{padding:12px}
 .scope{margin:20px 0 10px;padding:10px 15px}
 .part{padding:0;break-before:page}
 .part>header{margin-bottom:15px}
 .part>header h1{font-size:24pt}
 .part>header p{font-size:10pt}
 h2{font-size:14.5pt;margin:21px 0 10px;padding-bottom:5px}
 h3{font-size:11.7pt;margin:17px 0 8px}
 h4{font-size:10.6pt}
 h1,h2,h3,h4,summary{break-after:avoid}
 p{orphans:3;widows:3;margin:6px 0}
 blockquote{padding:9px 13px;margin:10px 0}
 details{padding:8px 12px;margin:10px 0 14px;break-inside:avoid}
 details:not([open])>div{display:block!important}
 .question{break-inside:avoid}
 details summary{list-style:none}
 details summary::before{content:"解析  ·  ";color:#567083}
 table{font-size:8.7pt;line-height:1.55;margin:10px 0}
 th,td{padding:5px 7px}
 tr{break-inside:avoid}
 thead{display:table-header-group}
 pre{font-size:8.3pt;break-inside:avoid}
 li{margin:2px 0}
 ul,ol{margin:7px 0}
 a{color:inherit}
 .section-links{font-size:9pt}
 .reader-note{font-size:8.5pt}
 .math.display{font-size:10pt}
 .map{break-inside:avoid}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
@media(max-width:700px){main{margin:0;padding:25px 20px}.cover{min-height:0}.cover h1{font-size:36px}.toc{grid-template-columns:1fr}.toolbar{gap:14px;padding:9px 5px}.toolbar a{font-size:12px}table{font-size:11px}th,td{padding:5px}.math.display{overflow-x:auto}}
"""

FLOW = """
<div class="map">
 <div class="row"><span class="node">Ch1 数字抽象与波形</span></div>
 <div class="row"><span class="node">Ch2 数值表示与编码</span><span class="branch">并行基础</span><span class="node">Ch3 逻辑门与电平</span></div>
 <div class="row"><span class="node">Ch4 布尔代数与 K-map</span><span>→</span><span class="node">Ch5 组合逻辑设计</span></div>
 <div class="row"><span class="node">Ch6 功能块、选择与连接</span><span>→</span><span class="node">电压、延迟与冒险检查</span></div>
 <p class="branch">Ch1 为 Ch2、Ch3 建立基础；Ch3 → Ch4 → Ch5 → Ch6，Ch2 支持 Ch5；Ch3 与 Ch6 共同支持实现检查。</p>
</div>
"""

def repair_overlines(match):
    ns = "http://www.w3.org/1998/Math/MathML"
    ET.register_namespace("", ns)
    root = ET.fromstring(match.group(0))
    for node in list(root.iter()):
        children = list(node)
        if node.tag == "{" + ns + "}mover" and len(children) == 2 and children[-1].text in ("¯", "‾"):
            expression = children[0]
            node.clear()
            node.tag = "{" + ns + "}mrow"
            node.set("style", "border-top:0.065em solid currentColor;padding-top:0.09em")
            node.append(expression)
    return ET.tostring(root, encoding="unicode")

def pandoc(text):
    r = subprocess.run(
        [str(PANDOC), "-f", "markdown+tex_math_dollars+raw_html+pipe_tables+task_lists",
         "-t", "html5", "--mathml", "--wrap=none"],
        input=text, encoding="utf-8", capture_output=True, check=True)
    if r.stderr.strip():
        raise RuntimeError("Pandoc conversion warning: " + r.stderr)
    # Chrome's macron glyph does not stretch across a compound expression.
    # A MathML row border preserves the exact complemented scope.
    return re.sub(r'<math\b.*?</math>', repair_overlines, r.stdout, flags=re.S)

def wikilink(match):
    raw = match.group(1)
    dest, _, label = raw.partition("|")
    name, _, anchor = dest.partition("#")
    display = label or name or anchor
    if name in DOC_IDS:
        url = "#" + ANCHORS.get((name, anchor), DOC_IDS[name])
    else:
        path = ROOT / "Notes" / (name + ".md")
        if not path.exists():
            raise FileNotFoundError(path)
        url = "../Notes/" + quote(name + ".md")
    return '<a href="' + url + '">' + html.escape(display) + "</a>"

def prepare(source):
    source = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", source, count=1, flags=re.S)
    source = re.sub(r"^# .*\n", "", source, count=1, flags=re.M)
    source = re.sub(r"\n---\n索引：.*\s*\Z", "\n", source)
    source = re.sub(r"```mermaid\n.*?\n```", FLOW, source, flags=re.S)
    source = re.sub(r"\[\[([^\]]+)\]\]", wikilink, source)
    lines = source.splitlines()
    converted = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"> \[!example\]-", line, re.I):
            answer = []
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                answer.append(re.sub(r"^> ?", "", lines[i]))
                i += 1
            body = pandoc("\n".join(answer))
            converted.append('<details open class="answer"><summary>答案与理由</summary><div>' + body + "</div></details>")
            continue
        line = re.sub(r"^> \[![^\]]+\][+-]?\s*(.*)$", r"> **\1**", line)
        converted.append(line)
        i += 1
    return "\n".join(converted)

def build_html():
    sections = []
    heading_index = {}
    math_count = 0
    for name, id_, _, _, _ in DOCS:
        source = (ROOT / "Notes" / (name + ".md")).read_text(encoding="utf-8-sig")
        for heading in re.findall(r"^#{2,6} (.+)$", source, re.M):
            converted = pandoc("## " + heading)
            generated_id = re.search(r'<h2 id="([^"]+)"', converted).group(1)
            ANCHORS[(name, heading)] = id_ + "-" + generated_id
    for name, id_, number, cn, en in DOCS:
        path = ROOT / "Notes" / (name + ".md")
        source = path.read_text(encoding="utf-8-sig")
        rendered = pandoc(prepare(source))
        if id_ == "practice":
            rendered = re.sub(
                r"(<h3\b.*?)(?=<h[23]\b|\Z)",
                lambda m: '<article class="question">' + m.group(1) + "</article>\n",
                rendered, flags=re.S)
        math_count += rendered.count("<math ")
        # Prefix each Pandoc heading ID so the four notes cannot collide.
        ids = re.findall(r'<h[2-6] id="([^"]+)"', rendered)
        for old_id in ids:
            rendered = rendered.replace('id="' + old_id + '"', 'id="' + id_ + "-" + old_id + '"')
            rendered = rendered.replace('href="#' + old_id + '"', 'href="#' + id_ + "-" + old_id + '"')
        headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', rendered)
        heading_index[id_] = [(a, re.sub("<[^>]+>", "", b)) for a, b in headings]
        nav = '<div class="section-links">' + "".join(
            '<a href="#' + a + '">' + b + "</a>" for a,b in headings) + "</div>"
        sections.append(f'<section class="part" id="{id_}"><header><div class="part-num">PART {number}</div><h1>{cn}</h1><p>{en} · ECE2050 / Chapters 1-6</p></header>{nav}{rendered}</section>')
    toc = "".join(f'<a href="#{id_}"><b>{n}</b>{cn}<small>{en}</small></a>' for _,id_,n,cn,en in DOCS)
    cover = f"""
    <section class="cover" id="top">
     <div class="eyebrow">ECE2050 · DIGITAL LOGIC AND SYSTEMS</div>
     <h1>期中复习资料<br>与知识大纲</h1>
     <p class="subtitle">Chapters 1-6 · 秋季学期 2026</p>
     <p class="intro">先用大纲定位知识，再理解原理与公式条件，最后通过闭卷自测检验掌握程度。每一类题都检查：<strong>位宽、编码、有效极性和适用条件。</strong></p>
     <div class="scope"><strong>收录内容</strong><br>六章知识清单 · 原理串讲 · 15 类公式与条件 · 33 组自测及解析 · 课件页码与勘误</div>
     <nav class="toc">{toc}</nav>
     <p><strong>阅读顺序：</strong>01 勾选薄弱点 → 02 查原理 → 03 默写公式 → 04 独立解题。</p>
     <p class="reader-note">离线阅读版可点击目录，逐题收起答案；打印版完整显示答案，闭卷练习时请先遮住解析。</p>
     <div class="meta">整理依据：本学期 Ch1-6 课件、HW1/HW2 与既有专题笔记；旧卷仅用于题型交叉检查。<br>资料日期：2026-10-20。具体考试安排见“原理复习”开头及课程最新公告。</div>
    </section>
    """
    toolbar = '<nav class="toolbar"><a href="#top">目录</a>' + "".join(f'<a href="#{id_}">{cn}</a>' for _,id_,_,cn,_ in DOCS) + '<button id="toggle-answers">收起答案</button></nav>'
    script = """<script>
    const button=document.getElementById('toggle-answers');
    button.addEventListener('click',()=>{const all=[...document.querySelectorAll('details.answer')];const open=all.some(e=>e.open);all.forEach(e=>e.open=!open);button.textContent=open?'展开答案':'收起答案';});
    let beforePrint=[];
    window.addEventListener('beforeprint',()=>{beforePrint=[...document.querySelectorAll('details')].map(e=>e.open);document.querySelectorAll('details').forEach(e=>e.open=true)});
    window.addEventListener('afterprint',()=>{document.querySelectorAll('details').forEach((e,i)=>e.open=beforePrint[i]??true)});
    </script>"""
    doc = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ECE2050 期中复习资料与知识大纲</title><style>' + CSS + '</style></head><body>' + toolbar + '<main>' + cover + "".join(sections) + '</main>' + script + "</body></html>"
    if "[[" in doc or "[!example]" in doc or "```mermaid" in doc:
        raise AssertionError("Unconverted Obsidian syntax")
    if doc.count('<details open class="answer">') != 33:
        raise AssertionError("Expected all 33 answers")
    ids = re.findall(r'\bid="([^"]+)"', doc)
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate HTML IDs")
    for target in re.findall(r'href="#([^"]+)"',doc):
        if html.unescape(target) not in [html.unescape(x) for x in ids]:
            raise AssertionError("Broken in-document link: " + target)
    HTML_PATH.write_text(doc, encoding="utf-8")
    return math_count, heading_index

def print_pdf():
    proc = subprocess.run([
        str(CHROME), "--headless", "--disable-gpu", "--no-first-run",
        "--no-default-browser-check", "--disable-extensions",
        "--user-data-dir=" + str(TMP / "chrome-profile"),
        "--print-to-pdf=" + str(RAW_PDF),
        "--no-pdf-header-footer", "--allow-file-access-from-files",
        "--virtual-time-budget=2500", HTML_PATH.as_uri()
    ], capture_output=True, timeout=90)
    (TMP / "chrome-print.log").write_bytes(proc.stderr)
    if not RAW_PDF.exists() or RAW_PDF.stat().st_size < 10000:
        raise RuntimeError("Print failed: " + proc.stderr.decode(errors="replace")[-2000:])
    reader = PdfReader(RAW_PDF)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    n = len(writer.pages)
    writer.add_outline_item("目录 / Contents", 0)
    for _,_,number,cn,en in DOCS:
        marker = "PART " + number
        for index,page in enumerate(reader.pages):
            if marker in page.extract_text():
                writer.add_outline_item(number + " " + cn + " / " + en, index)
                break
    for index, page in enumerate(writer.pages):
        if index == 0:
            continue
        stream = io.BytesIO()
        w,h = float(page.mediabox.width),float(page.mediabox.height)
        c = canvas.Canvas(stream, pagesize=(w,h))
        c.setStrokeColorRGB(.81,.87,.9)
        c.line(48,37,w-48,37)
        c.setFont("Helvetica",8)
        c.setFillColorRGB(.34,.43,.49)
        c.drawString(48,25,"ECE2050  |  Midterm review  |  Ch1-6")
        c.drawRightString(w-48,25,f"{index + 1} / {n}")
        c.save()
        overlay = PdfReader(stream)
        page.merge_page(overlay.pages[0])
    writer.add_metadata({"/Title":"ECE2050 期中复习资料与知识大纲","/Author":"ECE2050 Study Notes","/Subject":"Chapters 1-6: outline, principles, formulas and 33 practice groups"})
    with PDF_PATH.open("wb") as f:
        writer.write(f)
    return n

if __name__ == "__main__":
    math_count, headings = build_html()
    pages = print_pdf()
    report = {"html":str(HTML_PATH),"pdf":str(PDF_PATH),"pages":pages,"math_expressions":math_count,"answers":33,"sections":{k:len(v) for k,v in headings.items()}}
    (TMP/"build-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))
