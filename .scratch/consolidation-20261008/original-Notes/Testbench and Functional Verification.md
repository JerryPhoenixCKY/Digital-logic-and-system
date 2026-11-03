---
tags:
  - ECE2050
  - hardware-description
date: 2026-09-30
aliases:
  - 测试平台与功能验证
  - Testbench and Functional Verification
  - Self-checking HDL testbench
---

# Testbench and Functional Verification · 测试平台与功能验证

> [!SUMMARY] Quick recall · 英文速览
> A testbench supplies stimuli and compares outputs with an independently stated expected behavior. A waveform is useful evidence, but assertions and coverage make failures and untested cases explicit.

## Core Definition · 核心定义

测试平台 (testbench) 没有外部硬件 ports，通过时钟、复位与输入激励驱动 DUT (design under test)。它包含 wait/assert 等 simulation constructs，不用于作为板上硬件顶层综合。

Golden/reference model 来自规范；若直接复制 DUT 的同一错误表达式，比较会一起错。状态向量更新、边沿前后窗口、reset priority 必须明确。

## Complete Minimal Example · 完整小型例子

此 testbench 对 [[Structural Shift Register Project]] 的 bidir4 interface，仿真 clock=10 ns，输入在远离 rising edge 的时刻设置：

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity tb_bidir4 is
end entity;

architecture sim of tb_bidir4 is
  signal clk : std_logic := '0';
  signal rst : std_logic := '1';
  signal r, sr, sl : std_logic := '0';
  signal q : std_logic_vector(3 downto 0);
  signal done : boolean := false;
begin
  dut : entity work.bidir4(structural)
    port map(clk => clk, rst => rst,
             right_left => r, sr => sr, sl => sl, q => q);

  clock_gen : process
  begin
    while not done loop
      clk <= '0'; wait for 5 ns;
      clk <= '1'; wait for 5 ns;
    end loop;
    wait;
  end process;

  stimulus : process
    variable expected : std_logic_vector(3 downto 0);
    constant bits : std_logic_vector(0 to 3) := "1011";
  begin
    wait for 2 ns;
    assert q = "0000" report "reset failure" severity failure;
    rst <= '0'; r <= '1'; sl <= '0';
    expected := "0000";
    for i in 0 to 3 loop
      sr <= bits(i);
      wait until rising_edge(clk);
      expected := bits(i) & expected(3 downto 1);
      wait for 1 ns;
      assert q = expected report "right shift failure" severity failure;
      wait until falling_edge(clk);
    end loop;

    r <= '0'; sl <= '0';
    wait until rising_edge(clk);
    expected := expected(2 downto 0) & '0';
    wait for 1 ns;
    assert q = expected report "left shift failure" severity failure;

    wait for 1 ns;
    rst <= '1';
    wait for 1 ns;
    assert q = "0000" report "async reset failure" severity failure;
    done <= true;
    report "directed checks passed" severity note;
    wait;
  end process;
end architecture;
```

Assertions wait beyond zero-time signal scheduling. Here 1 ns is a deliberate check delay in a zero-delay behavioral model, not a guaranteed physical FF delay. A timing simulation needs an observation point compatible with its actual delays.

## Trace and Coverage · 波形与覆盖

预期 right-shift state=1000、0100、1010、1101；left step=1010；异步 reset=0000。q 的物理预期参考 bit order 与 design 一致。

The code is a directed teaching example, not exhaustive verification. To extend it, enumerate all initial states using a loading/initialization method permitted by the interface, then test both directions and all SR/SL pairs. If the design has no parallel load, reach states through a defined serial loading sequence rather than forcing internal state in the normal functional test.

## Test Dimensions · 测试维度

| Dimension | Examples | Catches |
|---|---|---|
| Data | All zero, all one, alternating, isolated 1 | Missing/shorted stages |
| Direction | Both modes and switches | Reversed mappings |
| Reset | Initially and between edges | Wrong reset semantics |
| Boundary | Edge-adjacent changes where specified | Timing model errors |
| State | Every reachable old word | Incomplete next-state logic |
| Unknowns | Unexpected U/X | Missing initialization/drivers |

不要只把一张“看起来合理”的 waveform 当通过依据；应标出 stimulus、expected、observed 与失败条件。功能仿真通过仍需 FPGA constraints、timing 与板上验证。

## Method and Exam English · 方法与答题

1. Read the DUT interface and behavior specification.
2. Choose an independently understandable reference recurrence.
3. Apply inputs away from capture edges for ordinary functional tests.
4. Observe after model updates and compare with assertions.
5. Report what was covered and what still needs testing.

**Question:** Why can an assertion immediately after `wait until rising_edge(clk)` see the old Q?

**Answer:** The clock event wakes processes, and their signal assignments are scheduled for later update cycles. An assertion in the same activation can run before Q has updated. Wait for the appropriate delta cycles or a specified observation delay before comparing.

## Connections · 相关笔记

[[VHDL Language and Modeling]], [[Structural Shift Register Project]], [[Sequence Detector]], [[Synchronous Counter Design]], [[Field-Programmable Gate Array]], [[Setup and Hold Timing]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
