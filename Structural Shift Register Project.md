---
tags:
  - ECE2050
  - hardware-description
date: 2026-09-30
updated: 2026-10-09
chapter: HDL
aliases:
  - 结构化移位寄存器项目
  - Structural Shift Register Project
  - 结构化移位寄存器项目 · HDL
  - 结构化双向移位寄存器项目
  - Structural VHDL shift register
---

# Structural Shift Register Project · 结构化移位寄存器项目

> [!SUMMARY] Quick recall · 英文速览
> Structural design instantiates reusable state cells and explicitly connects next-state logic. Bit order, shift direction, and control priority define correctness.

## 1 · 规范先写成位方程

本教学实现为 **4 位双向移位寄存器**：状态读作 q(3 downto 0)，正沿采样，高有效异步复位。R=1 时向低位右移、SR 进入 q3；R=0 时左移、SL 进入 q0。先写每位下一态，再实例化 DFF，避免凭“左／右”文字接反。此实现每拍移位；保持与并行装载是另加选择分支的扩展功能。

### Specification and Boundary · 规范与边界

本教学实现 4 个正沿 DFF；高有效 asynchronous reset；状态按 q(3 downto 0) 阅读，right_left=1 表示数值向低位 right shift，SR 进入 q3；right_left=0 left shift，SL 进入 q0。两侧输入单独提供。如果原图编号方向不同，先重写映射再接线，不能把本模型误标为原图逐引脚复制。

$$d_3=R\cdot SR+\bar Rq_2,\quad d_2=Rq_3+\bar Rq_1,$$
$$d_1=Rq_2+\bar Rq_0,\quad d_0=Rq_1+\bar RSL.$$

R=right_left。每条式子是两个 AND 加 OR 的二选一逻辑；四个 d 由同一旧 q 计算。

### Connections · 概念关系与应用

