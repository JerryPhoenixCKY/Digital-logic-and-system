---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
updated: 2026-10-08
chapter: Ch5
aliases:
  - 组合逻辑分析与设计
  - Combinational Logic Analysis and Design
  - 组合逻辑分析与设计 · Ch5
  - AND-OR and AND-OR-Invert Logic
  - 与或逻辑与与或非逻辑
  - AND-OR Logic
  - AND-OR-Invert Logic
  - AOI Logic
  - Combinational Logic Analysis
  - 组合逻辑分析
  - Logic Circuit Analysis
  - Combinational Logic Design
  - 组合逻辑设计
  - Combinational analysis and implementation
---

# Combinational Logic Analysis and Design · 组合逻辑分析与设计

> [!SUMMARY] Quick recall · 英文速览
> Analysis derives a function from a circuit; design implements a specification. Both meet at a complete truth table and independently verified equations.

## 1 · Combinational Logic Design · 需求先于门

规范明确输入事件、有效极性、变量顺序、输出条件和无效输入。先建立完整真值表，再写 SOP／POS、化简、选择硬件，最后比较所有指定输入。稳态变量均为无量纲 0/1。

> [!example]- Combinational Logic Design · 推导与例题
> **Derivation · 规范到方程**
>
> | Step | Deliverable | Why it matters |
> |---|---|---|
> | Define inputs | Meaning and active polarity | Distinguishes LOW voltage from FALSE event |
> | Enumerate cases | Truth table | Prevents missing conditions |
> | Choose ON/OFF sets | SOP or POS | Makes minimization reproducible |
> | Minimize | K-map with marked groups | Preserves all specified rows |
> | Implement | Gates, decoder, MUX or ROM | Fits available hardware |
> | Verify | Compare every defined input row | Detects polarity and indexing mistakes |
>
> **Expression and Truth Table to Circuit · 课件 p.16**
>
> 布尔表达式 (Boolean expression) $X=AB+CDE$ 直接对应二输入 AND、三输入 AND 和末级 OR。反变量必须由可用的互补输入或反相器提供。[[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构|AND-OR and AND-OR-Invert Logic]] 比较与或和与或非结构。
>
> 课件另一张真值表只有 $ABC=011,100$ 输出 1，变量顺序明确为 ABC。因此：
>
> $$
> X=\sum m(3,4)=\bar ABC+A\bar B\bar C.
> $$
>
> Each row contributes one complete minterm. The two ON rows differ in three bits, so they cannot be combined into one K-map group. The unlisted rows are zeros, not don't-cares.

## 2 · AND-OR and AND-OR-Invert Logic · 形式落到结构

AND-OR 计算 $AB+CD$；AOI 计算 $\overline{AB+CD}=(\bar A+\bar B)(\bar C+\bar D)$。AND→OR 的两级描述不限制门数，也通常不计输入反相器；实际门数与延迟由器件输入数、反变量是否可用决定。

