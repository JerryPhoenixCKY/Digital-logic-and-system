---
tags:
  - ECE2050
  - counters
date: 2026-09-30
aliases:
  - 同步计数器设计
  - Synchronous Counter Design
  - Counter excitation synthesis
---

# Synchronous Counter Design · 同步计数器设计

> [!SUMMARY] Quick recall · 英文速览
> Design begins with the required sequence, then derives next-state bits and flip-flop excitation inputs. Don't-cares may simplify the implementation, but the resulting unused-state transitions still need checking.

## Design Method · 设计方法

状态图 → next-state table → excitation table → K-map → input equations → implementation → 全状态核对。DFF 的激励直接为 $D_i=Q_i^+$；TFF 为 $T_i=Q_i\oplus Q_i^+$；JK 用逐位 transition table。

不要把 current state 和 next state 的 bit 列混在一起；所有输入函数以 current Q 与控制输入表示。题目要求 DFF 时最终 equations 要给 D，而不是仅列 J/K。

## Worked Example 1 · Modulo-3 with recovery

设状态 00→01→10→00；unused 11→00，初态 00。

| Current | Next | D1 | D0 | Pulse P |
|---|---|---|---|---|
| 00 | 01 | 0 | 1 | 0 |
| 01 | 10 | 1 | 0 | 0 |
| 10 | 00 | 0 | 0 | 1 |
| 11 | 00 | 0 | 0 | 0 |

$$D_1=\bar Q_1Q_0,\quad D_0=\bar Q_1\bar Q_0,\quad P=Q_1\bar Q_0.$$

P 每三拍重复一次，frequency=$f_{clk}/3$，HIGH 一拍所以 duty=1/3。两位状态不意味着随便挑一位就能得到相同 duty 的波形；若要求 50% divide-by-3 输出，仅正沿更新的简单三态 decode 不能每 1.5 周期改变一次。

## Worked Example 2 · 指定非顺序计数

要求 0→5→1→2→7→6→3→4→0，使用三个 FF。按 Q2Q1Q0 排列：

| Current decimal | Current bits | Next bits |
|---|---|---|
| 0 | 000 | 101 |
| 1 | 001 | 010 |
| 2 | 010 | 111 |
| 3 | 011 | 100 |
| 4 | 100 | 000 |
| 5 | 101 | 001 |
| 6 | 110 | 011 |
| 7 | 111 | 110 |

使用 DFF 可得到一组简洁式：

$$D_2=\bar Q_2\bar Q_0+Q_1Q_0,$$
$$D_1=\bar Q_2\bar Q_1Q_0+Q_1\bar Q_0+Q_2Q_1,$$
$$D_0=Q_2\bar Q_1Q_0+\bar Q_2\bar Q_0+Q_1\bar Q_0.$$

由每位 next=1 的 minterms 配对而来。也可保留 canonical D equations 完成验证，再改用 JK 激励化简；D 方案与 JK 方案都是同一行为的不同实现。

## JK Design · JK 设计细节

例如 000→101：bit2 为 0→1，所以 J2=1,K2=X；bit1 0→0 所以 J1=0,K1=X；bit0 0→1 所以 J0=1,K0=X。所有行分别填表，然后每个 J/K 变量各自画 K-map。

A valid but not always minimal JK implementation is $J_i=Q_i^+$ and $K_i=\overline{Q_i^+}$. The excitation-table don't-cares can produce a smaller circuit because each input matters only for one current-state value.

## Verification and Review · 验证与复习

Check every state, not only a few clock pulses. Confirm cycle length, absence of unintended branches, reset entry, and unused-state behavior. For an up/down counter, include both direction values for each state.

**Exam question:** Why does a simplified JK expression sometimes omit the current bit itself?

**Answer:** When Q=0, K is irrelevant; when Q=1, J is irrelevant. These excitation don't-cares can eliminate literals while preserving the desired next state through the JK characteristic equation.

## Connections · 相关笔记

[[Counters]], [[JK and T Flip-Flops]], [[Karnaugh Map]], [[State Encoding and Unused States]], [[Finite State Machine]], [[Testbench and Functional Verification]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
