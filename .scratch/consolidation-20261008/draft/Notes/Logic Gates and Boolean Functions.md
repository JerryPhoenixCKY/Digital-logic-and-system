---
tags:
  - ECE2050
  - logic-gates
date: 2026-09-16
updated: 2026-10-08
chapter: Ch3
aliases:
  - 逻辑门与布尔函数
  - Logic Gates and Boolean Functions
  - 逻辑门与布尔函数 · Ch3
  - Logic Gates
  - 逻辑门
  - 门电路
  - Logic Gate
  - Inverter
  - 反相器
  - 非门
  - 反相器与缓冲器
  - NOT Gate
  - Buffer
  - AND Gate
  - 与门
  - AND 门
  - AND Operation
  - OR Gate
  - 或门
  - OR 门
  - OR Operation
  - NAND Gate
  - 与非门
  - NAND 门
  - NAND Operation
  - NOR Gate
  - 或非门
  - NOR 门
  - NOR Operation
  - Exclusive-OR Gate
  - 异或门
  - XOR 门
  - 异或
  - XOR Gate
  - Exclusive-NOR Gate
  - 同或门
  - XNOR 门
  - 同或
  - XNOR Gate
---

# Logic Gates and Boolean Functions · 逻辑门与布尔函数

> [!SUMMARY] Quick recall · 英文速览
> A logic gate maps input bits to an output bit. Start with the truth table, then connect the algebraic expression, symbol, and waveform.

## 1 · Logic Gates · 统一的布尔模型

逻辑门 (logic gates) 在稳态下实现布尔函数，n 个输入需 $2^n$ 行真值表。所有逻辑量无量纲；$+$ 是 OR，相乘是 AND，横线是 NOT，$\oplus$ 是 XOR。物理电压的有效条件见 [[Logic Levels and Noise Margins]]。

> [!example]- Logic Gates · 推导与例题
> **图示与讲义依据**
>
> ![[logic-gate-symbols.svg]]
> *图 1 — 八种基本门的标准符号 (distinctive shape) 与表达式，一行一个：NOT / BUF 是单输入，
> 其余六个都是两输入。注意气泡只出现在 NOT / NAND / NOR / XNOR 上——有气泡就一定取反，
> 表达式的横线长度也正好覆盖气泡所"管辖"的那部分运算。*
>
> ![[ch3-two-input-gates.png]]
> *图 2 — 讲义 p.12 原图：两输入门总表（AND / OR / NAND / NOR / XOR / XNOR 的符号、表达式与 4 行真值表）。
> 这是本章最该背下来的一张表：六个门的输入列完全一样，差别只在输出列。*
>
> **Derivation · 推导过程**
>
> **① 为什么 $n$ 个输入正好有 $2^n$ 种组合**
>
> 每个输入 2 种取值，$n$ 个输入互相独立，按乘法原理把各自的选择数相乘：
>
> $$N_{\text{rows}}=\underbrace{2\times2\times\cdots\times2}_{n\ \text{个}}=2^{n}$$
>
> - 意义：真值表的**行数只由输入个数决定，与是哪种门无关**；行号就是输入组合的二进制值。
> - 数值校验（逐条对回讲义）：$n=1\Rightarrow2^1=2$ 行——p.4 / p.5 的 NOT 表正好 2 行；
>   $n=2\Rightarrow2^2=4$ 行——p.12 的每个门 4 行；$n=3\Rightarrow2^3=8$ 行——p.13 的 AND3 与 XOR3 各 8 行；
>   继续推算 $n=4\Rightarrow16$ 行、$n=8\Rightarrow256$ 行 ✓。
>
> **② 三种描述方式其实是一件事**
>
> - **真值表 → 表达式**：把输出为 1 的每一行写成一个乘积项（该行取 1 的变量写原变量、取 0 的写反变量），
>   再把各项相加，得到 SOP（Ch4 [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]]）。
>   例（讲义 p.12 的 XOR 列）：输出为 1 的行是 $01$ 与 $10$，于是 $Y=\bar AB+A\bar B$。
> - **真值表 → 时序图**：时序图就是"把真值表沿时间轴摊开"。任一时刻读出 $(A,B)$，
>   拿这个组合去查真值表的对应行，就是该时刻的 $Y$（[[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算|AND Gate]] / [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算|OR Gate]] 两篇的时序图就是按这个规则画的）。
>   校验：$t=15$ ns 处若 $A=1,B=0$，查 AND 表第 3 行 $(10)$ 得 $Y=0$ ✓；
>   $t=30$ ns 处若 $A=1,B=1$，查第 4 行 $(11)$ 得 $Y=1$ ✓。
> - **表达式 → 真值表**：把 4 行输入逐个代入表达式求值即可（这就是 Ch4 完全归纳法的算法）。
>
> **③ 表的行按二进制顺序列出（讲义 p.13）**
>
> 两输入按 $00,01,10,11$；三输入按 $000,001,010,011,100,101,110,111$——即从全 0 数到全 1。
>
> - 意义：这样**不漏行、不重复**，而且行号 = 输入组合的整数值，查表时可以直接"数"出来。
> - 数值校验：两输入 4 行正好是 $0,1,2,3$；三输入 8 行正好是 $0\sim7$，第一行全 0、最后一行全 1 ✓。
>   讲义 p.13 底部那句话就是这个规则：*Truth table rows are listed in binary order.*
>
> **④ 气泡与"怎么验证"（讲义 p.8–9 的 How to verify/prove?）**
>
> NAND / NOR 的符号是"母门 + 输出气泡"。要证明 $Y=\overline{AB}$ 真的等于"先 AND 再取反"，
> 最直接的办法是**穷举真值表**（perfect induction，Ch4 [[Boolean Algebra and Circuit Models#5 · Proof by Perfect Induction · 穷举与代数验证|Proof by Perfect Induction]]）：
>
> | $A$ | $B$ | $AB$ | $\overline{AB}$ | $\bar A+\bar B$ |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 1 | 1 |
> | 0 | 1 | 0 | 1 | 1 |
> | 1 | 0 | 0 | 1 | 1 |
> | 1 | 1 | 1 | 0 | 0 |
>
> 逐行比对第 4、5 列 → 完全相同，所以 $\overline{AB}=\bar A+\bar B$。这正是 DeMorgan 定理
> （Ch4 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]）在门级的样子，也是"气泡可以从输出端搬到输入端"的原因。
>
> **Worked Example · 例题**
>
> **Example 1 — 同一组输入读出六个门（讲义 p.12 总表逐行核对）**
>
> 题目：$A,B$ 按二进制顺序取 $00,01,10,11$，写出 AND、OR、NAND、NOR、XOR、XNOR 六列输出。
> 已知六个门的输入列相同，只是"输出为 1 的条件"不同。
>
> 解：逐行按条件判——AND 要全 1；OR 要有 1；NAND 是 AND 取反；NOR 是 OR 取反；
> XOR 要两个输入不同；XNOR 要两个输入相同。
>
> | $A$ | $B$ | AND $AB$ | OR $A+B$ | NAND $\overline{AB}$ | NOR $\overline{A+B}$ | XOR $A\oplus B$ | XNOR $\overline{A\oplus B}$ |
> |---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
> | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
> | 1 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
> | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
>
> **数值校验 (Numerical check)**：六个门正好是 AND/NAND、OR/NOR、XOR/XNOR 三对互补门，
> 所以**每一行都有且仅有 3 个 1**（$00$ 行是 NAND、NOR、XNOR；$01$ 行是 OR、NAND、XOR；
> $10$ 行同 $01$；$11$ 行是 AND、OR、XNOR）✓；
> 按列数 1 的个数：$1,3,3,1,2,2$，与流程图的分支行数完全吻合 ✓。
>
> **Example 2 — 行数 $2^n$（讲义 p.13 的 AND3 与 XOR3）**
>
> 题目：讲义 p.13 给出 AND3 ($Y=ABC$) 与 XOR3（odd parity：奇数个 1 时输出 1）两张表。
> 它们各有几行？若把输入换成 5 个呢？
>
> 解：$n=3\Rightarrow2^3=8$ 行；$n=5\Rightarrow2^5=32$ 行。行数与门的种类无关。
>
> **数值校验 (Numerical check)**：讲义 p.13 两张表都是 8 行、行序为 $000\to111$ ✓；
> AND3 的 8 行里只有 $111\to1$（1 行 = $2^0$）✓；
> XOR3 的 8 行里是 $001,010,100,111$ 四行为 1，$4=2^{3-1}$ ✓；
> 而 $n=5$ 时 $2^5=32=8\times4$，正好是 $n=3$ 的四倍 ✓。
>
> ![[ch3-multiple-input-gates.png]]
> *图 3 — 讲义 p.13 原图：多输入门（AND3 与 XOR3）。注意它的行序就是从 $000$ 数到 $111$，
> AND3 只有 1 行是 1、XOR3 有 4 行是 1——"数 1 的行数"是认门的最快办法。*
>
> **Example 3 — 从真值表反推门（自算）**
>
> 题目：某门的 4 行输出依次为 `1,0,0,1`（输入按 $00,01,10,11$），它是什么门？
>
> 解：输出为 1 的行是 $00$ 与 $11$，共 2 行 $=2^{2-1}$，所以是 XOR / XNOR 之一；
> 再看规律：两行都是"输入相同"（$00$ 相同、$11$ 相同）→ 是 **XNOR**（相等检测器）。
>
> **数值校验 (Numerical check)**：XNOR 的表达式 $Y=\overline{A\oplus B}$：
> $A\oplus B$ 在 $00$、$11$ 两行为 0，取反得 1；在 $01$、$10$ 两行为 1，取反得 0 →
> 输出列 `1,0,0,1` 与题目完全一致 ✓。
>
> **Gates as functions and interfaces · 门的功能与接口**
>
> A gate symbol answers a Boolean question, but a working connection must also satisfy electrical and timing requirements. Truth-table equivalence means that two implementations settle to the same logical output for each input combination. It does not imply equal delay, drive strength, switching power, or sensitivity to a transition glitch.
>
> Read a gate diagram from its input conditions toward the output. A bubble indicates inversion at that boundary. It does not necessarily mean that the external control is active-low; active polarity describes which voltage asserts the required action. The specification and the symbol must be interpreted together.
>
> **Worked application — select the needed primitive.** A、B 表示两个条件。要求“至少一个满足”用 OR，输入 11 时输出 1；要求“恰好一个满足”用 XOR，11 时输出 0；要求“两个都满足”用 AND。对 00/01/10/11 三种输出列依次为 OR=`0111`，XOR=`0110`，AND=`0001`。仅检查 01 会误以为 OR 与 XOR 等价，应专门检查 11。
>
> In English: choose test inputs that distinguish the candidate functions. A single counterexample disproves equivalence, whereas a proof of equivalence requires every valid input combination or an algebraic identity.
>
> **English exam question:** Can any Boolean function be built using only AND gates?
>
> **Answer:** No. AND-only networks cannot generate inversion or arbitrary OR behavior from uncomplemented inputs. NAND alone or NOR alone is functionally complete because each can construct NOT and the other required operations.
>
> The construction is detailed in [[Universal Gates and Bubble Pushing]]. Connect behavior to [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]], physical settling to [[Propagation Delay and Logic Hazards]], and practical failure isolation to [[Digital Logic Troubleshooting]].