> [!example]- AND-OR and AND-OR-Invert Logic · 推导与例题
> **图示与讲义依据**
>
> ![[and-or-aoi-logic.svg]]
> *图 1 — 相同输入下，(a) 输出 $AB+CD$；(b) 输出其补 $\overline{AB+CD}$。输入与输出均明确标注，气泡表示最终反相。*
>
> **Logic Levels and Gate Count · 逻辑级数与门数**
>
> **两级逻辑 (two-level logic)** 指主要组合结构的 AND→OR 或 OR→AND 两级，通常不计产生反变量的输入反相器 (input inverters)。它不限制第一层只能有两个门，也不限制每个门只能有两个输入。
>
> AOI can be implemented by AND gates followed by a NOR gate. If OR and NOT are physically separate gates, that realization has an additional output stage. A Boolean form alone does not specify the physical propagation delay or packaged gate count.
>
> 课件 p.6 的图按 AND→OR→Invert 连接；同页 “ORs followed by ANDs” 对应德摩根变换后的等价 POS 形式 $(\bar A+\bar B)(\bar C+\bar D)$。读图时应先看横线覆盖范围，不能把 $\overline{AB+CD}$ 写成 $\overline{AB}+\overline{CD}$。
>
> **Worked Example 1 · 课件 p.4 的 SOP**
>
> 变量顺序取 $ABC$，课件三个乘积项是：
>
> $$
> Y=\bar A\bar B\bar C+A\bar B\bar C+A\bar BC
> =\sum m(0,4,5).
> $$
>
> The term $\bar A\bar B\bar C$ selects 000; $A\bar B\bar C$ selects 100; $A\bar BC$ selects 101. A shared literal or a shared input inverter does not make the terms electrically connected at their outputs: the OR gate combines them.
>
> 可进一步化简为：
>
> $$
> Y=\bar B\bar C(\bar A+A)+A\bar BC
> =\bar B(\bar C+AC)
> =\bar B(\bar C+A).
> $$
>
> 最后一步用吸收规则 (absorption rule) $X+\bar XZ=X+Z$。代入 000、100、101 得 1，001、111 得 0；完整 ON set 仍是 $\{0,4,5\}$。化简方法见 [[Boolean Forms and Algebraic Simplification#4 · Boolean Expression Simplification · 保持函数再比较代价|Boolean Expression Simplification]]。

## 3 · 先处理极性：储罐报警

三个传感器高电平表示过低，至少两个过低的高有效报警为 $H=AB+AC+BC$，包含 111。若 LOW 表示过低，报警为 $L=\bar A\bar B+\bar A\bar C+\bar B\bar C=\overline{AB+AC+BC}$。报警器低有效时再对 L 取补。

> [!example]- AND-OR and AND-OR-Invert Logic · 推导与例题
> **Worked Example 2 · 高有效液位传感器，课件 p.5**
>
> 三个储罐的原始传感器电平为 $A,B,C$。**高有效 (active-high)** 表示输入为 1 时液位过低；报警输出 $H=1$ 表示至少两个储罐过低。
>
> $$
> H=AB+AC+BC=\sum m(3,5,6,7).
> $$
>
> This is the three-input majority function. “Any two” in this circuit includes the all-three case. The OR gate reports whether a pair exists; it does not count pairs.
>
> | $ABC$ | 过低储罐数 | $H$ |
> |---|---|---|
> | 000 | 0 | 0 |
> | 001 | 1 | 0 |
> | 010 | 1 | 0 |
> | 011 | 2 | 1 |
> | 100 | 1 | 0 |
> | 101 | 2 | 1 |
> | 110 | 2 | 1 |
> | 111 | 3 | 1 |
>
> 若要求“恰好两个 (exactly two)”，必须排除 111，输出应为 $\bar ABC+A\bar BC+AB\bar C$，不能继续用 $AB+AC+BC$。
>
> **Worked Example 3 · 低有效传感器与 AOI，课件 p.7**
>
> **低有效 (active-low)** 表示原始电平 $A=0$ 时储罐 A 过低；B、C 同理。高有效报警的事件方程为：
>
> $$
> L=\bar A\bar B+\bar A\bar C+\bar B\bar C.
> $$
>
> 课件用没有输入反相器的 AOI 结构实现它：
>
> $$
> \begin{aligned}
> L&=\overline{AB+AC+BC}\\
>  &=(\bar A+\bar B)(\bar A+\bar C)(\bar B+\bar C)\\
>  &=\bar A\bar B+\bar A\bar C+\bar B\bar C.
> \end{aligned}
> $$
>
> The complement of “at least two raw inputs are HIGH” is “at least two raw inputs are LOW” for exactly three Boolean inputs. This identity explains the output inverter in the source circuit; the sensor polarity by itself does not determine the alarm polarity.
>
> | $ABC$ | 过低储罐数，即 0 的个数 | $AB+AC+BC$ | $L$ |
> |---|---|---|---|
> | 000 | 3 | 0 | 1 |
> | 001 | 2 | 0 | 1 |
> | 010 | 2 | 0 | 1 |
> | 011 | 1 | 1 | 0 |
> | 100 | 2 | 0 | 1 |
> | 101 | 1 | 1 | 0 |
> | 110 | 1 | 1 | 0 |
> | 111 | 0 | 1 | 0 |
>
> 如报警器本身低有效，应输出 $\bar L=AB+AC+BC$。区分“发生低液位事件”和“对应电压是 LOW”可以避免重复反相。

> [!example]- Combinational Logic Design · 推导与例题
> **Worked Example 1 · 储罐报警**
>
> 三个传感器 $A,B,C=1$ 表示液位过低；任意至少两个过低则报警。满足条件的 minterms 为 $m_3,m_5,m_6,m_7$，变量顺序 ABC。
>
> $$Y=\bar ABC+A\bar BC+AB\bar C+ABC=AB+AC+BC.$$
>
> The three products cover the three possible pairs. Their overlap at 111 is allowed: OR does not count how many terms are TRUE. Check 110 → 1, 100 → 0, and 111 → 1.
>
> 若传感器 LOW 表示过低，先定义事件 $a=\bar A,b=\bar B,c=\bar C$；高有效报警为 $Y=\bar A\bar B+\bar A\bar C+\bar B\bar C$。若报警也低有效，再取补；不能只因为输入低有效就自动反相输出。
>
> 课件 p.5、p.7 的两种极性、完整真值表及 $\overline{AB+AC+BC}$ 的 AOI 实现见 [[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构|AND-OR and AND-OR-Invert Logic]]。

## 4 · 精确处理量词：四个输入中恰好三个为 1

变量顺序 ABCD，$i=8A+4B+2C+D$：

$$X=\bar ABCD+A\bar BCD+AB\bar CD+ABC\bar D=\sum m(7,11,13,14).$$

1111 与 0001 均输出 0。四个 ON 格互不相邻，所以最小两级 SOP 仍有四项。at least three 包含 1111；四输入 XOR 还包含恰好一个 1，这两个函数都不符合本题。

> [!example]- Combinational Logic Design · 推导与例题
> **Worked Example 2 · 恰好四个输入中的三个为 1，课件 p.17**
>
> 输入顺序为 $ABCD$，A 为最高有效位 (most significant bit, MSB)，行编号 $i=8A+4B+2C+D$。输出 $X=1$ 当且仅当四个同时给出的输入里恰好有三个 1：
>
> $$
> X=\bar ABCD+A\bar BCD+AB\bar CD+ABC\bar D
> =\sum m(7,11,13,14).
> $$
>
> | $i$ | $ABCD$ | 1 的个数 | $X$ |
> |---|---|---|---|
> | 0 | 0000 | 0 | 0 |
> | 1 | 0001 | 1 | 0 |
> | 2 | 0010 | 1 | 0 |
> | 3 | 0011 | 2 | 0 |
> | 4 | 0100 | 1 | 0 |
> | 5 | 0101 | 2 | 0 |
> | 6 | 0110 | 2 | 0 |
> | 7 | 0111 | 3 | 1 |
> | 8 | 1000 | 1 | 0 |
> | 9 | 1001 | 2 | 0 |
> | 10 | 1010 | 2 | 0 |
> | 11 | 1011 | 3 | 1 |
> | 12 | 1100 | 2 | 0 |
> | 13 | 1101 | 3 | 1 |
> | 14 | 1110 | 3 | 1 |
> | 15 | 1111 | 4 | 0 |
>
> Any two ON patterns differ in two positions, so none are adjacent in a K-map. Every single-bit neighbor contains either two or four 1s and must output 0. With no don't-cares, all four four-literal terms are necessary in the minimum two-level SOP.
>
> 允许四输入门时，用四个四输入 AND 接一个四输入 OR；若互补输入未提供，另计四个 NOT。二级是主 AND-OR 结构的级数，不是总门数；只有二输入门时需分解多输入门。
>
> **不要替换为 XOR。** $A\oplus B\oplus C\oplus D$ 在恰好一个或三个输入为 1 时都输出 1；例如 0001 应有 $X=0$，但 XOR 为 1。“至少三个”则包含 1111，函数为 $ABC+ABD+ACD+BCD$，也与本题不同。
>
> **Sanity check:** four of sixteen rows assert the output, matching $\binom{4}{3}=4$. Testing 0111, 1111, and 0001 distinguishes exactly-three, at-least-three, and odd-parity specifications.

## 5 · Combinational Logic Analysis · 从连接恢复函数

逐节点命名，按门写方程，再向输出代入。课件 p.18：$n=\overline{\bar A\bar B\bar C}=A+B+C$，$X=nC+n+D=n+D=A+B+C+D$，关键是直通分支对 nC 的吸收。

课件 p.19：
$$X=A\bar B\bar C+AB\bar C\bar D+\bar A\bar B\bar CD+\bar A\bar B\bar C\bar D=\bar B\bar C+A\bar C\bar D.$$
原始 ON set 为 $\{0,1,8,9,12\}$；最大四格组与必要两格组可重叠。完整步骤和图示在下方对应推导中。

> [!example]- Combinational Logic Analysis · 推导与例题
> **Scope and Model · 范围与模型**
>
> **组合逻辑分析 (combinational logic analysis)** 从已有连接求输出函数；[[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|组合逻辑设计 (combinational logic design)]] 从规范选择连接。本篇集中讲课件 p.18–19 的电路化简，前置是 [[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|Combinational Circuit]] 的无反馈、单驱动构成规则。
>
> 所有输入、内部节点 (internal nodes) 与输出均为无量纲的 0/1。$+$ 是 OR，相乘是 AND，上横线是 NOT。分析假设输入电平有效、电路传播已稳定；稳态等价不保证相同的转换波形或延迟。
>
> **Read the Circuit · 电路到方程**
>
> 1. 确定主输入 (primary inputs)、主输出 (primary outputs) 和变量顺序，给内部节点命名为 $n_1,n_2,\ldots$。
> 2. 沿信号方向逐级写方程；先写 gate function，再代入该门的输入。
> 3. 单独记录每个反相气泡 (inversion bubble)；横线必须覆盖正确的变量或整个子式。
> 4. 同一节点的所有分支使用同一个值。实心圆点表示连接；无连接标记的交叉不能自行当成分叉。
> 5. 将内部节点逐层代入输出，再用 [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则|Laws and Rules of Boolean Algebra]] 或 [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并|Karnaugh Map]] 化简。
> 6. 按相同变量顺序穷举全部 $2^n$ 行，比较原始节点模型与最终表达式。
>
> Keep the original equations as an independent reference. Deriving a truth table only from the simplified answer would not reveal a transcription error in the original circuit.
>
> **Worked Example 1 · 重复支路被吸收，课件 p.18**
>
> 主输入为 $A,B,C,D$，输出为 $X$。A、B、C 先各反相，再经过三输入 AND 和一个 NOT。令这段输出为 $n$：
>
> $$
> n=\overline{\bar A\bar B\bar C}=A+B+C.
> $$
>
> $n$ 一路直接送末级 OR，另一路与原始输入 $C$ 相与。D 直接送末级 OR，因此：
>
> $$
> \begin{aligned}
> X&=nC+n+D\\
>  &=n+D &&\text{absorption: }n+nC=n\\
>  &=A+B+C+D.
> \end{aligned}
> $$
>
> The direct branch $n$ already covers every case covered by $nC$. Removing that AND branch preserves the steady-state function. With a four-input OR available, the entire network reduces to one OR gate; with only two-input gates, a four-input OR requires a small tree.
>
> | $ABCD$ | $n$ | $nC$ | Original $nC+n+D$ | Reduced $A+B+C+D$ |
> |---|---|---|---|---|
> | 0000 | 0 | 0 | 0 | 0 |
> | 0001 | 0 | 0 | 1 | 1 |
> | 0010 | 1 | 1 | 1 | 1 |
> | 1000 | 1 | 0 | 1 | 1 |
> | 1111 | 1 | 1 | 1 | 1 |
>
> 完整真值表只有 0000 一行输出为 0。这里先应用德摩根定理 (DeMorgan's theorem)，再应用吸收律；不能把 $\overline{\bar A\bar B\bar C}$ 误读为 $\bar A\bar B\bar C$。
>
> **Worked Example 2 · 四乘积项化为两项，课件 p.19**
>
> 原电路是四个 AND 输出送同一个 OR；变量顺序为 $ABCD$。从原图读到：
>
> $$
> X=A\bar B\bar C+AB\bar C\bar D
> +\bar A\bar B\bar CD+\bar A\bar B\bar C\bar D.
> $$
>
> 先合并只差 $D$ 的最后两项，再提取 $\bar C$：
>
> $$
> \begin{aligned}
> X&=A\bar B\bar C+AB\bar C\bar D
> +\bar A\bar B\bar C(D+\bar D)\\
>  &=\bar C\,[A\bar B+AB\bar D+\bar A\bar B]\\
>  &=\bar C\,[\bar B(A+\bar A)+AB\bar D]\\
>  &=\bar C\,[\bar B+AB\bar D]\\
>  &=\bar C\,(\bar B+A\bar D)\\
>  &=\boxed{\bar B\bar C+A\bar C\bar D}.
> \end{aligned}
> $$
>
> 倒数第二步用 $U+\bar UV=U+V$，其中 $U=\bar B$、$V=A\bar D$。这一步删除了第二项中的 $B$，但没有删除公共因子 $\bar C$。
>
> **K-map Cross-check · 卡诺图复核**
>
> $$
> X=\sum m(0,1,8,9,12),\qquad i=8A+4B+2C+D.
> $$
>
> | $AB\backslash CD$ | 00 | 01 | 11 | 10 |
> |---|---|---|---|---|
> | 00 | 1 | 1 | 0 | 0 |
> | 01 | 0 | 0 | 0 | 0 |
> | 11 | 1 | 0 | 0 | 0 |
> | 10 | 1 | 1 | 0 | 0 |
>
> The four-cell group $\{0,1,8,9\}$ wraps across the top and bottom edges and gives $\bar B\bar C$. The two-cell group $\{8,12\}$ gives $A\bar C\bar D$. Cell 8 belongs to both groups, which is allowed.
>
> ![[combinational-reduction-kmap.svg]]
> *图 1 — 课件 p.19 的四格组和两格组；虚线提示上下边相邻，$m_8$ 被重叠覆盖。蓝色组消去 A、D，红色组消去 B。*
>
> Each group is necessary: $m_0$ needs the first implicant and $m_{12}$ needs the second. No eight-cell group is possible because it would include specified zeros. Thus these are the two essential prime implicants for the minimum SOP.
>
> **代入检查。** 0001 由 $\bar B\bar C$ 覆盖；1100 由 $A\bar C\bar D$ 覆盖；1101 两项都为 0；任意 $C=1$ 都为 0。精简电路是一个二输入 AND、一个三输入 AND 与一个 OR；若反变量未直接提供，还需产生 $\bar B,\bar C,\bar D$。
>
> **Bubble Pushing as Analysis · 用气泡推移读混合门**
>
> [[Universal Gates and Bubble Pushing#4 · 三级门链：从输出向输入化简|三级门链例题]] 从 NOR→NAND→NAND 得到：
>
> $$
> n_1=\overline{A+B},\qquad n_2=\overline{n_1C},\qquad
> Y=\overline{n_2D}=\bar A\bar BC+\bar D.
> $$
>
> Writing node equations and redrawing equivalent gate symbols are two checks on the same function. Begin at the output when pushing bubbles; begin at the inputs when evaluating the original node equations.
>
> **Limits and Common Errors · 边界与误区**
>
> - **横线范围错 (wrong complement scope)**：$\overline{PQ}+R$ 与 $\overline{PQ+R}$ 是不同函数。
> - **丢掉共享节点 (lost fan-out)**：某节点直通输出的支路可能使另一支路被吸收，p.18 就是例子。
> - **K-map 不跨边 (missed wrap-around)**：p.19 的四格组需要首尾行相邻。
> - **把最小 SOP 当成唯一最优硬件**：门输入数、反相器、共享逻辑和延迟会影响实现代价。
> - **把逻辑等价当成波形等价**：简化可能改变 [[Propagation Delay and Logic Hazards|延迟与逻辑冒险 (logic hazards)]]；采样电路还需满足 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]]。

## 6 · 更一般的分类与匹配

同时给出的 ABCD 检测连续 110：$Y=AB\bar C+BC\bar D$，ON set 为 $\{6,12,13,14\}$。跨时钟的串行匹配需要状态，见 [[Finite State Machine Design and Applications]]。五位分类分别枚举 prime、square 和 divisible 条件；0 是平方数和 15 的倍数，却不是素数。

> [!example]- Combinational Logic Design · 推导与例题
> **Worked Example 3 · 同时四位中的模式**
>
> 四个同时给出的输入按 ABCD 从左至右排列。要求出现连续 110，则可出现在 ABC 或 BCD：
>
> $$Y=AB\bar C+BC\bar D=B(A\bar C+C\bar D)=B(A+C)(\bar C+\bar D).$$
>
> 最后一步用 $XY+\bar XZ=(X+Z)(\bar X+Y)$ 的适当变量替换；也可枚举核对。ON set 是 $\{6,12,13,14\}$，因为 0110、1100、1101、1110 满足条件。1011 没有 110，输出 0。
>
> This is a combinational pattern detector. A serial 110 detector must remember previous symbols and belongs to [[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀|Sequence Detector]]. The physical input format decides whether memory is necessary.
>
> **Worked Example 4 · 五位分类**
>
> 5-bit unsigned input $B_4\ldots B_0$ 表示 0–31。prime 输出的 ON set 是 $\{2,3,5,7,11,13,17,19,23,29,31\}$；square 是 $\{0,1,4,9,16,25\}$；被 3 与 5 同时整除是 $\{0,15,30\}$。0 不是 prime，但 $0=0^2=15\times0$。
>
> Write each output as the sum of its minterms, then minimize separately. Do not redefine a mathematical condition because a familiar example omitted zero.

## 7 · 验证、实现与易错重点

> [!IMPORTANT] 原始模型必须独立保留
> 先按原连线求内部节点，再与简化式比较；只拿最终式生成真值表，会漏掉抄图错误。规范等价、门数减少和时序正确应分别检查。

NAND／NOR 实现见 [[Universal Gates and Bubble Pushing]]；优先掩码与二进制位置码见 [[Comparison Decoding and Selection]]；检错见 [[Digital Logic Troubleshooting]]。课件十道判断题放入下方复习练习。

> [!example]- AND-OR and AND-OR-Invert Logic · 推导与例题
> **XOR and XNOR · 异或与同或的边界**
>
> 课件 p.8–9 的**异或 (Exclusive-OR, XOR)** 与**同或 (Exclusive-NOR, XNOR)** 是另外两种常用组合函数，完整符号与推导分别在 [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]]、[[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-NOR Gate]]。
>
> $$
> A\oplus B=A\bar B+\bar AB,
> \qquad
> \overline{A\oplus B}=AB+\bar A\bar B=(\bar A+B)(A+\bar B).
> $$
>
> For two inputs, XOR detects inequality and XNOR detects equality. For a reduction over several inputs, XOR reports an odd number of 1s. An even-parity **generator** uses that XOR result as its added bit; see [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]].

