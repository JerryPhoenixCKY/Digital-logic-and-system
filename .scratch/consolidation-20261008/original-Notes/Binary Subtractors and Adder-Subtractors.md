---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 二进制减法器与加减器
  - Binary Subtractors and Adder-Subtractors
  - Full subtractor
---

# Binary Subtractors and Adder-Subtractors · 二进制减法器与加减器

> [!SUMMARY] Quick recall · 英文速览
> A subtractor tracks borrow; an adder-subtractor computes subtraction by adding the two's complement. Difference and borrow have different meanings and must be derived separately.

## Core Definition · 核心定义

半减器 (half subtractor) 算 $A-B$；全减器再减输入借位 $B_{in}$。本篇 $B$ 是 subtrahend bit，$B_{in}$ 是 borrow-in，$B_{out}$ 是 borrow-out；名称不同，避免全部写成 B。

$$A-B-B_{in}=D-2B_{out}.$$

这是普通整数守恒：借 1 相当于从高位借来 2 个本位单位。差分位为模 2 结果。

## Derivation · 推导

$$D=A\oplus B\quad(HA\text{-style subtractor}),\qquad B_{out}=\bar AB\quad\text{when }B_{in}=0.$$

全减器：

$$D=A\oplus B\oplus B_{in},$$
$$B_{out}=\bar AB+\bar A B_{in}+BB_{in}.$$

For A=0, either B or borrow-in requires borrowing. For A=1, borrowing is needed only when both B and borrow-in are 1. This yields the same equation without guessing from the adder carry formula.

| A | B | $B_{in}$ | D | $B_{out}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |

## Adder-Subtractor · 共用加法器

对 n 位加减器，mode $M=0$ 加法，$M=1$ 减法：

$$S=A+(B\oplus\{n\{M\}\})+M\pmod{2^n}.$$

符号 $\{n\{M\}\}$ 表示 n 个相同 M 位的掩码。$M=1$ 时每个 $B_i$ 反相，初始进位为 1；$M=0$ 时 B 不变且初始 carry=0。

For unsigned subtraction implemented this way, carry-out=1 means no borrow, and carry-out=0 means borrow, under the stated equal-width convention. Signed overflow still requires the signed criterion; carry-out alone is insufficient.

## Worked Examples · 例题

**Borrow.** $A=0,B=1,B_{in}=1$，原式为 −2；$D=0,B_{out}=1$，右侧 $0-2=-2$，正确。

**Four-bit subtraction.** $3-5$: `0011 + 1010 + 1 = 1110`。无符号解释保留值为 14，存在借位；补码解释为 −2。$7-3$: `0111 + 1100 + 1 = 1 0100`，carry=1，无借位，结果 4。

**Decoder.** 变量顺序 $(B_{in},A,B)$ 时，difference 的 ON set 为 $\{1,2,4,7\}$，borrow 的 ON set 为 $\{1,4,5,7\}$。换变量顺序后索引会变，必须重编表。

## Pitfalls and Review · 易错点与复习

- A sum bit and difference bit both use XOR, but carry and borrow do not have the same equation.
- 补码减法必须“反相并加 1”；只反相是 one's complement。
- “Perform signed subtraction” requires stating the signed values and testing range overflow.

**Exam answer:** “The difference bit is the parity of A, B, and borrow-in. The borrow output is asserted exactly when B plus borrow-in exceeds A.”

## Connections · 相关笔记

[[Binary Arithmetic]], [[Two's Complement Representation]], [[Half Adder and Full Adder]], [[Decoder]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
