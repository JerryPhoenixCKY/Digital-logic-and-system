from pathlib import Path
root=Path(__file__).resolve().parents[1]
notes=root/'Notes'
def edit(title,fn):
    p=notes/(title+'.md')
    t=p.read_text(encoding='utf-8')
    new=fn(t)
    if new!=t:
        p.write_text(new,encoding='utf-8')
def insert(title,heading,content):
    def change(t):
        if heading in t:
            return t
        return t.replace('## Connections · 相关笔记',heading+'\n\n'+content.strip()+'\n\n## Connections · 相关笔记')
    edit(title,change)

edit('Combinational Circuit',lambda t:t.replace('—— 讲义 p.6 注明属于 Chapter 5 的内容','；本库在 Ch4 建立模型，Ch5 展开分析设计').replace('—— 讲义 p.6 注明属于 Chapter 6','；本课程 Ch7 开始详细讨论').replace('任意一条被破坏，电路就不再是组合电路 —— 规则 2 被破坏会得到不确定的电平（推导 3），\n  规则 3 被破坏会得到记忆（feedback），两者都属于 Ch6 的时序电路。','违反任一规则就不能由这套组合构成模型保证正确性。多驱动可能产生冲突；反馈可能形成\n  存储、振荡或其他不满足该模型的行为，不能统一归成正常时序电路。').replace('这时候"输出 = 当前输入的函数"这句话不再成立 —— 电路记住了上一次的结果，属于时序逻辑。','此时不能按无环组合网络直接逐级求值。合适的反馈能保存状态，但反相反馈也可能振荡；\n需结合实际拓扑判断，不能仅凭有环就保证稳定记忆。').replace('讲义 p.6 把这类电路归给 Chapter 6 的时序逻辑。','稳定反馈的存储机制见 [[Set-Reset Latch]]；时序设计主线见 [[Sequential Logic]]。').replace('有回路就有记忆，即使没有时钟（Example 3）','有回路需检查存储或振荡等行为；无时钟并不保证组合（Example 3）').replace('sequential logic（Ch6 内容）—— 有记忆的电路；两者的分界线就是本篇的三条规则。','[[Sequential Logic]]（Ch7）—— 研究有状态的逻辑模型；三条规则是本篇组合模型的构成约束。').replace('E -- yes --> Z[Feedback: it has memory]','E -- yes --> Z[Feedback: analyze storage or oscillation]'))

edit("Karnaugh Map with Don't Cares",lambda t:t.replace('七段译码器本身会在 Ch6 的**译码器/编码器**里再次出现（尚未建笔记）。','[[Seven-Segment Display and Code Conversion]] 给出 Ch6 的完整显示接口、零抑制和码制转换。'))
edit('POS Minimization with Karnaugh Map',lambda t:t.replace('译码器/编码器实现（Ch6）会在最小 POS 与最小 SOP 之间做取舍（尚未建笔记）。','[[Decoder]]、[[Multiplexer and Demultiplexer]] 与 [[Universal Gates and Bubble Pushing]] 比较不同实现。'))

edit('Number Base Conversion',lambda t:t.replace('**规则：从最右（LSB）开始向左每 $k$ 位一组；最左一组不足 $k$ 位时补 0。**','**整数部分从 binary point 向左每 $k$ 位一组，最左不足时补 0；小数部分从点向右分组，最右不足时补 0。**').replace('这是八 / 十六进制存在的**唯一理由**','这是八 / 十六进制便于阅读二进制位串的主要原因之一').replace('分组方向永远是**从右往左**，方向搞反是本节最高频的错误。','本图只含整数，所以从右往左分组；小数部分应从点向右分组。').replace('$R$ 进制与 $S$ 进制之间没有直接算法（除非两者都是 2 的幂），因为"位权展开"这个定义本身就是\n**用十进制数值**表达的：','任意 $R$ 到 $S$ 的转换可通过位权值、整数除法/小数乘法完成，也可在目标进制中直接累积。\n这里选择 decimal 作为便于人工核算的中间表示，并非理论上必须先写成十进制：'))

