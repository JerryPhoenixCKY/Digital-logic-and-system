---
tags:
  - ECE2050
  - registers
date: 2026-09-30
aliases:
  - 移位寄存器
  - Shift Registers
  - SISO SIPO PISO PIPO
---

# Shift Registers · 移位寄存器

> [!SUMMARY] Quick recall · 英文速览
> A shift register stores a word and moves each bit to a neighboring stage at the clock edge. Every stage uses the old state. Serial order, displayed bit order, and physical drawing direction must be stated explicitly.

## Core Definition · 核心定义

定义 4-bit 状态向量 $Q_3Q_2Q_1Q_0$，Q3 为 MSB。本篇 right shift 指向低位：

$$Q^+=\{SR,Q_3,Q_2,Q_1\}.$$

left shift 指向高位：$Q^+=\{Q_2,Q_1,Q_0,SL\}$。SR/SL 是对应边界的 serial input。讲义电路若把 Q0 画在左侧，“向图右移”可能对应位编号增加；必须先写节点更新式，不能从词语猜数值右移。

| Type | Entry | Observation | Typical use |
|---|---|---|---|
| SISO | One bit per edge | Last stage | Sample delay |
| SIPO | Serial | Whole word | Receive/expand inputs |
| PISO | Parallel load | Serial | Transmit/serialize |
| PIPO | Parallel | Parallel | Store a word |

PIPO 本身可只是并行寄存器；“parallel” 不自动表示每个周期也会 shift。

## Derivation · Universal register

本篇 mode=$S_1S_0$：00 hold、01 right、10 left、11 parallel load。每个 D 输入前的 MUX 选择旧自身、相邻旧位、另侧旧位或并行输入。reset 若有则明确优先级。

All flip-flops share the clock. Their outputs change together logically, after physical clock-to-Q delays. Updating the stages one at a time with new values would incorrectly propagate a bit through the whole register in one edge.

## Worked Example 1 · 左右混合

初态 Q=1011，SR=0，SL=1：

| Edge | Mode | New $Q_3Q_2Q_1Q_0$ |
|---|---|---|
| 0 | Initial | 1011 |
| 1 | Right | 0101 |
| 2 | Right | 0010 |
| 3 | Left | 0101 |
| 4 | Hold | 0101 |
| 5 | Load 1100 | 1100 |

检查 right step：1011 无符号是 11，右移补 0 得 floor(11/2)=5。left shift 有限位宽会丢掉 MSB，不能总当作精确乘 2。

## Worked Example 2 · 串入和时延

初值 0000，right shift serial input 按时间为 1,0,1,1，状态为 1000、0100、1010、1101。最早输入的 bit 最终到 Q0，所以按 Q3…Q0 阅读得到输入时间顺序的反向。

An n-stage pipeline whose recurrence is $Q_0[k+1]=X[k]$, $Q_i[k+1]=Q_{i-1}[k]$ gives $Q_{n-1}[k+n]=X[k]$. From the first capture edge to the last-stage capture edge there are n−1 edge intervals. Calling its discrete input-to-output delay n cycles uses the stated pre-edge input indexing; define the timing reference to avoid an off-by-one claim.

![[serial-shift-trace.svg]]
*Figure · 以Q3Q2Q1Q0读状态，串入1、0、1、1；每个正沿都用旧状态生成四位新状态。图中的shifted out是该边沿前的旧Q0。*

## Applications and Review · 应用与复习

PISO load 1011，若每次先观察 Q0 再 right shift，则发送 1,1,0,1（LSB first）。若输出取 Q3 并 left shift，则可以 MSB first；两种都能工作，但协议必须一致。

For a serial link, wire count is reduced at the cost of several bit intervals per word. A UART adds framing and sampling rules; a bare shift register alone is not a complete UART.

**Exam answer:** “I define the stored word as Q3Q2Q1Q0. At each active edge I compute all four new bits from the pre-edge state and the sampled direction input, then update the entire word.”

## Serial interfaces and matrix scanning · 串行接口与矩阵扫描

SIPO converts a defined serial bit sequence into a parallel word; PISO does the reverse. A complete UART additionally defines framing, bit timing, sampling, and any parity/stop fields. A shift register is one building block, not a complete asynchronous communication protocol.

串入顺序决定字节位序；例如从Q3串入四位1011，最终为1101，不能自动当成1011。按目标bit order安排输入，或在输出解释中明确重排。课程的 [[Keyboard Scanning and Encoding]] 用环形寄存器移动one-cold行选择，再由编码器与key-code register保存位置。

## Connections · 相关笔记

[[D Latch and D Flip-Flop]], [[Multiplexer and Demultiplexer]], [[Register Enable and Reset]], [[Ring and Johnson Counters]], [[Cyclic Redundancy Check]], [[Structural Shift Register Project]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
