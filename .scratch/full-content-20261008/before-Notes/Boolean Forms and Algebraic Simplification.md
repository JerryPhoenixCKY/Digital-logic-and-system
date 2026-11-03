---
tags:
  - ECE2050
  - boolean-algebra
  - boolean-forms
date: 2026-09-16
updated: 2026-10-08
chapter: Ch4
aliases:
  - 布尔表达形式与代数化简
  - Boolean Forms and Algebraic Simplification
  - 布尔表达形式与代数化简 · Ch4
  - Minterm and Maxterm
  - 最小项与最大项
  - 最小项
  - 最大项
  - Minterm
  - Maxterm
  - Truth Table and Boolean Expression
  - 真值表与布尔表达式
  - 真值表转表达式
  - Truth Table to Expression
  - Sum-of-Products Form
  - 与或式
  - 积之和形式
  - Sum-of-Products
  - SOP Form
  - SOP
  - Product-of-Sums Form
  - 或与式
  - 和之积形式
  - Product-of-Sums
  - POS Form
  - POS
  - Boolean Expression Simplification
  - 布尔代数化简
  - 逻辑表达式化简
  - Logic Simplification
---

# Boolean Forms and Algebraic Simplification · 布尔表达形式与代数化简

> [!SUMMARY] Quick recall · 英文速览
> Canonical forms record truth-table rows exactly. Simplification removes unnecessary literals while preserving every specified output.

## 1 · Minterm and Maxterm · 一行对应一个项

固定变量顺序 $ABC$，行编号 $i=4A+2B+C$。最小项 (minterm) $m_i$ 仅在第 i 行为 1：取 1 的变量原写，取 0 的变量取补。最大项 (maxterm) $M_i=\bar m_i$ 仅在第 i 行为 0，文字极性相反。

例如 i=2 对应 010：$m_2=\bar AB\bar C$，$M_2=A+\bar B+C$。两种项都包含变量域中的每个变量。

