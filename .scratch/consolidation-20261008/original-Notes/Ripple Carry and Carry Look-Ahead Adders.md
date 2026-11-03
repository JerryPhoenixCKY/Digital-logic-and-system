---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 串行进位与超前进位加法器
  - Ripple Carry and Carry Look-Ahead Adders
  - RCA and CLA
---

# Ripple Carry and Carry Look-Ahead Adders · 串行进位与超前进位加法器

> [!SUMMARY] Quick recall · 英文速览
> Ripple carry computes each carry from the previous carry. Carry look-ahead expands that recurrence so several carries can be computed from the original inputs. Propagate has both OR and XOR conventions; state which one you use.

## Core Definition · 核心定义

第 $i$ 位输入 $A_i,B_i$，$C_i$ 为该位输入进位，$C_{i+1}$ 为输出进位。采用 XOR propagate：

$$G_i=A_iB_i,\quad P_i=A_i\oplus B_i,\quad C_{i+1}=G_i+P_iC_i,\quad S_i=P_i\oplus C_i.$$

$G_i$ (generate) 表示不管前级如何都产生进位；$P_i$ (propagate) 表示前级进位能够传到后级。

OR propagate $P_i^{OR}=A_i+B_i$ 也可用于同一个 carry recurrence，因为 $G_i=1$ 时已经保证 carry=1。但是 OR propagate 不能直接替代 sum 式中的 XOR。Neither convention changes the arithmetic result.

## Derivation · 展开进位链

$$C_1=G_0+P_0C_0,$$
$$C_2=G_1+P_1G_0+P_1P_0C_0,$$
$$C_3=G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0,$$
$$C_4=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0+P_3P_2P_1P_0C_0.$$

每一步把前级 $C_i$ 代入并展开。所有输入已经稳定后，CLA 能并行生成 carry，而 RCA 必须逐级等待。大 fan-in 的 AND/OR 门未必与二输入门一样快，所以“只需两层”是有条件的门模型。

## Worked Examples · 例题

**Carry propagation.** $A=1111,B=0000,C_0=1$。每位 $G_i=0,P_i=1$，所以 $C_1=C_2=C_3=C_4=1$，sum=0000，总和 16。这是典型贯穿全链的 carry 条件。

**Generate and kill.** $A=1010,B=0111,C_0=0$。按 $i=0,1,2,3$，$G=(0,1,0,0)$，$P=(1,0,1,1)$，得到 $C=(C_0,C_1,C_2,C_3,C_4)=(0,0,1,1,1)$，sum=0001；10+7=17。

**Timing model.** 假定每级 carry delay=450 ps，4-bit RCA 到最终 carry 的延迟是 $4\times450=1800$ ps，前提是 A/B 已经到达。若还需要最终 sum 的 XOR，计算该输出时应另加其延迟。不能把 carry-out 的延迟当成所有输出的延迟。

A simplified look-ahead path may pass through propagate/generate logic, an AND layer, and an OR layer. Add the delays on the actual path; do not compare a four-stage RCA with a CLA model that silently assumes unlimited fan-in.

## Method and Exam English · 求解与答题

1. Declare bit order and the propagate convention.
2. Compute each $G_i$ and $P_i$ from the operands.
3. Expand carry expressions from the recurrence.
4. Identify the path to the requested output and sum its delays.
5. Check both the full arithmetic value and the retained width.

**Self-check:** Can OR propagate be used in $S_i=P_i\oplus C_i$?

**Answer:** No. When A=B=1 and carry-in=0, OR propagate is 1, but the correct sum is 0. Use XOR propagate for the sum even if the carry network uses OR propagate.

## Connections · 相关笔记

[[Half Adder and Full Adder]], [[Two's Complement Representation]], [[Propagation Delay and Logic Hazards]], [[Setup and Hold Timing]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
