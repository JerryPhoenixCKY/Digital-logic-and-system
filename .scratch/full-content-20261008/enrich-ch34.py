from pathlib import Path
import re, json, itertools, hashlib

ROOT = Path.cwd()
BASE = ROOT / '.scratch/full-content-20261008'
OUT = BASE / 'draft/Notes'
OUT.mkdir(parents=True, exist_ok=True)
MAP = json.loads((ROOT / '.scratch/consolidation-20261008/mapping.json').read_text(encoding='utf-8-sig'))
LINKS = json.loads((ROOT / '.scratch/consolidation-20261008/link-mapping.json').read_text(encoding='utf-8-sig'))
targets = [g for g in MAP['groups'] if g['chapter'] in ('Ch3','Ch4')]
texts = {g['target']:(ROOT / 'Notes' / (g['target']+'.md')).read_text(encoding='utf-8-sig') for g in targets}
added = {}

def insert(target, marker, content):
    assert texts[target].count(marker)==1, (target,marker,texts[target].count(marker))
    texts[target] = texts[target].replace(marker, content.strip()+'\n\n'+marker)
    added.setdefault(target,[]).extend(re.findall(r'^### (.+)$',content,re.M))

G='Logic Gates and Boolean Functions'
L='Logic Levels and Noise Margins'
A='Boolean Algebra and Circuit Models'
F='Boolean Forms and Algebraic Simplification'
K='Karnaugh Map Minimization'

insert(G, '> [!example]- Logic Gates · 推导与例题', r'''
### 门的分类、符号与描述方式 (classification and representations)

输入写作 $A,B,C,\ldots$，输出常写 $Y,F,Z$；补 (complement) 可写 $\bar A=\overline A=A'$。下表的式子用于一输入或两输入；多输入条件另列，避免把“不同/相同”误用于三输入。

| 门 | 输入数与表达式 | 输出为 1 的条件 | 图形与记号 |
|---|---|---|---|
| NOT / BUF | 单输入，$\bar A$ / $A$ | A=0 / A=1 | 三角形，有/无输出气泡 |
| AND / NAND | 通常至少两输入，$AB$ / $\overline{AB}$ | 全部为 1 / 不全为 1 | D形，AND无气泡、NAND有输出气泡 |
| OR / NOR | 通常至少两输入，$A+B$ / $\overline{A+B}$ | 至少一个 1 / 全部为 0 | OR 弧形，NOR 带输出气泡 |
| XOR / XNOR | 两输入，$A\oplus B$ / $\overline{A\oplus B}$ | 不同 / 相同 | OR 本体再加输入侧弧线，XNOR 带输出气泡 |

真值表 (truth table) 给出全部组合的稳态值；逻辑表达式 (logic expression) 适合推导和化简；时序图 (timing diagram) 展示各波形共用时间轴后的关系。三者描述同一逻辑功能，**时序图必须另说明零延迟还是实际延迟**。讲义的门图与完整两输入表保留在下方例题中。

形状符号与矩形符号不能只凭外形猜：`&` 表示 AND，`≥1` 表示至少一个输入有效；两输入的 `=1` 与 XOR 等价，因为恰好一个 1 就是奇数个 1。扩展到多输入时，**恰好一个有效输入**与**奇数个有效输入**不再相同；奇数性符号可用 `2k+1`。例如 111 的三输入 XOR 为 1，“恰好一个”则为 0。读图应核对功能表及限定符。[TI, Overview of IEEE Standard 91, Table 1](https://www.ti.com.cn/cn/lit/pdf/sdyz001)

### 理想模型、有效极性与读表方法 (validity and method)

稳态布尔模型假定输入已经是有效 0/1；理想时序图再假定零延迟、输入不取电流、输出驱动/扇出无限。真实门的电平范围、负载能力、传播延迟必须单独查证。逻辑门在实际跳变时输出也会经过中间电压，不能把“两个合法稳态电平”理解成“电压永远只有两个数值”。

正逻辑 (positive logic) 用 HIGH 表示 1；负逻辑 (negative logic) 用 LOW 表示 1。对同一物理电路整体改用负逻辑时，AND/OR 的逻辑描述会按对偶关系交换。**低有效 (active-low)** 只规定哪个电平断言某个事件，不能与整体的负逻辑约定混为一谈。气泡 (bubble / negation indicator) 表示该端口取补；控制端的有效含义还需结合功能规范。

1. 列出 n 个不同输入及其含义，写全 $2^n$ 种组合，通常按自然二进制顺序。
2. 从表达式或“输出为 1 的条件”逐行填表，再对照符号的主体、输入/输出气泡和横线范围。
3. 认门时先看所有行的规律。输出 1 的行数可作为线索：AND/NOR 各一行，OR/NAND 各 $2^n-1$ 行，XOR/整体取补各 $2^{n-1}$ 行；**计数相同不足以证明是该门**，必须核对具体行。
4. 画时序图时，在每个输入稳定区间查表，标注延迟后再放输出边沿；题目要哪一种描述形式，就交付对应形式。

悬空输入、多个普通输出短接和组合反馈环不属于这一基本构成模型，连接约束见 [[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|组合电路模型]]。输入数“至少 2”是本课多输入门的常用分类；一输入 AND/OR 在代数上退化为 BUF，一输入 NAND/NOR 退化为 NOT，不能把课程分类误说成函数在数学上无定义。
''')

insert(G, '> [!example]- Inverter · 推导与例题', r'''
### Inverter and Buffer · 单输入功能与适用边界

非门 (NOT gate) 只有一个输入：$Y=\bar A$，英文读作 “NOT A”, “A bar” 或 “the complement of A”。两个输入的 $\overline{AB}$ 是先 AND 再取补的 NAND，$\overline{A+B}$ 是 NOR；若要对复杂函数取反，先计算该函数，再接单输入反相器。

| A | NOT $\bar A$ | BUF $A$ |
|---|---|---|
| 0 | 1 | 0 |
| 1 | 0 | 1 |

BUF 的作用包括提供驱动能力 (drive capability)、电压恢复/整形 (regeneration) 和按需要引入延迟；能否完成这些任务取决于输入电平、负载和器件规范。串联两级 NOT 只在稳态逻辑上等于 BUF，不能据此保证延迟、功耗或驱动能力相同，也不能泛称一定比专用 BUF 多多少晶体管。

读图顺序为“确认单输入 → 看输出气泡 → 填两行表 → 找输入沿 → 放置输出的相反沿”。真实器件分别用输出高到低的 $t_{PHL}$、低到高的 $t_{PLH}$；仅在二者相等的固定延迟模型中，整条反相波形可统一平移。若二者不同，占空比也可能改变，详见 [[Propagation Delay and Logic Hazards]]。双重补 $\overline{\bar A}=A$ 与单次补 $\bar A$ 必须分清。
''')

insert(G, '> [!example]- AND Gate · 推导与例题', r'''
### AND Gate · 同时满足、许可与门控

与门 (AND gate) 为 $Y=A\cdot B=AB$，读作 “A AND B”；三个输入写 $ABC$，n 输入写 $\prod_i A_i$。0/1 上的布尔乘与算术乘的值相同，只要一个输入为 0 就使整个积为 0；输入接 1 则为恒等许可 $A\cdot1=A$。前者是屏蔽 (masking)，后者才是把这一输入固定成不限制其余条件。

填真值表只在全 1 行写 1，n 输入仍只有这一行输出 1。画波形时先并合各输入为 0 的时间区间，这些区间内输出为 0；其余区间才满足全 1。门控 (gating) $Y=A\cdot E$ 中，E=0 禁止，E=1 传递 A。实际时钟门控不能只照这个稳态等式连门，必须处理使能跳变和毛刺。

“有一个 1 就为 1”是 OR 的规则；“所有 AND 输入为 1 时输出为 0”是错误命题。三输入门要写 8 行；不论输入数，定义中的 **all inputs** 不能换成 **any input**。所有输入应有明确驱动并满足 [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围|逻辑电平]]。AND 是 [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|SOP]] 的乘积层，也是 [[Binary Arithmetic Circuits]] 中半加器的进位函数。
''')

insert(G, '> [!example]- OR Gate · 推导与例题', r'''
### OR Gate · 包含或与控制值

或门 (OR gate) 为 $Y=A+B$，读作 “A OR B”；n 输入为 $\sum_i A_i$，这里的和号表示 OR。其条件是**至少一个输入为 1**，包含两个或多个同时为 1，所以 $1+1=1$，不会产生算术进位。OR 的弧形输入边与 AND 的平背/D 形要分清。

真值表仅全 0 行为 0，其余为 1。画波形先找“所有输入同时为 0”的区间，再把剩余区间置 1；等价地，输出为 1 的时间集合是各输入为 1 区间的并集。$A+0=A$ 表示接 0 不限制 A；$A+1=1$ 表示任何一个恒 1 输入都会屏蔽其余输入的变化。与 AND 的 $A1=A,A0=0$ 对照记忆。

文字中的 “at least one” 使用 OR；“exactly one” 在两输入时才对应 XOR。检查输入 11 是区分两者的关键。输入中1的数量不会使布尔输出“更大”，实际驱动能力则取决于器件和负载。OR 与 AND 互为对偶，不能因此把它们的输出列视为逐行互补；输出互补配对是 OR/NOR 与 AND/NAND。OR 汇总事件，也组成 [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|POS]] 的和项层。
''')

insert(G, '> [!example]- NAND Gate · 推导与例题', r'''
### NAND Gate · 先与后取补

与非门 (NAND gate) 输出 $Y=\overline{AB}$，n 输入为 $\overline{\prod_i A_i}$：**只有全 1 时为 0，只要一个 0 就为 1**。英文答句：**“Y is LOW only when all inputs are HIGH.”** 横线必须覆盖整个乘积，顺序是 “AND then invert”。D 形本体的输出端气泡实现这一记号；若把气泡移到所有输入端，必须同时把本体换成 OR，才保持 $\bar A+\bar B$ 的等价功能。

方法是先列 AND 中间值，再逐行取补；最后检查唯一的 0 是否落在全 1 行。自然二进制排序有利于自检，其他不重不漏的排序也有效，卡诺图使用 Gray 排序更不是错误。$\overline{AB}\ne\bar A\bar B$：01 时二者为 1 与 0，是直接反例。

NAND 可构成 NOT、AND、OR，因此有功能完备性 (functional completeness)；推导与具体连接集中在 [[Universal Gates and Bubble Pushing]]。工程上不能仅凭“更常用”就断言任意 NAND 实现的功耗或延迟优于其他门，应结合逻辑家族、扇入和负载比较。
''')

