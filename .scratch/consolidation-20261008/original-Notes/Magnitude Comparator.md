---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 数值比较器
  - Magnitude Comparator
  - Digital comparator
---

# Magnitude Comparator · 数值比较器

> [!SUMMARY] Quick recall · 英文速览
> Equality requires equality at every bit. Magnitude is determined by the highest-order unequal bit. A lower-order mismatch matters only when all higher bits are equal.

## Core Definition · 核心定义

本篇先比较同宽 unsigned $A,B$，输出 $E=(A=B)$，$G=(A>B)$，$L=(A<B)$，高有效。稳定有效输入下恰好一个输出为 1。

## Derivation · 从一位到多位

一位：$e_i=\overline{A_i\oplus B_i}$，$g_i=A_i\bar B_i$，$l_i=\bar A_iB_i$。

两位且 bit 1 为 MSB：

$$E=e_1e_0,\qquad G=g_1+e_1g_0,\qquad L=l_1+e_1l_0.$$

四位：$G=g_3+e_3g_2+e_3e_2g_1+e_3e_2e_1g_0$，$L$ 对应把 g 换成 l，$E=e_3e_2e_1e_0$。低位判断被高位相等条件门控。

The first unequal position determines the result because its weight exceeds the sum of all lower weights. For bit k, $2^k>2^k-1$, so lower bits cannot reverse that decision.

## Worked Examples · 例题

**Example 1.** $A=10,B=01$：$g_1=1$，所以 G=1；低位的 $l_0=1$ 被 $e_1=0$ 屏蔽。若对所有 $g_i$ 直接 OR，会把低位的重要性看得过大。

**Example 2.** $A=1010,B=1001$，最高两位相等，bit1 首次不同且 A=1，故 A>B。10>9 验证。

**Cascading.** 两个 4-bit comparator 比较 8 位。低位模块比较结果接入高位模块的 cascade inputs；高位只有本地相等时才接受低位结论。最底层初始化为 equal=1、greater=less=0。不要把加法器的 carry chain 接法套成同名但无含义的信号。

**Signed boundary.** 同一 `1000` 与 `0111`：unsigned 是 8>7；4-bit two's complement 是 −8<7。先比较符号，符号相同再按适当位串规则比较；等宽同符号补码的 unsigned 顺序一致。

## Application · 最小值选择器

要输出 $\min(A,B)$，用 G 控制 [[Multiplexer and Demultiplexer]]，G=1 选 B，否则选 A。若题目规定 A=B 为 don't-care，可利用这些行化简；这是接口的特例，不改变比较器本身的 equality 定义。

## Method and Exam English · 方法与答题

- Start at the MSB, and continue only while the bits are equal.
- 明确 active-HIGH outputs；输出名 A>B 不是把 A 与 B 导线直接相减。
- Exhaustively test $2^{2n}$ operand pairs for a small n-bit comparator.

**Self-check:** Does XNOR on the two MSBs alone prove equality?

**Answer:** No. Every corresponding pair must be equal; AND all bitwise XNOR results. For two-bit inputs 10 and 11, the MSBs match but the numbers differ.

## Connections · 相关笔记

[[Exclusive-NOR Gate]], [[Two's Complement Representation]], [[Combinational Logic Design]], [[Encoder and Priority Encoder]], [[Cascaded Counters and Digital Clocks]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
