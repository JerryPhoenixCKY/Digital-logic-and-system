from pathlib import Path
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
OLD = ROOT / '.scratch/consolidation-20261008'
mapping = json.loads((OLD / 'link-mapping.json').read_text('utf-8'))
groups = json.loads((OLD / 'mapping.json').read_text('utf-8'))['groups']
targets = {g['target'] for g in groups}
mine = [g for g in groups if g['chapter'] in {'Ch1', 'Ch5', 'Review'}]
with zipfile.ZipFile(WORK / 'before-enrichment.zip') as z:
    before = {Path(p).stem: z.read(p).decode('utf-8-sig').replace('\r\n', '\n') for p in z.namelist() if p.endswith('.md')}

def links(text):
    text = text.replace('[[Boolean Forms and Algebraic Simplification 1', '[[Boolean Forms and Algebraic Simplification')
    def sub(m):
        if m[1]:
            return m[0]
        path, sep, label = m[2].partition('|')
        base, _, heading = path.partition('#')
        if base in targets or base not in mapping:
            return m[0]
        dest = mapping[base]
        return '[[' + dest['target'] + '#' + dest['heading'] + '|' + (label if sep else base) + ']]'
    return re.sub(r'(!?)\[\[([^\]]+)\]\]', sub, text)

def original(name, heading):
    raw = (OLD / 'original-Notes' / (name + '.md')).read_text('utf-8')
    parts = re.split(r'^## ([^\n]+)\n', raw, flags=re.M)
    result = dict(zip(parts[1::2], parts[2::2]))[heading]
    result = re.sub(r'^索引：.*$', '', result, flags=re.M)
    return links(re.sub(r'\n---\s*$', '', result).strip())

def insert_before_folds(text, ix, content):
    pp = re.split(r'^## ([^\n]+)\n', text, flags=re.M)
    j = 2*ix
    b = pp[j]
    where = b.find('\n> [!example]-')
    if where < 0:
        b = b.rstrip() + '\n\n' + content.strip() + '\n\n'
    else:
        b = b[:where].rstrip() + '\n\n' + content.strip() + '\n' + b[where:]
    pp[j] = b
    out = pp[0]
    for h, body in zip(pp[1::2], pp[2::2]):
        out += '## ' + h + '\n' + body
    return out

coverage = []
notes = {g['target']: links(before[g['target']]) for g in mine}

foundation = 'Digital Foundations and Waveforms'
notes[foundation] = notes[foundation].replace(
    '数字抽象 (digital abstraction) 把一段允许的电压解释为逻辑 0/1；导线电压本身仍连续变化。先确定“信息是什么意思”，再选择表示它的位宽、电平极性和采样方式。正逻辑 (positive logic) 与低有效控制 (active-low control) 可以同时存在。',
    '数字量 (digital quantity) 的信息取离散值，模拟量 (analog quantity) 可以连续变化。数字抽象 (digital abstraction) 把满足阈值条件的一段连续电压解释为逻辑 0/1；并不要求导线电压只取 0 V 和电源电压两个值。先确定信息含义，再选择位宽、电平极性和采样方式。\n\nAbstraction hides unnecessary detail while preserving the behavior required at the next level. A truth table avoids solving every transistor equation, but does not remove voltage limits or propagation delay from the interface contract.')
notes[foundation] = insert_before_folds(notes[foundation], 1,
    '### Static and Dynamic Discipline · 数字抽象的适用前提\n\n' + original('Digital Abstraction and System Design', 'Assumptions and Validity · 适用前提'))
