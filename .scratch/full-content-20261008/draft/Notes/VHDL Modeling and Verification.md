---
tags:
  - ECE2050
  - hardware-description
date: 2026-09-30
updated: 2026-10-09
chapter: HDL
aliases:
  - VHDL建模与验证
  - VHDL Modeling and Verification
  - VHDL建模与验证 · HDL
  - VHDL Language and Modeling
  - VHDL语言与建模
  - VHSIC Hardware Description Language
  - Testbench and Functional Verification
  - 测试平台与功能验证
  - Self-checking HDL testbench
---

# VHDL Modeling and Verification · VHDL建模与验证

> [!SUMMARY] Quick recall · 英文速览
> VHDL describes concurrent hardware. A testbench drives the design and checks an independent reference model; simulation success is one layer of evidence.

## 1 · VHDL Language and Modeling · 接口与实现

entity 定义端口，architecture 描述实现。`std_logic` 可表示多值逻辑；数值运算使用明确的 `unsigned`／`signed` 类型并声明位宽，不能把位向量的显示形式当作整数语义。

### Core Definition · 核心定义

VHDL 是 hardware description language。entity 声明 ports，architecture 声明内部 signals 与逻辑。dataflow 用 concurrent equations，structural 用 instances/port map，behavioral 常用 process 描述。不同风格可以描述相同的硬件。

采用 `IEEE.std_logic_1164` 的 logic types；算术用 `IEEE.numeric_std` 中 `unsigned`/`signed` 明确数值含义。`std_logic_vector` 本身是一组逻辑值，没有自动确定的 signed 数值解释。

### Types and Operators · 类型与运算

| Form | Meaning | Important boundary |
|---|---|---|
| `'0'`, `'1'` | Scalar logic literal | Single quotes |
| `"1010"` | Vector literal | Double quotes |
| `<=` assignment | Schedule a signal value | Relational `<=` in a condition has another meaning |
| `:=` | Variable assignment | Immediate within that execution |
| `&` | Concatenation | Order determines bit position |
| `unsigned(v)` | Explicit numeric interpretation | Does not add an extra sign bit |
| `rising_edge(clk)` | Detect valid rising transition | Use for a synchronous capture event |

`std_logic` 的 U/X/Z 等为模拟信息；resolved type 可以计算多个 driver 的 resolution，不能因此任意短接真实输出。`std_ulogic` 可帮助发现不允许的多驱动。

### Numeric width · 数值类型与算术位宽

完整算术代码需同时引入 `use ieee.std_logic_1164.all;` 和 `use ieee.numeric_std.all;`。例如 a、b 都是 `std_logic_vector(3 downto 0)`，s5 是五位 unsigned，可写 `s5 <= resize(unsigned(a), 5) + resize(unsigned(b), 5);`；先扩宽操作数再相加，才能保留第 5 位进位。`signed` 扩宽作符号扩展，`unsigned` 扩宽作零扩展；转换只解释同一位串，不自动修复此前已截断的结果。

## 2 · 并发、过程与更新时机

architecture 中各并发语句与 process 并行存在；process 内顺序执行不意味着硬件逐条耗时。signal 的赋值通过 delta cycle 更新，variable 在当前过程立即更新；连续给同一 signal 赋值不能当作软件累加器。

### Assignment scheduling · 同一过程内的赋值调度

signal 赋值 (`<=`) 安排后续更新，过程本次激活中的后续语句仍读取未更新的 signal 值；variable 赋值 (`:=`) 则供后续语句立即读取。对同一 signal 的同一零延迟更新时刻，单次过程激活中后面的赋值覆盖前面的安排，例如连续写两次 `count <= count + 1;` 不表示同一拍加 2。对不同信号的赋值则分别生效，`q1 <= d; q2 <= q1;` 正好形成两级寄存器。

process 的顺序语句 (sequential statements) 是模拟执行语义；组合/时序硬件的区别由敏感事件、时钟条件及是否需要保持历史决定。architecture 中多个 process 与 concurrent assignments 并行响应其触发事件。

> [!example]- VHDL Language and Modeling · 推导与例题
> **Concurrent and Sequential Semantics · 并发与顺序语义**
>
> ```vhdl
> -- Concurrent dataflow: both equations exist at the same time.
> p <= a xor b;
> s <= p xor cin;
> ```
>
> p 更新会在仿真的后续 delta cycle 触发 s 更新；零时间 delta 是模拟调度，不是实际门延迟。把两个语句上下交换，不改变此 dataflow network。
>
> ```vhdl
> process(clk)
> begin
>   if rising_edge(clk) then
>     q1 <= d;
>     q2 <= q1;
>   end if;
> end process;
> ```
>
> q2 读旧 q1，所以是两个寄存器级，不是同一边沿 d 直接到 q2。变量赋值 `v := d; q2 <= v;` 则 q2 读取本次新 v；语言语义改变了数据路径。

