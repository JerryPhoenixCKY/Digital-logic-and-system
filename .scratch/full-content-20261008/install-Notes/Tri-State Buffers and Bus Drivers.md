---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
updated: 2026-10-09
chapter: Ch6
aliases:
  - 三态缓冲与总线驱动
  - Tri-State Buffers and Bus Drivers
  - 三态缓冲与总线驱动 · Ch6
  - 三态缓冲器与总线驱动
  - Three-state logic
---

# Tri-State Buffers and Bus Drivers · 三态缓冲与总线驱动

> [!SUMMARY] Quick recall · 英文速览
> High impedance releases a shared line. It is neither a driven zero nor an unknown Boolean value; bus ownership prevents competing drivers.

## 1 · 三态与使能

三态缓冲器 (tri-state buffer) 在使能时传递输入，关闭时输出高阻抗 Z (high impedance)。Z 描述驱动状态，X 描述逻辑值未知，二者不同；接收端读到什么电压还取决于其他驱动和偏置。

### Core Definition and Validity · 定义与条件

三态缓冲器 (tri-state buffer) 在使能有效时驱动数据，关闭时呈高阻 (high impedance)。本篇用高有效 EN；实际符号若有气泡，则有效极性相反。

| EN | D | Output |
|---|---|---|
| 0 | X | Z |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

总线 (bus) 允许多个潜在驱动器，但同一时刻须由协议保证只有一个普通推挽输出有效。[[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|Combinational Circuit]] 的单驱动模型仍适用于每个有效工作状态；三态共享是明确管理的例外。

### Pitfalls and Review · 易错点与复习

- Z means released, while X means unknown or conflicting in simulation.
- 未使能的输出不一定为 0，必须看 function table。
- Open output faults and deliberately disabled tri-state outputs have different causes.
- Active-low output enable is asserted with 0; a LOW data value is still data.

**Exam question:** Why can two tri-state drivers share a wire while two ordinary gate outputs cannot be connected arbitrarily?

**Answer:** Disabled tri-state drivers release the wire. The control logic ensures that only the selected driver drives it. Ordinary outputs remain active and can impose conflicting voltages.

### Connections · 相关笔记

[[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]] gives a single-driver selection alternative. [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]] uses chip selection. [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] separates simulated resolution from physical drivers.

## 2 · 总线共享与冲突

共享总线 (bus) 的各驱动使能需互斥，通常满足任意时刻至多一者开启。两个驱动一个送 1、另一个送 0 会产生冲突，不能用普通 OR 函数解释。

> [!example]- Tri-State Buffers and Bus Drivers · 推导与例题
> **Mechanism · 机制**
>
> In a two-source bus selector, one driver is enabled when select=0 and the other when select=1. If both are disabled, the bus may float unless another defined circuit provides a level. If both are enabled and disagree, there is contention, not a logical OR operation.
>
> VHDL `std_logic` resolution can report conflicting drivers as `X`; it does not make that physical connection safe. Internal FPGA tri-state descriptions may be implemented as multiplexers, so use a MUX for ordinary internal data selection and reserve explicit tri-state behavior for interfaces that require it.

## 3 · 切换与实际边界

切换所有者应先释放旧驱动再开启新驱动，遵守使能／关闭延迟。所有驱动关闭时需规定默认偏置或允许的无效状态。FPGA 内部共享数据通常综合为 MUX，实际 I/O 三态需由目标资源支持。

> [!example]- Tri-State Buffers and Bus Drivers · 推导与例题
> **Worked Examples · 例题**
>
> **Two-source bus.** Driver A carries 1, driver B carries 0. ENA=1, ENB=0 gives bus=1. Reversing the enables gives bus=0. ENA=ENB=1 causes contention. ENA=ENB=0 gives Z at the driver level, with the actual bus voltage determined by loading, leakage, and any bias circuit.
>
> **ROM output.** 两片 ROM 可以共享数据总线，地址高位决定 chip select。读某片时只开启其输出，另一片关闭。不能因为地址不同，就认为两片的输出自动不冲突。

## 4 · 重点测试

> [!IMPORTANT] 单驱动与定义明确
> 检查互斥使能、全关闭、所有者切换与每个数据模式。悬空输入不能自动假定为 HIGH；波形有冲突时先检查驱动权，而不是改布尔方程。

## Sources · 课件依据

主线课件：[Ch6 lecture](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
