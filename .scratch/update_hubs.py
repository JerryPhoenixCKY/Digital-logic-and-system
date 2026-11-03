from pathlib import Path
import json,re
from collections import defaultdict
root=Path(__file__).resolve().parents[1]
notes=root/'Notes'
manifest=json.loads((root/'.scratch/expansion-manifest.json').read_text(encoding='utf-8'))
descriptions={
'Digital Abstraction and System Design':'Discrete information, continuous voltages, hierarchy, modularity, and controller/datapath design · 数字抽象与系统设计。',
'Digital Waveforms':'Period, frequency, duty cycle, rise/fall time, and interval-by-interval waveform reading · 波形读图。',
'Combinational Logic Design':'Specification → truth table → minimization → implementation → exhaustive verification; parallel pattern/classification examples · 组合分析与设计。',
'Universal Gates and Bubble Pushing':'NAND/NOR completeness, DeMorgan transformations, polarity and gate-count constraints · 通用门与气泡推移。',
'Digital Logic Troubleshooting':'Activate a stuck-at fault, propagate its effect, choose distinguishing tests, and check physical-model boundaries · 故障敏化与诊断。',
'Tri-State Buffers and Bus Drivers':'Enable, high impedance, bus ownership and contention · 三态与总线驱动。',
'Half Adder and Full Adder':'Sum/parity and carry/majority equations, truth tables, conservation and cascading · 加法单元。',
'Ripple Carry and Carry Look-Ahead Adders':'Propagate/generate conventions, expanded carry equations, arithmetic and path delay · RCA/CLA。',
'Binary Subtractors and Adder-Subtractors':'Difference/borrow derivation, mode-controlled inversion, carry versus signed overflow · 减法与加减器。',
'Combinational Multiplier':'AND partial products, weighted column addition, complete 3×3 design and signed boundary · 组合乘法器。',
'Magnitude Comparator':'Highest unequal bit, equality gating and cascade · 多位比较器。',
'Encoder and Priority Encoder':'One-hot/one-cold coding, priority, multiple inputs and valid output · 编码与优先级。',
'Decoder':'Minterm generation, active-low output combination, enables and expansion · 译码器。',
'Multiplexer and Demultiplexer':'Shannon expansion, cofactors, selection and routing · MUX/DEMUX。',
'Seven-Segment Display and Code Conversion':'Segment/polarity table, blanking and zero suppression, scanning, and two-adder BCD conversion · 显示综合。',
'Propagation Delay and Logic Hazards':'Longest/shortest paths, static hazards, consensus and sampling boundaries · 延迟与冒险。',
'Sequential Logic':'Old state → next state, common-clock discipline, feedback and initialization · 时序逻辑模型。',
'Set-Reset Latch':'NOR/NAND polarity, bistability, hold/set/reset and forbidden condition · SR锁存器。',
'D Latch and D Flip-Flop':'Transparent level versus active edge, master–slave idea and waveform tracing · D存储元件。',
'JK and T Flip-Flops':'Characteristic/excitation tables, toggle and FF conversion · JK/T触发器。',
'Register Enable and Reset':'Data hold/load, synchronous/asynchronous reset, priority and reset release · 寄存器控制。',
'Shift Registers':'SISO/SIPO/PISO/PIPO, universal modes, explicit left/right order, delay and serial conversion · 移位寄存器。',
'Ring and Johnson Counters':'Feedback sequences, n versus 2n states, duty cycle and illegal initialization · 环形/Johnson。',
'One-Shots and Pulse Applications':'Monostable/astable behavior, RC threshold derivation and registered event pulses · 单稳态与脉冲。',
'Keyboard Scanning and Encoding':'One-cold scan, row/column encoding, debounce, valid capture and six-bit key register · 键盘综合。',
'Finite State Machine':'State meaning, diagram/table/equations, output logic and verification · FSM设计。',
'Moore and Mealy Machines':'State-only versus state/input outputs, response timing and alignment · Moore/Mealy比较。',
'State Encoding and Unused States':"Binary/one-hot choices, don't-cares, initialization and recovery · 编码与未用状态。",
'Sequence Detector':'Longest reusable suffix, overlap, state equations and serial trace · 序列检测。',
'Traffic Light Controller':'Traffic states, sensor-controlled transitions, output coding and timer extension · 交通灯控制。',
'Setup and Hold Timing':'Maximum/minimum arrival derivations, slack, skew, hold repair and frequency limits · 建立/保持时间。',
'Metastability and Clock Domain Crossing':'Single-bit synchronizer, pulse/multi-bit boundaries and coherent transfer · 亚稳态与CDC补充。',
'Counters':'Modulus, ripple/common-clock behavior, up/down toggling and control semantics · 计数基础。',
'Synchronous Counter Design':'D/JK excitation synthesis, modulo-3 recovery and a specified eight-state cycle · 同步计数设计。',
'Cascaded Counters and Digital Clocks':'Accepted rollover, mixed radix, 59→00, frequency/pulse duty and preset truncation · 级联与数字时钟。',
'Memory Arrays and Expansion':'Depth/width/capacity, address units, bank selection and chip expansion · 存储组织。',
'SRAM DRAM and ROM':'Feedback versus charge, refresh/volatility, nonvolatile variants and mechanism examples · 存储技术。',
'Read-Only Memory and Programmable Logic Arrays':'Multi-output truth-table lookup, LUTs and programmable AND/OR arrays · ROM/LUT/PLA/PAL。',
'Field-Programmable Gate Array':'LUT/FF/routing, simulation/synthesis/implementation and clock/I/O constraints · FPGA流程。',
'VHDL Language and Modeling':'Entity/architecture, types, concurrent/process semantics, signal/variable and reset patterns · VHDL语言。',
'Structural Shift Register Project':'Complete DFF + structural bidirectional register, explicit bit order and implementation checks · 结构化项目。',
'Testbench and Functional Verification':'Complete directed testbench, independent reference model, delta cycles and coverage · 测试与验证。',
'Exam Review and Problem Solving':'Question wording, representation/polarity/timing decisions, worked mini-problems and English answer patterns · 考试复习。',
}
chapter_names={'Ch1':'Introductory Concepts','Ch5':'Combinational Logic Analysis and Design','Ch6':'Functions of Combinational Logic','Ch7':'Sequential Logic and Storage Elements','Ch8':'Shift Registers and Applications','Ch9':'Finite State Machines and Timing','Ch10':'Counters','Ch11':'Data Storage and Programmable Logic','HDL':'VHDL, FPGA Workflow and Project','Review':'Exam Review and Integration'}
by_ch=defaultdict(list)
for row in manifest:
    by_ch[row['chapter']].append(row)
