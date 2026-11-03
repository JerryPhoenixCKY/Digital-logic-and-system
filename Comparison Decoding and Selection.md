---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
updated: 2026-10-13
chapter: Ch6
aliases:
  - 比较译码与选择电路
  - Comparison Decoding and Selection
  - 比较译码与选择电路 · Ch6
  - Magnitude Comparator
  - 数值比较器
  - Digital comparator
  - Encoder and Priority Encoder
  - 编码器与优先编码器
  - Priority encoding
  - Priority Circuit
  - 优先电路
  - Decoder
  - 译码器
  - Binary decoder
  - Multiplexer and Demultiplexer
  - 多路选择器与分配器
  - MUX and DEMUX
  - 74HC85
  - 74LS85
  - 74HC147
  - 74HC154
  - 74HC42
  - 74HC151
---

# Comparison Decoding and Selection · 比较译码与选择电路

> [!SUMMARY] Quick recall · 英文速览
> Compare values, decode codes into lines, select one winning request, then route data. Codes, winner masks, and active polarity are different interfaces.

讲义对应：[PDF p.19–35](../ECE2050-Chap6.pdf#page=19) 为比较、编码和译码，[p.39–45](../ECE2050-Chap6.pdf#page=39) 为 MUX/DEMUX。以下芯片连接采用讲义的功能模型；输入 X 表示可取 0 或 1，不表示可以悬空。

## 1 · Magnitude Comparator · 最高不同位决定大小

数值比较器 (magnitude comparator) 对声明为 unsigned 的字从最高位向下比较。相等信号 $E=\prod_i\overline{A_i\oplus B_i}$；较大条件是在某位 $A_i\bar B_i$ 成立且更高位全相等。signed 比较先考虑符号，不能直接沿用无符号位权。

### Core Definition · 核心定义

本篇先比较同宽 unsigned $A,B$，输出 $E=(A=B)$，$G=(A>B)$，$L=(A<B)$，高有效 (active-HIGH)。稳定有效输入下恰好一个输出为 1。

> [!example]- Magnitude Comparator · 推导与例题
> **Derivation · 从一位到多位**
>
> 一位：$e_i=\overline{A_i\oplus B_i}$，$g_i=A_i\bar B_i$，$l_i=\bar A_iB_i$。
>
> 两位且 bit 1 为 MSB：
>
> $$E=e_1e_0,\qquad G=g_1+e_1g_0,\qquad L=l_1+e_1l_0.$$
>
> 四位：$G=g_3+e_3g_2+e_3e_2g_1+e_3e_2e_1g_0$，$L$ 对应把 g 换成 l，$E=e_3e_2e_1e_0$。低位判断被高位相等条件门控。
>
> The first unequal position determines the result because its weight exceeds the sum of all lower weights. For bit k, $2^k>2^k-1$, so lower bits cannot reverse that decision.
>
> **Worked Examples · 例题**
>
> **Example 1.** $A=10,B=01$：$g_1=1$，所以 G=1；低位的 $l_0=1$ 被 $e_1=0$ 屏蔽。若对所有 $g_i$ 直接 OR，会把低位的重要性看得过大。
>
> **Example 2.** $A=1010,B=1001$，最高两位相等，bit1 首次不同且 A=1，故 A>B。10>9 验证。
>
> **Cascading.** 两个 4-bit comparator 比较 8 位。低位模块比较结果接入高位模块的 cascade inputs；高位只有本地相等时才接受低位结论。最底层初始化为 equal=1、greater=less=0。不要把加法器的 carry chain 接法套成同名但无含义的信号。
>
> **Signed boundary.** 同一 `1000` 与 `0111`：unsigned 是 8>7；4-bit two's complement 是 −8<7。先比较符号，符号相同再按适当位串规则比较；等宽同符号补码的 unsigned 顺序一致。
>
> **Application · 最小值选择器**
>
> 要输出 $\min(A,B)$，用 G 控制 [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]]，G=1 选 B，否则选 A。若题目规定 A=B 为 don't-care，可利用这些行化简；这是接口的特例，不改变比较器本身的 equality 定义。

