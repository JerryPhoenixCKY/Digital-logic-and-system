---
tags:
  - ECE2050
  - review
date: 2026-09-30
updated: 2026-10-27
chapter: Review
aliases:
  - 考试复习与解题方法
  - Exam Review and Problem Solving
  - 考试复习与解题方法 · Review
  - Digital logic exam review
---

# Exam Review and Problem Solving · 考试复习与解题方法

> [!SUMMARY] Quick recall · 英文速览
> Read the specification, choose the model, derive independently, and test the boundaries. A familiar-looking answer is not evidence of correctness.

> [!IMPORTANT] Midterm Ch1–6 · 本次期中入口
> 按当前课件整理的 [[Midterm Review Guide]] 覆盖六章原理与明确考试范围，配套 [[Midterm Formula Sheet]] 和 [[Midterm Practice and Answers]]。本篇继续保留全学期综合方法；Ch7 以后的详细设计不并入本次期中主线。

## 1 · 用先修链组织复习

数制与表示→逻辑门与接口→布尔形式与化简→组合功能块→存储与时序→状态机／计数器→存储／HDL。先闭卷写 governing equation，再做典型例题，最后检查条件和反例。

### Deliverables · 复习目标与题目交付物

这篇是复习导航与解题模板，不替代各概念的详细推导。数字逻辑题通常要求完成一条可验证的链：**文字规范 → 数学/状态模型 → 电路或代码 → 功能与时序检查**。

An answer should state what the circuit means before showing how it is built. “Simplify,” “canonical,” “implement,” “trace,” and “design” request different deliverables; a correct simplified expression can still be the wrong answer to a canonical-form question.