insert(G, '> [!example]- NOR Gate · 推导与例题', r'''
### NOR Gate · 先或后取补

或非门 (NOR gate) 为 $Y=\overline{A+B}$，n 输入为 $\overline{\sum_i A_i}$：**只有全 0 时为 1，只要有一个 1 就为 0**。英文答句：**“Y is HIGH only when all inputs are LOW.”** OR 本体加输出气泡，等价为所有输入带气泡的 AND：$\bar A\bar B$。

先逐行算 OR 再取補，检查唯一的 1 是否位于全 0 行。$\overline{A+B}$、$\bar A+\bar B$ 和 $\overline{AB}$ 的横线范围决定了不同函数；后两式互等，属于 NAND。把气泡只搬到输入端却保留 OR 本体会改变 NOR 的功能。

NAND 与 NOR 互为对偶，**它们的真值表不逐行互补**；应同时取反输入和输出来比对：$\mathrm{NOR}(A,B)=\overline{\mathrm{NAND}(\bar A,\bar B)}$。NOR 同样是通用门，实际面积、功耗和速度取决于实现。两门的等价转换由 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan 定理]] 保证，电气输入边界仍需满足。
''')

insert(G, '> [!example]- Exclusive-OR Gate · 推导与例题', r'''
### Exclusive-OR Gate · 模2加法、受控反相与奇数性

异或门 (exclusive-OR gate, XOR) 的两输入判据是不同为 1，$A\oplus B=A\bar B+\bar AB=(A+B)\overline{AB}$。$\oplus$ 是模2加法 (modulo-2 addition)，$1\oplus1=0$，没有整数进位。图形为 OR 本体加输入侧额外弧线，无输出气泡。

多输入定义为 XOR 归约 (XOR reduction)，交换律和结合律使 $A\oplus B\oplus C$ 有唯一意义；数每行 1 的个数，奇数输出 1，偶数（含0）输出0。三输入 111 也输出1，不能译成“恰好一个输入为1”或“所有输入不相同”。两输入 SOP 展开式不能直接套给更多变量。

求解顺序：定域并列全输入 → 数奇偶填表 → 需要 SOP 时为各 1 行写最小项并相或 → 按要求选 XOR 门或等价 AND/OR/NOT 结构。用于算术时必须另计算进位，半加器为 $S=A\oplus B,C=AB$；01与10给不同为1，11给S=0但C=1，表示 $10_2$。

检验典型代数性质：$A\oplus0=A$，$A\oplus1=\bar A$，$A\oplus A=0$，$A\oplus\bar A=1$。不能误写成 XNOR 的同号两项，也不能把 XOR 与 OR 混用。[[Parity and Cyclic Redundancy Checks]] 使用无进位模2运算；[[Data Coding and Character Representation]] 中 Gray 编码可用逐位 XOR。
''')

insert(G, '> [!example]- Exclusive-NOR Gate · 推导与例题', r'''
### Exclusive-NOR Gate · 两位相等、偶数性与校验边界

同或门 (exclusive-NOR gate, XNOR) 为 $A\odot B=\overline{A\oplus B}=AB+\bar A\bar B$，也常用等价记号 $A\equiv B$；图形是 XOR 加输出气泡。两输入相等才为1，00和11都为1，所以它与“只在00为1”的 NOR 不同。相反输入输出0的命题属于 XNOR，不属于 XOR。

本课的 n 输入 XNOR 明确定义为**整个 n 输入 XOR 取一次补**：$\overline{\bigoplus_i A_i}$，偶数个1输出1。三输入 011为1、111为0，说明它不检测全部输入彼此相同。数偶数个0仅在 n 为偶数时与此等价，不能作为一般规则。二输入 $A\odot A=1$ 与 XOR 的自消性质不同。

多个二输入 XNOR 级联会引入 n−1 次补，结果为 $\bigoplus_i A_i\oplus((n-1)\bmod2)$；n为奇数时得到 XOR，n为偶数时才得到其补。二输入XNOR本身可交换、可结合，但其级联运算与本课“n输入整体XOR的补”的约定必须区分。实现偶数性指示时可明确用 XOR 树再加一次反相。

多位相等检测须**逐位 XNOR 再 AND**：$E=\prod_i\overline{A_i\oplus B_i}$，或先将逐位 XOR 相 OR 再取补。生成校验位时，数据 XOR 生成偶校验位，数据 XOR 的补生成奇校验位；检查时必须包括收到的校验位。不要把“偶数性指示”“偶校验位生成”“偶校验通过”三者混同。方法是先确定比较/校验任务，再写逐位函数或整体归约，最后验证全部指定输入。
''')

insert(G, '## Sources · 课件依据', r'''
### 复习与关系 (review and connections)

从 [[Number Systems and Base Conversion]] 的位和组合数进入门函数，再经 [[Boolean Algebra and Circuit Models]] 的构成规则连成网络。符号、表达式、真值表必须一致；实际连线还要通过 [[Logic Levels and Noise Margins]] 的静态接口检查，以及 [[Propagation Delay and Logic Hazards]] 的动态检查。输出气泡将整列取补，内部某个输入气泡只取补那个输入；气泡记号不意味着电路中必然有一只独立反相器。

**English answer pattern:** “An n-input gate has $2^n$ input combinations. Its truth table specifies the steady-state Boolean function; voltage limits, load capability, and timing require separate specifications.”
''')

insert(L, '> [!example]- Logic Levels · 推导与例题', r'''
### 四个保证边界与电压区间 (guaranteed interface limits)

逻辑值由电压**范围**表示，理想例子“0=GND=0 V、1=$V_{DD}$=5 V”只是单点近似，不能用它判断4.99 V或3.2 V。以下均为指定供电、温度、输出电流和负载条件下的接口限值；本文以 $V_{SS}=\mathrm{GND}=0$ V 为参考，其他电源域须改用相应参考。

| 参数 | 英文含义 | 谁定义/保证 | 判断方向 |
|---|---|---|---|
| $V_{OL(max)}$ | maximum output LOW voltage | 驱动器 | LOW 时输出不高于它 |
| $V_{OH(min)}$ | minimum output HIGH voltage | 驱动器 | HIGH 时输出不低于它 |
| $V_{IL(max)}$ | maximum recognized input LOW voltage | 接收器 | 不高于它才保证识别 LOW |
| $V_{IH(min)}$ | minimum recognized input HIGH voltage | 接收器 | 不低于它才保证识别 HIGH |

接收 LOW 区间通常为 $[0,V_{IL(max)}]$，HIGH 区间为 $[V_{IH(min)},V_{DD}]$；中间**开区间** $V_{IL(max)}<V_{in}<V_{IH(min)}$ 是未保证区 (undefined input region)。驱动输出的保证范围则更严格，LOW通常为 $[0,V_{OL(max)}]$，HIGH通常为 $[V_{OH(min)},V_{DD}]$。因此接收端能接受的范围**比同极性的输出保证范围更宽**，两者之间才留有噪声预算，不能说接收器更“挑剔”。输入容许范围的上/下界仍以器件规范为准，特别是具有过压容许能力的输入。

同家族、相同条件的教学例子常满足 $V_{OL}<V_{IL}<V_{IH}<V_{OH}$。这是一种有正余量的理想排序，**不是所有接口必然满足的公理**。跨器件时应分别检验 $V_{OH(min),driver}\ge V_{IH(min),receiver}$ 和 $V_{OL(max),driver}\le V_{IL(max),receiver}$。若等号成立，静态边界可相接但没有额外噪声余量。

### 判电平、检查直连与常见误区 (method and pitfalls)

1. 先找接收端的输入阈值，再按“大于等于HIGH下限、小于等于LOW上限”判电平；落在未保证区则不能给出保证的0/1。
2. 分清当下测量余量 $V_{in}-V_{IH}$ 或 $V_{IL}-V_{in}$，与由最差输出保证得到的**设计噪声容限**。空载测到4.9 V不能取代 $V_{OH(min)}$。
3. 检查驱动—接收两侧的全部四个限值，计算两侧余量，再核对绝对/推荐输入电压、电流、负载、供电范围和时序。
4. 任一余量为负，表示静态接口**不保证**；典型实物可能工作，不能宣称“必然每次失败”。修改家族、电平转换或驱动结构后重算。

未保证区不是稳定的第三布尔值，也不是自动就近舍入；可能造成抖动、振荡或CMOS输入级持续电流。浮空端应按器件要求固定。相同电源不充分证明兼容，不同电源也不必然不兼容。讲义p.23的TTL/CMOS/LVTTL/LVCMOS数值在下方完整表中复核，作为课程示例，不能代替某个具体料号在给定条件下的手册。

电压HIGH/LOW、布尔1/0和控制的有效/无效是三个层次：正逻辑选择HIGH=1，active-low则可用LOW断言一个动作。电平范围讲静态有效性，传播延迟与上升/下降时间见 [[Propagation Delay and Logic Hazards]]；断开驱动的Z见 [[Tri-State Buffers and Bus Drivers]]。
''')

