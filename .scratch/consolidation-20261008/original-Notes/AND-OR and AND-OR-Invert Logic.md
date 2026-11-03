---
tags:
  - ECE2050
  - combinational-design
date: 2026-10-08
aliases:
  - AND-OR and AND-OR-Invert Logic
  - 与或逻辑与与或非逻辑
  - AND-OR Logic
  - AND-OR-Invert Logic
  - AOI Logic
---

# AND-OR and AND-OR-Invert Logic · 与或逻辑与与或非逻辑

> [!SUMMARY] Quick recall · 英文速览
> AND-OR implements a sum of products. AND-OR-Invert (AOI) complements that sum and can be rewritten as a product of sums by DeMorgan's theorem. Input polarity and output polarity must be specified separately.

## Core Definition · 核心定义

**与或逻辑 (AND-OR logic)** 先用与门 (AND gates) 产生乘积项，再用或门 (OR gate) 合并。**与或非逻辑 (AND-OR-Invert logic, AOI)** 在这个结果上取反。它们把 [[Sum-of-Products Form|积之和 (SOP)]] 和 [[Product-of-Sums Form|和之积 (POS)]] 落实为门级电路 (gate-level circuit)。

本篇所有变量均为无量纲的布尔量，取值为 0 或 1；相邻变量表示 AND，$+$ 表示 OR，上横线表示 NOT。$A,B,C,D$ 是输入，$Y$ 是输出。真值表描述有效逻辑电平下、传播完成后的稳态功能。

| Structure · 结构 | Equation · 方程 | Interpretation · 含义 |
|---|---|---|
| AND-OR | $Y=AB+CD$ | 任意乘积项为 1，输出就为 1 |
| AND-OR-Invert | $Y=\overline{AB+CD}$ | 所有乘积项都为 0，输出才为 1 |
| AOI 的等价 POS | $Y=(\bar A+\bar B)(\bar C+\bar D)$ | 两个和项都为 1，输出才为 1 |

For an arbitrary SOP $F=P_1+\cdots+P_k$, AND-OR computes $F$, while AOI computes $\bar F$. DeMorgan gives $\bar F=\bar P_1\cdots\bar P_k$. Complementing each product creates the corresponding sum term.

![[and-or-aoi-logic.svg]]
*图 1 — 相同输入下，(a) 输出 $AB+CD$；(b) 输出其补 $\overline{AB+CD}$。输入与输出均明确标注，气泡表示最终反相。*

## Logic Levels and Gate Count · 逻辑级数与门数

**两级逻辑 (two-level logic)** 指主要组合结构的 AND→OR 或 OR→AND 两级，通常不计产生反变量的输入反相器 (input inverters)。它不限制第一层只能有两个门，也不限制每个门只能有两个输入。

AOI can be implemented by AND gates followed by a NOR gate. If OR and NOT are physically separate gates, that realization has an additional output stage. A Boolean form alone does not specify the physical propagation delay or packaged gate count.

课件 p.6 的图按 AND→OR→Invert 连接；同页 “ORs followed by ANDs” 对应德摩根变换后的等价 POS 形式 $(\bar A+\bar B)(\bar C+\bar D)$。读图时应先看横线覆盖范围，不能把 $\overline{AB+CD}$ 写成 $\overline{AB}+\overline{CD}$。

## Worked Example 1 · 课件 p.4 的 SOP

变量顺序取 $ABC$，课件三个乘积项是：

$$
Y=\bar A\bar B\bar C+A\bar B\bar C+A\bar BC
=\sum m(0,4,5).
$$

The term $\bar A\bar B\bar C$ selects 000; $A\bar B\bar C$ selects 100; $A\bar BC$ selects 101. A shared literal or a shared input inverter does not make the terms electrically connected at their outputs: the OR gate combines them.

可进一步化简为：

$$
Y=\bar B\bar C(\bar A+A)+A\bar BC
=\bar B(\bar C+AC)
=\bar B(\bar C+A).
$$

最后一步用吸收规则 (absorption rule) $X+\bar XZ=X+Z$。代入 000、100、101 得 1，001、111 得 0；完整 ON set 仍是 $\{0,4,5\}$。化简方法见 [[Boolean Expression Simplification]]。

## Worked Example 2 · 高有效液位传感器，课件 p.5

