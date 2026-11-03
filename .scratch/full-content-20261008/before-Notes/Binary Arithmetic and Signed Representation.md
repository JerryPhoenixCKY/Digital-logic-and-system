---
tags:
  - ECE2050
  - binary-arithmetic
  - signed-numbers
date: 2026-09-16
updated: 2026-10-08
chapter: Ch2
aliases:
  - 二进制运算与有符号表示
  - Binary Arithmetic and Signed Representation
  - 二进制运算与有符号表示 · Ch2
  - Binary Arithmetic
  - 二进制算术运算
  - 二进制四则运算
  - Binary Addition and Subtraction
  - Sign-Magnitude Representation
  - 原码
  - 符号数值表示法
  - 符号-幅值表示
  - Sign and Magnitude
  - Two's Complement Representation
  - 补码
  - 二进制补码
  - 二的补码
  - 2's Complement
  - Signed Binary Multiplication and Division
  - 有符号二进制乘除法
  - 补码乘除法
  - Two's Complement Multiplication and Division
---

# Binary Arithmetic and Signed Representation · 二进制运算与有符号表示

> [!SUMMARY] Quick recall · 英文速览
> Arithmetic uses positional weights. Fixed width determines which bits are retained; signed representation determines what those bits mean.

## 1 · Binary Arithmetic · 先看无符号运算

二进制算术 (binary arithmetic) 使用进位、借位和位权。$1+1=10_2$；乘法是部分积移位相加；除法满足 $a=bq+r$。N 位运算保留低 N 位时按模 $2^N$ 回绕；进位必须与被保留的结果分开记录。