edit('Floating-Point Numbers',lambda t:t.replace('它只有 $2^{32}$ 个可表示值','它只有 $2^{32}$ 种位模式（正负零与不同NaN模式不等于同数量的不同实数）').replace('`0.1 + 0.2 != 0.3`、比较经过舍入的计算结果时','某些计算会出现如 binary64 的 `0.1 + 0.2 != 0.3`；具体结果取决于格式和每步舍入。比较经过舍入的计算结果时').replace('**十进制↔二进制两次舍入**的巧合，`0.1 + 0.2 == 0.3` 为假。','最短十进制输出对该存储值的显示。binary64 中 `0.1 + 0.2 == 0.3` 为假；\n若每步严格按 binary32 round-to-nearest 舍入，该比较可为真，不能把这个反例当成所有格式的定律。').replace('正确：永远是 $1.F$（例 3 中漏掉会得到 $100$ 而不是 $228$）。','正确：normal finite values 用 $1.F$；subnormal 用 $0.F$ 并采用其指定阶码（例3是normal）。').replace('正确：比较 $|x-y| < \\varepsilon$，或对金额改用定点/整数。','正确：按任务语义选择精确比较或有依据的绝对/相对容差；金额常用有规定scale的定点/整数。'))
insert('Floating-Point Numbers','## Custom 16-bit format · 自定义十六位格式',r'''
The supplied custom format has one sign bit, four exponent bits, eleven fraction bits, and bias seven. It is **not IEEE binary16**, which uses one sign bit, five exponent bits, ten fraction bits, and bias fifteen. Field width alone does not identify a format.

For a normal value in the custom model, $x=(-1)^s(1+F/2^{11})2^{E-7}$; use only the special-value rules explicitly specified for that format. IEEE zero/subnormal/infinity conventions cannot be inferred from the word “16-bit”.

**Worked check.** 取s=1、E=1001₂=9、F=01000000000₂=512，值为 $-(1+512/2048)2^{9-7}=-1.25\times4=-5$。把bias错用15会得到−0.01953125，错误来自format，不是补码符号处理。
''')

edit('Cyclic Redundancy Check',lambda t:t.replace('干净帧余 `000`（无错）','干净帧余 `000`（未检出错误）').replace('$D_{in}$ 从最右一级喂入','图中 $D_{in}$ 从左侧 $D_0$ 喂入').replace('接收端复算**：整帧除 $G$，余数全 0 → 接受；否则报错并请求重传。','接收端复算**：整帧除 $G$，余数全 0 → 未检出错误；否则报错，后续恢复策略由协议规定。'))
insert('Cyclic Redundancy Check','## Degree-three serial divider · 三阶生成式的串行模型',r'''
For $G=x^3+x$ itself, use three remainder bits $R_2R_1R_0$, zero initialization, and MSB-first input. Appending one bit d shifts the old polynomial; the outgoing $R_2x^3$ is reduced by $x^3+x$, yielding:

$$R_2^+=R_1,\qquad R_1^+=R_0\oplus R_2,\qquad R_0^+=d.$$

Feed data followed by **three** zeros to compute the conventional three-bit checksum. 数据11010011给出010，发送11010011010；题目数据10110010给出110，发送10110010110。接收整帧后寄存器000表示整除、未检出错误。

The preserved four-stage diagram instead uses $H=xG$ and the explicitly described four-bit extension. The two networks are not interchangeable for arbitrary input; `1000` is a simple counterexample. Compare [[Shift Registers]] and [[Testbench and Functional Verification]] to verify the recurrence against direct polynomial division.
''')