insert(L, '> [!example]- DC Transfer Characteristic · 推导与例题', r'''
### VTC读数与模型适用范围 (curve interpretation)

电压传输特性 (voltage transfer characteristic, VTC) 是指定供电、温度与负载下的稳态曲线 $V_{out}=f(V_{in})$。缓冲器单调上升，左/右平台为LOW/HIGH；反相器单调下降，左/右平台为HIGH/LOW。平台值和边界可用于构建一个静态模型，但一条典型曲线的端点**不是跨工艺、温度、负载的保证值**。

| 量 | 定义与单位 | 限制 |
|---|---|---|
| 局部增益 (gain) $A=dV_{out}/dV_{in}$ | 无量纲斜率，反相器为负 | 过渡区与平台斜率不同 |
| 单位增益点 (unity-gain points) | 某类静态模型中 $|A|=1$ 的两处输入电压 | 反相器为斜率−1；缓冲器为+1；应说明采用此定义 |
| 切换电压 (switching voltage) $V_M$ | 反相器常取 $f(V_M)=V_M$，单位V | 对称模型可为 $V_{DD}/2$，不是保证阈值 |
| 过渡宽度 (transition width) $W$ | $V_{IH}-V_{IL}$，单位V | 必须明确所用输入边界定义 |

晶体管阈值电压 (transistor threshold voltage, $V_T$ 或 $V_{TH}$) 描述某只MOS晶体管的导通条件；$V_M$ 描述整个反相器的切换点；$V_{IL}/V_{IH}$ 描述逻辑输入保证边界。**三者不是同一个量**。改变p/n管相对强度可能移动反相器曲线：在其他条件不变的简单CMOS模型中，p管更强常使切换点上移、n管更强使其下移；HIGH/LOW余量如何变化需重新读取完整曲线。

### 读曲线与恢复能力检查 (method and pitfalls)

1. 核对横轴输入、纵轴输出及工作条件，辨别缓冲/反相方向。
2. 读取输出平台和采用的输入边界；如果图采用单位增益定义，寻找相应斜率点，不能凭“看起来离开平台”替代。
3. 对反相器找 $V_{out}=V_{in}$ 的交点；对缓冲器，交点可能不唯一，须由明确模型规定切换位置，不能无条件套反相器的定义。
4. 计算 $W$ 与两种噪声余量，用 $NM_H+NM_L=(V_{OH}-V_{OL})-W$ 复核；跨器件接口必须使用发送/接收各自参数。
5. 检查平台附近的小扰动是否被衰减（局部 $|A|<1$）、过渡区是否有恢复所需的高增益。静态恢复能力不代替瞬态波形与采样时序检查。

理想对称、轨到轨、零宽过渡的阶跃模型才给 $NM_H=NM_L=V_{DD}/2$；一般只应使用上述总和恒等式。有限过渡带与非轨到轨输出都会减少总余量，但**不保证两个单独余量都小于半电源**，非对称曲线可能一大一小。近似 $W\approx V_{DD}/|A|$ 还需轨到轨摆幅与线性过渡模型，不能把中间一点的最大斜率当整个过渡带的平均斜率。

降低 $V_{DD}$ 时只有在阈值比例、输出摆幅比例等假设保持时才可作同比缩放；跨逻辑族的数值不能只按供电大小排名。VTC为DC结果，不能从它推出 $t_{PHL},t_{PLH}$、建立时间或最大时钟频率。
''')

insert(L, '> [!example]- Noise Margin · 推导与例题', r'''
### 噪声来源与两侧预算 (noise sources and polarity)

噪声 (noise) 是使信号退化的扰动，包括导线/接触电阻压降、电源噪声 (power-supply noise)、邻线容性/感性串扰 (crosstalk)、漏电、反射和地弹 (ground bounce)。其中电阻压降为 $IR$，需要有相应电流；不能只因“长线有电阻”就忽略负载条件断言会产生固定压降。

| 方向 | 所比较的最坏边界 | 会消耗余量的扰动 |
|---|---|---|
| HIGH | 驱动器最低HIGH减接收器最低HIGH | 高电平向下偏移，如压降、负向耦合 |
| LOW | 接收器最高LOW减驱动器最高LOW | 低电平向上偏移，如地弹、正向耦合 |

噪声容限 (noise margin) 单位是伏特，表示接口的DC电压预算；噪声免疫能力 (noise immunity) 是更广泛的工程描述，两者不能把幅度、时间都合为一个数字。两侧不必对称：讲义LVCMOS例的0.9 V与0.54 V意味着相同幅度双向扰动的短板是LOW侧。

### 预算方法、失效判断与选型误区 (budget method)

1. 定下发送端与接收端，选覆盖各自实际供电、温度、输出电流及负载范围的保证限值；两个不同电源域不必有相同 $V_{DD}$。
2. 各算 $NM_H,NM_L$，不要用平均值、不只算一侧，也不用典型 $V_{DD}$ 替代 $V_{OH(min)}$。
3. 为两种极性分别汇总**可能同时发生、同方向**的最坏退化，包括地参考差；若有统计/相关性依据可使用相应模型，不能无依据把随机噪声平方和当保证。
4. 用剩余预算 $R_H=NM_H-\Delta_H$、$R_L=NM_L-\Delta_L$ 判定并保留设计余量。达到边界时没有额外余量，超过边界意味着失去识别保证，未必已稳定翻成另一个值。
5. 不通过时检查电平转换、家族选择、布线间距/回流、驱动缓冲和负载；随后独立检查动态毛刺、抖动、反射、建立/保持时间。

0.4 V容限不能分别吸收0.4 V压降、0.4 V串扰、0.4 V地弹；它们同方向出现时要相加。也不能只为“容限更大”选器件，应同时考虑速度、功耗、输入容许电压和驱动能力。讲义5 V→4.5 V示例区分了**实测仍为HIGH**与**最坏输出保证不足以承受0.5 V退化**，下方保留数值推导。

**English answer pattern:** “Noise margin is a worst-case static voltage budget for a driver–receiver interface. It must be checked for both polarities; it does not by itself prove correct dynamic sampling.”
''')

insert(A, '> [!example]- Combinational Circuit · 推导与例题', r'''
### 完整电路描述、节点与构成条件 (composition)

逻辑电路 (logic circuit) 的完整描述包括输入 (inputs)、输出 (outputs)、功能规范 (functional specification) 与时序规范 (timing specification)。功能可由表/方程给出；时序说明输入改变后输出何时有效。最高系统时钟频率还需配合寄存器、路径与时钟约束，不能看成单个组合元件独有的参数。

节点 (node) 是由理想导线连成同一电位的一组端点，不能把每个引脚算一个节点。输入节点由外部驱动；内部节点传递中间结果；输出节点向外提供结果。电路元件 (circuit element) 可以是一只门，也可以是整块加法器，关键是它本身满足组合模型。

三条组合构成规则 (rules of combinational composition) 分别约束元件、节点和整体依赖图：

1. 每个元件都是组合的，锁存器/触发器不能藏在某个“组合元件”内部。
2. 每个节点要么是外部输入，要么恰由一个元件输出驱动；普通推挽输出不得直接并接。三态/开漏等共享驱动是有额外电气与使能条件的模型，见 [[Tri-State Buffers and Bus Drivers]]。
3. 信号依赖无循环路径，因而可按拓扑顺序逐级计算唯一稳态结果。

组合是无记忆 (memoryless) 的**稳态模型**，并非零延迟。输入刚变时，真实输出可能暂时受此前输入和路径延迟影响；需要等待稳定后才能用 $Y=F(\mathbf x)$。无时钟不等于组合，有反馈也不自动等于正常存储电路。

### 判断步骤与错误连接 (analysis steps)

按“合并导线成节点 → 查每个元件 → 数每个节点的驱动输出 → 沿依赖检查环路 → 逐节点写式并代入输出”分析。外部输入节点由外部驱动，不能因没有内部输出驱动而误判为浮空；内部/输出节点无驱动或多驱动均超出基本规则。

扇出 (fan-out) 是一输出接多个输入，逻辑构成上允许，物理上仍受电流与电容限制；两个输出接一节点则是多驱动。并接输出即使部分行同值，也不能据此保证所有行安全，冲突行由 [[Logic Levels and Noise Margins]] 的电气模型判断。反馈环可能产生记忆、振荡或不确定行为，应回到 [[Sequential Logic and Flip-Flops]] 的状态模型及具体电路，不能只用真值表枚举冒充动态证明。
''')

insert(A, '> [!example]- Boolean Equation · 推导与例题', r'''
### 二值命题、运算词典与优先级 (Boolean specification)

布尔变量 (Boolean variable) 表示一个二值命题 (proposition)，如 $R=1$ 表示下雨，$\bar R$ 表示不下雨。输出可各有自己的函数，如全加器 $S=F(A,B,C_{in})$、$C_{out}=G(A,B,C_{in})$。多值量需先编码或定义比较条件，而不是把25 °C直接当成0/1变量。

| 文字条件 | 运算 | 写法 |
|---|---|---|
| and / 并且 | AND | $AB$ |
| or / 或者，默认包含或 | OR | $A+B$ |
| not / 没有、不 | NOT | $\bar A$ |
| but not / 但不 | AND-NOT | $A\bar B$ |

运算优先级为 NOT > AND > OR；$M+CT\bar X=M+(CT\bar X)$，不能改成 $(M+C)T\bar X$。长横线本身还限定了整体作用域，必须按其覆盖范围算。$+$ 不是计数，$A+A=A$，$1+1=1$；0/1上的AND与算术乘同值，但不允许普通代数里的系数消元或除法。

### 从文本到函数的步骤与边界 (translation method)

先点名输出和全部输入 → 明确1表示的事件与针脚极性 → 翻译连接词、exactly/at least及否定 → 用括号保留语义 → 检查能区分候选函数的边界行 → 列完整表或给合法代数证明 → 再化简。抽查能发现错误，不能把“抽查几行相同”说成证明。

本章 $Y=F(\mathbf x)$ 是组合函数，右侧只含当前输入/组合内部节点；$Y=Y+C$ 不再是直接给出唯一输出的组合规范。布尔方程**也可以**描述时序电路的下一状态，但需显式加入当前状态、时间索引和更新规则，见 [[Finite State Machine Design and Applications]]。方程说明功能，不代替延迟、负载与竞争冒险规范；若变量的事件含义或active-low极性写错，化简不能修复需求。
''')