notes[foundation] = insert_before_folds(notes[foundation], 3, r'''
### Design Principles · 抽象如何组成可靠系统

| Principle | 中文含义 | Concrete application |
|---|---|---|
| Hierarchy | 按层次组织 | Transistors → gates → adders → datapath |
| Modularity | 接口明确、可替换 | Reuse a verified two-input MUX |
| Regularity | 重复结构易扩展 | Repeat one full-adder stage per bit |
| Discipline | 用约束保证可靠 | Valid voltage levels and clock timing |

数据与控制分开后，先验证模块自身的行为，再检查组合后的接口契约。位宽、事件是否只计一次、复位初态和输出极性均属于契约，不能仅因模块单独通过测试就假定整个系统成立。
''')
notes[foundation] = insert_before_folds(notes[foundation], 2, r'''
### Measurement Conventions · 波形量与测量约定

| Term | Typical measurement convention | 中文解释 |
|---|---|---|
| Rise time $t_r$ | 10% to 90% of amplitude | 上升沿过渡时间 |
| Fall time $t_f$ | 90% to 10% | 下降沿过渡时间 |
| Pulse width | Often between 50% crossing points | 同一脉冲宽度 |
| Period | Corresponding edges of successive cycles | 完整重复时间 |
| Amplitude | Voltage or current excursion | 电压或电流幅值 |

这些百分比是测量约定，不能代替接收器的逻辑阈值。非理想波形应先按题目指定的交点定义测量；恒定直流信号没有通常意义的周期性边沿，不能用一段 HIGH 持续时间冒充周期。时间单位先换算：$1\,\mathrm{ms}=10^{-3}\,\mathrm{s}$，$1\,\mathrm{ns}=10^{-9}\,\mathrm{s}$。
''')
notes[foundation] = insert_before_folds(notes[foundation], 5,
    '### Review and Exam Wording · 方法与英文题意\n\n' +
    original('Digital Abstraction and System Design', 'Method and Review · 方法与复习') + '\n\n' +
    original('Digital Waveforms', 'Pitfalls and Exam English · 易错点与英文答题') + '\n\n' +
    '### Prerequisites and Applications · 先修与应用\n\n' +
    '位宽从 [[Number Systems and Base Conversion]] 建立，组合功能从 [[Logic Gates and Boolean Functions]] 与 [[Boolean Algebra and Circuit Models]] 建立。状态由 [[Sequential Logic and Flip-Flops]] 保存，系统实现可使用 [[Programmable Logic and FPGA]]；[[Counter Design and Digital Clocks]] 展示模块级联，[[Propagation Delay and Logic Hazards]] 与 [[Sequential Timing and Clock Domain Crossing]] 给波形模型加上真实时序条件。')
notes[foundation] = re.sub(r'\n> \[!example\]- Digital Waveforms · 推导与例题\n> \*\*Pitfalls and Exam English.*?(?=\n## 3)', '\n', notes[foundation], flags=re.S)

combo = 'Combinational Logic Analysis and Design'
notes[combo] = insert_before_folds(notes[combo], 1, r'''
### Analysis, Design and Specification · 模型与题意

分析 (analysis) 从既有连接推出函数；设计 (design) 从规范 (specification) 推出连接。稳态组合模型为 $\mathbf Y=F(\mathbf X)$，其中 $\mathbf X$ 是当前输入向量、$\mathbf Y$ 是当前输出向量，各分量为无量纲的 0/1；它不保存此前输入的历史。

“At least two” 包含更多输入有效的情况，“exactly two” 排除它们。“Consecutive” 在并行字中指相邻位置；若题目指定跨时钟串行流，则需状态机。所有量词都必须先落实到真值表，不能凭相似电路直接套式。
''')
notes[combo] = insert_before_folds(notes[combo], 2, r'''
### Formal Structures · 结构定义与一般式

与或逻辑 (AND-OR logic) 先形成乘积项，再由 OR 合并；与或非逻辑 (AND-OR-Invert logic, AOI) 对该 SOP 的整体输出取补。相邻变量表示 AND，$+$ 表示 OR，上横线表示 NOT，均按有效电平且传播完成后的稳态模型解释。

| Structure | Equation | Meaning |
|---|---|---|
| AND-OR | $Y=AB+CD$ | 任一乘积项为 1 即有效 |
| AOI | $Y=\overline{AB+CD}$ | 所有乘积项都为 0 才有效 |
| Equivalent POS | $Y=(\bar A+\bar B)(\bar C+\bar D)$ | 两个和项同时满足 |

一般 SOP $F=P_1+\cdots+P_k$ 的 AOI 输出为 $\bar F=\bar P_1\cdots\bar P_k$。每个乘积项取补后成为一个和项，这给出从 SOP 补函数到 POS 的完整对应，而非仅对个别输入加反相器。
''')
notes[combo] = insert_before_folds(notes[combo], 5,
    '### Exam Recall · 可检验的完整答句\n\n' + original('Combinational Logic Analysis', 'Exam Recall · 英文答题与复习'))
