---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 半加器与全加器
  - Half Adder and Full Adder
  - HA and FA
---

# Half Adder and Full Adder · 半加器与全加器

> [!SUMMARY] Quick recall · 英文速览
> A half adder adds two bits; a full adder also accepts a carry-in. The sum bit is parity and the carry-out is majority. Repeating full adders builds a wider arithmetic unit.

## Core Definition · 核心定义

半加器 (half adder) 输入 $A,B$，输出 sum $S$、carry $C$。全加器 (full adder) 另有输入进位 $C_{in}$。用整数守恒解释位权：

$$A+B=S+2C,\qquad A+B+C_{in}=S+2C_{out}.$$

等号两边这里是普通整数加法；下述 Boolean 式中的 $+$ 是 OR。不能混用两种含义。

## Derivation · 推导

总和的最低位是奇偶性：$S=A\oplus B$（HA），$S=A\oplus B\oplus C_{in}$（FA）。总和至少为 2 时需要进位，即至少两个输入为 1：

$$C=AB,\qquad C_{out}=AB+AC_{in}+BC_{in}=AB+(A\oplus B)C_{in}.$$

The first half adder gives $p=A\oplus B$ and $g=AB$. The second adds $p$ and $C_{in}$, giving $S=p\oplus C_{in}$ and $h=pC_{in}$. OR the two carry signals: $C_{out}=g+h$. They cannot both be 1 because $AB=1$ forces $p=0$.

| A | B | $C_{in}$ | S | $C_{out}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

## Worked Examples · 例题

**All HIGH.** $1+1+1=3=11_2$，因此 $S=1,C_{out}=1$。全加器不是“输入全 1 时 sum=0”，那只适用于没有 carry-in 的半加器。

**Four-bit addition.** $A=1100,B=1100,C_0=0$。从 LSB 起，前两位各为 0；第 2 位 $1+1+0$ 得 $S_2=0,C_3=1$；最高位 $1+1+1$ 得 $S_3=1,C_4=1$。总输出 `1 1000`=24，低四位为 8。

For unsigned interpretation, carry-out indicates that the four-bit result is insufficient. For two's complement, both inputs represent −4 and the four-bit result 1000 represents −8, so there is no signed overflow. The same physical adder supports both interpretations.

**Decoder implementation.** 若 ABC 中 C 表示 carry-in，$S=\Sigma m(1,2,4,7)$，$C_{out}=\Sigma m(3,5,6,7)$。高有效 [[Decoder]] 输出用 OR 合并；低有效输出则用 NAND 合并相应 minterms。

## Method and Review · 方法与复习

- Keep the initial carry explicit; tie it to 0 only for ordinary addition.
- Name every intermediate carry in a wider adder.
- 用 $A+B+C_{in}=S+2C_{out}$ 逐行校验，能够同时检查两个输出。
- The full-adder sum is a three-input parity function, not an “exactly one HIGH” detector.

**Exam question:** Can a full adder be made from two half adders alone?

**Answer:** Two half adders produce the partial sums and carries; an OR function is also needed to combine the carries. Omitting that function leaves the carry-out incomplete.

## Connections · 相关笔记

[[Binary Arithmetic]], [[Exclusive-OR Gate]], [[Parity Bit]], [[Ripple Carry and Carry Look-Ahead Adders]], [[Combinational Multiplier]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