insert(A, '> [!example]- Boolean Axioms · 推导与例题', r'''
### A1–A5与对偶原理 (axioms and duality)

布尔代数 (Boolean algebra) 在二值域 $\{0,1\}$ 上定义AND/OR/NOT。本课的五条基础约定和对应对偶如下；这套课程编号是二值运算定义，不是所有数学教材都采用的抽象公理体系。

| 编号 | 本课公理 | 对偶约定 | 含义 |
|---|---|---|---|
| A1 | B≠1时B=0 | B≠0时B=1 | 二值域，仅0和1 |
| A2 | $0'=1$ | $1'=0$ | 取補 |
| A3 | $0\cdot0=0$ | $1+1=1$ | AND/OR常量值 |
| A4 | $1\cdot1=1$ | $0+0=0$ | AND/OR常量值 |
| A5 | $0\cdot1=1\cdot0=0$ | $1+0=0+1=1$ | 两种不同输入的运算值 |

公理作为出发点，规则/定理则由它们推出。对偶原理 (principle of duality) 说：若一个布尔恒等式成立，则**等式两边**同时交换AND/OR与0/1后仍为恒等式，变量及原有取补不变。这不意味着一个表达式与其对偶函数值相等，也不意味着任意非恒真等式取对偶后在同一输入行仍有相同真值。

取对偶的操作可对任意表达式定义；要保持等式有效性，应对完整恒等式两边同时操作。方法是先识别运算树（包括省略的乘号），交换每个运算与常量，保持字母、横线和**原有分组**，必要时补括号后再按常规优先级写出。例如 $A+BC$ 的对偶是 $A(B+C)$；不能只换字符写成 $AB+C$。再取一次对偶应恢复原式。

取补 (complementation) 则把函数值0/1翻转，需用DeMorgan递归展开；它与对偶有不同作用。只换运算忘换常量会出错：$A+1=1$ 的对偶是 $A0=0$。局部等价子式在任何更大表达式内都能替换，包括取补内部；局部**取对偶**则不一般保持原函数。
''')

insert(A, '> [!example]- Laws and Rules of Boolean Algebra · 推导与例题', r'''
### 三条定律与十二规则完整表 (laws and rules)

| 定律 | OR形式 | AND形式/对应分配形式 |
|---|---|---|
| 交换律 (commutative law) | $A+B=B+A$ | $AB=BA$ |
| 结合律 (associative law) | $A+(B+C)=(A+B)+C$ | $A(BC)=(AB)C$ |
| 分配律 (distributive law) | $A+BC=(A+B)(A+C)$ | $A(B+C)=AB+AC$ |

AND分配于OR和OR分配于AND都成立，后者是普通算术没有的布尔特性。结合只保证稳态功能，级联门仍会增加路径延迟。

| Floyd编号 | 规则 | 对偶/名称 |
|---|---|---|
| 1 | $A+0=A$ | Rule2，恒等元 (identity) |
| 2 | $A1=A$ | Rule1 |
| 3 | $A+1=1$ | Rule4，控制值 |
| 4 | $A0=0$ | Rule3 |
| 5 | $A+A=A$ | Rule6，幂等 (idempotence) |
| 6 | $AA=A$ | Rule5 |
| 7 | $A+\bar A=1$ | Rule8，互补 (complementarity) |
| 8 | $A\bar A=0$ | Rule7 |
| 9 | $\overline{\bar A}=A$ | 自对偶，对合 (involution) |
| 10 | $A+AB=A$ | $A(A+B)=A$，吸收 (absorption) |
| 11 | $A+\bar AB=A+B$ | $A(\bar A+B)=AB$ |
| 12 | $(A+B)(A+C)=A+BC$ | $AB+AC=A(B+C)$，分配/提取 |

规则中的A/B/C可代入任意布尔子表达式，不只单字母。例如 $(X+\bar Y)+(X+\bar Y)Z=X+\bar Y$。规则1–9去常量、重复与双补；10–12是吸收、消除冗余文字与提取结构的常用工具，但不能说前九条不减少表达式中的文字，也不能说提公因子只有一条唯一方法。

### 按结构选规则与避免误用 (rule selection)

顺序通常是“定域/辨SOP或POS → 去0/1 → 合并重复与互补 → 处理长横线 → 提公因子 → 吸收 → 再查反变量结构”。$A+AB$ 用Rule10；$A+\bar AB$ 用Rule11，不能直接将二者混同。每一步注明依据，并在需要时穷举验证。合法等价子式可在括号/横线内部替换；不允许毫无依据把某个A改成1。

求和项为0，所有文字必须为0；求积项为1，所有文字必须为1。这是下方讲义p.18例题的判定法。$A^2$作为重复布尔乘可写但等于A，不能保留普通多项式的次数和系数意义。逻辑变短不自动意味着门数、速度、功耗最优：SOP的直接实现是AND→OR，POS是OR→AND；实际实现代价见 [[Combinational Logic Analysis and Design]] 与 [[Universal Gates and Bubble Pushing]]。
''')

insert(A, '> [!example]- DeMorgan\'s Theorems · 推导与例题', r'''
### 横线的范围、门级等价与递归步骤 (DeMorgan method)

德摩根定理 (DeMorgan's theorems) 的操作指令是 **“Break the long bar and change the operator.”** 把横线下最外层的积变为各因子取补后的和，把最外层的和变为各项取补后的积，每个操作数都要处理。两条定理互为对偶，但“求对偶”本身不等于取補。

门级等价为NAND=输入取补的OR，NOR=输入取补的AND；把输出气泡搬到**全部**输入端时本体也要交换。它保证全部输入组合的稳态函数相同，不保证相同传播延迟或硬件结构。

1. 找到最外层长横线，判断它覆盖的是和还是积，把里面的复合子式暂当整体。
2. 交换这个层级的运算，同时取补每个操作数；保留括号，已有取补用双补消去。
3. 对内部仍有长横线的子式递归，最后用其他规则整理。
4. 用完整真值表或代数链证明等价；抽查只用于找错。

例如 $\overline{A(B+C)}=\bar A+\overline{B+C}=\bar A+\bar B\bar C$；不能误写为 $\bar A+\bar B+\bar C$。若原式是 $A+\overline{B+C}$，A没有被横线覆盖，正确为 $A+\bar B\bar C$，不能顺带把A取补。$\overline{ABC}=\bar A+\bar B+\bar C$，不能只反相第一个因子。

用途包括读NAND/NOR多级电路、气泡推移和求反函数。对 $F=AB+CD$ 整体取补得 $\bar F=(\bar A+\bar B)(\bar C+\bar D)$；**这是一份反函数的POS**，并非F本身的POS。若要保持同一函数改写形式，需要正确处理第二次取補或重新按OFF行建立POS。下方保留两条真值表、多变量推广和全部例题。
''')

insert(A, '> [!example]- Proof by Perfect Induction · 推导与例题', r'''
### 完全穷举与代数证明的选择 (proof methods)

本课完全归纳法 (perfect induction / proof by exhaustion) 指在**有限二值定义域**上穷举，并非“基例+归纳步”的数学归纳法 (mathematical induction)。n个独立变量共有 $2^n$ 行；全部逐点相等就是函数相等。2/3/4/10/20变量分别有4/8/16/1024/1,048,576行，手算难度指数增长，但软件穷举5个或更多变量仍常实用，不能把“n≥5”写成方法失效。

| 方法 | 操作 | 适用与限制 |
|---|---|---|
| Method1：完全穷举 | 计算两式每一行并对比 | 少变量清楚直接；软件可扩展；必须不漏不重 |
| Method2：代数证明 | 用已成立的公理/定理逐步改写一边为另一边，或二者为共同式 | 结构清楚时简洁；必须每步等价，不能循环论证 |

真值表步骤：汇总两边全部不同变量并固定顺序 → 列 $2^n$ 行 → 按括号、NOT、AND、OR写中间列 → 把最终两列并排 → 全等才宣布成立，否则给一行反例。只算一边无法证明等价；抽查几行一致仍不是证明。代数法应标注所用规则，并可另用穷举检查；两种方法之外还存在自动形式验证，本课表格不应被误读成“所有证明方式只有两种”。

有约束输入或don't-care时，必须明确验证范围：等价需在全部指定输入上保持规范；不同X行可以取不同值，两个实现的X行也可能不同。见 [[Boolean Forms and Algebraic Simplification#2 · Truth Table and Boolean Expression · 用真值表定义全集|真值表与域]]、[[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|无关项]]。本章公理与规则支撑化简，构成规则保证组合模型，二者分别检查“式子合法”和“电路连接合法”。
''')

insert(F, '> [!example]- Minterm and Maxterm · 推导与例题', r'''
### 文字、乘积项与编号全集 (terms and domain)

定义域 (domain) 是输入变量全集及其约定顺序，未必必须按字母排，但全题应一致。文字 (literal) 是变量或其补，例如A和 $\bar A$；乘积项 (product term) 是文字的AND。严格说，**蕴含项 (implicant) 必须相对于函数F定义**：T为乘积项且 $T=1\Rightarrow F=1$，才是F的蕴含项；不能把任意乘积都叫某函数的蕴含项。

最小项 (minterm) 恰含域中每个变量一次并相与，最小项只在一行取1；最大项 (maxterm) 恰含每个变量一次并相或，只在一行取0。它们是形式的名字，不依赖该项是否被某个F选入。域为ABC时 $\bar AC$ 是缺B的乘积项，覆盖两行，不是最小项；是否为F的蕴含项还要看F在这两行的值。

| i | ABC | $m_i$：仅本行为1 | $M_i$：仅本行为0 |
|---|---|---|---|
| 0 | 000 | $\bar A\bar B\bar C$ | $A+B+C$ |
| 1 | 001 | $\bar A\bar BC$ | $A+B+\bar C$ |
| 2 | 010 | $\bar AB\bar C$ | $A+\bar B+C$ |
| 3 | 011 | $\bar ABC$ | $A+\bar B+\bar C$ |
| 4 | 100 | $A\bar B\bar C$ | $\bar A+B+C$ |
| 5 | 101 | $A\bar BC$ | $\bar A+B+\bar C$ |
| 6 | 110 | $AB\bar C$ | $\bar A+\bar B+C$ |
| 7 | 111 | $ABC$ | $\bar A+\bar B+\bar C$ |

### 写项步骤与极性自检 (polarity check)

先固定域、变量顺序和最高有效位 (MSB)，将输入行按二进制读为i，再按最小项“1原/0補”相乘，最大项“0原/1補”相加。把本行代入，应有 $m_i=1,M_i=0$；再换任一其他行，应有 $m_i=0,M_i=1$。编号从0至 $2^n-1$，各有 $2^n$ 个项。

每项必须含n个不同变量且每个恰一次；域变化、顺序变化或漏变量均须重新展开。$M_i=\bar m_i$ 由 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan]] 得到，变量极性相反。最大项内部是OR，不是AND；多个最大项之间才是AND。完整 $Σm$ 定义的函数，在未列入且未另标don't-care的行上是0，不能任意补漏项。
''')