notes[combo] = insert_before_folds(notes[combo], 7,
    '### Specification Checks · 自检与误区\n\n' + original('AND-OR and AND-OR-Invert Logic', 'Quick Check · 自检') + '\n\n' +
    '例如 ABCD=1010 时 $AB+CD=0$，而 $(A+B)(C+D)=1$，一个反例就足以否定这两个形式的一般等价。\n\n' +
    original('Combinational Logic Design', 'Pitfalls and Review · 误区与复习') + '\n\n' +
    '### From Representation to Implementation · 表达、实现与验证的衔接\n\n' +
    '用 [[Boolean Forms and Algebraic Simplification]] 记录真值表、标准式与简化式，以 [[Boolean Algebra and Circuit Models]] 的代数和穷举规则证明等价。随后按约束选择 [[Universal Gates and Bubble Pushing]]、[[Comparison Decoding and Selection]] 或 [[Programmable Logic and FPGA]] 的实现；[[Digital Logic Troubleshooting]] 将同一逐节点模型用于正常／故障函数的比较。')

universal = 'Universal Gates and Bubble Pushing'
notes[universal] = insert_before_folds(notes[universal], 1, r'''
### Why Completeness Follows · 功能完备性的证明链

NOT、AND、OR 可以从完整真值表构造任意函数的标准积之和 (canonical SOP)。因此，只要 NAND 或 NOR 能分别构成这三种运算，就获得任意布尔函数的实现能力；证明不是仅展示一个特定例子。输入、内部节点与输出均为无量纲布尔量，等价按有效电平下的稳态模型判断。
''')
notes[universal] = insert_before_folds(notes[universal], 5,
    '### Implementation Procedure · 求解步骤与英文约束\n\n' + original(universal, 'Method and Exam English · 方法与答题') + '\n\n' +
    '### Concept Connections · 原语、函数与时序\n\n' +
    '基本门的定义见 [[Logic Gates and Boolean Functions]]，函数来自 [[Combinational Logic Analysis and Design]]；实现后还需按 [[Propagation Delay and Logic Hazards]] 检查路径时延与冒险。')

trouble = 'Digital Logic Troubleshooting'
notes[trouble] = insert_before_folds(notes[trouble], 1,
    '### Scope and Physical Interpretation · 诊断目标与适用条件\n\n' +
    '故障诊断先比较预期与实测行为，再设计能区分候选原因的试验。布尔故障模型是对物理损伤的假设；应先用 [[Boolean Algebra and Circuit Models]] 命名内部节点与驱动者，再用 [[Logic Levels and Noise Margins]] 判断实测电压是否属于有效 0/1。\n\n' +
    original(trouble, 'Assumptions and Validity · 模型与适用条件'))
notes[trouble] = insert_before_folds(notes[trouble], 5,
    '### Measurement Procedure · 实际排查步骤与仪器选择\n\n' + original(trouble, 'Method and Steps · 实际排查流程') + '\n\n' +
    '### Diagnostic Pitfalls · 不可省略的诊断条件\n\n' + original(trouble, 'Common Errors · 常见误区') + '\n\n' +
    '### English Exam Q&A · 检测与定位的完整答句\n\n' + original(trouble, 'English Exam Q&A · 英文答题训练') + '\n\n' +
    '### Review Contract · 结论必须包含的条件\n\n' + original(trouble, 'Method and Review · 复习检查'))
notes[trouble] = re.sub(r'\n> \[!example\]- Digital Logic Troubleshooting · 推导与例题\n> \*\*Common Errors[^\n]*\n(?:>[^\n]*\n)*', '\n', notes[trouble])

