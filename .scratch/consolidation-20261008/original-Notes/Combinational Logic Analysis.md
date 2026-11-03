---
tags:
  - ECE2050
  - combinational-design
date: 2026-10-08
aliases:
  - Combinational Logic Analysis
  - 组合逻辑分析
  - Logic Circuit Analysis
---

# Combinational Logic Analysis · 组合逻辑分析

> [!SUMMARY] Quick recall · 英文速览
> Analyze a combinational circuit by naming internal nodes, writing one equation per gate, and substituting toward the output. Simplify only after the original function is clear, then compare all input combinations.

## Scope and Model · 范围与模型

**组合逻辑分析 (combinational logic analysis)** 从已有连接求输出函数；[[Combinational Logic Design|组合逻辑设计 (combinational logic design)]] 从规范选择连接。本篇集中讲课件 p.18–19 的电路化简，前置是 [[Combinational Circuit]] 的无反馈、单驱动构成规则。

所有输入、内部节点 (internal nodes) 与输出均为无量纲的 0/1。$+$ 是 OR，相乘是 AND，上横线是 NOT。分析假设输入电平有效、电路传播已稳定；稳态等价不保证相同的转换波形或延迟。

## Read the Circuit · 电路到方程

1. 确定主输入 (primary inputs)、主输出 (primary outputs) 和变量顺序，给内部节点命名为 $n_1,n_2,\ldots$。
2. 沿信号方向逐级写方程；先写 gate function，再代入该门的输入。
3. 单独记录每个反相气泡 (inversion bubble)；横线必须覆盖正确的变量或整个子式。
4. 同一节点的所有分支使用同一个值。实心圆点表示连接；无连接标记的交叉不能自行当成分叉。
5. 将内部节点逐层代入输出，再用 [[Laws and Rules of Boolean Algebra]] 或 [[Karnaugh Map]] 化简。
6. 按相同变量顺序穷举全部 $2^n$ 行，比较原始节点模型与最终表达式。

Keep the original equations as an independent reference. Deriving a truth table only from the simplified answer would not reveal a transcription error in the original circuit.

## Worked Example 1 · 重复支路被吸收，课件 p.18

主输入为 $A,B,C,D$，输出为 $X$。A、B、C 先各反相，再经过三输入 AND 和一个 NOT。令这段输出为 $n$：

$$
n=\overline{\bar A\bar B\bar C}=A+B+C.
$$

$n$ 一路直接送末级 OR，另一路与原始输入 $C$ 相与。D 直接送末级 OR，因此：

$$
\begin{aligned}
X&=nC+n+D\\
 &=n+D &&\text{absorption: }n+nC=n\\
 &=A+B+C+D.
\end{aligned}
$$

The direct branch $n$ already covers every case covered by $nC$. Removing that AND branch preserves the steady-state function. With a four-input OR available, the entire network reduces to one OR gate; with only two-input gates, a four-input OR requires a small tree.

| $ABCD$ | $n$ | $nC$ | Original $nC+n+D$ | Reduced $A+B+C+D$ |
|---|---|---|---|---|
| 0000 | 0 | 0 | 0 | 0 |
| 0001 | 0 | 0 | 1 | 1 |
| 0010 | 1 | 1 | 1 | 1 |
| 1000 | 1 | 0 | 1 | 1 |
| 1111 | 1 | 1 | 1 | 1 |