insert(F, '> [!example]- Truth Table and Boolean Expression · 推导与例题', r'''
### 真值表与标准式的双向映射 (table conversion)

真值表把域内每一组合写成一行，因此域决定行数、每个标准项的文字数及编号意义。标准SOP记录ON行号，标准POS记录OFF行号；完全指定函数的两个集合不交且并为全集。例 $F=\sum m(3,4,6,7)=\prod M(0,1,2,5)$ 在ABC的8行上均给 `00011011`。

表达式转表：标准SOP将列出的行置1、其余0；标准POS将列出的行置0、其余1。非标准表达式必须逐行代值或展开其覆盖集合，不能假定一项只代表一行：ABC域中AB覆盖2行、C覆盖4行。简化式 $BC+A\bar C$ 也不能直接读出两个行号。

表转式：固定域与顺序 → 写全输出规范 → 收集ON/OFF → 分别写最小项之和/最大项之积 → 按要求化简 → 验证全部指定行。完全指定且有k行1时，标准SOP有k项、标准POS有 $2^n-k$ 项；选较少的一侧便于**写标准式**，但不能据此证明它化简后或门级实现一定更便宜。

### “Don't Care”表注与规范X的区别 (table annotation)

讲义p.43–44在逐项填表时所标的“不用再关心此项”，表示某个minterm/maxterm对此行的**汇总结果没有决定作用**。该项的数学值仍是确定的：其他行的minterm为0、maxterm为1，不可随意更改。这种过程表注不同于规范允许任意输出的don't-care condition (X)。

真正的X行可以使两个合法实现产生不同值；此时ON/OFF/DC三集合共同划分全集，不能无视DC就把ON与OFF宣称为严格互补。输入端X若表示此输入“不影响本行条件”，通常只是压缩若干确定输出行，也不等于输出无指定。详见 [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|don't-care]]。

常见错法是漏表行、变量顺序变动、非标准项误读单行、将 $Σm$ 与 $ΠM$ 同一行号列表照抄、化简后未回核。抽查被删项原本为1的行可找错，完整穷举或合法推导才证明等价。
''')

insert(F, '> [!example]- Sum-of-Products Form · 推导与例题', r'''
### Sum-of-Products Form · 形态、标准式与构建步骤

与或式 (sum-of-products, SOP) 为 $F=P_1+\cdots+P_k$，每个P为文字的乘积；任一乘积项为1即使F为1。单独一个文字也算乘积项。$AB+BC+DE$、$A+BC+DEF$是SOP；$DF+E(A+B)$不是直接SOP，需要先分配展开。

标准/正则SOP (standard/canonical SOP) 的每项都是域内的最小项，称最小项之和 (sum of minterms)。域为ABC时 $A\bar BC+AB$ 是SOP但不标准；补C后为 $A\bar BC+ABC+AB\bar C$。最简式有时仍然标准，例如两变量XOR的两项各有A/B，不能把“简化SOP通常不标准”误成必然。

编号 $\sum m(1,3)$ 表示OR两个最小项，不是求1+3。构建步骤是固定域/顺序 → 选输出1行 → 按1原/0補写每个 $m_i$ → 相或 → 核对项数等于ON行数、每项含全域、全部行与表相符。若项缺Z，用 $Z+\bar Z=1$：$P=P(Z+\bar Z)=PZ+P\bar Z$，缺多个变量则重复，合并重复最小项。

每个有限布尔函数都可由ON行机械写成标准SOP；全0函数为0（空OR），全1函数含全部最小项后化为1。形式上的AND→OR两级不计输入取补层；实际反变量生成、扇入限制和负载可能增加门/级数。SOP圈1、NAND-NAND映射与成本见 [[Karnaugh Map Minimization#2 · SOP 圈 1：覆盖与最小性|K图SOP]]、[[Universal Gates and Bubble Pushing]]。

“SOP”要求项的形态，“standard SOP”要求全域，“minimum SOP”要求指定成本最小，三者不能替代。补变量不能乘 $Z\bar Z=0$；域增添输入后所有标准项都要补齐；题目要标准式时不能只交缩短式。
''')

insert(F, '> [!example]- Product-of-Sums Form · 推导与例题', r'''
### Product-of-Sums Form · 形态、标准式与构建步骤

或与式 (product-of-sums, POS) 为 $F=S_1\cdots S_k$，每个S为文字的和；任一和项为0即使F为0。单独一个文字可算和项。$(A+B)(C+D)(E+F)$、$A(B+C)(D+E)$是POS；$(D+E)(F+GH)$的第二个括号有AND，需先用 $F+GH=(F+G)(F+H)$ 拆成POS。

标准/正则POS (standard/canonical POS) 的每个和项是含全域的最大项，称最大项之积 (product of maxterms)。编号 $\prod M(0,2)=(A+B)(\bar A+B)$ 在AB四行输出 `0101`，与 $\sum m(1,3)$ 为同一个函数；乘积号是AND各个最大项，列表数字只是编号。

构建步骤是固定域/顺序 → 选输出0行 → 按0原/1補写各 $M_i$ → 相与 → 核对括号数等于OFF行数、每项含全域、全部行与表相符。缺Z的和项S可补 $Z\bar Z=0$：$S=S+Z\bar Z=(S+Z)(S+\bar Z)$。单纯乘 $(Z+\bar Z)=1$ 虽等价，**不会完成标准POS的补变量结构**，需要正确分配。

全1函数可写空AND=1，全0函数含全部最大项后化为0。标准POS选0行而非1行；最大项内部OR、项间AND，圈0读出极性与SOP相反。简化POS不必含全域，单文字如C可看作一个和项，$C\bar M$则为两个一文字和项。

POS直接实现为OR→AND，也可用NOR-NOR；选SOP/POS应先满足题目所需形式，再比较化简后的项数、总文字、取补及实际器件代价。对一个SOP取一次补得到的是**反函数**的POS，不是同一函数自动转形。正确同函数形式可由OFF行或两次取補建立。
''')

insert(F, '> [!example]- Boolean Expression Simplification · 推导与例题', r'''
### 化简的前提、成本与步骤 (simplification method)

布尔化简 (Boolean simplification) 用等价改写减小文字数 (literal count)、项数 (term count) 或嵌套深度；目标须说明是两级SOP/POS，还是具体门族的实现。通常按“先最少项数，再在这些方案中最少总文字数”比较两级最小式；不应要求“每一项各自最短”而忽略覆盖全局。

文字数近似反映门输入用量，项数近似反映第一级门数；它们不是门级面积、功耗或延迟的精确换算。提因子可能减少文字却增加级数；共享反变量、可用门族、负载和冒险约束都会改变最优实现。手工化简只证明所得到式子的等价与代价；K图也须完成全局覆盖比较才可证明最小，不能因画了图就自动宣布minimum。

1. 固定域、全部指定行与目标形式，先处理长横线或明显可立即吸收的结构。
2. 按需要分配展开或提公共因子，不强求所有题都先爆展开成完整SOP。
3. 找只差一个变量正反的项：$XY+X\bar Y=X$；两项若差两个变量就不能照此消去。
4. 用Rule10吸收 $X+XY$，用Rule11处理 $X+\bar XY$；它们是不同结构。
5. 需要制造伙伴时，将已有项乘 $Z+\bar Z=1$ 再展开；不是凭空添加任意项。重复已有项也可由幂等性合法引入。
6. 每步写规则依据，直到无明显吸收/配对，再验证全部指定行并比较候选成本。

XOR/XNOR可先展开为AND/OR/NOT再使用这些规则，也可直接使用已证XOR恒等式，并非一定必须展开。$A\bar B+\bar AB$ 是两变量XOR，不可化成B；$AB+AC+B$ 仍可吸收为 $AC+B$。表达式短不能证明正确，也不能用化简修正已写错的规范；表错必须回到需求修改。

**English answer pattern:** “Each simplification step must preserve the Boolean function on every specified input. A shorter expression is not necessarily a minimum expression or the fastest physical implementation.”
''')

insert(K, '> [!example]- Karnaugh Map · 推导与例题', r'''
### 布局、坐标与代数含义 (layout and adjacency)

每格代表一个输入组合，即一个最小项的座位，n变量有 $2^n$ 格。三变量通常2×4、四变量4×4；本课图中AB/CD的行列有转置，读图必须以图上的变量标签为准，不能按画面位置猜位权。

| 变量数 | 一种惯用行标签 | 列标签 | 格数 |
|---|---|---|---|
| 3 | C=0、1 | AB=00、01、11、10 | 8 |
| 4 | CD=00、01、11、10 | AB=00、01、11、10 | 16 |

自然二进制编号用于行号，Gray排列用于格子位置，两者不可混淆。AB=10、CD=01表示输入1001，对应 $m_9$；不是把第几列第几行直接拼成自然序号。行列转置不改变逻辑邻接；首尾回绕、四角可共同成组，对角线通常差两位，不能组成二格组。

组对应一个布尔子立方体 (Boolean cube)：k个自由变量必须出现全部 $2^k$ 种组合，其余变量固定。三/四变量图上的合法组是边长为2的幂的矩形，可跨边界；总格数为2的幂还不充分，L形4格也非法。组大小 $2^k$ 时消去k个变量、保留n−k个文字，其代数基础是 $X\bar Y+XY=X$。

### 适用规模与证明责任 (validity)

先有完整的0/1/X规范或准确标准项列表，才能填图；遗漏格就是改变函数。K图适于少变量的人工化简，5变量可用两张相关图、6变量也有扩展画法，但更大域通常由算法/综合工具处理。Quine–McCluskey等精确算法本身也会随规模增长，不能把它说成任意大问题的轻松替代。

分组结果必须在所有指定行正确；“最大组”降低单项文字数，“最小覆盖”降低整个函数项数，两者不同。物理静态冒险可能要求冗余共识项 (consensus term)，这时应清楚说明优化目标包含时序要求，见 [[Propagation Delay and Logic Hazards]]。
''')

