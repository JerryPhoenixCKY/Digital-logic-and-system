from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
BASE = ROOT / '.scratch' / 'consolidation-20261008'
DEST = WORK / 'draft' / 'Notes'
GROUPS = json.loads((BASE / 'mapping.json').read_text('utf-8'))['groups']
LINKS = json.loads((BASE / 'link-mapping.json').read_text('utf-8'))
SELECTED = [g for g in GROUPS if g['chapter'] in {'Ch6', 'Ch7', 'Ch8', 'Ch9', 'Ch10', 'Ch11', 'HDL'}]
assert len(SELECTED) == 16

# Reuse the established routing data without importing its file-writing code.
tree = ast.parse((BASE / 'assemble.py').read_text('utf-8'))
ROUTES = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROUTES' for t in n.targets))
CURRENT = {g['target']: (ROOT / 'Notes' / (g['target'] + '.md')).read_text('utf-8') for g in SELECTED}
HEADINGS = {g['target']: re.findall(r'^## ([^\n]+)', (ROOT / 'Notes' / (g['target'] + '.md')).read_text('utf-8'), re.M) for g in GROUPS}
SOURCE_GROUP = {s: g for g in GROUPS for s in g['sources']}
SKIP = re.compile(r'^(Core Definition|Assumptions|Method|Connections|Pitfalls(?: and Review)?\s*·|Exam English(?: and Connections| and Review)?\s*·|English Exam Q&A|Quick Check|Exam Recall)', re.I)

def route(source, heading):
    for pattern, ix in ROUTES.get(source, []):
        if re.search(pattern, heading, re.I):
            return ix
    return HEADINGS[SOURCE_GROUP[source]['target']].index(LINKS[source]['heading']) + 1

def links(text):
    def sub(m):
        if m[1]:
            return m[0]
        full, sep, label = m[2].partition('|')
        name, hashmark, anchor = full.partition('#')
        if name not in LINKS:
            return m[0]
        data = LINKS[name]
        target = data['target']
        if name == target and not hashmark:
            return m[0]
        heading = data['heading']
        if hashmark and name in SOURCE_GROUP:
            heading = HEADINGS[target][route(name, anchor) - 1]
        return '[[' + target + '#' + heading + '|' + (label if sep else name) + ']]'
    return re.sub(r'(!?)\[\[([^\]]+)\]\]', sub, text)

def clean(text):
    text = re.sub(r'^索引：.*$', '', text, flags=re.M)
    text = re.sub(r'\n---\s*$', '', text)
    text = re.sub(r'^> \[!([A-Z]+)\][+-]?\s*(.*)$', r'**\2**', text, flags=re.M)
    text = re.sub(r'^> ?', '', text, flags=re.M)
    text = re.sub(r'^#{3,6} (.+)$', r'**\1**', text, flags=re.M)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def normalized(text):
    text = re.sub(r'^> ?', '', text, flags=re.M)
    text = re.sub(r'!?\[\[([^\]]+)\]\]', lambda m: m[1].split('|')[-1].split('#')[0], text)
    text = re.sub(r'^#{1,6} ', '', text, flags=re.M)
    text = text.replace('**', '')
    return re.sub(r'\s+', '', text)

def source_sections(raw):
    pp = re.split(r'^## ([^\n]+)\n', raw, flags=re.M)
    return list(zip(pp[1::2], pp[2::2]))

def quoted_section(heading, body):
    raw = '**' + heading + '**\n\n' + links(clean(body))
    return '\n'.join('> ' + line if line else '>' for line in raw.splitlines())

def visible_section(heading, body):
    body = re.sub(r'^索引：.*$', '', body, flags=re.M)
    body = re.sub(r'\n---\s*$', '', body).strip()
    body = re.sub(r'^### ', '#### ', body, flags=re.M)
    return '### ' + heading + '\n\n' + links(body)