[[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] 提供实例化语法，[[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]] 是状态单元，[[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] 提供方向递推，[[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]] 选择每位来源；[[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]] 提供独立测试，[[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现|Field-Programmable Gate Array]] 完成映射与约束检查。

## 2 · 复用 DFF 与连接顶层

基础 DFF 只在有效边沿采样，复位方式与规范相符。顶层组合选择 next-state，端口映射 (port map) 将每个实例的 D、Q、clock、reset 明确连到实际信号。共时钟下各实例使用旧 Q。

> [!example]- Structural Shift Register Project · 推导与例题
> **Reusable DFF · 基础触发器**
>
> 下面是独立的完整 design unit：
>
> ```vhdl
> library ieee;
> use ieee.std_logic_1164.all;
>
> entity dff_ar is
>   port(clk, rst, d : in std_logic;
>        q : out std_logic);
> end entity;
>
> architecture rtl of dff_ar is
> begin
>   process(clk, rst)
>   begin
>     if rst = '1' then
>       q <= '0';
>     elsif rising_edge(clk) then
>       q <= d;
>     end if;
>   end process;
> end architecture;
> ```
>
> Reset has priority and acts without waiting for the clock. A synchronous version would place the reset test inside the rising-edge branch. Do not silently switch those semantics when reusing the component.
>
> **Structural Top Level · 结构化顶层**
>
> ```vhdl
> library ieee;
> use ieee.std_logic_1164.all;
>
> entity bidir4 is
>   port(clk, rst, right_left, sr, sl : in std_logic;
>        q : out std_logic_vector(3 downto 0));
> end entity;
>
> architecture structural of bidir4 is
>   signal qi, di : std_logic_vector(3 downto 0);
> begin
>   di(3) <= (right_left and sr)
>        or ((not right_left) and qi(2));
>   di(2) <= (right_left and qi(3))
>        or ((not right_left) and qi(1));
>   di(1) <= (right_left and qi(2))
>        or ((not right_left) and qi(0));
>   di(0) <= (right_left and qi(1))
>        or ((not right_left) and sl);
>
>   stages : for i in 0 to 3 generate
>     ff : entity work.dff_ar(rtl)
>       port map(clk => clk, rst => rst,
>                d => di(i), q => qi(i));
>   end generate;
>   q <= qi;
> end architecture;
> ```
>
> This uses structural DFF instances and explicit Boolean gate equations. If the learning requirement additionally asks for every AND/OR as an instance, create those gate entities and replace the equations with named port maps without changing the truth functions. Compile `dff_ar` before the top-level entity.

## 3 · 运行轨迹与独立验证

从复位后的 0000 开始，R=1、SR 依次输入 1、0、1、1，状态依次为 1000、0100、1010、1101。再 R=0、SL=0 得 1010；下一拍 SL=1 得 0101。预期模型使用位方程而非复制连线。覆盖 16 个旧状态、2 个方向、4 组双串行输入，并检查边沿间异步复位与方向改变。

### Verification Plan · 验证路径

1. Test the DFF independently: edge capture and asynchronous reset.
2. Test right shift with several serial patterns from known initial state.
3. Test left shift and direction changes between edges.
4. Assert reset between edges and confirm immediate logical clearing.
5. Check all 16 old words × 2 directions × 4 serial-input pairs in a reference model.
6. Compare old-state-derived next words with the structural simulation trace.

行为模型可写 `qi <= sr & qi(3 downto 1)` 或 `qi <= qi(2 downto 0) & sl`，用于对照，并不能替代要求练习 port-map 的结构实现。

> [!example]- Structural Shift Register Project · 推导与例题
> **Worked Example · 从零串入后反向**
>
> reset 后0000，R=1，SR依次1,0,1,1，四次 edge 后状态1000、0100、1010、1101。再 R=0、SL=0，下一 edge 到1010；再SL=1，下一edge到0101。每一步和 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] 的 recurrence 一致。
>
> 若 R 在 edge 附近变化，四个 d 的选择都可能违反 setup/hold；“方向只影响组合门”不表示它无需同步。实际按钮控制请先执行 [[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界|Metastability and Clock Domain Crossing]] 的接口处理。
>

## 4 · 综合与实现

完整源代码、实例化与测试要求在下方展开；功能通过后检查目标 FPGA 引脚、时钟、I/O 电气和时序。实际资源优化可以改变门的形状，但不能改变约定的寄存器行为。

> [!IMPORTANT] 两个常见错误
> 信号赋值的更新不即时，不能当软件循环移位；方向端改变也会改变 D 输入，必须满足采样条件，外部按钮信号需先处理同步与去抖。

### Pitfalls and Exam English · 误区与答题

- Four FFs have one shared clock, not a clock derived from adjacent Q.
- Don't use a variable loop that repeatedly shifts a newly updated word during one edge.
- Internal `qi` provides feedback and avoids depending on output-port readability.
- Testbench signals and synthesizable entities belong to different roles.

**Answer:** “Direction selects the data source for each D input. At the active edge, all four DFFs capture simultaneously, so each bit moves exactly one stage using the previous register contents.”

### Feature boundary · 教学实现与扩展接口

当前 `bidir4` 只有 `clk, rst, right_left, sr, sl, q` 接口，每个有效正沿执行一次左移或右移；高有效 rst 在边沿之间也可清零。它没有 EN、hold mode 或 parallel-load 数据端口。若要扩展为通用寄存器，需明确新增接口、选择分支、复位优先级与对应测试；[[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|通用移位寄存器]] 的四种模式不能当成现有代码已支持的功能。

## Sources · 课件依据

课程资料：[VHDL tutorial](../LGU_HUB_ECE2050/Tutorial6--VHDL-Tut-for%20reference.pdf)、[project specification](../LGU_HUB_ECE2050/ECE2050Project.pdf)。

---
索引：[[ECE2050.1]] · [[Glossary]]