> [!example]- Exam Review and Problem Solving · 推导与例题
> **Learning Path · 按先修关系复习**
>
> | Stage | Prerequisite → next topic | Exit question · 自查问题 |
> |---|---|---|
> | 1. Representation | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] → [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] → [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] | Can I explain the value of these bits at this width? |
> | 2. Boolean meaning | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型\|Logic Gates]] → [[Boolean Forms and Algebraic Simplification#2 · Truth Table and Boolean Expression · 用真值表定义全集\|Truth Table and Boolean Expression]] → [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项\|Minterm and Maxterm]] | Can I identify exactly which rows produce 1/0? |
> | 3. Simplification | [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则\|Laws and Rules of Boolean Algebra]] → [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并\|Karnaugh Map]] → [[Karnaugh Map Minimization#3 · POS Minimization with Karnaugh Map · 圈 0 读和项\|POS Minimization with Karnaugh Map]] | Is the result equivalent on every required row? |
> | 4. Building blocks | [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门\|Combinational Logic Design]] → [[Comparison Decoding and Selection#2 · Decoder · 代码变线路\|Decoder]] / [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配\|Multiplexer and Demultiplexer]] / [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒\|Half Adder and Full Adder]] | Can I connect all inputs with correct polarity? |
> | 5. Stored state | [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在\|Sequential Logic]] → [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿\|D Latch and D Flip-Flop]] → [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级\|Register Enable and Reset]] → [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式\|Shift Registers]] | Which values are sampled, held, or updated? |
> | 6. State design | [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史\|Finite State Machine]] → [[Finite State Machine Design and Applications#2 · Moore and Mealy Machines · 输出依赖与时间对齐\|Moore and Mealy Machines]] → [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复\|State Encoding and Unused States]] | Does every state/input pair have a defined transition? |
> | 7. System use | [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构\|Counters]] → [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量\|Memory Arrays and Expansion]] / [[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积\|Read-Only Memory and Programmable Logic Arrays]] → [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现\|VHDL Language and Modeling]] | Can I connect function, state, storage, and implementation? |
>
> 先补最早断开的依赖，不要直接背后续式子。看不懂 counter 激励表时，先回 [[Sequential Logic and Flip-Flops#4 · JK and T Flip-Flops · 条件更新|JK and T Flip-Flops]]；看不懂 ROM 地址宽度时，先回 [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|Bits and Bytes]] 与 [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|Binary Number System]]。
>
> For each topic, practice four passes: explain it in one English sentence, derive one result in Chinese, solve a small example without notes, and check the answer using another representation. Review the resulting error pattern rather than rereading every page equally.

## 2 · 读题先标六项约束

变量顺序、位宽、signed／unsigned、有效极性、有效边沿／初态、exactly／at least 与 invalid-state 策略。并行字匹配与串行序列识别需不同模型；复位并不自动发生在上电。

> [!example]- Exam Review and Problem Solving · 推导与例题
> **Read the Question · 先把题意变成约束**
>
> 在草稿第一行记录六项：**representation / width / bit order / polarity / clock edge / initial state**。不适用的项目写“combinational”或“unsigned”，不要留下可能改变答案的空白。
>
> Words such as **exactly**, **at least**, **highest priority**, **overlapping**, **synchronous**, and **asynchronous** change the model. Underline them and translate them into a table or equation before drawing gates.
>
> “至少两个为 1”在三输入时是 $AB+AC+BC$，包含 111；“恰好两个为 1”是 $AB\overline C+A\overline BC+\overline ABC$，不包含 111。先列边界反例能防止把两种要求混同。

## 3 · 数制、算术与表示

转换用位权复核；补码先算数学结果再检查范围；定点明确缩放；浮点先分类特殊码。carry、borrow、signed overflow 和 rounding 分别解释。

> [!example]- Exam Review and Problem Solving · 推导与例题
> **Number Problems · 数制与算术题**
>
> 1. 确定位串是 unsigned、two's complement、sign magnitude、BCD 还是浮点；同一位串可能有不同值。
> 2. 对 signed arithmetic 先写十进制预期符号与大致大小，再按固定宽度计算。扩位时 two's complement 要 sign extension。
> 3. 区分 carry 与 signed overflow。负数加正数不会因最终 carry=1 就自动 overflow。
> 4. Binary↔octal/hex grouping begins at the binary point. Pad zeros only at the outside ends; never move the point.
> 5. For [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|Cyclic Redundancy Check]], divide with XOR, append degree-many zeros, and transmit exactly degree-many remainder bits.
>
> **Mini-example — signed multiplication.** 4 位 two's complement `1011`=-5、`1101`=-3，乘积 +15。若要求完整 8 位结果，应写 `00001111`；`1111` 在 4 位 signed 模型下是 -1。数学值正确仍需满足输出宽度。
>
> **Mini-example — fractional grouping.** `10.101101₂`：向三位分组得 `010.101 101`，故 $2.55_8$；向四位分组得 `0010.1011 0100`，故 $2.B4_{16}$。二者都等于 $2+45/64=2.703125$。

## 4 · 布尔与组合设计

先列 ON／OFF／don't-care，再给分组、方程与实现；核对输出极性与额外反相器。最小表达式不保证无冒险。优先输出先判断是独热掩码还是紧凑代码。

> [!example]- Exam Review and Problem Solving · 推导与例题
> **Boolean Forms and K-maps · 标准式与卡诺图**
>
> Canonical SOP lists minterms for every 1 row; canonical POS lists maxterms for every 0 row. Each canonical term contains every variable once. A simplified SOP/POS need not contain every variable in each term.
>
> 对变量顺序 ABC，$F=AB+C$ 在编号 1,3,5,6,7 为 1，所以：
>
> $$F=\Sigma m(1,3,5,6,7)=\Pi M(0,2,4).$$
>
> 若要求完整 standard POS，应展开为 $(A+B+C)(A+\overline B+C)(\overline A+B+C)$。最简 POS $(A+C)(B+C)$ 与它等价，但不是 canonical POS。
>
> K-map procedure: label axes in Gray-code order; fill cells from the specification; group 1s for SOP or 0s for POS; use power-of-two rectangular groups and wraparound adjacency; remove changing variables; check all required cells afterward.
>
> Don't cares 可以选用，也可以不选；组必须帮助覆盖 required 1/0，不能单独圈一组 X 当成必需项。规范要求 unused states recover 时，不能把其 next-state rows 全部丢成 X。
>
> A quick consistency check uses the original truth table, not the drawing alone. For $F=AB+C$, C=1 must produce F=1 for all A/B, and C=0 must reduce to AB. These two cofactors catch many misplaced K-map groups.
>
> **Gate and Block Implementation · 门与功能块实现**
>
> **NAND only.** 先得 SOP，再应用 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]。对 $F=AB+C$，令 $n_1=\overline{AB}=\operatorname{NAND}(A,B)$，$n_2=\overline C=\operatorname{NAND}(C,C)$，最终 $F=\operatorname{NAND}(n_1,n_2)$。三个门，输入反相信号由实际 NAND 生成。
>
> Draw each inversion explicitly. If complementary inputs are unavailable, account for the inverter gates and their delay. Bubble pushing preserves a function only when the gate operation changes consistently with the moved inversions; use [[Universal Gates and Bubble Pushing]].
>
> **MUX.** 固定选择顺序 $(S_1,S_0)=(A,B)$，把每组 AB 下的 F 写成剩余变量 C 的函数：00→C，01→C，10→C，11→1。故 4:1 MUX 的 $(D_0,D_1,D_2,D_3)=(C,C,C,1)$。
>
> For a decoder, first identify whether the outputs are minterms $m_i$ or active-low complements $\overline{m_i}$. OR the selected active-high lines; NAND the selected active-low lines. Set enable inputs to their asserted levels rather than leaving them unspecified.
>
> **Adders and comparators.** 从最低位处理 carry/borrow，从最高位判断无符号大小。检查最终 carry、sum width 与 signed interpretation；器件级联输入也属于功能规范，见 [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径|Ripple Carry and Carry Look-Ahead Adders]] 与 [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]]。