三个储罐的原始传感器电平为 $A,B,C$。**高有效 (active-high)** 表示输入为 1 时液位过低；报警输出 $H=1$ 表示至少两个储罐过低。

$$
H=AB+AC+BC=\sum m(3,5,6,7).
$$

This is the three-input majority function. “Any two” in this circuit includes the all-three case. The OR gate reports whether a pair exists; it does not count pairs.

| $ABC$ | 过低储罐数 | $H$ |
|---|---|---|
| 000 | 0 | 0 |
| 001 | 1 | 0 |
| 010 | 1 | 0 |
| 011 | 2 | 1 |
| 100 | 1 | 0 |
| 101 | 2 | 1 |
| 110 | 2 | 1 |
| 111 | 3 | 1 |

若要求“恰好两个 (exactly two)”，必须排除 111，输出应为 $\bar ABC+A\bar BC+AB\bar C$，不能继续用 $AB+AC+BC$。

## Worked Example 3 · 低有效传感器与 AOI，课件 p.7

**低有效 (active-low)** 表示原始电平 $A=0$ 时储罐 A 过低；B、C 同理。高有效报警的事件方程为：

$$
L=\bar A\bar B+\bar A\bar C+\bar B\bar C.
$$

课件用没有输入反相器的 AOI 结构实现它：

$$
\begin{aligned}
L&=\overline{AB+AC+BC}\\
 &=(\bar A+\bar B)(\bar A+\bar C)(\bar B+\bar C)\\
 &=\bar A\bar B+\bar A\bar C+\bar B\bar C.
\end{aligned}
$$

The complement of “at least two raw inputs are HIGH” is “at least two raw inputs are LOW” for exactly three Boolean inputs. This identity explains the output inverter in the source circuit; the sensor polarity by itself does not determine the alarm polarity.

| $ABC$ | 过低储罐数，即 0 的个数 | $AB+AC+BC$ | $L$ |
|---|---|---|---|
| 000 | 3 | 0 | 1 |
| 001 | 2 | 0 | 1 |
| 010 | 2 | 0 | 1 |
| 011 | 1 | 1 | 0 |
| 100 | 2 | 0 | 1 |
| 101 | 1 | 1 | 0 |
| 110 | 1 | 1 | 0 |
| 111 | 0 | 1 | 0 |

如报警器本身低有效，应输出 $\bar L=AB+AC+BC$。区分“发生低液位事件”和“对应电压是 LOW”可以避免重复反相。

## XOR and XNOR · 异或与同或的边界

课件 p.8–9 的**异或 (Exclusive-OR, XOR)** 与**同或 (Exclusive-NOR, XNOR)** 是另外两种常用组合函数，完整符号与推导分别在 [[Exclusive-OR Gate]]、[[Exclusive-NOR Gate]]。

$$
A\oplus B=A\bar B+\bar AB,
\qquad
\overline{A\oplus B}=AB+\bar A\bar B=(\bar A+B)(A+\bar B).
$$

For two inputs, XOR detects inequality and XNOR detects equality. For a reduction over several inputs, XOR reports an odd number of 1s. An even-parity **generator** uses that XOR result as its added bit; see [[Parity Bit]].

## Quick Check · 自检

1. $AB+CD$ 与 $\overline{AB+CD}$ 在每一行都互补；$AB+CD$ 不等于 $(A+B)(C+D)$。
2. 三个输入为 111 时，高有效传感器例题报警；低有效传感器例题不报警。
3. AND-OR 可有多个乘积项，每项也可有多个输入。
4. 门级实现需核对反相器、最大门输入数 (fan-in) 与 [[Propagation Delay and Logic Hazards|传播延迟 (propagation delay)]]。

## Sources · 来源

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.4–9：AND-OR、AOI、液位监测、XOR/XNOR；[本地课件](../ECE2050-Chap5.pdf#page=4)。两种极性的完整真值表与代数化简为根据原图展开的推导。

## Connections · 相关笔记

[[Combinational Logic Design]] 从需求确定函数；[[Combinational Logic Analysis]] 从已有电路恢复函数；[[DeMorgan's Theorems]] 支撑 AOI 的变换；[[Universal Gates and Bubble Pushing]] 给出 NAND/NOR 实现。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
