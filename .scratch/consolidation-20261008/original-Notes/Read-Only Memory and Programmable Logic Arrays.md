---
tags:
  - ECE2050
  - memory
date: 2026-09-30
aliases:
  - ROM与可编程逻辑阵列
  - Read-Only Memory and Programmable Logic Arrays
  - ROM LUT PLA PAL
---

# Read-Only Memory and Programmable Logic Arrays · ROM与可编程逻辑阵列

> [!SUMMARY] Quick recall · 英文速览
> A ROM implements a truth table by addressing stored outputs. A PLA implements selected product terms and OR combinations. A LUT is a small programmable truth table used inside FPGA logic.

## Core Definition · 核心定义

用 N-bit 输入作为地址，M-bit stored word 作为 M 个输出，就把 truth table 写入 $2^N\times M$ array。ROM 的 address decoder 产生所有 minterms；output connections/data 指定哪些行给1。

PLA (programmable logic array) 有可配置 AND 与 OR 阵列，按所需 product terms 实现 SOP；PAL 的经典模型为 programmable AND、fixed OR。这里 programmability 指配置连接；固定结构/布线资源不等于“所有连接不可编程”。

## Derivation · ROM 编程表

要求地址 A1A0 时输出 $(X,Y,Z)=(A_1\oplus A_0,A_1+A_0,A_1A_0)$：

| Address | X | Y | Z | Stored XYZ |
|---|---|---|---|---|
| 00 | 0 | 0 | 0 | 000 |
| 01 | 1 | 1 | 0 | 110 |
| 10 | 1 | 1 | 0 | 110 |
| 11 | 0 | 1 | 1 | 011 |

Capacity=4×3=12 bit。若存储输出顺序改为 ZYX，word 必须相应重排；所有 bit 格子的 dots/0/1 都应按明确极性读。

The address bits select a row; they are not ANDed numerically with the stored word. The output is the entry stored at that row, after the specified access delay.

## Worked Example · PLA 共享乘积

要求 $X=\bar ABC+A\bar BC$，$Y=\bar AB$。定义 $P_1=\bar ABC$、$P_2=A\bar BC$、$P_3=\bar AB$；X=P1+P2，Y=P3。若另一个输出也用 P1，可共享该 product term。

| Product | A | B | C | Connect to X | Connect to Y |
|---|---|---|---|---|---|
| P1 | Complement | True | True | Yes | No |
| P2 | True | Complement | True | Yes | No |
| P3 | Complement | True | Unused | No | Yes |

“Unused” in the AND-array table means omit that literal from the product; it does not mean drive an input wire to floating X. For A,B,C=0,1,1, P1=P3=1, giving X=Y=1. For 1,0,1, X=1,Y=0.

## ROM versus PLA versus LUT · 对比

- ROM/LUT：explicitly store every input combination，适合任意 truth table。
- PLA：store/select useful implicants，适合可共享且简化后的 SOP。
- N-input single-output LUT needs $2^N$ configuration bits; a 4-input LUT needs16。
- A larger logic function may use several LUTs and routing; a LUT's stored table does not by itself add sequential state to the user function.

Configuration storage is different from runtime state. A LUT output can be combinational even though its truth table is stored in memory. A separate FF produces clocked behavior.

## Method and Exam English · 方法与答题

1. Fix input address order and output bit order.
2. Enumerate the full truth table for ROM/LUT.
3. For PLA, minimize each output and identify shareable products.
4. Check selected-row and connection polarity.
5. Confirm the timing of read versus registered output.

**Exam answer:** “The ROM stores the output vector for each address pattern. The PLA instead generates selected product terms and combines them into outputs. Both realize the specified Boolean functions, but their internal representations and resource costs differ.”

## Connections · 相关笔记

[[Sum-of-Products Form]], [[Minterm and Maxterm]], [[Decoder]], [[Memory Arrays and Expansion]], [[Field-Programmable Gate Array]], [[Seven-Segment Display and Code Conversion]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