### Chapter 6 Review · 功能块与判断题，p.55–56

本版 [讲义 p.2](../ECE2050-Chap6.pdf#page=2) 把期中范围列为 Ch1–6，考试为闭卷并允许计算器。第六章复习先检查“位权、极性、选择顺序、时序路径”，再用边界输入验证；第七章以后的状态与寄存器问题另按后续主线复习。

| Skill · 闭卷交付物 | Check · 最小验证 | Canonical note |
|---|---|---|
| Half/full adder · 半加器与全加器 | 写 sum/carry 并验证整数守恒；111 的 sum=1、carry=1 | [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒\|HA/FA]] |
| Carry network · 进位网络 | 声明 OR/XOR propagate；区分块内 CLA 与块间 ripple | [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径\|RCA/CLA]] |
| Comparator · 比较器 | MSB 优先；低片结论传高片，底层级联输入为 equal | [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小\|Comparator]] |
| Priority encoder · 优先编码器 | 用重叠请求测试获胜者；74HC147 的 7 输出为反相码 1000 | [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码\|Priority encoder]] |
| Decoder · 译码器 | 5-to-32 地址 15/16 跨片；低有效输出用 NAND 合并 ON 行 | [[Comparison Decoding and Selection#2 · Decoder · 代码变线路\|Decoder]] |
| Seven-segment control · 七段控制 | 区分 LT/BI/RBI；0030.0800 → 30.08 保留内部零 | [[Seven-Segment Display and Code Conversion#3 · Blanking and Zero Suppression · 控制输出可见性\|Blanking and zero suppression]] |
| MUX/DEMUX · 选择与分配 | 先固定 select 位序，再求各数据端余因子 (cofactor) | [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配\|MUX/DEMUX]] |
| Delay/hazard · 延迟与冒险 | 最长/最短路径分开；共识项 (consensus term) 不改变稳态表 | [[Propagation Delay and Logic Hazards]] |
| Multiplier · 乘法器设计扩展 | 生成同权部分积 (partial product)，逐列用 HA/FA 压缩并保留完整位宽 | [[Binary Arithmetic Circuits#4 · Combinational Multiplier · 从部分积到列加法\|Multiplier]] |

> [!example]- True/False quiz · 讲义 p.56 的十题与理由
> 下列判断与 [p.56 的勾叉](../ECE2050-Chap6.pdf#page=56) 一致，简述题意后补上必要的输入、输出含义。
>
> | # | Statement · 题意 | Answer | Why · 判断依据 |
> |---|---|---|---|
> | 1 | Half-adder adds two bits · 半加器加两个 bit | True | 输入 A、B；输出 S、C |
> | 2 | Half-adder has carry only · 半加器只有进位输出 | False | 还必须输出 sum |
> | 3 | Full-adder adds only two bits · 全加器只加两个 bit 并给两个输出 | False | 还要加 carry-in，共三个一位输入；两个输出这部分正确 |
> | 4 | Full-adder uses only 2-input XOR gates · 只能用二输入 XOR 实现全加器 | False | XOR 构成 parity/sum，carry 还需实现至少两输入为 1 的函数 |
> | 5 | A=B=Cin=1 gives sum=1 · 三输入全 1 时和位为 1 | True | $1+1+1=3=11_2$，sum=1、carry=1 |
> | 6 | Comparator outputs 0 for equality · 相等时比较器输出为 0 | False | 本章高有效 equality/XNOR 输出为 1；greater/less 此时为 0，必须指明哪一输出 |
> | 7 | Decoder detects a specified input combination · 译码器检测指定输入组合 | True | 每条输出对应一个输入码的匹配条件 |
> | 8 | 4-line-to-10-line and 1-of-10 are different decoder types · 两者为不同类型 | False | 本章 BCD-to-decimal 的两种命名；有效时十选一 |
> | 9 | Encoder reverses the decoder direction · 编码器信息方向与译码器相反 | True | 在合法输入约定下，线路→码与码→线路；多请求需另定义 priority |
> | 10 | MUX routes one source to several lines · MUX 单源分配至多路 | False | 此为 DEMUX；MUX 从多个输入选择一个送单输出 |
>
> 第 3 题原句未写 only，但课件判 False 的意图是遗漏第三个输入 $C_{in}$。回答时明确 “A full adder adds A, B, and carry-in, and produces sum and carry-out”，避免把两个操作数与三个 bit 输入混同。第 6 题也不能把一个输出值推广为所有 comparator outputs。

## 5 · 时序、状态与计数

逐边沿读旧状态、同时计算下一态；setup 取最长路径，hold 取最短路径；偏斜按统一符号加入。FSM 用状态含义解释转移，计数器检查实际状态数、末态和暂停时的级联行为。

> [!example]- Exam Review and Problem Solving · 推导与例题
> **Timing Problems · 时序约束题**
>
> 先把 launch register → combinational path → capture register 的方向标清。忽略 clock skew 时：
>
> $$T\ge t_{pcq}+t_{pd,comb}+t_{setup},\qquad t_{ccq}+t_{cd,comb}\ge t_{hold}.$$
>
> $t_{pcq}$、$t_{pd,comb}$ 是最大延迟；$t_{ccq}$、$t_{cd,comb}$ 是最小延迟。Setup 用最长路径，hold 用最短路径，两者不是把同一组数字代两次。详细 skew 约定见 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]]。
>
> **Mini-example.** $t_{pcq}=2\ \mathrm{ns}$、最长组合延迟 $7\ \mathrm{ns}$、setup $1\ \mathrm{ns}$：$T_{min}=10\ \mathrm{ns}$，$f_{max}=100\ \mathrm{MHz}$。若 $t_{ccq}=0.5\ \mathrm{ns}$、最短组合延迟 $0.2\ \mathrm{ns}$、hold $1\ \mathrm{ns}$，则 $0.7<1$，hold 失败。
>
> Increasing the clock period can resolve a setup violation but does not fix the stated hold violation. A hold repair needs extra minimum data-path delay or an appropriate clock-path change, verified under a defined timing model.
>
> **State Tracing and FSM Design · 状态追踪与状态机设计**
>
> 追踪同步电路时，每个有效时钟边沿前先计算**全部** next-state/激励输入，再同时更新全部触发器。不可更新 $Q_0$ 后立刻把新 $Q_0$ 用于同一边沿的 $Q_1$；那会把同步电路误算成连锁的软件赋值。
>
> For a three-bit shift register with $Q_2^+=Q_1$, $Q_1^+=Q_0$, $Q_0^+=d$, initial 000 and serial data 1,0,1,1, the post-edge states are 001,010,101,011. The displayed word order and serial input position are stated explicitly.
>
> FSM design proceeds through meaning of states → transitions → output rules → encoding → next-state table → flip-flop inputs → implementation. Moore output depends on current state; Mealy output depends on state and current input. Determine whether an observed output is before or after a clock edge.
>
> For D flip-flops, $D_i=Q_i^+$. For J-K flip-flops, use the excitation table for the requested $Q_i\to Q_i^+$ transition; its don't cares are different from unspecified functional states. Include reset and unused-state behavior before minimization.
>
> **Word matching versus serial matching · 并行字匹配与串行序列**
>
> 四个同时输入 ABCD 表示一个四位字，要求字中含连续 `110` 时，只有两种位置：ABC=110 或 BCD=110。
>
> $$Y=AB\overline C+BC\overline D=\Sigma m(6,12,13,14).$$
>
> 例：0110、1100、1101、1110 为 1，1011 为 0。对应 POS 是 $Y=B(A+C)(\overline C+\overline D)$。用 consensus theorem 可知展开后多出的 $AB\overline D$ 不改变函数，也可枚举全部 16 个字校验。
>
> This is combinational substring matching. A serial detector receives one bit per clock and must remember a suffix of earlier inputs; use [[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀|Sequence Detector]]. “Sequence 110” alone does not tell you which interface is intended.
>
> **Counter and ROM Problems · 计数器与查表存储**
>
> **Counter.** 写出 requested cycle 而不是只猜 toggle 式；计算模数为周期内不同状态数。同步 modulus-3 例：00→01→10→00，并规定 unused 11→00，可得：
>
> $$D_1=\overline Q_1Q_0,\qquad D_0=\overline Q_1\,\overline Q_0.$$
>
> 这四个状态代入分别得到 01、10、00、00。某个状态解码输出每三拍重复一次，频率 $f_{clk}/3$，但脉宽只一拍时 duty cycle 是 1/3，不是 50%。模数不等于电路所有可能编码数。
>
> For a binary counter DOWN transition from 1000, the next four-bit word is 0111. For a BCD decade counter, define its legal range and wrap rule separately; the word “counter” does not select a number representation.
>
> **ROM.** $a$ address bits give $2^a$ words; word width w gives capacity $2^aw$ bits. 一个把三位 ABC 中 1 的个数输出为两位二进制的 ROM，需要 $8\times2=16$ bits，其地址 000–111 的数据为 `00,01,01,10,01,10,10,11`。
>
> Use input combinations as addresses and the complete output word as stored data. A ROM implements a truth table; it does not need a separate OR gate for each output when the lookup contents already encode the result.

## Chapter 7 Review · 状态元件与判断题，p.31–32

[第 7 章讲义 p.31–32](../ECE2050-Chap7.pdf#page=31) 的复习主线是状态 (state)、SR 锁存器 (SR latch)、D 锁存器 (D latch)、D 触发器 (D flip-flop)、JK 触发器 (JK flip-flop) 和寄存器及其使能、复位、置位。判断时先确定器件对**电平还是边沿**敏感，再检查输入极性与是否有异步控制；定义和波形分析见 [[Sequential Logic and Flip-Flops]]。

| # | Statement · 题意 | 判断 | 理由 |
|---|---|---|---|
| 1 | 锁存器只有一个稳定状态 | 错 | 理想双稳态锁存器可稳定保存 0 或 1；一个稳定状态是单稳态器件的特征。 |
| 2 | 锁存器的 Q 为低时处于复位状态 | 对 | 在正常有效的互补输出约定下，Q=0 表示已复位；这不要求复位输入此刻仍被断言。SR 禁态需另行处理。 |
| 3 | 锁存器和触发器都是双稳态器件 | 对 | 均可保存 0 或 1；区别在于锁存器通常对有效电平敏感，边沿触发器在指定边沿采样。 |
| 4 | 边沿触发 D 触发器在 D 每次改变时都改变状态 | 错 | 正常工作时只在指定有效时钟边沿采样 D；其他时间 D 改变不直接更新 Q。异步控制是另一个例外。 |
| 5 | 边沿触发器需要时钟输入 | 对 | 要有指定的触发边沿作为采样事件；不是把任意数据变化都视为一次捕获。 |
| 6 | 边沿触发 JK 触发器的 J、K 均为高时，每个时钟脉冲都改变状态 | 对 | 在每个**有效边沿**且输入满足时序要求时，$Q^+=\overline Q$；每个完整时钟周期仅按指定边沿翻转一次，异步控制未断言。 |

上述题意与答案依据 [讲义 p.32](../ECE2050-Chap7.pdf#page=32) 中的六个判断题及正文分析；答案和条件是根据器件模型推导，不是讲义给出的答案标记。$Q$ 表示当前存储值，$Q^+$ 表示指定有效边沿后的下一状态。

## 6 · 存储与 HDL

容量拆成深度×位宽；ROM 地址与数据按真值表编程。VHDL 区分 signal／variable、组合／时钟过程与 delta cycle；testbench 的参考结果独立来自规范。

> [!example]- Exam Review and Problem Solving · 推导与例题
> **VHDL Problems · 从行为到硬件**
>
> Read the **entity** as an interface and the **architecture** as a hardware description. Concurrent assignments coexist; a clocked process updates registers on its specified edge. Signal assignments in one process do not behave like immediate updates to ordinary programming variables.
>
> 组合过程应给每个输出在所有分支赋值，防止意外 latch；时序过程必须明确 reset/enable 的优先级。算术先确认 `unsigned`/`signed` 与位宽，不能仅因为 `std_logic_vector` 长得像二进制数就假定其数值语义。
>
> **Mini-example — unintended latch.** `if en='1' then y <= a; end if;` 放在组合过程时，en=0 分支没有给 y 新值，描述了保存旧值。若目标为组合选择器，应补 `else y <= '0';`；若目标为保存数据，应在时钟过程里描述 enable register。
>
> Check simulation against the same truth/state table used for the hand derivation, using [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]]. Test reset, hold/enable, boundary inputs, and several clock edges; one attractive waveform is not proof of complete coverage.

## 7 · 重点自查与答句

> [!IMPORTANT] 最有效的反例
> exactly 与 at least 用全 1 区分；XOR 与 exactly-three 用 0001 区分；优先编码用重叠请求；校验用双比特错误；时序用最早与最迟到达；计数器用暂停在末态。

“With the declared variable order, the ON set is … . The reduced expression agrees on every specified row. The implementation additionally requires … under the stated polarity and timing assumptions.”

下方保留跨章综合例题与英文答题练习；遇到薄弱环节从 [[ECE2050.1]] 回到对应主线笔记。

### English Exam Q&A · 常用完整答句

**Q: How do canonical and simplified forms differ?** Every term in a canonical form contains all variables. Simplification removes unnecessary literals while preserving the function on the specified input combinations.

**Q: Why does a synchronous state trace use old values?** All registers sample their inputs at the same active edge. Their new outputs appear only after clock-to-Q delay, so the next-state equations are evaluated from the pre-edge state.

**Q: Why can a slower clock leave a failure unresolved?** Hold time constrains the earliest arrival of new data after the capture edge. Changing the cycle period does not, by itself, delay that earliest arrival.

### Closed-Book Check · 考前自查与错题归因

- I can name the representation and justify the required width.
- I can distinguish canonical forms, minimal forms, and a physical implementation.
- I can translate an active-low pin into asserted/inactive behavior.
- I can evaluate next-state logic before updating the current state.
- I can explain why my test vectors cover the requirement and state what remains untested.

把每道错题归到“概念/题意/符号/推导/验证”中的一类，回到对应的 canonical note 修正理解。需要电路故障敏化时转到 [[Digital Logic Troubleshooting]]；需要 display/BCD 综合题时转到 [[Seven-Segment Display and Code Conversion]]。

> [!example]- Exam Review and Problem Solving · 推导与例题
> **Checking Reference Solutions · 如何使用参考答案**
>
> 参考答案适合比较方法，但每个结论仍需符合题意、位宽与图中极性。教材剪贴页中的“negative edge”说明可能属于旁边另一个示例；如果实际题目指定 positive-edge，必须按本题边沿计算。
>
> One earlier supplied CRC example uses data `10110010` and generator `1010` but appends four zeros and reports a twelve-bit code. The generator has degree three, so the conventional systematic CRC model needs three appended zeros and a three-bit remainder.
>
> 按该模型，$10110010000\div1010$ 的 XOR 余数为 `110`，正确发送码为 **`10110010110`**（8+3=11 bits）；再除一次余数为 0。生成式常数项为 0 还意味着它不具备常用 CRC 生成多项式的一般选择特性，但不改变这里的除法位数。
>
> **当前学期版本区别：** [当前 Ch2 PDF p.71](../ECE2050-Chap2.pdf#page=71) 的数据为 `11010011`，生成码同为 `1010`。仍应补三个零，但余数是 **`010`**、发送码是 **`11010011010`**；不要把不同数据版本的余数混用。更多源文件更正见 [[Midterm Review Guide]]。
>
> Check answers independently: evaluate all rows for small Boolean functions, decode arithmetic results back to decimal, trace state cycles, verify timing inequalities, and divide the transmitted CRC word again. A successful check should use the original specification rather than repeating the same possibly wrong intermediate equation.

## Sources · 章节补充依据

Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 6: Combinational Building Blocks*，[本次讲义 PDF p.55–56](../ECE2050-Chap6.pdf#page=55)：章末清单、HA/FA 乘法器设计问题与十个判断题；p.2：该版课件的考试范围说明。详细推导与图示见上表链接；其余跨章练习保留原内容。

Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 7: Sequential Logic Design*，[本次讲义 PDF p.31–32](../ECE2050-Chap7.pdf#page=31)：本章复习清单与六个判断题；器件工作方式见 p.4–30。

---
索引：[[ECE2050.1]] · [[Glossary]]
