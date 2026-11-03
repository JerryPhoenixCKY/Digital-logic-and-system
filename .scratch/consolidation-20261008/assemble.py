from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
DEST = WORK / 'draft' / 'Notes'
GROUPS = json.loads((WORK / 'mapping.json').read_text('utf-8'))['groups']
parts = re.split(r'^@@@ ([^\n]+)\n', (WORK / 'core-notes.md').read_text('utf-8'), flags=re.M)
CORE = dict(zip(parts[1::2], parts[2::2]))
assert set(CORE) == {g['target'] for g in GROUPS}

# One logical entry point for every former topic; deeper examples stay beside it.
ENTRY = [
    [1, 2], [1, 2, 2, 2, 2, 3, 4], [1, 2, 3, 4], [1, 3], [2, 3, 4], [1, 3],
    [1, 2, 2, 2, 3, 3, 4, 4], [1, 2, 3], [1, 2, 3, 3, 4, 5], [1, 2, 3, 3, 4],
    [1, 4, 3], [2, 5, 1], [1], [1], [1, 2, 3, 4], [1, 3, 2, 4], [1], [1], [1],
    [1, 2, 3, 4, 5], [1, 3], [1], [1], [1, 2, 3, 4, 5], [1, 3], [1, 2, 3],
    [1, 3], [1, 3], [1, 4], [1], [1],
]
assert len(ENTRY) == len(GROUPS)

HEADINGS = {t: re.findall(r'^## ([^\n]+)', b, re.M) for t, b in CORE.items()}
SOURCE = {}
OLD_NAMES = {}
for g, indices in zip(GROUPS, ENTRY):
    assert len(g['sources']) == len(indices)
    for name, ix in zip(g['sources'], indices):
        raw = (ROOT / 'Notes' / (name + '.md')).read_text('utf-8')
        fm = yaml.safe_load(raw.split('---', 2)[1])
        SOURCE[name] = {'raw': raw, 'fm': fm, 'group': g, 'entry': ix}
        for alias in [name] + fm['aliases']:
            if alias in OLD_NAMES:
                assert OLD_NAMES[alias]['group']['target'] == g['target'], alias
            OLD_NAMES[alias] = SOURCE[name]

CHAPTERS = [
    ('Ch1', 'Digital Foundations · 数字基础', '从电压、逻辑值与波形建立数字系统模型。'),
    ('Ch2', 'Number Representation and Coding · 数值表示与编码', '位权 → 位宽与符号 → 精度 → 数据含义 → 检错。'),
    ('Ch3', 'Gates and Electrical Interfaces · 逻辑门与电气接口', '先判断布尔功能，再检查电压阈值与噪声预算。'),
    ('Ch4', 'Boolean Algebra and Minimization · 布尔代数与化简', '模型与规则 → 真值表与标准式 → 最小覆盖。'),
    ('Ch5', 'Combinational Analysis and Design · 组合逻辑分析与设计', '从需求或连线得到函数，验证等价后选择实现，再测试故障。'),
    ('Ch6', 'Combinational Building Blocks · 组合功能块', '算术 → 比较与选择 → 显示转换 → 总线 → 延迟与冒险。'),
    ('Ch7', 'State and Storage Elements · 状态与存储元件', '反馈保持 → 锁存与边沿采样 → 激励与控制优先级。'),
    ('Ch8', 'Shift and Pulse Applications · 移位与脉冲应用', '移位反馈产生扫描顺序，脉冲与捕获机制形成输入接口。'),
    ('Ch9', 'State Machines and Timing · 状态机与时序', '先设计状态与转移，再检查路径和跨域协议。'),
    ('Ch10', 'Counters and Digital Clocks · 计数器与数字时钟', '从状态序列推激励，按接受的进位同步级联。'),
    ('Ch11', 'Memory and Programmable Logic · 存储与可编程逻辑', '存储组织与保持机制 → 查表和共享逻辑 → FPGA 实现。'),
    ('HDL', 'VHDL and Project Verification · VHDL 与项目验证', '语言语义 → 完整建模 → 独立验证 → 结构化项目。'),
    ('Review', 'Integrated Review · 综合复习', '闭卷回忆核心方程，按题意建模，用边界与反例验证。'),
]

