---
tags:
  - ECE2050
  - hardware-description
date: 2026-09-30
aliases:
  - 结构化双向移位寄存器项目
  - Structural Shift Register Project
  - Structural VHDL shift register
---

# Structural Shift Register Project · 结构化双向移位寄存器项目

> [!SUMMARY] Quick recall · 英文速览
> Structural modeling instantiates storage elements and connects explicit next-state logic. A bidirectional register is a bank of DFFs preceded by direction-controlled data selection.

## Specification and Boundary · 规范与边界

本教学实现 4 个正沿 DFF；高有效 asynchronous reset；状态按 q(3 downto 0) 阅读，right_left=1 表示数值向低位 right shift，SR 进入 q3；right_left=0 left shift，SL 进入 q0。两侧输入单独提供。如果原图编号方向不同，先重写映射再接线，不能把本模型误标为原图逐引脚复制。

$$d_3=R\cdot SR+\bar Rq_2,\quad d_2=Rq_3+\bar Rq_1,$$
$$d_1=Rq_2+\bar Rq_0,\quad d_0=Rq_1+\bar RSL.$$

R=right_left。每条式子是两个 AND 加 OR 的二选一逻辑；四个 d 由同一旧 q 计算。

## Reusable DFF · 基础触发器

下面是独立的完整 design unit：

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity dff_ar is
  port(clk, rst, d : in std_logic;
       q : out std_logic);
end entity;

architecture rtl of dff_ar is
begin
  process(clk, rst)
  begin
    if rst = '1' then
      q <= '0';
    elsif rising_edge(clk) then
      q <= d;
    end if;
  end process;
end architecture;
```

Reset has priority and acts without waiting for the clock. A synchronous version would place the reset test inside the rising-edge branch. Do not silently switch those semantics when reusing the component.

## Structural Top Level · 结构化顶层

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity bidir4 is
  port(clk, rst, right_left, sr, sl : in std_logic;
       q : out std_logic_vector(3 downto 0));
end entity;

architecture structural of bidir4 is
  signal qi, di : std_logic_vector(3 downto 0);
begin
  di(3) <= (right_left and sr)
       or ((not right_left) and qi(2));
  di(2) <= (right_left and qi(3))
       or ((not right_left) and qi(1));
  di(1) <= (right_left and qi(2))
       or ((not right_left) and qi(0));
  di(0) <= (right_left and qi(1))
       or ((not right_left) and sl);

  stages : for i in 0 to 3 generate
    ff : entity work.dff_ar(rtl)
      port map(clk => clk, rst => rst,
               d => di(i), q => qi(i));
  end generate;
  q <= qi;
end architecture;
```

This uses structural DFF instances and explicit Boolean gate equations. If the learning requirement additionally asks for every AND/OR as an instance, create those gate entities and replace the equations with named port maps without changing the truth functions. Compile `dff_ar` before the top-level entity.

## Worked Example · 从零串入后反向

reset 后0000，R=1，SR依次1,0,1,1，四次 edge 后状态1000、0100、1010、1101。再 R=0、SL=0，下一 edge 到1010；再SL=1，下一edge到0101。每一步和 [[Shift Registers]] 的 recurrence 一致。

若 R 在 edge 附近变化，四个 d 的选择都可能违反 setup/hold；“方向只影响组合门”不表示它无需同步。实际按钮控制请先执行 [[Metastability and Clock Domain Crossing]] 的接口处理。

## Verification Plan · 验证路径

1. Test the DFF independently: edge capture and asynchronous reset.
2. Test right shift with several serial patterns from known initial state.
3. Test left shift and direction changes between edges.
4. Assert reset between edges and confirm immediate logical clearing.
5. Check all 16 old words × 2 directions × 4 serial-input pairs in a reference model.
6. Compare old-state-derived next words with the structural simulation trace.

行为模型可写 `qi <= sr & qi(3 downto 1)` 或 `qi <= qi(2 downto 0) & sl`，用于对照，并不能替代要求练习 port-map 的结构实现。

## Pitfalls and Exam English · 误区与答题

- Four FFs have one shared clock, not a clock derived from adjacent Q.
- Don't use a variable loop that repeatedly shifts a newly updated word during one edge.
- Internal `qi` provides feedback and avoids depending on output-port readability.
- Testbench signals and synthesizable entities belong to different roles.

**Answer:** “Direction selects the data source for each D input. At the active edge, all four DFFs capture simultaneously, so each bit moves exactly one stage using the previous register contents.”

## Connections · 相关笔记

[[VHDL Language and Modeling]], [[D Latch and D Flip-Flop]], [[Shift Registers]], [[Multiplexer and Demultiplexer]], [[Testbench and Functional Verification]], [[Field-Programmable Gate Array]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