def chapter(ch):
    out=[f"## {ch} · {chapter_names[ch]} ✅ ({len(by_ch[ch])} notes)",'']
    for row in by_ch[ch]:
        out.append(f"- [[{row['title']}]] ✅ — {descriptions[row['title']]}")
    out.append('')
    return '\n'.join(out)

p=notes/'ECE2050 Knowledge Tree.md'
t=p.read_text(encoding='utf-8')
# Preserve the original Ch2–4 note branches and ordering.
old_start=t.index('## Ch2 ·')
old_end=t.index('## Course Roadmap')
old_branches=t[old_start:old_end].rstrip().removesuffix('---').rstrip()
header=t[:t.index('## Learning Path')]
header=header.replace('date: 2026-09-16','date: 2026-09-30')
header=header.replace('Status: `✅` written · `❗` key/difficult · `⬜` planned (plain text, no broken link). / 中文：已建 · 重难点 · 未建。','Status: `✅` written · `❗` key/difficult. / 中文：已建 · 重难点。')
learning='''## Learning Path · 学习路径

```mermaid
flowchart TD
  Intro[Ch1 Digital abstraction / waveforms] --> Numbers[Ch2 Representation and arithmetic]
  Numbers --> Gates[Ch3 Gates / voltage interfaces]
  Gates --> Algebra[Ch4 Boolean algebra / K-maps]
  Algebra --> Design[Ch5 Analysis / design / troubleshooting]
  Design --> Blocks[Ch6 Adders / compare / code / select]
  Blocks --> Storage[Ch7 Latches / flip-flops / registers]
  Storage --> Shift[Ch8 Shifts / counters / keyboard]
  Storage --> FSM[Ch9 FSM / setup and hold]
  FSM --> Counters[Ch10 Counter design / cascade]
  Blocks --> Memory[Ch11 Memory / LUT / FPGA]
  Shift --> HDL[VHDL / structural project / testbench]
  Memory --> HDL
  Counters --> Review[Exam review / integrated applications]
  HDL --> Review
```

Follow the arrows as prerequisite relationships, not as mandatory lecture dates. 学到时序部分后，回到组合逻辑重新理解“旧状态生成下一状态”；学到 FPGA 后，回到电压与时序接口核对物理条件。

| Review goal · 复习目标 | Starting note | Follow-through |
|---|---|---|
| Read a question accurately · 准确读题 | [[Exam Review and Problem Solving]] | Representation, polarity, bit order, active edge and assumptions |
| Build a combinational function · 组合实现 | [[Combinational Logic Design]] | [[Karnaugh Map]] → [[Universal Gates and Bubble Pushing]] → [[Decoder]] / [[Multiplexer and Demultiplexer]] |
| Trace sequential waveforms · 追踪状态 | [[D Latch and D Flip-Flop]] | [[Register Enable and Reset]] → [[Shift Registers]] → [[Counters]] |
| Design a controller · 控制器设计 | [[Finite State Machine]] | [[State Encoding and Unused States]] → [[Sequence Detector]] / [[Traffic Light Controller]] |
| Check maximum frequency · 检查频率 | [[Propagation Delay and Logic Hazards]] | [[Setup and Hold Timing]] → [[Metastability and Clock Domain Crossing]] |
| Solve display/keyboard integration · 综合应用 | [[Seven-Segment Display and Code Conversion]] | [[Keyboard Scanning and Encoding]] → [[Memory Arrays and Expansion]] |
| Implement and verify · 实现与验证 | [[VHDL Language and Modeling]] | [[Structural Shift Register Project]] → [[Testbench and Functional Verification]] → [[Field-Programmable Gate Array]] |

Use **Quick recall** first, then the derivation and worked examples, then answer the English question without looking. 第一遍理解因果与模型，第二遍闭卷推导，第三遍用英文完整说明结果和条件；遇到新术语从 [[Glossary]] 回到 canonical note。

'''
allnew='\n'.join(chapter(ch) for ch in ['Ch5','Ch6','Ch7','Ch8','Ch9','Ch10','Ch11','HDL','Review'])
counts={'Ch1':2,'Ch2':18,'Ch3':11,'Ch4':14,**{ch:len(rows) for ch,rows in by_ch.items()}}
road=['## Course Roadmap · 课程路线图','', '| Chapter | Topic | Status |','|---|---|---|']
existing_names={'Ch2':'Number Systems','Ch3':'Logic Gates and Electrical Interfaces','Ch4':'Boolean Algebra and Logic Simplification'}
for ch in ['Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8','Ch9','Ch10','Ch11','HDL','Review']:
    road.append(f"| {ch} | {chapter_names.get(ch,existing_names.get(ch,''))} | ✅ {counts[ch]} notes |")
