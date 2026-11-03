---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
updated: 2026-10-08
aliases:
  - 组合逻辑设计
  - Combinational Logic Design
  - Combinational analysis and implementation
---

# Combinational Logic Design · 组合逻辑设计

> [!SUMMARY] Quick recall · 英文速览
> Analysis finds the function of a given circuit. Design creates a circuit from a specification. Convert the wording into a complete truth table before minimizing or choosing an implementation.

## Core Definition · 核心定义

分析 (analysis) 从连接推出方程；设计 (design) 从需求推出连接。规范 (specification) 必须包含输入含义、有效极性、输出条件与无效输入处理。稳态模型是 $Y=F(X)$，其中 $X$ 为当前输入向量，$Y$ 为当前输出；所有分量都是无量纲的 0/1。电路分析的逐节点推导见 [[Combinational Logic Analysis]]。

“At least two” includes three or four. “Exactly two” excludes them. “Consecutive” refers to adjacent positions in a supplied word unless the question specifies a serial stream over clock cycles. These small words change the truth table.

## Derivation · 规范到方程

| Step | Deliverable | Why it matters |
|---|---|---|
| Define inputs | Meaning and active polarity | Distinguishes LOW voltage from FALSE event |
| Enumerate cases | Truth table | Prevents missing conditions |
| Choose ON/OFF sets | SOP or POS | Makes minimization reproducible |
| Minimize | K-map with marked groups | Preserves all specified rows |
| Implement | Gates, decoder, MUX or ROM | Fits available hardware |
| Verify | Compare every defined input row | Detects polarity and indexing mistakes |

### Expression and Truth Table to Circuit · 课件 p.16

布尔表达式 (Boolean expression) $X=AB+CDE$ 直接对应二输入 AND、三输入 AND 和末级 OR。反变量必须由可用的互补输入或反相器提供。[[AND-OR and AND-OR-Invert Logic]] 比较与或和与或非结构。

课件另一张真值表只有 $ABC=011,100$ 输出 1，变量顺序明确为 ABC。因此：

$$
X=\sum m(3,4)=\bar ABC+A\bar B\bar C.
$$

Each row contributes one complete minterm. The two ON rows differ in three bits, so they cannot be combined into one K-map group. The unlisted rows are zeros, not don't-cares.

## Worked Example 1 · 储罐报警

三个传感器 $A,B,C=1$ 表示液位过低；任意至少两个过低则报警。满足条件的 minterms 为 $m_3,m_5,m_6,m_7$，变量顺序 ABC。

$$Y=\bar ABC+A\bar BC+AB\bar C+ABC=AB+AC+BC.$$

The three products cover the three possible pairs. Their overlap at 111 is allowed: OR does not count how many terms are TRUE. Check 110 → 1, 100 → 0, and 111 → 1.

若传感器 LOW 表示过低，先定义事件 $a=\bar A,b=\bar B,c=\bar C$；高有效报警为 $Y=\bar A\bar B+\bar A\bar C+\bar B\bar C$。若报警也低有效，再取补；不能只因为输入低有效就自动反相输出。

课件 p.5、p.7 的两种极性、完整真值表及 $\overline{AB+AC+BC}$ 的 AOI 实现见 [[AND-OR and AND-OR-Invert Logic]]。

## Worked Example 2 · 恰好四个输入中的三个为 1，课件 p.17

输入顺序为 $ABCD$，A 为最高有效位 (most significant bit, MSB)，行编号 $i=8A+4B+2C+D$。输出 $X=1$ 当且仅当四个同时给出的输入里恰好有三个 1：

$$
X=\bar ABCD+A\bar BCD+AB\bar CD+ABC\bar D
=\sum m(7,11,13,14).
$$

| $i$ | $ABCD$ | 1 的个数 | $X$ |
|---|---|---|---|
| 0 | 0000 | 0 | 0 |
| 1 | 0001 | 1 | 0 |
| 2 | 0010 | 1 | 0 |
| 3 | 0011 | 2 | 0 |
| 4 | 0100 | 1 | 0 |
| 5 | 0101 | 2 | 0 |
| 6 | 0110 | 2 | 0 |
| 7 | 0111 | 3 | 1 |
| 8 | 1000 | 1 | 0 |
| 9 | 1001 | 2 | 0 |
| 10 | 1010 | 2 | 0 |
| 11 | 1011 | 3 | 1 |
| 12 | 1100 | 2 | 0 |
| 13 | 1101 | 3 | 1 |
| 14 | 1110 | 3 | 1 |
| 15 | 1111 | 4 | 0 |

Any two ON patterns differ in two positions, so none are adjacent in a K-map. Every single-bit neighbor contains either two or four 1s and must output 0. With no don't-cares, all four four-literal terms are necessary in the minimum two-level SOP.

允许四输入门时，用四个四输入 AND 接一个四输入 OR；若互补输入未提供，另计四个 NOT。二级是主 AND-OR 结构的级数，不是总门数；只有二输入门时需分解多输入门。

