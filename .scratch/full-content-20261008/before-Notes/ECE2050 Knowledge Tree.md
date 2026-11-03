---
tags:
  - ECE2050
  - index
date: 2026-09-30
updated: 2026-10-08
aliases:
  - ECE2050 知识树
  - Knowledge Tree
  - 数字逻辑与系统知识树
  - 知识树
---

# ECE2050 Knowledge Tree · 知识树

> [!NOTE] Learning route · 学习路线
> 全库按章节组织为 **31 篇主线笔记**，每章 1–5 篇。先读正文中的定义、核心方程和重要提示；需要验证过程时，再展开同一小节的推导、例题与图示。术语可从 [[Glossary]] 反查。

**完整主线：** 数字模型 → 数值表示 → 逻辑与接口 → 布尔化简 → 组合设计与功能块 → 存储和采样 → 状态机与计数器 → 存储／可编程逻辑 → HDL 验证。

> [!IMPORTANT] 三条贯穿全课的检查
> **含义：** 位宽、编码、极性、事件与无效输入。**功能：** 方程、真值表与状态转换是否一致。**实现：** 电平、延迟、采样与物理接口是否满足假设。

## Ch1 · Digital Foundations · 数字基础

从电压、逻辑值与波形建立数字系统模型。

- ✅ [[Digital Foundations and Waveforms]] · **数字基础与波形** — Digital systems interpret continuous voltages as discrete symbols. Correct function, valid voltage levels, and valid sampling time are three separate requirements.

## Ch2 · Number Representation and Coding · 数值表示与编码

位权 → 位宽与符号 → 精度 → 数据含义 → 检错。

- ✅ ❗ [[Number Systems and Base Conversion]] · **数制与进制转换** — A radix defines digits and positional weights. Conversion preserves numerical value; an unlabelled bit pattern does not define its own interpretation.
- ✅ ❗ [[Binary Arithmetic and Signed Representation]] · **二进制运算与有符号表示** — Arithmetic uses positional weights. Fixed width determines which bits are retained; signed representation determines what those bits mean.
- ✅ ❗ [[Fixed-Point and Floating-Point Numbers]] · **定点数与浮点数** — Fixed point applies a fixed scale to an integer. Floating point stores a sign, exponent, and fraction; its range and precision are different properties.
- ✅ ❗ [[Data Coding and Character Representation]] · **数据编码与字符表示** — A code assigns bit patterns to meanings. BCD preserves decimal digits, Gray code preserves one-bit adjacency, and ASCII assigns codes to characters.
- ✅ ❗ [[Parity and Cyclic Redundancy Checks]] · **奇偶校验与循环冗余校验** — Parity checks the number of flipped bits modulo two. CRC checks polynomial divisibility; its guarantees depend on the generator and frame length.

## Ch3 · Gates and Electrical Interfaces · 逻辑门与电气接口

先判断布尔功能，再检查电压阈值与噪声预算。

- ✅ [[Logic Gates and Boolean Functions]] · **逻辑门与布尔函数** — A logic gate maps input bits to an output bit. Start with the truth table, then connect the algebraic expression, symbol, and waveform.
- ✅ [[Logic Levels and Noise Margins]] · **逻辑电平与噪声容限** — Output guarantees and input acceptance limits define compatibility. Noise margin is the difference between those limits, not the nominal supply voltage.

## Ch4 · Boolean Algebra and Minimization · 布尔代数与化简

模型与规则 → 真值表与标准式 → 最小覆盖。

- ✅ ❗ [[Boolean Algebra and Circuit Models]] · **布尔代数与组合电路模型** — Define a valid combinational model before manipulating equations. Boolean laws preserve a function, while composition rules constrain the physical topology.
- ✅ ❗ [[Boolean Forms and Algebraic Simplification 1]] · **布尔表达形式与代数化简** — Canonical forms record truth-table rows exactly. Simplification removes unnecessary literals while preserving every specified output.
- ✅ ❗ [[Karnaugh Map Minimization]] · **卡诺图化简** — Gray-code adjacency makes a group eliminate changing variables. Group 1s for SOP, 0s for POS, and use don't-cares only when the specification permits them.

## Ch5 · Combinational Analysis and Design · 组合逻辑分析与设计

从需求或连线得到函数，验证等价后选择实现，再测试故障。

- ✅ ❗ [[Combinational Logic Analysis and Design]] · **组合逻辑分析与设计** — Analysis derives a function from a circuit; design implements a specification. Both meet at a complete truth table and independently verified equations.
- ✅ ❗ [[Universal Gates and Bubble Pushing]] · **通用门与气泡推移** — NAND and NOR are complete construction sets. DeMorgan's theorem moves complements between gate inputs and outputs while exchanging the gate body.
- ✅ ❗ [[Digital Logic Troubleshooting]] · **数字逻辑故障诊断** — A fault test must activate the fault and propagate its effect. Detection and unique diagnosis are different goals.

## Ch6 · Combinational Building Blocks · 组合功能块

算术 → 比较与选择 → 显示转换 → 总线 → 延迟与冒险。