## 2 · Inverter, AND Gate and OR Gate · 三种基本运算

| 输入 AB | NOT A | AND | OR | NAND | NOR | XOR | XNOR |
|---|---|---|---|---|---|---|---|
| 00 | 1 | 0 | 0 | 1 | 1 | 0 | 1 |
| 01 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 10 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 11 | 0 | 1 | 1 | 0 | 0 | 0 | 1 |

反相器 (inverter) 输出 $\bar A$。AND 要求所有条件同时成立，OR 表示至少一个条件成立；OR 的“或”包含两者都成立。n 输入 AND 仅全 1 时输出 1；n 输入 OR 仅全 0 时输出 0。

缓冲器 (buffer / BUF) 为 $Y=A$，保留逻辑值，可承担驱动或接口功能。正逻辑用较高电压表示 1；控制的 active-high／active-low 则说明哪种电平断言事件，必须结合规范解释。

> [!example]- Inverter · 推导与例题
> **图示与讲义依据**
>
> ![[ch3-inverter-symbol.png]]
> *图 1 — 讲义 p.4 原图：反相器的符号与输出端的 negation indicator。符号方向永远是从左（输入）
> 到右（输出），三角形尖端指向输出。*
>
> ![[ch3-single-input-gates.png]]
> *图 2 — 讲义 p.5 原图：单输入门 NOT / BUF 的符号、表达式与真值表对照。
> 两张表**只有输出列不同**：$A=0$ 时 NOT 给 1 而 BUF 给 0，这就是"有没有那个小圆圈"的全部差别。*
>
> **Derivation · 推导过程**
>
> **① 真值表为什么只有 2 行**
>
> $n=1\Rightarrow2^1=2$ 行，即**把输入的所有可能取值一个个列完**：
> $A=0\Rightarrow Y=\bar0=1$；$A=1\Rightarrow Y=\bar1=0$。
>
> - 意义：单输入门的规格就是"两行表 + 一个表达式 + 一个符号"，与多输入门相比少的是组合数，不是种类。
> - 数值校验：两行、两列输入输出，穷举完整 ✓；把输出列取反就得到另一个单输入门：
>   NOT 的输出列 `1,0` 恰好是 BUF 输出列 `0,1` 的补 ✓。
>
> **② 两次取反等于原值：$\overline{\bar A}=A$**
>
> 反相器的定义是逐位取反，取反两次自然回到原值：
>
> $$Y=\overline{\bar A}=A$$
>
> - 意义：这就是逻辑代数里的**对合律 (involution)**，也是"两个反相器串联 = 一个 buffer"的依据。
> - 数值校验：$A=0\to\bar A=1\to\overline{\bar A}=0$ ✓；$A=1\to\bar A=0\to\overline{\bar A}=1$ ✓。
>   两种输入都回到原值，所以行为与 BUF 的真值表 `0,0` / `1,1` 完全一致 ✓。
> - 但工程上**不能**随手用两个反相器代替 buffer：延迟变成 $2t_{pd}$、晶体管数量翻倍、功耗更大。
>   逻辑等价 ≠ 工程等价。
>
> **③ 时序图怎么读：理想零延迟 vs 真实延迟**
>
> 讲义 p.4 给时序图的定义：*a graph that displays the relationship of two or more waveforms
> with respect to each other on a time basis*——**两个（或多个）波形在时间轴上的相互关系**。
> 读单输入门的时序图只要盯两件事：**Y 是否与 A 相反**、**沿是否对齐**。
>
> - **理想（零延迟）**：A 的每一个跳变沿处 Y 立刻反向跳变，两个沿重合，看图时一条竖线能同时穿过两条沿。
> - **真实（有延迟）**：Y 的跳变落后一个**传播延迟 (propagation delay)** $t_{pd}$，
>   逻辑功能不变，但波形整体右移。图 3 用 $A$：$0\sim20$ ns 高、$20\sim40$ ns 低（周期 40 ns、50% 占空比），
>   $t_{pd}=4$ ns 画出两种情形。
>
> ![[inverter-timing.svg]]
> *图 3 — (a) 理想反相器：虚线竖线同时穿过 A 的沿和 Y 的沿，两条沿严格对齐；
> (b) 真实反相器：Y 就是同一条波形右移 $t_{pd}=4$ ns，双箭头标出 A 在 20 ns 的下降沿与
> Y 在 24 ns 的上升沿之间的时间差。*
>
> - 数值校验：A 的高电平时间是 $80$ ns 里的 $40$ ns（$0\sim20$ 与 $40\sim60$），占空比 $40/80=50\%$；
>   理想 Y 的高电平是 $20\sim40$ 与 $60\sim80$，也是 $40$ ns，$50\%$ ✓；
>   真实 Y 的高电平是 $0\sim4$、$24\sim44$、$64\sim80$，合计 $4+20+16=40$ ns，仍是 $50\%$ ✓
>   ——**延迟不改变占空比，只把整条波形推后**。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.5 的 NOT / BUF 对照表逐行核对**
>
> 题目：把 $A$ 依次取 $0,1$，写出 NOT 与 BUF 的输出，并说明两张表的关系。
>
> 解：NOT 是取反，$A=0\Rightarrow Y=1$、$A=1\Rightarrow Y=0$；
> BUF 是复制，$A=0\Rightarrow Y=0$、$A=1\Rightarrow Y=1$。
>
> **数值校验 (Numerical check)**：把 NOT 的输出列 $1,0$ 逐行取反得到 $0,1$，正是 BUF 的输出列 ✓；
> 反过来把 BUF 取反就得到 NOT ✓；两表在每一行的输出都**不同**（$0$ vs $1$、$1$ vs $0$），
> 所以"反相器"与"缓冲器"是功能不同的两个门，不能混写 ✓。
>
> **Example 2 — 读图 3(b)：写出真实反相器的跳变时刻（延伸：传播延迟）**
>
> 题目：$A$ 为周期 $40$ ns 的方波，$t=0$ 时由低变高、$t=20$ ns 由高变低、$t=40$ ns 再变高……
> 反相器的 $t_{pd}=4$ ns，且 $t<0$ 时 $A=0$。求 $Y$ 的前几个跳变时刻与占空比。
>
> 解：$Y(t)=\overline{A(t-4\ \text{ns})}$，即"把 A 推后 4 ns 再取反"。
>
> - $t<0$ 时 $A=0\Rightarrow Y=1$，所以 $Y$ 从高电平开始；
> - A 在 $0$ ns 上升（$A$ 变 1）→ Y 在 $0+4=4$ ns **下降**；
> - A 在 $20$ ns 下降（$A$ 变 0）→ Y 在 $20+4=24$ ns **上升**；
> - A 在 $40$ ns 上升 → Y 在 $44$ ns 下降；A 在 $60$ ns 下降 → Y 在 $64$ ns 上升。
>
> **数值校验 (Numerical check)**：$[0,80)$ ns 内 Y 的高电平区间为 $[0,4)$、$[24,44)$、$[64,80)$，
> 合计 $4+20+16=40$ ns，占空比 $40/80=50\%$，与输入的 $50\%$ 相同 ✓；
> 每个 Y 的沿都比对应的 A 沿晚 $24-20=4$ ns、$44-40=4$ ns ✓，与 $t_{pd}=4$ ns 一致。
>
> **Example 3 — 两级反相器串联（自算）**
>
> 题目：把两个反相器串起来，输入 $A$ 依次取 $0,1$，求最终输出与总延迟（每个 $t_{pd}=4$ ns）。
>
> 解：$A\to\bar A\to\overline{\bar A}=A$，所以逻辑上等价于一个 BUF。
>
> **数值校验 (Numerical check)**：$A=0$：$0\to1\to0$，输出 0 ✓；$A=1$：$1\to0\to1$，输出 1 ✓，
> 两行都与 BUF 的真值表相同 ✓。总延迟 $=2\times4=8$ ns，是单个反相器的两倍——
> 所以"用两个反相器凑一个 buffer"是有代价的（见推导 ②）。
>
> **Inversion, assertion, and physical delay · 取反、有效状态与延迟**
>
> An inverter computes the Boolean complement. An active-low control is a specification saying that LOW asserts an action. These ideas often appear together, but they are not synonyms: an active-low input can feed a larger function, and an inverter can operate on ordinary data without defining any control action.
>
> Two cascaded inverters restore the original steady-state Boolean value because $\overline{\bar A}=A$. Real stages still add delay and loading. “Equivalent to a buffer” therefore refers to functionality, not a promise that the output changes at exactly the same time as the input.
>
> **Worked application — convert a reset request.** reset=1 表示请求复位，而元件有低有效 reset_n 引脚。用 $reset_n=\overline{reset}$，reset=0 时引脚为 1、不复位，reset=1 时引脚为 0、复位。若假设反相器传播延迟为 3 ns，则有效电平约晚 3 ns 到达；实际复位释放还必须满足存储元件的 recovery/removal 条件。
>
> In English: first translate the semantic request into the required pin level, then evaluate timing. The bubble at a reset pin describes an asserted LOW level. A clock bubble describes an edge polarity in a different context, so symbols should be read with their pin roles.
>
> **English exam question:** Does adding two inverters remove a logic hazard by canceling the inversions?
>
> **Answer:** Not in general. The final polarity is restored, but a pulse can propagate through both stages, depending on its width and the gates' physical response. Boolean cancellation does not cancel propagation delays or prove hazard immunity.
>
> Continue with [[Universal Gates and Bubble Pushing]], [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]], [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力|DC Transfer Characteristic]], and [[Propagation Delay and Logic Hazards]].