# The original links carry useful prerequisite/application relationships.
# Turn link-only clouds into a short explanation beside their own topic.
RELATION = {
 'Half Adder and Full Adder': '[[Binary Arithmetic]] 提供位宽与数值核对；[[Exclusive-OR Gate]] 与 [[Parity Bit]] 解释 sum 的奇偶性；单元级 carry 连接成 [[Ripple Carry and Carry Look-Ahead Adders]]，相同单元也压缩 [[Combinational Multiplier]] 的同权列。',
 'Ripple Carry and Carry Look-Ahead Adders': '从 [[Half Adder and Full Adder]] 的单级 carry 递推展开；[[Two\'s Complement Representation]] 决定有符号结果解释；[[Propagation Delay and Logic Hazards]] 给出路径延迟模型，[[Setup and Hold Timing]] 把加法路径纳入寄存器间的时间预算。',
 'Binary Subtractors and Adder-Subtractors': '用 [[Binary Arithmetic]] 的整数守恒校验 borrow；[[Two\'s Complement Representation]] 使减法复用 [[Half Adder and Full Adder]]；也可把真值表交给 [[Decoder]] 实现。',
 'Combinational Multiplier': '[[Binary Arithmetic]] 决定结果位宽，[[AND Gate]] 形成部分积，[[Half Adder and Full Adder]] 合并同权列；[[Ripple Carry and Carry Look-Ahead Adders]] 提供加法子结构，最长路径仍按 [[Propagation Delay and Logic Hazards]] 的规则计算。',
 'Magnitude Comparator': '[[Exclusive-NOR Gate]] 构成逐位 equality；[[Two\'s Complement Representation]] 改变 signed 比较含义；按 [[Combinational Logic Design]] 的规范验证，再与 [[Encoder and Priority Encoder]] 比较“最高位优先”的门控思路；[[Cascaded Counters and Digital Clocks]] 展示比较/末态判断的系统应用。',
 'Encoder and Priority Encoder': '依 [[Combinational Logic Design]] 确定优先级和 valid；它与 [[Decoder]] 的信息方向相反；输入 X 的压缩含义须与 [[Karnaugh Map with Don\'t Cares]] 区分。门实现可用 [[Universal Gates and Bubble Pushing]]；[[Shift Registers]] 提供扫描码，[[Magnitude Comparator]] 同样使用较高位优先的屏蔽结构。',
 'Decoder': '每条线对应 [[Minterm and Maxterm]] 的一行；可实现 [[Half Adder and Full Adder]] 或 [[Binary Subtractors and Adder-Subtractors]] 的 ON sets。与 [[Encoder and Priority Encoder]] 比较码→线/线→码方向；用于 [[Memory Arrays and Expansion]] 的地址片选与 [[Seven-Segment Display and Code Conversion]] 的显示转换。',
 'Multiplexer and Demultiplexer': '由 [[Truth Table and Boolean Expression]] 求 cofactors；[[Decoder]] 的 enable 可在极性合适时作 DEMUX data。[[Magnitude Comparator]] 驱动最小值选择；[[Register Enable and Reset]] 用反馈 MUX 实现保持；[[Shift Registers]] 选择相邻位，[[Read-Only Memory and Programmable Logic Arrays]] 提供查表实现的对照。',
 'Propagation Delay and Logic Hazards': '[[Combinational Circuit]] 的无环模型允许逐路径求延迟；[[Karnaugh Map]] 的邻格共同覆盖可检查单输入静态冒险；[[Universal Gates and Bubble Pushing]] 改变实现路径，[[Digital Waveforms]] 描述瞬态，最终采样窗口由 [[Setup and Hold Timing]] 约束。',
 'Sequential Logic': '与 [[Combinational Circuit]] 比较是否需要历史；[[Set-Reset Latch]] 的反馈和 [[D Latch and D Flip-Flop]] 的捕获提供状态单元，再组成 [[Finite State Machine]]、[[Counters]] 与 [[Shift Registers]]。',
 'Set-Reset Latch': '[[NOR Gate]] 与 [[NAND Gate]] 决定控制极性；反馈是 [[Sequential Logic]] 的最小存储例子，受控输入形成 [[D Latch and D Flip-Flop]]。禁态释放的不确定性与 [[Metastability and Clock Domain Crossing]] 的物理问题相联系。',
 'D Latch and D Flip-Flop': '用 [[Digital Waveforms]] 追踪透明窗口与边沿；[[Register Enable and Reset]] 增加控制，[[JK and T Flip-Flops]] 给出其他更新规则；采样必须满足 [[Setup and Hold Timing]]，可用 [[VHDL Language and Modeling]] 描述并组成 [[Shift Registers]]。',
 'JK and T Flip-Flops': '通过 [[D Latch and D Flip-Flop]] 与 [[Multiplexer and Demultiplexer]] 实现相同特征函数；[[Synchronous Counter Design]] 反向查激励表，[[Karnaugh Map with Don\'t Cares]] 化简有根据的 X；所有 next states 仍遵守 [[Sequential Logic]] 的统一旧状态更新。',
 'Register Enable and Reset': '[[D Latch and D Flip-Flop]] 提供采样元件，[[Multiplexer and Demultiplexer]] 在 D 路径选择 load/feedback；控制应用于 [[Shift Registers]] 与 [[Counters]]，且 EN、同步控制须满足 [[Setup and Hold Timing]]；[[VHDL Language and Modeling]] 用分支位置表达复位语义。',
 'Shift Registers': '[[D Latch and D Flip-Flop]] 组成各级，[[Multiplexer and Demultiplexer]] 选择模式，[[Register Enable and Reset]] 明确控制；反馈变体见 [[Ring and Johnson Counters]]，线性反馈运算与 [[Cyclic Redundancy Check]] 相联系；[[Structural Shift Register Project]] 只实现本课的四位双向移位子集。',
 'Ring and Johnson Counters': '由 [[Shift Registers]] 改接反馈得到循环，[[Register Enable and Reset]] 建立合法 seed；[[Encoder and Priority Encoder]] 把扫描线路变成位置码。它们与 [[Counters]] 的二进制递增机制不同，非法码策略须结合 [[State Encoding and Unused States]]。',
 'Keyboard Scanning and Encoding': '[[Ring and Johnson Counters]] 与 [[Shift Registers]] 产生行扫描；[[Encoder and Priority Encoder]] 编位置，[[One-Shots and Pulse Applications]] 控制延迟捕获；[[Cascaded Counters and Digital Clocks]] 产生扫描事件；[[JK and T Flip-Flops]] 保存按键码，[[Read-Only Memory and Programmable Logic Arrays]] 变成字符；异常按 [[Digital Logic Troubleshooting]] 逐级定位。',
 'Finite State Machine': '[[Sequential Logic]] 提供状态递推模型；[[Moore and Mealy Machines]] 指定输出依赖，[[State Encoding and Unused States]] 指定表示与恢复。[[Sequence Detector]]、[[Traffic Light Controller]] 与 [[Synchronous Counter Design]] 是不同状态语义的应用，最后通过 [[VHDL Language and Modeling]] 实现。',
 'Moore and Mealy Machines': '在 [[Finite State Machine]] 框架中比较输出函数；[[Sequence Detector]] 与 [[Traffic Light Controller]] 给出时序窗口和控制应用；接收输出须满足 [[Setup and Hold Timing]]，[[Testbench and Functional Verification]] 应分别检查 edge 前与 edge 后的有效窗口。',
 'State Encoding and Unused States': '[[Bits and Bytes]] 给出编码容量；[[Karnaugh Map with Don\'t Cares]] 只能使用规范许可的 X；[[Finite State Machine]] 的语义在不同编码中应一致。[[Ring and Johnson Counters]] 与 [[Synchronous Counter Design]] 展示非法循环/恢复，[[Field-Programmable Gate Array]] 的映射决定实际资源与时延。',
 'Sequence Detector': '先按 [[Finite State Machine]] 定义有用历史，再按 [[Moore and Mealy Machines]] 规定检测窗口，以 [[State Encoding and Unused States]] 编码；[[Shift Registers]] 是保存全部最近符号的另一思路；重叠、复位和边界由 [[Testbench and Functional Verification]] 核对。',
 'Traffic Light Controller': '状态与输出分别依 [[Finite State Machine]]、[[Moore and Mealy Machines]] 建模；[[Decoder]] 把灯编码映射为控制，[[Counters]] 与 [[Cascaded Counters and Digital Clocks]] 提供时长事件；所有采样与输出接收仍受 [[Setup and Hold Timing]] 约束。',
 'Setup and Hold Timing': '[[Propagation Delay and Logic Hazards]] 提供最长/最短路径，[[D Latch and D Flip-Flop]] 提供采样窗口；[[Sequential Logic]] 的状态递推以这些物理条件为前提。异步关系需另外按 [[Metastability and Clock Domain Crossing]] 处理，[[Field-Programmable Gate Array]] 用约束和实现后报告检验预算。',
 'Metastability and Clock Domain Crossing': '[[Setup and Hold Timing]] 说明违反窗口的来源，[[Register Enable and Reset]] 的复位释放也涉及跨域；[[Gray Code]] 约束相邻码变化，[[Digital Abstraction and System Design]] 解释数字模型的物理边界。[[One-Shots and Pulse Applications]] 的事件不可直接当慢 level 同步，[[Testbench and Functional Verification]] 还须验证协议完整性。',
 'Counters': '[[JK and T Flip-Flops]] 给出 toggle 元件，[[Synchronous Counter Design]] 从状态表求激励；[[Ring and Johnson Counters]] 是另一类循环状态编码，[[Cascaded Counters and Digital Clocks]] 按 rollover 扩展；decode 的瞬态由 [[Propagation Delay and Logic Hazards]] 分析。',
 'Synchronous Counter Design': '先由 [[Counters]] 确定序列，按 [[JK and T Flip-Flops]] 查激励，再用 [[Karnaugh Map]] 化简；[[State Encoding and Unused States]] 定义恢复。它是 [[Finite State Machine]] 设计的一种，最终全状态检查见 [[Testbench and Functional Verification]]。',
 'Cascaded Counters and Digital Clocks': '[[Counters]] 定义各级模数，[[Register Enable and Reset]] 定义接受条件与优先级；[[Decoder]] 产生 terminal predicate，供 [[Traffic Light Controller]] 等定时应用。不要把 [[Propagation Delay and Logic Hazards]] 中的 decode 毛刺当 clock；异常进位可按 [[Digital Logic Troubleshooting]] 追踪。',
 'Memory Arrays and Expansion': '[[Bits and Bytes]] 与 [[Hexadecimal Number System]] 提供容量单位和地址范围；[[Decoder]] 选行/选 bank，[[Tri-State Buffers and Bus Drivers]] 管共享读总线；[[SRAM DRAM and ROM]] 解释保存机制，[[Read-Only Memory and Programmable Logic Arrays]] 把组织用于真值表实现。',
 'SRAM DRAM and ROM': '逻辑组织见 [[Memory Arrays and Expansion]]；SRAM 的双稳态与 [[Set-Reset Latch]] 相近。[[Read-Only Memory and Programmable Logic Arrays]] 使用存储作函数表，[[Field-Programmable Gate Array]] 区分配置与运行状态；器件机制与 [[Digital Abstraction and System Design]] 的功能抽象要分开。',
 'Read-Only Memory and Programmable Logic Arrays': '[[Sum-of-Products Form]] 与 [[Minterm and Maxterm]] 分别解释 PLA 乘积和 ROM 行；[[Decoder]] 与 [[Memory Arrays and Expansion]] 提供地址结构。[[Field-Programmable Gate Array]] 采用 LUT/FF 资源，[[Seven-Segment Display and Code Conversion]] 是多输出查表的应用。',
 'Field-Programmable Gate Array': '[[Read-Only Memory and Programmable Logic Arrays]] 解释 LUT，[[Sequential Logic]] 解释 FF 的运行状态；用 [[VHDL Language and Modeling]] 建模并在 [[Structural Shift Register Project]] 练习连接；[[Testbench and Functional Verification]] 检查功能，[[Setup and Hold Timing]] 检查实现时间。',
 'Testbench and Functional Verification': '语言调度见 [[VHDL Language and Modeling]]；本例 DUT 为 [[Structural Shift Register Project]]，同样方法用于 [[Sequence Detector]] 与 [[Synchronous Counter Design]]。功能覆盖之外还要检查 [[Field-Programmable Gate Array]] 的映射与 [[Setup and Hold Timing]] 的路径条件。',
 'Structural Shift Register Project': '[[VHDL Language and Modeling]] 提供实例化语法，[[D Latch and D Flip-Flop]] 是状态单元，[[Shift Registers]] 提供方向递推，[[Multiplexer and Demultiplexer]] 选择每位来源；[[Testbench and Functional Verification]] 提供独立测试，[[Field-Programmable Gate Array]] 完成映射与约束检查。',
}

