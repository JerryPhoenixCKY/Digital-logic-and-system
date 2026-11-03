---
tags:
  - ECE2050
  - counters
date: 2026-09-30
updated: 2026-10-09
chapter: Ch10
aliases:
  - 计数器设计与数字时钟
  - Counter Design and Digital Clocks
  - 计数器设计与数字时钟 · Ch10
  - Counters
  - 计数器
  - Binary and decade counters
  - Synchronous Counter Design
  - 同步计数器设计
  - Counter excitation synthesis
  - Cascaded Counters and Digital Clocks
  - 级联计数器与数字时钟
  - Terminal count and frequency division
---

# Counter Design and Digital Clocks · 计数器设计与数字时钟

> [!SUMMARY] Quick recall · 英文速览
> A counter is a specified state sequence. Derive next state from old state, recover from invalid states, and enable higher digits on accepted rollover.

## 1 · Counters · 模数与时钟结构

计数器 (counter) 循环经过 M 个不同状态，模数 (modulus) 是状态数量，不一定等于最大显示数字加 1。异步纹波计数器由前级输出触发后级；同步计数器共享时钟，靠激励逻辑决定更新。

### Core Definition · 核心定义

计数器 (counter) 是有指定状态序列的 [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]]。n 位 binary counter 的完整计数范围 0–$2^n-1$，modulus=$2^n$。十进制 BCD decade counter 走 0–9，modulus=10，需要 4 位但不是 mod16。

$$q^+=\begin{cases}(q+1)\bmod M,&\text{up}\\(q-1)\bmod M,&\text{down}.\end{cases}$$

此整数式定义规则计数，不描述不规则序列的通用 next-state logic。q 是编码/整数值；M 是完整循环的状态数。

> [!example]- Counters · 推导与例题
> **Asynchronous versus Synchronous · 异步与同步**
>
> 异步 ripple counter：只有第一级直接由外部 clock 驱动，后级用前级输出边沿驱动；变化逐级 ripple。同步 counter：所有 FF 使用同一 clock，组合条件决定某一位是否翻转。
>
> | Feature | Ripple counter | Synchronous counter |
> |---|---|---|
> | Clock inputs | Cascade from preceding stages | Common clock |
> | Intermediate transition codes | Often significant | Still possible from clock-to-Q mismatch |
> | Delay model | Can accumulate through stages | Clock-to-Q plus control/decode logic |
> | Typical design analysis | Check edge polarity and Q/NOT Q connections | Derive all next states from old state |
>
> “Synchronous” does not imply zero physical delay or glitch-free decoding. It describes the clock relationship. Enable and load behavior can also differ from chip to chip.
>
> **Worked Examples · 例题**
>
> **3-bit up.** 011→100：旧低位 Q0=Q1=1，所以 T0=T1=T2=1，三位都翻转。100→101 时低位旧 Q0=0，只有 T0=1，其余为 0。
>
> **Ripple delay.** n=4、每级 clock-to-Q worst case=8 ns，在需贯穿所有级的 rollover 事件中，最终状态可在 32 ns 后才到达。哪些转换会达到该延迟，取决于各级触发边沿与 Q/NOT Q 接法；普通对应 up ripple 模型中的 0111→1000、1111→0000 会贯穿四级。
>
> **Frequency.** 完整 binary ripple counter 的 bit i 输出重复频率为 $f_{clk}/2^{i+1}$，50% duty 在完整稳态周期中成立。mod3 的 decode pulse 可每三拍重复，但 duty 可能为 1/3，不是自动 50%。

### Method and Exam English · 方法与答题

1. Determine intended state sequence and initial state.
2. Identify synchronous versus ripple clocks.
3. Write each FF input and active edge.
4. Compute next states, including control priority.
5. Count the distinct states before the first repeated state.

**Exam answer:** “The modulus is the length of the repeating state cycle reached from the specified initial state. Although four flip-flops can represent sixteen codes, this decade counter uses only ten of them.”

### Connections · 概念关系与应用

