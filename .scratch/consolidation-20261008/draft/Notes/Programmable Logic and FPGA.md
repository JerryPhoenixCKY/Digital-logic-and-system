---
tags:
  - ECE2050
  - memory
  - programmable-logic
date: 2026-09-30
updated: 2026-10-08
chapter: Ch11
aliases:
  - 可编程逻辑与FPGA
  - Programmable Logic and FPGA
  - 可编程逻辑与FPGA · Ch11
  - Read-Only Memory and Programmable Logic Arrays
  - ROM与可编程逻辑阵列
  - ROM LUT PLA PAL
  - Field-Programmable Gate Array
  - 现场可编程门阵列
  - FPGA
---

# Programmable Logic and FPGA · 可编程逻辑与FPGA

> [!SUMMARY] Quick recall · 英文速览
> A ROM or LUT stores a truth table. A PLA shares product terms. An FPGA combines programmable logic, state elements, routing, and constrained physical implementation.

## 1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积

n 输入、m 输出的任意组合函数可用 $2^n\times m$ 的 ROM 表示，输入是地址、内容是输出；这是功能存储量，不含器件附加开销。PLA 采用可编程 AND／OR 阵列，允许多输出共享乘积项；PAL 的可编程范围需按结构声明。

> [!example]- Read-Only Memory and Programmable Logic Arrays · 推导与例题
> **Derivation · ROM 编程表**
>
> 要求地址 A1A0 时输出 $(X,Y,Z)=(A_1\oplus A_0,A_1+A_0,A_1A_0)$：
>
> | Address | X | Y | Z | Stored XYZ |
> |---|---|---|---|---|
> | 00 | 0 | 0 | 0 | 000 |
> | 01 | 1 | 1 | 0 | 110 |
> | 10 | 1 | 1 | 0 | 110 |
> | 11 | 0 | 1 | 1 | 011 |
>
> Capacity=4×3=12 bit。若存储输出顺序改为 ZYX，word 必须相应重排；所有 bit 格子的 dots/0/1 都应按明确极性读。
>
> The address bits select a row; they are not ANDed numerically with the stored word. The output is the entry stored at that row, after the specified access delay.
>
> **Worked Example · PLA 共享乘积**
>
> 要求 $X=\bar ABC+A\bar BC$，$Y=\bar AB$。定义 $P_1=\bar ABC$、$P_2=A\bar BC$、$P_3=\bar AB$；X=P1+P2，Y=P3。若另一个输出也用 P1，可共享该 product term。
>
> | Product | A | B | C | Connect to X | Connect to Y |
> |---|---|---|---|---|---|
> | P1 | Complement | True | True | Yes | No |
> | P2 | True | Complement | True | Yes | No |
> | P3 | Complement | True | Unused | No | Yes |
>
> “Unused” in the AND-array table means omit that literal from the product; it does not mean drive an input wire to floating X. For A,B,C=0,1,1, P1=P3=1, giving X=Y=1. For 1,0,1, X=1,Y=0.
>
> **ROM versus PLA versus LUT · 对比**
>
> - ROM/LUT：explicitly store every input combination，适合任意 truth table。
> - PLA：store/select useful implicants，适合可共享且简化后的 SOP。
> - N-input single-output LUT needs $2^N$ configuration bits; a 4-input LUT needs16。
> - A larger logic function may use several LUTs and routing; a LUT's stored table does not by itself add sequential state to the user function.
>
> Configuration storage is different from runtime state. A LUT output can be combinational even though its truth table is stored in memory. A separate FF produces clocked behavior.

## 2 · LUT：查表实现组合逻辑

k 输入 LUT 存储 $2^k$ 个真值 bit。配置内容在逻辑运行时作为固定函数使用；用户的运行状态另由 FF 等资源保存。查找表和通用读写存储的角色不同。

## 3 · Field-Programmable Gate Array · 从函数到物理实现

FPGA 由 LUT、触发器、可编程连线和 I/O 等构成。设计流程：行为建模→功能仿真→综合→布局布线→约束下的时序分析→上板验证。

> [!example]- Field-Programmable Gate Array · 推导与例题
> **Design Flow · 设计流程**
>
> ```mermaid
> flowchart LR
>   RTL[Specify and write HDL] --> Sim[Functional simulation]
>   Sim --> Synth[Synthesis and resource mapping]
>   Synth --> Impl[Placement and routing]
>   Impl --> Timing[Timing and constraint review]
>   Timing --> Config[Generate configuration]
>   Config --> Board[Program and verify on board]
> ```
>
> Synthesis 将行为/结构转为可实现逻辑；implementation 决定资源放置与连接；bitstream/configuration 配置器件。Behavioral simulation 成功不能代替物理 timing review。
>
> **Worked Example · 四位 enabled register**
>
> 功能 $Q^+=EN?D:Q$：需要保存4位，因此通常对应4个 FF；输入选择由 MUX/FF内 enable resource 实现。若同 clock 下 q<=d，没有 EN，不能因为时钟 HIGH 持续很久就让 q 透明跟随。
>
> **LUT capacity.** 一个4输入、1输出 LUT 存16个 truth bits。要直接表示任意5输入、1输出函数，完整 table有32 bit；可分解为两个4-input cofactors 再 MUX，或按目标设备其他资源实现。资源估算不是实际综合 report。

## 4 · 约束与可靠运行

时钟、输入／输出时延、电气标准和引脚分配要明确。仿真正确只证明所测模型功能；布局后的时序收敛 (timing closure) 和实际接口条件仍需验证。异步输入、复位释放和共享总线问题不会由综合工具自动替规范作出决定。

> [!IMPORTANT] 状态与配置分开
> LUT 定义函数，FF 保存运行状态，约束定义外部承诺。读到一个逻辑真值表，不能据此断定整个系统无状态。

> [!example]- Field-Programmable Gate Array · 推导与例题
> **Constraints and Interfaces · 约束与接口**
>
> 必须指定 top-level ports、target device、clock period、I/O pin mapping 与电气标准，涉及板上连接时核对该 board 的资料。讲义中的旧版 Vivado 菜单和示例引脚是历史演示；本篇保留阶段逻辑，不当作当前安装版本的操作保证。
>
> An unconstrained clock can leave a design without a meaningful required frequency. An incorrect pin constraint can produce the right simulated waveform on the wrong physical pin. These are different failures, so inspect both logic and interface constraints.
>
> 不把普通输入按钮当 clock；先同步/debounce 并产生 enable event。内部多驱动 `X` 或未赋值 latch 应在 simulation/synthesis warnings 中追查。
>
> **Practical Review · 实践与复习**
>
> | Evidence | Supports | Does not by itself prove |
> |---|---|---|
> | Functional simulation | RTL behavior on tested stimuli | Timing closure or electrical wiring |
> | Synthesis report | Mapped registers and logic | Correct external pin assignment |
> | Timing report | Constrained timing paths | Correct functional specification |
> | Board observation | Tested physical behavior | All untested states and interfaces |
>
> **Exam question:** Why does a memory-based LUT still implement combinational logic?
>
> **Answer:** Its configuration bits define a fixed truth table during operation. Current inputs address that table and determine the output. Clocked user state requires a register or another state element; configuration memory alone does not make the function depend on prior inputs.

## Sources · 课件依据

主线课件：[Ch11 lecture](../LGU_HUB_ECE2050/ECE2050-Chap11.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