# Promote governing models/tables; leave lengthy numerical traces and complete
# implementation examples as the existing local expandable blocks.
PROMOTE = {
 ('Half Adder and Full Adder', 'Derivation'): 1,
 ('Binary Subtractors and Adder-Subtractors', 'Derivation'): 3,
 ('Decoder', 'Enable and Pin Constraints'): 2,
 ('Set-Reset Latch', 'NAND Variant'): 2,
 ('D Latch and D Flip-Flop', 'Comparison'): 3,
 ('JK and T Flip-Flops', 'Excitation Table'): 4,
 ('JK and T Flip-Flops', 'Conversion'): 4,
 ('Register Enable and Reset', 'Reset and Set'): 5,
 ('Register Enable and Reset', 'Timing Boundary'): 5,
 ('Shift Registers', 'Derivation'): 1,
 ('Keyboard Scanning and Encoding', 'Mechanism'): 1,
 ('Keyboard Scanning and Encoding', 'Debounce and Capture'): 3,
 ('Keyboard Scanning and Encoding', 'Multi-key Boundary'): 4,
 ('Finite State Machine', 'State Meaning and Completeness'): 1,
 ('Moore and Mealy Machines', 'Output Timing'): 2,
 ('Moore and Mealy Machines', 'Tradeoffs'): 2,
 ('State Encoding and Unused States', 'Don\'t-Care Policy'): 3,
 ('Sequence Detector', 'Specification'): 4,
 ('Sequence Detector', 'Encoded Equations'): 4,
 ('Traffic Light Controller', 'Specification'): 5,
 ('Traffic Light Controller', 'Transition Table'): 5,
 ('Traffic Light Controller', 'Derivation'): 5,
 ('Traffic Light Controller', 'Timer Extension'): 5,
 ('Setup and Hold Timing', 'Definitions and Assumptions'): 1,
 ('Metastability and Clock Domain Crossing', 'Validity Boundaries'): 4,
 ('Synchronous Counter Design', 'Design Method'): 2,
 ('Synchronous Counter Design', 'JK Design'): 2,
 ('Memory Arrays and Expansion', 'Width Expansion'): 2,
 ('Memory Arrays and Expansion', 'Depth Expansion'): 2,
 ('Memory Arrays and Expansion', 'Interface and Timing'): 4,
 ('Read-Only Memory and Programmable Logic Arrays', 'ROM versus PLA versus LUT'): 2,
 ('VHDL Language and Modeling', 'Types and Operators'): 1,
 ('VHDL Language and Modeling', 'Coding Review and Boundaries'): 3,
 ('Testbench and Functional Verification', 'Test Dimensions'): 5,
 ('Structural Shift Register Project', 'Specification and Boundary'): 1,
 ('Structural Shift Register Project', 'Verification Plan'): 3,
 ('Structural Shift Register Project', 'Pitfalls and Exam English'): 4,
}