# Put the new figures adjacent to the definitions they explain.
edit('Setup and Hold Timing',lambda t:t.replace('## Setup Derivation · 建立约束推导','![[setup-hold-window.svg]]\n*Figure 1 · 共同时间轴上的采样窗口：D在建立/保持区间稳定，Q在clock-to-Q延迟后改变；示意长度不代表器件保证值。*\n\n## Setup Derivation · 建立约束推导') if '![[setup-hold-window.svg]]' not in t else t)
edit('Setup and Hold Timing',lambda t:t.replace('## Worked Example · 同时检查两条约束','![[register-short-long-paths.svg]]\n*Figure 2 · 同一组合网络的最长/最短路径概念：分别用于setup与hold；上下框是路径分析示意，不是将两个门输出短接的接线图。*\n\n## Worked Example · 同时检查两条约束') if '![[register-short-long-paths.svg]]' not in t else t)
edit('Shift Registers',lambda t:t.replace('## Applications and Review · 应用与复习','![[serial-shift-trace.svg]]\n*Figure · 以Q3Q2Q1Q0读状态，串入1、0、1、1；每个正沿都用旧状态生成四位新状态。图中的shifted out是该边沿前的旧Q0。*\n\n## Applications and Review · 应用与复习') if '![[serial-shift-trace.svg]]' not in t else t)
insert('Shift Registers','## Serial interfaces and matrix scanning · 串行接口与矩阵扫描',r'''
SIPO converts a defined serial bit sequence into a parallel word; PISO does the reverse. A complete UART additionally defines framing, bit timing, sampling, and any parity/stop fields. A shift register is one building block, not a complete asynchronous communication protocol.

串入顺序决定字节位序；例如从Q3串入四位1011，最终为1101，不能自动当成1011。按目标bit order安排输入，或在输出解释中明确重排。课程的 [[Keyboard Scanning and Encoding]] 用环形寄存器移动one-cold行选择，再由编码器与key-code register保存位置。
''')
insert('Ring and Johnson Counters','## One-cold scan application · 独冷扫描应用',r'''
An eight-stage ring initialized to `11111110` moves one zero around an active-low row interface. Its selected-row identity is valid only while the one-cold invariant holds. The same feedback wiring initialized to all ones cannot create a zero by itself.

扫描逻辑与采样控制见 [[Keyboard Scanning and Encoding]]。行选择、编码与捕获之间必须有稳定窗口，不能仅凭环形序列正确就宣布键盘接口完整。
''')
insert('Encoder and Priority Encoder','## Position codes in a scanned keyboard · 扫描键盘中的位置码',r'''
An eight-row matrix uses a three-bit row encoder and an eight-column matrix uses a three-bit column encoder. Combining the fields produces a six-bit position code, with an independent valid condition. Active-low one-cold inputs require the corresponding input polarity conversion or device model.

[[Keyboard Scanning and Encoding]] 把该组合块连接到扫描状态、debounce与load事件；编码器本身不能决定一次按下应产生几次字符。
''')
insert('One-Shots and Pulse Applications','## Delayed key capture · 延迟捕获按键',r'''
In the course's keyboard example, one-shots delay the accepted capture event and temporarily inhibit scanning. This keeps the row identity aligned with the column code while the key-code register loads. The selected pulse width must suit the specified settling model.

完整路径见 [[Keyboard Scanning and Encoding]]。增加R或C在相同threshold模型下延长pulse；不能据此推定任意机械开关都去抖成功。shared-clock实现可用计数器和enable替代异步脉冲时钟。
''')

p=root/'Tools/README.md'
t=p.read_text(encoding='utf-8').replace('43 篇专题笔记','86 篇专题笔记').replace('49 张自绘 SVG','52 张自绘 SVG')
t=t.replace('中文保留用于推导、易混淆条件和例题解释。','中文保留用于推导、易混淆条件和例题解释。整体可读文字的英文比例以约40%为目标，代码、数学和元数据不计入估算。')
t+='\n## 2026-09-30 全库扩展验证\n\n规划与概念覆盖记录在 `.scratch/PLAN-Expansion-20260930.md`、`.scratch/source-coverage-20260930.md`；\n新增例题验算为 `.scratch/verify_expansion.py` 和 `.scratch/application-checks.py`。\n`.scratch/audit_expansion.py` 核对知识树、术语表、canonical links、语义入链和英文比例估算。\n仅按需要运行构建脚本；正式笔记完成后的手工编辑不要被草稿重建覆盖。\n'
p.write_text(t,encoding='utf-8')
print('Integrated corrected models, explicit application links, figures, and tool documentation')