# Route specialised material into the relevant point of the newly authored line.
ROUTES = {
 'Digital Abstraction and System Design': [(r'Derivation|Worked', 3)],
 'Digital Waveforms': [(r'Derivation|Worked', 4)],
 'Parity Bit': [(r'Gate-Level|generation', 2)],
 'Cyclic Redundancy Check': [(r'guarantees|Worked', 4)],
 'AND-OR and AND-OR-Invert Logic': [(r'Example 2', 3), (r'Example 3', 3), (r'XOR', 7)],
 'Combinational Logic Design': [(r'Example 1', 3), (r'Example 2', 4), (r'Example 3|Example 4', 6), (r'Priority|Quiz|Pitfalls', 7)],
 'Universal Gates and Bubble Pushing': [(r'^Bubble', 3), (r'Example 4', 4), (r'Worked', 2)],
 'Digital Logic Troubleshooting': [(r'Derivation', 2), (r'Example [12]', 3), (r'Example 3', 4), (r'English|Common Errors', 5)],
 'Seven-Segment Display and Code Conversion': [(r'Truth Table', 1), (r'Derivation', 2), (r'Code Conversion|Worked', 5), (r'Pitfalls|English', 4)],
 'Tri-State Buffers and Bus Drivers': [(r'Mechanism', 2), (r'Worked', 3)],
 'Propagation Delay and Logic Hazards': [(r'Example 1', 1), (r'Derivation|Example 2', 2), (r'Sampling', 3)],
 'Register Enable and Reset': [(r'Timing Boundary', 6)],
 'Shift Registers': [(r'Example 2|Serial interfaces', 2)],
 'One-Shots and Pulse Applications': [(r'Derivation|Worked', 2), (r'Edge Detection|Delayed', 3)],
 'Keyboard Scanning and Encoding': [(r'Timing', 4), (r'Debounce', 3), (r'Worked', 2), (r'Multi-key', 4)],
 'Setup and Hold Timing': [(r'Worked|Skew', 2)],
 'Metastability and Clock Domain Crossing': [(r'Validity|Worked', 4)],
 'Counters': [(r'Derivation', 2), (r'Control Inputs', 4)],
 'Cascaded Counters and Digital Clocks': [(r'Example [23]', 4)],
 'Memory Arrays and Expansion': [(r'Width|Depth', 2), (r'Interface', 4)],
 'SRAM DRAM and ROM': [(r'Worked', 4)],
 'Field-Programmable Gate Array': [(r'Constraints|Practical', 4)],
 'VHDL Language and Modeling': [(r'Concurrent', 2), (r'Combinational|Reset|Coding', 3), (r'Exam', 5)],
 'Testbench and Functional Verification': [(r'Trace|Test Dimensions', 5)],
 'Structural Shift Register Project': [(r'Reusable|Structural', 2), (r'Worked|Verification', 3), (r'Pitfalls', 4)],
 'Exam Review and Problem Solving': [(r'Learning', 1), (r'Read the Question', 2), (r'Number', 3), (r'Boolean|Gate and Block', 4), (r'Timing|State Tracing|Counter', 5), (r'VHDL', 6), (r'Checking|English', 7)],
}

def route(source, heading):
    info = SOURCE[source]
    for pattern, ix in ROUTES.get(source, []):
        if re.search(pattern, heading, re.I):
            return ix
    return info['entry']

WIKI = re.compile(r'(!?)\[\[([^\]]+)\]\]')

def rewrite_links(text):
    def sub(m):
        if m[1]:
            return m[0]
        full, sep, label = m[2].partition('|')
        name, hashmark, anchor = full.partition('#')
        if name not in OLD_NAMES:
            return m[0]
        info = OLD_NAMES[name]
        target = info['group']['target']
        if name == target and not hashmark:
            return m[0]
        ix = route(next(n for n, s in SOURCE.items() if s is info), anchor) if hashmark else info['entry']
        # Obsidian heading links use the displayed heading, not web URL slugs.
        heading = HEADINGS[target][ix - 1]
        display = label if sep else name
        return '[[' + target + '#' + heading + '|' + display + ']]'
    return WIKI.sub(sub, text)

def unique(items):
    return list(dict.fromkeys(items))

