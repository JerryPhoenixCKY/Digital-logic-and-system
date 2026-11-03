---
tags:
  - ECE2050
  - hardware-description
date: 2026-09-30
aliases:
  - VHDL语言与建模
  - VHDL Language and Modeling
  - VHSIC Hardware Description Language
---

# VHDL Language and Modeling · VHDL语言与建模

> [!SUMMARY] Quick recall · 英文速览
> An entity defines an interface; an architecture defines its implementation. Statements in a process run sequentially during an activation, while processes and concurrent statements describe concurrent hardware.

## Core Definition · 核心定义

VHDL 是 hardware description language。entity 声明 ports，architecture 声明内部 signals 与逻辑。dataflow 用 concurrent equations，structural 用 instances/port map，behavioral 常用 process 描述。不同风格可以描述相同的硬件。

采用 `IEEE.std_logic_1164` 的 logic types；算术用 `IEEE.numeric_std` 中 `unsigned`/`signed` 明确数值含义。`std_logic_vector` 本身是一组逻辑值，没有自动确定的 signed 数值解释。

## Types and Operators · 类型与运算

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

## Concurrent and Sequential Semantics · 并发与顺序语义

```vhdl
-- Concurrent dataflow: both equations exist at the same time.
p <= a xor b;
s <= p xor cin;
```

p 更新会在仿真的后续 delta cycle 触发 s 更新；零时间 delta 是模拟调度，不是实际门延迟。把两个语句上下交换，不改变此 dataflow network。

```vhdl
process(clk)
begin
  if rising_edge(clk) then
    q1 <= d;
    q2 <= q1;
  end if;
end process;
```

q2 读旧 q1，所以是两个寄存器级，不是同一边沿 d 直接到 q2。变量赋值 `v := d; q2 <= v;` 则 q2 读取本次新 v；语言语义改变了数据路径。

## Combinational versus Clocked Process · 组合与时钟过程

```vhdl
process(a, b, sel)
begin
  y <= a;                 -- default assigns all paths
  if sel = '1' then
    y <= b;
  end if;
end process;
```

Explicit sensitivity lists must include all read signals for this combinational model. `process(all)` is the VHDL-2008 alternative when the configured tool mode supports it. Omitting a required signal can make simulation stale while synthesis still builds input-dependent logic.

如果 combinational process 的某些路径不给 y 赋值，就表示保留旧值，可能推断 latch。clocked process 省略 inactive-edge assignment 是正常 FF hold；同样的“不赋值”要结合事件结构判断。

## Reset Examples · 复位例题

```vhdl
-- Synchronous, active-high reset; reset outranks enable.
process(clk)
begin
  if rising_edge(clk) then
    if rst = '1' then
      q <= (others => '0');
    elsif en = '1' then
      q <= d;
    end if;
  end if;
end process;
```

Asynchronous reset moves the reset test before `rising_edge` and includes rst in `process(clk, rst)`. A reset inside the rising-edge conditional cannot reset between edges merely because rst appears in the sensitivity list.

## Worked Examples · 例题

**Unsigned comparison.** `greater <= '1' when unsigned(a) > unsigned(b) else '0';`，对 a=1000,b=0111 得1。换为 `signed` 时 a=−8,b=7，输出0。类型决定 interpretation，位串本身没有改变。

**Width.** 两个4位 unsigned 相加可能需要5位。先 `resize` operands 到5位再加才能保留 carry；只把4位结果赋给5位目标，不能保证此前被截掉的 carry 自动回来。

**Process trap.** `if en='1' then q<=d; end if;` 在 level-sensitive `process(en,d)` 中是 latch；在 `if rising_edge(clk)` 内则是 enabled FF。所谓 “behavioral is sequential” 只描述语句执行顺序，不意味着必然生成时序电路。

## Coding Review and Boundaries · 编写检查与边界

- Basic identifiers are case-insensitive; avoid consecutive/trailing underscores and reserved words.
- Use ordinary straight quotes and matching `end if`, `end process`, and architecture boundaries.
- Named port maps make connection intent clearer than long positional lists.
- Do not use `inout` merely to read an ordinary output; use an internal signal. Output readability also depends on the language revision.
- `'-'` is a simulation logic value, not automatic wildcard equality; use an explicit matching operation or specified synthesis don't-care treatment.

The snippets explain language and hardware behavior. Their enclosing declarations, vector widths, and library context must be supplied consistently before compiling. They are not a claim that a particular installed tool version was tested.

## Exam English and Connections · 答题与关联

**Answer:** “The two signal assignments inside the clocked process both evaluate their right-hand sides using the pre-update signal values. Therefore q2 receives the previous q1 and the circuit forms a two-stage register chain.”

[[Combinational Circuit]], [[Sequential Logic]], [[D Latch and D Flip-Flop]], [[Register Enable and Reset]], [[Tri-State Buffers and Bus Drivers]], [[Structural Shift Register Project]], [[Testbench and Functional Verification]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
