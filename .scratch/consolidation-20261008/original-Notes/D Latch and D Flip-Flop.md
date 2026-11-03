---
tags:
  - ECE2050
  - sequential-logic
date: 2026-09-30
aliases:
  - D锁存器与D触发器
  - D Latch and D Flip-Flop
  - D storage elements
---

# D Latch and D Flip-Flop · D锁存器与D触发器

> [!SUMMARY] Quick recall · 英文速览
> A D latch is level-sensitive and transparent during its enabled level. A D flip-flop is edge-triggered and captures one value at the active clock edge. They have different timing behavior despite sharing a data input.

## Core Definition · 核心定义

高电平透明 D latch 用 E 使能：E=1 时 Q 跟随 D，E=0 时保持。对合法二值稳态模型：

$$Q^+=ED+\bar EQ.$$

正沿 DFF 则在 rising edge 上 $Q^+=D$，边沿之间保持。三角形 clock 符号表示边沿触发；若三角形前有气泡，通常表示 falling edge。

## Derivation · 消除 SR 禁态

由 [[Set-Reset Latch]] 的高有效 SR 型，取 $S=ED,R=E\bar D$。E=0 时 S=R=0 保持；E=1 时只有一个控制有效，因此不会产生 S=R=1。

Two D latches controlled on opposite clock levels form an idealized master-slave DFF. At CLK=0, the master tracks D while the slave holds. When CLK rises, the master closes and the slave opens, transferring the captured master value to Q. Practical implementation must avoid uncontrolled overlap of transparency windows.

## Comparison · 对比

| Feature | D latch | Positive-edge DFF |
|---|---|---|
| Sensitive event | Entire enabled level | LOW→HIGH edge |
| Q can follow D mid-HIGH | Yes | No |
| Storage while inactive | Holds | Holds between edges |
| Basic HDL pattern | Incomplete level conditional | `rising_edge(clk)` |

## Worked Examples · 波形例题

**Example 1.** CLK 0→1 时 D=0；CLK 保持 1 时 D 变 1；CLK 1→0 时 D 仍 1。D latch：先 0，再跟随为 1，下降后保持 1。正沿 DFF：正沿采 0，中途保持 0；要等下一个正沿才可能采 1。

**Example 2.** 有效正沿前 D 依次为 1,0,1,1，DFF 初值 0；边沿后 Q 为 1,0,1,1。每次值只在 clock-to-Q 延迟后出现在物理输出，不是刚改变 D 就输出。

**Example 3.** DFF 的 D 接 NOT Q。每个正沿 $Q^+=\bar Q$，输出每两次 clock 才完成一个周期，所以 $f_Q=f_{clk}/2$。该连接实现无使能的 toggle function。

## Assumptions and Pitfalls · 条件与误区

The input must satisfy setup and hold around the capture event. For a latch, the closing event is important; while open, propagation from D to Q is also relevant. A transparent latch cannot be treated as an edge-triggered register by merely drawing its output changes at edges.

- Rising-edge triggering is a symbol/HDL property, not a universal property of every FF.
- 没有 reset 时，实际初态未必已知；例题初态须声明。
- “Sequential statements” in VHDL does not automatically mean sequential hardware.

## Exam English · 英文答题

**Question:** Why does Q remain unchanged when D changes while CLK is HIGH in a positive-edge DFF?

**Answer:** The flip-flop samples only on the LOW-to-HIGH clock transition. A later data change is outside that capture event, so the stored state remains unchanged until the next active edge, provided no asynchronous control is asserted.

## Connections · 相关笔记

[[Digital Waveforms]], [[Register Enable and Reset]], [[JK and T Flip-Flops]], [[Setup and Hold Timing]], [[VHDL Language and Modeling]], [[Shift Registers]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
