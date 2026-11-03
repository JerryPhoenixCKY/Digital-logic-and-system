---
tags:
  - ECE2050
  - karnaugh-map
date: 2026-09-16
updated: 2026-10-09
chapter: Ch4
aliases:
  - 卡诺图化简
  - Karnaugh Map Minimization
  - 卡诺图化简 · Ch4
  - Karnaugh Map
  - 卡诺图
  - K 图
  - K-Map
  - Karnaugh Map with Don't Cares
  - 含无关项的卡诺图
  - 无关项
  - 卡诺图无关项
  - Don't Care Conditions
  - POS Minimization with Karnaugh Map
  - 卡诺图 POS 最小化
  - 卡诺图求最小或与式
  - 用卡诺图求 POS
  - K-Map POS Minimization
---

# Karnaugh Map Minimization · 卡诺图化简

> [!SUMMARY] Quick recall · 英文速览
> Gray-code adjacency makes a group eliminate changing variables. Group 1s for SOP, 0s for POS, and use don't-cares only when the specification permits them.

## 1 · Karnaugh Map · 为什么相邻格能够合并

卡诺图 (Karnaugh map) 用 Gray 顺序 00、01、11、10 排列，每对相邻格只差一个变量。图的首尾边相邻，四角可成组；对角线不相邻。组为 $2^k$ 格矩形，变化的 k 个变量被消去。

### 布局、坐标与代数含义 (layout and adjacency)

每格代表一个输入组合，即一个最小项的座位，n变量有 $2^n$ 格。三变量通常2×4、四变量4×4；本课图中AB/CD的行列有转置，读图必须以图上的变量标签为准，不能按画面位置猜位权。

| 变量数 | 一种惯用行标签 | 列标签 | 格数 |
|---|---|---|---|
| 3 | C=0、1 | AB=00、01、11、10 | 8 |
| 4 | CD=00、01、11、10 | AB=00、01、11、10 | 16 |

自然二进制编号用于行号，Gray排列用于格子位置，两者不可混淆。AB=10、CD=01表示输入1001，对应 $m_9$；不是把第几列第几行直接拼成自然序号。行列转置不改变逻辑邻接；首尾回绕、四角可共同成组，对角线通常差两位，不能组成二格组。

组对应一个布尔子立方体 (Boolean cube)：k个自由变量必须出现全部 $2^k$ 种组合，其余变量固定。三/四变量图上的合法组是边长为2的幂的矩形，可跨边界；总格数为2的幂还不充分，L形4格也非法。组大小 $2^k$ 时消去k个变量、保留n−k个文字，其代数基础是 $X\bar Y+XY=X$。

### 适用规模与证明责任 (validity)

先有完整的0/1/X规范或准确标准项列表，才能填图；遗漏格就是改变函数。K图适于少变量的人工化简，5变量可用两张相关图、6变量也有扩展画法，但更大域通常由算法/综合工具处理。Quine–McCluskey等精确算法本身也会随规模增长，不能把它说成任意大问题的轻松替代。

分组结果必须在所有指定行正确；“最大组”降低单项文字数，“最小覆盖”降低整个函数项数，两者不同。物理静态冒险可能要求冗余共识项 (consensus term)，这时应清楚说明优化目标包含时序要求，见 [[Propagation Delay and Logic Hazards]]。