完整真值表只有 0000 一行输出为 0。这里先应用德摩根定理 (DeMorgan's theorem)，再应用吸收律；不能把 $\overline{\bar A\bar B\bar C}$ 误读为 $\bar A\bar B\bar C$。

## Worked Example 2 · 四乘积项化为两项，课件 p.19

原电路是四个 AND 输出送同一个 OR；变量顺序为 $ABCD$。从原图读到：

$$
X=A\bar B\bar C+AB\bar C\bar D
+\bar A\bar B\bar CD+\bar A\bar B\bar C\bar D.
$$

先合并只差 $D$ 的最后两项，再提取 $\bar C$：

$$
\begin{aligned}
X&=A\bar B\bar C+AB\bar C\bar D
+\bar A\bar B\bar C(D+\bar D)\\
 &=\bar C\,[A\bar B+AB\bar D+\bar A\bar B]\\
 &=\bar C\,[\bar B(A+\bar A)+AB\bar D]\\
 &=\bar C\,[\bar B+AB\bar D]\\
 &=\bar C\,(\bar B+A\bar D)\\
 &=\boxed{\bar B\bar C+A\bar C\bar D}.
\end{aligned}
$$

倒数第二步用 $U+\bar UV=U+V$，其中 $U=\bar B$、$V=A\bar D$。这一步删除了第二项中的 $B$，但没有删除公共因子 $\bar C$。

### K-map Cross-check · 卡诺图复核

$$
X=\sum m(0,1,8,9,12),\qquad i=8A+4B+2C+D.
$$

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 00 | 1 | 1 | 0 | 0 |
| 01 | 0 | 0 | 0 | 0 |
| 11 | 1 | 0 | 0 | 0 |
| 10 | 1 | 1 | 0 | 0 |

The four-cell group $\{0,1,8,9\}$ wraps across the top and bottom edges and gives $\bar B\bar C$. The two-cell group $\{8,12\}$ gives $A\bar C\bar D$. Cell 8 belongs to both groups, which is allowed.

![[combinational-reduction-kmap.svg]]
*图 1 — 课件 p.19 的四格组和两格组；虚线提示上下边相邻，$m_8$ 被重叠覆盖。蓝色组消去 A、D，红色组消去 B。*

Each group is necessary: $m_0$ needs the first implicant and $m_{12}$ needs the second. No eight-cell group is possible because it would include specified zeros. Thus these are the two essential prime implicants for the minimum SOP.

**代入检查。** 0001 由 $\bar B\bar C$ 覆盖；1100 由 $A\bar C\bar D$ 覆盖；1101 两项都为 0；任意 $C=1$ 都为 0。精简电路是一个二输入 AND、一个三输入 AND 与一个 OR；若反变量未直接提供，还需产生 $\bar B,\bar C,\bar D$。

## Bubble Pushing as Analysis · 用气泡推移读混合门

[[Universal Gates and Bubble Pushing#Worked Example 4 · 三级门链，课件 p.30–31|三级门链例题]] 从 NOR→NAND→NAND 得到：

$$
n_1=\overline{A+B},\qquad n_2=\overline{n_1C},\qquad
Y=\overline{n_2D}=\bar A\bar BC+\bar D.
$$

Writing node equations and redrawing equivalent gate symbols are two checks on the same function. Begin at the output when pushing bubbles; begin at the inputs when evaluating the original node equations.

## Limits and Common Errors · 边界与误区

- **横线范围错 (wrong complement scope)**：$\overline{PQ}+R$ 与 $\overline{PQ+R}$ 是不同函数。
- **丢掉共享节点 (lost fan-out)**：某节点直通输出的支路可能使另一支路被吸收，p.18 就是例子。
- **K-map 不跨边 (missed wrap-around)**：p.19 的四格组需要首尾行相邻。
- **把最小 SOP 当成唯一最优硬件**：门输入数、反相器、共享逻辑和延迟会影响实现代价。
- **把逻辑等价当成波形等价**：简化可能改变 [[Propagation Delay and Logic Hazards|延迟与逻辑冒险 (logic hazards)]]；采样电路还需满足 [[Setup and Hold Timing]]。

## Exam Recall · 英文答题与复习

“Let $n=\overline{\bar A\bar B\bar C}$. The output is $X=nC+n+D$. By absorption, $X=n+D=A+B+C+D$. The original and reduced circuits agree for all sixteen input combinations.”

For a K-map answer, state the variable order, ON set, group sizes, and resulting terms. A drawing without an equation leaves the reader unable to check whether a bubble or an input polarity was omitted.

## Sources · 来源

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.18–19：Example 2 / Example 3；p.30–31：三级气泡推移；[本地课件](../ECE2050-Chap5.pdf#page=18)。内部节点命名、逐步代数解释与边界分析为根据原图补充的推导。

## Connections · 相关笔记

[[Boolean Equation]]、[[Truth Table and Boolean Expression]] 用不同形式记录函数；[[Proof by Perfect Induction]] 说明穷举验证；[[Digital Logic Troubleshooting]] 将节点模型用于故障分析。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