review = 'Exam Review and Problem Solving'
notes[review] = insert_before_folds(notes[review], 1,
    '### Deliverables · 复习目标与题目交付物\n\n' + original(review, 'Core Definition · 核心目标'))
notes[review] = insert_before_folds(notes[review], 7,
    '### English Exam Q&A · 常用完整答句\n\n' + original(review, 'English Exam Q&A · 常用完整答句') + '\n\n' +
    '### Closed-Book Check · 考前自查与错题归因\n\n' + original(review, 'Method and Review · 考前自查'))

routes = {
 'Digital Abstraction and System Design': {'Core Definition':1, 'Assumptions':1, 'Derivation':3, 'Worked':3, 'Method':5, 'Connections':5},
 'Digital Waveforms': {'Core Definition':2, 'Derivation':4, 'Worked':4, 'Pitfalls':5, 'Connections':5},
 'AND-OR and AND-OR-Invert Logic': {'Core Definition':2, 'Logic Levels':2, 'Worked Example 1':2, 'Worked Example 2':3, 'Worked Example 3':3, 'XOR':7, 'Quick Check':7, 'Sources':8, 'Connections':7},
 'Combinational Logic Analysis': {'Scope':5, 'Read':5, 'Worked':5, 'Bubble':5, 'Limits':5, 'Exam':5, 'Sources':8, 'Connections':7},
 'Combinational Logic Design': {'Core':1, 'Derivation':1, 'Worked Example 1':3, 'Worked Example 2':4, 'Worked Example 3':6, 'Worked Example 4':6, 'Priority':7, 'Chapter':7, 'Pitfalls':7, 'Connections':7, 'Sources':8},
 'Universal Gates and Bubble Pushing': {'Core':1, 'Derivation':1, 'Bubble':3, 'Worked Example 4':4, 'Worked Examples':2, 'Method':5, 'Connections':5, 'Sources':6},
 'Digital Logic Troubleshooting': {'Core':1, 'Assumptions':1, 'Derivation':2, 'Worked Example 1':3, 'Worked Example 2':3, 'Worked Example 3':4, 'Method':5, 'Common':5, 'English':5},
 'Exam Review and Problem Solving': {'Core':1, 'Learning':1, 'Read':2, 'Number':3, 'Boolean':4, 'Gate':4, 'Timing':5, 'State':5, 'Counter':5, 'VHDL':6, 'Checking':7, 'English':7, 'Method':7},
}
skip = re.compile(r'^(Core Definition|Assumptions|Method|Connections|Pitfalls(?: and Review)?\s*·|Exam English(?: and Connections| and Review)?\s*·|English Exam Q&A|Quick Check|Exam Recall)', re.I)
for g in mine:
    t = notes[g['target']]
    out = WORK / 'draft/Notes' / (g['target'] + '.md')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(t, 'utf-8')
    h2 = re.findall(r'^## ([^\n]+)', t, re.M)
    for name in g['sources']:
        raw = (OLD / 'original-Notes' / (name + '.md')).read_text('utf-8')
        for heading in re.findall(r'^## ([^\n]+)', raw, re.M):
            ix = next((i for p, i in routes[name].items() if heading.startswith(p)), 1)
            ix = min(ix, len(h2))
            coverage.append({'source':name, 'source_heading':heading, 'target':g['target'], 'target_heading':h2[ix-1],
                'status':'restored' if skip.search(heading) else 'preserved',
                'detail': 'Merged into visible definitions, conditions, procedure or recall; repeated formulas use the same authoritative explanation.' if skip.search(heading) else 'Original detailed derivation, example, figure or special discussion remains in the matching section.'})
(WORK / 'coverage-root.json').write_text(json.dumps(coverage, ensure_ascii=False, indent=2), 'utf-8')
print(json.dumps({'drafts':len(notes), 'source_sections':len(coverage), 'visible_layers_restored':sum(x['status']=='restored' for x in coverage)}, ensure_ascii=False))
