---
tags:
  - ECE2050
  - programmable-logic
date: 2026-09-30
aliases:
  - 现场可编程门阵列
  - Field-Programmable Gate Array
  - FPGA
---

# Field-Programmable Gate Array · 现场可编程门阵列

> [!SUMMARY] Quick recall · 英文速览
> An FPGA maps hardware descriptions onto configurable logic, registers, routing, and other resources. Simulation checks a model; implementation and timing analysis check whether the mapped design meets the physical constraints.

## Core Definition · 核心定义

FPGA 是可在现场配置的集成电路。教学 logic element 通常包括 LUT、FF、MUX；器件还可有 carry resources、RAM、DSP 与 I/O。具体 LUT 输入数和 architecture 依器件，不应把某个例子的 four-input LUT 当成所有 FPGA 的定义。

LUT 执行 combinational function，FF 保存 runtime state，routing 连接模块。HDL 描述的多个 concurrent statements 对应并行硬件；不是 CPU 把每行逐条执行。

## Design Flow · 设计流程

```mermaid
flowchart LR
  RTL[Specify and write HDL] --> Sim[Functional simulation]
  Sim --> Synth[Synthesis and resource mapping]
  Synth --> Impl[Placement and routing]
  Impl --> Timing[Timing and constraint review]
  Timing --> Config[Generate configuration]
  Config --> Board[Program and verify on board]
```

Synthesis 将行为/结构转为可实现逻辑；implementation 决定资源放置与连接；bitstream/configuration 配置器件。Behavioral simulation 成功不能代替物理 timing review。

## Worked Example · 四位 enabled register

功能 $Q^+=EN?D:Q$：需要保存4位，因此通常对应4个 FF；输入选择由 MUX/FF内 enable resource 实现。若同 clock 下 q<=d，没有 EN，不能因为时钟 HIGH 持续很久就让 q 透明跟随。

**LUT capacity.** 一个4输入、1输出 LUT 存16个 truth bits。要直接表示任意5输入、1输出函数，完整 table有32 bit；可分解为两个4-input cofactors 再 MUX，或按目标设备其他资源实现。资源估算不是实际综合 report。

## Constraints and Interfaces · 约束与接口

必须指定 top-level ports、target device、clock period、I/O pin mapping 与电气标准，涉及板上连接时核对该 board 的资料。讲义中的旧版 Vivado 菜单和示例引脚是历史演示；本篇保留阶段逻辑，不当作当前安装版本的操作保证。

An unconstrained clock can leave a design without a meaningful required frequency. An incorrect pin constraint can produce the right simulated waveform on the wrong physical pin. These are different failures, so inspect both logic and interface constraints.

不把普通输入按钮当 clock；先同步/debounce 并产生 enable event。内部多驱动 `X` 或未赋值 latch 应在 simulation/synthesis warnings 中追查。

## Practical Review · 实践与复习

| Evidence | Supports | Does not by itself prove |
|---|---|---|
| Functional simulation | RTL behavior on tested stimuli | Timing closure or electrical wiring |
| Synthesis report | Mapped registers and logic | Correct external pin assignment |
| Timing report | Constrained timing paths | Correct functional specification |
| Board observation | Tested physical behavior | All untested states and interfaces |

**Exam question:** Why does a memory-based LUT still implement combinational logic?

**Answer:** Its configuration bits define a fixed truth table during operation. Current inputs address that table and determine the output. Clocked user state requires a register or another state element; configuration memory alone does not make the function depend on prior inputs.

## Connections · 相关笔记

[[Read-Only Memory and Programmable Logic Arrays]], [[Sequential Logic]], [[VHDL Language and Modeling]], [[Structural Shift Register Project]], [[Testbench and Functional Verification]], [[Setup and Hold Timing]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