### Comparator Cascading · 比较结果由低位传给高位，p.22–23

级联输入 (cascading inputs) 是来自更低位的比较结论，不是第二组普通操作数。将八位字拆成高四位 H、低四位 L，定义每块的本地结论 $G_H,E_H,L_H$ 与 $G_L,E_L,L_L$，分别表示 greater、equal、less，且为高有效。对合法的一组三选一结论：

$$G=G_H+E_HG_L,\qquad E=E_HE_L,\qquad L=L_H+E_HL_L.$$

高位不相等时直接决定结果；高位相等时才透传低位结论。最底层的输入设为 $(I_{A>B},I_{A=B},I_{A<B})=(0,1,0)$，表示尚未比较的更低部分“相等”。

> [!example]- 74HC85/74LS85 cascade · 两个边界例题
> ![[ch6-comparator-cascade.png]]
> *讲义 p.23 原图：低位片的三个结果连接高位片的同名级联输入，最终输出取自高位片。*
>
> **Self-calculated checks：** $A=0011\ 0111$、$B=0011\ 1001$。高位均为 3，低位 7<9，所以最终 A<B。若 $A=0100\ 0000$、$B=0011\ 1111$，高位 4>3 已决定 A>B；低位 0<15 不可反转它。十进制分别为 55<57、64>63。
>
> Do not OR the two chips' greater outputs without equality gating. Also do not feed arbitrary simultaneous greater/equal/less assertions into these equations: the simplified cascade model assumes a legal comparison result, and the chip's complete function table defines other combinations.

### Method and Exam English · 方法与答题

- Start at the MSB, and continue only while the bits are equal.
- 明确 active-HIGH outputs；输出名 A>B 不是把 A 与 B 导线直接相减。
- Exhaustively test $2^{2n}$ operand pairs for a small n-bit comparator.

**Self-check:** Does XNOR on the two MSBs alone prove equality?

**Answer:** No. Every corresponding pair must be equal; AND all bitwise XNOR results. For two-bit inputs 10 and 11, the MSBs match but the numbers differ.

### Connections · 概念关系与应用

[[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-NOR Gate]] 构成逐位 equality；[[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]] 改变 signed 比较含义；按 [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]] 的规范验证，再与 [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码|Encoder and Priority Encoder]] 比较“最高位优先”的门控思路；[[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转|Cascaded Counters and Digital Clocks]] 展示比较/末态判断的系统应用。

## 2 · Decoder · 代码变线路

n-to-$2^n$ 译码器 (decoder) 为每种输入生成一个最小项 (minterm)。高有效输出 OR ON 行；低有效输出需按德摩根选择末级门。使能 (enable) 决定输出是否参与，扩展时高地址位选择芯片，低地址位送各片。

### Core Definition · 核心定义

2-to-4 decoder 输入 $A_1A_0$，高有效 enable E。正逻辑输出：

$$Y_0=E\bar A_1\bar A_0,\ Y_1=E\bar A_1A_0,\ Y_2=EA_1\bar A_0,\ Y_3=EA_1A_0.$$

若 E=0，四个输出全 0；若 E=1，恰好一条为 1。独热 (one-hot) 描述有效的输出；低有效译码器是独冷 (one-cold)，disabled 时通常全 HIGH，仍须看给定 function table。

### Enable and Pin Constraints · 使能与引脚条件

Enable inputs can have mixed polarity. A device requiring one HIGH and two LOW enables must receive that exact combination. Translate a named chip's table into an enable predicate first; do not assume every enable pin is active-HIGH.

例如 74HC154 教学模型的两个外部使能为低有效：两者都 LOW 才选一路低输出。内部可能用一个正逻辑 E 表示“已使能”，这个 E 与外部引脚不是同一极性的信号。器件接线若依赖具体 pin number，应核对该器件资料。