> [!example]- AND Gate · 推导与例题
> **图示与讲义依据**
>
> ![[ch3-two-input-gates.png]]
> *图 1 — 讲义 p.12 原图：两输入门总表。**AND 在总表的最左一列**：D 形符号、$Y=AB$、
> 4 行真值表里只有最后一行 $11$ 输出 1。与它并排的 OR 把符号换成弧形、把"全 1"换成"有 1"即为对偶。*
>
> **Derivation · 推导过程**
>
> **① 从"当且仅当"导出 4 行真值表**
>
> 把输入按二进制顺序列全，再逐行检查"是否所有输入都为 1"：
>
> | 行 | $A$ | $B$ | 判断 | $Y$ |
> |---|---|---|---|---|
> | 1 | 0 | 0 | $A$ 就是 0，条件不成立 | 0 |
> | 2 | 0 | 1 | $A=0$，条件不成立 | 0 |
> | 3 | 1 | 0 | $B=0$，条件不成立 | 0 |
> | 4 | 1 | 1 | 全为 1，条件成立 | 1 |
>
> - 意义：**输出为 1 的行只有 1 行**（全 1 那行），输出为 0 的行有 $2^n-1$ 行。这是 AND 的"指纹"。
> - 数值校验：4 行 $=2^2$ ✓；1 行为 1 ✓；$2^2-1=3$ 行为 0 ✓；把 4 行输出按 $A\cdot B$ 重算得 $0,0,0,1$ ✓。
>
> **② $n$ 输入推广：$Y=A\cdot B\cdot C\cdots$，行数 $2^n$，只有全 1 那行是 1**
>
> - 意义：AND 的"当且仅当"在 $n$ 个输入下写法不变，只是乘积项变长；
>   真值表按 $2^n$ 行、二进制顺序排（讲义 p.13 的 AND3 就是 8 行）。
> - 数值校验：AND3 的 8 行中，只有 $111$ 一行满足"全 1"，输出 1；其余 7 行 $=2^3-1$ 行输出 0 ✓。
>   再往下：AND4 需要 $2^4=16$ 行，仍只有 1 行输出 1 ✓——**行数随 $n$ 指数增长，而"1 的行数"恒为 1**。
>
> **③ 门控 (gating)：为什么它真的是一扇"门"**
>
> 把 $Y=AB$ 里的一个输入当作**使能 (enable)**，另一个当作**数据**，例如取 $B$ 为使能、$A$ 为数据：
>
> $$B=1\Rightarrow Y=A \quad(\text{数据放行}); \qquad B=0\Rightarrow Y=0 \quad(\text{数据被挡住})$$
>
> - 意义：$B=0$ 就像把门关上——**不管 $A$ 怎么变，输出都被钉在 0**。这就是"任一输入为 0，
>   输出被门控为 0"的准确含义，也是 AND 在硬件里做掩码 (masking) 的原理。
> - 数值校验：取 $A$ 的序列 $1,0,1,1$、$B$ 的序列 $1,0,1,0$，逐拍相与：
>   $1\cdot1=1$、$0\cdot0=0$、$1\cdot1=1$、$1\cdot0=0$ → $Y=1,0,1,0$ ✓。
>   第 2 拍被 $B=0$ 关掉、第 4 拍同样被 $B=0$ 关掉，而第 3 拍的 $A=1$ 因为 $B=1$ 被放行 ✓。
>
> ![[and-gate-timing.svg]]
> *图 2 — AND 的时序图：A 在 $10\sim40$ ns 为 1、B 在 $20\sim60$ ns 为 1，输出 Y 只在
> $20\sim40$ ns（两者同时为 1 的那一段）为 1。浅红色带标出"至少一个输入为 0"的时间段，
> 带下的短标签写着是哪个输入在门控（$B=0$ / $A=0$），绿色带是全图唯一能让 Y 变成 1 的窗口。*
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.12 总表的 AND 列逐行核对（与 OR / XOR 对照）**
>
> 题目：$A,B$ 按 $00,01,10,11$ 排列，写出 AND 的输出，并与同一张表里 OR、XOR 的输出对照。
>
> 解：AND 只有"全 1"才给 1：
>
> | $A$ | $B$ | AND $AB$ | OR $A+B$ | XOR $A\oplus B$ |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 |
> | 0 | 1 | 0 | 1 | 1 |
> | 1 | 0 | 0 | 1 | 1 |
> | 1 | 1 | 1 | 1 | 0 |
>
> **数值校验 (Numerical check)**：AND 列有 $1$ 行为 1、$3$ 行为 0（$1+3=4=2^2$ ✓）；
> OR 列有 $3$ 行为 1；XOR 列有 $2$ 行为 1（$2=2^{2-1}$ ✓）；
> 三列在 $11$ 行的取值分别是 $1,1,0$——**$1+1=1$ 是布尔加，$1\cdot1=1$ 是布尔乘，
> $1\oplus1=0$**，一行把三个门区分开 ✓。
>
> **Example 2 — 讲义 p.13 的 AND3：$Y=ABC$ 逐行核对**
>
> 题目：三输入 AND，$A,B,C$ 按二进制顺序取 $000\sim111$，求 8 行输出。
>
> 解：只有 $111$ 一行全为 1，因此 $Y$ 在 $000,001,010,011,100,101,110$ 七行为 0，在 $111$ 行为 1。
>
> **数值校验 (Numerical check)**：行数 $2^3=8$ ✓；输出为 1 的行数为 1 ✓，为 0 的行数 $8-1=7=2^3-1$ ✓；
> 用乘积逐行重算：$0\cdot0\cdot0=0$、$0\cdot0\cdot1=0$、$0\cdot1\cdot0=0$、$0\cdot1\cdot1=0$、
> $1\cdot0\cdot0=0$、$1\cdot0\cdot1=0$、$1\cdot1\cdot0=0$、$1\cdot1\cdot1=1$ ✓ 与判据一致。
>
> ![[ch3-multiple-input-gates.png]]
> *图 3 — 讲义 p.13 原图：多输入门，左侧即 AND3（$Y=ABC$）。8 行表里只有最后一行 $111$ 输出 1；
> 把它与右边的 XOR3 并排看，就能体会"数 1 的行数"为什么是认门的最快办法。*
>
> **Example 3 — 掩码 (masking)：用一个输入当使能（自算）**
>
> 题目：$Y=A\cdot B$，其中 $A$ 是数据序列 $1,0,1,1$，$B$ 是使能序列 $1,0,1,0$（两序列逐拍对齐）。
> 求 $Y$ 序列，并说明哪些拍被"挡住"。
>
> 解：逐拍做布尔乘：$1\cdot1=1$、$0\cdot0=0$、$1\cdot1=1$、$1\cdot0=0$ → $Y=1,0,1,0$。
>
> **数值校验 (Numerical check)**：第 4 拍 $A=1$ 却被 $B=0$ 挡住，输出 0 ✓——这正说明
> "**输入 1 不保证输出 1**"，被门控的那一拍与 $A$ 无关；
> 第 2 拍 $A=B=0$，输出 0 是两个 0 共同的结果 ✓；第 1、3 拍 $B=1$，数据被放行，$Y$ 与 $A$ 相同 ✓。
> 逐拍输出 $1,0,1,0$ 与 $A\cdot B$ 的 4 行真值表完全对得上 ✓。
>
> **Qualified conditions and enables · 条件许可与使能**
>
> AND expresses a conjunction: every required predicate must be true. Calling one input an enable does not change the truth table; it assigns that input a role in a larger design. The enable must have the asserted polarity expected by the expression. An active-low permission should first be translated to a positive predicate or be shown explicitly with inversion.
>
> A common implementation mistake is to gate a clock with an ordinary AND gate and an enable that can change at any time. If the enable rises while the clock is already HIGH, the output can contain an unintended edge. Boolean correctness of $Y=CE$ does not by itself make that output a suitable register clock.
>
> **Worked application — motor permission.** run=1 请求运行，door_closed=1 门已关，fault_n=1 表示没有故障。令 $M=run\cdot door\_closed\cdot fault_n$。输入 111 时允许，110 时因 fault_n=0 禁止。若信号改为 fault=1 表示故障，则公式要变为 $M=run\cdot door\_closed\cdot\overline{fault}$，不能照抄同一个变量名和极性。
>
> In English: the conditions are semantic predicates, not just pin levels. Verify the dangerous and inactive cases individually, and ensure that each control signal has a defined source rather than an undriven input.
>
> **English exam question:** What does a LOW enable do to an AND data gate?
>
> **Answer:** It forces the output LOW regardless of the data input. A HIGH enable passes the data's Boolean value. This is a combinational data-selection behavior; it does not store the previous output.
>
> Use [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]] for controlled register updates, [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]] for selecting held versus new data, and [[Propagation Delay and Logic Hazards]] for transitions on real paths.