**不要替换为 XOR。** $A\oplus B\oplus C\oplus D$ 在恰好一个或三个输入为 1 时都输出 1；例如 0001 应有 $X=0$，但 XOR 为 1。“至少三个”则包含 1111，函数为 $ABC+ABD+ACD+BCD$，也与本题不同。

**Sanity check:** four of sixteen rows assert the output, matching $\binom{4}{3}=4$. Testing 0111, 1111, and 0001 distinguishes exactly-three, at-least-three, and odd-parity specifications.

## Worked Example 3 · 同时四位中的模式

四个同时给出的输入按 ABCD 从左至右排列。要求出现连续 110，则可出现在 ABC 或 BCD：

$$Y=AB\bar C+BC\bar D=B(A\bar C+C\bar D)=B(A+C)(\bar C+\bar D).$$

最后一步用 $XY+\bar XZ=(X+Z)(\bar X+Y)$ 的适当变量替换；也可枚举核对。ON set 是 $\{6,12,13,14\}$，因为 0110、1100、1101、1110 满足条件。1011 没有 110，输出 0。

This is a combinational pattern detector. A serial 110 detector must remember previous symbols and belongs to [[Sequence Detector]]. The physical input format decides whether memory is necessary.

## Worked Example 4 · 五位分类

5-bit unsigned input $B_4\ldots B_0$ 表示 0–31。prime 输出的 ON set 是 $\{2,3,5,7,11,13,17,19,23,29,31\}$；square 是 $\{0,1,4,9,16,25\}$；被 3 与 5 同时整除是 $\{0,15,30\}$。0 不是 prime，但 $0=0^2=15\times0$。

Write each output as the sum of its minterms, then minimize separately. Do not redefine a mathematical condition because a familiar example omitted zero.

## Priority and Don't-Cares · 优先级与无关项，课件 p.20–22

优先电路 (priority circuit) 在多个请求同时有效时，只断言最高优先级的获胜线路。课件输出 $Y_3Y_2Y_1Y_0$ 是独热获胜掩码 (one-hot winner mask)，并不是二进制位置码。完整推导和两种输出的对照见 [[Encoder and Priority Encoder]]。

In the compact table, a lower-priority input marked X means either 0 or 1 produces the same specified output. It does not permit arbitrary outputs for multiple requests and does not describe an electrically floating input. Distinguish this table compression from an unspecified output used in [[Karnaugh Map with Don't Cares]].

## Chapter Quiz · 课件 p.33 判断题复习

| Topic · 判断要点 | T/F | Reason · 理由 |
|---|---|---|
| AND-OR 仅能由两个二输入 AND 构成 | F | 乘积项数和各项输入数不受此限制 |
| AOI 展开为 AND-OR-Invert | T | 最终结果为 SOP 的补 |
| 相同的两个 XOR 输入得到 LOW | T | $0\oplus0=1\oplus1=0$ |
| 不同的两个 XNOR 输入得到 HIGH | F | 不同时 XNOR 为 0 |
| XOR 不能构成奇偶校验发生器 | F | 偶校验位等于数据位的 XOR |
| NAND 可以实现 AND | T | NAND 的结果再用 tied-input NAND 反相 |
| NOR 无法实现 OR | F | NOR 的结果再反相即 OR |
| 任意 SOP 均能仅用 NAND 实现 | T | NAND-NAND，加必要的同类输入反相器 |
| NAND 的对偶画法是 negative-AND | F | 应为 negative-OR；negative-AND 对应 NOR |
| Negative-OR 与 NAND 等价 | T | $\bar A+\bar B=\overline{AB}$ |

## Pitfalls and Review · 误区与复习

- [[Karnaugh Map with Don't Cares]]：只有规范允许不关心的输入才能标 X。
- [[Truth Table and Boolean Expression]]：canonical form 包含每个变量；simplified form 可省变量。
- [[Digital Logic Troubleshooting]]：故障分析先对内部节点作替换，再重新求函数。

**Exam answer pattern:** “With ABC as the variable order, the output is asserted for minterms … . Grouping adjacent cells gives … . Substitution on all specified rows confirms the implementation.”

## Connections · 相关笔记

Prerequisites: [[Boolean Equation]], [[Sum-of-Products Form]], [[Product-of-Sums Form]]. Analysis and structures: [[Combinational Logic Analysis]], [[AND-OR and AND-OR-Invert Logic]]. Implementations: [[Universal Gates and Bubble Pushing]], [[Decoder]], [[Multiplexer and Demultiplexer]], [[Read-Only Memory and Programmable Logic Arrays]].

## Sources · 来源

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.5、7、16–22、33；[本地课件](../ECE2050-Chap5.pdf#page=16)。完整真值表、最小 SOP 的理由与判断题解释为独立推导。四位模式与五位分类例题保留为既有补充练习。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