> [!example]- Decoder · 推导与例题
> **Derivation · 为什么是 minterm**
>
> 输入的一行由每个变量取正或补的唯一乘积描述。decoder 输出正好实现这些乘积，因此 $F=\Sigma m(S)$ 可以 OR 集合 S 对应的输出。
>
> With active-low outputs $L_i=\bar m_i$, DeMorgan's law gives $F=\overline{\prod_{i\in S}L_i}$. Use a NAND across the selected LOW-active lines. Simply OR-ing them usually produces the wrong polarity.
>
> **Worked Examples · 例题**
>
> **XOR.** $F(A_1,A_0)=\Sigma m(1,2)$。高有效输出 $F=Y_1+Y_2$；低有效输出 $F=\overline{L_1L_2}$。输入 01 时一条所选线有效，F=1；11 时两条所选低有效线都 HIGH，NAND=0。
>
> **Full adder.** 输入 ABC，C 是 carry-in。sum 选 1,2,4,7；carry 选 3,5,6,7。先标清 decoder 的 A0 是否接 C，不能凭图中上下位置猜 MSB。
>
> **Expansion.** 用两个 2-to-4 块构造 3-to-8：低两位同时接两块，高位 A2=0 使能低编号块，A2=1 使能高编号块。最终 index=$4A_2+2A_1+A_0$。disabled block 不应驱动一个有效输出。
>

### 74HC154 Expansion · 两个低有效译码器组成 5-to-32，p.32–34

74HC154 为四线至十六线译码器 (4-line-to-16-line decoder)，输出和两个外部片选 (chip select) 均为低有效 (active-LOW)。设外部输入为 $\overline{CS_1},\overline{CS_2}$，内部正逻辑使能为：

$$E=\overline{\overline{CS_1}+\overline{CS_2}}.$$

两外部片选都 LOW 时 E=1；**E=1 表示使能，选中的输出反而为 LOW**。讲义 p.33 的“Output HIGH”指产生内部 EN 的 NOR 输出，不是选中的译码输出。

> [!example]- Five-bit decoder · 高位选芯片，低位选片内线路
> ![[ch6-decoder-expansion.png]]
> *讲义 p.34 原图：低地址 $A_3\ldots A_0$ 同时接两片；$A_4$ 及其反相控制低、高编号块。*
>
> 原图低块的两个低有效片选同接 $A_4$，高块的两个片选同接 $\bar A_4$，因此 $E_L=\bar A_4$、$E_H=A_4$。等价接法是每片一个片选接逻辑 0，另一片选分别接 $A_4$（低块）与 $\bar A_4$（高块）。令 $m_i$ 为低四位的第 i 个最小项 (minterm)，$i=0,\ldots,15$：
>
> $$L_i=\overline{\bar A_4m_i},\qquad L_{16+i}=\overline{A_4m_i}.$$
>
> $A_4=0$ 时选 0–15，$A_4=1$ 时选 16–31。原图蓝字是 **$\bar A_4=0$ when >15**：它对应高块低有效片选，不能漏读反相横线而解释成 $A_4=0$。
>
> **Self-calculated example：** 地址 `10110`=22，高块启用、片内地址 `0110`=6，所以全局 $L_{22}=0$；其余 31 条为 1。边界 `01111` 选 15，`10000` 选 16。稳定输入下应恰好一条 LOW，换片瞬间另按 [[Propagation Delay and Logic Hazards]] 检查。

### BCD-to-Decimal Decoder · 十条线路与六个非法码，p.35

BCD 至十进制译码器 (BCD-to-decimal decoder) 接收四位 8421 BCD，只为 0–9 提供十条输出，因而也称 1-of-10 decoder。讲义 74HC42 图采用低有效输出；它与十六输出的完整二进制译码器不是相同接口。

在十个四变量最小项的理想功能模型中，输入 `1001` 仅使 9 号输出 LOW；输入 10–15 不匹配任何合法十进制行，十条均 HIGH。这是非法 BCD 码 (invalid BCD code) 的“无线路选中”，不是数字 0，也不是普通编码器的“无输入”。从 p.35 的波形选定一个时段，先读 $A_3A_2A_1A_0$，再检查哪条低有效输出下降；短暂毛刺需另行分析。

