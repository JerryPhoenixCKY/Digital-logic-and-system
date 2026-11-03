---
tags:
  - ECE2050
  - sequential-logic
date: 2026-09-30
aliases:
  - 寄存器使能与复位
  - Register Enable and Reset
  - Enabled and resettable registers
---

# Register Enable and Reset · 寄存器使能与复位

> [!SUMMARY] Quick recall · 英文速览
> Enable chooses load or hold at the clock edge. Synchronous reset acts at an edge; asynchronous reset can act between edges. Priority among reset, load, enable, and hold must be specified.

## Core Definition · 核心定义

寄存器 (register) 由多位状态元件组成，通常共享 clock。对每一位，高有效 EN 的 enabled DFF：

$$Q^+=EN\cdot D+\overline{EN}\cdot Q.$$

EN=0 的保持用输出反馈到输入的 MUX 实现。不是把 clock 用普通 AND 随意截断；clock gating 的可靠实现需要专门时序约束。

## Reset and Set · 复位与置位

高有效 synchronous reset R：只在有效边沿执行，$Q^+=0$ if R=1，否则正常 load/hold。高有效 asynchronous reset：R=1 时不用等 clock 就把 Q 强制为 0。set/preset 对称地强制为 1。

If reset has priority over enable, the next-state rule is:

$$Q^+=\begin{cases}0,&R=1\\D,&R=0,EN=1\\Q,&R=0,EN=0.\end{cases}$$

This recurrence describes edge behavior for synchronous reset. For asynchronous reset, add the between-edge reset action to the waveform model; an edge-only table is not the whole behavior.

## Worked Examples · 例题

**Example 1.** 四位 Q 初值 1010，边沿时 EN=0,D=0011，Q 保持 1010；下次 EN=1，Q 变 0011；再下次 R=1,EN=1，reset priority 使 Q=0000。

**Example 2.** 在两个正沿之间 R 从 0 到 1：异步复位输出随 reset 延迟变 0；同步复位仍保持旧值，直到下一个正沿。两种设计的 HDL sensitivity list 与 if 条件位置不同。

**Example 3.** 高有效 synchronous set：$D_{effective}=S+D$，因为 S=1 时输入固定 1，S=0 时保留 D。仅在 capture edge 生效；这不等同于修改内部 FF 的 asynchronous preset pin。

## Timing Boundary · 时序边界

Reset assertion and release have different concerns. An asynchronous assertion can establish a state without the clock, but release near a clock edge may violate recovery/removal constraints. A synchronously released reset is often used to make restart consistent; this is an implementation practice, not a proof that every reset circuit is safe.

EN 与同步控制也是待采样的数据路径，需要满足 setup/hold。若同时要求 LOAD、EN、CLR，按 function table 的 priority 写分段式，再作波形；不能自行选择顺序。

## Method and Exam English · 方法与答题

1. List control polarity and synchronous/asynchronous behavior.
2. Write the priority from highest to lowest.
3. Record control values just before each edge.
4. Apply asynchronous events immediately when asserted.
5. Confirm that “hold” retains every bit, rather than loading zero.

**Question:** Does EN=0 force Q=0?

**Answer:** No. Enable LOW normally inhibits loading and retains the previous value. Reset is a separate control with its own polarity, timing, and priority.

## Connections · 相关笔记

[[D Latch and D Flip-Flop]], [[Multiplexer and Demultiplexer]], [[Shift Registers]], [[Counters]], [[Setup and Hold Timing]], [[VHDL Language and Modeling]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