> [!example]- Combinational Logic Design · 推导与例题
> **Priority and Don't-Cares · 优先级与无关项，课件 p.20–22**
>
> 优先电路 (priority circuit) 在多个请求同时有效时，只断言最高优先级的获胜线路。课件输出 $Y_3Y_2Y_1Y_0$ 是独热获胜掩码 (one-hot winner mask)，并不是二进制位置码。完整推导和两种输出的对照见 [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码|Encoder and Priority Encoder]]。
>
> In the compact table, a lower-priority input marked X means either 0 or 1 produces the same specified output. It does not permit arbitrary outputs for multiple requests and does not describe an electrically floating input. Distinguish this table compression from an unspecified output used in [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]].
>
> **Chapter Quiz · 课件 p.33 判断题复习**
>
> | Topic · 判断要点 | T/F | Reason · 理由 |
> |---|---|---|
> | AND-OR 仅能由两个二输入 AND 构成 | F | 乘积项数和各项输入数不受此限制 |
> | AOI 展开为 AND-OR-Invert | T | 最终结果为 SOP 的补 |
> | 相同的两个 XOR 输入得到 LOW | T | $0\oplus0=1\oplus1=0$ |
> | 不同的两个 XNOR 输入得到 HIGH | F | 不同时 XNOR 为 0 |
> | XOR 不能构成奇偶校验发生器 | F | 偶校验位等于数据位的 XOR |
> | NAND 可以实现 AND | T | NAND 的结果再用 tied-input NAND 反相 |
> | NOR 无法实现 OR | F | NOR 的结果再反相即 OR |
> | 任意 SOP 均能仅用 NAND 实现 | T | NAND-NAND，加必要的同类输入反相器 |
> | NAND 的对偶画法是 negative-AND | F | 应为 negative-OR；negative-AND 对应 NOR |
> | Negative-OR 与 NAND 等价 | T | $\bar A+\bar B=\overline{AB}$ |

## Sources · 课件依据

主线课件：[Ch5 lecture](../ECE2050-Chap5.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.4–9：AND-OR、AOI、液位监测、XOR/XNOR；[本地课件](../ECE2050-Chap5.pdf#page=4)。两种极性的完整真值表与代数化简为根据原图展开的推导。

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.18–19：Example 2 / Example 3；p.30–31：三级气泡推移；[本地课件](../ECE2050-Chap5.pdf#page=18)。内部节点命名、逐步代数解释与边界分析为根据原图补充的推导。

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.5、7、16–22、33；[本地课件](../ECE2050-Chap5.pdf#page=16)。完整真值表、最小 SOP 的理由与判断题解释为独立推导。四位模式与五位分类例题保留为既有补充练习。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