## 3 · 组合与时钟建模

组合 process 完整覆盖所有分支与相关输入，避免无意锁存；时钟 process 在 `rising_edge(clk)` 更新寄存器，复位的敏感列表和位置体现同步／异步语义。使能关闭时保持状态应与硬件规范一致。

### Coding Review and Boundaries · 编写检查与边界

- Basic identifiers are case-insensitive; avoid consecutive/trailing underscores and reserved words.
- Use ordinary straight quotes and matching `end if`, `end process`, and architecture boundaries.
- Named port maps make connection intent clearer than long positional lists.
- Do not use `inout` merely to read an ordinary output; use an internal signal. Output readability also depends on the language revision.
- `'-'` is a simulation logic value, not automatic wildcard equality; use an explicit matching operation or specified synthesis don't-care treatment.

The snippets explain language and hardware behavior. Their enclosing declarations, vector widths, and library context must be supplied consistently before compiling. They are not a claim that a particular installed tool version was tested.

> [!example]- VHDL Language and Modeling · 推导与例题
> **Combinational versus Clocked Process · 组合与时钟过程**
>
> ```vhdl
> process(a, b, sel)
> begin
>   y <= a;                 -- default assigns all paths
>   if sel = '1' then
>     y <= b;
>   end if;
> end process;
> ```
>
> Explicit sensitivity lists must include all read signals for this combinational model. `process(all)` is the VHDL-2008 alternative when the configured tool mode supports it. Omitting a required signal can make simulation stale while synthesis still builds input-dependent logic.
>
> 如果 combinational process 的某些路径不给 y 赋值，就表示保留旧值，可能推断 latch。clocked process 省略 inactive-edge assignment 是正常 FF hold；同样的“不赋值”要结合事件结构判断。
>
> **Reset Examples · 复位例题**
>
> ```vhdl
> -- Synchronous, active-high reset; reset outranks enable.
> process(clk)
> begin
>   if rising_edge(clk) then
>     if rst = '1' then
>       q <= (others => '0');
>     elsif en = '1' then
>       q <= d;
>     end if;
>   end if;
> end process;
> ```
>
> Asynchronous reset moves the reset test before `rising_edge` and includes rst in `process(clk, rst)`. A reset inside the rising-edge conditional cannot reset between edges merely because rst appears in the sensitivity list.
>

## 4 · Testbench and Functional Verification · 规范作为独立参照

testbench 为 DUT 产生时钟、复位、模式和数据；参考模型从规范建立，不复制 DUT 的内部表达式。对小组合模块穷举，对时序模块测试初态、所有模式、方向切换、复位优先级、边界和长序列。

### Core Definition · 核心定义

测试平台 (testbench) 没有外部硬件 ports，通过时钟、复位与输入激励驱动 DUT (design under test)。它包含 wait/assert 等 simulation constructs，不用于作为板上硬件顶层综合。

Golden/reference model 来自规范；若直接复制 DUT 的同一错误表达式，比较会一起错。状态向量更新、边沿前后窗口、reset priority 必须明确。

> [!example]- Testbench and Functional Verification · 推导与例题
> **Complete Minimal Example · 完整小型例子**
>
> 此 testbench 对 [[Structural Shift Register Project]] 的 bidir4 interface，仿真 clock=10 ns，输入在远离 rising edge 的时刻设置：
>
> ```vhdl
> library ieee;
> use ieee.std_logic_1164.all;
>
> entity tb_bidir4 is
> end entity;
>
> architecture sim of tb_bidir4 is
>   signal clk : std_logic := '0';
>   signal rst : std_logic := '1';
>   signal r, sr, sl : std_logic := '0';
>   signal q : std_logic_vector(3 downto 0);
>   signal done : boolean := false;
> begin
>   dut : entity work.bidir4(structural)
>     port map(clk => clk, rst => rst,
>              right_left => r, sr => sr, sl => sl, q => q);
>
>   clock_gen : process
>   begin
>     while not done loop
>       clk <= '0'; wait for 5 ns;
>       clk <= '1'; wait for 5 ns;
>     end loop;
>     wait;
>   end process;
>
>   stimulus : process
>     variable expected : std_logic_vector(3 downto 0);
>     constant bits : std_logic_vector(0 to 3) := "1011";
>   begin
>     wait for 2 ns;
>     assert q = "0000" report "reset failure" severity failure;
>     rst <= '0'; r <= '1'; sl <= '0';
>     expected := "0000";
>     for i in 0 to 3 loop
>       sr <= bits(i);
>       wait until rising_edge(clk);
>       expected := bits(i) & expected(3 downto 1);
>       wait for 1 ns;
>       assert q = expected report "right shift failure" severity failure;
>       wait until falling_edge(clk);
>     end loop;
>
>     r <= '0'; sl <= '0';
>     wait until rising_edge(clk);
>     expected := expected(2 downto 0) & '0';
>     wait for 1 ns;
>     assert q = expected report "left shift failure" severity failure;
>
>     wait for 1 ns;
>     rst <= '1';
>     wait for 1 ns;
>     assert q = "0000" report "async reset failure" severity failure;
>     done <= true;
>     report "directed checks passed" severity note;
>     wait;
>   end process;
> end architecture;
> ```
>
> Assertions wait beyond zero-time signal scheduling. Here 1 ns is a deliberate check delay in a zero-delay behavioral model, not a guaranteed physical FF delay. A timing simulation needs an observation point compatible with its actual delays.