> [!example]- Binary Arithmetic · 推导与例题
> **Derivation · 推导过程**
>
> **① 加法：法则与逐列进位链**
>
> 把"有多进位进来"也算进去，第 $i$ 列的三个输入是 $a_i$、$b_i$、$c_i$（carry-in），输出是
> 本位和 $s_i$ 与向高位的进位 $c_{i+1}$：
>
> $$
> s_i=a_i\oplus b_i\oplus c_i,
> \qquad
> c_{i+1}=a_ib_i+c_i\,(a_i\oplus b_i)
> $$
>
> - 意义：$s_i$ 用**异或**（三个输入里有奇数个 1 就是 1），$c_{i+1}$ 用"至少两个输入是 1"
>   （三个两两组合取或）。这正是后面 Ch6 全加器的公式，所以竖式不是"手算技巧"，而是电路结构。
> - 数值校验（取 $1011_2+0110_2$ 的第 2 列 $i=2$：$a_2=0$、$b_2=1$、$c_2=1$）：
>   $s_2=0\oplus1\oplus1=0$ ✓；$c_3=0\cdot1+1\cdot(0\oplus1)=0+1=1$ ✓ ——
>   与图 1(a) 中该列的"$0+1+1=10$"一致。
> - 完整进位链（$1011_2+0110_2=1\,0001_2$，讲义 p.29）：
>   $c_0=0$；第 0 列 $1+0+0=1$，$c_1=0$；第 1 列 $1+1+0=10$，本位 0、$c_2=1$；
>   第 2 列 $0+1+1=10$，本位 0、$c_3=1$；第 3 列 $1+0+1=10$，本位 0、$c_4=1$。
>   于是结果 $=c_4s_3s_2s_1s_0=1\,0001_2=17$ ✓（$11+6=17$）
> - 溢出预告：结果的最高位 $c_4=1$ 落在第 4 位，而两个操作数都只有 4 位——**这一位就是溢出信号**。
>
> ![[binary-addition-carries.svg]]
> *图 1 — (a) $1011_2+0110_2$ 的竖式：每一列标出 carry-in 与 carry-out，箭头表示"本列的进位
> 就是左边一列的进位输入"，最终得到 5 位结果 `1 0001`。(b) 若寄存器只有 4 位，最高位的进位
> 被迫丢弃，`1 0001` 变成 `0001` = 1，与真值 17 相差 16 —— 这就是溢出。*
>
> **② 减法：借位就是"向高位借 2"**
>
> $0-1$ 时向左边借 1 位，因为 $2^i=2\times2^{i-1}$，所以借来的 1 在本列值 **2**：
>
> $$
> 0-1\;\Longrightarrow\;(0+2)-1=1,\quad\text{并向高位借 }1
> $$
>
> - 意义：和十进制的退位减法完全一样，只是每借一次值 2（十进制借一次值 10）。
> - 数值校验（$1001_2-0011_2$，即 $9-3$）：第 0 列 $1-1=0$；第 1 列 $0-1$ 要向第 2 列借，
>   而第 2 列是 0，于是继续向第 3 列借 → 第 3 列的 1 变成 0，第 2 列变成 $10_2$ 并借 1 给第 1 列
>   （自己剩 $1$）；第 1 列 $10_2-1=1$；第 2 列 $1-0=1$；第 3 列 $0-0=0$ → 结果 `0110` $=6$ ✓（$9-3=6$）
> - 不够减时：$0011_2-0101_2$（$3-5$）会借出第 3 位，得到 `1110` $=14$ 且借位标志 = 1。
>   这不是"14"，而是 $-2 \bmod 16=14$ ✓（$3-5=-2$，$-2+16=14$）。
>
> **③ 乘法：只有 $1\times1=1$ → 部分积移位相加**
>
> $A\times B=\sum_{i} b_i\cdot(A\times2^{i})$：乘数第 $i$ 位是 1 就把 $A$ 左移 $i$ 位写下来，是 0 就写全 0，
> 最后把 $n$ 行**部分积**加起来。
>
> - 意义：二进制乘法不需要乘法表，只需要**移位寄存器和加法器**——这就是硬件乘法器的全部（Ch8 内容）。
> - 位数规律：$m$ 位 $\times$ $n$ 位，结果最多 $m+n$ 位（$4\times4$ 位最多 8 位），累加器必须留够宽度。
> - 数值校验（$1011_2\times1101_2$，自算）：见 Example 2，结果 $1000\,1111_2=143=11\times13$ ✓。
>
> **④ 除法：长除与"反复相减"是同一件事**
>
> 商第 $i$ 位问的是"**被除数当前余下部分能不能再减一个除数**"：能就写 1 并减掉，不能就写 0。
> 所以"反复相减、数相减次数"与"长除法"给出同一个商，只是前者在二进制里每一步只减一次。
>
> - 意义：商的一位 = 一次比较 + 一次减法，硬件里就是"移位 + 减 + 判符号"（见 [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确|Signed Binary Multiplication and Division]]）。
> - 数值校验（$(1001)_2\div(11)_2$，讲义 p.33）：$9\div3$。反复相减：$9-3=6$（第 1 次）、
>   $6-3=3$（第 2 次）、$3-3=0$（第 3 次）→ 相减 3 次，商 $=3=11_2$，余数 $=0$ ✓。
>
> **⑤ 溢出：固定位宽的模运算语义**
>
> $N$ 位无符号加法器实际计算的是
>
> $$
> S=(A+B)\bmod 2^{N},
> \qquad
> \text{overflow}\iff A+B>2^{N}-1\iff c_{N}=1
> $$
>
> - 意义：第 $N$ 位（最高列的 carry-out）恰好是 $2^N$ 的权，丢弃它就等于减去 $2^N$——
>   这正是"取模"。所以溢出不是玄学：**丢一位 = 减 $2^N$**。
> - 数值校验：$11+6=17$ 需要 5 位；4 位加法器给出 $17\bmod16=1$，即 `0001`；
>   误差 $17-1=16=2^4$ ✓（与图 1(b) 完全对应）。
> - 另一个方向：$3-5=-2$，4 位结果 $(-2)\bmod16=14=$ `1110`，借位标志 = 1 ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — $11+6$ 的竖式进位链（讲义 p.29）**
>
> 题目：用 4 位二进制计算 $1011_2+0110_2$，写出每一列的 carry-in / carry-out，并判断结果需要几位。
>
> 解（列号从 LSB 起为 0）：
> 1. 第 0 列：$1+0+0=1$，本位 1，carry-out 0。
> 2. 第 1 列：$1+1+0=10_2$，本位 0，carry-out 1。
> 3. 第 2 列：$0+1+1=10_2$，本位 0，carry-out 1。
> 4. 第 3 列：$1+0+1=10_2$，本位 0，carry-out 1 —— 它是结果的第 4 位。
> 5. 结果：`1 0001`（5 位），十进制 $16+1=17$。
>
> **数值校验 (Numerical check)**：$11+6=17$ ✓；$1\,0001_2=16+1=17$ ✓；
> 每列的 carry-out 等于左边一列的 carry-in（$c_1=0,c_2=1,c_3=1,c_4=1$）✓；
> 若只有 4 位，`1 0001` 截成 `0001`$=1$，误差 $17-1=16=2^4$ ✓。
>
> **Example 2 — $1011_2\times1101_2$ 的部分积（自算，含部分积表）**
>
> 题目：计算 $1011_2\times1101_2$，用部分积表说明，并把结果写成 4 位一组。
>
> 解：$1011_2=11$、$1101_2=13$。乘数从 LSB 起是 $1,0,1,1$：
>
> | 乘数位 | 权 | 部分积（8 位对齐） | 十进制 |
> |---|---|---|---|
> | $b_0=1$ | $2^0$ | `0000 1011` | 11 |
> | $b_1=0$ | $2^1$ | `0000 0000` | 0 |
> | $b_2=1$ | $2^2$ | `0010 1100` | 44 |
> | $b_3=1$ | $2^3$ | `0101 1000` | 88 |
> | **求和** | | **`1000 1111`** | **143** |
>
> **数值校验 (Numerical check)**：$11\times13=143$ ✓；求和过程
> `0000 1011`$+$`0010 1100`$=$`0011 0111`$=55$，$55+88=143$ ✓；
> $1000\,1111_2=128+8+4+2+1=143$ ✓；位数 $4+4=8$ ✓（143 需要 8 位，7 位装不下）。
>
> **Example 3 — $(1001)_2\div(11)_2$ 的两种视角（讲义 p.33）**
>
> 题目：计算 $9\div3$ 的二进制除法，给出商与余数。
>
> 解一（反复相减，商 = 相减次数）：$1001_2-11_2=110_2$（第 1 次）、$110_2-11_2=11_2$（第 2 次）、
> $11_2-11_2=0$（第 3 次，余数到 0 停止）→ 商 $=11_2=3$，余数 $=0$。
>
> 解二（长除，逐位试商）：被除数 `1001`、除数 `11`。
> ① 取 `1`$=1<3$ → 商位 0；② 取 `10`$=2<3$ → 商位 0；③ 取 `100`$=4\ge3$ → 商位 1，余 $4-3=1$；
> ④ 落下末位得 `11`$=3\ge3$ → 商位 1，余 $3-3=0$。商 $=0011_2$，去掉前导 0 即 `11`$=3$。
>
> **数值校验 (Numerical check)**：$3\times3+0=9$ ✓（商 × 除数 + 余数 = 被除数）；
> 两种视角给出同一个商 `11`$=3$ 与余数 $0$ ✓；余数 $0<$ 除数 $3$ ✓（停止条件成立）。
>
> **Example 4 — 哪些 4 位无符号加法会溢出？（自算）**
>
> 题目：判断 $11+6$、$7+9$、$5+9$、$15+1$ 在 4 位无符号加法器上是否溢出，并给出实际输出。
>
> 解：
>
> | 算式 | 精确和 | 5 位二进制 | 最高列 carry-out | 4 位输出 | 是否溢出 |
> |---|---|---|---|---|---|
> | $11+6$ | 17 | `1 0001` | 1 | `0001`$=1$ | **溢出**（误差 16） |
> | $7+9$ | 16 | `1 0000` | 1 | `0000`$=0$ | **溢出**（误差 16） |
> | $5+9$ | 14 | `0 1110` | 0 | `1110`$=14$ | 不溢出 |
> | $15+1$ | 16 | `1 0000` | 1 | `0000`$=0$ | **溢出**（误差 16） |
>
> **数值校验 (Numerical check)**：$7+9=16>15=2^4-1$ ✓ 溢出；$5+9=14\le15$ ✓ 不溢出；
> $15+1=16$ → $16\bmod16=0$ ✓ 输出 `0000`；
> 判据一致：carry-out = 1 $\iff$ 精确和 $>2^4-1=15$ ✓（这四行的 carry-out 与"是否溢出"完全对应）。
>
> **Arithmetic as Boolean hardware · 算术怎样变成门电路**
>
> A binary addition column has two output roles: the sum bit stays in its current position, and the carry bit moves to the next weight. For bits $a,b,c_{in}$, the arithmetic identity is
>
> $$a+b+c_{in}=s+2c_{out}.$$
>
> The addition symbols here denote integer addition. The logic expressions are $s=a\oplus b\oplus c_{in}$ and $c_{out}=ab+ac_{in}+bc_{in}$, where the final “+” denotes OR. Stating that distinction prevents the common error of treating the output sum bit as the entire numeric sum.
>
> **Worked application — one column, then a word.** 最高位之前某列输入 $a=b=c_{in}=1$，总数为 3=`11`，故 $s=1,c_{out}=1$，且 $1+2\times1=3$。对 4 位无符号 $14+3$：`1110+0011=1 0001`，保留低 4 位是 1，carry-out=1；完整精确值 17 需要第 5 位。carry 并没有使精确和变成 1，而是宽度限制丢掉了 16。
>
> In English: a fixed-width result is a stored residue. Report both the residue and the overflow condition when the problem asks for an $N$-bit computation. If the circuit supplies an extra carry output, that output may be used to reconstruct the full unsigned sum.
>
> **English exam question:** Is the carry-out from subtraction by $A+\bar B+1$ the borrow-out?
>
> **Answer:** Under the usual fixed-width unsigned implementation, carry-out 1 indicates no borrow, and carry-out 0 indicates a borrow. They are complements in that convention. A signed subtraction must instead check its signed representable range.
>
> For implementation, follow [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]], [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径|Ripple Carry and Carry Look-Ahead Adders]], and [[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路|Binary Subtractors and Adder-Subtractors]].

## 2 · Sign-Magnitude Representation · 符号不能直接参与加法