- ✅ [[Binary Arithmetic Circuits]] · **二进制算术电路** — Build arithmetic from one-bit cells. Carry logic sets adder delay; inversion plus carry-in reuses an adder for subtraction.
- ✅ [[Comparison Decoding and Selection]] · **比较译码与选择电路** — Compare values, decode codes into lines, select one winning request, then route data. Codes, winner masks, and active polarity are different interfaces.
- ✅ [[Seven-Segment Display and Code Conversion]] · **七段显示与码制转换** — Segment truth tables describe lit shapes; electrical polarity maps those commands to levels. BCD-to-binary conversion preserves the decimal value.
- ✅ [[Tri-State Buffers and Bus Drivers]] · **三态缓冲与总线驱动** — High impedance releases a shared line. It is neither a driven zero nor an unknown Boolean value; bus ownership prevents competing drivers.
- ✅ [[Propagation Delay and Logic Hazards]] · **传播延迟与逻辑冒险** — The longest path bounds settling; the shortest path bounds the earliest change. Different path delays can create glitches in an otherwise equivalent Boolean function.

## Ch7 · State and Storage Elements · 状态与存储元件

反馈保持 → 锁存与边沿采样 → 激励与控制优先级。

- ✅ ❗ [[Sequential Logic and Flip-Flops]] · **时序逻辑与触发器** — State records history. Distinguish level-sensitive storage from edge-triggered storage, then add explicit enable and reset priorities.

## Ch8 · Shift and Pulse Applications · 移位与脉冲应用

移位反馈产生扫描顺序，脉冲与捕获机制形成输入接口。

- ✅ [[Shift Registers and Ring Counters]] · **移位寄存器与环形计数器** — A shift register moves old-state bits simultaneously. Ring and Johnson counters choose the feedback path to create cyclic patterns.
- ✅ [[One-Shots and Pulse Applications]] · **单稳态与脉冲应用** — A one-shot produces a timed excursion after a trigger. A registered edge detector instead produces an event pulse measured in clock cycles.
- ✅ [[Keyboard Scanning and Encoding]] · **键盘扫描与编码** — Scan one line, sense the other dimension, encode a valid position, then capture once per qualified key event.

## Ch9 · State Machines and Timing · 状态机与时序

先设计状态与转移，再检查路径和跨域协议。

- ✅ ❗ [[Finite State Machine Design and Applications]] · **有限状态机设计与应用** — State summarizes the relevant past. Define state meaning before encoding, derive complete transitions, then verify traces and unused states.
- ✅ ❗ [[Sequential Timing and Clock Domain Crossing]] · **时序约束与时钟域跨越** — Setup limits the latest arrival; hold limits the earliest arrival. Clock-domain crossing requires a transfer protocol beyond ordinary synchronous path checks.

## Ch10 · Counters and Digital Clocks · 计数器与数字时钟

从状态序列推激励，按接受的进位同步级联。

- ✅ ❗ [[Counter Design and Digital Clocks]] · **计数器设计与数字时钟** — A counter is a specified state sequence. Derive next state from old state, recover from invalid states, and enable higher digits on accepted rollover.

## Ch11 · Memory and Programmable Logic · 存储与可编程逻辑

存储组织与保持机制 → 查表和共享逻辑 → FPGA 实现。

- ✅ [[Memory Organization and Technologies]] · **存储组织与存储技术** — Depth and width define memory capacity. Technology explains how a bit is retained, read, written, and lost.
- ✅ [[Programmable Logic and FPGA]] · **可编程逻辑与FPGA** — A ROM or LUT stores a truth table. A PLA shares product terms. An FPGA combines programmable logic, state elements, routing, and constrained physical implementation.

## HDL · VHDL and Project Verification · VHDL 与项目验证

语言语义 → 完整建模 → 独立验证 → 结构化项目。

- ✅ ❗ [[VHDL Modeling and Verification]] · **VHDL建模与验证** — VHDL describes concurrent hardware. A testbench drives the design and checks an independent reference model; simulation success is one layer of evidence.
- ✅ ❗ [[Structural Shift Register Project]] · **结构化移位寄存器项目** — Structural design instantiates reusable state cells and explicitly connects next-state logic. Bit order, shift direction, and control priority define correctness.

## Review · Integrated Review · 综合复习

闭卷回忆核心方程，按题意建模，用边界与反例验证。

- ✅ [[Exam Review and Problem Solving]] · **考试复习与解题方法** — Read the specification, choose the model, derive independently, and test the boundaries. A familiar-looking answer is not evidence of correctness.

## Study Checkpoints · 阶段检查

1. **Ch1–3：** 能解释一个位串的数值与含义，并分别计算其逻辑输出和电气裕量。
2. **Ch4–6：** 能从需求或门图建立函数，化简、实现并穷举验证指定输入。
3. **Ch7–10：** 能逐边沿追踪状态，推导激励，并检查建立／保持、未用态恢复和级联条件。
4. **Ch11 与 HDL：** 能组织存储接口，解释查表实现，并用独立参考模型验证硬件描述。

✅ 表示已有完整主线内容；❗标记需要反复练习的章节。考前按 [[Exam Review and Problem Solving]] 检查条件、方程、边界与英文答句。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