insert(K, '## 3 · POS Minimization with Karnaugh Map · 圈 0 读和项', r'''
### SOP圈组五规则与全局覆盖 (cover method)

1. 覆盖每个指定1至少一次，不能含指定0；允许组间重叠。
2. 按横/竖邻接构成矩形，不能斜着圈，不能圈3格、6格或L形。
3. 每个方向跨度为1、2、4…，并试图扩成更大合法组。
4. 使用左右/上下边界回绕，四角可成四格组。
5. 各组内恒1的变量原写、恒0的变量取補，变化变量消去，最后将乘积项相OR。

主蕴含项 (prime implicant) 是不能再扩大的合法1组；必要主蕴含项 (essential prime implicant) 覆盖了至少一个**不被其他主蕴含项覆盖**的指定1。先选必要项，再为其余1比较候选覆盖。只看某格“好像只有一种画法”容易漏掉另一种最大组，应核对全部候选主蕴含项。

最小两级SOP通常按项数首先最少，其次在该项数下使**总文字数**最少。一个覆盖所有1的合法方案，只证明正确；一组一组都已扩到最大也未必证明全局minimum。可用必要项证明下界，再比较剩余覆盖，或用精确覆盖算法确认。删除一个组前应检查是否仍覆盖全部指定1。

零函数没有1组，结果为0；全1图可圈全域，所有变量消去，结果为1。最后列出每组行号、保留/消去变量、最终式，并回代完整指定真值表。最小SOP与最小POS项数、文字数及实际门族成本需分别比较。
''')

insert(K, '> [!example]- POS Minimization with Karnaugh Map · 推导与例题', r'''
### 圈0是反函数的SOP再取補 (POS method)

对 $\bar F$ 圈1，就等价于对F圈0；若 $\bar F=T_1+\cdots+T_r$，由DeMorgan得 $F=\bar T_1\cdots\bar T_r$。所以每个零组读为一个**和项 (sum term)**，最后相与；仅当组只有一格并含全域变量时，这一和项才是严格的**最大项 (maxterm)**。扩大的零组不再包含全域，不能都称为maxterm。

| 组内变量 | 圈1的乘积项 | 圈0的和项 |
|---|---|---|
| 恒0 | $\bar X$ | X |
| 恒1 | X | $\bar X$ |
| 有变化 | 消去 | 消去 |

步骤是按变量标签填0/1/X → 找最大合法零组（包括孤立单格） → 先选必要零组再比较覆盖 → 依上表读和项 → 所有和项AND → 验证指定0全为0、指定1全为1。零组不得包含指定1，必须覆盖全部指定0，允许重叠、回绕和有帮助的X。

误用圈1的极性或把零组项写成“乘积相OR”都改变函数；不能概括成“任何极性误写都会恰好得到反函数”，须回代实际式子查错。全0图圈全域得和项0、F=0；全1图没有零组，空AND得F=1。无X时最小SOP/POS逐行等价；有X时只需在全部指定行一致，各自完成的X行可能不同。
''')

insert(K, '> [!example]- Karnaugh Map with Don\'t Cares · 推导与例题', r'''
### 三类格的义务与X的来源 (don't-care specification)

无关条件 (don't-care condition) 是规范允许该输入行输出0或1，记X；它不是硬件的第三逻辑输出。两类来源为：系统保证不会出现的输入组合，或该组合下此输出不被使用/没有要求。BCD的1010–1111是非法数字码，但只有系统排除这些输入或输出规范真的无要求时，才能设X；错误、上电或传输过程是否会触发非法码，需要结合完整系统判断。

| 格 | SOP圈1 | POS圈0 |
|---|---|---|
| 指定1 | 必须覆盖 | 禁止纳入 |
| 指定0 | 禁止纳入 | 必须覆盖 |
| X | 可作1扩大有用组，也可不用 | 可作0扩大有用组，也可不用 |

X不改变几何规则。不要新增只覆盖X的冗余组，不要求覆盖全部X，也不要求所有X取同一值；不同组共享X时可以同时覆盖，最终式在每个X行仍只有一个确定稳态值。

### 利用X与回读结果 (method and pitfalls)

先填好ON/OFF/DC全集，可先把X固定为0作SOP基准（POS基准固定为1），再把有帮助的X纳入更大组，比较整个覆盖的项数与文字数，最后回读全部指定行以及所选实现的X行。基准不是必须先做一次完整最小化，目的只是展示X提供的收益。

利用X可能只减少文字数、也可能减少项数，不能承诺一定“两者都变少”。圈了某个X后最终输出由所选方程固定，不能运行时随机选择。若回读发现某个X行需要报警、全灭或状态恢复，该行其实有要求，应把它改为0/1再重新最小化；不要在化简后继续称其任意。

分开做SOP和POS时可以选择不同X完成方式，各自在指定行满足同一不完全规范；这不保证两式在X行也相等。BCD完整显示接口见 [[Seven-Segment Display and Code Conversion]]，状态恢复见 [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|未用状态]]；表格中输入X的压缩记号与输出don't-care定义须分开。
''')

def replace(target, old, new, count=1):
    assert old in texts[target], (target,old)
    texts[target]=texts[target].replace(old,new,count)

# Correct misleading retained statements without removing the existing worked cases.
replace(G, '传播延迟只移动响应边沿。', '在固定延迟模型中可据传播延迟移动响应边沿；真实门还需区分两种转换延迟及脉冲响应。')
replace(G, '——**延迟不改变占空比，只把整条波形推后**。', '——**本例假定两种转换延迟相同，所以占空比不变；真实门的两种延迟不同则可改变占空比**。')
replace(G, '延迟变成 $2t_{pd}$、晶体管数量翻倍、功耗更大。', '在每级延迟都为 $t_{pd}$ 的假设下总延迟为 $2t_{pd}$；晶体管数量和功耗则取决于具体两级结构与专用buffer的实现，不能一概推定倍数。')
replace(G, 'NAND 的输出列 `1,1,1,0`，逐位取反得 `0,0,0,1`，正是 NOR 的输出列 ✓（两表互补）。', 'NAND输出列为 `1,1,1,0`，NOR为 `1,0,0,0`，并非逐位互补。将NAND的输入和输出同时取反，则得到NOR；01/10两行也验证这一点。')
replace(G, '紧挨着它左边的第四张是 NAND，两列恰好互补', '紧挨着它左边的第四张是NAND，两者互为对偶、输出列并非逐位互补')
replace(G, '$A$ 两格一个周期、$B$ 一格一个周期', '$A$ 的周期为4格、$B$ 的周期为2格')
replace(G, '**⑤ 工程直觉：为什么 NOR 常被"NAND + 反相器"替代**', '**⑤ 工程直觉：比较静态CMOS中的NAND与NOR**')
replace(G, '所以**凡是能用 NAND 搭的逻辑，实际芯片里往往真的全用 NAND 搭**', '因此NAND在基本静态CMOS实现中常有面积/结构上的优势，但不能据此断言实际芯片全用NAND')
replace(G, '所以同一工艺下 NAND 往往比 NOR 快、面积也更划算 —— 这也是后面组合逻辑综合时偏爱 NAND 的原因', '在相同晶体管尺寸等简单比较条件下，串联PMOS的NOR上拉可能较弱；实际尺寸优化、输入数与负载会改变速度/面积结果。NOR不能简单用相同输入的NAND再反相替代，那会得到AND；需结合DeMorgan及输入取补转换')

replace(L, '用讲义 p.23 的实测值画出两个真实家族', '用讲义 p.23 的示例限值画出两个家族')
replace(L, r'0 区间 $[0,\,0.4]$ V、过渡带 $[0.8,\,2.0]$ V、', r'驱动LOW保证区间 $[0,\,0.4]$ V、接收未保证开区间 $(0.8,\,2.0)$ V、')
replace(L, r'1 区间 $[2.4,\,5]$ V；', r'驱动HIGH保证区间 $[2.4,\,5]$ V；')
replace(L, '接口规范只需要四个数就能描述一条曲线，因为曲线两端是平的、中间是陡的。', '四个限值足以表达这一层静态接口兼容要求，但不能重建整条VTC，也不能代替所有器件参数。')
replace(L, r'CMOS 动态功耗 $P = C\,V_{DD}^{2}f$，与 $V_{DD}$ **平方**成正比。', r'CMOS充放电动态功耗模型 $P_{dyn}\approx\alpha C_{eff}V_{DD}^{2}f$，其中活动因子 $\alpha$ 无量纲、有效电容 $C_{eff}$ 单位F、频率f单位Hz；下方比值假定三者不变，仅比较动态项。')
replace(L, '代价是**噪声容限的绝对值一起变小**：3.3 V 的 LVCMOS 只有 $NM_H=0.9$ V、$NM_L=0.54$ V，而 5 V 的\n> TTL 已经"只有" 0.4 V。', '若同一模型的全部电平限值按供电同比缩放，**噪声容限绝对值也同比下降**；跨逻辑族不能只按电源大小比较：3.3 V LVCMOS例的 $NM_H=0.9$ V、$NM_L=0.54$ V，反而大于5 V TTL例的0.4 V。')
replace(L, '两者都 $\\ge 1.8$ → 都是 **1**（该器件 $V_{DD}=3.3$ V，\n>    4.99 V 已超电源，实际会打到输入保护二极管，这里只做门限判断）。', '3.2 V在所给容许输入范围内可判为1；4.99 V虽超过HIGH阈值，却必须另查是否有5 V tolerant输入与容许电压，不能单凭阈值宣布是合法1或断言一定有某种钳位结构。')
replace(L, '驱动器连"最低的高电平"都到不了对方的门限，必须加电平转换。', '驱动器的最低HIGH保证低于接收要求，因此直连没有HIGH识别保证；可选择合适家族或电平转换。')
replace(L, r'若输出恰好落在 }V_{OH}(\min)\text{，这个压降就会读错}', r'若输出恰好落在 }V_{OH}(\min)\text{，这个压降会使HIGH识别失去保证}')
replace(L, 'V $<2.0$ V → 读错。', 'V $<2.0$ V → 进入未保证区，HIGH识别失去保证。')
replace(L, r'$4.5\ge1.8$（LVCMOS）✓ —— 这个例子里的信号**没有**被读错。', r'$4.5\ge1.8$（LVCMOS）仅是阈值比较，还需确认该输入可容许4.5 V；对例题的5 V TTL接收端，该实测信号仍是HIGH。')
replace(L, '真实门的过渡带都要吃掉约四分之一电源', '这两个课程示例的输入未保证带宽约为各自电源的四分之一，不能作为所有真实门的通用比例')
replace(L, '邻线串扰 $+0.15$ V', '同方向负向串扰的退化幅度0.15 V')
replace(L, '$V_M$ 上移意味着"更容易被判成 1"，高电平方向的余量被吃掉。', '$V_M$ 上移意味着反相器由HIGH输出切向LOW输出通常需要更高输入电压；若 $V_{IH}$ 同时上移，高电平方向余量会缩小。不能只由交点移动定量推出保证边界。')
replace(L, '$n$ 管关断、$p$ 管导通', '接近输出HIGH平台；MOS导通区域取决于晶体管阈值与输入位置')
replace(L, '$p$ 管关断、$n$ 管导通', '接近输出LOW平台；MOS导通区域取决于晶体管阈值与输入位置')
replace(L, '饱和区（左）', '稳定平台区（左）')
replace(L, '饱和区（右）', '稳定平台区（右）')
replace(L, '两管都导通，电流急剧变化', '两管可能同时导通，输出对输入较敏感')
replace(L, r'斜率 $=\lvert A\rvert$ 最大', '斜率为负，其绝对值在过渡区通常较大')
replace(L, '$V_M=2.5$ V 是它与 $V_{out}=V_{in}$ 直线的交点', '本例规定的切换位置为2.5 V；缓冲器与 $V_{out}=V_{in}$ 的交点不一定唯一')