原码 (sign-magnitude representation) 用最高位 s 表示符号，其余位形成幅值 M：$x=(-1)^sM$。N 位范围为 $\pm(2^{N-1}-1)$，存在 +0、−0。不同符号相加要比较幅值；将整个位串直接无符号相加通常不成立。

> [!example]- Sign-Magnitude Representation · 推导与例题
> **图示与讲义依据**
>
> ![[sign-magnitude-zero.svg]]
> *图 1 — (a) 4 位原码的全部 16 个码字按它们所表示的十进制值排在数轴上：$0111$ 与 $1111$ 是范围的两个端点，
> 而 $0000$（$+0$）与 $1000$（$-0$）**叠在同一个位置**，这就是"两个零"。(b) 用竖式算 $(-6)+(+6)$：
> $1110+0110=1\,0100$，也就是十进制的 20 —— 符号位被当成普通权重位卷进了加法。(b) 说明的是下文第 2 条缺陷。*
>
> **Derivation · 推导过程**
>
> **1. 为什么范围是对称的，而且"少一个数"**
>
> $N$ 位一共 $2^{N}$ 个码字，原码把它们分成两半：
>
> | 码字区间 | 数量 | 含义 |
> |---|---|---|
> | `0000` … `0111` | $2^{N-1}$ 个 | 符号位 0：$+0$ 到 $+(2^{N-1}-1)$ |
> | `1000` … `1111` | $2^{N-1}$ 个 | 符号位 1：$-0$ 到 $-(2^{N-1}-1)$ |
>
> 负半边的 $2^{N-1}$ 个码字里，`1000` 被 $-0$ 占掉，真正能用的负数只有 $2^{N-1}-1$ 个。
> 所以范围是 $[-(2^{N-1}-1),\,2^{N-1}-1]$，**对称但不含 $-2^{N-1}$**。
>
> 数值校验（$N=4$）：负码字 $1000\dots1111$ 共 8 个，其中 $1000$ 是 $-0$，剩下 $1001\dots1111$ 恰好 7 个，
> 对应 $-1\dots-7$ ✓ 与 $[-(2^{3}-1),2^{3}-1]=[-7,7]$ 吻合。
>
> **2. 为什么加法不成立：符号位被当成权重位**
>
> 原码的符号位就摆在最高位，而无符号加法器**不认识"符号"这个概念**，它只会把每一位按权重相加。
> 于是符号位 $a_{N-1}$ 被当成权重 $2^{N-1}$ 的普通数据位：
>
> | 列（$N=4$） | $2^{3}$（符号位） | $2^{2}$ | $2^{1}$ | $2^{0}$ |
> |---|---|---|---|---|
> | $-6$ | $1$ | $1$ | $1$ | $0$ |
> | $+6$ | $0$ | $1$ | $1$ | $0$ |
> | 逐位和 | $1$（并产生向 $2^{4}$ 的进位 $1$） | $0$ | $0$ | $0$ |
> | 结果 | $1$ | $0$ | $1$ | $0$ |
>
> $1110_{(2)}=14$，$0110_{(2)}=6$，$14+6=20=1\,0100_{(2)}$ —— 也就是说，**两个绝对值相同、符号相反的数的码字相加，
> 得到的是两个幅值之和的两倍**。丢弃第 5 位进位后剩下 $0100$，在原码里读作 $+4$，也不是 $0$。
>
> 要做对，硬件必须走完全不同的路（见下方 Mermaid）：先看符号是否相同 → 同号则幅值相加、符号照抄；
> 异号则比较两个幅值、大减小、结果取绝对值大的那个的符号。**一次加法要比较三次**，这就是原码被淘汰的原因。
>
> ```mermaid
> flowchart TD
>     A["Two sign/magnitude operands"] --> B{"Sign bits equal?"}
>     B -- yes --> C["Add the two magnitudes<br/>keep the common sign"]
>     B -- no --> D{"Which magnitude is larger?"}
>     D -- "first" --> E["Subtract: |A| - |B|<br/>sign = sign of A"]
>     D -- "second" --> F["Subtract: |B| - |A|<br/>sign = sign of B"]
>     C --> G["Attach the sign bit to the result"]
>     E --> G
>     F --> G
>     G --> H{"Magnitudes equal<br/>and signs differ?"}
>     H -- yes --> I["Result is +0 or -0<br/>pick one by convention"]
>     H -- no --> J["Result code word"]
> ```
>
> **3. 两个零带来的额外代价**
>
> $0000$ 与 $1000$ 表示同一个数 $0$，于是：
>
> - 判零电路要写成 `(code == 0000) or (code == 1000)`，而不是一次比较；
> - 加法结果可能是 $+0$ 也可能是 $-0$，下游必须规定统一用哪一个；
> - $16$ 个码字只承载 $15$ 个数值，编码效率 $15/16$。
>
> **一句话记住原码的处境**
> 原码 = **"能读不能算"**。它像一个带正负号的标签，贴上去很清楚，
> 但你不能把标签直接扔进加法器 —— 加法器只认位权。
>
> **Worked Example · 例题**
>
> **Example 1 — 写出 $-6$ 的 4 位原码（讲义 p.36）**
>
> 题目：用 4 位原码表示 $-6$，并指出符号位与幅值位各是哪几位。
>
> 解：
> 1. 位宽 $N=4$ → 幅值位 $N-1=3$ 位。
> 2. $|-6|=6=110_{(2)}$，已经是 3 位，无需补零。
> 3. $6$ 是负数 → 符号位取 $1$，得到 `1110`。
> 4. 于是 $a_3=1$ 是符号位（负），$a_2a_1a_0=110$ 是幅值 $=6$。
>
> **数值校验 (Numerical check)**：反过来解码 $1110$ → 符号位 $1$ 判为负，幅值 $110_2=4+2=6$，故为 $-6$ ✓。
> 与讲义 p.36 的 $+6=0110$ / $-6=1110$ 完全一致；两者只差最高位 ✓。
>
> **Example 2 — 用 $(-6)+(+6)$ 演示加法失效（讲义 p.37）**
>
> 题目：直接对 $1110$ 与 $0110$ 做二进制加法，看看会发生什么。
>
> 解：
> 1. $1110_{(2)}=8+4+2=14$，$0110_{(2)}=4+2=6$。
> 2. $14+6=20$，二进制是 $1\,0100_{(2)}$（第 5 位是进位）。
> 3. 若保留 5 位，结果是 $20$；若按 4 位截断，得 $0100$，原码读作 $+4$。
>
> **数值校验 (Numerical check)**：
> - $1110+0110$ 逐位验算：$0+0=0$；$1+1=0$ 进位 $1$；$1+1+1=1$ 进位 $1$；$1+0+1=0$ 进位 $1$ → 结果 `1 0100` ✓
> - 真值要求 $(-6)+(+6)=0$，而两种读法分别得到 $20$ 与 $+4$，**都 $\ne 0$** ✓（$20\ne0$、$4\ne0$）
> - 这正是讲义 p.37 标注 `(wrong!)` 的那一步。
>
> **Example 3 — 8 位原码的范围与端点**
>
> 题目：8 位原码能表示的最大数、最小数各是多少？$-6$ 的 8 位原码是什么？
>
> 解：
> 1. 范围公式：$[-(2^{7}-1),\,2^{7}-1]=[-127,\,+127]$。
> 2. 最大数：`0111 1111` $=+127$；最小数：`1111 1111` $=-127$。
> 3. $-6$：幅值 $6=$ `000 0110`（补到 7 位），加符号位得 `1000 0110`。
>
> **数值校验 (Numerical check)**：
> - $0111\,1111_2 = 64+32+16+8+4+2+1 = 127$ ✓；$1111\,1111$ 的幅值是 $127$、符号为负 → $-127$ ✓
> - $1000\,0110$ 的幅值 $000\,0110_2=6$ → $-6$ ✓
> - 注意端点差：8 位无符号最大是 $255$，8 位原码最大只有 $127$ —— 符号位吃掉了整整一半码字 ✓
>
> **Comparing signed representations · 有符号表示的英文理解**
>
> Sign-magnitude is a valid representation with a separate sign and unsigned magnitude. It supports arithmetic when the hardware explicitly handles those fields. The limitation is that an ordinary binary adder cannot treat the entire word as a positional integer and automatically obtain the correct signed result.
>
> For equal signs, add the magnitudes and retain the sign, provided the magnitude fits. For opposite signs, subtract the smaller magnitude from the larger and use the sign of the larger operand. If the magnitudes are equal, the mathematical result is zero; the implementation should state whether it normalizes both zero codes to positive zero.
>
> **Worked application — opposite signs.** 5 位原码：−9=`11001`，+4=`00100`。拆出 signs 1/0 与 magnitudes 9/4，因异号做 $9-4=5$，取幅值较大的 −9 的符号，结果 `10101`=−5。普通位串相加却得 `11101`，按原码读是 −13，说明不能直接沿用无符号加法。将−5回代 $-9+4=-5$ 即验证。
>
> In English: the failed direct addition is evidence about the chosen adder algorithm, not evidence that the representation cannot support arithmetic. A dedicated sign-magnitude datapath can calculate correctly, but it needs sign selection and magnitude comparison.
>
> **English exam question:** Why do $N$ sign-magnitude bits represent only $2^N-1$ distinct numeric values?
>
> **Answer:** There are $2^N$ patterns, but the all-zero magnitude appears with both sign choices. Positive zero and negative zero therefore refer to the same mathematical value. All nonzero magnitudes have one positive and one negative encoding.
>
> Compare [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]] for reuse of a standard adder. [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] provides the magnitude ordering needed here, while [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|Floating-Point Numbers]] also separates a sign from a magnitude-related field.