### Method and Exam English · 方法与答题

1. Read the DUT interface and behavior specification.
2. Choose an independently understandable reference recurrence.
3. Apply inputs away from capture edges for ordinary functional tests.
4. Observe after model updates and compare with assertions.
5. Report what was covered and what still needs testing.

**Question:** Why can an assertion immediately after `wait until rising_edge(clk)` see the old Q?

**Answer:** The clock event wakes processes, and their signal assignments are scheduled for later update cycles. An assertion in the same activation can run before Q has updated. Wait for the appropriate delta cycles or a specified observation delay before comparing.

### Connections · 概念关系与应用

语言调度见 [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]]；本例 DUT 为 [[Structural Shift Register Project]]，同样方法用于 [[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀|Sequence Detector]] 与 [[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励|Synchronous Counter Design]]。功能覆盖之外还要检查 [[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现|Field-Programmable Gate Array]] 的映射与 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] 的路径条件。

## 5 · 断言、采样与覆盖

在时钟边沿后等待规定的仿真更新，再用 assertion 比较预期输出。delta cycle 不等于真实门延迟。零错误只代表已覆盖条件一致；综合可行性、约束时序和物理接口仍需分别检查。

> [!IMPORTANT] 保留完整可运行例子
> 下方实现与 testbench 包含库、类型、时钟和检查逻辑；实际项目结构化端口连接见 [[Structural Shift Register Project]]。不要只保存一个无法解释上下文的赋值片段。

### Test Dimensions · 测试维度

| Dimension | Examples | Catches |
|---|---|---|
| Data | All zero, all one, alternating, isolated 1 | Missing/shorted stages |
| Direction | Both modes and switches | Reversed mappings |
| Reset | Initially and between edges | Wrong reset semantics |
| Boundary | Edge-adjacent changes where specified | Timing model errors |
| State | Every reachable old word | Incomplete next-state logic |
| Unknowns | Unexpected U/X | Missing initialization/drivers |

不要只把一张“看起来合理”的 waveform 当通过依据；应标出 stimulus、expected、observed 与失败条件。功能仿真通过仍需 FPGA constraints、timing 与板上验证。

> [!example]- VHDL Language and Modeling · 推导与例题
> **Worked Examples · 例题**
>
> **Unsigned comparison.** `greater <= '1' when unsigned(a) > unsigned(b) else '0';`，对 a=1000,b=0111 得1。换为 `signed` 时 a=−8,b=7，输出0。类型决定 interpretation，位串本身没有改变。
>
> **Width.** 两个4位 unsigned 相加可能需要5位。先 `resize` operands 到5位再加才能保留 carry；只把4位结果赋给5位目标，不能保证此前被截掉的 carry 自动回来。
>
> **Process trap.** `if en='1' then q<=d; end if;` 在 level-sensitive `process(en,d)` 中是 latch；在 `if rising_edge(clk)` 内则是 enabled FF。所谓 “behavioral is sequential” 只描述语句执行顺序，不意味着必然生成时序电路。

> [!example]- Testbench and Functional Verification · 推导与例题
> **Trace and Coverage · 波形与覆盖**
>
> 预期 right-shift state=1000、0100、1010、1101；left step=1010；异步 reset=0000。q 的物理预期参考 bit order 与 design 一致。
>
> The code is a directed teaching example, not exhaustive verification. To extend it, enumerate all initial states using a loading/initialization method permitted by the interface, then test both directions and all SR/SL pairs. If the design has no parallel load, reach states through a defined serial loading sequence rather than forcing internal state in the normal functional test.
>

### Exam English and Connections · 答题与关联

**Answer:** “The two signal assignments inside the clocked process both evaluate their right-hand sides using the pre-update signal values. Therefore q2 receives the previous q1 and the circuit forms a two-stage register chain.”

[[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|Combinational Circuit]], [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]], [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]], [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]], [[Tri-State Buffers and Bus Drivers]], [[Structural Shift Register Project]], [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]].

## Sources · 课件依据

课程资料：[VHDL tutorial](../LGU_HUB_ECE2050/Tutorial6--VHDL-Tut-for%20reference.pdf)、[project specification](../LGU_HUB_ECE2050/ECE2050Project.pdf)。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