### Method and Review · 方法与复习

1. Write the decoder's bit ordering and enabled condition.
2. Determine whether selected outputs are HIGH or LOW.
3. Map input rows to output indices.
4. Choose OR, NAND, or polarity conversion accordingly.
5. Check both an ON row and an OFF row, then enumerate all rows.

**Self-check:** An enabled 3-to-8 decoder has input 101. Which line is selected?

**Answer:** Line 5. Its voltage is 1 for active-HIGH outputs or 0 for active-LOW outputs.

### Connections · 概念关系与应用

每条线对应 [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项|Minterm and Maxterm]] 的一行；可实现 [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]] 或 [[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路|Binary Subtractors and Adder-Subtractors]] 的 ON sets。与 [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码|Encoder and Priority Encoder]] 比较码→线/线→码方向；用于 [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]] 的地址片选与 [[Seven-Segment Display and Code Conversion]] 的显示转换。

## 3 · Encoder and Priority Encoder · 线路变代码

普通编码器 (encoder) 假设至多一条请求有效。优先编码器 (priority encoder) 选最高优先请求，四路输入 $D_3>D_2>D_1>D_0$ 的获胜掩码 (winner mask)：

$$W_3=D_3,\ W_2=\bar D_3D_2,\ W_1=\bar D_3\bar D_2D_1,\ W_0=\bar D_3\bar D_2\bar D_1D_0.$$

二位二进制码 (binary code) 为 $Y_1=D_3+D_2,Y_0=D_3+\bar D_2D_1$，有效指示 (valid indicator) $V=\sum_iD_i$。这里 $\sum_iD_i$ 表示 Boolean OR。输入 0110 给掩码 0100、代码 10；0000 和 0001 的代码都可为 00，必须用 V 区分。

> [!IMPORTANT] X 的含义
> 1XXX 表示低优先输入任意变化仍给同一获胜输出；所有输入组合的输出仍已指定，不是可随便化简的输出无关项。

### Core Definition · 核心定义

编码器 (encoder) 将独热 (one-hot) 输入线路转为紧凑的二进制码 (binary code)。4-to-2 编码器输入 $D_0\ldots D_3$，输出 $Y_1Y_0$。普通编码器需约定同时最多一个输入为 1；优先编码器 (priority encoder) 取消这个限制，但必须给出优先级顺序 (priority order)。所有输入、输出与有效指示均为无量纲的 0/1；本篇默认高有效、稳态组合逻辑。

