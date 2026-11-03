---
tags:
  - ECE2050
  - review
date: 2026-09-30
aliases:
  - 考试复习与解题方法
  - Exam Review and Problem Solving
  - Digital logic exam review
---

# Exam Review and Problem Solving · 考试复习与解题方法

> [!SUMMARY] Quick recall · 英文速览
> Read the specification before choosing a technique. Record representation, width, variable order, active polarity, clock edge, and initial state. Derive intermediate results, then use an independent check rather than relying on a printed solution.

## Core Definition · 核心目标

这篇是复习导航与解题模板，不替代各概念的详细推导。数字逻辑题通常要求完成一条可验证的链：**文字规范 → 数学/状态模型 → 电路或代码 → 功能与时序检查**。

An answer should state what the circuit means before showing how it is built. “Simplify,” “canonical,” “implement,” “trace,” and “design” request different deliverables; a correct simplified expression can still be the wrong answer to a canonical-form question.

## Learning Path · 按先修关系复习

| Stage | Prerequisite → next topic | Exit question · 自查问题 |
|---|---|---|
| 1. Representation | [[Number Systems]] → [[Number Base Conversion]] → [[Two's Complement Representation]] | Can I explain the value of these bits at this width? |
| 2. Boolean meaning | [[Logic Gates]] → [[Truth Table and Boolean Expression]] → [[Minterm and Maxterm]] | Can I identify exactly which rows produce 1/0? |
| 3. Simplification | [[Laws and Rules of Boolean Algebra]] → [[Karnaugh Map]] → [[POS Minimization with Karnaugh Map]] | Is the result equivalent on every required row? |
| 4. Building blocks | [[Combinational Logic Design]] → [[Decoder]] / [[Multiplexer and Demultiplexer]] / [[Half Adder and Full Adder]] | Can I connect all inputs with correct polarity? |
| 5. Stored state | [[Sequential Logic]] → [[D Latch and D Flip-Flop]] → [[Register Enable and Reset]] → [[Shift Registers]] | Which values are sampled, held, or updated? |
| 6. State design | [[Finite State Machine]] → [[Moore and Mealy Machines]] → [[State Encoding and Unused States]] | Does every state/input pair have a defined transition? |
| 7. System use | [[Counters]] → [[Memory Arrays and Expansion]] / [[Read-Only Memory and Programmable Logic Arrays]] → [[VHDL Language and Modeling]] | Can I connect function, state, storage, and implementation? |

先补最早断开的依赖，不要直接背后续式子。看不懂 counter 激励表时，先回 [[JK and T Flip-Flops]]；看不懂 ROM 地址宽度时，先回 [[Bits and Bytes]] 与 [[Binary Number System]]。

For each topic, practice four passes: explain it in one English sentence, derive one result in Chinese, solve a small example without notes, and check the answer using another representation. Review the resulting error pattern rather than rereading every page equally.

## Read the Question · 先把题意变成约束

在草稿第一行记录六项：**representation / width / bit order / polarity / clock edge / initial state**。不适用的项目写“combinational”或“unsigned”，不要留下可能改变答案的空白。

Words such as **exactly**, **at least**, **highest priority**, **overlapping**, **synchronous**, and **asynchronous** change the model. Underline them and translate them into a table or equation before drawing gates.

“至少两个为 1”在三输入时是 $AB+AC+BC$，包含 111；“恰好两个为 1”是 $AB\overline C+A\overline BC+\overline ABC$，不包含 111。先列边界反例能防止把两种要求混同。

## Number Problems · 数制与算术题

1. 确定位串是 unsigned、two's complement、sign magnitude、BCD 还是浮点；同一位串可能有不同值。
2. 对 signed arithmetic 先写十进制预期符号与大致大小，再按固定宽度计算。扩位时 two's complement 要 sign extension。
3. 区分 carry 与 signed overflow。负数加正数不会因最终 carry=1 就自动 overflow。
4. Binary↔octal/hex grouping begins at the binary point. Pad zeros only at the outside ends; never move the point.
5. For [[Cyclic Redundancy Check]], divide with XOR, append degree-many zeros, and transmit exactly degree-many remainder bits.

**Mini-example — signed multiplication.** 4 位 two's complement `1011`=-5、`1101`=-3，乘积 +15。若要求完整 8 位结果，应写 `00001111`；`1111` 在 4 位 signed 模型下是 -1。数学值正确仍需满足输出宽度。

**Mini-example — fractional grouping.** `10.101101₂`：向三位分组得 `010.101 101`，故 $2.55_8$；向四位分组得 `0010.1011 0100`，故 $2.B4_{16}$。二者都等于 $2+45/64=2.703125$。

## Boolean Forms and K-maps · 标准式与卡诺图

Canonical SOP lists minterms for every 1 row; canonical POS lists maxterms for every 0 row. Each canonical term contains every variable once. A simplified SOP/POS need not contain every variable in each term.

对变量顺序 ABC，$F=AB+C$ 在编号 1,3,5,6,7 为 1，所以：

$$F=\Sigma m(1,3,5,6,7)=\Pi M(0,2,4).$$

若要求完整 standard POS，应展开为 $(A+B+C)(A+\overline B+C)(\overline A+B+C)$。最简 POS $(A+C)(B+C)$ 与它等价，但不是 canonical POS。

K-map procedure: label axes in Gray-code order; fill cells from the specification; group 1s for SOP or 0s for POS; use power-of-two rectangular groups and wraparound adjacency; remove changing variables; check all required cells afterward.

Don't cares 可以选用，也可以不选；组必须帮助覆盖 required 1/0，不能单独圈一组 X 当成必需项。规范要求 unused states recover 时，不能把其 next-state rows 全部丢成 X。

A quick consistency check uses the original truth table, not the drawing alone. For $F=AB+C$, C=1 must produce F=1 for all A/B, and C=0 must reduce to AB. These two cofactors catch many misplaced K-map groups.

## Gate and Block Implementation · 门与功能块实现

**NAND only.** 先得 SOP，再应用 [[DeMorgan's Theorems]]。对 $F=AB+C$，令 $n_1=\overline{AB}=\operatorname{NAND}(A,B)$，$n_2=\overline C=\operatorname{NAND}(C,C)$，最终 $F=\operatorname{NAND}(n_1,n_2)$。三个门，输入反相信号由实际 NAND 生成。

Draw each inversion explicitly. If complementary inputs are unavailable, account for the inverter gates and their delay. Bubble pushing preserves a function only when the gate operation changes consistently with the moved inversions; use [[Universal Gates and Bubble Pushing]].

**MUX.** 固定选择顺序 $(S_1,S_0)=(A,B)$，把每组 AB 下的 F 写成剩余变量 C 的函数：00→C，01→C，10→C，11→1。故 4:1 MUX 的 $(D_0,D_1,D_2,D_3)=(C,C,C,1)$。

For a decoder, first identify whether the outputs are minterms $m_i$ or active-low complements $\overline{m_i}$. OR the selected active-high lines; NAND the selected active-low lines. Set enable inputs to their asserted levels rather than leaving them unspecified.

**Adders and comparators.** 从最低位处理 carry/borrow，从最高位判断无符号大小。检查最终 carry、sum width 与 signed interpretation；器件级联输入也属于功能规范，见 [[Ripple Carry and Carry Look-Ahead Adders]] 与 [[Magnitude Comparator]]。

## Timing Problems · 时序约束题

先把 launch register → combinational path → capture register 的方向标清。忽略 clock skew 时：

$$T\ge t_{pcq}+t_{pd,comb}+t_{setup},\qquad t_{ccq}+t_{cd,comb}\ge t_{hold}.$$

$t_{pcq}$、$t_{pd,comb}$ 是最大延迟；$t_{ccq}$、$t_{cd,comb}$ 是最小延迟。Setup 用最长路径，hold 用最短路径，两者不是把同一组数字代两次。详细 skew 约定见 [[Setup and Hold Timing]]。

**Mini-example.** $t_{pcq}=2\ \mathrm{ns}$、最长组合延迟 $7\ \mathrm{ns}$、setup $1\ \mathrm{ns}$：$T_{min}=10\ \mathrm{ns}$，$f_{max}=100\ \mathrm{MHz}$。若 $t_{ccq}=0.5\ \mathrm{ns}$、最短组合延迟 $0.2\ \mathrm{ns}$、hold $1\ \mathrm{ns}$，则 $0.7<1$，hold 失败。

Increasing the clock period can resolve a setup violation but does not fix the stated hold violation. A hold repair needs extra minimum data-path delay or an appropriate clock-path change, verified under a defined timing model.

## State Tracing and FSM Design · 状态追踪与状态机设计

追踪同步电路时，每个有效时钟边沿前先计算**全部** next-state/激励输入，再同时更新全部触发器。不可更新 $Q_0$ 后立刻把新 $Q_0$ 用于同一边沿的 $Q_1$；那会把同步电路误算成连锁的软件赋值。

For a three-bit shift register with $Q_2^+=Q_1$, $Q_1^+=Q_0$, $Q_0^+=d$, initial 000 and serial data 1,0,1,1, the post-edge states are 001,010,101,011. The displayed word order and serial input position are stated explicitly.

FSM design proceeds through meaning of states → transitions → output rules → encoding → next-state table → flip-flop inputs → implementation. Moore output depends on current state; Mealy output depends on state and current input. Determine whether an observed output is before or after a clock edge.

For D flip-flops, $D_i=Q_i^+$. For J-K flip-flops, use the excitation table for the requested $Q_i\to Q_i^+$ transition; its don't cares are different from unspecified functional states. Include reset and unused-state behavior before minimization.

### Word matching versus serial matching · 并行字匹配与串行序列

四个同时输入 ABCD 表示一个四位字，要求字中含连续 `110` 时，只有两种位置：ABC=110 或 BCD=110。

$$Y=AB\overline C+BC\overline D=\Sigma m(6,12,13,14).$$

例：0110、1100、1101、1110 为 1，1011 为 0。对应 POS 是 $Y=B(A+C)(\overline C+\overline D)$。用 consensus theorem 可知展开后多出的 $AB\overline D$ 不改变函数，也可枚举全部 16 个字校验。

This is combinational substring matching. A serial detector receives one bit per clock and must remember a suffix of earlier inputs; use [[Sequence Detector]]. “Sequence 110” alone does not tell you which interface is intended.

## Counter and ROM Problems · 计数器与查表存储

**Counter.** 写出 requested cycle 而不是只猜 toggle 式；计算模数为周期内不同状态数。同步 modulus-3 例：00→01→10→00，并规定 unused 11→00，可得：

$$D_1=\overline Q_1Q_0,\qquad D_0=\overline Q_1\,\overline Q_0.$$

这四个状态代入分别得到 01、10、00、00。某个状态解码输出每三拍重复一次，频率 $f_{clk}/3$，但脉宽只一拍时 duty cycle 是 1/3，不是 50%。模数不等于电路所有可能编码数。

For a binary counter DOWN transition from 1000, the next four-bit word is 0111. For a BCD decade counter, define its legal range and wrap rule separately; the word “counter” does not select a number representation.

**ROM.** $a$ address bits give $2^a$ words; word width w gives capacity $2^aw$ bits. 一个把三位 ABC 中 1 的个数输出为两位二进制的 ROM，需要 $8\times2=16$ bits，其地址 000–111 的数据为 `00,01,01,10,01,10,10,11`。

Use input combinations as addresses and the complete output word as stored data. A ROM implements a truth table; it does not need a separate OR gate for each output when the lookup contents already encode the result.

## VHDL Problems · 从行为到硬件

Read the **entity** as an interface and the **architecture** as a hardware description. Concurrent assignments coexist; a clocked process updates registers on its specified edge. Signal assignments in one process do not behave like immediate updates to ordinary programming variables.

组合过程应给每个输出在所有分支赋值，防止意外 latch；时序过程必须明确 reset/enable 的优先级。算术先确认 `unsigned`/`signed` 与位宽，不能仅因为 `std_logic_vector` 长得像二进制数就假定其数值语义。

**Mini-example — unintended latch.** `if en='1' then y <= a; end if;` 放在组合过程时，en=0 分支没有给 y 新值，描述了保存旧值。若目标为组合选择器，应补 `else y <= '0';`；若目标为保存数据，应在时钟过程里描述 enable register。

Check simulation against the same truth/state table used for the hand derivation, using [[Testbench and Functional Verification]]. Test reset, hold/enable, boundary inputs, and several clock edges; one attractive waveform is not proof of complete coverage.

## Checking Reference Solutions · 如何使用参考答案

参考答案适合比较方法，但每个结论仍需符合题意、位宽与图中极性。教材剪贴页中的“negative edge”说明可能属于旁边另一个示例；如果实际题目指定 positive-edge，必须按本题边沿计算。

One supplied CRC example uses data `10110010` and generator `1010` but appends four zeros and reports a twelve-bit code. The generator has degree three, so the conventional systematic CRC model needs three appended zeros and a three-bit remainder.

按该模型，$10110010000\div1010$ 的 XOR 余数为 `110`，正确发送码为 **`10110010110`**（8+3=11 bits）；再除一次余数为 0。生成式常数项为 0 还意味着它不具备常用 CRC 生成多项式的一般选择特性，但不改变这里的除法位数。

Check answers independently: evaluate all rows for small Boolean functions, decode arithmetic results back to decimal, trace state cycles, verify timing inequalities, and divide the transmitted CRC word again. A successful check should use the original specification rather than repeating the same possibly wrong intermediate equation.

## English Exam Q&A · 常用完整答句

**Q: How do canonical and simplified forms differ?** Every term in a canonical form contains all variables. Simplification removes unnecessary literals while preserving the function on the specified input combinations.

**Q: Why does a synchronous state trace use old values?** All registers sample their inputs at the same active edge. Their new outputs appear only after clock-to-Q delay, so the next-state equations are evaluated from the pre-edge state.

**Q: Why can a slower clock leave a failure unresolved?** Hold time constrains the earliest arrival of new data after the capture edge. Changing the cycle period does not, by itself, delay that earliest arrival.

## Method and Review · 考前自查

- I can name the representation and justify the required width.
- I can distinguish canonical forms, minimal forms, and a physical implementation.
- I can translate an active-low pin into asserted/inactive behavior.
- I can evaluate next-state logic before updating the current state.
- I can explain why my test vectors cover the requirement and state what remains untested.

把每道错题归到“概念/题意/符号/推导/验证”中的一类，回到对应的 canonical note 修正理解。需要电路故障敏化时转到 [[Digital Logic Troubleshooting]]；需要 display/BCD 综合题时转到 [[Seven-Segment Display and Code Conversion]]。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