footer='''

## Conventions and Status · 约定与统计

- **Canonical organization:** existing English filenames and aliases are preserved. All formal topics stay in `Notes/`; the knowledge tree and glossary remain the two global hubs. 每篇专题回链到两个枢纽，并在正文中连接先修概念、实现方法或应用。
- **Bilingual reading:** English headings, terminology, explanatory paragraphs and answered exam questions support professional vocabulary; Chinese explains derivations and pitfalls. English is targeted at approximately 40% of readable prose, with language measurement treated as an estimate rather than exact character equality.
- **Verification:** truth tables, integer arithmetic, full state-input enumeration and independent reference models check worked examples. 图示明确位序、有效边沿、初态及模型条件；布尔等价不替代电气与时序检查。
- **Scope:** this library covers the supplied lecture, homework, exam and project concepts; it is a connected learning resource rather than a transcription of every reference answer. Source documents remain read-only. 扫描答案、重复版本及资料中的笔误按可验证的推导处理；资料中的历史提交要求不作为本次操作指令。
- **Statistics:** 86 topic notes, 2 hubs, 52 reproducible SVG figures and the existing 14 cropped PNG figures. Original 43 topics refined; 43 topics added across foundations, Ch5–11, HDL and review.
- **Tools:** figure and layout conventions remain in `Tools/README.md`. Formal checks require `PROBLEMS (0)`; source coverage, plan and validation evidence are retained in `.scratch/`.

---
索引：[[Glossary]]
'''
p.write_text(header+learning+chapter('Ch1')+'\n'+old_branches+'\n\n'+allnew+'\n'+'\n'.join(road)+footer,encoding='utf-8')