> [!example]- Encoder and Priority Encoder · 推导与例题
> **Derivation · 推导**
>
> 普通 one-hot 情况：$Y_1=D_2+D_3$，$Y_0=D_1+D_3$。若 D1=D2=1，会输出 11，错误地像 D3；因此 one-hot 假设不可省略。
>
> 取 D3 最高优先、高有效。先生成获胜线路：
>
> $$W_3=D_3,\ W_2=\bar D_3D_2,\ W_1=\bar D_3\bar D_2D_1,\ W_0=\bar D_3\bar D_2\bar D_1D_0.$$
> $$Y_1=D_3+D_2,\qquad Y_0=D_3+\bar D_2D_1,\qquad V=D_3+D_2+D_1+D_0.$$
>
> Notice that the output code is different from the winner mask. The W signals are one-hot; the Y signals encode the index. V specifies whether the code represents an actual request.
>
> | Inputs $D_3D_2D_1D_0$ | Code | V |
> |---|---|---|
> | 1XXX | 11 | 1 |
> | 01XX | 10 | 1 |
> | 001X | 01 | 1 |
> | 0001 | 00 | 1 |
> | 0000 | 00 by convention | 0 |
>
> X here means that a lower-priority input cannot change the result. It does not mean the physical input must be electrically unknown.
>
> **Priority Circuit Versus Priority Encoder · 优先电路与编码输出，Ch5 p.20–22**
>
> 课件输入名是 $A_3A_2A_1A_0$，输出名是 $Y_3Y_2Y_1Y_0$。它要求 “Output asserted corresponding to most significant TRUE input”，因此这四位输出是**独热获胜掩码 (one-hot winner mask)**。为避免与本篇二位编码输出 $Y_1Y_0$ 混淆，以下用 $D_i$ 对应课件 $A_i$，用 $W_i$ 对应课件 $Y_i$。
>
> | $D_3D_2D_1D_0$ | Winner mask $W_3W_2W_1W_0$ | Binary code $Y_1Y_0$ | $V$ |
> |---|---|---|---|
> | 0000 | 0000 | 00 | 0 |
> | 0001 | 0001 | 00 | 1 |
> | 0010 | 0010 | 01 | 1 |
> | 0011 | 0010 | 01 | 1 |
> | 0100 | 0100 | 10 | 1 |
> | 0101 | 0100 | 10 | 1 |
> | 0110 | 0100 | 10 | 1 |
> | 0111 | 0100 | 10 | 1 |
> | 1000 | 1000 | 11 | 1 |
> | 1001 | 1000 | 11 | 1 |
> | 1010 | 1000 | 11 | 1 |
> | 1011 | 1000 | 11 | 1 |
> | 1100 | 1000 | 11 | 1 |
> | 1101 | 1000 | 11 | 1 |
> | 1110 | 1000 | 11 | 1 |
> | 1111 | 1000 | 11 | 1 |
>
> Two invariants make the winner equations easy to verify: at most one $W_i$ is 1, and $W_3+W_2+W_1+W_0=V$. Each lower winner includes complements of every higher input, so a higher request suppresses all lower requests.
>
> 从获胜线路编码可得到前面的紧凑式：
>
> $$
> \begin{aligned}
> Y_1&=W_3+W_2=D_3+D_2,\\
> Y_0&=W_3+W_1=D_3+\bar D_2D_1.
> \end{aligned}
> $$
>
> 例如 1011 应获胜于 D3：课件输出为 1000，编码输出为 11；两者表达同一个选择结果，但格式不同。
>
> **Input X Versus Output Don't-Care · 输入压缩与输出无关项**
>
> 课件 p.22 把 16 行压缩为 $0000\to0000$、$0001\to0001$、$001X\to0010$、$01XX\to0100$、$1XXX\to1000$。输入端 X 是“任意取值仍给相同输出”，一行分别代表 1、1、2、4、8 种输入，共 16 种。
>
> Those X symbols compact an already complete truth table. The outputs remain specified for all sixteen patterns. They do not justify turning multiple-request cases into output don't-cares for K-map minimization.
>
> 另一个设计若明确声明 all-zero 时位置码不被使用，且使用者受有效指示 (valid indicator) V 控制，则该行的 **code 输出**可另行指定为无关项；这属于新规范，不能由 p.22 的输入 X 自动推断。通用规则见 [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]]。
>
> **Worked Examples · 例题**
>
> **Example 1.** D=0110，D2 与 D1 同时请求。W2=1，其余 0；code=10，V=1。输出不会是普通编码器的 11。
>
> **Example 2.** D=0001 与 D=0000 都可给 code=00，但 V 分别为 1、0。没有 V 时无法区分“请求 0”和“没有请求”。
>
> **Active-low interface.** 若外部 $\bar D_i=0$ 表示请求，先形成正逻辑 request $D_i=\overline{\bar D_i}$。如果输出也是低有效 binary code，则再取补。输入低有效与输出低有效是两个独立约定。
>
> **Eight-to-three extension.** 最高获胜输入 $W_i=D_i\prod_{j=i+1}^{7}\bar D_j$；每个 code bit OR 所有索引该位为 1 的 W。适用于中断仲裁或按键选择。
>
> **Position codes in a scanned keyboard · 扫描键盘中的位置码**
>
> An eight-row matrix uses a three-bit row encoder and an eight-column matrix uses a three-bit column encoder. Combining the fields produces a six-bit position code, with an independent valid condition. Active-low one-cold inputs require the corresponding input polarity conversion or device model.
>
> [[Keyboard Scanning and Encoding]] 把该组合块连接到扫描状态、debounce与load事件；编码器本身不能决定一次按下应产生几次字符。