> [!example]- OR Gate · 推导与例题
> **图示与讲义依据**
>
> ![[ch3-two-input-gates.png]]
> *图 1 — 讲义 p.12 原图：两输入门总表。**OR 在总表第二列**：弧形符号、$Y=A+B$、
> 4 行真值表里**只有第一行 $00$ 输出 0**。把它与左列 AND 逐行对比：两列恰好互为"镜像"——
> AND 只有 1 行是 1，OR 只有 1 行是 0。*
>
> **Derivation · 推导过程**
>
> **① 从"任一为 1"导出 4 行真值表**
>
> | 行 | $A$ | $B$ | 判断 | $Y$ |
> |---|---|---|---|---|
> | 1 | 0 | 0 | 没有一个是 1 | 0 |
> | 2 | 0 | 1 | $B=1$，条件成立 | 1 |
> | 3 | 1 | 0 | $A=1$，条件成立 | 1 |
> | 4 | 1 | 1 | 两个都是 1，条件更成立 | 1 |
>
> - 意义：**输出为 0 的行只有 1 行**（全 0 那行），输出为 1 的行有 $2^n-1$ 行——这是 OR 的"指纹"。
> - 数值校验：4 行 $=2^2$ ✓；1 行为 0、$2^2-1=3$ 行为 1 ✓；
>   用 $A+B$ 重算输出列得 $0,1,1,1$ ✓（注意第 4 行是 $1+1=1$，不是 2）。
>
> **② $n$ 输入推广：$Y=A+B+C+\cdots$，行数 $2^n$，只有全 0 行是 0**
>
> - 意义："有 1 就 1"在 $n$ 个输入下不变，只是或项变长；真值表按 $2^n$ 行、二进制顺序排。
> - 数值校验：三输入 OR3 共 $2^3=8$ 行，只有 $000$ 一行输出 0，其余 $8-1=7=2^3-1$ 行输出 1 ✓；
>   四输入 OR4 是 $2^4=16$ 行、15 行输出 1 ✓——行数与 OR 的"1 的行数"都随 $n$ 变化，
>   但"**0 的行数恒为 1**"这条性质不变 ✓。
>
> **③ 对偶性：AND 的"零元"与 OR 的"壹元"**
>
> 把 $0$、$1$ 与 AND、OR 互换，两条式子是**对偶**的：
>
> $$A\cdot 0=0 \quad(\text{AND 被 0 门控}) \qquad\leftrightarrow\qquad A+1=1 \quad(\text{OR 被 1 强制拉高})$$
>
> - 意义：AND 里那个"说了算"的输入值是 0，OR 里是 1；所以 AND 做**掩码清零**、OR 做**置位 (set)**。
> - 数值校验：$A=0$ 时 $0\cdot0=0$、$0+1=1$；$A=1$ 时 $1\cdot0=0$、$1+1=1$ ✓——
>   无论 $A$ 取什么，$A\cdot0$ 恒为 0、$A+1$ 恒为 1，与真值表逐行一致 ✓（Ch4 会有完整的定律表 [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则|Laws and Rules of Boolean Algebra]]）。
>
> **④ 时序图怎么读**
>
> - 方法：**先把两个输入为 0 的时间段找出来**，只有这些时间段 Y 才是 0；
>   其余任何一段（哪怕只有一个输入是 1）Y 都是 1。
> - 图 2 用的是与 [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算|AND Gate]] 完全相同的一组 A / B 波形，唯一变化的是输出：AND 只取"同时为 1"的重叠段，
>   OR 取"至少一个为 1"的全部时间段——把两张图叠起来看，OR 的 1 区间正好覆盖 AND 的 1 区间。
>
> ![[or-gate-timing.svg]]
> *图 2 — OR 的时序图：A 在 $10\sim40$ ns 为 1、B 在 $20\sim60$ ns 为 1，输出 Y 从 $10$ ns 一直保持到
> $60$ ns 为 1——$10\sim20$ ns 只有 A 是 1、$40\sim60$ ns 只有 B 是 1，都足以让 Y 为 1（绿色带）。
> 只有 $0\sim10$ ns 与 $60\sim80$ ns 两段（两个输入都是 0）Y 才为 0，浅红色带与带下短标签标出的正是这两段。*
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.12 的 OR 列 + p.25 陷阱题判定**
>
> 题目：(a) $A,B$ 按 $00,01,10,11$ 排列，写出 OR 输出；(b) 判断讲义 p.25 第 3 题
> *If any input to an OR gate is zero, the output is zero* 的真假并给出反例。
>
> 解：(a) 只有 $00$ 行输出 0，其余三行输出 1：`0,1,1,1`。
> (b) 该命题**为假**——"某个输入为 0"只是必要条件之一，只有**所有**输入都为 0 才输出 0。
>
> **数值校验 (Numerical check)**：反例取 $A=0,B=1$，按定义 $Y=A+B=0+1=1\ne0$，命题被推翻 ✓；
> 再逐行核对 4 行：$0+0=0$、$0+1=1$、$1+0=1$、$1+1=1$ ✓——4 行里 3 行为 1，与"只有 1 行为 0"一致 ✓。
>
> **Example 2 — 三输入 OR3（自算，与讲义 p.13 的 AND3 / XOR3 同一种行序）**
>
> 题目：$Y=A+B+C$，输入按二进制顺序取 $000\sim111$，求 8 行输出。
>
> 解：只有 $000$ 行三个输入全为 0，输出 0；其余 7 行输出 1。
>
> **数值校验 (Numerical check)**：行数 $2^3=8$ ✓；输出为 0 的行数 $1$ ✓，为 1 的行数 $8-1=7=2^3-1$ ✓；
> 逐行重算：$000\to0$；$001,010,011,100,101,110,111$ 各有至少一个 1，全部为 1 ✓。
> 与讲义 p.13 的 AND3（只有 $111\to1$，1 行是 1）对照：两者的"1 的行数"分别是 7 与 1，
> 相加 $7+1=8$，正好把 8 行分完 ✓——这两个门在同一张表上是互补的。
>
> **Example 3 — 布尔加 ≠ 算术加（自算）**
>
> 题目：分别用布尔加与算术加计算 $1+1$、$1+1+1$，并说明差别。
>
> 解：布尔加 $1+1=1$、$1+1+1=1$（OR 是"有没有 1"，不是"有几个 1"）；
> 算术加 $1+1=10_2$、$1+1+1=11_2$（有进位，见 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]]）。
>
> **数值校验 (Numerical check)**：用真值表反查：$A=1,B=1$ 时 $Y=A+B=1$ ✓，与 $1+1=1$ 一致；
> 三输入时 $111$ 行 $Y=1$ ✓，而算术结果是 $3_{10}=11_2$——如果 OR 的 $+$ 也按算术进位，
> $111$ 行就会得到 3，而 OR 的输出只能是 0 或 1，矛盾 ✓。
> 所以布尔式 $Y=A+B$ 里的 "$+$" 只表示 OR，与 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 的加法符号必须分清。
>
> **Inclusive OR in specifications · 题目中的包含或**
>
> Logical OR is inclusive: any one TRUE input is sufficient, and multiple TRUE inputs are also allowed. Natural-language “or” can be ambiguous, so an exam specification containing “exactly one” requires XOR-like behavior rather than ordinary OR. “At least one” requires OR.
>
> OR combines Boolean conditions, not physical output pins. Two gate outputs wired together do not implement an OR function when they are ordinary push-pull drivers. A defined OR gate has separate inputs and one output driver. Special shared-bus arrangements need their own electrical model and enable protocol.
>
> **Worked application — alarm aggregation.** smoke、overheat、manual=1 各表示报警条件，$A=smoke+overheat+manual$。输入 110 表示两种故障同时发生，A=1，应持续报警。若误用三输入 XOR，110 中两个 1 得输出 0，恰好在双故障时撤销报警。枚举 000、100、110、111，OR 输出 0、1、1、1；XOR 为 0、1、0、1。
>
> In English: when simultaneous causes should reinforce an action, count-free Boolean OR is appropriate. It reports whether the set of asserted causes is nonempty; it does not report how many causes are present.
>
> **English exam question:** Why is $1+1=1$ valid in Boolean algebra but not in binary integer arithmetic?
>
> **Answer:** In a Boolean expression “+” denotes OR, so two TRUE conditions still produce TRUE. Integer addition produces the value two, represented as `10` in binary with a carry. The same written symbol denotes different operations in the two contexts.
>
> Compare [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]], [[Boolean Algebra and Circuit Models#2 · Boolean Equation · 从需求写函数|Boolean Equation]], and [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]]. For physical sharing, follow [[Tri-State Buffers and Bus Drivers]].

## 3 · NAND Gate and NOR Gate · 输出取补与气泡

NAND 为 $\overline{AB}$，NOR 为 $\overline{A+B}$。输出气泡表示对整个门函数取反；输入气泡只反相对应输入。

$$\overline{AB}=\bar A+\bar B,\qquad\overline{A+B}=\bar A\bar B.$$

因此 NAND 的等价符号是 negative-OR，NOR 的是 negative-AND。通用性与多级气泡推移集中见 [[Universal Gates and Bubble Pushing]]。

> [!example]- NAND Gate · 推导与例题
> **图示与讲义依据**
>
> ![[nand-gate-timing.svg]]
> *图 1 — $A$（周期 4）、$B$（周期 2）与 $Y=\overline{A\cdot B}$ 的时序图，同一时间轴上并排画出
> AND 的输出 $A\cdot B$（蓝）作对照。灰底的两格是 $A\cdot B=1$ 的时刻（第 4、8 格），NAND 在那里把 1 翻成 0；
> 其余各格两者互补 —— 这就是讲义 p.8 "How to verify/prove?" 的图形答案：NAND = AND + 反相器。*
>
> **Derivation · 推导过程**
>
> **① 从 AND 出发接一个反相器**
>
> 把 AND 的输出 $X=AB$ 送进反相器（$Y=\overline{X}$），立刻得到
>
> $$Y=\overline{AB}$$
>
> - 意义：NAND 不是新发明的运算，它只是**两个已学门的串联**，所以它的真值表可以把 AND 的真值表整列取反得到。
> - 数值校验（取 $A=1,B=1$）：$X=1\cdot1=1\Rightarrow Y=\bar1=0$ ✓（与真值表第 4 行一致）；
>   取 $A=1,B=0$：$X=1\cdot0=0\Rightarrow Y=\bar0=1$ ✓（第 3 行一致）。
>
> **② 逐行穷举 (perfect induction)**
>
> 不需要任何定理，把 $2^2=4$ 种输入全代一遍就能确认定义式：
>
> | $A$ | $B$ | $X=AB$ | $Y=\bar X=\overline{AB}$ | 与真值表一致？ |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 1 | ✓ |
> | 0 | 1 | 0 | 1 | ✓ |
> | 1 | 0 | 0 | 1 | ✓ |
> | 1 | 1 | 1 | 0 | ✓ |
>
> - 意义：这就是 Ch4 的**完全归纳法 (perfect induction)** 的雏形
>   （链 [[Boolean Algebra and Circuit Models#5 · Proof by Perfect Induction · 穷举与代数验证|Proof by Perfect Induction]]）：变量少时，穷举所有行就是最硬的证明。
> - 数值校验：四行全部一致，且"输出 0 的行数 = 1"，正是 AND 的"输出 1 的行数 = 1"取反的结果 ✓。
>
> **③ 用德摩根定理改写成"反相输入的 OR"**
>
> $$\overline{AB}=\bar A+\bar B$$
>
> - 意义：同一个 NAND 门有两种等价画法 —— 一个 D 形门带输出气泡，或者一个 OR 门带**两个输入气泡**。
>   这条式子是 Ch4 德摩根定理的第一条（链 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]），也是"气泡搬家 (bubble pushing)"的合法依据。
> - 数值校验（取 $A=1,B=0$）：左边 $=\overline{1\cdot0}=\bar0=1$；右边 $=\bar1+\bar0=0+1=1$ ✓（两式相等）。
> - 逐行核对（Python 复核全部 4 行）：四行中 $\overline{AB}$ 与 $\bar A+\bar B$ 全部相等 ✓。
>
> **④ 工程直觉：为什么数字电路偏爱 NAND**
>
> CMOS 工艺里，"先 AND 再取反"比"直接 AND"便宜：AND 门内部其实就是 NAND 加一个反相器。
> 所以**凡是能用 NAND 搭的逻辑，实际芯片里往往真的全用 NAND 搭**（NAND 与 NOR 是通用门 universal gate，
> Ch5 会系统讲怎么只用一个门型实现任意逻辑）。
>
> **Worked Example · 例题**
>
> **Example 1 — 三输入 NAND3 的真值表（讲义 p.13 的 AND3 表加气泡）**
>
> 题目：讲义 p.13 中间那张表是三输入 AND3，$Y=ABC$，只有 $111$ 一行输出 1。求三输入 NAND3 的真值表。
>
> 解：对 AND3 的输出列整列取反（气泡的作用）：
>
> | $A$ | $B$ | $C$ | $ABC$（p.13 的 AND3） | $Y=\overline{ABC}$（NAND3） |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 1 |
> | 0 | 0 | 1 | 0 | 1 |
> | 0 | 1 | 0 | 0 | 1 |
> | 0 | 1 | 1 | 0 | 1 |
> | 1 | 0 | 0 | 0 | 1 |
> | 1 | 0 | 1 | 0 | 1 |
> | 1 | 1 | 0 | 0 | 1 |
> | 1 | 1 | 1 | 1 | **0** |
>
> **数值校验 (Numerical check)**：$2^3=8$ 行齐全 ✓；输出列恰好一个 0（在 $111$）✓；
> 用 Python 逐行复核 $Y=\lnot(A\land B\land C)$：八行全部一致 ✓；
> $n$ 输入的通式 $Y=\overline{A\cdot B\cdots}$，输入每多一个，表的行数翻倍而"0 的行数"始终是 1 ✓。
>
> ![[ch3-multiple-input-gates.png]]
> *图 2 — 讲义 p.13 原图：多输入门的三组符号、表达式与真值表，行都按二进制顺序列出。
> 左表是 NOR3（$Y=\overline{A+B+C}$，只有 $000$ 输出 1），中间是本例用的 AND3（$Y=ABC$），
> 右表是三输入 XOR（奇数个 1 输出 1，见 [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]]）。NAND3 就是中间那张 AND3 的输出加一个气泡，
> 即本例题表格的最后一列。*
>
> **Example 2 — 从波形读出 NAND 的输出（自算，配合图 1）**
>
> 题目：图 1 中 $A$ 的波形是 `0011 0011`、$B$ 是 `0101 0101`（每格 1 个时间单位）。求 $Y$ 的波形。
>
> 解：逐格先算 $A\cdot B$ 再取反：
>
> | 格 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
> |---|---|---|---|---|---|---|---|---|
> | $A$ | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
> | $B$ | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
> | $A\cdot B$ | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
> | $Y=\overline{AB}$ | 1 | 1 | 1 | **0** | 1 | 1 | 1 | **0** |
>
> **数值校验 (Numerical check)**：$Y=$ `1110 1110` ✓；$A$ 两格一个周期、$B$ 一格一个周期，
> 于是四种输入组合 $(00,01,10,11)$ 恰好各出现两次，波形把真值表的两组"1,1,1,0"重复了一遍 ✓；
> $Y$ 与 $A\cdot B$ 逐格相加恒为 1（互补）✓ —— 与图 1 中两条输出波形的关系一致。
>
> **Example 3 — 德摩根改写：把 NAND 画成"反相输入的 OR"（自算）**
>
> 题目：用 $\overline{AB}=\bar A+\bar B$ 重新计算 Example 2 的每一格，确认结果不变。
>
> 解：$\bar A$ 是 `1100 1100`，$\bar B$ 是 `1010 1010`，两者按位 OR：`1110 1110` ✓ 与 Example 2 的 $Y$ 完全相同。
>
> **数值校验 (Numerical check)**：OR 的每一格只要有一个 1 就是 1，因此只有 $A=B=1$ 的格子（第 4、8 格）为 0 ✓；
> 这就是"两个输入气泡 + OR 门"的波形解释，与 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]] 的 $\overline{AB}=\bar A+\bar B$ 逐行一致 ✓。
>
> **NAND as a complete construction set · NAND 的功能完备性**
>
> NAND is functionally complete because it can construct inversion and conjunction, then use DeMorgan's theorem to construct disjunction. Tie both inputs together to obtain $\overline{AA}=\bar A$. Invert a NAND output to obtain AND. With complemented inputs, NAND produces $\overline{\bar A\bar B}=A+B$.
>
> A NAND-NAND implementation of SOP deliberately uses two inversions. The first level produces complemented products. The second level complements their AND, which becomes an OR of the original products. Do not insert extra output inversion after the final NAND unless the specification requires the complemented function.
>
> **Worked application — three NAND gates.** 实现 $Y=AB+CD$：$n_1=\overline{AB}$，$n_2=\overline{CD}$，$Y=\overline{n_1n_2}=AB+CD$。取 ABCD=1100，n1=0、n2=1、Y=1；取 1010，两乘积都 0，n1=n2=1，Y=0。中间低电平代表“该乘积已满足”，因此第二级的输出极性要沿式子检查。
>
> In English: the NAND network preserves the function of the two-level SOP. Its physical delay and input count must still be evaluated against available gates and the timing specification.
>
> **English exam question:** How many two-input NAND gates are sufficient to construct a two-input OR if only uncomplemented A and B are available?
>
> **Answer:** Three: one NAND with tied A inputs to generate $\bar A$, one with tied B inputs to generate $\bar B$, and a final NAND of those complements. The resulting output is $A+B$.
>
> For diagram transformations use [[Universal Gates and Bubble Pushing]] and [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]. The same primitive becomes a memory element only with a suitable feedback topology, as explained in [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]].