replace(A, '四个变量组合类别由 A决定', '输入组合可按A的两种取值分类')
replace(A, '枚举 4 行可见两式**不是同一个式子**', '对三变量应枚举8行；这里用一行即可见两式**不是同一个函数**')
replace(A, '**1. 规则从公理来：以 Rule 5 ($A+A=A$) 为例**', '**1. 用已证规则演示Rule5：$A+A=A$**')
replace(A, '一条"看起来显然"的规则也可以由公理推出来（讲义 p.20 的 Method 2）：', '假定所用规则已经独立建立，可用以下等价链演示Rule5（讲义p.20的Method2形式）。这不是Rule5的基础推导：若Rule12本身依赖幂等性，就不能用未证的Rule12回头建立Rule5，否则形成循环论证。')
replace(A, '因为 $A+0=A$ 本身是恒等式', '因为本例F简化成自对偶的函数A；恒等式本身并不保证其中的函数自对偶')
replace(A, '而是取决于"上一次留下的值"，这正是**记忆**。', '还需初始条件和动态电路确定；适当的稳定反馈可能实现记忆，不能仅凭这条方程保证实际存储。')
replace(A, '> | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 ✓ |', '> | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 ✓ |')
replace(A, '> | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 ✓ |', '> | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 ✓ |')
replace(F, r'$m_{11}=0\cdot1\cdot0\cdot0=0$', r'$m_{11}=0\cdot0\cdot0\cdot0=0$')
replace(F, r'(b) $B\bar C$ 是 literal 的乘积 → **implicant**；只有 2 个 literal、缺 $A$ → 不是 minterm。', r'(b) $B\bar C$ 是文字的乘积项；只有2个文字、缺A，因此不是minterm。尚未指定函数F，不能无条件称其为F的implicant；若F在该项覆盖的两行都为1，它才是F的蕴含项。')
replace(F, '每一行里只有"属于本行"的那一项为 1，另外两项为 0（标 Don\'t Care）', '在ON行里，属于本行的那一项为1、其他项为0；非ON行所有已列项为0。下表保留讲义的Don\'t Care过程标注，但这些项值确定为0，不是输出X')
replace(F, '第 1 行 $0+0+1=1$ ✓、\n> 第 4 行 $1+0+0=1$ ✓、第 7 行 $0+0+1=1$ ✓', '索引1行的三项依次为 $1+0+0=1$ ✓、\n> 索引4行为 $0+1+0=1$ ✓、索引7行为 $0+0+1=1$ ✓')
replace(F, '（不在列表里的 $M_1,M_4,M_7$ 在本行取 1，按讲义的写法标 Don\'t Care）', '（在索引1、4、7行，表中已列出的五个maxterm全为1；本行的 $M_i$ 虽本应为0，却未包含在乘积中，所以输出为1。Don\'t Care仍只是过程表注）')
replace(F, '是化简里唯一"越写越长"的动作', '是化简中一种有意增加项数的合法动作（幂等复制已有项也是另一种）')
replace(F, r'原式 $=0+0+1=1$，结果 $=0+1=1$', r'原式 $=0+1+1=1$，结果 $=0+1=1$')

# General terminology corrections in the retained K-map material.
texts[K]=texts[K].replace('每个圈读成一个 maxterm', '每个圈读成一个和项（单格且含全域时为maxterm）')
texts[K]=texts[K].replace('**Read zero groups as maxterms · 零圈怎样读最大项**', '**Read zero groups as sum terms · 零圈怎样读和项**')
texts[K]=texts[K].replace('圈 **0** → 每个圈读成一个 maxterm', '圈 **0** → 每个圈读成一个和项')
texts[K]=texts[K].replace('圈 1 得到一对互补形式', '圈 1 得到同一函数的两种形式')
texts[K]=texts[K].replace('**Example 2 — 三变量 POS：圈 0 与圈 1 得到一对互补形式**', '**Example 2 — 三变量 POS：圈0与圈1得到同一函数的两种形式**')
# Keep present figures but flag a misleading grouping caption: the B=1 region contains zeros.
replace(K, '$B=1$ 的两行四列与 $A=1,C=1$ 的四格、外加 $B=C=D=0$ 的一对', '$B=D=1$ 的四格、$B=C=1$ 的四格、$A=C=1$ 的四格，以及 $B=C=D=0$ 的一对（B=1的整片区域含指定0，不能圈成八格）')
texts[K]=texts[K].replace('（`verify_ch34.py` 对 16 行逐行比对通过）。', '（逐行穷举检查）。')
replace(K, r'全部 8 行（$m_7\ldots m_0$ 顺序读）', r'全部8行（$m_0\ldots m_7$ 顺序读）')
replace(K, r'（1 项做不到：$m_3$ 不与 $m_0,m_1,m_4,m_5,m_6$ 中任何一个相邻）', r'（一个乘积项的ON集合必须有 $2^k$ 格，不能恰好覆盖本题3个1；所给两组达成下界）')
replace(K, '都是被孤立 1 逼出来的必需项', '各覆盖了只能由该主蕴含项覆盖的指定1格，因而都是必要主蕴含项')
replace(K, r'$m_0$ 与 $m_{10}$ 在图上是"斜对角"，但沿着边界回绕后它们是相邻的', r'$m_0$与 $m_{10}$本身相差A/C两位，不能独立圈成二格；四角组 $\{0,2,8,10\}$ 同时包含A/C的全部组合，因而可作为回绕四格矩形')
replace(K, r'（$0001$：$A=0,C=0,\bar B\bar D=0\cdot1=0', r'（$0001$：$A=0,C=0,\bar B\bar D=1\cdot0=0')

def remap_links(text):
    text=text.replace('Boolean Forms and Algebraic Simplification 1','Boolean Forms and Algebraic Simplification')
    canon=set(MAP['old_to_new'].values())|{'ECE2050 Knowledge Tree','Glossary'}
    def fn(m):
        full=m.group(1); ref,sep,display=full.partition('|'); name,hashmark,heading=ref.partition('#')
        if name in canon or name not in LINKS:
            return m.group(0)
        hit=LINKS[name]
        dest=hit['target']+'#'+hit['heading']
        if hashmark: # Legacy subheadings no longer exist: route to the merged source section.
            dest=hit['target']+'#'+hit['heading']
        return '[['+dest+'|'+(display if sep else name)+']]'
    return re.sub(r'\[\[([^\]\n]+)\]\]',fn,text)

for target,t in texts.items():
    t=remap_links(t).replace('\r\n','\n').replace('\r','')
    # Avoid duplicate spelling of the row-string example, and preserve canonical H2 anchors.
    t=re.sub(r'\n{4,}','\n\n\n',t)
    t=t.replace('補','补')
    assert not any(ord(c)<32 and c not in '\n\t' for c in t),target
    texts[target]=t
    (OUT/(target+'.md')).write_text(t,encoding='utf-8')