### Decimal-to-BCD Encoding · 十进制位置码与反相输出，p.25–27

十进制至 BCD 编码器 (decimal-to-BCD encoder) 的输出是一个数字的四位代码，并非对多个有效输入“求和”。讲义 p.25 的普通高有效编码器，设至多一个 $D_j=1$、j=0–9，输出位权 8、4、2、1，则：

$$A_0=D_1+D_3+D_5+D_7+D_9,\qquad A_1=D_2+D_3+D_6+D_7,$$
$$A_2=D_4+D_5+D_6+D_7,\qquad A_3=D_8+D_9.$$

这些式子以独热假设为前提；如果 D1 和 D2 同时有效，普通 OR 编码会得到 `0011`，不能解释为优先选择 D2。

> [!example]- 74HC147 keyboard example · pin number、digit 与 code 分开读
> ![[ch6-priority-encoder147.png]]
> *讲义 p.27 原图：按键拉低输入；输出旁的气泡和横线标明 BCD complement。引脚号不等于十进制优先编号。*
>
> 74HC147 的图示输入 1–9 为低有效请求，较大十进制数字优先。输出是反相 BCD (BCD complement)，读结果时先找获胜数字，再分别对四个代码位取补。
>
> 原例 pin 1、4、13 同时 LOW，按图中引脚映射分别为数字 4、7、3，因此获胜数字是 **7**；按正常 8421 位序其 BCD 为 `0111`，芯片输出 $\bar A_3\bar A_2\bar A_1\bar A_0$ 为 **`1000`**。不能把输出当成正常数字 8，也不能因 pin 13 最大就选数字 13。
>
> 图中没有专门的数字 0 编码输入。全体 1–9 输入不被断言时，按此补码接口对应零代码；系统仍需独立的按键有效条件，区分“0 键”与“没有按键”。优先选择也不能代替 [[Keyboard Scanning and Encoding]] 的去抖和事件捕获。

### Eight-to-Three Priority Table · X 压缩的是低优先输入，p.28

讲义 p.28 用高有效八路输入 $D_7>\cdots>D_0$，输出 $Q_2Q_1Q_0$ 编码最高有效输入。下面 V 是笔记为解释“无请求”补充的有效指示 (valid indicator)，讲义图中只有三个代码输出。

| $D_7D_6D_5D_4D_3D_2D_1D_0$ | $Q_2Q_1Q_0$ | V |
|---|---|---|
| 1XXXXXXX | 111 | 1 |
| 01XXXXXX | 110 | 1 |
| 001XXXXX | 101 | 1 |
| 0001XXXX | 100 | 1 |
| 00001XXX | 011 | 1 |
| 000001XX | 010 | 1 |
| 0000001X | 001 | 1 |
| 00000001 | 000 | 1 |
| 00000000 | 000 by the lecture convention | 0 |

An X in the input columns means either LOW or HIGH is allowed because a higher request already wins. It is not an unassigned output row. For example, `00110100` selects D5 and returns `101`; the lower D4 and D2 do not change the code.

### Pitfalls and Review · 易错点与复习

- A decoder selects a line from a code; an encoder creates a code from a line.
- 优先级不保证公平；一直存在高优先请求时，低优先可能 starvation。
- 验证重叠请求和 all-zero 情况，不能只测试 one-hot。

**Exam answer:** “The highest asserted input suppresses all lower-priority inputs. The valid signal prevents the no-input case from being confused with input zero.”

### Connections · 概念关系与应用

