---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 多路选择器与分配器
  - Multiplexer and Demultiplexer
  - MUX and DEMUX
---

# Multiplexer and Demultiplexer · 多路选择器与分配器

> [!SUMMARY] Quick recall · 英文速览
> A MUX selects one data input for one output. A DEMUX routes one data input to one selected output. Shannon expansion turns a MUX into a general Boolean-function implementation.

## Core Definition · 核心定义

2:1 MUX 的 select S 决定选 D0 或 D1：

$$Y=\bar SD_0+SD_1.$$

4:1 MUX 用两位 $S_1S_0$，$Y=D_{2S_1+S_0}$。select 是**地址/控制**，data 是被选择的值。$2^k$:1 需要 k 条 select，不能混淆 data count 与 select count。

## Derivation · Shannon expansion

$$F(A,X)=\bar A F(0,X)+A F(1,X).$$

两种 A 的情况互斥且穷尽，所以这就是 2:1 MUX。对两个 select 重复分解，可以让 4:1 MUX 实现三变量函数，其 data inputs 分别为 0、1、剩余变量或其补。

When reducing a three-variable truth table into four MUX data inputs, inspect each pair of rows for the remaining variable C. Output pair 00 gives constant 0; 11 gives constant 1; 01 gives C; 10 gives NOT C. This method prevents guessing.

## Worked Examples · 例题

**XOR using a MUX.** 选 A：A=0 时 $F=B$，A=1 时 $F=\bar B$，因此 D0=B、D1=NOT B。A=1,B=0 → 1，符合 XOR。

**Majority.** $F=AB+AC+BC$，select=AB。四组 cofactor 为 D0=0、D1=C、D2=C、D3=1。检查 011 → D1=C=1；100 → D2=C=0。

**Parity.** $F=A\oplus B\oplus C$，select=AB，data=(C,NOT C,NOT C,C)。C=0 时 data 为 0,1,1,0；C=1 时正好反相。

## Demultiplexing · 分配

1:4 DEMUX 的单数据输入为 D，$Y_i=Dm_i(S_1,S_0)$。D=0 时所有输出 0；D=1 时相当于 decoder。选择 10 且 D=1：输出 Y2=1，其余 0。

A decoder's enable can serve as the data input only when the device's enable and output polarity produce the required DEMUX function. An active-low decoder does not automatically give positive-logic DEMUX outputs.

## Pitfalls and Practical Use · 误区与应用

- MUX is many-to-one; DEMUX is one-to-many.
- 使能关闭后的输出由 device table 决定，不必然 Z。
- Do not leave unused inputs floating; assign defined constants when implementing logic.
- [[Tri-State Buffers and Bus Drivers]] shows a different physical way to select a bus source.
- A counter plus a MUX can serialize a stored word, provided the word stays stable during the full scan.

**Exam question:** Implement a three-variable function using a 4:1 MUX. What are the first two decisions?

**Answer:** Choose and order the two select variables, then derive the four cofactors with respect to the remaining variable. State the enable condition before connecting the data inputs.

## Connections · 相关笔记

[[Truth Table and Boolean Expression]], [[Decoder]], [[Magnitude Comparator]], [[Register Enable and Reset]], [[Shift Registers]], [[Read-Only Memory and Programmable Logic Arrays]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