def frontmatter(fm):
    # Existing aliases are plain strings. Avoid quoting unless YAML needs it.
    def scalar(x):
        s = str(x)
        if re.search(r'[:\[\]{}#\n]|^[-?!&*]|^(true|false|null)$', s, re.I):
            return json.dumps(s, ensure_ascii=False)
        return s
    out = ['---']
    for key, value in fm.items():
        if isinstance(value, list):
            out += [key + ':'] + ['  - ' + scalar(v) for v in value]
        else:
            out.append(key + ': ' + scalar(value))
    out += ['---', '']
    return '\n'.join(out) + '\n'

def split_sections(text):
    # Headings at line start outside fenced code; source code has no ## headers.
    pp = re.split(r'^## ([^\n]+)\n', text, flags=re.M)
    return list(zip(pp[1::2], pp[2::2]))

def clean(content):
    content = re.sub(r'^索引：.*$', '', content, flags=re.M)
    content = re.sub(r'\n---\s*$', '', content)
    # Flatten nested callouts before wrapping in one expandable example block.
    content = re.sub(r'^> \[!([A-Z]+)\][+-]?\s*(.*)$', r'**\2**', content, flags=re.M)
    content = re.sub(r'^> ?', '', content, flags=re.M)
    content = re.sub(r'^#{3,6} (.+)$', r'**\1**', content, flags=re.M)
    # Correct overstatements retained in detailed prose.
    content = content.replace('$R$ 或 $S$ 里出现 10，就必须老老实实走中枢。',
                              '经过十进制是便于手算的通用路线，不是数学上唯一的转换算法。')
    content = content.replace('它正好是 1 K', '它等于 1 Ki；十进制前缀 k 表示 1000')
    content = content.replace('`1011` 就算不带小数点，也不是十进制数（它没有下标时通常按二进制读）。',
                              '`1011` 在十进制、二进制、八进制和十六进制中都可作为合法写法；必须由下标或上下文确定。')
    return re.sub(r'\n{3,}', '\n\n', content).strip()

def figure_excerpt(raw, asset):
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        if '![[%s]]' % asset in line:
            chunk = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip():
                if lines[j].startswith('##'):
                    break
                chunk.append(lines[j])
                j += 1
            return clean('\n'.join(chunk))
    raise ValueError(asset)

SKIP = re.compile(r'^(Core Definition|Assumptions|Method|Connections|Pitfalls(?: and Review)?\s*·|Exam English(?: and Connections| and Review)?\s*·|English Exam Q&A|Quick Check|Exam Recall)', re.I)

