---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
updated: 2026-10-08
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
---

# Comparison Decoding and Selection · 比较译码与选择电路

> [!SUMMARY] Quick recall · 英文速览
> Compare values, decode codes into lines, select one winning request, then route data. Codes, winner masks, and active polarity are different interfaces.

## 1 · Magnitude Comparator · 最高不同位决定大小

数值比较器 (magnitude comparator) 对声明为 unsigned 的字从最高位向下比较。相等信号 $E=\prod_i\overline{A_i\oplus B_i}$；较大条件是在某位 $A_i\bar B_i$ 成立且更高位全相等。signed 比较先考虑符号，不能直接沿用无符号位权。

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

## 2 · Decoder · 代码变线路

n-to-$2^n$ 译码器 (decoder) 为每种输入生成一个最小项。高有效输出 OR ON 行；低有效输出需按德摩根选择末级门。使能 (enable) 决定输出是否参与，扩展时高地址位选择芯片，低地址位送各片。

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
> **Enable and Pin Constraints · 使能与引脚条件**
>
> Enable inputs can have mixed polarity. A device requiring one HIGH and two LOW enables must receive that exact combination. Translate a named chip's table into an enable predicate first; do not assume every enable pin is active-HIGH.
>
> 例如 74HC154 教学模型的两个外部使能为低有效：两者都 LOW 才选一路低输出。内部可能用一个正逻辑 E 表示“已使能”，这个 E 与外部引脚不是同一极性的信号。器件接线若依赖具体 pin number，应核对该器件资料。

## 3 · Encoder and Priority Encoder · 线路变代码

普通编码器假设至多一条请求有效。优先编码器选最高优先请求，四路输入 $D_3>D_2>D_1>D_0$ 的获胜掩码：

$$W_3=D_3,\ W_2=\bar D_3D_2,\ W_1=\bar D_3\bar D_2D_1,\ W_0=\bar D_3\bar D_2\bar D_1D_0.$$

二位位置码为 $Y_1=D_3+D_2,Y_0=D_3+\bar D_2D_1$，有效指示 $V=\sum_iD_i$。输入 0110 给掩码 0100、代码 10；0000 和 0001 的代码都可为 00，必须用 V 区分。

> [!IMPORTANT] X 的含义
> 1XXX 表示低优先输入任意变化仍给同一获胜输出；所有输入组合的输出仍已指定，不是可随便化简的输出无关项。

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

## 4 · Multiplexer and Demultiplexer · 选择与分配

2:1 MUX 为 $Y=\bar SD_0+SD_1$，是香农展开 (Shannon expansion) $F=\bar SF|_{S=0}+SF|_{S=1}$ 的硬件。DEMUX 把一个数据输入按选择送至一条线路，其他线路输出由有效极性规定。

实现布尔函数时，选部分变量作为选择端，逐组计算剩余变量的余因子 (cofactor)；数据端可能为 0、1、变量或其补，不能只填最终表达式的某个系数。

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

## 5 · 模块边界与测试

先规定输入编码、优先级和全部有效极性，再列完整真值表。测试重叠请求、无请求、使能关闭和相反数据；只测试 one-hot 输入会漏掉优先级错误。

## Sources · 课件依据

主线课件：[Ch6 lecture](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.20–22：优先电路、四路独热方程、完整与压缩真值表；[本地课件](../ECE2050-Chap5.pdf#page=20)。二位编码与 V 是在四路获胜模型上展开的推导，课件该例题的输出仍为四路独热。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
