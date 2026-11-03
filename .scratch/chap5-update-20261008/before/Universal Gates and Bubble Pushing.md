---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
aliases:
  - 通用门与气泡推移
  - Universal Gates and Bubble Pushing
  - Universal logic gates
---

# Universal Gates and Bubble Pushing · 通用门与气泡推移

> [!SUMMARY] Quick recall · 英文速览
> NAND and NOR are functionally complete. Bubble pushing applies DeMorgan's laws to a gate symbol while preserving its function; every moved complement must be accounted for.

## Core Definition · 核心定义

功能完备 (functional completeness) 指只用某一种门，就能实现任意 Boolean function。NOT、AND、OR 足以从真值表构造 canonical SOP；若能用 NAND 或 NOR 实现这三种运算，就证明其通用性。

## Derivation · 基本构造

用 $\operatorname{NAND}(A,B)=\overline{AB}$：

$$\bar A=\operatorname{NAND}(A,A),$$
$$AB=\operatorname{NAND}(\operatorname{NAND}(A,B),\operatorname{NAND}(A,B)),$$
$$A+B=\operatorname{NAND}(\bar A,\bar B).$$

NOR 的对应式是 $\bar A=\operatorname{NOR}(A,A)$，$A+B=\overline{\operatorname{NOR}(A,B)}$，$AB=\operatorname{NOR}(\bar A,\bar B)$。所有取补都可用同类门完成。

**SOP → NAND–NAND.** 对 $Y=P_1+P_2$，写 $Y=\overline{\bar P_1\bar P_2}$。第一层给出补乘积，第二层 NAND 恢复 OR。POS 同理得到 NOR–NOR。Literal inverters count as additional gates when complementary inputs are not available.

## Bubble Pushing · 气泡推移

根据 [[DeMorgan's Theorems]]，NAND 可画成**输入有气泡的 OR**，NOR 可画成输入有气泡的 AND。门体 AND↔OR 改变，输入/输出取补同步改变；不是只在一条线上随意加气泡。

Two inversion bubbles cancel only when they represent consecutive complements on the same signal. If a wire branches, changing its interpretation must preserve every branch. Work from the output toward the inputs and write an intermediate equation after each transformation.

| Original | Equivalent interpretation | Common wrong claim |
|---|---|---|
| NAND | Negative-OR | Negative-AND |
| NOR | Negative-AND | Negative-OR |
| Two NOT stages | Buffer function | Zero physical delay |

## Worked Examples · 例题

**Example 1.** $Y=AB+CD$。令 $n_1=\overline{AB},n_2=\overline{CD}$，$Y=\overline{n_1n_2}$，共三个二输入 NAND。输入 ABCD=1100 时 $n_1=0,n_2=1,Y=1$；0010 时 $n_1=n_2=1,Y=0$。

**Example 2.** $Y=(A+B)(C+D)$。令 $n_1=\overline{A+B},n_2=\overline{C+D}$，$Y=\overline{n_1+n_2}$，共三个二输入 NOR。0001 → 0；1001 → 1，均符合原 POS。

**Example 3.** 没有反相信号时，$Y=\bar AB+AC$ 的 NAND 实现需先产生 $\bar A$，再计算两个补乘积与末级 NAND，共四个 NAND。题目若说 complementary inputs are directly available，才可不计该 inverter。

## Method and Exam English · 方法与答题

1. Obtain a clear SOP for NAND or POS for NOR.
2. Apply an outer double complement and DeMorgan's law.
3. Name internal nodes so each gate input is unambiguous.
4. Count gates, input fan-in, and inversion stages under the actual constraints.
5. Verify the truth table; then evaluate physical delay separately.

“Only NAND gates” forbids a standalone NOT symbol unless it is implemented by a tied-input NAND. “Basic gates” may permit NOT, AND, and OR; read the listed allowance.

## Connections · 相关笔记

[[NAND Gate]], [[NOR Gate]] supply the primitives. [[Combinational Logic Design]] supplies functions. [[Propagation Delay and Logic Hazards]] explains why Boolean equivalence does not imply identical timing.

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
