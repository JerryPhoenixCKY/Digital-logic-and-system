---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
updated: 2026-10-08
aliases:
  - 通用门与气泡推移
  - Universal Gates and Bubble Pushing
  - Universal logic gates
---

# Universal Gates and Bubble Pushing · 通用门与气泡推移

> [!SUMMARY] Quick recall · 英文速览
> NAND and NOR are functionally complete. Bubble pushing applies DeMorgan's laws to a gate symbol while preserving its function; every moved complement must be accounted for.

## Core Definition · 核心定义

通用门 (universal gate) 的功能完备性 (functional completeness) 指只用该门，就能实现任意布尔函数 (Boolean function)。NOT、AND、OR 足以从真值表构造标准积之和 (canonical SOP)；若能用 NAND 或 NOR 实现这三种运算，就证明其通用性。所有输入、内部节点和输出都为无量纲的 0/1；本篇等价关系按有效电平下的稳态模型判断。

## Derivation · 基本构造

用 $\operatorname{NAND}(A,B)=\overline{AB}$：

$$\bar A=\operatorname{NAND}(A,A),$$
$$AB=\operatorname{NAND}(\operatorname{NAND}(A,B),\operatorname{NAND}(A,B)),$$
$$A+B=\operatorname{NAND}(\bar A,\bar B).$$

NOR 的对应式是 $\bar A=\operatorname{NOR}(A,A)$，$A+B=\overline{\operatorname{NOR}(A,B)}$，$AB=\operatorname{NOR}(\bar A,\bar B)$。所有取补都可用同类门完成。

### Complete Construction Table · 完整基本门构造，课件 p.24–25

令 $N(A,B)=\overline{AB}$ 表示二输入 NAND，$R(A,B)=\overline{A+B}$ 表示二输入 NOR。以下假设只有原始输入 A、B 可用，不预先提供反变量；同名中间节点只生成一次。

| Allowed gates | Target | Node equations | Gate count |
|---|---|---|---|
| NAND only | NOT | $Y=N(A,A)=\bar A$ | 1 |
| NAND only | AND | $t=N(A,B),\ Y=N(t,t)$ | 2 |
| NAND only | OR | $a=N(A,A),\ b=N(B,B),\ Y=N(a,b)$ | 3 |
| NAND only | NOR | 上行 OR 输出为 $t$，再 $Y=N(t,t)$ | 4 |
| NOR only | NOT | $Y=R(A,A)=\bar A$ | 1 |
| NOR only | OR | $t=R(A,B),\ Y=R(t,t)$ | 2 |
| NOR only | AND | $a=R(A,A),\ b=R(B,B),\ Y=R(a,b)$ | 3 |
| NOR only | NAND | 上行 AND 输出为 $t$，再 $Y=R(t,t)$ | 4 |

Tying the two gate inputs to the same signal creates an inverter. It does not mean that two gate outputs are connected together. Gate counts change if complementary inputs are supplied or if a result can be shared elsewhere.

**SOP → NAND–NAND.** 对 $Y=P_1+P_2$，写 $Y=\overline{\bar P_1\bar P_2}$。第一层给出补乘积，第二层 NAND 恢复 OR。POS 同理得到 NOR–NOR。Literal inverters count as additional gates when complementary inputs are not available.

For POS $Y=S_1S_2$, write $Y=\overline{\bar S_1+\bar S_2}$. The first NOR layer computes complemented sums and the final NOR restores the product. Arbitrary SOP/POS functions remain implementable when fan-in is limited, but the circuit may need additional stages.

## Bubble Pushing · 气泡推移

根据 [[DeMorgan's Theorems]]，NAND 可画成**输入有气泡的 OR**，NOR 可画成输入有气泡的 AND。门体 AND↔OR 改变，输入/输出取补同步改变；不是只在一条线上随意加气泡。

反相气泡 (inversion bubble) 是逻辑补的符号。**气泡推移 (bubble pushing)** 向后推时，把一个输出气泡移到所有输入，同时交换 AND/OR 门体；向前推时，必须对所有输入上的气泡一起处理，再移到输出。只推一条输入、遗漏另一条，会改变函数。

![[demorgan-gate-equivalence.svg]]
*图 1 — NAND = negative-OR；NOR = negative-AND。等价符号的输入气泡只作用于它们各自的输入。*

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

## Worked Example 4 · 三级门链，课件 p.30–31

原图依次是一个 NOR、两个 NAND；A、B 送第一门，C 送第二门，D 送末门。先用内部节点写出原电路：

$$
n_1=\overline{A+B},\qquad
n_2=\overline{n_1C},\qquad
Y=\overline{n_2D}.
$$

从输出向输入推气泡，并保留每个门的取补：

$$
\begin{aligned}
Y&=\bar n_2+\bar D &&\text{final NAND as negative-OR}\\
 &=n_1C+\bar D &&\text{two consecutive complements cancel}\\
 &=\overline{A+B}\,C+\bar D\\
 &=\boxed{\bar A\bar BC+\bar D} &&\text{NOR as negative-AND}.
\end{aligned}
$$

![[bubble-pushing-cascade.svg]]
*图 2 — (a) 原 NOR→NAND→NAND 链；(b) 等价的输入反相 AND→AND→输入 D 带气泡的 OR。内部节点与最终表达式采用同一极性。*

**Boundary checks.** If D=0, the final NAND must output 1, matching $\bar D=1$. If D=1, $Y=\bar A\bar BC$, so only ABC=001 asserts the output. All sixteen ABCD patterns agree between the original node equations and the reduced form.

末级 D 输入上的气泡找不到相邻输出气泡抵消，因此必须保留 $\bar D$。把它省略为 D 会在 D=0 时立即给出错误结果。物理上的两个反相器虽逻辑抵消，仍有延迟和负载。

## Method and Exam English · 方法与答题

1. Obtain a clear SOP for NAND or POS for NOR.
2. Apply an outer double complement and DeMorgan's law.
3. Name internal nodes so each gate input is unambiguous.
4. Count gates, input fan-in, and inversion stages under the actual constraints.
5. Verify the truth table; then evaluate physical delay separately.

“Only NAND gates” forbids a standalone NOT symbol unless it is implemented by a tied-input NAND. “Basic gates” may permit NOT, AND, and OR; read the listed allowance.

## Connections · 相关笔记

[[NAND Gate]], [[NOR Gate]] supply the primitives. [[Combinational Logic Design]] supplies functions. [[Propagation Delay and Logic Hazards]] explains why Boolean equivalence does not imply identical timing.

## Sources · 来源

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.24–25、27–31；[本地课件](../ECE2050-Chap5.pdf#page=24)。基本门构造、三级电路的节点方程与气泡步骤均对照原图；门数按二输入门且反变量未提供的条件计算。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