> [!example]- Karnaugh Map · 推导与例题
> **图示与讲义依据**
>
> ![[kmap-rules.svg]]
> *图 1 — (a) 两种尺寸的编号布局：每格标出 minterm 编号 $m_i$ 与它的 `ABCD` 编码，行列都按格雷码 `00 01 11 10`，
> 因此任意两个相邻格（含跨边界相邻）只差一位。(b) 合法与非法圈组对照：$1\times2$ 对、$2\times2$ 方阵、四角回绕
> 都合法；斜对角、3 格、L 形都不合法。虚线框表示"左右两条边界是接起来的"（回绕）。*
>
> **Derivation · 推导过程**
>
> **1. 为什么相邻两格能合并：$X\bar Y+XY=X$**
>
> 相邻（只差一个变量）意味着两格的积项可以写成同一个"其余部分 $X$"乘上"变化那位的两种取值"：
>
> $$
> \underbrace{X\bar Y}_{Y=0 \text{ 的格}}+\underbrace{XY}_{Y=1 \text{ 的格}}
> =X(\bar Y+Y)=X\cdot 1=X
> $$
>
> - **意义**：两格合并后，那个**变来变去**的变量（$Y$）连同它的横线一起消失，只剩两格**共同**的 $X$。圈组五规则的
>   第 2–5 条（水平/竖直、2 的幂、尽量大、可回绕）本质上都是"找更多只差一个变量的格"。
> - **数值校验**：$B=1,C=1$ 固定时，$A$ 的两种取值给出 $m_7=ABC$ 与 $m_3=\bar ABC$；
>   $ABC+\bar ABC = BC(A+\bar A)=BC\cdot1=BC$ ✓（这就是下面例题 1 里的第二个圈）。
> - 行列表头之所以必须是格雷码：只有相邻编号**只差一位**，"两格合并消一个变量"才成立；用自然二进制编号，
>   相邻两格可能差两三位，$X\bar Y+XY$ 这套就套不上去（[[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束|Gray Code]] 里"相邻只差 1 位"就是为它服务的）。
>
> **2. 圈多大，就消掉几个变量**
>
> 一般地，若一个圈内**恰好有 $k$ 个变量在变化**，则这 $k$ 个变量全部消掉，**积项的 literal 数 $=n-k$**：
>
> | 圈的大小 | 变化的变量数 $k$ | 积项 literal 数（$n=4$） | 例子 |
> |---|---|---|---|
> | 1 格 | 0 | 4 | $A\bar BC\bar D$ |
> | 2 格 | 1 | 3 | $\bar ABD$ |
> | 4 格 | 2 | 2 | $\bar AC$ |
> | 8 格 | 3 | 1 | $B$ |
> | 16 格 | 4 | 0 | $Y=1$（全 1） |
>
> - **意义**：圈越大越省。规则 4"每个圈要尽可能大"就是这条的直接推论：$2$ 格的圈留 3 个字母，$4$ 格的圈只留 2 个。
> - **数值校验**：例题 1 的 `AB=01` 竖直 2 格圈里 $C$ 在变 → $n-k=3-1=2$ 个 literal，正是 $BC$ ✓；
>   例题 3 的 $\bar AC$ 是 4 格圈，$B,D$ 两个变量在变 → $4-2=2$ 个 literal ✓。
>
> **3. 从一个圈读出积项（本课最核心的一步）**
>
> 1. 圈里**一直为 1** 的变量 → 写**原变量**（如 $B$）；
> 2. 圈里**一直为 0** 的变量 → 写**反变量**（如 $\bar D$）；
> 3. 圈里**又 0 又 1** 的变量 → **直接丢掉**。
>
> 把所有圈的积项 **OR** 起来，就是最小 SOP（这就是 [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 的形式）。圈 0 时的对偶规则
> （0 写原变量、1 写反变量、再 AND）见 [[Karnaugh Map Minimization#3 · POS Minimization with Karnaugh Map · 圈 0 读和项|POS Minimization with Karnaugh Map]]。
>
> **Worked Example · 例题**
>
> **Example 1 — 3 变量：讲义 p.50**
>
> 题目：由下表求真值表对应的最小 SOP。
>
> | $A$ | $B$ | $C$ | $Y$ |
> |---|---|---|---|
> | 0 | 0 | 0 | 0 |
> | 0 | 0 | 1 | 0 |
> | 0 | 1 | 0 | 1 |
> | 0 | 1 | 1 | 1 |
> | 1 | 0 | 0 | 0 |
> | 1 | 0 | 1 | 0 |
> | 1 | 1 | 0 | 0 |
> | 1 | 1 | 1 | 1 |
>
> 解：
> 1. 画 $2\times4$ 框：列 `AB` = `00 01 11 10`，行 `C` = `0`,`1`。
> 2. 填格：输出为 1 的是 $m_2,m_3,m_7$，其余填 0。
> 3. 圈：$\{m_2,m_3\}$ 是 `AB=01` 这一列的上下两格 → 2 格圈，$C$ 在变、$A=0,B=1$ 不变 → $\bar AB$；
>    $\{m_3,m_7\}$ 是 `C=1` 这一行的左右两格 → 2 格圈，$A$ 在变、$B=1,C=1$ 不变 → $BC$。
> 4. 两个圈 OR 起来：$Y=\bar AB+BC$。
>
> **数值校验 (Numerical check)**：把两项代回全部8行（$m_0\ldots m_7$ 顺序读）：
>
> | $ABC$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
> |---|---|---|---|---|---|---|---|---|
> | 真值表 $Y$ | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 |
> | $\bar AB+BC$ | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 |
>
> 逐列相同 ✓（Python 枚举 8 种输入：真值表 `00110001`，式子 `00110001`，完全一致）。
> 另一个自检：$\bar AB$ 覆盖 $\{m_2,m_3\}$、$BC$ 覆盖 $\{m_3,m_7\}$，并集 $\{m_2,m_3,m_7\}$ = 真值表里所有 1 ✓；
> 穷举最小化程序也确认 **2 项 / 4 个 literal 已是最小**（一个乘积项的ON集合必须有 $2^k$ 格，不能恰好覆盖本题3个1；所给两组达成下界）。
>
> **抄式子别丢横线**
> 讲义 p.50 的答案写成 $\bar AB+BC$（$A$ 上有一条横线）。从 PDF 里取文字时上划线经常被丢掉，
> 只剩 "AB + BC" ——那对应的是 $m_6,m_7,m_3$，与本题的 1 不符。**算式抄下来一定要用真值表回代一遍。**
>
> ![[ch4-kmap-3var-basic.png]]
> *图 2 — 讲义 p.50 原图：左边 3 变量真值表、右边同一张表的卡诺图，两个 2 格圈分别读出 $\bar AB$ 与 $BC$。*
>
> **Example 2 — 3 变量：讲义 p.51（6 项压成 3 项）**
>
> 题目：化简 $Y=\bar A\bar B\bar C+\bar A\bar BC+\bar AB\bar C+ABC+A\bar B\bar C+A\bar BC$。
>
> 解：
> 1. 六个项对应 $m_0,m_1,m_2,m_4,m_5,m_7=1$，只有 $m_3,m_6$ 是 0。
> 2. 圈 $\{m_0,m_1,m_4,m_5\}$：`B=0` 的四格构成一个 $2\times2$ 圈，$A,C$ 在变 → $\bar B$。
> 3. 圈 $\{m_0,m_2\}$：`A=0,C=0` 的两格 → $\bar A\bar C$。
> 4. 圈 $\{m_5,m_7\}$：`A=1,C=1` 的两格 → $AC$。
> 5. $Y=\bar B+\bar A\bar C+AC$（讲义 p.51 的答案）。
>
> **数值校验 (Numerical check)**：$\bar B$ 覆盖 $\{0,1,4,5\}$、$\bar A\bar C$ 覆盖 $\{0,2\}$、$AC$ 覆盖 $\{5,7\}$，
> 并集 $\{0,1,2,4,5,7\}$ 正好是真值表的全部 1（$m_3,m_6$ 为 0）✓。Python 枚举 8 行：
> 真值表 `11101101`，式子 `11101101`，逐行一致 ✓。代价对比：原来 6 项 18 个 literal，现在 **3 项 5 个 literal**。
>
> ![[ch4-kmap-3var-example.png]]
> *图 3 — 讲义 p.51 原图：同一个 3 变量图上的第二例，六个圈合并成三个（$\bar B$ 吃掉中间四格）。*
>
> **Example 3 — 4 变量：讲义 p.52**
>
> 题目：由下列真值表（讲义把它横过来写：每个变量占一行、16 列对应 $m_0\ldots m_{15}$）求最小 SOP。
>
> | 变量 | $m_0$ | $m_1$ | $m_2$ | $m_3$ | $m_4$ | $m_5$ | $m_6$ | $m_7$ | $m_8$ | $m_9$ | $m_{10}$ | $m_{11}$ | $m_{12}$ | $m_{13}$ | $m_{14}$ | $m_{15}$ |
> |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
> | $A$ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
> | $B$ | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
> | $C$ | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
> | $D$ | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
> | $Y$ | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
>
> 解：
> 1. 把 1 填进图（行 `CD`、列 `AB`，见下表；讲义 p.52 的图就是这个排布）：
>
> | $CD \backslash AB$ | 00 | 01 | 11 | 10 |
> |---|---|---|---|---|
> | 00 | 1 | 0 | 0 | 1 |
> | 01 | 0 | 1 | 0 | 1 |
> | 11 | 1 | 1 | 0 | 0 |
> | 10 | 1 | 1 | 0 | 1 |
>
> 2. 四个圈：
>    - $\{m_3,m_7,m_2,m_6\}$：`A=0`（列 `00`,`01`）且 `C=1`（行 `11`,`10`）→ $2\times2$ 圈 → $\bar AC$；
>    - $\{m_5,m_7\}$：`A=0,B=1,D=1`，$C$ 在变 → 2 格圈 → $\bar ABD$；
>    - $\{m_8,m_9\}$：`A=1,B=0,C=0`，$D$ 在变 → 2 格圈 → $A\bar B\bar C$；
>    - $\{m_0,m_2,m_8,m_{10}\}$：`B=0,D=0` 且 `A,C` 在变 → **四角回绕**的 4 格圈 → $\bar B\bar D$。
> 3. $Y=\bar AC+\bar ABD+A\bar B\bar C+\bar B\bar D$。
>
> **数值校验 (Numerical check)**：$\bar AC$ 覆盖 $\{2,3,6,7\}$、$\bar ABD$ 覆盖 $\{5,7\}$、$A\bar B\bar C$ 覆盖 $\{8,9\}$、
> $\bar B\bar D$ 覆盖 $\{0,2,8,10\}$，并集 $\{0,2,3,5,6,7,8,9,10\}$ 与真值表 16 行的 1 完全吻合 ✓。
> Python 枚举 16 种输入：真值表 `1011011111100000`，式子 `1011011111100000`，逐位一致 ✓；
> 穷举最小化确认它是最小的 **4 项 / 10 个 literal**（其中 $\bar AC$、$A\bar B\bar C$、$\bar ABD$ 各覆盖了只能由该主蕴含项覆盖的指定1格，因而都是必要主蕴含项）。
> 最后一个格是四角圈：$m_0$与 $m_{10}$本身相差A/C两位，不能独立圈成二格；四角组 $\{0,2,8,10\}$ 同时包含A/C的全部组合，因而可作为回绕四格矩形——这就是规则 5 的价值。
>
> ![[ch4-kmap-4var.png]]
> *图 4 — 讲义 p.52 原图：4 变量图（行 `CD`、列 `AB`）与四个圈；答案 $\bar AC+\bar ABD+A\bar B\bar C+\bar B\bar D$ 中
> 三条横线同样会在 PDF 取文字时丢失。*
>
> **Group meaning and implementation choices · 圈组含义与实现选择**
>
> Each power-of-two group removes the variables that change within it. The surviving literals describe every covered row, including wrapped edge cells. Gray-code ordering makes neighboring cells differ in one variable; ordinary binary order does not preserve that adjacency around the map.
>
> An essential prime implicant covers at least one ON cell that no other prime implicant covers. Include it, then cover the remaining required cells. A valid cover is not automatically a minimum cover; compare alternatives under the stated term/literal metric. Physical hazard requirements can justify a redundant consensus group.
>
> **Worked application.** ABCD 域中ON set=0,2,8,10。这四行的B=D=0，而A/C全部组合都出现；四个角回绕成一组，得到 $F=\bar B\bar D$。对索引10=1010代入得1，对索引11=1011因D=1得0。
>
> **English exam question:** Why cannot two diagonal cells be grouped merely because they look close?
>
> **Answer:** A legal adjacent grouping corresponds to variation in exactly the eliminated variables over a rectangular power-of-two set. A diagonal pair usually differs in two variables and cannot remove just one literal. Apply the result to [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]] and verify transient needs with [[Propagation Delay and Logic Hazards]].

## 2 · SOP 圈 1：覆盖与最小性

覆盖所有指定 1，禁止包含指定 0。优先使用最大组，允许重叠；必要时跨边连接。圈内保持 1 的变量原写，保持 0 的变量取补。不能只追求“圈数量少”而忽略文字数与必要蕴含项。

### SOP圈组五规则与全局覆盖 (cover method)

1. 覆盖每个指定1至少一次，不能含指定0；允许组间重叠。
2. 按横/竖邻接构成矩形，不能斜着圈，不能圈3格、6格或L形。
3. 每个方向跨度为1、2、4…，并试图扩成更大合法组。
4. 使用左右/上下边界回绕，四角可成四格组。
5. 各组内恒1的变量原写、恒0的变量取补，变化变量消去，最后将乘积项相OR。

主蕴含项 (prime implicant) 是不能再扩大的合法1组；必要主蕴含项 (essential prime implicant) 覆盖了至少一个**不被其他主蕴含项覆盖**的指定1。先选必要项，再为其余1比较候选覆盖。只看某格“好像只有一种画法”容易漏掉另一种最大组，应核对全部候选主蕴含项。

最小两级SOP通常按项数首先最少，其次在该项数下使**总文字数**最少。一个覆盖所有1的合法方案，只证明正确；一组一组都已扩到最大也未必证明全局minimum。可用必要项证明下界，再比较剩余覆盖，或用精确覆盖算法确认。删除一个组前应检查是否仍覆盖全部指定1。

零函数没有1组，结果为0；全1图可圈全域，所有变量消去，结果为1。最后列出每组行号、保留/消去变量、最终式，并回代完整指定真值表。最小SOP与最小POS项数、文字数及实际门族成本需分别比较。

## 3 · POS Minimization with Karnaugh Map · 圈 0 读和项

圈内保持 0 的变量原写，保持 1 的变量取补，再把所得和项相与。相邻 1/0 的拓扑相同，但读出文字极性的规则相反。检查每个和项在其零圈上确为 0。

### 圈0是反函数的SOP再取补 (POS method)

对 $\bar F$ 圈1，就等价于对F圈0；若 $\bar F=T_1+\cdots+T_r$，由DeMorgan得 $F=\bar T_1\cdots\bar T_r$。所以每个零组读为一个**和项 (sum term)**，最后相与；仅当组只有一格并含全域变量时，这一和项才是严格的**最大项 (maxterm)**。扩大的零组不再包含全域，不能都称为maxterm。

| 组内变量 | 圈1的乘积项 | 圈0的和项 |
|---|---|---|
| 恒0 | $\bar X$ | X |
| 恒1 | X | $\bar X$ |
| 有变化 | 消去 | 消去 |

步骤是按变量标签填0/1/X → 找最大合法零组（包括孤立单格） → 先选必要零组再比较覆盖 → 依上表读和项 → 所有和项AND → 验证指定0全为0、指定1全为1。零组不得包含指定1，必须覆盖全部指定0，允许重叠、回绕和有帮助的X。

误用圈1的极性或把零组项写成“乘积相OR”都改变函数；不能概括成“任何极性误写都会恰好得到反函数”，须回代实际式子查错。全0图圈全域得和项0、F=0；全1图没有零组，空AND得F=1。无X时最小SOP/POS逐行等价；有X时只需在全部指定行一致，各自完成的X行可能不同。

> [!example]- POS Minimization with Karnaugh Map · 推导与例题
> **Derivation · 推导过程**
>
> 以讲义 p.56 的例题为例：标准 POS 的六个和项说明函数在 **$m(1,2,3,4,9,12)$ 这 6 行上为 0**，
> 其余 10 行为 1。填成四变量卡诺图（行 `CD`、列 `AB`，Gray 码排列）：
>
> | $AB\backslash CD$ | 00 | 01 | 11 | 10 |
> |---|---|---|---|---|
> | **00** | 1 | **0** | **0** | **0** |
> | **01** | **0** | 1 | 1 | 1 |
> | **11** | **0** | 1 | 1 | 1 |
> | **10** | 1 | **0** | 1 | 1 |
>
> **（1）圈 0（求最小 POS）**：
>
> | 圈 | 覆盖 | 圈内 $A,B,C,D$ | 读出的和项 |
> |---|---|---|---|
> | ① | $0010,0011$ | $A=0,B=0,C=1\ (D\ \text{变})$ | $A+B+\bar C$ |
> | ② | $0001,1001$ | $B=0,C=0,D=1\ (A\ \text{变})$ | $B+C+\bar D$ |
> | ③ | $0100,1100$ | $B=1,C=0,D=0\ (A\ \text{变})$ | $\bar B+C+D$ |
>
> $$
> \boxed{F_{\min\text{-POS}}=(A+B+\bar C)(B+C+\bar D)(\bar B+C+D)}
> $$
>
> **（2）同一张图圈 1（求最小 SOP）**：$B=D=1$ 的四格、$B=C=1$ 的四格、$A=C=1$ 的四格，以及 $B=C=D=0$ 的一对（B=1的整片区域含指定0，不能圈成八格）
>
> $$
> F_{\min\text{-SOP}}=\bar B\bar C\bar D+BD+BC+AC
> $$
>
> **数值校验 (Numerical check)**：把两个式子各自代回**全部 16 行**——
> 6 个 0 行全得 0 ✓、10 个 1 行全得 1 ✓，且两式逐行完全一致 ✓
> （逐行穷举检查）。**同一个函数、两种形式，圈法不同而已。**
>
> ![[kmap-pos-minimization.svg]]
> *图 1 — 同一张卡诺图的两种读法：(a) 圈 **0** → 每个圈读成一个和项（单格且含全域时为maxterm），三个和项相乘得最小 POS；
> (b) 圈 **1** → 每个圈读成一个积项，四项相或得最小 SOP。*
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.56：同一张图同时给出最小 POS 与最小 SOP**
>
> 题目：把标准 POS $\prod M(1,2,3,4,9,12)$ 化成 (a) 最小 POS、(b) 标准 SOP、(c) 最小 SOP。
> 解：
>
> - (a) 圈 0 得 $F=(A+B+\bar C)(B+C+\bar D)(\bar B+C+D)$；
> - (b) 标准 SOP = 把 10 个 1 行全部写成 minterm 再 OR：
>   $\sum m(0,5,6,7,8,10,11,13,14,15)$（每一项含全部四个变量）；
> - (c) 圈 1 得 $F=\bar B\bar C\bar D+BD+BC+AC$。
>
> **数值校验**：三个式子逐行代入完全一致 ✓；项数 (a) 3 项 / (c) 4 项，都远少于标准 SOP 的 10 项 ✓。
>
> ![[ch4-kmap-pos-to-sop.png]]
> *图 2 — 讲义 p.56 原图：练习题给出的六个 maxterm、先填 0 再填 1、然后分别读出最小 POS 与最小 SOP。*
>
> **Example 2 — 三变量 POS：圈 0 与圈 1 得到同一函数的两种形式**
>
> **关于讲义 p.55 的例题 4-34 / 4-35**
> 讲义这两题的和项在下标与横线在文本抽取中残缺（`========== PAGE 55 ==========` 只剩
> "000 001 010 011 110" 与 "X000 0010 1001 0100 1100" 两组编号），因此本篇给出一个**完全自洽、
> 可逐行验证**的三变量例题；讲义原图见下方图 3。
>
> 题目：$F=\prod M(0,1,2,4)$，即 $F$ 在 $m_0,m_1,m_2,m_4$ 四行为 0，其余（$m_3,m_5,m_6,m_7$）为 1。
> 解：填 2×4 卡诺图（行 $A$，列 $BC$ 按 `00 01 11 10`）：
>
> | $A\backslash BC$ | 00 | 01 | 11 | 10 |
> |---|---|---|---|---|
> | **0** | **0**($m_0$) | **0**($m_1$) | 1($m_3$) | **0**($m_2$) |
> | **1** | **0**($m_4$) | 1($m_5$) | 1($m_7$) | 1($m_6$) |
>
> **圈 0**：$\{m_0,m_1\}$ 相邻 → 读 $A+B$；$\{m_0,m_2\}$ 靠**列回绕**相邻 → 读 $A+C$；
> $\{m_0,m_4\}$ 上下相邻 → 读 $B+C$：
>
> $$
> F_{\min\text{-POS}}=(A+B)(A+C)(B+C)
> $$
>
> **圈 1**（同一张图）：$\{m_3,m_7\}=BC$、$\{m_5,m_7\}=AC$、$\{m_6,m_7\}=AB$：
>
> $$
> F_{\min\text{-SOP}}=AB+AC+BC
> $$
>
> **数值校验**：两式在 8 行上逐行一致——0 行 $m_0,m_1,m_2,m_4$ 全为 0 ✓、1 行全为 1 ✓；
> $AB+AC+BC$ 正是"三输入多数表决"，与 [[Boolean Algebra and Circuit Models#2 · Boolean Equation · 从需求写函数|Boolean Equation]] 里全加器的进位式 $C_{out}=AB+AC_{in}+BC_{in}$ 同形 ✓。
>
> ![[ch4-kmap-pos-example.png]]
> *图 3 — 讲义 p.55 原图：例题 4-34/4-35 的 POS 卡诺图（圈 0 读 maxterm）。*
>
> **Read zero groups as sum terms · 零圈怎样读和项**
>
> Group zeros rather than ones. A variable that stays zero in a zero group appears uncomplemented in the corresponding sum term; a variable that stays one appears complemented. This makes the entire sum zero precisely on the grouped rows. Variables that change disappear.
>
> The resulting POS is the product of those sum terms. You may also minimize the complement as an SOP and apply DeMorgan's law, but clearly distinguish F from NOT F at every step. Forgetting the final complement swaps the ON and OFF sets.
>
> **Worked application.** ABC域中，F仅在A=0,B=1时为0，C无关。OFF set为2,3；对应和项 $A+\bar B$。代入010/011得0，代入000得1，代入110得1。若误写 $\bar A+B$，就在原来的零组上得1。
>
> **English exam question:** Are minimum SOP and minimum POS necessarily implemented at the same cost?
>
> **Answer:** No. Their terms, literals, and required complements can differ, as can the available gate family. Compare both forms under the actual constraints. [[Universal Gates and Bubble Pushing]] maps POS into NOR networks; [[Propagation Delay and Logic Hazards]] adds the separate timing assessment.

## 4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务

X 可视为 0 或 1，选择能扩大有用组的取值；无需覆盖全部 X。BCD 非法输入能否标 X，要由无效输入处理规范决定。优先电路输入端的 X 只是压缩真值表，不等于未指定输出。

### 三类格的义务与X的来源 (don't-care specification)

无关条件 (don't-care condition) 是规范允许该输入行输出0或1，记X；它不是硬件的第三逻辑输出。两类来源为：系统保证不会出现的输入组合，或该组合下此输出不被使用/没有要求。BCD的1010–1111是非法数字码，但只有系统排除这些输入或输出规范真的无要求时，才能设X；错误、上电或传输过程是否会触发非法码，需要结合完整系统判断。

| 格 | SOP圈1 | POS圈0 |
|---|---|---|
| 指定1 | 必须覆盖 | 禁止纳入 |
| 指定0 | 禁止纳入 | 必须覆盖 |
| X | 可作1扩大有用组，也可不用 | 可作0扩大有用组，也可不用 |

X不改变几何规则。不要新增只覆盖X的冗余组，不要求覆盖全部X，也不要求所有X取同一值；不同组共享X时可以同时覆盖，最终式在每个X行仍只有一个确定稳态值。

### 利用X与回读结果 (method and pitfalls)

先填好ON/OFF/DC全集，可先把X固定为0作SOP基准（POS基准固定为1），再把有帮助的X纳入更大组，比较整个覆盖的项数与文字数，最后回读全部指定行以及所选实现的X行。基准不是必须先做一次完整最小化，目的只是展示X提供的收益。

利用X可能只减少文字数、也可能减少项数，不能承诺一定“两者都变少”。圈了某个X后最终输出由所选方程固定，不能运行时随机选择。若回读发现某个X行需要报警、全灭或状态恢复，该行其实有要求，应把它改为0/1再重新最小化；不要在化简后继续称其任意。

分开做SOP和POS时可以选择不同X完成方式，各自在指定行满足同一不完全规范；这不保证两式在X行也相等。BCD完整显示接口见 [[Seven-Segment Display and Code Conversion]]，状态恢复见 [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|未用状态]]；表格中输入X的压缩记号与输出don't-care定义须分开。

> [!example]- Karnaugh Map with Don't Cares · 推导与例题
> **图示与讲义依据**
>
> ![[ch4-kmap-dont-care.png]]
> *图 1 — 讲义 p.59 原图：一张含 7 个 X 的四变量卡诺图（行 `CD`、列 `AB`，按 Gray 码 `00 01 11 10` 排列）。*
>
> **Derivation · 推导过程**
>
> 以讲义 p.59 的图为例（7 个 1、2 个 0、7 个 X）：
>
> | $A B C D$ | $Y$ | $A B C D$ | $Y$ |
> |---|---|---|---|
> | 0000 | 1 | 1000 | 1 |
> | 0001 | 0 | 1001 | 1 |
> | 0010 | 1 | 1010 | X |
> | 0011 | 1 | 1011 | X |
> | 0100 | 0 | 1100 | X |
> | 0101 | X | 1101 | X |
> | 0110 | 1 | 1110 | X |
> | 0111 | 1 | 1111 | X |
>
> **第一步：先只圈 1，看能圈多大。** 1 的分布是"左下角一堆 + 顶行两个"，天生零散：
>
> $$
> Y_{X=0}=\bar AC+A\bar B\bar C+\bar A\bar B\bar D
> $$
>
> **第二步：把 X 当 1，圈出三个大圈。**（图 2 已把三个圈画出来）
>
> | 圈 | 覆盖的格 | 圈内不变的变量 | 读出的积项 |
> |---|---|---|---|
> | ① | $A=1$ 的全部 8 格（含 6 个 X） | $A=1$ | $A$ |
> | ② | $C=1$ 的全部 8 格（含 4 个 X） | $C=1$ | $C$ |
> | ③ | 四个角 $0000,0010,1000,1010$（含 1 个 X，**靠回绕**） | $B=0,\ D=0$ | $\bar B\bar D$ |
>
> $$
> Y=A+C+\bar B\bar D
> $$
>
> - 物理意义：三个圈分别锁住"$A$ 为真""$C$ 为真""$B,D$ 同时为假"三种情况，任一成立输出就是 1；
> - **数值校验**：把 $Y=A+C+\bar B\bar D$ 代回全部 16 行——7 个 1 行全得 1 ✓、2 个 0 行
>   （$0001$：$A=0,C=0,\bar B\bar D=1\cdot0=0\Rightarrow 0$ ✓；$0100$：$A=0,C=0,\bar B\bar D=0\cdot1=0\Rightarrow 0$ ✓）；
>   按索引5,10,11,12,13,14,15排列的7个X行取 $0,1,1,1,1,1,1$，都是允许值 ✓。
> - 对比：上述把X固定为0的方案为3项、8个文字；利用X后 **3项、4个文字**。
>   本例减少的是literal count，不是乘积项个数；不同X行无需都取相同值。
>
> ![[kmap-dont-care.svg]]
> *图 2 — 同一张图的两种画法：(a) 按讲义给出 1/0/X 与每格的 minterm 编号；(b) 三个圈——其中两个"吞掉"X 格，
> 第三个 $\bar B\bar D$ 靠**回绕**把四个角圈在一起，最终读出 $Y=A+C+\bar B\bar D$。*
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.59：用 X 把零散的 1 合并成大圈**
>
> 题目见上面的真值表。解：按图 2 的三个圈得 $Y=A+C+\bar B\bar D$。
> **数值校验 (Numerical check)**：16行逐行代入——7个1行全为1 ✓；2个0行全为0 ✓；
> 7个X行的输出为0,1,1,1,1,1,1（允许）✓。上述基准3项8文字变为3项4文字 ✓。
>
> **Example 2 — 讲义 p.60–61（例题 4-32）：BCD → 七段译码器的段 a**
>
> 七段数码管的 **a 段**（顶横）在显示 $0,2,3,5,6,7,8,9$ 时点亮，在 $1,4$ 时熄灭；
> BCD 的 $1010$–$1111$ **不是合法数字**，因此输出为 X：
>
> | 数字 | $A B C D$ | 段 a | 数字 | $A B C D$ | 段 a |
> |---|---|---|---|---|---|
> | 0 | 0000 | 1 | 5 | 0101 | 1 |
> | 1 | 0001 | 0 | 6 | 0110 | 1 |
> | 2 | 0010 | 1 | 7 | 0111 | 1 |
> | 3 | 0011 | 1 | 8 | 1000 | 1 |
> | 4 | 0100 | 0 | 9 | 1001 | 1 |
> | — | 1010–1111 | X | | | |
>
> 解：圈 $A=1$ 的 8 格（含 6 个 X）、圈 $C=1$ 的 8 格、圈 $B=D=1$ 的 4 格、圈 $B=D=0$ 的 4 格：
>
> $$
> a=A+C+BD+\bar B\bar D
> $$
>
> **数值校验**：逐行代入——8 个"亮"的行全为 1 ✓，$0001$（数字 1）得 $0+0+0+0=0$ ✓，
> $0100$（数字 4）得 $0+0+0+0=0$ ✓，$1010$–$1111$ 得 1（X，允许）✓；
> 最后一式可读作 $a=A+C+(B\odot D)$：**"最高位为 1，或次高位为 1，或 B 与 D 相同"**——
> 这正好解释了 2/3/6/7 连续点亮、8/9 靠 $A$ 点亮的原因 ✓。
>
> ![[ch4-seven-segment-kmap.png]]
> *图 3 — 讲义 p.61 原图：例题 4-32 的 BCD→七段译码器真值表与段 a 的卡诺图（$1010$–$1111$ 全为 X）。*
>
> **Example 3 — 反例：什么时候不能把 X 当 1**
>
> 若某组合其实**会出现**且要求输出 0（例如译码器要驱动一个报警灯），却被图省事标成 X，
> 化简后式子在该行可能取 1 → 报警灯误亮。
> **校验方法**：把圈出来的式子代回该行；一旦取值与真实要求不符，说明 X 标错了，必须改回 0。
>
> **Don't-care freedom and invalid-input policy · 自由度与非法输入策略**
>
> A don't-care states that the specification accepts either Boolean output on that input row. The implemented circuit still produces one definite steady-state result there. It does not physically output the symbol X or choose a value afresh during each use.
>
> For BCD inputs, treating ten through fifteen as don't-cares is valid only when those codes are excluded or their outputs are unconstrained. If invalid codes must blank a display or raise an alarm, add that requirement to the table before minimizing. A state encoding also needs a deliberate recovery policy if invalid states can occur.
>
> **Worked application.** 段a最简式在非法BCD输入1010上输出1，这在don't-care规范中允许；如果现在要求非法码全灭，则检测 $I_{bad}=A(B+C)$ 并令 $a_{safe}=\bar I_{bad}a$。在1010时Ibad=1，所以强制灭；原来的化简结果并没有“自动失效保护”。
>
> **English exam question:** Must every don't-care cell be used in the final groups?
>
> **Answer:** No. Use only those that improve a cover of required cells; a group covering only don't-cares creates no useful obligation. Check [[Seven-Segment Display and Code Conversion]] for the complete interface and [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]] for recovery behavior.

## 5 · 从分组到证明：两个边界例

四变量函数 $F=\sum m(0,1,8,9,12)$，四格跨边组给 $\bar B\bar C$，两格组给 $A\bar C\bar D$，二者在 $m_8$ 重叠。结果 $F=\bar B\bar C+A\bar C\bar D$。

恰好三个输入为 1 的 $\{7,11,13,14\}$ 互不相邻，没有无关项时只能保留四个四文字最小项；不能用 XOR 替代，因为 XOR 还包含恰好一个 1。

> [!IMPORTANT] 最终检查
> 写出变量顺序、各组覆盖、消去变量和最终方程；穷举指定行验证。最小稳态方程仍可能存在逻辑冒险，见 [[Propagation Delay and Logic Hazards]]。

## Sources · 课件依据

主线课件：[Ch4 lecture](../ECE2050-Chap4.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
