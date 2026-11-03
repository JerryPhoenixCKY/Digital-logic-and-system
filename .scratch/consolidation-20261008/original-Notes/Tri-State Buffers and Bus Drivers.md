---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
aliases:
  - 三态缓冲器与总线驱动
  - Tri-State Buffers and Bus Drivers
  - Three-state logic
---

# Tri-State Buffers and Bus Drivers · 三态缓冲器与总线驱动

> [!SUMMARY] Quick recall · 英文速览
> A tri-state buffer outputs 0, 1, or high impedance Z. Z disconnects the driver; it is not a third Boolean value and does not force the bus LOW.

## Core Definition and Validity · 定义与条件

三态缓冲器 (tri-state buffer) 在使能有效时驱动数据，关闭时呈高阻 (high impedance)。本篇用高有效 EN；实际符号若有气泡，则有效极性相反。

| EN | D | Output |
|---|---|---|
| 0 | X | Z |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

总线 (bus) 允许多个潜在驱动器，但同一时刻须由协议保证只有一个普通推挽输出有效。[[Combinational Circuit]] 的单驱动模型仍适用于每个有效工作状态；三态共享是明确管理的例外。

## Mechanism · 机制

In a two-source bus selector, one driver is enabled when select=0 and the other when select=1. If both are disabled, the bus may float unless another defined circuit provides a level. If both are enabled and disagree, there is contention, not a logical OR operation.

VHDL `std_logic` resolution can report conflicting drivers as `X`; it does not make that physical connection safe. Internal FPGA tri-state descriptions may be implemented as multiplexers, so use a MUX for ordinary internal data selection and reserve explicit tri-state behavior for interfaces that require it.

## Worked Examples · 例题

**Two-source bus.** Driver A carries 1, driver B carries 0. ENA=1, ENB=0 gives bus=1. Reversing the enables gives bus=0. ENA=ENB=1 causes contention. ENA=ENB=0 gives Z at the driver level, with the actual bus voltage determined by loading, leakage, and any bias circuit.

**ROM output.** 两片 ROM 可以共享数据总线，地址高位决定 chip select。读某片时只开启其输出，另一片关闭。不能因为地址不同，就认为两片的输出自动不冲突。

## Pitfalls and Review · 易错点与复习

- Z means released, while X means unknown or conflicting in simulation.
- 未使能的输出不一定为 0，必须看 function table。
- Open output faults and deliberately disabled tri-state outputs have different causes.
- Active-low output enable is asserted with 0; a LOW data value is still data.

**Exam question:** Why can two tri-state drivers share a wire while two ordinary gate outputs cannot be connected arbitrarily?

**Answer:** Disabled tri-state drivers release the wire. The control logic ensures that only the selected driver drives it. Ordinary outputs remain active and can impose conflicting voltages.

## Connections · 相关笔记

[[Multiplexer and Demultiplexer]] gives a single-driver selection alternative. [[Memory Arrays and Expansion]] uses chip selection. [[VHDL Language and Modeling]] separates simulated resolution from physical drivers.

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
