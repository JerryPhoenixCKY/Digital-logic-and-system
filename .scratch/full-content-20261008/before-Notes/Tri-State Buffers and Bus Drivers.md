---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
updated: 2026-10-08
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
