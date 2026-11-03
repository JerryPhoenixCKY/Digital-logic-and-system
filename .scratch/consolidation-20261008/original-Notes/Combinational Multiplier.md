---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 组合乘法器
  - Combinational Multiplier
  - Array multiplier
---

# Combinational Multiplier · 组合乘法器

> [!SUMMARY] Quick recall · 英文速览
> Binary multiplication creates AND-generated partial products and adds columns of equal weight. An m-bit unsigned operand times an n-bit operand needs up to m+n result bits.

## Core Definition and Derivation · 定义与推导

设 $A=\sum_{i=0}^{m-1}a_i2^i$，$B=\sum_{j=0}^{n-1}b_j2^j$，且本节为 unsigned：

$$AB=\sum_i\sum_j(a_ib_j)2^{i+j}.$$

partial product $p_{ij}=a_i b_j$ 用 AND 门产生，其权为 $2^{i+j}$。相同权列的两个位用 HA，三个位用 FA，carry 进入下一权列。乘法器是组合逻辑，不需要因为“有很多加法步骤”就引入 clock。

## Worked Example · 3×3 位乘法

$A=101_2=5$，$B=111_2=7$。六位对齐的三行部分积为：

| Multiplier bit | Row | Decimal value |
|---|---|---|
| $b_0=1$ | 000101 | 5 |
| $b_1=1$ | 001010 | 10 |
| $b_2=1$ | 010100 | 20 |
| Total | 100011 | 35 |

To design the network rather than merely calculate the product, name the column signals. $z_0=p_{00}$. A half adder combines $p_{10},p_{01}$ into $z_1,c_2$. At weight 4, a full adder combines $p_{20},p_{11},c_2$ into $s_2,c_3$, then a half adder combines $s_2,p_{02}$ into $z_2,d_3$. At weight 8, add $p_{21},p_{12},c_3$, then combine the sum with $d_3$. At weight 16, add $p_{22}$ and both carries from the previous weight; its sum and carry form $z_4,z_5$.

该列压缩方案需要 9 个 AND、3 个 HA、3 个 FA；它是一个有效拓扑，并非唯一最优电路。给每个中间 carry 命名，避免同一 carry 被遗漏或重复。

## Timing and Signed Boundary · 时序与有符号边界

The longest delay is the longest sensitizable path through the actual AND and adder network. Count both carry and sum arcs using the problem's delay model. Multiplying the number of all adders by one delay overestimates parallel sections and may underestimate a sum path.

Signed multiplication needs sign treatment: the MSB has negative weight in two's complement. Do not multiply raw negative patterns as unsigned and merely add a sign bit afterward. [[Signed Binary Multiplication and Division]] derives sign extension and wider results.

## Practical Examples and Review · 应用与复习

**Maximum value.** 两个 3-bit unsigned 最大值相乘：$7\times7=49=110001_2$，需要 6 位；5 位只能到 31。不是所有乘积都用满 6 位，但输出设计应覆盖最大情况。

**Signed case.** 4-bit `1011` 是 −5，`1010` 是 −6，乘积 +30，8-bit `00011110`。把两个原始码当 11 与 10 会得到 110，改变了问题。

**Exam question:** Why are partial products shifted before addition?

**Answer:** The multiplier bit at position j has weight $2^j$. Its AND-generated row represents A multiplied by that weight, so each row must be aligned j positions to the left before addition.

## Connections · 相关笔记

[[Binary Arithmetic]], [[AND Gate]], [[Half Adder and Full Adder]], [[Ripple Carry and Carry Look-Ahead Adders]], [[Propagation Delay and Logic Hazards]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