> [!example]- Minterm and Maxterm · 推导与例题
> **图示与讲义依据**
>
> ![[minterm-maxterm-table.svg]]
> *图 1 — (a) 3 变量、(b) 2 变量的 minterm / maxterm 对照表。阴影行 $i$ 同时是 $m_i$ **唯一取 1** 的行
> 和 $M_i$ **唯一取 0** 的行（最右两列），所以 $M_i=\bar m_i$：把 $m_i$ 取反（De Morgan 拆横线、
> 乘号变加号）就得到 $M_i$。*
>
> **Derivation · 推导过程**
>
> **1. 为什么 minterm 只能在一行为 1**
>
> $n$ 个 literal 全部相乘，要结果为 1，必须**每一个** literal 都为 1 ——
> 而每个 literal 正好规定了一个变量的取值（原变量要求 1、反变量要求 0）。
> $n$ 个变量、每个都被规定死，于是只有唯一一种输入组合能满足 → 只有 1 行为 1。
>
> - 意义：minterm 是"行号的选择器"（row selector）：$m_i$ 就是"当前输入等于第 $i$ 行"这个事件的布尔表达式。
> - 数值校验：$m_5=A\bar BC$，枚举 8 行得 $0,0,0,0,0,1,0,0$ —— 只有第 5 行是 1 ✓。
>
> **2. 为什么 maxterm 只能在一行为 0（以及 $M_i=\bar m_i$）**
>
> maxterm 是**和**：要结果为 0，必须每一项都为 0，也就是每个变量都被"反向"规定死 → 同样唯一。
> 把两者的关系写成公式：
>
> $$
> M_i = \overline{m_i}
> $$
>
> - 意义：$M_i$ 就是 $m_i$ 的反函数。因为 $m_i$ 只在一行为 1，所以 $\overline{m_i}$ 只在一行为 0 —— 这正是 maxterm。
> - 推导（用 [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式|DeMorgan's Theorems]]）：以 $i=2$ 为例，$m_2=\bar AB\bar C$，取反后拆横线（乘变加、各自取反）：
>
> $$
> \overline{m_2}=\overline{\bar A\cdot B\cdot\bar C}=\bar{\bar A}+\bar B+\bar{\bar C}=A+\bar B+C=M_2
> $$
>
> - 数值校验：枚举 8 行，$m_2 = 0,0,1,0,0,0,0,0$，$M_2 = 1,1,0,1,1,1,1,1$ ——
>   两列逐位相反 ✓；且 $m_2$ 唯一取 1 的行是第 2 行、$M_2$ 唯一取 0 的行也是第 2 行 ✓。
> - 顺带得到两个计数事实：$\sum_i m_i = 1$（所有 minterm 之和恒为 1，因为每一行恰好有一个 minterm 为 1）、
>   $\prod_i M_i = 0$（所有 maxterm 之积恒为 0）。
>
> **3. 2 变量的表（讲义 p.36–37 直接用到的两个表）**
>
> | $i$ | $A$ $B$ | minterm $m_i$ | maxterm $M_i$ | $m_i$ 在行 $i$ | $M_i$ 在行 $i$ |
> |---|---|---|---|---|---|
> | 0 | 0 0 | $\bar A\bar B$ | $A+B$ | 1 | 0 |
> | 1 | 0 1 | $\bar AB$ | $A+\bar B$ | 1 | 0 |
> | 2 | 1 0 | $A\bar B$ | $\bar A+B$ | 1 | 0 |
> | 3 | 1 1 | $AB$ | $\bar A+\bar B$ | 1 | 0 |
>
> - 讲义 p.36 的表：$Y=F(A,B)=\bar AB+AB$ 只在 $m_1,m_3$ 两行取 1 → 写作 $Y=\sum m(1,3)$；
> - 讲义 p.37 的表：同一个函数用 maxterm 写，取 0 的两行是 $M_0=A+B$ 与 $M_2=\bar A+B$
>   → $Y=\prod M(0,2)$。两种写法枚举 4 行都得 $0,1,0,1$ ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 从一行写出 minterm 与 maxterm（4 变量）**
>
> 题目：某 4 变量函数的 domain 是 $\{A,B,C,D\}$。对于输入 $A=1,B=0,C=1,D=1$：
> (a) 写出它的 minterm 与编号；(b) 写出它的 maxterm 与编号。
>
> 解：
> 1. 行值写成二进制 `1011` $= 8+0+2+1 = 11$ → $i=11$。
> 2. minterm：取 1 的写原变量、取 0 的写反变量 → $m_{11}=A\bar BCD$。
> 3. maxterm：取 0 的写原变量、取 1 的写反变量 → $M_{11}=\bar A+B+\bar C+\bar D$。
>
> **数值校验 (Numerical check)**：代入 $(1,0,1,1)$：
> $m_{11}=1\cdot\bar 0\cdot1\cdot1=1\cdot1\cdot1\cdot1=1$ ✓；
> $M_{11}=\bar 1+0+\bar 1+\bar 1=0+0+0+0=0$ ✓。
> 再代入 $(0,1,0,0)$（`0100` $=4$）：$m_{11}=0\cdot1\cdot0\cdot0=0$ ✓，$M_{11}=1+1+1+1=1$ ✓。
> 枚举全部 16 行：$m_{11}$ 只在第 11 行为 1、$M_{11}$ 只在第 11 行为 0 ✓。
>
> **Example 2 — 术语辨认（讲义 p.35 的分类练习）**
>
> 题目：domain 为 $\{A,B,C\}$。判断下列各项分别是 literal、implicant、minterm 还是 maxterm：
> (a) $\bar A$；(b) $B\bar C$；(c) $A\bar BC$；(d) $(A+\bar B+C)$；(e) $(A+\bar B)$。
>
> 解：
> 1. (a) $\bar A$ 是**补变量**，也是一个 **literal**（literal = 变量或其补）。
> 2. (b) $B\bar C$ 是 literal 的乘积 → **implicant**；只有 2 个 literal、缺 $A$ → 不是 minterm。
> 3. (c) $A\bar BC$ 含全部 3 个变量 → **minterm**，行值是 `101` $=5$，即 $m_5$。
> 4. (d) 含全部 3 个变量的和 → **maxterm**；它是"取 0 写原变量"，对应行 `010` → $M_2=A+\bar B+C$。
> 5. (e) $(A+\bar B)$ 是和、但缺 $C$ → 只是"和项"，**不是** maxterm（它在 2 行为 0）。
>
> **数值校验 (Numerical check)**：(e) 在 $(A,B,C)=(0,1,0)$ 与 $(0,1,1)$ 两行都等于 0
> （$0+\bar 1=0$）→ 有两行为 0，违反"maxterm 只在一行为 0" ✓ 判定正确。
> (c) 在 8 行上为 $0,0,0,0,0,1,0,0$，只在第 5 行为 1 ✓。
>
> **Example 3 — 验证 $M_5=\overline{m_5}$**
>
> 题目：用 De Morgan 证明 $M_5=\overline{m_5}$，并用真值表核对。
>
> 解：
> 1. 行 `101` 的 minterm 是 $m_5=A\bar BC$，maxterm 是 $M_5=\bar A+B+\bar C$。
> 2. 取反并拆横线：$\overline{m_5}=\overline{A\bar BC}=\bar A+\bar B+\bar C$ ✗ ——
>    注意这一步**没有**直接得到 $M_5$，需要小心反变量的反：
>
> $$
> \overline{A\bar BC}=\bar A+\overline{\bar B}+\bar C=\bar A+B+\bar C=M_5
> $$
>
> **数值校验 (Numerical check)**：枚举 8 行，
> $m_5=0,0,0,0,0,1,0,0$，$M_5=1,1,1,1,1,0,1,1$，两者**逐位相反** ✓；
> $M_5$ 唯一取 0 的行是第 5 行，与 $m_5$ 唯一取 1 的行一致 ✓。
>
> **Row identities and polarity · 行编号与取补方向**
>
> A minterm is true on exactly one row; a maxterm is false on exactly one row. Their subscripts refer to the same input pattern, not to whether the overall function is one or zero there. For the same variable order, maxterm M_i is the complement of minterm m_i.
>
> In a minterm, a row bit zero requires a complemented literal. In a maxterm, a row bit zero requires an uncomplemented literal so that this sum evaluates to zero on the selected row. The reversed rule follows directly from the desired output at that row.
>
> **Worked application.** 变量顺序 ABC，索引5是101：$m_5=A\bar BC$；$M_5=\bar A+B+\bar C$。在101时前者1、后者0。在100时 m5=0，M5因 $\bar C=1$ 得1。补关系逐行成立。
>
> **English exam question:** Why is a decoder useful for generating a canonical SOP?
>
> **Answer:** An enabled active-high binary decoder generates one minterm per output line. OR the lines corresponding to the function's ON set. With active-low outputs, combine the complemented minterms using the appropriate NAND form. Continue to [[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] and [[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积|Read-Only Memory and Programmable Logic Arrays]].

## 2 · Truth Table and Boolean Expression · 用真值表定义全集

n 个变量有 $2^n$ 行。输出为 1 的 ON set、为 0 的 OFF set 和允许任意输出的 don't-care set 需分别列出；只有规范允许时才能把某行标 X。

> [!example]- Truth Table and Boolean Expression · 推导与例题
> **Derivation · 推导过程**
>
> **1. 标准 SOP → 真值表（讲义 p.43）**
>
> $$
> Y=\sum m(i_1,i_2,\dots)\ \Longrightarrow\ Y(j)=1 \iff j\in\{i_1,i_2,\dots\}
> $$
>
> - 意义：minterm 是"行号选择器"，所以把 $2^n$ 行写全后，只需给列出的那几个行号打 1。
> - 数值校验（讲义 p.43 的例子）：$Y=\bar A\bar BC+A\bar B\bar C+ABC$（即 $\sum m(1,4,7)$），
>   8 行输出 $=0,1,0,0,1,0,0,1$ —— 恰好在 1、4、7 三行为 1 ✓。
>
> **2. 标准 POS → 真值表（讲义 p.44）**
>
> $$
> Y=\prod M(i_1,i_2,\dots)\ \Longrightarrow\ Y(j)=0 \iff j\in\{i_1,i_2,\dots\}
> $$
>
> - 意义：maxterm 是"行号消除器"——它在自己那一行为 0。所以 AND 起来后，这些行必为 0，其余行必为 1。
> - 数值校验（讲义 p.44 的例子）：$Y=\prod M(0,2,3,5,6)$，8 行输出 $=0,1,0,0,1,0,0,1$ ✓。
>   注意它与第 1 条**完全相同** —— 讲义 p.43 与 p.44 讲的就是同一个函数的两种写法 ✓。
>
> **3. 真值表 → 最小 SOP / 最小 POS（讲义 p.45–46 的 $X$ 例）**
>
> 先把真值表读成标准式（第 1、2 条），再用 [[Boolean Forms and Algebraic Simplification 1#4 · Boolean Expression Simplification · 保持函数再比较代价|Boolean Expression Simplification]] 化简：
>
> $$
> X=\bar ABC+A\bar B\bar C+AB\bar C+ABC
> =(\bar ABC+ABC)+(A\bar B\bar C+AB\bar C)
> =BC+A\bar C
> $$
>
> - 第一步：把 4 个 1 行两两配对，每对只差一个变量的正反；
> - 第二步：$BC(A+\bar A)=BC$，$A\bar C(\bar B+B)=A\bar C$ —— Rule 7 + Rule 2。
>
> POS 侧同理（把 0 行配对）：
>
> $$
> X=(A+B+C)(A+B+\bar C)(A+\bar B+C)(\bar A+B+\bar C)
> =\underbrace{(A+B+C)(A+\bar B+C)}_{A+C}\cdot\underbrace{(A+B+\bar C)(\bar A+B+\bar C)}_{B+\bar C}
> =(A+C)(B+\bar C)
> $$
>
> - 意义：两个只差一个变量的 maxterm 相乘，那个变量被消掉（Rule 12 的逆用：$(X+Y)(X+\bar Y)=X$）。
> - 数值校验：枚举 8 行，$BC+A\bar C = 0,0,0,1,1,0,1,1$ ✓；
>   $(A+C)(B+\bar C)=0,0,0,1,1,0,1,1$ ✓ —— 与真值表**逐行一致**，两者也互为等价形式 ✓。
> - 最小性核对（穷举所有单个乘积项 / 单个和项）：没有任何**一项**能同时覆盖 4 个 1 行而不多带 0 行，
>   也没有任何一个和项能同时覆盖 4 个 0 行而不多带 1 行 → 两项（SOP）与两项（POS）都已是最少 ✓。
>
> ![[truth-table-conversion.svg]]
> *图 1 — 标准 SOP / 真值表 / 标准 POS 的三向互转，用讲义 p.45–46 的 $X$ 例走完一圈：
> $X=\sum m(3,4,6,7)$（左）与 $X=\prod M(0,1,2,5)$（右）描述同一个函数；中间是真值表，
> 阴影行是输出为 1 的行（SOP 的来源），未阴影行是输出为 0 的行（POS 的来源），
> 两个编号集合互补。*
>
> **Worked Example · 例题**
>
> **Example 1 — 由标准 SOP 填真值表（讲义 p.43）**
>
> 题目：domain 为 $\{A,B,C\}$，$Y=\bar A\bar BC+A\bar B\bar C+ABC$。填真值表，并按讲义的写法标出 Don't Care。
>
> 解：三项分别是 $m_1,m_4,m_7$。每一行里只有"属于本行"的那一项为 1，另外两项为 0（标 Don't Care）：
>
> | $A$ | $B$ | $C$ | $\bar A\bar BC$ | $A\bar B\bar C$ | $ABC$ | 输出 $Y$ |
> |---|---|---|---|---|---|---|
> | 0 | 0 | 0 | Don't Care | Don't Care | Don't Care | 0 |
> | 0 | 0 | 1 | **1** | Don't Care | Don't Care | 1 |
> | 0 | 1 | 0 | Don't Care | Don't Care | Don't Care | 0 |
> | 0 | 1 | 1 | Don't Care | Don't Care | Don't Care | 0 |
> | 1 | 0 | 0 | Don't Care | **1** | Don't Care | 1 |
> | 1 | 0 | 1 | Don't Care | Don't Care | Don't Care | 0 |
> | 1 | 1 | 0 | Don't Care | Don't Care | Don't Care | 0 |
> | 1 | 1 | 1 | Don't Care | Don't Care | **1** | 1 |
>
> **数值校验 (Numerical check)**：逐行代入三项并把结果 OR：第 1 行 $0+0+1=1$ ✓、
> 第 4 行 $1+0+0=1$ ✓、第 7 行 $0+0+1=1$ ✓，其余行三项全 0 → 输出 0 ✓。
> 整表输出 $=0,1,0,0,1,0,0,1$，即 $Y=\sum m(1,4,7)$ ✓。
>
> **Example 2 — 由标准 POS 填真值表（讲义 p.44）**
>
> 题目：$Y=(A+B+C)(A+\bar B+C)(A+\bar B+\bar C)(\bar A+B+\bar C)(\bar A+\bar B+C)$。填真值表。
>
> 解：五个 maxterm 是 $M_0,M_2,M_3,M_5,M_6$，它们各自的行输出为 0，其余行为 1
> （不在列表里的 $M_1,M_4,M_7$ 在本行取 1，按讲义的写法标 Don't Care）：
>
> | $A$ | $B$ | $C$ | 本行的 maxterm 在列表里吗 | 五项在本行的值 | 输出 $Y$ |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 是（$M_0=A+B+C$） | $M_0=0$，其余为 1 | 0 |
> | 0 | 0 | 1 | 否（$M_1$ 未列出） | 全为 1（Don't Care） | 1 |
> | 0 | 1 | 0 | 是（$M_2=A+\bar B+C$） | $M_2=0$，其余为 1 | 0 |
> | 0 | 1 | 1 | 是（$M_3=A+\bar B+\bar C$） | $M_3=0$，其余为 1 | 0 |
> | 1 | 0 | 0 | 否（$M_4$ 未列出） | 全为 1（Don't Care） | 1 |
> | 1 | 0 | 1 | 是（$M_5=\bar A+B+\bar C$） | $M_5=0$，其余为 1 | 0 |
> | 1 | 1 | 0 | 是（$M_6=\bar A+\bar B+C$） | $M_6=0$，其余为 1 | 0 |
> | 1 | 1 | 1 | 否（$M_7$ 未列出） | 全为 1（Don't Care） | 1 |
>
> **数值校验 (Numerical check)**：任抽一行代回原式：
> 第 4 行 $(1,0,0)$：五个 maxterm 依次为 $M_0=A+B+C=1$、$M_2=A+\bar B+C=1$、$M_3=A+\bar B+\bar C=1$、
> $M_5=\bar A+B+\bar C=0+0+1=1$、$M_6=\bar A+\bar B+C=0+1+0=1$ → AND 得 1 ✓；
> 第 3 行 $(0,1,1)$：$M_3=A+\bar B+\bar C=0+0+0=0$ → AND 必为 0 ✓。
> 8 行输出 $=0,1,0,0,1,0,0,1$ —— 与 Example 1 **完全相同** ✓：
> p.43 与 p.44 是同一个函数的 SOP 与 POS（编号集合互补）。
>
> **Example 3 — 从真值表到最小 SOP 与最小 POS（讲义 p.45–46 的 $X$ 例）**
>
> 题目：$X=\bar ABC+A\bar B\bar C+AB\bar C+ABC$。写出真值表、$\sum m$ 形式、以及最小的 SOP 与 POS。
>
> 解：
> 1. 四项是 $m_3,m_4,m_6,m_7$ → $X=\sum m(3,4,6,7)$，真值表 $0,0,0,1,1,0,1,1$。
> 2. 0 行是 0、1、2、5 → POS 侧 $X=\prod M(0,1,2,5)=(A+B+C)(A+B+\bar C)(A+\bar B+C)(\bar A+B+\bar C)$。
> 3. 最小 SOP：$(\bar ABC+ABC)=BC$，$(A\bar B\bar C+AB\bar C)=A\bar C$ → $X=BC+A\bar C$。
> 4. 最小 POS：$(A+B+C)(A+\bar B+C)=A+C$，$(A+B+\bar C)(\bar A+B+\bar C)=B+\bar C$ → $X=(A+C)(B+\bar C)$。
>
> **数值校验 (Numerical check)**：枚举 8 行，四种写法
> （标准 SOP、标准 POS、$BC+A\bar C$、$(A+C)(B+\bar C)$）的输出都是 $0,0,0,1,1,0,1,1$ ✓。
> 再抽一行：第 4 行 $(1,0,0)$ —— 标准 SOP 由 $A\bar B\bar C$ 得 1 ✓；
> $BC+A\bar C = 0+1\cdot1 = 1$ ✓；$(A+C)(B+\bar C)=(1+0)(0+1)=1$ ✓。
> 最小性核对：没有任何单项能覆盖 4 个 1 行而不带入 0 行，所以 2 项已是最少 ✓。
>
> **A table as a verification contract · 真值表是验证契约**
>
> Use one declared variable order throughout the table, minterm list, Karnaugh map, decoder connections, and MUX select inputs. A truth table is not simply a presentation of a final expression; it is the independently stated contract used to judge every implementation.
>
> For multiple outputs, each output has its own ON set and OFF set. Outputs may share intermediate product terms in a physical implementation, but that sharing must preserve each column separately. A valid code indicator is often an additional output rather than an interpretation guessed from the data bits.
>
> **Worked application.** full adder 以ABC为输入，C表示carry-in。sum ON set为1,2,4,7；carry ON set为3,5,6,7。在111行，sum=1且carry=1，合成值 $1+2=3$；两列都为1并不冲突。
>
> **English exam question:** Why can a priority encoder's data table be insufficient by itself?
>
> **Answer:** Code zero may mean input zero is active or no input is active. A separate valid output distinguishes those cases when required by the interface. Read [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码|Encoder and Priority Encoder]] for that boundary and [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]] for multi-output arithmetic verification.

## 3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式

标准 SOP 取 ON 行的最小项相或；标准 POS 取 OFF 行的最大项相与：

$$F=\sum_{i\in ON}m_i=\prod_{i\in OFF}M_i.$$

简化 SOP／POS 不一定每项包含全部变量。SOP 对应 AND→OR，POS 对应 OR→AND；“标准”“最小”与“门级实现最优”不是同一个条件。

> [!example]- Sum-of-Products Form · 推导与例题
> **Derivation · 推导过程**
>
> **1. 从真值表到标准 SOP（逐行选择）**
>
> $$
> Y=\sum_{i:\,Y(i)=1} m_i
> $$
>
> - 意义：把真值表"输出为 1"的行号收集起来，直接写成 $\sum m(\cdot)$；再展开成 minterm 的 OR。
> - 数值校验（讲义 p.43 的例子）：某 3 变量函数在 `001`、`100`、`111` 三行为 1，
>   于是 $Y=\bar A\bar BC+A\bar B\bar C+ABC=\sum m(1,4,7)$。
>   枚举 8 行：$0,1,0,0,1,0,0,1$ —— 与"行 1、4、7 为 1"完全一致 ✓。
>
> **2. 把非标准 SOP 补成标准 SOP（讲义 p.40）**
>
> 缺变量的乘积项乘上 $(X+\bar X)=1$（Rule 7），再用分配律展开：
>
> $$
> A\bar BC + A\bar B\bar CD
> = A\bar BC(D+\bar D) + A\bar B\bar CD
> = A\bar BCD + A\bar BC\bar D + A\bar B\bar CD
> $$
>
> - 意义：domain 是 $\{A,B,C,D\}$ 时，$A\bar BC$ 只有 3 个 literal，缺 $D$；
>   乘 $(D+\bar D)$ 把"缺的那一位"补成两种取值，一项变两项。
> - 数值校验：枚举 16 行（$ABCD$ 从 `0000` 到 `1111`），左边与右边**逐行相同**：
>   $0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0$ —— **16 行完全一致** ✓。
>   展开后三项都含 $A,B,C,D$ 四个 literal ✓ 是标准 SOP。
>
> **3. 判断标准 SOP 的三步自查**
>
> 1. 写下 domain（例如 $\{A,B,C\}$），数出变量个数 $n$。
> 2. 每一项是不是**恰好 $n$ 个 literal**且每个变量出现一次？（$AB$ 不合格，$AB\bar C$ 合格）
> 3. 有没有 OR 混进乘积项内部？有就不是 SOP（先展开再用第 2 步查）。
>
> ![[sop-from-truth-table.svg]]
> *图 1 — 讲义 p.43 的例子：真值表里输出为 1 的三行（`001`、`100`、`111`）被高亮取出，
> 每行换成对应 minterm（1 写原变量、0 写反变量），再 OR 成
> $Y=\bar A\bar BC+A\bar B\bar C+ABC=\sum m(1,4,7)$。输出为 0 的行直接跳过。*
>
> **Worked Example · 例题**
>
> **Example 1 — 异或的 SOP（讲义 p.36 的两变量例子）**
>
> 题目：写出 $Y=A\oplus B$ 的真值表与标准 SOP。
>
> 解：
> 1. 真值表（不同为 1）：$(0,0)\to0$、$(0,1)\to1$、$(1,0)\to1$、$(1,1)\to0$。
> 2. 输出为 1 的行是行 1（`01`）与行 2（`10`）→ $m_1=\bar AB$，$m_2=A\bar B$。
> 3. 所以 $Y=\bar AB+A\bar B=\sum m(1,2)$，也可以写成 $Y=A\oplus B$（见 [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]]）。
>
> **数值校验 (Numerical check)**：枚举 4 行，$\bar AB+A\bar B=0,1,1,0$ ✓
> 与"不同为 1"一致；与讲义 p.36 的 $\sum m(1,3)$ 型写法对照，可见**编号直接就是真值表**。
>
> **Example 2 — 由真值表写标准 SOP（讲义 p.43，配图 1）**
>
> 题目：某函数 $Y(A,B,C)$ 在 `001`、`100`、`111` 三行为 1，其余为 0。写出它的标准 SOP。
>
> 解：
> 1. 行号：`001` $=m_1$、`100` $=m_4$、`111` $=m_7$。
> 2. $m_1=\bar A\bar BC$；$m_4=A\bar B\bar C$；$m_7=ABC$。
> 3. $Y=\bar A\bar BC+A\bar B\bar C+ABC=\sum m(1,4,7)$。
>
> **数值校验 (Numerical check)**：枚举 8 行得 $0,1,0,0,1,0,0,1$ ——
> 第 1、4、7 行为 1，其余为 0 ✓；三项的 literal 数都是 3 = domain 大小 ✓ 是标准 SOP。
> 再化简一步：$AB\bar C+ABC=AB$，得 $Y=\bar A\bar BC+A\bar B\bar C+AB$（已不是标准式）。
>
> **Example 3 — 补变量：把 3 变量项补成 4 变量标准 SOP（讲义 p.40）**
>
> 题目：domain 为 $\{A,B,C,D\}$，把 $Y=A\bar BC+A\bar B\bar CD$ 写成标准 SOP。
>
> 解：
> 1. $A\bar BC$ 缺 $D$：乘 $(D+\bar D)=1$ → $A\bar BC(D+\bar D)=A\bar BCD+A\bar BC\bar D$。
> 2. $A\bar B\bar CD$ 已含 4 个 literal，不动。
> 3. $Y=A\bar BCD+A\bar BC\bar D+A\bar B\bar CD$。
>
> **数值校验 (Numerical check)**：枚举 16 行（$ABCD$ 从 `0000` 到 `1111`），原式与结果**逐行相同**：
> 两边都只在 `1001`（$A=1,B=0,C=0,D=1$）以及 `1010`、`1011`（$A=1,B=0,C=1$，$D$ 任意）时为 1
> → 向量 $0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0$ ✓；展开式三项各含 4 个 literal ✓。
> 对应的编号写法：$Y=\sum m(9,10,11)$ —— 其中 $m_9$ 来自原来的 $A\bar B\bar CD$，
> $m_{10},m_{11}$ 由第一项补上 $(D+\bar D)$ 展开而来。
>
> **Example 4 — 午餐例子：SOP 与 POS 化简到同一个式子（讲义 p.39）**
>
> 题目（讲义 p.38–39）：去食堂吃午饭，"没吃"($E=0$) 当且仅当**不干净**($C=0$) 或**只有肉饼**($M=1$)。
> (a) 写真值表；(b) 写出 SOP 并化简；(c) 由 POS 化简，比较两者。
>
> 解：
> 1. 真值表（domain $\{C,M\}$）：
>
> | $C$ | $M$ | $E$ | 说明 |
> |---|---|---|---|
> | 0 | 0 | 0 | 不干净 → 不吃 |
> | 0 | 1 | 0 | 不干净 → 不吃 |
> | 1 | 0 | 1 | 干净且不是肉饼 → 吃 |
> | 1 | 1 | 0 | 只有肉饼 → 不吃 |
>
> 2. SOP：输出为 1 的行只有行 2（`10`）→ $E=m_2=C\bar M$，已经最简。
> 3. POS：输出为 0 的行是 0、1、3 → $E=(C+M)(C+\bar M)(\bar C+\bar M)$
>    （maxterm 的写法见 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Product-of-Sums Form]]），化简：
>
> $$
> (C+M)(C+\bar M)=C+M\bar M=C+0=C
> \quad\Longrightarrow\quad
> E=C(\bar C+\bar M)=C\bar C+C\bar M=0+C\bar M=C\bar M
> $$
>
> **数值校验 (Numerical check)**：枚举 4 行，SOP 的 $C\bar M=0,0,1,0$；
> POS 展开前的 $(C+M)(C+\bar M)(\bar C+\bar M)=0,0,1,0$ —— **4 行完全一致** ✓。
> 两种形式都化简到 $E=C\bar M$：**SOP 与 POS 描述同一个函数**，只是出发点不同（1 行 vs 0 行）。
>
> **Canonical SOP and hardware mapping · 标准与或式怎样落地**
>
> An SOP is an OR of product terms. A canonical SOP uses minterms containing every variable; a simplified SOP may omit variables within a term. Expanding a simplified term produces several minterms because the omitted variables can take either value.
>
> Do not confuse Boolean addition with counting the number of active products. If AB and AC are both true, AB+AC is still one. Overlapping coverage is allowed. In a NAND–NAND realization, first produce each complemented product and then NAND those values to recover the OR of the original products.
>
> **Worked application.** $Y=A\bar B$ 在变量域 ABC 内，C 可为0或1，所以 $Y=A\bar B(C+\bar C)=m_4+m_5$。若题目只有AB两个变量，标准式就是原来的 $A\bar B=m_2$，不能凭空引入C再沿用相同索引。
>
> **English exam question:** What changes when complementary inputs are unavailable?
>
> **Answer:** Every required complemented literal must be generated, usually adding an inverter or an equivalent tied-input NAND. The truth function remains the same, but the gate count and delay can change. Use [[Universal Gates and Bubble Pushing]] for implementation and [[Boolean Forms and Algebraic Simplification 1#2 · Truth Table and Boolean Expression · 用真值表定义全集|Truth Table and Boolean Expression]] to check the declared variable domain.

> [!example]- Product-of-Sums Form · 推导与例题
> **Derivation · 推导过程**
>
> **1. 从真值表到标准 POS（逐行选择）**
>
> $$
> Y=\prod_{i:\,Y(i)=0} M_i
> $$
>
> - 意义：把"输出为 0"的行号收集起来写成 $\prod M(\cdot)$，再展开成 maxterm 的 AND。
> - 为什么成立：每个 $M_i$ 只在第 $i$ 行为 0、其它行都为 1（见 [[Boolean Forms and Algebraic Simplification 1#1 · Minterm and Maxterm · 一行对应一个项|Minterm and Maxterm]]）。
>   把 0 行的 $M_i$ 全部 AND 起来：在任何 0 行，至少有一个因子是 0 → 整体为 0 ✓；
>   在任何 1 行，所有因子都是 1 → 整体为 1 ✓。
> - 数值校验（讲义 p.44 的例子）：某 3 变量函数在 `000`、`010`、`011`、`101`、`110` 五行为 0，
>   于是 $Y=(A+B+C)(A+\bar B+C)(A+\bar B+\bar C)(\bar A+B+\bar C)(\bar A+\bar B+C)=\prod M(0,2,3,5,6)$。
>   枚举 8 行得 $0,1,0,0,1,0,0,1$ —— 与"第 0、2、3、5、6 行为 0"完全一致 ✓。
>
> **2. 把非标准 POS 补成标准 POS（讲义 p.41，用 Rule 12）**
>
> 和项缺变量时，**加上** $X\bar X=0$（Rule 8），再用 Rule 12 $X+YZ=(X+Y)(X+Z)$ 拆成两个和项：
>
> $$
> A+\bar B+C
> = A+\bar B+C+D\bar D
> = (A+\bar B+C+D)(A+\bar B+C+\bar D)
> $$
>
> - 意义：domain 是 $\{A,B,C,D\}$ 时 $A+\bar B+C$ 缺 $D$；补上 $D\bar D=0$（OR 加 0 不改变结果）
>   再拆括号，一项变两项。
> - 数值校验：枚举 16 行（$ABCD$ 从 `0000` 到 `1111`），
>   左边在且仅在 `0100`、`0101` 两行为 0 → 向量 $1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1$；
>   右边两个和项之积同样是该向量 ✓ —— **16 行完全一致**。
> - 与 SOP 的补变量对比（对照 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]]）：SOP 是**乘** $(X+\bar X)=1$ 把项拆开，
>   POS 是**加** $X\bar X=0$ 再拆括号 —— 一个用 Rule 7，一个用 Rule 8 + Rule 12。
>
> **3. POS 与 SOP 的等价性（讲义 p.39 的午餐例子）**
>
> 讲义 p.39 用同一个真值表同时写出 SOP 与 POS，并把两边都化简到同一个式子：
>
> - SOP（取 1 行，只有行 `10`）：$E=C\bar M$；
> - POS（取 0 行，行 `00`、`01`、`11`）：$E=(C+M)(C+\bar M)(\bar C+\bar M)$，化简后也是 $C\bar M$。
>
> ![[pos-from-truth-table.svg]]
> *图 1 — 讲义 p.44 的例子：真值表里输出为 0 的五行为被高亮取出，每行换成一个 maxterm
> （**0 写原变量、1 写反变量**，与 minterm 相反），再 AND 成
> $Y=\prod M(0,2,3,5,6)$。这张图的真值表与 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 的图 1 是同一个函数：
> SOP 取 1 行得 $\sum m(1,4,7)$，POS 取 0 行得 $\prod M(0,2,3,5,6)$，两组编号正好互补。*
>
> **Worked Example · 例题**
>
> **Example 1 — 异或的 POS（与 SOP 对照）**
>
> 题目：写出 $Y=A\oplus B$ 的标准 POS。
>
> 解：
> 1. 真值表：$(0,0)\to0$、$(0,1)\to1$、$(1,0)\to1$、$(1,1)\to0$；0 行是行 0 与行 3。
> 2. $M_0=A+B$（0 写原变量）；$M_3=\bar A+\bar B$（1 写反变量）。
> 3. $Y=(A+B)(\bar A+\bar B)=\prod M(0,3)$。
>
> **数值校验 (Numerical check)**：枚举 4 行，$(A+B)(\bar A+\bar B)=0,1,1,0$ ✓
> 与 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 例题 1 的 $\sum m(1,2)$ **逐行一致** —— 两种形式同一个函数；
> 编号集合 $\{0,3\}$ 与 $\{1,2\}$ 互补 ✓。
>
> **Example 2 — 由真值表写标准 POS（讲义 p.44，配图 1）**
>
> 题目：某函数 $Y(A,B,C)$ 在 `000`、`010`、`011`、`101`、`110` 五行为 0，其余为 1。写出标准 POS。
>
> 解：
> 1. 行号：0、2、3、5、6。
> 2. 每个 0 行写 maxterm（0 → 原变量，1 → 反变量）：
>    $M_0=A+B+C$、$M_2=A+\bar B+C$、$M_3=A+\bar B+\bar C$、
>    $M_5=\bar A+B+\bar C$、$M_6=\bar A+\bar B+C$。
> 3. $Y=(A+B+C)(A+\bar B+C)(A+\bar B+\bar C)(\bar A+B+\bar C)(\bar A+\bar B+C)=\prod M(0,2,3,5,6)$。
>
> **数值校验 (Numerical check)**：枚举 8 行得 $0,1,0,0,1,0,0,1$ ——
> 第 0、2、3、5、6 行为 0 ✓；每个括号 3 个 literal = domain 大小 ✓ 是标准 POS。
> 顺带核对：把 $M_2=A+\bar B+C$ 在行 `010` 代入得 $0+0+0=0$ ✓（maxterm 在自己的行必须为 0）。
>
> **Example 3 — 补变量：把和项补成标准 POS（讲义 p.41 + p.42 的 Rule 12）**
>
> 题目：domain 为 $\{A,B,C,D\}$，把 $Y=(A+\bar B+C)(\bar A+B)$ 写成标准 POS。
>
> 解：
> 1. $A+\bar B+C$ 缺 $D$：加 $D\bar D=0$，再拆：
>    $(A+\bar B+C+D)(A+\bar B+C+\bar D)$。
> 2. $\bar A+B$ 缺 $C,D$：$\bar A+B+C\bar C+D\bar D$ 要分两次拆：
>    $(\bar A+B+C)(\bar A+B+\bar C)$ 再各自补 $D$ →
>    $(\bar A+B+C+D)(\bar A+B+C+\bar D)(\bar A+B+\bar C+D)(\bar A+B+\bar C+\bar D)$。
> 3. 合起来共 6 个和项，每项 4 个 literal —— 这就是标准 POS：
>    $Y=\prod M(4,5,8,9,10,11)$。
>
> **数值校验 (Numerical check)**：枚举 16 行（$ABCD$ 从 `0000` 到 `1111`），
> 原式 $=1,1,1,1,0,0,1,1,0,0,0,0,1,1,1,1$ —— 0 出现在
> `0100`、`0101`（第一个括号为 0：$A{=}0,B{=}1,C{=}0$）与
> `1000`～`1011`（第二个括号为 0：$A{=}1,B{=}0$）；展开后的 6 项之积是**同一条向量** ✓。
> 对照 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 的例题 3：SOP 补变量是"乘 $(X+\bar X)=1$ 拆一项"，
> POS 是"加 $X\bar X=0$ 后用 Rule 12 拆一项"，两者互为对偶。
>
> **Example 4 — 午餐例子：POS 化简后与 SOP 完全一致（讲义 p.39）**
>
> 题目（接 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 例题 4）：真值表 $C M \to E = 00{\to}0,\ 01{\to}0,\ 10{\to}1,\ 11{\to}0$。
> 用 POS 化简，并说明它与 SOP 的关系。
>
> 解：
> 1. 0 行是行 0、1、3 → $E=(C+M)(C+\bar M)(\bar C+\bar M)$。
> 2. 前两个括号用 Rule 12（$X+YZ=(X+Y)(X+Z)$ 的逆用）：$(C+M)(C+\bar M)=C+M\bar M$。
> 3. Rule 8：$M\bar M=0$；Rule 1：$C+0=C$。
> 4. 于是 $E=C(\bar C+\bar M)=C\bar C+C\bar M=0+C\bar M=C\bar M$。
>
> **数值校验 (Numerical check)**：枚举 4 行，
> $(C+M)(C+\bar M)(\bar C+\bar M)=0,0,1,0$ ✓；SOP 的 $C\bar M=0,0,1,0$ ✓ —— **两边逐行相同**，
> 都化简到 $E=C\bar M$，这就是讲义 p.39 上写的 "same"。
> 物理含义也对：$E=C\bar M$ = "干净 (clean) 且不是肉饼 (not meatloaf) 才吃" ✓。
>
> **Canonical POS from OFF rows · 从零行建立标准或与式**
>
> A POS is an AND of sum terms. A canonical POS includes one maxterm for each row where the function is zero. Each selected maxterm forces the product to zero on its own row; on an ON row, all those maxterms are one, so their product is one.
>
> The product does not include maxterms for ON rows. This reverses the selection rule used in canonical SOP, which collects ON minterms. SOP and POS can describe the same truth table even though they select opposite row sets.
>
> **Worked application.** ABC 域中 $F=\Sigma m(1,3,5,7)$，输出其实等于C。OFF set为0,2,4,6，故 $F=\Pi M(0,2,4,6)$。逐个最大项的形式较长，但最简POS只有一个和项C；canonical并不等于minimum。
>
> **English exam question:** Which universal-gate structure naturally implements POS?
>
> **Answer:** A NOR–NOR network produces the complements of the sum terms and then complements their OR, yielding the AND of the original sums. Literal inverters may still be required. Compare [[Karnaugh Map Minimization#3 · POS Minimization with Karnaugh Map · 圈 0 读和项|POS Minimization with Karnaugh Map]], [[Universal Gates and Bubble Pushing]], and [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] before choosing the lower-cost implementation.

## 4 · Boolean Expression Simplification · 保持函数再比较代价

典型动作是提公共因子、合并互补项和吸收冗余项：$XY+X\bar Y=X$，$X+\bar XY=X+Y$。为展开成标准 SOP，可乘 $(Z+\bar Z)=1$；标准 POS 可用 $P=(P+Z)(P+\bar Z)$ 补变量。

**例。** $AB+A\bar B=A$；而 $AB+\bar AC$ 不能随意删掉 A。每次改写先保证变量域与所有指定行不变。

> [!example]- Boolean Expression Simplification · 推导与例题
> **Derivation · 推导过程**
>
> **1. 化简的三个"动作"**
>
> 所有化简步骤，本质只有三个动作（讲义 p.31–33 的四个例子全部由它们组成）：
>
> | 动作 | 用到的规则 | 典型形态 | 一句话 |
> |---|---|---|---|
> | **合并 (combine)** | Rule 5 $A+A=A$、Rule 7 $A+\bar A=1$ | $A\bar B+AB=A(\bar B+B)=A$ | 两项只差一个变量的正反 → 该变量消去 |
> | **吸收 (absorb)** | Rule 10 $A+AB=A$、Rule 11 $A+\bar AB=A+B$ | $BC+BCD=BC(1+D)=BC$ | 一项"包含"另一项 → 短的那项赢 |
> | **展开/补项 (expand)** | 分配律、Rule 7、Rule 12 | $CD=CD(B+\bar B)$ | 缺变量时乘上 $(X+\bar X)=1$ 造出新项 |
>
> - 意义：看到式子先问"哪里只差一个变量的正反"（合并）、"哪一项是另一项的真子集"（吸收）、
>   "哪一项缺变量"（补项），三步之内基本能下手。
> - 数值校验（吸收）：$BC+BCD$ 在 8 行上的取值分别是 $0,0,0,0,0,0,1,1$（按 $BCD$ 从 `000` 到 `111`），
>   $BC$ 同样是 $0,0,0,0,0,0,1,1$ —— 完全一致 ✓，所以 $BC+BCD=BC$ 合法。
>
> ```mermaid
> flowchart TD
>     A[Boolean expression] --> B{Two terms differ in<br/>exactly one literal?}
>     B -- yes --> C["combine: A·B' + A·B = A"]
>     B -- no --> D{One term contains<br/>the other?}
>     D -- yes --> E["absorb: X + X·Y = X  (Rule 10)"]
>     D -- no --> F{Is a term missing<br/>a domain variable?}
>     F -- yes --> G["expand: X = X·(Y + Y') = X·Y + X·Y'"]
>     F -- no --> H{Still simplifiable?}
>     C --> H
>     E --> H
>     G --> H
>     H -- yes --> A
>     H -- no --> I[Check by enumerating all 2^n rows]
> ```
>
> **2. 为什么补一项不改变函数：$X=X\cdot 1=X(Y+\bar Y)$**
>
> $$
> X = X\cdot 1 = X(Y+\bar Y) = XY + X\bar Y
> $$
>
> - 意义：把一个乘积项**复制**成两项，是化简里唯一"越写越长"的动作，但它是后面合并/吸收的燃料。
>   讲义四个例子里有两个（Example 1、Example 4）都靠它。
> - 数值校验：$CD$ 在 $(B,C,D)=(0,1,1)$ 时 $=1$；$CD(B+\bar B)=1\cdot(0+1)=1$ ✓；
>   在 $(1,1,1)$ 时 $CD=1$，$CD(B+\bar B)=1\cdot(1+0)=1$ ✓ —— 两行都相等，其它行两边同为 0 ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.31 Example 1：复制一项造出两对**
>
> 题目：化简 $Y = A\bar BC + ABC + \bar ABC$。
>
> 解：
>
> | 步骤  | 表达式                                     | 用到的规则                                |
> | --- | --------------------------------------- | ------------------------------------ |
> | 1   | $Y = A\bar BC + ABC + \bar ABC$         | 原式                                   |
> | 2   | $= A\bar BC + ABC + ABC + \bar ABC$     | $X = X + X$（Rule 5 的反用，复制 $ABC$）     |
> | 3   | $= (A\bar BC + ABC) + (ABC + \bar ABC)$ | 结合律，分成两对                             |
> | 4   | $= AC(\bar B + B) + BC(A + \bar A)$     | 分配律（各提公因子）                           |
> | 5   | $= AC\cdot 1 + BC\cdot 1$               | Rule 7：$B+\bar B = 1$、$A+\bar A = 1$ |
> | 6   | $= AC + BC$                             | Rule 2：$X\cdot 1 = X$                |
>
> **数值校验 (Numerical check)**：按 $(A,B,C)$ 从 `000` 到 `111` 枚举 8 行：
> 原式 $= 0,0,0,1,0,1,0,1$；结果 $AC+BC = 0,0,0,1,0,1,0,1$ —— **8 行完全一致** ✓。
> 第 4 步的两对分别是：$A\bar BC+ABC$ 只在 $A=1,C=1$ 时为 1（$B$ 无关）→ $AC$；
> $ABC+\bar ABC$ 只在 $B=1,C=1$ 时为 1（$A$ 无关）→ $BC$ ✓。
>
> **Example 2 — 讲义 p.31 Example 2：提公因子后 Rule 7**
>
> 题目：化简 $Y = \bar AB + AB$。
>
> 解：
>
> $$
> Y = (\bar A + A)B = 1\cdot B = B
> $$
>
> - 第 1 步是分配律的反用（提公因子 $B$）：$\bar AB + AB = (\bar A + A)B$，
> - 第 2 步用 Rule 7（$A+\bar A = 1$），第 3 步用 Rule 2（$X\cdot 1 = X$）。
>
> **数值校验 (Numerical check)**：4 行 $(A,B) = (0,0),(0,1),(1,0),(1,1)$：
> 原式 $= 0,1,0,1$；$B = 0,1,0,1$ —— **4 行完全一致** ✓。
>
> **别把这一例记成 $A\bar B + \bar AB$**
> $A\bar B + \bar AB$ 是**异或**（XOR），它**不能**化简成 $B$：
> 枚举 4 行得 $0,1,1,0$，而 $B = 0,1,0,1$，第 3 行 $(1,0)$ 就分道扬镳 ✗。
> 讲义 p.31 的 Example 2 是 $\bar AB + AB$（两项都含 $B$、只差 $A$ 的正反），才能提出公因子 $B$。
>
> **Example 3 — 讲义 p.32 Example 3：完整照抄讲义的标注**
>
> 题目：化简 $Y = AB + A(B+C) + B(B+C)$。
>
> 解（右侧文字就是讲义上标注的规则）：
>
> | 步骤 | 表达式 | 用到的规则 |
> |---|---|---|
> | 1 | $Y = AB + A(B+C) + B(B+C)$ | 原式 |
> | 2 | $= AB + AB + AC + BB + BC$ | distributive law |
> | 3 | $= AB + AC + B + BC$ | Rule 5（$AB+AB=AB$）、Rule 6（$BB=B$） |
> | 4 | $= AB + AC + B$ | Rule 10（$B+BC=B$） |
> | 5 | $= AC + B$ | Rule 10（$B+AB=B$） |
>
> **数值校验 (Numerical check)**：8 行枚举，原式 $= 0,0,1,1,0,1,1,1$；
> $AC + B = 0,0,1,1,0,1,1,1$ —— **完全一致** ✓。
> 第 3 行 $(0,1,0)$ 是关键行：原式 $AB=0$、$A(B+C)=0$、$B(B+C)=1$，得 1；
> $AC+B = 0+1 = 1$ ✓。
>
> **讲义 p.32 的规则编号有一处笔误**
> 讲义把 $BB=B$ 这一步标成 `Rule 7`；按讲义 p.19 的规则表，$A\cdot A=A$ 是 **Rule 6**，
> Rule 7 是 $A+\bar A=1$（本例里没有出现正反相加）。写作业时按 Rule 6 标注。
>
> **Example 4 — 讲义 p.33 Example 4：补项 $CD(B+\bar B)$ 后再吸收**
>
> 题目：化简 $Y = BC + \bar BD + CD$。
>
> 解：
>
> | 步骤 | 表达式 | 用到的规则 |
> |---|---|---|
> | 1 | $Y = BC + \bar BD + CD$ | 原式（domain = $\{B,C,D\}$） |
> | 2 | $= BC + \bar BD + CD(B + \bar B)$ | Rule 7（$B+\bar B=1$），$CD\cdot 1 = CD$ |
> | 3 | $= BC + \bar BD + BCD + \bar BCD$ | 分配律展开补出来的那一项 |
> | 4 | $= BC + BCD + \bar BD + \bar BCD$ | 交换律 + 结合律，排成两对 |
> | 5 | $= BC(1 + D) + \bar BD(1 + C)$ | 分配律（各自提公因子） |
> | 6 | $= BC + \bar BD$ | Rule 10：$X+XY=X$，用了两次 |
>
> ![[simplification-example4.svg]]
> *图 1 — 讲义 p.33 例④ 的分步推导：第 2 步把 $CD$ 乘上 $(B+\bar B)=1$ 补成两项，
> 第 5 步提出公因子后，第 6 步用 Rule 10 把 $BCD$ 与 $\bar BCD$ 各吸收掉一次，
> 结果 $BC+\bar BD$ 与原式在全部 8 行上取值相同。*
>
> **数值校验 (Numerical check)**：按 $(B,C,D)$ 枚举 8 行，
> $BC+\bar BD+CD = 0,1,0,1,0,0,1,1$；$BC+\bar BD = 0,1,0,1,0,0,1,1$ —— **完全一致** ✓。
> 特别核对 $(B,C,D)=(0,1,1)$：原式 $=0+0+1=1$，结果 $=0+1=1$ ✓ —— 被吸收的正是 $CD$ 这一项。
>
> **中间项的横线不能丢**
> 若把题目写成 $BC+BD+CD$，那么 $(B,C,D)=(0,1,1)$ 时原式 $=1$ 而 $BC+BD=0$ ✗，
> "化简"立刻不成立。$CD$ 之所以多余，是因为它被 $\bar BD$ 在 $B=0$ 时、被 $BC$ 在 $B=1$ 时
> 分别覆盖 —— 这个论证依赖 $\bar B$。
>
> **Preserve behavior, then evaluate cost · 先等价，再比较代价**
>
> Simplification must preserve every specified output row. Annotate intermediate steps with the identity used, especially when absorbing a term or removing a complement. A shorter expression that silently changes one legal input combination is an incorrect design, regardless of how many gates it saves.
>
> Specify the cost metric. Literal count, number of gates, maximum fan-in, logic depth, and path delay are related but not identical. A two-level expression requiring an unavailable six-input gate may need decomposition and additional delay. Complement availability also changes the inverter count.
>
> **Worked application.** $Y=AB+A\bar B+\bar AC$，前两项为 $A(B+\bar B)=A$；再 $A+\bar AC=A+C$。如果只能使用二输入 NOR，先产生 $n=\overline{A+C}$，再用 tied-input NOR 反相得到 Y，共两门。该实现没有说物理 delay 为零。
>
> **English exam question:** What evidence should accompany a claimed minimum circuit?
>
> **Answer:** State the permitted gates, available complements, and optimization metric, then show that the function is preserved on the required rows. A Boolean minimum alone is not a timing proof. Compare [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]], [[Universal Gates and Bubble Pushing]], and [[Propagation Delay and Logic Hazards]].

## 5 · 重点与检查顺序

> [!IMPORTANT] 先固定变量顺序
> $\sum m(\cdot)$ 与 $\prod M(\cdot)$ 的索引都由同一行编号定义，但取 ON／OFF 集不同。漏变量、反写最大项极性与误用无关项是三类高频错误。

代数不易识别的合并用 [[Karnaugh Map Minimization]]；实现的级数与极性在 [[Combinational Logic Analysis and Design]] 核对。

## Sources · 课件依据

主线课件：[Ch4 lecture](../ECE2050-Chap4.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