> [!example]- NOR Gate · 推导与例题
> **图示与讲义依据**
>
> ![[nor-gate-timing.svg]]
> *图 1 — $A$（周期 4）、$B$（周期 2）与 $Y=\overline{A+B}$ 的时序图，并排画出 OR 的输出 $A+B$（蓝）作对照。
> 灰底的两格是 $A+B=0$（第 1、5 格，两个输入同时为 0），只有那里 NOR 的输出气泡把 0 抬成 1 ——
> 对应真值表的第一行（$A=B=0$）。*
>
> **Derivation · 推导过程**
>
> **① 从 OR 出发接一个反相器**
>
> 把 OR 的输出 $X=A+B$ 送进反相器（$Y=\bar X$）：
>
> $$Y=\overline{A+B}$$
>
> - 意义：NOR 也是"两个已学门的串联"，真值表可由 OR 的真值表整列取反得到。
> - 数值校验（取 $A=0,B=0$）：$X=0+0=0\Rightarrow Y=\bar0=1$ ✓（真值表第 1 行）；
>   取 $A=0,B=1$：$X=0+1=1\Rightarrow Y=\bar1=0$ ✓（第 2 行）。
>
> **② 逐行穷举 (perfect induction)**
>
> | $A$ | $B$ | $X=A+B$ | $Y=\bar X=\overline{A+B}$ | 与真值表一致？ |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 1 | ✓ |
> | 0 | 1 | 1 | 0 | ✓ |
> | 1 | 0 | 1 | 0 | ✓ |
> | 1 | 1 | 1 | 0 | ✓ |
>
> - 意义：四行一次代完，不用任何定理（链 [[Boolean Algebra and Circuit Models#5 · Proof by Perfect Induction · 穷举与代数验证|Proof by Perfect Induction]]）。
> - 数值校验：输出列恰好一个 1，位置在 $A=B=0$ ✓；这正是 OR 输出列"三个 1"取反后的结果 ✓。
>
> **③ 德摩根改写：NOR = "反相输入的 AND"**
>
> $$\overline{A+B}=\bar A\bar B$$
>
> - 意义：同一个 NOR 门可以画成"OR + 输出气泡"，也可以画成"两个输入气泡 + AND 门"。
>   这是 Ch4 德摩根定理的第二条（链 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]），也是气泡搬家的依据。
> - 数值校验（取 $A=0,B=1$）：左边 $=\overline{0+1}=\bar1=0$；右边 $=\bar0\cdot\bar1=1\cdot0=0$ ✓。
> - 逐行核对（Python 复核全部 4 行）：$\overline{A+B}$ 与 $\bar A\bar B$ 四行全等 ✓。
>
> **④ 与 NAND 的对偶 (duality)**
>
> 把布尔式里的 **AND ↔ OR**、**0 ↔ 1** 同时互换，得到的式子叫**对偶式 (dual)**：
>
> | NAND 一侧 | 对偶操作 | NOR 一侧 |
> |---|---|---|
> | $Y=\overline{AB}$（全 1 时输出 0） | AND↔OR、0↔1 | $Y=\overline{A+B}$（全 0 时输出 1） |
> | 符号：D 形 + 输出气泡 | 形状对偶 | 符号：弧形 + 输出气泡 |
> | $\overline{AB}=\bar A+\bar B$ | 两边取对偶 | $\overline{A+B}=\bar A\bar B$ |
>
> - 意义：NAND 与 NOR 的每一条性质都能"翻译"过去；记住一个，另一个就免费得到（链 [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则|Boolean Axioms]]）。
> - 数值校验：NAND 的输出列 `1,1,1,0`，逐位取反得 `0,0,0,1`，正是 NOR 的输出列 ✓（两表互补）。
>
> **⑤ 工程直觉：为什么 NOR 常被"NAND + 反相器"替代**
>
> CMOS 里 NAND 的串联管在**下拉 (pull-down)** 一侧（NMOS 串起来仍然够强），
> 而 NOR 的串联管在**上拉 (pull-up)** 一侧（PMOS 本来就弱，串起来更慢）。
> 所以同一工艺下 NAND 往往比 NOR 快、面积也更划算 —— 这也是后面组合逻辑综合时偏爱 NAND 的原因
> （通用门的系统用法见 Ch5）。
>
> **Worked Example · 例题**
>
> **Example 1 — 两输入 NOR 与三输入 NOR3（讲义 p.12 / p.13 原表）**
>
> 题目：讲义 p.12 的第五张表是 NOR2（$Y=\overline{A+B}$）；p.13 最左边的表是三输入 NOR3。逐行核对这两张表。
>
> 解（p.12 的 NOR2，行按二进制顺序）：
>
> | $A$ | $B$ | $A+B$ | $Y=\overline{A+B}$（讲义 p.12） |
> |---|---|---|---|
> | 0 | 0 | 0 | 1 |
> | 0 | 1 | 1 | 0 |
> | 1 | 0 | 1 | 0 |
> | 1 | 1 | 1 | 0 |
>
> 解（p.13 左表的 NOR3，$Y=\overline{A+B+C}$）：
>
> | $A$ | $B$ | $C$ | $A+B+C$ | $Y=\overline{A+B+C}$ |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 0 | **1** |
> | 0 | 0 | 1 | 1 | 0 |
> | 0 | 1 | 0 | 1 | 0 |
> | 0 | 1 | 1 | 1 | 0 |
> | 1 | 0 | 0 | 1 | 0 |
> | 1 | 0 | 1 | 1 | 0 |
> | 1 | 1 | 0 | 1 | 0 |
> | 1 | 1 | 1 | 1 | 0 |
>
> **数值校验 (Numerical check)**：NOR2 输出列 `1,0,0,0` ✓、NOR3 输出列 `1,0,0,0,0,0,0,0` ✓；
> 用 Python 逐行复核 $Y=\lnot(A\lor B\lor C)$ 全部 8 行一致 ✓；
> "1 的个数 = 1"且都在第一行（全 0 行）—— 这正是 NOR 的签名 ✓。
>
> ![[ch3-two-input-gates.png]]
> *图 2 — 讲义 p.12 原图：六个两输入门（从左到右依次是 AND、OR、XOR、NAND、NOR、XNOR）的符号、表达式与真值表，
> NOR 是第五张表，它的 $Y$ 列只有第一行（$A=B=0$）为 1；紧挨着它左边的第四张是 NAND，两列恰好互补 —— 对照着看最省力。*
>
> **Example 2 — 从波形读出 NOR 的输出（自算，配合图 1）**
>
> 题目：图 1 中 $A=$ `0011 0011`、$B=$ `0101 0101`。求 $Y$ 的波形，并指出 $Y=1$ 的格子。
>
> 解：先算 $A+B$ 再取反：
>
> | 格 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
> |---|---|---|---|---|---|---|---|---|
> | $A$ | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
> | $B$ | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
> | $A+B$ | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 |
> | $Y=\overline{A+B}$ | **1** | 0 | 0 | 0 | **1** | 0 | 0 | 0 |
>
> **数值校验 (Numerical check)**：$Y=$ `1000 1000` ✓；$Y=1$ 只出现在第 1、5 格，而这两格恰好是
> $(A,B)=(0,0)$ ✓；$Y$ 与 $A+B$ 逐格互补（相加恒为 1）✓ —— 与图 1 的两条波形一致。
>
> **Example 3 — 真假判断题（讲义 p.25 Quiz 原题）**
>
> 题目：判断并说明理由。
> (a) "A NOR gate can be considered as an OR gate followed by an inverter."
> (b) "If any input to an OR gate is zero, the output is zero."
>
> 解：
> (a) **True**。$Y=\overline{A+B}$ 就是先把两个输入 OR 起来，再取反；气泡即那个反相器。
> (b) **False**。OR 输出为 0 的条件是**所有**输入都为 0，不是"任意一个为 0"。
>    反例：$A=1,B=0\Rightarrow A+B=1$，输出是 1 而不是 0。
>
> **数值校验 (Numerical check)**：(a) 逐行：$A+B$ 列 `0,1,1,1` 取反得 `1,0,0,0`，与 NOR2 真值表相同 ✓；
> (b) 在 $A=1,B=0$ 这一行，$A+B=1$ ✓，"任一输入为 0 则输出为 0"被这一行直接推翻 ✓
> （OR 的真值表里输出为 1 的行有 3 行，只有全 0 行是 0）。
>
> **NOR implementation and zero conditions · NOR 实现与零条件**
>
> NOR is functionally complete and is naturally paired with product-of-sums expressions. A NOR-NOR network inverts each first-level sum, then complements the OR of those inversions. DeMorgan's theorem recovers the AND of the original sums.
>
> NOR's output is TRUE when none of its inputs is TRUE. This makes it useful for an “all clear” condition. In a real system the meaning of each input must be specified: a LOW wire does not automatically mean the corresponding fault is absent if the fault input itself is active-low.
>
> **Worked application — NOR-NOR POS.** 实现 $Y=(A+B)(C+D)$：$n_1=\overline{A+B}$、$n_2=\overline{C+D}$，末级 $Y=\overline{n_1+n_2}$。取 1001，两和项均为 1，n1=n2=0，Y=1；取 1000，第二个和项为 0，n2=1，Y=0。最后一级不能改成 NAND，否则不再保持 POS 函数。
>
> In English: a first-level NOR reports that a clause is false. The final NOR is HIGH only when neither clause is false, which is exactly the conjunction of the original clauses.
>
> **English exam question:** Can an XOR replace a NOR because both output zero for some mixed inputs?
>
> **Answer:** No. For inputs 00, NOR outputs 1 and XOR outputs 0. For 01, NOR outputs 0 and XOR outputs 1. A replacement must match every specified row, not merely one shared output value.
>
> Apply this reasoning to [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Product-of-Sums Form]], [[Karnaugh Map Minimization#3 · POS Minimization with Karnaugh Map · 圈 0 读和项|POS Minimization with Karnaugh Map]], [[Universal Gates and Bubble Pushing]], and [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]]. Cross-coupling changes the system from a feedforward function into a state-dependent network.

## 4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性

$$A\oplus B=A\bar B+\bar AB,\qquad\overline{A\oplus B}=AB+\bar A\bar B.$$

两输入 XOR 检测不同，XNOR 检测相同。多输入 XOR 检测奇数个 1，其整体补检测偶数个 1；它们并不检测“所有输入相同”。多个二输入 XNOR 串联不能直接替代“XOR 全部输入后取一次补”。

> [!IMPORTANT] XOR 不统计“至少一个”
> $1+1=1$ 是布尔 OR；$1\oplus1=0$ 是异或；算术 $1+1=10_2$ 则包含进位。半加器需要 XOR 给和位、AND 给进位。

> [!example]- Exclusive-OR Gate · 推导与例题
> **图示与讲义依据**
>
> ![[xor-gate-timing.svg]]
> *图 1 — $A$（周期 4）、$B$（周期 2）与 $Y=A\oplus B$ 的时序图。每个格子顶部标出两个输入的比较结果：
> `≠`（不同，红）或 `=`（相同，灰）；灰底格子正是 $A\neq B$ 的四格（第 2、3、6、7 格），
> $Y$ 在那里为 1 —— 与真值表的两行 "不同 → 1" 完全对应。*
>
> **Derivation · 推导过程**
>
> **① 从真值表写出 $Y=A\bar B+\bar AB$**
>
> "不同为 1"意味着输出为 1 的行只有两行：$(A,B)=(0,1)$ 与 $(1,0)$。
> 按 Ch4 的规则，每行写一个含全部变量的乘积项（取值为 1 的变量写原变量、取值为 0 的写反变量），再 OR：
>
> $$Y=\underbrace{\bar AB}_{(0,1)\text{ 行}}+\underbrace{A\bar B}_{(1,0)\text{ 行}}$$
>
> - 意义：真值表 → 标准 SOP 是一步机械操作（链 [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]]、[[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项|Minterm and Maxterm]]）。
> - 数值校验（取 $A=1,B=0$）：$A\bar B=1\cdot1=1$、$\bar AB=0\cdot0=0\Rightarrow Y=1$ ✓；
>   取 $A=1,B=1$：$A\bar B=1\cdot0=0$、$\bar AB=0\cdot1=0\Rightarrow Y=0$ ✓（两个乘积项同时为 0）。
> - 全表核验（Python 复核 4 行）：$A\bar B+\bar AB$ 与"两输入不同"完全一致 ✓。
>
> **② 另一种等价写法：$A\oplus B=(A+B)\overline{AB}$**
>
> - 意义：把"至少一个 1"（$A+B$）与"不是两个都 1"（$\overline{AB}$）相乘 —— 这就是用 OR/NAND/AND 搭 XOR 的经典结构。
> - 数值校验（取 $A=1,B=1$）：$(1+1)\cdot\overline{1\cdot1}=1\cdot0=0$ ✓；
>   取 $A=0,B=1$：$(0+1)\cdot\overline{0\cdot1}=1\cdot1=1$ ✓。四行逐一代入都与第 ① 条相同 ✓。
>
> **③ 多输入推广：奇数个 1 → 1**
>
> 三输入时把定义写成"1 的个数为奇数"：
>
> $$Y=A\oplus B\oplus C=\sum m(1,2,4,7)$$
>
> - 意义：三种"恰好一个 1"的行 $(001,010,100)$ 加上"恰好三个 1"的行 $(111)$，共 4 行输出 1 —— 这就是
>   **奇数性指示 (odd-parity indication)** 函数，也是讲义 p.13 右表标注 "Odd parity" 的原因（逐行核对见 Example 2）；若把该结果作为新增位，则生成的是偶校验码字。
> - 数值校验：$A=1,B=1,C=1$ 时 1 的个数是 3（奇）→ $Y=1$ ✓；$A=1,B=1,C=0$ 时是 2（偶）→ $Y=0$ ✓。
> - 递推校验：$A\oplus B\oplus C=(A\oplus B)\oplus C$ —— 先算前两个的奇偶，再与第三个异或 ✓（Python 逐行一致）。
>
> **④ XOR 的代数性质（都能用真值表一行行验证）**
>
> | 性质 | 式子 | 直觉 |
> |---|---|---|
> | 与 0 异或 | $A\oplus0=A$ | 0 不改变奇偶性 |
> | 与 1 异或 | $A\oplus1=\bar A$ | 1 翻转该位 |
> | 自异或 | $A\oplus A=0$ | 两个相同的 1 抵消 |
> | 与反变量 | $A\oplus\bar A=1$ | 恰好一个 1 |
> | 交换/结合 | $A\oplus B=B\oplus A$、$(A\oplus B)\oplus C=A\oplus(B\oplus C)$ | 与 1 的个数有关，与顺序无关 |
>
> - 意义："$A\oplus1=\bar A$"说明 XOR 是**可编程反相器**（把控制位当开关），
>   而 "$A\oplus A=0$"是 CRC 校验"两端再除一遍、余数为 0 就判无错"的原理（链 [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|Cyclic Redundancy Check]]）。
> - 数值校验：$A=1$ 时 $A\oplus1=0=\bar1$ ✓、$A\oplus A=1\oplus1=0$ ✓、$A\oplus\bar A=1\oplus0=1$ ✓。
>
> **⑤ 应用：XOR 把两个比特"相加"（讲义 p.11）**
>
> 两个 1 位二进制数相加的结果是 2 位：本位和 (Sum) 与进位 (Carry)：
>
> $$1+1=10_2\ \Rightarrow\ \text{Sum}=0,\ \text{Carry}=1$$
>
> 对照真值表会发现：**Sum 列就是 XOR 的输出**，**Carry 列就是 AND 的输出**（对应"两个都是 1"那一行）。
> 于是 `XOR + AND` 两个门就构成了 **半加器 (half adder)**（链 [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算|AND Gate]]、[[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]]）：
>
> $$\text{Sum}=A\oplus B,\qquad \text{Carry}=A\cdot B,\qquad 2\cdot\text{Carry}+\text{Sum}=A+B$$
>
> - 意义：这是 Ch2 的二进制加法第一次落到门上；把多个半加器串起来（低级进位接下一级）就是全加器与多位加法器（Ch6 内容）。
> - 数值校验：$A=1,B=1$：Sum $=0$、Carry $=1$，$2\times1+0=2=A+B$ ✓；$A=1,B=0$：Sum $=1$、Carry $=0$，$2\times0+1=1$ ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 两输入 XOR：真值表、SOP 与等价式三路对齐（讲义 p.10 / p.12）**
>
> 题目：讲义 p.12 第三张表是 XOR2（$Y=A\oplus B$）。用三种方法算出 $Y$ 并互相对照：
> (a) 定义（不同为 1）；(b) $A\bar B+\bar AB$；(c) $(A+B)\overline{AB}$。
>
> | $A$ | $B$ | (a) 不同为 1 | (b) $A\bar B$ | (b) $\bar AB$ | (b) OR 后 | (c) $A+B$ | (c) $\overline{AB}$ | (c) 相乘 |
> |---|---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
> | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |
> | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 |
> | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
>
> **数值校验 (Numerical check)**：三列结果 `0,1,1,0` 完全相同 ✓（用 Python 对 4 行全部复核）；
> $Y=1$ 的行数是 2，恰好等于真值表里"两个输入不同"的组合数 $C_2^1=2$ ✓；
> 把 $Y$ 整列取反得 `1,0,0,1` —— 那是 [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-NOR Gate]] 的输出 ✓。
>
> ![[ch3-xor-xnor.png]]
> *图 2 — 讲义 p.10 原图：左半是 XOR 的符号、表达式与真值表，右半是 XNOR，底部是两者的时序图。
> 本例题用的是左边那张表；注意 XOR 符号输入侧多出的那道弧线，以及 XNOR = XOR 加输出气泡。*
>
> **Example 2 — 三输入 XOR3：奇数个 1 的指示（讲义 p.13 右表逐行核对）**
>
> 题目：讲义 p.13 最右边的三输入表标注 "Odd parity: Output true if an odd number of inputs are true"。
> 逐行核对它的 $Y$ 列，并说明它为什么是"奇数个 1 输出 1"。
>
> | $A$ | $B$ | $C$ | 1 的个数 | 奇偶 | $Y=A\oplus B\oplus C$（讲义 p.13 原表） |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 偶 | 0 |
> | 0 | 0 | 1 | 1 | 奇 | 1 |
> | 0 | 1 | 0 | 1 | 奇 | 1 |
> | 0 | 1 | 1 | 2 | 偶 | 0 |
> | 1 | 0 | 0 | 1 | 奇 | 1 |
> | 1 | 0 | 1 | 2 | 偶 | 0 |
> | 1 | 1 | 0 | 2 | 偶 | 0 |
> | 1 | 1 | 1 | 3 | 奇 | 1 |
>
> **数值校验 (Numerical check)**：读出的 $Y$ 列是 `0,1,1,0,1,0,0,1`，与讲义 p.13 原表逐行一致 ✓；
> 用 Python 复核 $\left(\sum\text{bits}\right)\bmod 2$ 的全部 8 行：完全一致 ✓；
> $Y=1$ 的行数 $=4=$ 奇数个 1 的组合数 $C_3^1+C_3^3=3+1$ ✓；
> 把 $Y$ 整列取反得 `1,0,0,1,0,1,1,0`，即"偶数个 1"（XNOR3，[[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-NOR Gate]]）✓。
>
> **Example 3 — 半加器：XOR 出 Sum、AND 出 Carry（讲义 p.11）**
>
> 题目：用 XOR 与 AND 实现"两个比特相加"，列出四种输入下的 Sum 与 Carry，并检查 $2\,\text{Carry}+\text{Sum}=A+B$。
>
> | $A$ | $B$ | Sum $=A\oplus B$（XOR） | Carry $=A\cdot B$（AND） | $2\,\text{Carry}+\text{Sum}$ | $A+B$ |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | $2\times0+0=0$ | 0 |
> | 0 | 1 | 1 | 0 | $2\times0+1=1$ | 1 |
> | 1 | 0 | 1 | 0 | $2\times0+1=1$ | 1 |
> | 1 | 1 | 0 | 1 | $2\times1+0=2$（即二进制 `10`） | 2 |
>
> **数值校验 (Numerical check)**：四行的 $2\,\text{Carry}+\text{Sum}$ 与 $A+B$ 全部相等 ✓（Python 复核）；
> $A=B=1$ 时 Sum $=0$、Carry $=1$，写成二进制就是 `10` $=2$ ✓ —— 与 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 里 $1+1=10_2$ 一致；
> 单独一个 XOR 只能给出 Sum，第 4 行的进位必须由 AND 提供 ✓。
>
> ![[xor-half-adder.svg]]
> *图 3 — 半加器原理图（脚本重画）：$A$、$B$ 各分两路（实心圆点是分叉节点），
> 上路进 XOR 得 Sum $=A\oplus B$，下路进 AND 得 Carry $=A\cdot B$；两个门的标注都是英文。*
>
> ![[ch3-xor-adder.png]]
> *图 4 — 讲义 p.11 原图："An XOR gate can be used to add two bits" —— 与本篇图 3 是同一个半加器结构
> （XOR 给 Sum 位，AND 给进位），对照看可以确认图的连线和本节表格说的是同一件事。*
>
> **XOR as difference and controlled inversion · 差异检测与受控取反**
>
> XOR reports a bit difference. Applied position by position, it forms a difference mask for two words: a one marks a position where they differ. OR-reducing that mask reports whether any difference exists; XOR-reducing it reports only the parity of the number of differences. Those reductions answer different questions.
>
> XOR also acts as a controlled inverter. In $Y=A\oplus C$, control $C=0$ passes A and $C=1$ complements A. This mechanism lets an adder invert every bit of B during subtraction while using the same control as the initial carry-in.
>
> **Worked application — conditional complement.** B=`0110`，减法控制 M=1，每位 $B_i\oplus M$ 得 `1001`，carry-in=M=1，因此相当于加 `1010`（4 位中 −6）。若 A=`1001` 按无符号读为 9，则 $9-6=3$，`1001+1001+0001=1 0011`，低 4 位=`0011`，carry=1 表示无 borrow。
>
> In English: the XOR gates invert the subtrahend conditionally, and the initial carry supplies the missing one in two's-complement negation. Setting M to zero restores ordinary addition without changing the datapath wiring.
>
> **English exam question:** Is a three-input XOR HIGH only when exactly one input is HIGH?
>
> **Answer:** No. It is HIGH when an odd number of inputs is HIGH, so both one HIGH input and three HIGH inputs produce 1. “Exactly one” requires a different three-variable Boolean function.
>
> Continue with [[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路|Binary Subtractors and Adder-Subtractors]], [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]], [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]], and [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|Cyclic Redundancy Check]]. The last two use XOR without integer carries, unlike the sum-and-carry arithmetic model.
>
> **Ch5 Application · 第五章门级应用**
>
> 课件 Ch5 p.8 以与或结构实现 $X=A\bar B+\bar AB$，p.11–14 则将 XOR 级联用于偶校验。**奇数性指示 (odd-parity indication)** 与**偶校验位发生器 (even-parity-bit generator)** 使用相同的 XOR 函数：前者描述原始数据，后者把结果作为新增位，使完整码字中 1 的总数为偶数。完整发生器与检查器见 [[Parity and Cyclic Redundancy Checks#2 · 门级发生器、检查器与错误边界|Parity Bit]]。
>
> This distinction also explains why a four-input XOR cannot detect “exactly three inputs are 1”: it additionally asserts for exactly one input. Compare [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]] and [[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构|AND-OR and AND-OR-Invert Logic]].
>
> 来源：Tinghuan CHEN, *ECE2050 Chapter 5: Combinational Logic Design*, PDF p.8、11–14；[第五章课件](../ECE2050-Chap5.pdf#page=8)。

> [!example]- Exclusive-NOR Gate · 推导与例题
> **图示与讲义依据**
>
> ![[xnor-gate-timing.svg]]
> *图 1 — $A$（周期 4）、$B$（周期 2）与 $Y=\overline{A\oplus B}$ 的时序图；虚线是 XOR 的输出 $A\oplus B$（灰），
> 实线是 XNOR。每格顶部标出输入比较结果 `=`（相同，红）或 `≠`（不同，灰）；灰底格子是"相同"的四格
> （第 1、4、5、8 格），$Y$ 在那里为 1 —— 与真值表的 "相同 → 1" 一致，也说明两条输出波形处处互补。*
>
> **Derivation · 推导过程**
>
> **① 从 XOR 接一个反相器**
>
> 把 XOR 的输出 $X=A\oplus B$ 取反：
>
> $$Y=\overline{A\oplus B}$$
>
> - 意义：XNOR 同样是"复合门"——符号上的输出气泡就是那个反相器。
> - 数值校验（取 $A=1,B=1$）：$X=1\oplus1=0\Rightarrow Y=\bar0=1$ ✓（真值表第 4 行）；
>   取 $A=0,B=1$：$X=1\Rightarrow Y=0$ ✓（第 2 行）。
>
> **② 从"相同为 1"直接写 SOP**
>
> 输出为 1 的行是 $(A,B)=(0,0)$ 与 $(1,1)$：取值为 1 的变量写原变量、取值为 0 的写反变量，再 OR：
>
> $$Y=\underbrace{\bar A\bar B}_{(0,0)\text{ 行}}+\underbrace{AB}_{(1,1)\text{ 行}}$$
>
> - 意义：与 XOR 的写法完全对称，只是把两个**交叉项**换成了两个**同号项**（链 [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]]）。
> - 数值校验（取 $A=0,B=0$）：$\bar A\bar B=1\Rightarrow Y=1$ ✓；取 $A=0,B=1$：$\bar A\bar B=0$、$AB=0\Rightarrow Y=0$ ✓。
> - 全表核验（Python 复核 4 行）：$AB+\bar A\bar B$ 与"两个输入相同"完全一致 ✓。
>
> **③ 代数证明：$\overline{A\bar B+\bar AB}=AB+\bar A\bar B$**
>
> 从 XOR 的 SOP 形式出发，用德摩根定理与分配律化到 XNOR 的 SOP 形式：
>
> $$
> \overline{A\bar B+\bar AB}
> =\overline{A\bar B}\cdot\overline{\bar AB}
> =(\bar A+B)(A+\bar B)
> =\underbrace{\bar AA}_{0}+\bar A\bar B+BA+\underbrace{B\bar B}_{0}
> =AB+\bar A\bar B
> $$
>
> - 意义：第一、二条等号都是德摩根（和取反 = 各项取反后相乘；乘积项取反 = 各变量取反后相加，
>   [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]），第三条用分配律展开（[[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则|Laws and Rules of Boolean Algebra]]）；
>   中间出现的 $\bar AA$ 与 $B\bar B$ 恒为 0 被丢掉。
> - 数值校验（取 $A=1,B=0$）：左式 $=\overline{A\bar B+\bar AB}=\overline{1\cdot1+0\cdot0}=\overline{1}=0$；
>   右式 $=AB+\bar A\bar B=1\cdot0+0\cdot1=0$ ✓（两式相等）。
> - 再取 $A=1,B=1$：左式 $=\overline{1\cdot0+0\cdot1}=\overline{0}=1$；右式 $=1\cdot1+0\cdot0=1$ ✓。
> - 四行全部核验（Python 逐行比对）：$\overline{A\bar B+\bar AB}$ 与 $AB+\bar A\bar B$ 在 4 行上完全相等 ✓。
>
> **④ 多输入：偶数个 1 → 1**
>
> $$Y=\overline{A\oplus B\oplus C}=\sum m(0,3,5,6)$$
>
> - 意义：四种"偶数个 1"的行 $(000,011,101,110)$ 输出 1 —— 这就是**偶数性指示 (even-parity indication)** 函数，
>   与 [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]] 的"奇数个 1"恰好互补（链 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]]）。
> - 数值校验：$A=B=C=1$ 时 1 的个数为 3（奇）→ $Y=0$ ✓；$A=B=C=0$ 时为 0（偶）→ $Y=1$ ✓；
>   把讲义 p.13 的 XOR3 列 `0,1,1,0,1,0,0,1` 逐位取反得 `1,0,0,1,0,1,1,0`，正是本式的 8 行结果 ✓。
>
> **⑤ 应用：相等检测器（equality detector）**
>
> 两个 $n$ 位二进制数 $A=A_{n-1}\cdots A_0$ 与 $B=B_{n-1}\cdots B_0$ 相等，当且仅当**每一位都相同**：
>
> $$E=(A_{n-1}\odot B_{n-1})\cdot(A_{n-2}\odot B_{n-2})\cdots(A_0\odot B_0)$$
>
> - 意义：每一位用 XNOR 给出"这一位相同"（1 = 相同），再把所有位**相与**（AND）—— 任一位不同，$E$ 立刻为 0。
>   等价写法：$E=\overline{(A_{n-1}\oplus B_{n-1})+\cdots+(A_0\oplus B_0)}$（各取 XOR 后 OR 起来再取反）。
> - 数值校验（2 位，$A=10_2$、$B=10_2$）：$A_1\odot B_1=1\odot1=1$、$A_0\odot B_0=0\odot0=1$，$E=1\cdot1=1$ ✓（相等）。
>   换成 $B=11_2$：$1\odot1=1$、$0\odot1=0$，$E=1\cdot0=0$ ✓（不相等）。
> - 位数校验：$n$ 位比较需要 $n$ 个 XNOR + $(n-1)$ 个 AND；用等价写法则是 $n$ 个 XOR + 1 个 NOR
>   （NOR 就是 OR 之后取反，直接给出 $E$）。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.10 的 XNOR 表逐行核对（含 p.25 的 T/F 陷阱题）**
>
> 题目：(a) 逐行核对讲义 p.10 的 XNOR 真值表；(b) 判断讲义 p.25 Quiz 的说法
> "The output of an exclusive-OR is 0 if the inputs are opposite" 是否正确。
>
> | $A$ | $B$ | XOR | XNOR（p.10 原表） | 我的核验：$AB+\bar A\bar B$ |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 1 | $0+1\cdot1=1$ ✓ |
> | 0 | 1 | 1 | 0 | $0+0\cdot0=0$ ✓ |
> | 1 | 0 | 1 | 0 | $0+1\cdot0=0$ ✓ |
> | 1 | 1 | 0 | 1 | $1\cdot1+0=1$ ✓ |
>
> 解 (b)：**False**。XOR 的判据是"输入**不同** → 1"，所以输入相反（一个 0 一个 1）时 XOR 输出是 **1** 而不是 0；
> 输出 0 的是"输入相同"的两行。把这句话里的 XOR 换成 XNOR 就对了（XNOR 在输入相反时为 0）。
>
> **数值校验 (Numerical check)**：XNOR 列 `1,0,0,1` 与 XOR 列 `0,1,1,0` 逐位互补（相加恒为 1）✓；
> (b) 用第 2 行检验：$A=0,B=1$（相反）时 XOR $=1$ ✓，所以原说法被这一行直接推翻 ✓；
> 若改成"XNOR 在输入相反时输出 0"，则第 2、3 行都给出 0 ✓，说法成立。
>
> ![[ch3-xor-xnor.png]]
> *图 2 — 讲义 p.10 原图：左半是 XOR、右半是 XNOR 的符号、表达式与真值表，底部是两者的时序图。
> 右半的表达式就是本篇的 $\overline{A\oplus B}$；请注意 XNOR 符号比 XOR 多出的那个输出气泡，
> 以及底部两条波形处处互补。*
>
> **Example 2 — 两位相等检测器（自算，配合 ⑤ 的公式）**
>
> 题目：用 XNOR 与 AND 比较两个 2 位数 $A=A_1A_0$ 与 $B=B_1B_0$，给出 $E=1$ 的条件，并验证
> $A=10_2$ 分别与 $B=10_2$、$B=01_2$、$B=11_2$ 比较的结果。
>
> 解：$E=(A_1\odot B_1)(A_0\odot B_0)$，逐位算 XNOR 再相与：
>
> | $A$ | $B$ | $A_1\odot B_1$ | $A_0\odot B_0$ | $E$ | 是否相等 |
> |---|---|---|---|---|---|
> | 10 | 10 | $1\odot1=1$ | $0\odot0=1$ | 1 | 相等 |
> | 10 | 01 | $1\odot0=0$ | $0\odot1=0$ | 0 | 不等 |
> | 10 | 11 | $1\odot1=1$ | $0\odot1=0$ | 0 | 不等 |
> | 10 | 00 | $1\odot0=0$ | $0\odot0=1$ | 0 | 不等 |
>
> **数值校验 (Numerical check)**：$10_2=2$，只有第 1 行满足 $A=B$ ✓；
> 用等价写法复核第 3 行：$(A_1\oplus B_1)+(A_0\oplus B_0)=0+1=1$，取反得 $E=0$ ✓（与表一致）；
> Python 穷举 $A,B\in\{0,1,2,3\}$ 的全部 16 对：$E=1$ 恰好出现在 $A=B$ 的 4 对上，其余 12 对为 0 ✓。
>
> **Example 3 — 三输入 XNOR3：偶数个 1 输出 1（由讲义 p.13 的 XOR3 表取反）**
>
> 题目：讲义 p.13 右表是三输入 XOR（奇数个 1 输出 1，$Y$ 列 `0,1,1,0,1,0,0,1`）。
> 求三输入 XNOR3 的真值表。
>
> | $A$ | $B$ | $C$ | 1 的个数 | XOR3（p.13 原表） | XNOR3 $=\overline{A\oplus B\oplus C}$ |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0（偶） | 0 | **1** |
> | 0 | 0 | 1 | 1（奇） | 1 | 0 |
> | 0 | 1 | 0 | 1（奇） | 1 | 0 |
> | 0 | 1 | 1 | 2（偶） | 0 | **1** |
> | 1 | 0 | 0 | 1（奇） | 1 | 0 |
> | 1 | 0 | 1 | 2（偶） | 0 | **1** |
> | 1 | 1 | 0 | 2（偶） | 0 | **1** |
> | 1 | 1 | 1 | 3（奇） | 1 | 0 |
>
> **数值校验 (Numerical check)**：XNOR3 的 $Y$ 列 `1,0,0,1,0,1,1,0` 正是 XOR3 列的逐位取反 ✓；
> $Y=1$ 的行数为 4 $=C_3^0+C_3^2=1+3$（偶数个 1 的组合数）✓；
> 用 Python 逐行复核 $\lnot\left(\left(\sum\text{bits}\right)\bmod2\right)$ 的 8 行全部一致 ✓；
> 注意第 8 行 $111$：三个输入**彼此相同**，但 1 的个数是 3（奇），所以 XNOR3 输出 **0** ——
> 这就是"多输入不能再说'相同为 1'"的原因 ✓。
>
> **Equality versus parity reduction · 相等与偶数重归约**
>
> Two-input XNOR is a bit equality test. Word equality requires all corresponding bit comparisons to be TRUE, so an AND of bitwise XNOR results is appropriate. A multi-input XNOR defined as the complement of a multi-input XOR instead reports an even number of ones; it is not a test that all inputs are identical.
>
> Be careful when constructing a multi-input function from two-input XNOR gates. $(A\odot B)\odot C=A\oplus B\oplus C$, because the two internal complements cancel. This is not $\overline{A\oplus B\oplus C}$. A symbol labeled XNOR3 must be interpreted according to its defined truth table rather than assumed equivalent to an arbitrary cascade.
>
> **Worked application — compare words.** A=`1010`，B=`1001`。逐位 XNOR 得 `1100`，AND-reduction=0，故不相等。若误用 XOR-reduction of the difference mask，A XOR B=`0011`，两个 1 的 parity=0，可能错误认为“没有差异”。正确不等检测是 OR-reduction=`1`。
>
> In English: equality requires zero differences, not an even number of differences. Reduction operators must match the intended word-level predicate.
>
> **English exam question:** What is $(0\odot0)\odot0$, and what is a three-input even-parity XNOR on 000?
>
> **Answer:** The cascade gives $1\odot0=0$. The complemented three-input XOR gives $\overline{0}=1$. They are different circuits, despite both being informally described with the word XNOR.
>
> Follow [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] for complete equality, greater-than, and less-than functions. In [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]], an even-parity **generator** uses XOR of data; an even-parity **checker** can complement the XOR of the full received word. Distinguish generation from checking.
>
> **Ch5 Application · 第五章等价结构与校验边界**
>
> 课件 Ch5 p.9 比较 XOR 后接 NOT 与同号乘积项相或两种实现：
>
> $$
> X=\overline{A\bar B+\bar AB}=(\bar A+B)(A+\bar B)=\bar A\bar B+AB.
> $$
>
> 两输入同或 (two-input XNOR) 可识别相等；多输入的偶数性指示 (even-parity indication) 应明确写成 $\overline{d_1\oplus\cdots\oplus d_n}$。它输出 1 表示数据中有偶数个 1；作为**新增校验位**使用时，它生成的是奇校验位。偶校验位本身使用 XOR，见 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]]。
>
> Do not assume that cascading binary XNOR gates always computes the complement of the full XOR reduction. Each binary XNOR introduces one complement: a chain over n inputs has n−1 complements. For three inputs, two XNOR stages yield $A\oplus B\oplus C$, rather than its complement. Use an XOR tree followed by one final inversion when an even-parity indication is required.
>
> 来源：Tinghuan CHEN, *ECE2050 Chapter 5: Combinational Logic Design*, PDF p.9；[第五章课件](../ECE2050-Chap5.pdf#page=9)。多输入级联边界为由二输入定义推导的补充。

## 5 · 从真值表到波形与应用

在每个输入稳定区间查表，传播延迟只移动响应边沿。AND 用于许可与门控；OR 合并事件；XOR 用于受控反相、奇偶校验；XNOR 后再 AND 可比较整个字。静态功能正确后，还应检查毛刺与采样时序。

## Sources · 课件依据

主线课件：[Ch3 lecture](../ECE2050-Chap3.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
