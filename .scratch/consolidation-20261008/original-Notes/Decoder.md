---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 译码器
  - Decoder
  - Binary decoder
---

# Decoder · 译码器

> [!SUMMARY] Quick recall · 英文速览
> An n-to-$2^n$ decoder selects one output for each input code. With active-high outputs, each selected line is a minterm. With active-low outputs, each line is its complement.

## Core Definition · 核心定义

2-to-4 decoder 输入 $A_1A_0$，高有效 enable E。正逻辑输出：

$$Y_0=E\bar A_1\bar A_0,\ Y_1=E\bar A_1A_0,\ Y_2=EA_1\bar A_0,\ Y_3=EA_1A_0.$$

若 E=0，四个输出全 0；若 E=1，恰好一条为 1。one-hot 描述有效的输出；低有效译码器是 one-cold，disabled 时通常全 HIGH，仍须看给定 function table。

## Derivation · 为什么是 minterm

输入的一行由每个变量取正或补的唯一乘积描述。decoder 输出正好实现这些乘积，因此 $F=\Sigma m(S)$ 可以 OR 集合 S 对应的输出。

With active-low outputs $L_i=\bar m_i$, DeMorgan's law gives $F=\overline{\prod_{i\in S}L_i}$. Use a NAND across the selected LOW-active lines. Simply OR-ing them usually produces the wrong polarity.

## Worked Examples · 例题

**XOR.** $F(A_1,A_0)=\Sigma m(1,2)$。高有效输出 $F=Y_1+Y_2$；低有效输出 $F=\overline{L_1L_2}$。输入 01 时一条所选线有效，F=1；11 时两条所选低有效线都 HIGH，NAND=0。

**Full adder.** 输入 ABC，C 是 carry-in。sum 选 1,2,4,7；carry 选 3,5,6,7。先标清 decoder 的 A0 是否接 C，不能凭图中上下位置猜 MSB。

**Expansion.** 用两个 2-to-4 块构造 3-to-8：低两位同时接两块，高位 A2=0 使能低编号块，A2=1 使能高编号块。最终 index=$4A_2+2A_1+A_0$。disabled block 不应驱动一个有效输出。

## Enable and Pin Constraints · 使能与引脚条件

Enable inputs can have mixed polarity. A device requiring one HIGH and two LOW enables must receive that exact combination. Translate a named chip's table into an enable predicate first; do not assume every enable pin is active-HIGH.

例如 74HC154 教学模型的两个外部使能为低有效：两者都 LOW 才选一路低输出。内部可能用一个正逻辑 E 表示“已使能”，这个 E 与外部引脚不是同一极性的信号。器件接线若依赖具体 pin number，应核对该器件资料。

## Method and Review · 方法与复习

1. Write the decoder's bit ordering and enabled condition.
2. Determine whether selected outputs are HIGH or LOW.
3. Map input rows to output indices.
4. Choose OR, NAND, or polarity conversion accordingly.
5. Check both an ON row and an OFF row, then enumerate all rows.

**Self-check:** An enabled 3-to-8 decoder has input 101. Which line is selected?

**Answer:** Line 5. Its voltage is 1 for active-HIGH outputs or 0 for active-LOW outputs.

## Connections · 相关笔记

[[Minterm and Maxterm]], [[Half Adder and Full Adder]], [[Binary Subtractors and Adder-Subtractors]], [[Encoder and Priority Encoder]], [[Memory Arrays and Expansion]], [[Seven-Segment Display and Code Conversion]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