依 [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]] 确定优先级和 valid；它与 [[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 的信息方向相反；输入 X 的压缩含义须与 [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]] 区分。门实现可用 [[Universal Gates and Bubble Pushing]]；[[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] 提供扫描码，[[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] 同样使用较高位优先的屏蔽结构。

## 4 · Multiplexer and Demultiplexer · 选择与分配

多路选择器 (multiplexer, MUX) 的 2:1 式为 $Y=\bar SD_0+SD_1$，是香农展开 (Shannon expansion) $F=\bar SF|_{S=0}+SF|_{S=1}$ 的硬件。解复用器 (demultiplexer, DEMUX) 把一个数据输入按选择送至一条线路，其他线路输出由有效极性规定。

实现布尔函数时，选部分变量作为选择端，逐组计算剩余变量的余因子 (cofactor)；数据端可能为 0、1、变量或其补，不能只填最终表达式的某个系数。

### Core Definition · 核心定义

2:1 MUX 的 select S 决定选 D0 或 D1：

$$Y=\bar SD_0+SD_1.$$

4:1 MUX 用两位 $S_1S_0$，$Y=D_{2S_1+S_0}$。select 是**地址/控制**，data 是被选择的值。$2^k$:1 需要 k 条 select，不能混淆 data count 与 select count。

四路选择的两级 AND–OR 模型是：

$$Y=\bar S_1\bar S_0D_0+\bar S_1S_0D_1+S_1\bar S_0D_2+S_1S_0D_3.$$

讲义 p.42 的另一实现用三个 2:1 MUX：第一级用 $S_0$ 分别选 D0/D1、D2/D3，第二级用 $S_1$ 选两个中间输出。交换选择位会重新排列地址；布尔等价的 AND–OR 与 MUX 树也有不同实际时延。若数据数 N 不是 $2^k$，通常需 $\lceil\log_2N\rceil$ 条选择位，并定义未使用选择码；讲义的 $\log_2N$ 针对完整二次幂规模。

> [!example]- Multiplexer and Demultiplexer · 推导与例题
> **Derivation · Shannon expansion**
>
> $$F(A,X)=\bar A F(0,X)+A F(1,X).$$
>
> 两种 A 的情况互斥且穷尽，所以这就是 2:1 MUX。对两个 select 重复分解，可以让 4:1 MUX 实现三变量函数，其 data inputs 分别为 0、1、剩余变量或其补。
>
> When reducing a three-variable truth table into four MUX data inputs, inspect each pair of rows for the remaining variable C. Output pair 00 gives constant 0; 11 gives constant 1; 01 gives C; 10 gives NOT C. This method prevents guessing.
>
> **Worked Examples · 例题**
>
> **XOR using a MUX.** 选 A：A=0 时 $F=B$，A=1 时 $F=\bar B$，因此 D0=B、D1=NOT B。A=1,B=0 → 1，符合 XOR。
>
> **Majority.** $F=AB+AC+BC$，select=AB。四组 cofactor 为 D0=0、D1=C、D2=C、D3=1。检查 011 → D1=C=1；100 → D2=C=0。
>
> **Parity.** $F=A\oplus B\oplus C$，select=AB，data=(C,NOT C,NOT C,C)。C=0 时 data 为 0,1,1,0；C=1 时正好反相。
>
> **Demultiplexing · 分配**
>
> 1:4 DEMUX 的单数据输入为 D，$Y_i=Dm_i(S_1,S_0)$。D=0 时所有输出 0；D=1 时相当于 decoder。选择 10 且 D=1：输出 Y2=1，其余 0。
>
> A decoder's enable can serve as the data input only when the device's enable and output polarity produce the required DEMUX function. An active-low decoder does not automatically give positive-logic DEMUX outputs.
>
> **Pitfalls and Practical Use · 误区与应用**
>
> - MUX is many-to-one; DEMUX is one-to-many.
> - 使能关闭后的输出由 device table 决定，不必然 Z。
> - Do not leave unused inputs floating; assign defined constants when implementing logic.
> - [[Tri-State Buffers and Bus Drivers]] shows a different physical way to select a bus source.
> - A counter plus a MUX can serialize a stored word, provided the word stays stable during the full scan.
>
> **Exam question:** Implement a three-variable function using a 4:1 MUX. What are the first two decisions?
>
> **Answer:** Choose and order the two select variables, then derive the four cofactors with respect to the remaining variable. State the enable condition before connecting the data inputs.

### Lecture MUX Examples · 固定表项与余因子，p.41–44

讲义 p.43 的查找表 (lookup table, LUT) 以 $(S_1,S_0)=(A,B)$ 为地址，四个数据输入为 $(0,1,0,0)$，所以唯一 ON 行是 01，$Y=\bar AB$。反相横线不可漏读；$AB$ 会把 ON 行改成 11。

> [!example]- Logic function generator · 同一函数用 8:1 与 4:1 实现
> ![[ch6-mux-function-generator.png]]
> *讲义 p.44 原图：$A_2A_1A_0$ 是按 4、2、1 排列的地址，74HC151 的低有效 EN 接逻辑 0，图示非反相 Y 输出使用常数表项。*
>
> 原表的 ON set 为 $\{1,3,5,6\}$：
>
> $$Y=\bar A_2\bar A_1A_0+\bar A_2A_1A_0+A_2\bar A_1A_0+A_2A_1\bar A_0.$$
>
> **8:1 MUX / 讲义连接：** 三个变量全部作 select，数据表项按地址 0–7 为 `(0,1,0,1,0,1,1,0)`。这时 data 是固定的真值表输出，不是另一组待计算的输入变量。
>
> **4:1 MUX / 笔记推导：** 选 $(S_1,S_0)=(A_2,A_1)$，分别比较剩余 $A_0=0,1$ 的两行：
>
> | $A_2A_1$ | $Y$ at $A_0=0$ | $Y$ at $A_0=1$ | Data cofactor |
> |---|---|---|---|
> | 00 | 0 | 1 | $D_0=A_0$ |
> | 01 | 0 | 1 | $D_1=A_0$ |
> | 10 | 0 | 1 | $D_2=A_0$ |
> | 11 | 1 | 0 | $D_3=\bar A_0$ |
>
> 例如地址 `110`：8:1 选 $D_6=1$；4:1 选 $D_3=\bar A_0=1$。地址 `111` 两者都给 0。推导结果还应检查其余六行。
>
> **Waveform check / p.41：** 从左到右八个稳定选择槽的 $S_1S_0$ 为 `00,01,10,11,00,01,10,11`；在对应输入波形上读取被选数据，得到 Y=`0,1,0,0,1,0,0,1`。沿时间对齐 select 与 data，不能把所有数据线做 OR。槽边界附近的行为另加传播延迟。

### Connections · 概念关系与应用

由 [[Boolean Forms and Algebraic Simplification#2 · Truth Table and Boolean Expression · 用真值表定义全集|Truth Table and Boolean Expression]] 求 cofactors；[[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 的 enable 可在极性合适时作 DEMUX data。[[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] 驱动最小值选择；[[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]] 用反馈 MUX 实现保持；[[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] 选择相邻位，[[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积|Read-Only Memory and Programmable Logic Arrays]] 提供查表实现的对照。

## 5 · 模块边界与测试

先规定输入编码、优先级和全部有效极性，再列完整真值表。测试重叠请求、无请求、使能关闭和相反数据；只测试 one-hot 输入会漏掉优先级错误。

## Sources · 课件依据

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 6: Combinational Building Blocks*，[本次讲义](../ECE2050-Chap6.pdf#page=19)，PDF p.19–23：XNOR equality、大小比较与 74HC85/74LS85 级联；p.25–28：十进制编码、74HC147 与八路优先表；p.29–35：译码、74HC154 扩展与 BCD-to-decimal；p.39–45：MUX、查表、逻辑函数生成与 DEMUX。PDF 页序与页脚编号一致。
- [库中原参考讲义](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。级联方程、五位译码表达式、4:1 余因子实现和数值边界测试为笔记推导；V 不是 p.28 图中自带的输出。

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.20–22：优先电路、四路独热方程、完整与压缩真值表；[本地课件](../ECE2050-Chap5.pdf#page=20)。二位编码与 V 是在四路获胜模型上展开的推导，课件该例题的输出仍为四路独热。

---
索引：[[ECE2050.1]] · [[Glossary]]