stats = []
provenance = {}
for g in GROUPS:
    target = g['target']
    fm = {'tags': unique(['ECE2050'] + [t for s in g['sources'] for t in SOURCE[s]['fm']['tags']]),
          'date': min(str(SOURCE[s]['fm']['date']) for s in g['sources']),
          'updated': '2026-10-08',
          'chapter': g['chapter'],
          'aliases': unique([g['chinese'], target, g['chinese'] + ' · ' + g['chapter']] +
                            [a for s in g['sources'] for a in [s] + SOURCE[s]['fm']['aliases']])}
    blocks = defaultdict(list)
    sources = []
    seen = set()
    for s in g['sources']:
        raw = SOURCE[s]['raw']
        kept = defaultdict(list)
        for h, c in split_sections(raw):
            if h.startswith('Sources'):
                sources.append(clean(c))
                continue
            if SKIP.search(h):
                continue
            c = clean(c)
            if not c:
                continue
            digest = hashlib.sha256(c.encode()).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            kept[route(s, h)].append('**' + h + '**\n\n' + c)
        # Keep all previously referenced diagrams, including ones in compressed definitions.
        used = '\n'.join(c for cs in kept.values() for c in cs)
        missing = [a for a in unique(re.findall(r'!\[\[([^\]|]+)', raw)) if '![[%s]]' % a not in used]
        if missing:
            kept[SOURCE[s]['entry']].insert(0, '**图示与讲义依据**\n\n' + '\n\n'.join(figure_excerpt(raw, a) for a in missing))
        for ix, chunks in sorted(kept.items()):
            expanded = '\n\n'.join(chunks)
            # The fold belongs to a primary concept, not to a second standalone note.
            label = s + ' · 推导与例题'
            block = '> [!example]- ' + label + '\n' + '\n'.join('> ' + line if line else '>' for line in expanded.splitlines())
            blocks[ix].append(block)
    body_parts = re.split(r'^## ([^\n]+)\n', CORE[target], flags=re.M)
    assembled = body_parts[0].strip() + '\n\n'
    for i in range(1, len(body_parts), 2):
        ix = (i + 1) // 2
        assembled += '## ' + body_parts[i] + '\n\n' + body_parts[i + 1].strip() + '\n\n'
        if blocks[ix]:
            assembled += '\n\n'.join(blocks[ix]) + '\n\n'
    if g['chapter'].startswith('Ch'):
        filename = ('ECE2050-Chap1(1).pdf' if g['chapter'] == 'Ch1' else 'ECE2050-' + g['chapter'].replace('Ch', 'Chap') + '.pdf')
        rel = filename if (ROOT / filename).is_file() else 'LGU_HUB_ECE2050/' + filename
        assert (ROOT / rel).is_file()
        sources.insert(0, '主线课件：[' + g['chapter'] + ' lecture](../' + quote(rel, safe='/') + ')。正文的讲义页码保留原编号；自算例题另行标注。')
    elif g['chapter'] == 'HDL':
        sources.insert(0, '课程资料：[VHDL tutorial](../LGU_HUB_ECE2050/Tutorial6--VHDL-Tut-for%20reference.pdf)、[project specification](../LGU_HUB_ECE2050/ECE2050Project.pdf)。')
    if sources:
        assembled += '## Sources · 课件依据\n\n' + '\n\n'.join(unique(sources)) + '\n\n'
    assembled = rewrite_links(assembled)
    text = frontmatter(fm) + '# ' + target + ' · ' + g['chinese'] + '\n\n' + assembled.rstrip() + '\n\n---\n索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]\n'
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / (target + '.md')).write_text(text, 'utf-8')
    stats.append({'chapter': g['chapter'], 'target': target, 'sources': len(g['sources']), 'lines': len(text.splitlines()), 'characters': len(text), 'folds': len(re.findall(r'^> \[!example\]-', text, re.M))})
    provenance[target] = {'original_topics': g['sources'], 'assets': unique(re.findall(r'!\[\[([^\]|]+)', text))}

tree_old = (ROOT / 'Notes' / 'ECE2050 Knowledge Tree.md').read_text('utf-8')
tree_fm = yaml.safe_load(tree_old.split('---', 2)[1])
tree_fm['updated'] = '2026-10-08'
tree = frontmatter(tree_fm) + '# ECE2050 Knowledge Tree · 知识树\n\n'
tree += '> [!NOTE] Learning route · 学习路线\n> 全库按章节组织为 **31 篇主线笔记**，每章 1–5 篇。先读正文中的定义、核心方程和重要提示；需要验证过程时，再展开同一小节的推导、例题与图示。术语可从 [[Glossary]] 反查。\n\n'
tree += '**完整主线：** 数字模型 → 数值表示 → 逻辑与接口 → 布尔化简 → 组合设计与功能块 → 存储和采样 → 状态机与计数器 → 存储／可编程逻辑 → HDL 验证。\n\n'
tree += '> [!IMPORTANT] 三条贯穿全课的检查\n> **含义：** 位宽、编码、极性、事件与无效输入。**功能：** 方程、真值表与状态转换是否一致。**实现：** 电平、延迟、采样与物理接口是否满足假设。\n\n'
for ch, title, purpose in CHAPTERS:
    gs = [g for g in GROUPS if g['chapter'] == ch]
    tree += '## ' + ch + ' · ' + title + '\n\n' + purpose + '\n\n'
    for g in gs:
        quick = re.search(r'^> (?!\[)([^\n]+)$', CORE[g['target']], re.M)[1]
        important = ' ❗' if ch in {'Ch2', 'Ch4', 'Ch5', 'Ch7', 'Ch9', 'Ch10', 'HDL'} else ''
        tree += '- ✅' + important + ' [[' + g['target'] + ']] · **' + g['chinese'] + '** — ' + quick + '\n'
    tree += '\n'
