---
tags:
  - ECE2050
  - memory
  - programmable-logic
date: 2026-09-30
updated: 2026-10-09
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

### Core Definition · 核心定义

用 N-bit 输入作为地址，M-bit stored word 作为 M 个输出，就把 truth table 写入 $2^N\times M$ array。ROM 的 address decoder 产生所有 minterms；output connections/data 指定哪些行给1。

PLA (programmable logic array) 有可配置 AND 与 OR 阵列，按所需 product terms 实现 SOP；PAL 的经典模型为 programmable AND、fixed OR。这里 programmability 指配置连接；固定结构/布线资源不等于“所有连接不可编程”。

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

### Method and Exam English · 方法与答题

1. Fix input address order and output bit order.
2. Enumerate the full truth table for ROM/LUT.
3. For PLA, minimize each output and identify shareable products.
4. Check selected-row and connection polarity.
5. Confirm the timing of read versus registered output.

**Exam answer:** “The ROM stores the output vector for each address pattern. The PLA instead generates selected product terms and combines them into outputs. Both realize the specified Boolean functions, but their internal representations and resource costs differ.”

### Connections · 概念关系与应用

[[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 与 [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项|Minterm and Maxterm]] 分别解释 PLA 乘积和 ROM 行；[[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 与 [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]] 提供地址结构。[[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现|Field-Programmable Gate Array]] 采用 LUT/FF 资源，[[Seven-Segment Display and Code Conversion]] 是多输出查表的应用。

## 2 · LUT：查表实现组合逻辑

k 输入 LUT 存储 $2^k$ 个真值 bit。配置内容在逻辑运行时作为固定函数使用；用户的运行状态另由 FF 等资源保存。查找表和通用读写存储的角色不同。

### ROM versus PLA versus LUT · 对比

- ROM/LUT：explicitly store every input combination，适合任意 truth table。
- PLA：store/select useful implicants，适合可共享且简化后的 SOP。
- N-input single-output LUT needs $2^N$ configuration bits; a 4-input LUT needs16。
- A larger logic function may use several LUTs and routing; a LUT's stored table does not by itself add sequential state to the user function.

Configuration storage is different from runtime state. A LUT output can be combinational even though its truth table is stored in memory. A separate FF produces clocked behavior.

## 3 · Field-Programmable Gate Array · 从函数到物理实现

FPGA 由 LUT、触发器、可编程连线和 I/O 等构成。设计流程：行为建模→功能仿真→综合→布局布线→约束下的时序分析→上板验证。

### Core Definition · 核心定义

FPGA 是可在现场配置的集成电路。教学 logic element 通常包括 LUT、FF、MUX；器件还可有 carry resources、RAM、DSP 与 I/O。具体 LUT 输入数和 architecture 依器件，不应把某个例子的 four-input LUT 当成所有 FPGA 的定义。

LUT 执行 combinational function，FF 保存 runtime state，routing 连接模块。HDL 描述的多个 concurrent statements 对应并行硬件；不是 CPU 把每行逐条执行。

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

### Connections · 概念关系与应用

[[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积|Read-Only Memory and Programmable Logic Arrays]] 解释 LUT，[[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]] 解释 FF 的运行状态；用 [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] 建模并在 [[Structural Shift Register Project]] 练习连接；[[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]] 检查功能，[[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] 检查实现时间。

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
索引：[[ECE2050.1]] · [[Glossary]]