# One record for every original numbered/top-level subsection, with a navigable destination.
source_heads={
    'Logic Gates':(G,'1 · Logic Gates · 统一的布尔模型','门的分类、符号与描述方式 (classification and representations)'),
    'Inverter':(G,'2 · Inverter, AND Gate and OR Gate · 三种基本运算','Inverter and Buffer · 单输入功能与适用边界'),
    'AND Gate':(G,'2 · Inverter, AND Gate and OR Gate · 三种基本运算','AND Gate · 同时满足、许可与门控'),
    'OR Gate':(G,'2 · Inverter, AND Gate and OR Gate · 三种基本运算','OR Gate · 包含或与控制值'),
    'NAND Gate':(G,'3 · NAND Gate and NOR Gate · 输出取补与气泡','NAND Gate · 先与后取补'),
    'NOR Gate':(G,'3 · NAND Gate and NOR Gate · 输出取补与气泡','NOR Gate · 先或后取补'),
    'Exclusive-OR Gate':(G,'4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性','Exclusive-OR Gate · 模2加法、受控反相与奇数性'),
    'Exclusive-NOR Gate':(G,'4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性','Exclusive-NOR Gate · 两位相等、偶数性与校验边界'),
    'Logic Levels':(L,'1 · Logic Levels · 保证值与接受范围','四个保证边界与电压区间 (guaranteed interface limits)'),
    'DC Transfer Characteristic':(L,'2 · DC Transfer Characteristic · 由传输曲线理解恢复能力','VTC读数与模型适用范围 (curve interpretation)'),
    'Noise Margin':(L,'3 · Noise Margin · 接口的预算','噪声来源与两侧预算 (noise sources and polarity)'),
    'Combinational Circuit':(A,'1 · Combinational Circuit · 先确认可以使用的模型','完整电路描述、节点与构成条件 (composition)'),
    'Boolean Equation':(A,'2 · Boolean Equation · 从需求写函数','二值命题、运算词典与优先级 (Boolean specification)'),
    'Boolean Axioms':(A,'3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则','A1–A5与对偶原理 (axioms and duality)'),
    'Laws and Rules of Boolean Algebra':(A,'3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则','三条定律与十二规则完整表 (laws and rules)'),
    "DeMorgan's Theorems":(A,"4 · DeMorgan's Theorems · 取补必须覆盖整个子式",'横线的范围、门级等价与递归步骤 (DeMorgan method)'),
    'Proof by Perfect Induction':(A,'5 · Proof by Perfect Induction · 穷举与代数验证','完全穷举与代数证明的选择 (proof methods)'),
    'Minterm and Maxterm':(F,'1 · Minterm and Maxterm · 一行对应一个项','文字、乘积项与编号全集 (terms and domain)'),
    'Truth Table and Boolean Expression':(F,'2 · Truth Table and Boolean Expression · 用真值表定义全集','真值表与标准式的双向映射 (table conversion)'),
    'Sum-of-Products Form':(F,'3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式','Sum-of-Products Form · 形态、标准式与构建步骤'),
    'Product-of-Sums Form':(F,'3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式','Product-of-Sums Form · 形态、标准式与构建步骤'),
    'Boolean Expression Simplification':(F,'4 · Boolean Expression Simplification · 保持函数再比较代价','化简的前提、成本与步骤 (simplification method)'),
    'Karnaugh Map':(K,'1 · Karnaugh Map · 为什么相邻格能够合并','布局、坐标与代数含义 (layout and adjacency)'),
    "Karnaugh Map with Don't Cares":(K,"4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务",'三类格的义务与X的来源 (don\'t-care specification)'),
    'POS Minimization with Karnaugh Map':(K,'3 · POS Minimization with Karnaugh Map · 圈 0 读和项','圈0是反函数的SOP再取補 (POS method)'),
}
corrections={
    'Logic Gates':'区分负逻辑与active-low；输入数分类非数学硬限制；输出1数量只是认门线索；多输入=1与奇数性区分。',
    'Inverter':'实际转换延迟可不对称、改变占空比；电压会连续过渡；两级NOT与专用BUF的功耗/晶体管数不可泛化。',
    'AND Gate':'固定输入1为AND恒等许可，原稿说不能让输入不限制其余条件过度绝对。',
    'OR Gate':'包含或与恰好一个/奇数性区分；与AND是对偶而非输出互补。',
    'NAND Gate':'不重不漏的真值表排序均合法；单输入退化有数学定义。',
    'NOR Gate':'NAND/NOR不是逐行互补；不同实现成本不能无条件泛化。',
    'Exclusive-OR Gate':'多输入恰好一个与奇数性区分；原稿三者只在11分歧的说法对XNOR并不成立，改为完整表与各定义。',
    'Exclusive-NOR Gate':'区分整体XOR取補与二输入XNOR级联；XNOR可结合但归约极性随输入数变化；校验生成与检查分开。',
    'Logic Levels':'接收范围更宽；未保证区开区间；不兼容意味着不保证非必然失败；保证条件限定；过压容许能力另查。',
    'DC Transfer Characteristic':'保证输入阈值/典型单位增益点/VM/晶体管VT分开；反相器为负斜率；缓冲器交点非通用VM；同比缩放需假设。',
    'Noise Margin':'超界为失去保证不等于必定逻辑翻转；噪声预算按方向；IR需电流；跨域保证参数条件各自适用。',
    'Combinational Circuit':'稳态无记忆不等于无动态历史；有反馈不必为稳定存储；区分外部输入与无内部驱动。',
    'Boolean Equation':'布尔方程亦可显式描述状态更新；组合规范才限定当前输入；抽查不证明。',
    'Boolean Axioms':'表达式可取对偶；恒等式两边取对偶才保证恒等；保留运算树而非简单字符替换。',
    'Laws and Rules of Boolean Algebra':'补全OR分配律；Rules1–9也可减少文字；合法子式可在横线内替换；POS直接OR→AND。',
    "DeMorgan's Theorems":'修正原误区中把正确展开误列为错误、把未覆盖A误取补；一次补得到反函数；当前折叠Example2的011/111两行中间值及011输出错误已直接修正。',
    'Proof by Perfect Induction':'n≥5并非方法失效；区分数学归纳法；并非所有证明途径只有两种。',
    'Minterm and Maxterm':'蕴含项须相对于F定义；最小项与乘积项形式分开。',
    'Truth Table and Boolean Expression':'标准式行少不证明实现最优；过程表注项值仍确定；有DC时ON/OFF非彼此严格补集。',
    'Sum-of-Products Form':'简化式有时仍标准；输入取补层/扇入增加实际级数；补变量因子精确。',
    'Product-of-Sums Form':'SOP一次取補不是同函数POS；补变量乘恒等因子合法但不完成标准POS结构。',
    'Boolean Expression Simplification':'最小需全局项数/总文字比较；K图非自动minimum；门成本非简单精确换算。',
    'Karnaugh Map':'最大组不必给最小覆盖；最小按项数优先总文字其次；扩大矩形须构成完整cube。',
    "Karnaugh Map with Don't Cares":'非法BCD不代表永远不出现；X收益可能只降文字不降项；SOP/POS在X行可不同。',
    'POS Minimization with Karnaugh Map':'扩大零圈对应和项而非全域maxterm；极性错不一定恰成反函数；修正p56B=1整片含零不合法。',
}
records=[]
for g in targets:
    for source in g['sources']:
        raw=(ROOT/'.scratch/consolidation-20261008/original-Notes'/(source+'.md')).read_text(encoding='utf-8-sig')
        headings=list(re.finditer(r'^(#{2,6}) (.+)$',raw,re.M))
        target,h2,h3=source_heads[source]
        records.append({'source':source+'.md','source_heading':'Where this fits / Quick recall / metadata','source_level':0,'status':'covered','target':target+'.md','target_heading':h2,'target_section':h2,'note':'原稿定位、先修/下游关系与英文速览已由canonical开头、对应H2定义及可见方法/关系段覆盖；原aliases保留于canonical前言。不复制原稿序号叙事。'})
        context=''
        for i,m in enumerate(headings):
            level=len(m.group(1)); heading=m.group(2).strip()
            if level==2: context=heading
            area=context.split(' · ')[0]
            status='restored'
            location=h3
            note='原内容融入当前主正文；原方法图与步骤语义合并，减少重复。'
            if area in ('Derivation','Worked Example') or area.startswith(('Gates as','Inversion,','Qualified','Inclusive','NAND as','NOR implementation','XOR as','Equality versus','Electrical','What a','Noise margins','Composition','Specification','Duality','Choose the','Move the','Exhaustive','Row identities','A table','Canonical SOP','Canonical POS','Preserve behavior','Group meaning','Don\'t-care freedom','Read zero','Ch5 Application')):
                status='covered';location=h2
                note='当前该H2内同名折叠“'+source+' · 推导与例题”已保留对应推导、表、例题或英文应用答句；未再次复制。'
            if area=='Connections':
                status='covered';location=h2
                note='有意义前置/实现/对照关系融入该H2及相邻H3；同一canonical内关系用H2/H3组织，未保留重复链接清单。'
            if area in ('Core Definition','Assumptions and Validity','Pitfalls','Method and Steps'):
                status='corrected';note=corrections[source]+' 其余正确定义、条件、表格和步骤已恢复到可见正文。'
            if source=='NOR Gate' and heading.startswith('④ 与 NAND'):
                status='corrected';note='保留对偶推导，纠正NAND输出逐位取补等于NOR的错误；同输入下NOR列为1000。'
            if source=='Karnaugh Map' and area in ('Worked Example','Derivation'):
                status='corrected';note='当前折叠例题保留；纠正m0/m10不是二格邻接、p50表顺序与最小性解释，并独立检查覆盖成本。'
            if source=='DC Transfer Characteristic' and area in ('Worked Example','Derivation'):
                status='corrected';note='保留静态模型与数值例，补充轨到轨、对称/线性及单位增益假设；反相器斜率与晶体管VT区分，缓冲器交点非通用VM。'
            if source=="DeMorgan's Theorems" and area=='Worked Example':
                status='corrected';note='全部原例题保留；Example2的011/111两行中间值及011行输出已修正，并逐项检查8行表。'
            records.append({'source':source+'.md','source_heading':heading,'source_level':level,'status':status,'target':target+'.md','target_heading':location,'target_section':h2,'note':note})

for entry in records:
    entry['target_heading']=entry['target_heading'].replace('補','补')
    entry['target_section']=entry['target_section'].replace('補','补')
report={'scope':'Ch3 and Ch4: 25 original notes into 5 canonical notes','files':[t+'.md' for t in texts], 'records':records, 'corrections':corrections, 'retained_current_h2':True, 'extra_files':{'DeMorgan\'s Theorems.md':'Parent confirmed identical original; its unique core/method/pitfall material integrated in canonical DeMorgan section. No move/delete.', 'Boolean Forms and Algebraic Simplification 1.md':'Parent confirmed empty; all references restored to canonical without changing extra file.'}}
(BASE/'coverage-ch34.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'written':list(texts),'records':len(records),'chars':{k:len(v) for k,v in texts.items()}},ensure_ascii=False))
