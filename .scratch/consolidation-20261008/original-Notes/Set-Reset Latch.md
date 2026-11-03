---
tags:
  - ECE2050
  - sequential-logic
date: 2026-09-30
aliases:
  - 置位复位锁存器
  - Set-Reset Latch
  - SR latch
---

# Set-Reset Latch · 置位复位锁存器

> [!SUMMARY] Quick recall · 英文速览
> An SR latch stores one bit using cross-coupled feedback. The NOR version has active-high S/R; the NAND version has active-low controls. Their hold and invalid input patterns differ.

## Core Definition · 核心定义

锁存器 (latch) 利用双稳态 (bistability) 保存一位 Q。对交叉 NOR、S 和 R 高有效：$Q=\overline{R+\bar Q}$，$\bar Q=\overline{S+Q}$。这里 $\bar Q$ 是互补输出标签；禁态时它并不保证等于 NOT Q。

| S | R | Action | Q next |
|---|---|---|---|
| 0 | 0 | Hold | Previous Q |
| 1 | 0 | Set | 1 |
| 0 | 1 | Reset | 0 |
| 1 | 1 | Invalid | Both outputs forced 0 while asserted |

## Derivation · 为什么能保持

S=R=0 时，Q 与另一个输出互相取反，(Q,other)=(0,1) 与 (1,0) 都自洽。输入不指定新的状态，反馈保持已有状态。S=1 强迫另一输出为 0，随后 Q=1；R=1 对称地强迫 Q=0。

The invalid input is not merely a harmless unused truth-table row. Both NOR outputs are LOW, and when both controls are released together, delay imbalance may determine the final state. It can become unpredictable or temporarily metastable.

在排除 S=R=1 的合法域内，特征式为：

$$Q^+=S+\bar RQ.$$

不能用此式给禁态制造“优先级”。原 NOR latch 的禁态行为由电路决定，不等于具有 set priority 的新设计。

## NAND Variant · NAND 型

交叉 NAND 的输入为低有效 $\bar S,\bar R$：11 保持，01 置位，10 复位，00 禁态且两个输出都 HIGH。记忆规则“都不有效时保持，两个都有效时禁态”比死记 00/11 更稳。

| NOR active-high | NAND active-low | Meaning |
|---|---|---|
| S=0,R=0 | $\bar S=1,\bar R=1$ | Hold |
| S=1,R=0 | $\bar S=0,\bar R=1$ | Set |
| S=0,R=1 | $\bar S=1,\bar R=0$ | Reset |
| S=1,R=1 | $\bar S=0,\bar R=0$ | Invalid |

## Worked Example · 事件序列

NOR 型初值 Q=0，依次 (S,R)=10、00、01、00，状态依次 1、1、0、0。NAND 型等价输入依次 01、11、10、11，得到相同状态序列。

If a waveform enters the invalid input condition, mark it explicitly. Do not continue the trace by choosing a convenient remembered value unless the question gives a release priority or delay assumption.

## Method and Review · 方法与复习

1. Identify NOR versus NAND and input bubbles.
2. Translate voltage levels into asserted/unasserted controls.
3. Segment the waveform at every S or R transition.
4. Apply set/reset/hold and preserve the initial state.
5. Label invalid assertion and uncertain release behavior.

**Exam question:** Is Q=0 necessarily an invalid state?

**Answer:** No. Q=0 is the valid reset state when the complementary output is 1. Invalidity concerns the control combination and loss of complementary outputs, not the stored value zero.

## Connections · 相关笔记

[[NOR Gate]], [[NAND Gate]], [[Sequential Logic]], [[D Latch and D Flip-Flop]], [[Metastability and Clock Domain Crossing]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