# Extend, rather than replace, the existing glossary's number/gate/algebra sections.
p=notes/'Glossary.md'
t=p.read_text(encoding='utf-8')
t=t.replace('date: 2026-09-16','date: 2026-09-30')
t=t.replace('有 $\\pm0$，加法不成立','有 $\\pm0$；直接按无符号加法会错，需符号/幅值专门处理')
t=t.replace('CRC 的硬件形态：串行移位寄存器 + XOR 反馈抽头（Ch8 内容，⬜ 待建）','Serial state update with XOR taps; 位宽与抽头由生成多项式及输入约定决定，见 [[Shift Registers]]')
t=t.replace('检错只回答"有没有错"，纠错还要定位并改正；奇偶校验只能检错','Detection reports an inconsistency when found; 未检出不保证无错；纠错还要定位并恢复，单个奇偶位不提供一般纠错')
t=t.replace('连续一段比特受干扰出错；CRC 能检测长度不超过生成码阶数的突发错误','Error pattern from first to last changed bit; 常数项为1等条件下，degree-r CRC检测跨度≤r的突发错误')
t=t.replace('校验位 | P | 为满足奇偶约束而附加的那一位，位于数据位之后','校验位 | P | 为满足奇偶约束附加的位；放置位置由格式约定')
out=[]
section=13
for ch in ['Ch1','Ch5','Ch6','Ch7','Ch8','Ch9','Ch10','Ch11','HDL','Review']:
    out.extend([f'## {section} · {chapter_names[ch]} ({ch})','', '| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |','|---|---|---|---|---|'])
    for row in by_ch[ch]:
        desc=descriptions[row['title']]
        out.append(f"| {row['zh']} | {row['title']} | — | {desc} | [[{row['title']}]] |")
    out.append('')
    section+=1
