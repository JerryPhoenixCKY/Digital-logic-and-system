---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
updated: 2026-10-13
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

三态缓冲器 (tri-state buffer) 在使能 (enable) 时传递输入，关闭时输出高阻抗 Z (high impedance)。Z 描述驱动状态，X 描述逻辑值未知 (unknown)，二者不同；接收端读到什么电压还取决于其他驱动和偏置。

### Core Definition and Validity · 定义与条件

三态缓冲器 (tri-state buffer) 在使能有效时驱动数据，关闭时呈高阻 (high impedance)。本篇用高有效 (active-HIGH) EN；实际符号若有气泡，则为低有效 (active-LOW)，有效极性相反。

| EN | D | Output |
|---|---|---|
| 0 | X | Z |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

总线 (bus) 允许多个潜在驱动器，但同一时刻须由协议保证只有一个普通推挽输出 (push-pull output) 有效。[[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|Combinational Circuit]] 的单驱动模型仍适用于每个有效工作状态；三态共享是明确管理的例外。

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

### Tri-State Multiplexer · 使能译码实现选择，p.40、42

讲义用三态缓冲器实现多路选择器 (multiplexer, MUX)：输出连到同一 Y，但只有选中的数据源驱动，其余源呈 Z。2:1 选择器的逻辑使能为 $e_0=\bar S,e_1=S$；有气泡的 enable 端表示低电平时启用，不是数据反相。

> [!example]- Gate MUX and tri-state MUX · 稳态功能相同，连接方式不同
> ![[ch6-mux-implementations.png]]
> *讲义 p.40 原图：左侧用 AND–OR 得到单个门输出，右侧两个三态输出共享 Y；上支路的使能有气泡。*
>
> | S | $e_0$ | $e_1$ | Driver 0 | Driver 1 | Y after settling |
> |---|---|---|---|---|---|
> | 0 | 1 | 0 | Drives $D_0$ | Z | $D_0$ |
> | 1 | 0 | 1 | Z | Drives $D_1$ | $D_1$ |
>
> p.42 的四路实现用译码使能：
>
> $$e_0=\bar S_1\bar S_0,\quad e_1=\bar S_1S_0,\quad e_2=S_1\bar S_0,\quad e_3=S_1S_0.$$
>
> 稳定合法地址下，普通整数计数 $\sum_i e_i=1$，恰好一个数据源开启。安全共享要求至多一个开启，即 $\sum_i e_i\le1$；确定的正常 MUX 输出还要求恰好一个开启。全关闭时 Y 的驱动状态为 Z，不能套用普通 Boolean OR 式把它算成 0。
>
> **Self-check：** 地址 10，$(D_3,D_2,D_1,D_0)=(0,1,0,1)$，只有 $e_2=1$，Y=1。若控制故障又打开 driver 3，两个源分别驱动 1 与 0，将产生总线冲突 (bus contention)，不能解释为 $1+0=1$。
>
> The Boolean enables are mutually exclusive only in the settled model. During a select transition, unequal enable/disable delays can create overlap or a released interval. Releasing the old driver before asserting the new one is a timing requirement, not a consequence proved by the stable truth table.

### Turnaround Timing · 释放与接管

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

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 6: Combinational Building Blocks*，[本次讲义](../ECE2050-Chap6.pdf#page=40)，PDF p.40：两个三态缓冲器实现 2:1 MUX；p.42：四路译码使能的三态实现。PDF 页序与页脚编号一致。
- [库中原参考讲义](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。互斥条件、全关闭与冲突反例及接管时序为功能模型的补充解释；FPGA 实现关联见 [[Programmable Logic and FPGA]]。

---
索引：[[ECE2050.1]] · [[Glossary]]