ADDITIONS = {
 ('Sequential Logic and Flip-Flops', 5): r'''### Reset timing · 复位输入与释放窗口

同步复位 (synchronous reset) 与 EN 一样，通过有效捕获边沿发挥作用，其路径检查是 setup/hold。异步复位 (asynchronous reset) 断言 (assertion) 可独立于 clock 清零，但解除断言 (deassertion) 必须避开器件规定的释放窗口：恢复时间 (recovery time) 是有效时钟边沿前所需的释放提前量；移除时间 (removal time) 是有效时钟边沿后所需的继续保持量，类比 setup/hold，却检查异步控制端。

这些是具体器件的时序要求，不是从“异步”一词推出的零延迟保证；还须满足最小复位脉宽。异步断言、同步释放 (asynchronous assertion, synchronous deassertion) 的结构须按每个目标时钟域实现并验证，保证各位一致退出复位。''',
 ('Sequential Timing and Clock Domain Crossing', 2): r'''### Timing slack · 时间裕量

在第 1 节的偏斜约定下，定义建立裕量 (setup slack) 和保持裕量 (hold slack)：

$$\text{slack}_{setup}=T+s-t_{pcq}-t_{pd}-t_{setup},$$
$$\text{slack}_{hold}=t_{ccq}+t_{cd}-t_{hold}-s.$$

所有量使用同一时间单位；大于等于 0 表示在本模型下通过。时钟不确定度、抖动与额外余量须按题目/约束加入，不可把以上理想预算当器件保证。先由 setup 得候选周期，再验证 hold；负 hold slack 不会因单独增大 T 自动变正。''',
 ('Finite State Machine Design and Applications', 5): r'''### Safe recovery · 安全恢复的范围

本四态二进制教学例已使用 00–11 全部编码，因此没有可供“其余码”恢复的二进制状态；reset→A 是该模型的规定起点，并不等于真实交通系统必须选择的安全重启状态。若新增 all-red、计时状态或采用 one-hot 编码，应分别规定非法编码时的灯输出和下一态，核对是否能进入安全状态并继续运行。

完整验证同时检查输出不冲突、最短黄灯/清空时长、最大绿灯/公平性、输入事件与复位恢复。综合后的 FSM 编码与恢复逻辑也要与这些要求一致；仅在 RTL 中写 `others` 不能证明物理系统的全部安全性质。''',
 ('Memory Organization and Technologies', 1): r'''### Capacity units · 容量单位与非二幂深度

本课容量例题中的 8K words 约定为 $8\times1024=8192$ words；容量用 KiB 明确二进制字节前缀。十进制 k/M 与二进制 Ki/Mi 不能混算。若实际深度 D 不是二的整数次幂，需要 $a=\lceil\log_2D\rceil$ 个地址 bit，但 $2^a-D$ 个地址模式不对应有效 word，应规定其行为。数据线数对应 W，不是 C；扩大 W 而不扩大 D 不增加逻辑地址位数。''',
 ('VHDL Modeling and Verification', 2): r'''### Assignment scheduling · 同一过程内的赋值调度

signal 赋值 (`<=`) 安排后续更新，过程本次激活中的后续语句仍读取未更新的 signal 值；variable 赋值 (`:=`) 则供后续语句立即读取。对同一 signal 的同一零延迟更新时刻，单次过程激活中后面的赋值覆盖前面的安排，例如连续写两次 `count <= count + 1;` 不表示同一拍加 2。对不同信号的赋值则分别生效，`q1 <= d; q2 <= q1;` 正好形成两级寄存器。

process 的顺序语句 (sequential statements) 是模拟执行语义；组合/时序硬件的区别由敏感事件、时钟条件及是否需要保持历史决定。architecture 中多个 process 与 concurrent assignments 并行响应其触发事件。''',
 ('VHDL Modeling and Verification', 1): r'''### Numeric width · 数值类型与算术位宽

完整算术代码需同时引入 `use ieee.std_logic_1164.all;` 和 `use ieee.numeric_std.all;`。例如 a、b 都是 `std_logic_vector(3 downto 0)`，s5 是五位 unsigned，可写 `s5 <= resize(unsigned(a), 5) + resize(unsigned(b), 5);`；先扩宽操作数再相加，才能保留第 5 位进位。`signed` 扩宽作符号扩展，`unsigned` 扩宽作零扩展；转换只解释同一位串，不自动修复此前已截断的结果。''',
 ('Structural Shift Register Project', 4): r'''### Feature boundary · 教学实现与扩展接口

当前 `bidir4` 只有 `clk, rst, right_left, sr, sl, q` 接口，每个有效正沿执行一次左移或右移；高有效 rst 在边沿之间也可清零。它没有 EN、hold mode 或 parallel-load 数据端口。若要扩展为通用寄存器，需明确新增接口、选择分支、复位优先级与对应测试；[[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|通用移位寄存器]] 的四种模式不能当成现有代码已支持的功能。''',
}