tree += '## Study Checkpoints · 阶段检查\n\n'
tree += '1. **Ch1–3：** 能解释一个位串的数值与含义，并分别计算其逻辑输出和电气裕量。\n'
tree += '2. **Ch4–6：** 能从需求或门图建立函数，化简、实现并穷举验证指定输入。\n'
tree += '3. **Ch7–10：** 能逐边沿追踪状态，推导激励，并检查建立／保持、未用态恢复和级联条件。\n'
tree += '4. **Ch11 与 HDL：** 能组织存储接口，解释查表实现，并用独立参考模型验证硬件描述。\n\n'
tree += '✅ 表示已有完整主线内容；❗标记需要反复练习的章节。考前按 [[Exam Review and Problem Solving]] 检查条件、方程、边界与英文答句。\n\n---\n索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]\n'
(DEST / 'ECE2050 Knowledge Tree.md').write_text(tree, 'utf-8')

gloss_old = (ROOT / 'Notes' / 'Glossary.md').read_text('utf-8')
gloss_fm = yaml.safe_load(gloss_old.split('---', 2)[1]); gloss_fm['updated'] = '2026-10-08'
rows = defaultdict(list); seen_terms = set()
for line in gloss_old.splitlines():
    if not line.startswith('|') or not re.search(r'\[\[', line):
        continue
    oldlink = re.search(r'\[\[([^#|\]]+)', line)[1]
    if oldlink not in OLD_NAMES:
        raise ValueError('Unclassified glossary row: ' + line)
    info = OLD_NAMES[oldlink]
    key = tuple(x.strip() for x in line.split('|')[1:3])
    if key in seen_terms:
        continue
    seen_terms.add(key)
    line = line.replace('覆盖全部 1 且圈最少的积之和', '覆盖全部指定 1、避开指定 0，按项数及文字数比较的最小积之和')
    line = line.replace('覆盖全部 0 且圈最少的和之积', '覆盖全部指定 0、避开指定 1，按项数及文字数比较的最小和之积')
    line = line.replace('$2^{10}=1024=1$ K 是工程速记起点', '$2^{10}=1024$；Ki 表示 1024，十进制 k 表示 1000')
    line = line.replace('每 3（4）位一组，从右往左，最左补 0', '从小数点向两侧每 3（4）位分组；整数向左补 0，小数向右补 0')
    line = line.replace('符号的值与位置无关；格雷码、循环码是典型例子', '数值不能按固定数位权简单相加；格雷码属非位权编码，不宜与传统非位权记数法混同')
    line = line.replace('某列相加超过基数 1 时', '某列二进制相加达到 2 时')
    line = line.replace('符号、指数、尾数三字段，用 $(1.M)\times2^{E-127}$ 解释', '符号、指数、尾数字段；正规数有隐含前导 1，特殊码另行分类')
    rows[info['group']['chapter']].append(rewrite_links(line))
gloss = frontmatter(gloss_fm) + '# ECE2050 Glossary · 术语表\n\n'
gloss += '> [!NOTE] How to use · 用法\n> 按章节找英文名、中文名或缩写；链接直接进入主线笔记的对应小节。完整推导、适用条件与例题留在专题中；学习顺序见 [[ECE2050 Knowledge Tree]]。\n\n'
for ch, title, _ in CHAPTERS:
    if not rows[ch]:
        continue
    gloss += '## ' + ch + ' · ' + title + '\n\n'
    gloss += '| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |\n|---|---|---|---|---|\n'
    gloss += '\n'.join(rows[ch]) + '\n\n'
gloss += '---\n索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]\n'
(DEST / 'Glossary.md').write_text(gloss, 'utf-8')

(WORK / 'assembly-report.json').write_text(json.dumps({'notes': stats, 'glossary_terms': len(seen_terms), 'provenance': provenance}, ensure_ascii=False, indent=2), 'utf-8')
(WORK / 'link-mapping.json').write_text(json.dumps({n: {'target': info['group']['target'], 'heading': HEADINGS[info['group']['target']][info['entry']-1]} for n, info in OLD_NAMES.items()}, ensure_ascii=False, indent=2), 'utf-8')
print(json.dumps({'topic_notes': len(stats), 'hubs': 2, 'glossary_terms': len(seen_terms), 'total_characters': sum(x['characters'] for x in stats), 'longest': sorted(stats, key=lambda x: x['characters'], reverse=True)[:5]}, ensure_ascii=False, indent=2))