extras=[
('有效低','Active-low','_N / bar','Asserted at logic LOW; 电平0表示控制已有效。','Register Enable and Reset'),
('高阻','High impedance','Z','Driver released; 不是强制0或未知X。','Tri-State Buffers and Bus Drivers'),
('有效指示','Valid indicator','V','Separates a meaningful code from no input; 区分零编号与无输入。','Encoder and Priority Encoder'),
('进位传播','Carry propagate','P','Carries an incoming carry under the declared OR/XOR convention; sum仍用XOR。','Ripple Carry and Carry Look-Ahead Adders'),
('进位产生','Carry generate','G','Both operand bits are1, producing carry independent of carry-in; 本位独立产生进位。','Ripple Carry and Carry Look-Ahead Adders'),
('消隐','Blanking','BI','Force display off; 与无效输入的don’t-care不同。','Seven-Segment Display and Code Conversion'),
('零抑制','Zero suppression','RBI/RBO','Hide insignificant zeros through a controlled chain; 保留内部有意义的0。','Seven-Segment Display and Code Conversion'),
('扫描槽频率','Scan slot rate','f_slot','Rate of one selected position update; 完整frame rate为slot rate除以位置数。','Keyboard Scanning and Encoding'),
('粘连故障','Stuck-at fault','SA0/SA1','A node is modeled constantly0/1; 是逻辑故障模型。','Digital Logic Troubleshooting'),
('故障敏化','Fault activation','—','Drive the healthy node opposite to its faulty value; 再令差异传播到可观察输出。','Digital Logic Troubleshooting'),
('最小污染延迟','Contamination delay','t_cd','Earliest possible output change after an input change; 最短路径用于hold检查。','Propagation Delay and Logic Hazards'),
('建立时间','Setup time','t_setup','Required stability before capture; 最迟到达须早于capture减setup。','Setup and Hold Timing'),
('保持时间','Hold time','t_hold','Required stability after capture; same-edge earliest-arrival约束。','Setup and Hold Timing'),
('时钟到输出延迟','Clock-to-Q delay','t_cq','Capture edge to changed Q; 区分最小t_ccq与最大t_pcq。','Setup and Hold Timing'),
('时钟偏斜','Clock skew','s','Difference in clock arrival; 本库s为capture比launch晚。','Setup and Hold Timing'),
('时间裕量','Timing slack','—','Available time minus required time under the stated check; 负值表示违反。','Setup and Hold Timing'),
('亚稳态','Metastability','—','Storage element temporarily lacks a valid stable logic output; 同步器降低传播风险。','Metastability and Clock Domain Crossing'),
('下一状态','Next state','Q+','State captured at next specified event; 由旧Q和当前输入计算。','Sequential Logic'),
('激励表','Excitation table','—','Required FF inputs for a current-to-next transition; 与characteristic table方向不同。','JK and T Flip-Flops'),
('独热编码','One-hot encoding','—','Exactly one bit asserted in a valid state; 需初始化与非法态策略。','State Encoding and Unused States'),
('独冷编码','One-cold encoding','—','Exactly one bit LOW in a valid code; 课程键盘扫描使用。','Keyboard Scanning and Encoding'),
('模数','Modulus','M','Number of distinct states in repeating cycle; 不是任意序列最大数值加1。','Counters'),
('末态','Terminal count','TC','Decode of designated last state; 接受的rollover还需要enable。','Cascaded Counters and Digital Clocks'),
('单稳态','Monostable','One-shot','One stable state; trigger produces a timed excursion and return。','One-Shots and Pulse Applications'),
('存储深度','Memory depth','D','Number of addressable words; 与每word位宽分开。','Memory Arrays and Expansion'),
('易失性','Volatility','—','Contents are not retained after loss of sustaining power; SRAM和DRAM均通常易失。','SRAM DRAM and ROM'),
('查找表','Lookup table','LUT','Inputs address fixed truth bits during logic operation; user state另由FF保存。','Read-Only Memory and Programmable Logic Arrays'),
('实体与体系结构','Entity / architecture','—','Interface / implementation in VHDL; 硬件端口与实现分离。','VHDL Language and Modeling'),
('端口映射','Port map','—','Connect instance ports to actual signals; named association明确连接。','Structural Shift Register Project'),
('零时间调度周期','Delta cycle','—','Simulation updates without elapsed physical time; 不等于真实门延迟。','VHDL Language and Modeling'),
('被测设计','Design under test','DUT','Implementation driven and checked by the testbench; 参考模型来自规范。','Testbench and Functional Verification'),
('时序收敛','Timing closure','—','Mapped constrained design satisfies timing requirements; 功能仿真通过不能单独证明。','Field-Programmable Gate Array'),
]
out.extend(['## 23 · Cross-chapter Working Vocabulary · 跨章常用术语','', '| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |','|---|---|---|---|---|'])
for zh,en,abbr,definition,target in extras:
    out.append(f'| {zh} | {en} | {abbr} | {definition} | [[{target}]] |')
t=t[:t.rfind('\n---\n索引：')].rstrip()+'\n\n'+'\n'.join(out)+'\n\n---\n索引：[[ECE2050 Knowledge Tree]]\n'
# Redirect previously introduced half-adder and display terms to their complete concepts.
t=t.replace('| [[Exclusive-OR Gate]] |\n\n## 11', '| [[Half Adder and Full Adder]] |\n\n## 11')
t=t.replace('| 七段译码器 | Seven-Segment Decoder | — | 把 BCD 码译成七段显示的译码器；非法 BCD 码是典型无关项 | [[Karnaugh Map with Don\'t Cares]] |','| 七段译码器 | Seven-Segment Decoder | — | Map BCD to segment commands; 非法码策略与极性须规定 | [[Seven-Segment Display and Code Conversion]] |')
p.write_text(t,encoding='utf-8')
print('Updated existing knowledge tree and glossary; expansion chapters:',dict((k,len(v)) for k,v in by_ch.items()))