coverage = []
actions = []
original_section_count = 0
for g in SELECTED:
    target = g['target']
    text = CURRENT[target]
    restored = defaultdict(list)
    reviews = defaultdict(list)
    promoted = defaultdict(list)
    records = []
    for source in g['sources']:
        raw = (BASE / 'original-Notes' / (source + '.md')).read_text('utf-8')
        sections = source_sections(raw)
        for heading, body in sections:
            original_section_count += 1
            ix = route(source, heading)
            source_key = heading.split(' · ')[0]
            record = {'source': source, 'source_section': heading, 'target': target,
                      'status': 'covered', 'target_section': HEADINGS[target][ix - 1],
                      'target_subsection': heading,
                      'coverage_note': '原稿内容已在当前对应正文/本节折叠推导例题中保留。'}
            if heading.startswith('Sources'):
                record['target_section'] = 'Sources · 课件依据'
                record['target_subsection'] = None
                record['coverage_note'] = '保留原来源条目及主线课件链接。'
                records.append(record)
                continue
            if SKIP.search(heading):
                original = links(clean(body))
                if normalized(original) in normalized(text):
                    record['coverage_note'] = '整节已覆盖；不重复添加。'
                else:
                    if source_key == 'Connections' and source in RELATION:
                        fragment = visible_section('Connections · 概念关系与应用', RELATION[source])
                        record['coverage_note'] = '原关系中的所有链接改为 canonical+对应主小节，按先修、实现与应用写为本地说明。'
                        record['target_subsection'] = 'Connections · 概念关系与应用'
                    else:
                        fragment = visible_section(heading, body)
                        record['coverage_note'] = '补回此前省略的完整定义/条件/方法/误区/英文答句，放在本主题对应小节；无新增备份附录。'
                    if re.match(r'^(Core Definition|Assumptions)', heading):
                        restored[ix].append(fragment)
                    else:
                        reviews[ix].append(fragment)
                    record['status'] = 'restored'
                    actions.append({'source': source, 'heading': heading, 'action': 'restore', 'target': target, 'section': ix})
            elif (source, source_key) in PROMOTE or (source == 'Seven-Segment Display and Code Conversion' and source_key in {'Truth Table and Polarity', 'Derivation'}):
                chunk = quoted_section(heading, body)
                if chunk not in text:
                    raise AssertionError(('Unable to locate intact current fragment', source, heading))
                text = text.replace(chunk, '', 1)
                if source == 'Seven-Segment Display and Code Conversion' and source_key == 'Derivation':
                    children = re.split(r'^### ([^\n]+)\n', body, flags=re.M)
                    child_ixs = [2, 3, 4]
                    if children[0].strip():
                        promoted[2].append(links(children[0].strip()))
                    for ci, dest_ix in zip(range(1, len(children), 2), child_ixs):
                        promoted[dest_ix].append(visible_section(children[ci], children[ci + 1]))
                    record['target_section'] = [HEADINGS[target][v - 1] for v in child_ixs]
                    record['target_subsection'] = [children[ci] for ci in range(1, len(children), 2)]
                    record['coverage_note'] = '原段逻辑、消隐与扫描分别完整移到第2/3/4节正文，推导公式和表格未删。'
                else:
                    ix = 1 if source == 'Seven-Segment Display and Code Conversion' else PROMOTE[(source, source_key)]
                    promoted[ix].append(visible_section(heading, body))
                    record['target_section'] = HEADINGS[target][ix - 1]
                    record['coverage_note'] = '内容原已保留；从折叠例题提升为对应正文的规则/表格/边界，逐行内容保持。'
                actions.append({'source': source, 'heading': heading, 'action': 'promote', 'target': target, 'section': ix})
            records.append(record)
            # Account for every original H3 as well as its parent H2.
            for child in re.findall(r'^### ([^\n]+)', body, re.M):
                child_record = dict(record)
                child_record['source_section'] = heading + ' > ' + child
                child_record['target_subsection'] = child
                if source == 'Seven-Segment Display and Code Conversion' and source_key == 'Derivation':
                    cix = {'Segment logic · 段逻辑': 2, 'Blanking and zero suppression · 消隐与零抑制': 3, 'Dynamic multiplexing · 动态扫描': 4}[child]
                    child_record['target_section'] = HEADINGS[target][cix - 1]
                records.append(child_record)
    # Remove only empty wrappers left after promotion; retained example bodies
    # remain byte-equivalent after link/blockquote normalization.
    text = re.sub(r'(?m)^> \[!example\]- [^\n]+\n(?:\s*\n|^>\s*\n)*(?=^## |^### |^> \[!|\Z)', '', text)
    # A removed quoted fragment can leave unquoted blank lines inside the
    # remaining example. Keep each callout and its body in one blockquote.
    text = re.sub(r'(?m)(^> \[!example\]- [^\n]+\n)(?:\n|>\s*\n)+(?=> (?!\[!))', r'\1>\n', text)
    text = re.sub(r'(?m)\n>\s*\n(?:\n|>\s*\n)+(?=> (?!\[!))', '\n>\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    pp = re.split(r'^## ([^\n]+)\n', text, flags=re.M)
    out = pp[0].rstrip() + '\n\n'
    for pi in range(1, len(pp), 2):
        heading, body = pp[pi], pp[pi + 1].strip()
        ix = (pi + 1) // 2
        if heading.startswith('Sources'):
            out += '## ' + heading + '\n\n' + body + '\n'
            continue
        # Core additions go before examples; review remains within the primary
        # topic after its examples, instead of collecting former notes at end.
        m = re.search(r'(?m)^> \[!example\]- ', body)
        split_at = m.start() if m else len(body)
        intro, detail = body[:split_at].rstrip(), body[split_at:].strip()
        chunks = [intro] + restored[ix] + promoted[ix]
        if (target, ix) in ADDITIONS:
            chunks.append(ADDITIONS[(target, ix)])
        if detail:
            chunks.append(detail)
        chunks += reviews[ix]
        out += '## ' + heading + '\n\n' + '\n\n'.join(c for c in chunks if c) + '\n\n'
    out = re.sub(r'\n{3,}', '\n\n', out)
    # All old conceptual references, including in preserved portions, resolve
    # to the existing canonical filenames and stable primary headings.
    out = links(out)
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / (target + '.md')).write_text(out.rstrip() + '\n', 'utf-8')
    for record in records:
        if record['source'] == 'Register Enable and Reset' and record['source_section'].startswith('Timing Boundary'):
            record['status'] = 'corrected'
            record['coverage_note'] += '补充 recovery/removal 定义；同步 reset 检查 setup/hold，异步 reset 释放另检查 recovery/removal 与最小脉宽。'
        if record['source'] == 'Traffic Light Controller' and record['source_section'].startswith('Specification'):
            record['status'] = 'corrected'
            record['coverage_note'] += '区别四态教学 reset→A 与实际安全恢复；四态二进制已占满编码，无未用二进制码。'
        if record['source'] == 'Structural Shift Register Project' and record['source_section'].startswith(('Specification', 'Verification')):
            record['status'] = 'corrected'
            record['coverage_note'] += '明确现有代码仅四位双向每拍移位+高有效异步复位；hold/load 是扩展，验证不假设其存在。'
    coverage.extend(records)

(WORK / 'coverage-ch6plus.json').write_text(json.dumps({
    'chapters': ['Ch6', 'Ch7', 'Ch8', 'Ch9', 'Ch10', 'Ch11', 'HDL'],
    'target_count': len(SELECTED), 'source_count': sum(len(g['sources']) for g in SELECTED),
    'original_H2_count': original_section_count,
    'scope': '逐原稿H2与H3记录；摘要与frontmatter用于定位概念，并非正文遗漏。现有推导、例题、图示与完整代码全部保留。',
    'status_counts': dict(Counter(r['status'] for r in coverage)),
    'omissions': [], 'sections': coverage, 'actions': actions,
}, ensure_ascii=False, indent=2), 'utf-8')
print(json.dumps({'targets': len(SELECTED), 'source_sections': original_section_count, 'status': dict(Counter(r['status'] for r in coverage)), 'actions': len(actions)}, ensure_ascii=False))
