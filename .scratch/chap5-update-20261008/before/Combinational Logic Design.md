---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
aliases:
  - 组合逻辑设计
  - Combinational Logic Design
  - Combinational analysis and implementation
---

# Combinational Logic Design · 组合逻辑设计

> [!SUMMARY] Quick recall · 英文速览
> Analysis finds the function of a given circuit. Design creates a circuit from a specification. Convert the wording into a complete truth table before minimizing or choosing an implementation.

## Core Definition · 核心定义

分析 (analysis) 从连接推出方程；设计 (design) 从需求推出连接。规范必须包含输入含义、有效极性、输出条件与无效输入处理。稳态模型是 $Y=F(X)$，其中 $X$ 为当前输入向量，$Y$ 为当前输出。

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

## Worked Example 1 · 储罐报警

三个传感器 $A,B,C=1$ 表示液位过低；任意至少两个过低则报警。满足条件的 minterms 为 $m_3,m_5,m_6,m_7$，变量顺序 ABC。

$$Y=\bar ABC+A\bar BC+AB\bar C+ABC=AB+AC+BC.$$

The three products cover the three possible pairs. Their overlap at 111 is allowed: OR does not count how many terms are TRUE. Check 110 → 1, 100 → 0, and 111 → 1.

若传感器 LOW 表示过低，先定义事件 $a=\bar A,b=\bar B,c=\bar C$；高有效报警为 $Y=\bar A\bar B+\bar A\bar C+\bar B\bar C$。若报警也低有效，再取补；不能只因为输入低有效就自动反相输出。

## Worked Example 2 · 同时四位中的模式

四个同时给出的输入按 ABCD 从左至右排列。要求出现连续 110，则可出现在 ABC 或 BCD：

$$Y=AB\bar C+BC\bar D=B(A\bar C+C\bar D)=B(A+C)(\bar C+\bar D).$$

最后一步用 $XY+\bar XZ=(X+Z)(\bar X+Y)$ 的适当变量替换；也可枚举核对。ON set 是 $\{6,12,13,14\}$，因为 0110、1100、1101、1110 满足条件。1011 没有 110，输出 0。

This is a combinational pattern detector. A serial 110 detector must remember previous symbols and belongs to [[Sequence Detector]]. The physical input format decides whether memory is necessary.

## Worked Example 3 · 五位分类

5-bit unsigned input $B_4\ldots B_0$ 表示 0–31。prime 输出的 ON set 是 $\{2,3,5,7,11,13,17,19,23,29,31\}$；square 是 $\{0,1,4,9,16,25\}$；被 3 与 5 同时整除是 $\{0,15,30\}$。0 不是 prime，但 $0=0^2=15\times0$。

Write each output as the sum of its minterms, then minimize separately. Do not redefine a mathematical condition because a familiar example omitted zero.

## Pitfalls and Review · 误区与复习

- [[Karnaugh Map with Don't Cares]]：只有规范允许不关心的输入才能标 X。
- [[Truth Table and Boolean Expression]]：canonical form 包含每个变量；simplified form 可省变量。
- [[Digital Logic Troubleshooting]]：故障分析先对内部节点作替换，再重新求函数。

**Exam answer pattern:** “With ABC as the variable order, the output is asserted for minterms … . Grouping adjacent cells gives … . Substitution on all specified rows confirms the implementation.”

## Connections · 相关笔记

Prerequisites: [[Boolean Equation]], [[Sum-of-Products Form]], [[Product-of-Sums Form]]. Implementations: [[Universal Gates and Bubble Pushing]], [[Decoder]], [[Multiplexer and Demultiplexer]], [[Read-Only Memory and Programmable Logic Arrays]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