[[Sequential Logic and Flip-Flops#4 · JK and T Flip-Flops · 条件更新|JK and T Flip-Flops]] 给出 toggle 元件，[[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励|Synchronous Counter Design]] 从状态表求激励；[[Shift Registers and Ring Counters#3 · Ring and Johnson Counters · 同样的移位，不同的反馈|Ring and Johnson Counters]] 是另一类循环状态编码，[[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转|Cascaded Counters and Digital Clocks]] 按 rollover 扩展；decode 的瞬态由 [[Propagation Delay and Logic Hazards]] 分析。

## 2 · Synchronous Counter Design · 从转换表求激励

二进制向上计数的 $T_i=E\prod_{j<i}Q_j$，最低位空乘积为 1。D 触发器直接取下一态方程；JK 按激励表求 J/K，不能把 J 简单当成下一态。

模 3 例：00→01→10→00，若规定 11→00 恢复，则 $D_1=\bar Q_1Q_0,D_0=\bar Q_1\bar Q_0$。指定非顺序计数应按给定序列逐行列下一态。

### Design Method · 设计方法

状态图 → next-state table → excitation table → K-map → input equations → implementation → 全状态核对。DFF 的激励直接为 $D_i=Q_i^+$；TFF 为 $T_i=Q_i\oplus Q_i^+$；JK 用逐位 transition table。

不要把 current state 和 next state 的 bit 列混在一起；所有输入函数以 current Q 与控制输入表示。题目要求 DFF 时最终 equations 要给 D，而不是仅列 J/K。

### JK Design · JK 设计细节

例如 000→101：bit2 为 0→1，所以 J2=1,K2=X；bit1 0→0 所以 J1=0,K1=X；bit0 0→1 所以 J0=1,K0=X。所有行分别填表，然后每个 J/K 变量各自画 K-map。

A valid but not always minimal JK implementation is $J_i=Q_i^+$ and $K_i=\overline{Q_i^+}$. The excitation-table don't-cares can produce a smaller circuit because each input matters only for one current-state value.

> [!example]- Counters · 推导与例题
> **Derivation · 同步二进制翻转条件**
>
> up counter 的 bit0 每拍翻转；bit1 在旧 bit0=1 时翻转；biti 在全部较低位都是 1 时翻转。因此：
>
> $$T_0=1,\qquad T_i=\prod_{j=0}^{i-1}Q_j\quad(i\ge1),\qquad Q_i^+=Q_i\oplus T_i.$$
>
> down counter 把条件改为较低位全 0：$T_i=\prod_{j=0}^{i-1}\bar Q_j$。可用 JK with J=K=T 实现。

> [!example]- Synchronous Counter Design · 推导与例题
>
> **Worked Example 1 · Modulo-3 with recovery**
>
> 设状态 00→01→10→00；unused 11→00，初态 00。
>
> | Current | Next | D1 | D0 | Pulse P |
> |---|---|---|---|---|
> | 00 | 01 | 0 | 1 | 0 |
> | 01 | 10 | 1 | 0 | 0 |
> | 10 | 00 | 0 | 0 | 1 |
> | 11 | 00 | 0 | 0 | 0 |
>
> $$D_1=\bar Q_1Q_0,\quad D_0=\bar Q_1\bar Q_0,\quad P=Q_1\bar Q_0.$$
>
> P 每三拍重复一次，frequency=$f_{clk}/3$，HIGH 一拍所以 duty=1/3。两位状态不意味着随便挑一位就能得到相同 duty 的波形；若要求 50% divide-by-3 输出，仅正沿更新的简单三态 decode 不能每 1.5 周期改变一次。
>
> **Worked Example 2 · 指定非顺序计数**
>
> 要求 0→5→1→2→7→6→3→4→0，使用三个 FF。按 Q2Q1Q0 排列：
>
> | Current decimal | Current bits | Next bits |
> |---|---|---|
> | 0 | 000 | 101 |
> | 1 | 001 | 010 |
> | 2 | 010 | 111 |
> | 3 | 011 | 100 |
> | 4 | 100 | 000 |
> | 5 | 101 | 001 |
> | 6 | 110 | 011 |
> | 7 | 111 | 110 |
>
> 使用 DFF 可得到一组简洁式：
>
> $$D_2=\bar Q_2\bar Q_0+Q_1Q_0,$$
> $$D_1=\bar Q_2\bar Q_1Q_0+Q_1\bar Q_0+Q_2Q_1,$$
> $$D_0=Q_2\bar Q_1Q_0+\bar Q_2\bar Q_0+Q_1\bar Q_0.$$
>
> 由每位 next=1 的 minterms 配对而来。也可保留 canonical D equations 完成验证，再改用 JK 激励化简；D 方案与 JK 方案都是同一行为的不同实现。
>
> **Verification and Review · 验证与复习**
>
> Check every state, not only a few clock pulses. Confirm cycle length, absence of unintended branches, reset entry, and unused-state behavior. For an up/down counter, include both direction values for each state.
>
> **Exam question:** Why does a simplified JK expression sometimes omit the current bit itself?
>
> **Answer:** When Q=0, K is irrelevant; when Q=1, J is irrelevant. These excitation don't-cares can eliminate literals while preserving the desired next state through the JK characteristic equation.

### Connections · 概念关系与应用

先由 [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] 确定序列，按 [[Sequential Logic and Flip-Flops#4 · JK and T Flip-Flops · 条件更新|JK and T Flip-Flops]] 查激励，再用 [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并|Karnaugh Map]] 化简；[[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]] 定义恢复。它是 [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]] 设计的一种，最终全状态检查见 [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]]。

## 3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转

十进制级联中，高位使能为 $E_H=E_L\cdot TC_L$，其中 TC 指低位处于末态；两级在同一时钟读旧状态并更新。只解码“末态”而不与允许计数的 E 相与，会在暂停时误触发高位。

### Core Definition · 核心定义

低位 modulus $M_0$、高位 $M_1$，每低位完整循环让高位加一，则总 modulus=$M_0M_1$。推广到 k 级为 $\prod_iM_i$，前提是正确的 wrap/enable/load 行为。

Terminal count (TC) 指定最后有效状态的 decode；carry/rollover event 表示本次 clock 接受后会 wrap 的条件。两者不一定相同：禁用计数时 TC 可一直 HIGH，但不应让高位每拍都增加。

> [!example]- Cascaded Counters and Digital Clocks · 推导与例题
> **Derivation · 同步级联**
>
> 最低位 enable E0=global enable。高一级 $E_1=E_0\land(q_0=M_0-1)$；再一级 $E_2=E_1\land(q_1=M_1-1)$。所有 q 都从 edge 前状态读取。
>
> For a synchronous load-on-terminal scheme, decode the last legal state M−1 so the next edge loads zero. Decoding M and then synchronously clearing on a later edge can introduce an extra state and change the modulus. Asynchronous clear-on-M uses a different timing model and may create short transient states.
>
> **Worked Example 1 · 两级十进制**
>
> 个位、十位各 mod10，组成 mod100。当前 09、E=1：个位 9→0、十位 0→1，同时变 10。当前 99：两位均 wrap 到 00。当前 09、E=0：保持 09，TC 虽为 1，但不产生接受事件。
>
> 若 input=10 kHz，个位 cycle=1 kHz，总 100-state cycle=100 Hz。两个 decade 级联是 divide-by-100，不是 divide-by-10。
>
> **Practical Timing · 实际时序**
>
> Decode glitches can falsely trigger a higher stage if used as a clock. A common-clock enable chain lets receiving FFs sample a condition under setup/hold constraints, although the enable path still contributes to critical timing.
>
> For an odd modulus, a terminal decode pulse has one-cycle width and duty 1/M. The output repetition frequency is $f_{clk}/M$; pulse width and 50% square-wave requirements are separate specifications.

### Method and Exam English · 方法与答题

- Define each stage's legal range, reset value, and wrap event.
- Connect a higher enable to the accepted lower rollover, not just a static display value.
- 在“59→00”与“禁用时末态保持”两种边界上验证。

**Answer pattern:** “All stages use the same clock. The next stage is enabled only when the lower stage is enabled and currently at its terminal count. The combined modulus is the product of the individual legal cycle lengths.”

### Connections · 概念关系与应用

[[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] 定义各级模数，[[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]] 定义接受条件与优先级；[[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 产生 terminal predicate，供 [[Finite State Machine Design and Applications#5 · Traffic Light Controller · 安全条件进入状态模型|Traffic Light Controller]] 等定时应用。不要把 [[Propagation Delay and Logic Hazards]] 中的 decode 毛刺当 clock；异常进位可按 [[Digital Logic Troubleshooting]] 追踪。

## 4 · 混合进制与预置截断

秒／分的 59→00 同时令上一级增加；个位模 10、十位模 6，满量程为 60 状态。预置计数要数实际经过的状态，并说明端点是否包含；分频输出的频率与高电平占空比也分别计算。

> [!IMPORTANT] 初态与控制优先级进入验证
> 检查使能关闭、装载、复位、末态、非法态与级联进位；不能只测试连续加 1。

> [!example]- Counters · 推导与例题
> **Control Inputs · 控制输入**
>
> Clear、load、enable、direction 与 terminal-count 控制应由 function table 指定。若同步 load LOW 优先于 count enable，则 LOAD=0 时即使 count disabled 也会在下一边沿加载；若器件另有条件，不得移植该假设。
>
> For a modulo-10 down counter, 0000 decrements to 1001, not to 1111. For a full four-bit binary down counter, 0000 goes to 1111. The word “decade” changes the sequence.

> [!example]- Cascaded Counters and Digital Clocks · 推导与例题
> **Worked Example 2 · 60进制时钟**
>
> seconds 0–59、minutes 0–59；当前 12:59:59，下一次 1 Hz tick 应得 13:00:00。更新前 seconds TC 与 minutes TC 同时为 1，因此小时 enable 在同一拍有效。
>
> One possible two-digit seconds implementation uses units 0–9 and tens 0–5. Units rollover enables tens; tens rollover at 5 only matters when units also roll at 9. Decoding tens=5 alone would repeatedly advance minutes while displaying 50–59.
>
> 教学 12-hour 系统若用 1–12，12 后应加载 1；若编码 0–11，解码显示与 roll 条件需另外定义。不能把两个约定的 terminal state 混用。
>
> **Worked Example 3 · Preset truncated count**
>
> 16-bit full binary cycle 长度 65536。要求 modulus 40000，可从 preset P=65536−40000=25536=0x63C0 开始，数到 65535 后下一事件加载 P。
>
> Number of visited states is $65535-25536+1=40000$. The +1 includes both endpoints. Check the loading event does not add an unintended separate waiting state; the scheme's count-enable and load semantics determine the actual cycle.

## Sources · 课件依据

主线课件：[Ch10 lecture](../LGU_HUB_ECE2050/ECE2050-Chap10.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