## 3 · Two's Complement Representation · 负权建立统一加法

补码 (two's complement) 的最高位是负权：

$$x=-b_{N-1}2^{N-1}+\sum_{i=0}^{N-2}b_i2^i.$$

范围 $-2^{N-1}\ldots2^{N-1}-1$。求相反数是在固定位宽内取反加 1；扩展到更多位时复制符号位。最小负数的正数超出原位宽范围，不能按一般例子处理。

> [!IMPORTANT] Carry 与 Overflow 分别检查
> 无符号加法看最高位进位；补码加法看“同号相加却变号”。两者判断的问题不同。减法先写 $A-B=A+\bar B+1$，再按题目约定解释进位／借位。

**例。** 四位 `0111+0001=1000`：无符号 7+1=8 未溢出，但补码范围最大为 7，因此有符号溢出。`1111+0001=0000` 有进位，却表示补码 −1+1=0，无有符号溢出。

> [!example]- Two's Complement Representation · 推导与例题
> **图示与讲义依据**
>
> ![[twos-complement-wheel.svg]]
> *图 1 — 4 位补码排成 16 格圆盘（每格 $22.5^\circ$）：顺时针走一格就是 $+1$，所以"加 $k$"就是"顺时针转 $k$ 格"。
> 从 `0111`（$+7$）再走一格会跨过符号分界线落到 `1000`（$-8$）—— 这就是补码的回绕点，
> 也解释了为什么 $+7$ 再加 $1$ 会得到 $-8$ 而不是 $+8$。*
>
> ![[nbit-range.svg]]
> *图 2 — 4 位下三种表示的对照（同一水平刻度）：unsigned 用满 16 个码字但拿负数没办法；
> sign/magnitude 的 16 个码字只表示 15 个值，多出来的那个被 $-0$ 吃掉，负半边停在 $-7$；
> two's complement 的 16 个码字对应 16 个值，代价是**不对称** —— 唯一多出来的码字 `1000` 变成了 $-8$，没有 $+8$ 与之配对。*
>
> **Derivation · 推导过程**
>
> **1. 为什么"MSB 负权"能自洽**
>
> 把 $N$ 位码字看成一圈 $2^{N}$ 个状态：`0000`…`1111` 顺着数下去，走过 `1111` 之后回到 `0000`。
> 若把 `1000` 起的后半圈解释成负数，最自然的做法就是"从 `1000` 开始每次减 $1$"：
>
> | 码字 | `0111` | `1000` | `1001` | `1010` | … | `1111` | `0000` |
> |---|---|---|---|---|---|---|---|
> | 值 | $+7$ | $-8$ | $-7$ | $-6$ | … | $-1$ | $0$ |
>
> 要让这个表与"按位权求和"一致，就必须把 MSB 的权从 $+8$ 改成 $-8$：$1001$ 若按正权读是 $9$，
> 按负权读是 $-8+1=-7$ ✓，正好接在 $-8$ 后面。**选择补码编码后，这个负位权与模 $2^N$ 的加法自洽；补码本身仍是一种表示约定。**
>
> 数值校验：把 4 位所有码字按 $x=-8a_3+4a_2+2a_1+a_0$ 算一遍，得到
> $0,1,2,3,4,5,6,7,-8,-7,-6,-5,-4,-3,-2,-1$ —— 与上面的表逐项吻合 ✓。
>
> **2. 反符号 (reverse the sign)：取反加 1**
>
> **算法**（讲义 p.40–41）：
>
> 1. **Invert the bits**（逐位取反，$0\leftrightarrow1$）；
> 2. **Add 1**。
>
> **为什么成立**：任意 $N$ 位码字 $x$ 与它的逐位取反 $\bar{x}$ 满足
>
> $$
> x + \bar{x} = \underbrace{11\cdots1}_{N\ \text{bits}} = 2^{N}-1
> \qquad\Longrightarrow\qquad
> \bar{x} = 2^{N}-1-x \;\equiv\; -1-x \pmod{2^{N}}
> $$
>
> 再 $+1$ 就得到 $\bar{x}+1 \equiv -x \pmod{2^{N}}$ —— **丢掉第 $N+1$ 位进位后，恰好是相反数**。
>
> - 意义：一个加法器 + 一排反相器就能求相反数，不需要任何"符号判断"电路。
> - 数值校验（$N=4$，$x=3=$ `0011`）：$\bar{x}=$ `1100`，$3+12=15=2^{4}-1$ ✓；
>   $\bar{x}+1=$ `1101` $=13$，而 $13-16=-3$ ✓。与讲义 p.40 的 `0011 → 1100 → 1101 = -3` 一致 ✓。
> - 数值校验（求 `1001` 的十进制值，讲义 p.41）：`1001` → 取反 `0110` → $+1$ 得 `0111` $=7$，
>   所以 `1001` $=-7$ ✓（与码表一致）。
>
> **命名陷阱：`taking the two's complement` 不是"求补码"**
> 讲义 p.40 特意提醒：历史上把"取反加 1"这个**动作**叫作 *taking the two's complement*，
> 但它容易和"把一个数表示成补码形式"混淆。本课统一叫 **reverse the sign**（求相反数）。
> 记住：**"补码"是名词（一种表示法），"取反加 1"是动词（求相反数）。**
>
> **3. 加法为什么成立，以及进位怎么读**
>
> **三步法**（讲义 p.42–43）：
>
> 1. 把两个十进制数都写成 $N$ 位二进制，**负数用补码形式**；
> 2. 直接做二进制加法（就是 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 里那个无符号加法器）；
> 3. 看符号：同号相加，结果符号应与加数相同；**符号不对就是溢出**。
>
> **第 $N+1$ 位的进位一律丢弃** —— 它不是错误，而是 $\bmod\,2^{N}$ 的定义本身。
>
> **异号相加时，进位直接告诉你结果的符号**（讲义 p.44）：
>
> - 有进位 (carry-out $=1$) → 结果**非负（也可能为零）**；
> - 无进位 (carry-out $=0$) → 结果**为负**。
>
> 为什么：设 $a\ge0$、$b<0$。$b$ 的码字是 $b+2^{N}$，于是 $a+(b+2^{N})=(a+b)+2^{N}$。
> 若 $a+b\ge0$，和 $\ge2^{N}$ → 产生进位；若 $a+b<0$，和 $<2^{N}$ → 没有进位。
>
> 数值校验：
> - $15+(-6)$：`0000 1111` $+$ `1111 1010` $=$ `1 0000 1001`，进位 $=1$，丢弃后 `0000 1001` $=9$ ✓（$15-6=9$ ✓，结果为正 ✓）
> - $16+(-24)$：`0001 0000` $+$ `1110 1000` $=$ `0 1111 1000`，**无**进位，`1111 1000` $=-128+64+32+16+8=-8$ ✓（$16-24=-8$ ✓，结果为负 ✓）
>
> 同号相加的对照：$5+9$ → `0000 0101` $+$ `0000 1001` $=$ `0 0000 1110` $=14$ ✓（无进位，正 ✓）；
> $-5+(-9)$ → `1111 1011` $+$ `1111 0111` $=$ `1 1111 0010` $=-14$ ✓（有进位，负 ✓）。
>
> **4. 溢出判据：同号相加而结果变号**
>
> **判据**（讲义 p.43）：两个加数**符号相同**，而结果的符号**与它们相反** → 溢出。
>
> $$
> \text{overflow} \;=\; \bigl(a_{N-1} = b_{N-1}\bigr)\ \wedge\ \bigl(s_{N-1} \ne a_{N-1}\bigr)
> $$
>
> - 意义：同号相加只会让绝对值更大，一旦大到越过边界，就会"翻"到环的另一侧，符号随之翻转。
> - 数值校验（讲义 p.43 原例）：`1000 0011` $+$ `1100 0110` $=$ `1 0100 1001`。
>   两个加数的 MSB 都是 $1$（同负），而 8 位结果 `0100 1001` 的 MSB 是 $0$（读作 $+73$）→ **符号翻转 → 溢出** ✓。
>   真值 $-125+(-58)=-183$，而 8 位补码范围是 $[-128,127]$，$-183<-128$ ✓ 确实越界。
> - **硬件等价写法**（超出讲义，供理解）：进位进 MSB 列 $c_{N-1}$ 与进位出 MSB 列 $c_{N}$ 不相等时溢出，
>   $\text{overflow}=c_{N-1}\oplus c_{N}$。上例 $c_7=0$、$c_8=1$ → 异或为 $1$ → 溢出 ✓；
>   而 $15+(-6)$ 中 $c_7=c_8=1$ → 异或为 $0$ → 不溢出 ✓。
>
> ![[overflow-detection.svg]]
> *图 3 — (a) 8 位补码数轴 $[-128,+127]$：$(-5)+(-9)=-14$ 落在范围内（合法）；
> $(-125)+(-58)=-183$ 越过左端 $-128$，丢掉第 9 位后"假象结果"是 `0100 1001` $=+73$
> （$-183+256=+73$，正是模 $2^{8}$ 回绕）。(b) 讲义 p.43 原例的逐列加法：两个加数的符号位都是 $1$，
> 而结果的符号位是 $0$ —— 符号翻转就是溢出的信号。*
>
> **5. 减法：加相反数**
>
> **减法 = 加上被减数的相反数**（讲义 p.45），而"相反数"用取反加 1 得到，所以**减法不需要减法器**：
>
> $$
> a-b \;=\; a + (-b) \;=\; a + \bigl(\bar{b}+1\bigr) \pmod{2^{N}}
> $$
>
> 数值校验：
> - $8-3$：$8+(-3)=$ `0000 1000` $+$ `1111 1101` $=$ `1 0000 0101`，**丢弃进位**得 `0000 0101` $=5$ ✓（$8-3=5$ ✓）
> - $3-5$：$3+(-5)=$ `0000 0011` $+$ `1111 1011` $=$ `0 1111 1110` $=-2$ ✓（$3-5=-2$ ✓）
>
> **为什么硬件偏爱补码**
> 一套**无符号加法器** + 一排**反相器**（配合最低位的 carry-in $=1$）就能同时做加法和减法：
> 减法时把 $b$ 取反、让 $c_0=1$，其余照旧。省掉整个减法器，也省掉符号比较电路 ——
> 这是补码在 1960 年代以后一统天下的真正原因。
>
> **6. 符号扩展 (sign extension)**
>
> 把 $N$ 位补码数加宽到 $M>N$ 位时，**把符号位复制到所有新增的高位**，数值不变：
>
> $$
> \underbrace{a_{N-1}}_{1\ \text{位}} \;\longrightarrow\; \underbrace{a_{N-1}\cdots a_{N-1}}_{M-N+1\ \text{位}}
> $$
>
> 数值校验：$-6$ 的 4 位码是 `1010`，扩到 8 位得 `1111 1010` $=-128+64+32+16+8+2=-6$ ✓。
> 若错误地补 $0$（`0000 1010`），会得到 $+10$ —— 数值被彻底改掉 ✗。
>
> **Worked Example · 例题**
>
> **Example 1 — $-6$ 的 4 位补码，并用反符号验证（讲义 p.41）**
>
> 题目：写出 $-6$ 的 4 位补码；再对它做一次取反加 1，看是否回到 $+6$。
>
> 解：
> 1. $|-6|=6=$ `0110`（4 位）。
> 2. 取反：`1001`。
> 3. 加 1：`1001 + 0001 = 1010` → $-6$ 的补码是 `1010`。
> 4. 反符号验证：`1010` → 取反 `0101` → $+1$ 得 `0110` $=+6$ ✓。
>
> **数值校验 (Numerical check)**：
> - 负权公式：`1010` $=-8+2=-6$ ✓
> - 取反加 1 的代数：$\bar{x}+1=2^{4}-1-x+1=16-x$；$x=$`1010`$=10$ → $16-10=6$ ✓
> - 与原码对照：原码的 $-6$ 是 `1110`（[[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法|Sign-Magnitude Representation]]），补码是 `1010`，**两者不同** —— 这也是最容易混的一处 ✓
>
> **Example 2 — 异号相加与进位判别（讲义 p.44）**
>
> 题目：用 8 位补码计算 $15+(-6)$ 与 $16+(-24)$，并解释进位。
>
> 解：
> 1. $15=$ `0000 1111`，$-6=$ `1111 1010`（$6=$`0000 0110` → 取反 `1111 1001` → $+1$）。
>    `0000 1111 + 1111 1010 = 1 0000 1001`；**有进位** → 结果为正，丢弃进位得 `0000 1001`。
> 2. $16=$ `0001 0000`，$-24=$ `1110 1000`（$24=$`0001 1000` → 取反 `1110 0111` → $+1$）。
>    `0001 0000 + 1110 1000 = 0 1111 1000`；**无进位** → 结果为负，结果就是 `1111 1000`。
>
> **数值校验 (Numerical check)**：
> - `0000 1001` $=8+1=9$，而 $15-6=9$ ✓；两加数异号（MSB $=0$ 与 $1$），结果 MSB $=0$，符号没翻转 → 不溢出 ✓
> - `1111 1000` $=-128+64+32+16+8=-8$，而 $16-24=-8$ ✓；结果 MSB $=1$，确实为负 ✓
> - 两条进位规则都被本例验证：有进位 → 正，无进位 → 负 ✓
>
> **Example 3 — 判断溢出：$(-125)+(-58)$（讲义 p.43）**
>
> 题目：在 8 位补码下计算 $(-125)+(-58)$，判断是否溢出。
>
> 解：
> 1. $125=$ `0111 1101` → 取反 `1000 0010` → $+1$ 得 `1000 0011` $=-125$。
> 2. $58=$ `0011 1010` → 取反 `1100 0101` → $+1$ 得 `1100 0110` $=-58$。
> 3. 相加：`1000 0011 + 1100 0110 = 1 0100 1001`，丢弃进位得 `0100 1001`。
> 4. 两个加数 MSB 都是 $1$，结果 MSB 是 $0$ → **符号翻转 → 溢出**。
>
> **数值校验 (Numerical check)**：
> - 真值 $-125-58=-183$，8 位补码范围 $[-128,127]$，$-183<-128$ ✓ 确实越界
> - 假象结果 `0100 1001` $=64+8+1=73$，而 $-183+2^{8}=-183+256=73$ ✓ 正是模 $2^{8}$ 回绕
> - 硬件判据复核：$c_7=0$、$c_8=1$ → $c_7\oplus c_8=1$ → 溢出 ✓
> - 注意：本例**有进位**却仍然溢出 —— 进位标志（无符号溢出）与符号溢出是两回事 ✗
>
> **Example 4 — 用加法实现减法：$3-5$（讲义 p.45）**
>
> 题目：不使用减法器，用 8 位补码算出 $3-5$。
>
> 解：
> 1. $3=$ `0000 0011`。
> 2. $-5$：$5=$ `0000 0101` → 取反 `1111 1010` → $+1$ 得 `1111 1011`。
> 3. `0000 0011 + 1111 1011 = 0 1111 1110`（无进位）。
> 4. `1111 1110` $=-128+64+32+16+8+4+2=-2$。
>
> **数值校验 (Numerical check)**：$3-5=-2$ ✓；结果 MSB $=1$（负）与两加数异号的情形一致（异号相加，无进位 → 结果为负 ✓）。
> 另一路核对：`1111 1110` 取反加 1 → `0000 0001` $+1$ 的前一步 `0000 0001`，即 `0000 0010` $=2$，故原数为 $-2$ ✓。
>
> **Example 5 — 8 位范围与 $-128$ 的特殊性**
>
> 题目：8 位补码的范围是什么？为什么 $+128$ 表示不了？$-128$ 取相反数会怎样？
>
> 解：
> 1. 范围 $[-2^{7},\,2^{7}-1]=[-128,\,127]$。
> 2. $+128$ 需要码字 `1000 0000`，但该码字按负权读是 $-128$；8 位里**没有**表示 $+128$ 的码字。
> 3. $-128$ = `1000 0000` → 取反 `0111 1111` → $+1$ 得 `1000 0000`，**回到自己**。
>
> **数值校验 (Numerical check)**：
> - `1000 0000` $=-128$ ✓；$+127$ 是 `0111 1111` ✓；正数比负数少一个（$128$ 个负数 vs $127$ 个正数 $+$ 一个零）✓
> - 对 $-128$ 取相反数得到 `1000 0000` $=-128$，说明 $+128$ 不可表示 —— 这正是"非对称范围"的代价 ✓
>
> **Signed subtraction and independent checks · 有符号减法与独立验证**
>
> Two's-complement arithmetic works because codes represent residues modulo $2^N$. Signed interpretation assigns the upper half of those residues to negative values. The most significant bit is commonly called the sign bit, but it also has negative positional weight; it is not an independent sign attached to an unsigned magnitude.
>
> For subtraction $A-B$, overflow occurs when $A$ and $B$ have different signs and the stored result has a sign different from $A$. Equivalently, apply the addition overflow rule to the adder that computes $A+\bar B+1$. Carry-out alone is insufficient because it describes unsigned wraparound under a different interpretation.
>
> **Worked application — verify a supplied solution.** 8 位题目 `00001100−11110110`：前者 $=12$，后者 $=246-256=-10$，故真值 $12-(-10)=22$。取反加 1 得 `00001010`，再算 `00001100+00001010=00010110`，即 22，范围 $[-128,127]$ 内且无 signed overflow。若解答文字写 13 或 23，与题目位串及竖式不符，应以两条独立计算链为准。
>
> In English: decoding the operands first gives an independent decimal check. The final bit pattern `00010110` agrees with 22, not 23. The two routes check both the arithmetic and the transcription of the original operands.
>
> **English exam question:** Why does $7-(-1)$ overflow in four bits even though the subtraction is mathematically simple?
>
> **Answer:** The true result is 8, outside the four-bit signed range −8 to 7. The adder stores `1000`, which is interpreted as −8. The operands have different signs, and the result sign differs from the minuend, so signed overflow is asserted.
>
> The circuit appears in [[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路|Binary Subtractors and Adder-Subtractors]]. Use [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] carefully: an unsigned comparison of negative codes does not implement signed ordering.

## 4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确

N 位乘 N 位的完整乘积一般需 2N 位；移位前确定符号扩展和部分积宽度。带符号除法还需声明向零截断等商约定，使余数满足 $a=bq+r$；除数不能为 0。算术右移复制符号，逻辑右移补 0。

> [!example]- Signed Binary Multiplication and Division · 推导与例题
> **Derivation · 推导过程**
>
> **1. 乘法：移位相加的逐步过程 (shift-and-add, step by step)**
>
> 被乘数 $A$、乘数 $B=b_{n-1}\dots b_1b_0$，从 $i=0$（最低位）开始逐位生成部分积：
>
> | 步骤 | 看乘数第 $i$ 位 | 这一行写什么 | 左移量 | 权值 |
> |---|---|---|---|---|
> | 0 | $b_0$ | $b_0=1$ 写 $A$，否则写 0 | 0 | $2^0$ |
> | 1 | $b_1$ | 同上 | 1 | $2^1$ |
> | $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ |
> | $n-1$ | $b_{n-1}$（无符号最高位） | 同上 | $n-1$ | $2^{n-1}$ |
>
> **小例子 $1011_2\times1101_2$**（此处为 4 位无符号幅值：$A=11$，$B=13$；不是 4 位补码正数）：
>
> | $i$ | $b_i$ | 部分积 | 十进制 |
> |---|---|---|---|
> | 0 | 1 | `0000 1011` | 11 |
> | 1 | 0 | `0000 0000` | 0 |
> | 2 | 1 | `0010 1100` | 44 |
> | 3 | 1 | `0101 1000` | 88 |
>
> 各行相加：$11+0+44+88=143=1000\,1111_2$ ✓ —— **乘法被化成了"看位、移位、相加"**：
> $n$ 位乘法只要 $n$ 次判断 + 至多 $n$ 次加法，与乘数的**数值大小**无关（只与位宽有关）。
>
> **讲义 p.46 的例题（$59\times83$）**：$59=11\,1011_2$，$83=101\,0011_2$，
> 按 $59$ 的各位取 $83$ 的移位值：
>
> | $i$ | $59$ 的第 $i$ 位 | 部分积 | 十进制 |
> |---|---|---|---|
> | 5 | 1 | $83\times32$ | 2656 |
> | 4 | 1 | $83\times16$ | 1328 |
> | 3 | 1 | $83\times8$ | 664 |
> | 2 | **0** | 不产生部分积 | 0 |
> | 1 | 1 | $83\times2$ | 166 |
> | 0 | 1 | $83\times1$ | 83 |
>
> $2656+1328+664+0+166+83=4897$ ✓，$4897_{10}=10\,0110\,0100\,001_2$。
>
> ![[signed-multiplication-partial-products.svg]]
> *图 1 — $59\times83$ 的部分积阶梯：顶部一行是各位的权值，每一行是一个 $83\times2^{i}$ 的移位部分积
> （乘数位为 0 的那一行显式标注"不产生部分积"），行和 $=4897$；图的下半部分把 $+4897$ 放进 14 位补码
> （取反 → 加 1）得到 $-4897=10\,1100\,1101\,1111_2$，并标出 14 位补码范围 $[-8192,+8191]$ 容得下它。*
>
> **2. 为什么补码可以这样算（原理与修正项）**
>
> **（a）移位相加为什么等于乘法。** 把乘数按位权展开：
>
> $$
> A\times B=A\times\sum_{i=0}^{n-1}b_i2^i=\sum_{i=0}^{n-1}b_i\bigl(A\cdot2^i\bigr)
> $$
>
> 左边是一次乘法，右边只是"移位 + 条件相加"。$A\cdot2^i$ 在硬件里就是左移 $i$ 位，低位补 0 即可。
>
> **（b）补码乘数多出来的那一项。** 补码下最高位的权是**负**的：
>
> $$
> B=-b_{n-1}2^{n-1}+\sum_{i=0}^{n-2}b_i2^i
> $$
>
> 若照 (a) 把 $b_{n-1}$ 也当成 $+2^{n-1}$，就会**多算** $b_{n-1}\cdot A\cdot2^{n-1}\cdot2$；两种等价的修正写法：
>
> 1. **修正项法**：先按无符号算出 $\sum b_iA2^i$，再减去最高位那一行的"错算量"（在 $2n$ 位宽度下表现为丢弃最高进位）；
> 2. **符号扩展法**（硬件常用）：把每个部分积**符号扩展**到 $2n$ 位后再相加 —— 符号位的负权值被自动带上，
>    不需要显式减法。**手算推荐这一种**。
>
> **（c）为什么"符号扩展"是必需的。** 取 4 位补码 $A=1011_2$（$=-5$）、$B=0011_2$（$=+3$），
> $A\times B=-15$，需要 8 位（$1111\,0001_2$）。两个部分积是 $A\cdot2^0$ 与 $A\cdot2^1$：
>
> | 处理方式 | 第 0 行 | 第 1 行 | 相加结果 | 判定 |
> |---|---|---|---|---|
> | **错误**：把补码位串当无符号数 | `0000 1011` $=+11$ | `0001 0110` $=+22$ | `0010 0001` $=+33$ | ✗ 符号丢失，$+33\ne-15$ |
> | **正确**：先符号扩展到 8 位 | `1111 1011` $=-5$ | `1111 0110` $=-10$ | `1111 0001` $=-15$ | ✓ 与 $-5\times3=-15$ 一致 |
>
> 原因：位串 `1011` 只有**在 4 位宽度里**才表示 $-5$；放进 8 位却不复制符号位时，最高位的权值变成 $+2^7$，
> 数值被解释成 $+11$。**符号扩展 = 把负权值带进新宽度**。
>
> **手算口诀**
> 画一张"权值行 + 每行左移"的表：**每一行都比上一行多一个前导符号位**；符号位那一行照常参与相加，
> 最后取结果的**低 $2n$ 位**。
>
> **3. 除法：反复相减的逐步过程 (repeated subtraction / restoring)**
>
> **算法**：$R\leftarrow|A|$，$Q\leftarrow0$；只要 $R\ge|B|$ 就做 $R\leftarrow R-|B|$、$Q\leftarrow Q+1$；
> 当 $R=0$ 或 $R<|B|$ 时停止，$Q$ 是商、$R$ 是余数。若某一步减完变负（多减了一次），
> 就把除数**加回**（restore），商不加 1 —— 这就是"**恢复余数除法 (restoring division)**"名字的由来。
>
> ![[signed-division-restoring.svg]]
> *图 2 — (a) 用反复相减做 $100\div25$：余数从 `0110 0100` 逐步减 `0001 1001`，每减一次商加 1，
> 第 4 次减完余数为 $0$ 即停止，商 $=4=0100_2$、余数 $=0$，故 $100=4\times25+0$；
> (b) 幅值算完后**再修符号**：同号得 $+4=0000\,0100_2$，异号得 $-4=1111\,1100_2$（取反加一），
> 并用位权回读 $1111\,1100_2=-4$ 校验。*
>
> **逐位长除法视角**（讲义 p.47 的 *Add 1 to quotient* 步骤）：把被除数逐位落下形成部分余数，
> 每落一位就比较"部分余数 $\ge$ 除数？"：是则减去除数并在商对应位记 1，否则记 0。
> 本质仍是反复相减，只是商位与移位被组织进了一条流水线。
>
> **符号修正**：幅值除法做完之后按 $\text{sign}(A/B)=\text{sign}(A)\oplus\text{sign}(B)$ 定符号；
> 负数商再"取反加一"。余数保持**截断除法**约定：余数符号跟随被除数。
>
> **4. 问题与修复 (Problems and How They Are Fixed)**
>
> | # | 问题 (Problem) | 为什么是问题 | 修复 (Fix) |
> |---|---|---|---|
> | 1 | 直接累加实现乘法 | 乘数是 $B$ 就要加 $B$ 次，$B=59$ 尚可，$B=10^6$ 不可接受 | **移位相加**：只看乘数的 $n$ 位，$n$ 次"判断—移位—加" |
> | 2 | 补码操作数不能直接累加（讲义 p.46：*must be in true form*） | 负数没有"真值位串"，直接累加符号会乱 | **两条正确路线二选一**：① 先转真值，算完再定符号；② 位串直接用 + 按符号位权值修正。**不要混用** |
> | 3 | 部分积忘记符号扩展 | 高位符号丢失，负值被读成正值（$0010\,0001=+33\ne-15$） | 每行**复制符号位**扩展到 $2n$ 位后再相加 |
> | 4 | 乘积位宽只留 $n$ 位 | $11\times13=143$ 需要 8 位，4 位放不下，高位被截 | 结果寄存器取 **$2n$ 位** |
> | 5 | 商的符号弄错 | 幅值除法本身不含符号信息 | 幅值算完后按**同号正 / 异号负**修正，负数商取反加一 |
> | 6 | 余数减成负数还在继续 | 多减了一次除数 | **restore**：加回除数，商不变；停止条件写成 $R=0$ 或 $R<|B|$ |
> | 7 | 余数符号约定不一致 | 不同语言/教材约定不同（截断 vs 向下取整） | 本课程统一用**截断除法**：余数与被除数同号 |
> | 8 | 术语混乱 | "取补码"既指表示法又指"取反加一" | 讲义 p.40 明确：求相反数一律叫 **reverse the sign**；见 [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]] |
>
> **Worked Example · 例题**
>
> **Example 1 — 4 位乘法 $1011_2\times1101_2$**
>
> 已知 $A=1011_2=11$，$B=1101_2=13$，求积。
> 解：按 $B$ 的位从低到高生成部分积（见推导第 1 节的表）：$11+0+44+88=143$。
> **数值校验 (Numerical check)**：$143=128+8+4+2+1=1000\,1111_2$ ✓；十进制验算 $11\times13=143$ ✓；
> 位宽检查：$4$ 位 $\times$ $4$ 位 $\Rightarrow$ $8$ 位结果，`1000 1111` 正好 8 位 ✓。
>
> **Example 2 — 讲义 p.46 的 $59\times83$ 与 $-4897$ 的补码形式**
>
> 已知 $A=59=11\,1011_2$，$B=83=101\,0011_2$，求 $A\times B$ 及 $-A\times B$ 的 14 位补码。
> 解：$59\times83=2656+1328+664+0+166+83=4897$。
> $4897<2^{13}=8192$，需要 $13$ 位幅值位 + $1$ 位符号 = $14$ 位：
> $+4897=$ `01 0011 0010 0001`；取反 `10 1100 1101 1110`；加 1 `10 1100 1101 1111` $=-4897$ ✓
> （与讲义 p.46 给出的 `10110011011111` 一致）。
> **数值校验**：位权回读 $10\,1100\,1101\,1111_2=-8192+2048+1024+128+64+16+8+4+2+1=-4897$ ✓；
> 范围检查：$14$ 位补码 $[-8192,\,+8191]$ 同时容得下 $\pm4897$ ✓。
>
> **Example 3 — 讲义 p.47 的除法 $01100100_2\div00011001_2$**
>
> 已知被除数 $100$、除数 $25$，求商与余数。解（反复相减，见图 2(a)）：
>
> | 步骤 | 余数（二进制） | 十进制 | 商 |
> |---|---|---|---|
> | 初始 | `0110 0100` | 100 | 0 |
> | 减 1 次 | `0100 1011` | 75 | 1 |
> | 减 2 次 | `0011 0010` | 50 | 2 |
> | 减 3 次 | `0001 1001` | 25 | 3 |
> | 减 4 次 | `0000 0000` | 0 | 4 |
>
> 余数为 $0$ → 停止。商 $=4=0100_2$，余数 $=0$。
> **数值校验**：$100=4\times25+0$ ✓；相减次数 $=4=$ 商的十进制值 ✓（无需 restore，恰好整除）。
>
> **Example 4 — 有余数与有符号的情形**
>
> (a) $100\div30$：$100\to70\to40\to10$，$10<30$ 停止 → 商 $=3=0011_2$，余数 $=10=0000\,1010_2$。
> **校验**：$3\times30+10=100$ ✓。
> (b) $100\div(-25)$：幅值部分同 Example 3 得 $4$；$\text{sign}(+)\oplus\text{sign}(-)=$ 异号 → 负，
> 商 $=-4=$ `1111 1100`。**校验**：位权回读 $1111\,1100_2=-128+64+32+16+8+4=-4$ ✓。
> (c) $(-100)\div(-25)$：同号 → 商 $=+4=$ `0000 0100` ✓。可见商的符号完全由操作数符号决定，与幅值无关。
>
> **Width and remainder semantics · 位宽与余数约定**
>
> Choose one multiplication route and retain its interpretation throughout. Magnitude multiplication treats all magnitude bits as nonnegative weights, then applies the product sign. Direct two's-complement multiplication instead assigns negative weight to the multiplier MSB and sign-extends partial products. Mixing those rules produces an incorrect result even when the individual shifts look familiar.
>
> For division truncated toward zero, the quotient has the XOR sign of nonzero operands and the remainder has the dividend's sign when nonzero. Always check $A=QD+R$ and $|R|<|D|$. “Floor division” uses a different rounding rule for negative quotients, so a result from a programming language is not a valid reference until its division convention is known.
>
> **Worked application — negative dividend.** 8 位补码 $A=-23$=`11101001`、$D=5$=`00000101`。先算幅值 $23=4\times5+3$，截断到零得 Q=−4=`11111100`、R=−3=`11111101`。验证 $(-4)\times5+(-3)=-23$，且 $3<5$。若 Q=−5，则 R=2，也满足恒等式但属于向下取整规则，不能混写成同一约定。
>
> In English: the identity alone does not select the rounding convention. The remainder magnitude and sign rules, together with the identity, define the result expected by the specified truncated division.
>
> **English exam question:** Can the most negative $N$-bit value always be divided by −1 in an $N$-bit quotient register?
>
> **Answer:** No. $-2^{N-1}/(-1)=2^{N-1}$ exceeds the maximum signed value $2^{N-1}-1$. This case needs an overflow policy or a wider quotient even though the divisor is nonzero.
>
> Implementations connect to [[Binary Arithmetic Circuits#4 · Combinational Multiplier · 从部分积到列加法|Combinational Multiplier]], [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]], and [[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路|Binary Subtractors and Adder-Subtractors]]. State the intermediate width before taking the absolute value of the most negative input.

## 5 · 解题与实现的连接

先写数学结果和允许范围，再编码、运算、解码复核。位串相同不代表 signed / unsigned 数值相同。门级加减乘结构见 [[Binary Arithmetic Circuits]]；小数的缩放另见 [[Fixed-Point and Floating-Point Numbers]]。

## Sources · 课件依据

主线课件：[Ch2 lecture](../ECE2050-Chap2.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
