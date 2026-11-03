---
tags:
  - ECE2050
  - number-foundations
  - number-bases
  - number-conversion
  - binary-data
date: 2026-09-16
updated: 2026-10-08
chapter: Ch2
aliases:
  - 数制与进制转换
  - Number Systems and Base Conversion
  - 数制与进制转换 · Ch2
  - Number Systems
  - 数制
  - 数制系统
  - 记数制
  - Number System
  - Decimal Number System
  - 十进制
  - 十进制数制
  - Decimal
  - Base-10
  - Binary Number System
  - 二进制
  - 二进制数制
  - Binary
  - Base-2
  - Octal Number System
  - 八进制
  - 八进制数制
  - Octal
  - Base-8
  - Hexadecimal Number System
  - 十六进制
  - Hexadecimal
  - Hex
  - Base-16
  - Number Base Conversion
  - 数制转换
  - 进制转换
  - Base Conversion
  - Radix Conversion
  - Bits and Bytes
  - 位与字节
  - 比特与字节
  - 位/字节/半字节
  - Bit and Byte
---

# Number Systems and Base Conversion · 数制与进制转换

> [!SUMMARY] Quick recall · 英文速览
> A radix defines digits and positional weights. Conversion preserves numerical value; an unlabelled bit pattern does not define its own interpretation.

## 1 · Number Systems · 位权是共同模型

数制 (number system) 由基数 R、数码与位权决定：

$$x=\sum_{i=-m}^{n}a_iR^i,\qquad R\ge2,\quad0\le a_i<R.$$

数码 $a_i$ 和 R 无量纲，i 为位置；小数点右边使用负次幂。先辨认进制与表示约定，再计算数值。没有上下文的 `1011` 不能自动判定为二进制。

> [!example]- Number Systems · 推导与例题
> **图示与讲义依据**
>
> ![[positional-weights.svg]]
> *图 1 — (a) $(568.23)_{10}$ 每一位的位权：柱子的高度就是位权 $10^{i}$（对数刻度，所以每往右一位矮一截），
> 柱顶写着"数码 $\times$ 位权 $=$ 该位贡献"，五段贡献相加正好还原 568.23。(b) 同样的画法换成 base-2：
> 位权序列变成 $2^{1},2^{0},2^{-1},2^{-2},2^{-3}$，被点亮的位（$2^{1}$、$2^{-1}$、$2^{-3}$）相加 $= 2.625$；
> 空位（虚线柱，数码 0）**不是不存在的位置**，只是"这个位置上没有贡献"——这正是后面读二进制、读补码、
> 读定点数时共同的读法。*
>
> **Derivation · 推导过程**
>
> **1. 从"位置决定倍率"推出通式**
>
> 把"位权制"这个想法写成式子只需要三步：
>
> 1. **定位置编号**：小数点左边第 0 位（最右的整数位）权为 $R^{0}=1$；往左每移一位指数 $+1$，
>    往右每移一位指数 $-1$。于是 $n$ 位整数 $+$ $m$ 位小数一共用到指数 $i = n-1,\dots,1,0,-1,\dots,-m$。
> 2. **定每一份的量**：第 $i$ 位的一份就是 $R^{i}$，写上数码 $a_i$ 就表示拿了 $a_i$ 份，即 $a_iR^{i}$。
> 3. **求和**：把每一份加起来，得到 $(N)_R=\sum_{i=-m}^{n-1} a_iR^{i}$。
>
> - 意义：这是一个**齐次加权和**——每一个位置只贡献自己的那一份，位置之间没有耦合。
>   正因为如此，"换基数"才可以逐位/逐组进行（见 [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|Number Base Conversion]] 的分组法）。
> - 数值校验（用 binary point 检验指数编号）：$(10.101)_2$ 中从左到右的指数应为 $1,0,-1,-2,-3$，
>   代入得 $1\times2 + 0\times1 + 1\times0.5 + 0\times0.25 + 1\times0.125 = 2.625$ ✓（讲义 p.7 同值）。
>
> **2. 同一串数字，不同基数就是不同的数**
>
> 通式里 $R$ 是自由参数，所以**同一串符号在不同基数下是不同数值**。以 `1011` 为例：
>
> | 记号 | 展开 | 数值 |
> |---|---|---|
> | $(1011)_2$ | $1\times8 + 0\times4 + 1\times2 + 1\times1$ | $11$ |
> | $(1011)_8$ | $1\times512 + 0\times64 + 1\times8 + 1\times1$ | $521$ |
> | $(1011)_{16}$ | $1\times4096 + 0\times256 + 1\times16 + 1\times1$ | $4113$ |
>
> - 意义：**没有下标就没有数值**。三位数字完全一样，结果差了 374 倍（$4113/11$）。
> - 数值校验：$512+8+1=521$ ✓；$4096+16+1=4113$ ✓（用 Python 复核：`int('1011',2)=11`、
>   `int('1011',8)=521`、`int('1011',16)=4113`）。
> - 位权下滑的速度也不同：base-10 每往右一位"矮"到 $1/10$，base-2 只"矮"到 $1/2$。
>   这就是图 1(a) 与图 1(b) 两条阶梯斜率不同的原因，也是"二进制写起来长"的根源。
>
> **3. 位宽与范围：全章导航表**
>
> 通式只给"值"，不给"能表示多少"。$N$ 位能装下多少个不同的位串，取决于**怎么解释最高位**：
>
> | 位宽 $N$ | 无符号 unsigned $[0,\,2^{N}-1]$ | 原码 sign-magnitude $[-(2^{N-1}-1),\,2^{N-1}-1]$ | 补码 two's complement $[-2^{N-1},\,2^{N-1}-1]$ |
> |---|---|---|---|
> | 4 | $[0,\,15]$ | $[-7,\,7]$ | $[-8,\,7]$ |
> | 8 | $[0,\,255]$ | $[-127,\,127]$ | $[-128,\,127]$ |
> | 16 | $[0,\,65535]$ | $[-32767,\,32767]$ | $[-32768,\,32767]$ |
> | 32 | $[0,\,4294967295]$ | $[-2147483647,\,2147483647]$ | $[-2147483648,\,2147483647]$ |
>
> - 意义：**同样的 $N$ 位，三种解释方式覆盖三段不同的范围**；位数决定"有多少个码字"，解释方式决定"码字怎么映射到数"。
> - 数值校验（$N=8$）：$2^{8}=256$ 个码字；无符号 $[0,255]$；原码 $\pm(2^{7}-1)=\pm127$；
>   补码下界 $-2^{7}=-128$。三者都是 256 个码字，只是分配方式不同 ✓。
> - 阅读顺序：位宽与容量 $\to$ [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|Bits and Bytes]]；负号怎么放 $\to$ [[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法|Sign-Magnitude Representation]]、
>   [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]]；小数点怎么放 $\to$ [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度|Fixed-Point Numbers]]、[[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|Floating-Point Numbers]]。
>
> ```mermaid
> flowchart TD
>     A["Base-R three elements: base, digit, weight"] --> B["Positional expansion: N = sum of a_i times R^i"]
>     B --> C["Decimal base-10"]
>     B --> D["Binary base-2"]
>     B --> E["Octal base-8"]
>     B --> F["Hexadecimal base-16"]
>     D --> G["Number Base Conversion: move between bases"]
>     D --> H["Bits and Bytes: how many values can N bits hold"]
>     H --> I["Sign-Magnitude and Two's Complement: where to put the minus"]
>     H --> J["Fixed-Point and Floating-Point: where to put the point"]
> ```
>
> **Worked Example · 例题**
>
> **Example 1 — 按位权展开 $(568.23)_{10}$（讲义 p.6）**
>
> 题目：把 $(568.23)_{10}$ 写成各路位权贡献之和。
>
> 解：
> 1. 整数部分 $568$，小数部分 $23$，小数点在 $8$ 与 $2$ 之间。
> 2. 逐位写：$5\times10^{2} + 6\times10^{1} + 8\times10^{0} + 2\times10^{-1} + 3\times10^{-2}$。
> 3. 化简每一份：$500 + 60 + 8 + 0.2 + 0.03$。
>
> **数值校验 (Numerical check)**：$500+60+8+0.2+0.03 = 568.23$ ✓，与 $2^{-1}=0.5$、$10^{-2}=0.01$ 的
> 位权定义一致（$2\times0.1=0.2$、$3\times0.01=0.03$）。
>
> **Example 2 — 同一串 `1011` 在三种基数下分别是多少**
>
> 题目：分别求 $(1011)_2$、$(1011)_8$、$(1011)_{16}$。
>
> 解：
> 1. base-2：$1\times8 + 0\times4 + 1\times2 + 1\times1 = 8+2+1 = 11$。
> 2. base-8：$1\times512 + 0\times64 + 1\times8 + 1\times1 = 512+8+1 = 521$。
> 3. base-16：$1\times4096 + 0\times256 + 1\times16 + 1\times1 = 4096+16+1 = 4113$。
>
> **数值校验 (Numerical check)**：用 Python 复核 `int('1011',2) = 11`、`int('1011',8) = 521`、
> `int('1011',16) = 4113` ✓。三个结果的数量级都低于各自的最高位权（$16$、$8^{4}=4096$、$16^{4}=65536$）✓。
> 结论：**同一串符号 + 不同下标 = 不同的数**，这也是本库把下标写死的理由。
>
> **Example 3 — 判断一串符号属于哪个数制（合法性检查）**
>
> 题目：`2374`、`19`、`1011` 这三个串，哪些能当八进制读？
>
> 解：
> 1. `2374`：四位都是 $0$–$7$ ✓，可以读作 $(2374)_8$。
> 2. `19`：出现数码 $9 > 8-1 = 7$ ✗，不可能是八进制（也不可能是二进制）。
> 3. `1011`：只有 $0$ 和 $1$，八进制、二进制、十六进制都合法——**必须靠上下文或下标消歧**。
>
> **数值校验 (Numerical check)**：$(2374)_8 = 2\times512 + 3\times64 + 7\times8 + 4\times1 = 1024+192+56+4 = 1276$ ✓
> （讲义 p.15 同值）。而 `19` 若按十进制读是 19，按十六进制读是 $1\times16+9=25$——正因为合法，
> 才更需要下标。
>
> **Representation choices · 表示法与英文理解**
>
> A base tells you how positional weights grow; an encoding tells you what a bit pattern means. These are separate decisions. The string `10000010` is not enough to determine a value until the problem states whether it is unsigned, two's complement, sign-magnitude, or biased. A stored pattern has no intrinsic signedness.
>
> Biased representation stores an offset from the value. If the unsigned stored integer is $u$ and the bias is $B$, then
>
> $$u=x+B,\qquad x=u-B.$$
>
> Here $B$ is a specified integer offset, not a sign bit. For an unrestricted $N$-bit biased integer encoding, the range is $[-B,2^N-1-B]$. A floating-point exponent can use the same mechanism while reserving some field values for special purposes. Therefore the range of a general biased integer must not be copied blindly into IEEE 754.
>
> **Worked application — decode before calculating.** 8 位偏移码 bias $B=63$，码字 `10000010`。先按无符号位权读 $u=128+2=130$，再减偏移：$x=130-63=67$。同一码字若按 8 位补码读，则 $130-256=-126$。差别来自表示规则，不是计算器出错。回代 $67+63=130$，恢复原码字。
>
> **English exam question:** An eight-bit biased system has bias 63. What does `10000010` represent, and what is its range?
>
> **Answer:** The stored unsigned integer is 130. Subtracting the bias gives 67. With all 256 codes available, values range from $0-63=-63$ to $255-63=192$. The most significant bit must not be interpreted as a two's-complement sign bit.
>
> When revising, explain one pattern in at least two encodings. This trains the distinction between a number, its representation, and the width of its container. Follow [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|Floating-Point Numbers]] for biased exponents, [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]] for semantic state codes, and [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]] for storage organization.

## 2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释

| 进制 | 数码 | 一位对应二进制位数 | 典型用途 |
|---|---|---|---|
| Decimal Number System · 十进制 | 0–9 | 无固定对应 | 人类数量 |
| Binary Number System · 二进制 | 0、1 | 1 | 逻辑与存储 |
| Octal Number System · 八进制 | 0–7 | 3 | 三位成组 |
| Hexadecimal Number System · 十六进制 | 0–9、A–F | 4 | 地址与位掩码 |

例如 $(10.101)_2=2+1/2+1/8=2.625$，$(568.23)_{10}=5\cdot10^2+6\cdot10+8+2/10+3/100$。数值与它的写法要分开。

> [!example]- Decimal Number System · 推导与例题
> **图示与讲义依据**
>
> ![[positional-weights.svg]]
> *图 1 — 十进制数 $(568.23)_{10}$ 的位权展开（左图 (a)）：柱高＝位权 $10^{i}$，从 $10^{2}=100$ 一路降到
> $10^{-2}=0.01$，每一级正好是右边的 10 倍——这就是"每往左一位大十倍"的图像。
> 柱顶的注解给出每位的实际贡献 $5\times10^{2}=500$、$6\times10^{1}=60$、$8\times10^{0}=8$、
> $2\times10^{-1}=0.2$、$3\times10^{-2}=0.03$，五项相加 $=568.23$。
> 小数点左边是整数、右边是小数，图里用虚线标出了这条分界。*
> *(图中 (b) 是同一套画法用在 base-2 上，留给 [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|Binary Number System]] 用；本篇只看 (a)。)*
>
> **Derivation · 推导过程**
>
> **1. 位权阶梯：为什么"每往左一位就大十倍"**
>
> 十进制的位权序列是 $10^{i}$，相邻两位的比值恒为 $10$：
>
> $$
> \frac{10^{i+1}}{10^{i}} = 10,\qquad i = \dots,-2,-1,0,1,2,\dots
> $$
>
> - 意义：只要记住"小数点左边第一位是 $1$、往左每一位乘 $10$；右边第一位是 $0.1$、往右每一位除以 $10$"，
>   就能随口读出任意十进制数。
> - 数值校验：$10^{2}=100$、$10^{1}=10$、$10^{0}=1$、$10^{-1}=0.1$、$10^{-2}=0.01$ ——
>   $100 \div 10 = 10$、$10 \div 10 = 1$、$1 \div 10 = 0.1$、$0.1 \div 10 = 0.01$ ✓，比值处处为 10。
>
> **2. $(568.23)_{10}$ 的展开与求和**
>
> $$
> \begin{aligned}
> (568.23)_{10}
> &= (5\times10^{2}) + (6\times10^{1}) + (8\times10^{0}) + (2\times10^{-1}) + (3\times10^{-2})\\
> &= (5\times100) + (6\times10) + (8\times1) + (2\times0.1) + (3\times0.01)\\
> &= 500 + 60 + 8 + 0.2 + 0.03 = 568.23
> \end{aligned}
> $$
>
> - 意义：**整数部分与小数部分走的是同一套规则**，只是指数从 $0$ 起一个往左、一个往右。
> - 数值校验：$500+60=560$，$560+8=568$；$0.2+0.03=0.23$；$568+0.23=568.23$ ✓（分两次加也对得上）。
>
> **3. "除以 10 取余"与十进制记法自洽**
>
> 把整数 $N$ 反复除以 10，第一个余数其实是 $N \bmod 10$，也就是**最低位 (LSD, least significant digit)**：
>
> $$
> N = 10\,q_0 + r_0,\qquad r_0 = N \bmod 10,\quad q_0 = \lfloor N/10 \rfloor
> $$
>
> 再对 $q_0$ 重复同样的动作，直到商为 0，把余数**从下往上**读就是十进制写法。
>
> - 意义：这条算法说明"十进制记法"本身就是"按 $10$ 的幂分解"，所以它才能同时是**记法**和**算法**。
> - 数值校验（以 $568$ 为例）：
>   $568 = 10\times56 + \mathbf{8}$；$56 = 10\times5 + \mathbf{6}$；$5 = 10\times0 + \mathbf{5}$。
>   余数依次是 $8,6,5$，倒过来读 $5,6,8$，即 $568 = 5\times10^{2}+6\times10^{1}+8\times10^{0}$ ✓。
>
> ```mermaid
> flowchart LR
>     A["Human writes decimal"] --> B["Convert to binary for the hardware"]
>     B --> C["Arithmetic in base-2"]
>     C --> D["Convert back to decimal"]
>     D --> E["Human reads the result"]
>     C --> F["Or keep base-10 digits as BCD to skip conversion"]
> ```
>
> **Worked Example · 例题**
>
> **Example 1 — 按位权展开 $(568.23)_{10}$（讲义 p.6）**
>
> 题目：把 $(568.23)_{10}$ 完全展开成位权之和。
>
> 解：
> 1. 整数部分 $568$：$5\times10^{2} + 6\times10^{1} + 8\times10^{0}$。
> 2. 小数部分 $0.23$：$2\times10^{-1} + 3\times10^{-2}$。
> 3. 合并化简：$500 + 60 + 8 + 0.2 + 0.03$。
>
> **数值校验 (Numerical check)**：$500+60+8 = 568$；$0.2+0.03 = 0.23$；$568+0.23 = 568.23$ ✓。
> 与讲义 p.6 的两行中间结果逐项相同（$(5\times100)+(6\times10)+(8\times1)+(2\times0.1)+(3\times0.01)$）。
>
> **Example 2 — 用"除以 10 取余"把 $(568)_{10}$ 写成位权形式**
>
> 题目：不查任何表，用反复除以 10 的方法说明 $568 = 5\times10^{2}+6\times10^{1}+8\times10^{0}$。
>
> 解：
> 1. $568 \div 10 = 56$ 余 $\mathbf{8}$ → 最低位 $a_0 = 8$（LSD 先出来）。
> 2. $56 \div 10 = 5$ 余 $\mathbf{6}$ → $a_1 = 6$。
> 3. $5 \div 10 = 0$ 余 $\mathbf{5}$ → $a_2 = 5$；商为 0，停止。
> 4. 余数**从下往上**读：$5\,6\,8$。
>
> **数值校验 (Numerical check)**：回代 $500+60+8 = 568$ ✓；商序列 $568 \to 56 \to 5 \to 0$ 每步整除，
> 余数恰好是 $568$ 的各位数字，说明该算法与十进制记法**自洽**（它就是把通式反过来用）。
> 注意：这条算法对任意基数 $R$ 都成立，把 10 换成 2、8、16 就得到
> [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|Number Base Conversion]] 里的"反复除法"。
>
> **Example 3 — "写不完"的小数与基数有关**
>
> 题目：$1/3$ 在十进制下写成小数会怎样？这说明了什么？
>
> 解：
> 1. $1 \div 3 = 0$ 余 $1$ → 第一位 $0.3$，余数又回到 $1$。
> 2. 余数重复 → 后面的位无限循环：$0.333\dots$。
> 3. 换到二进制：$1/3 = 0.0101\,0101\dots_2$，同样写不完（但 $1/10=0.1_{10}$ 在二进制下也是无限循环的 $0.0001\,1001\,1001\dots_2$）。
>
> **数值校验 (Numerical check)**：$3 \times 0.3333 = 0.9999 \ne 1$，而 $3\times(1/3)=1$ ✓ ——
> "写不完"是**表示方式**的限制，不是数值本身有问题；同理 $0.1$ 在二进制里也写不完，
> 这正是 [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|Floating-Point Numbers]] 里"$0.1$ 无法精确表示"的根源。
>
> **Decimal intent in digital hardware · 十进制语义与英文理解**
>
> Decimal notation is convenient for human quantities, but digital hardware may store those quantities in binary. A decimal display requirement does not imply that every internal register must use BCD. The designer can count in binary and convert at the output, or maintain one decimal digit per counter. The choice affects the arithmetic, the number of storage bits, and the decoding logic.
>
> The words “decimal number” identify a radix, whereas “fractional number” identifies a noninteger value. An integer such as 120 is decimal when written in base ten. A value such as $10.1_2$ is fractional but binary. Keep these two classifications independent when reading English questions.
>
> **Worked application — seconds display.** 仪表显示 00–59 s，共 60 种数值。纯二进制计数至少需 $\lceil\log_2 60\rceil=6$ 位；以两位 BCD 存则需 8 位。59 的二进制是 `111011`，BCD 是 `0101 1001`。后一种可把十位 5 和个位 9 分别送入显示译码器，但状态转移必须在 59 后回到 00，不能继续到 60。
>
> In English: six bits are sufficient to enumerate sixty values, but two BCD digits require eight bits because each digit has its own four-bit field. The extra codes are not additional valid seconds. Display format and state range are separate specifications.
>
> **English exam question:** Why does a two-digit decimal counter not necessarily require seven bits because $99<128$?
>
> **Answer:** Seven bits suffice for an unsigned binary encoding of 0–99. A two-digit BCD encoding uses two four-bit fields and therefore requires eight bits. The answer depends on the requested representation, not only on the maximum numeric value.
>
> Apply this distinction in [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码|Binary Coded Decimal]], [[Seven-Segment Display and Code Conversion]], and [[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转|Cascaded Counters and Digital Clocks]].

> [!example]- Binary Number System · 推导与例题
> **图示与讲义依据**
>
> ![[binary-powers-and-counting.svg]]
> *图 1 — (a) $2^{0}$ 到 $2^{10}$ 的位权（对数刻度）与十进制值：柱子每往右一格就翻倍，
> $2^{10}=1024$ 用红色标出，它等于 1 Ki；十进制前缀 k 表示 1000。(b) 四位二进制的完整计数序列 `0000`–`1111`
> （左列 0–7，右列 8–15），每一位下方的红色三角标出"这一步翻的是哪一位"：
> `bit 0` 每一步都翻，`bit 1` 每 2 步翻一次，`bit 2` 每 4 步，`bit 3` 每 8 步；
> 唯一的例外是 `0111 -> 1000`，它一次翻了全部四位——这就是"进位链"的直观样子。*
>
> **Derivation · 推导过程**
>
> **1. 位权阶梯：为什么是"每隔一位翻倍"**
>
> $$
> \frac{2^{i+1}}{2^{i}} = 2
> \qquad\Longrightarrow\qquad
> \dots,\;2^{-2}=0.25,\;2^{-1}=0.5,\;2^{0}=1,\;2^{1}=2,\;2^{2}=4,\;2^{3}=8,\dots
> $$
>
> - 意义：**相邻位权永远差 2 倍**。所以二进制只有"要"和"不要"两种选择，
>   不需要像十进制那样为每一位准备 10 个符号。
> - 数值校验：$0.5\times2=1$、$1\times2=2$、$2\times2=4$、$4\times2=8$、$8\times2=16$ ✓（正是表 1 的右列）。
>
> **2. 逐步展开 $(10.101)_2$（讲义 p.7）**
>
> $$
> \begin{aligned}
> (10.101)_2
> &= (1\times2^{1}) + (0\times2^{0}) + (1\times2^{-1}) + (0\times2^{-2}) + (1\times2^{-3})\\
> &= (1\times2) + (0\times1) + (1\times0.5) + (0\times0.25) + (1\times0.125)\\
> &= 2 + 0 + 0.5 + 0 + 0.125 = (2.625)_{10}
> \end{aligned}
> $$
>
> - 意义：`10.101` 里两个 `0` 位上**没有贡献**，但位权仍然占着位置——
>   二进制点的位置决定了整串数的量级。
> - 数值校验：$2+0.5=2.5$，$2.5+0.125=2.625$ ✓；用另一条路核对：
>   $(10.101)_2$ 去掉小数点就是 $10101_2=21$，而小数点左移 3 位等价于除以 $2^{3}=8$，
>   $21/8=2.625$ ✓（两种算法同值）。
>
> **3. 加 1 的进位链与各位翻转频率**
>
> 二进制加 1 的规则只有一条：**从最低位开始，遇到 1 就变 0 并向左进位，遇到 0 就变 1 并停止。**
>
> $$
> \dots 0111 + 1 = 1000,\qquad 1011 + 1 = 1100,\qquad 1111 + 1 = 1\,0000
> $$
>
> - 意义：`bit 0` 每加一次就翻一次（周期 2），`bit 1` 每 2 次翻一次（周期 4），
>   `bit k` 每 $2^{k}$ 次翻一次（周期 $2^{k+1}$）——**低位翻转快，高位翻转慢**（图 1(b) 的红三角）。
> - 数值校验：从 `1011`（11）数 5 个数：`1100`(12)、`1101`(13)、`1110`(14)、`1111`(15)、`10000`(16)；
>   每一步只在"最低的那个 0"处变 1、它右边的 1 全部变 0，总位数在 `1111 -> 1 0000` 时从 4 位涨到 5 位 ✓
>   （Python：`[bin(11+k) for k in range(1,6)]`）。
>
> 四位二进制的完整计数表（讲义 p.9 的 Counting in Binary，本库把位串一律补成 4 位便于对齐）：
>
> | 十进制 | 四位二进制 | 十进制 | 四位二进制 |
> |---|---|---|---|
> | 0 | `0000` | 8 | `1000` |
> | 1 | `0001` | 9 | `1001` |
> | 2 | `0010` | 10 | `1010` |
> | 3 | `0011` | 11 | `1011` |
> | 4 | `0100` | 12 | `1100` |
> | 5 | `0101` | 13 | `1101` |
> | 6 | `0110` | 14 | `1110` |
> | 7 | `0111` | 15 | `1111` |
>
> 从这张表能直接读出两件事：① **4 位一共 $2^{4}=16$ 个码字**，正好覆盖 $[0,15]$；
> ② 每一个码字与十进制一一对应，**没有多义、没有重码**（这与后面 [[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法|Sign-Magnitude Representation]]
> 的 $\pm0$ 形成对照）。
>
> ```mermaid
> flowchart TD
>     A["Add 1 to the least significant bit"] --> B{"Is that bit 1?"}
>     B -- "no, it is 0" --> C["Set it to 1 and stop"]
>     B -- "yes, it is 1" --> D["Set it to 0 and carry to the next bit on the left"]
>     D --> E{"Any bit left?"}
>     E -- yes --> B
>     E -- "no, carry out of the MSB" --> F["Widen the number: a new 1 appears on the left"]
> ```
>
> **4. 二进制太长：八/十六进制为什么能"压缩"**
>
> $$
> 2^{3} = 8,\qquad 2^{4} = 16
> $$
>
> - 意义：因为 $8$ 与 $16$ 都是 $2$ 的幂，**每 3 位（或 4 位）二进制恰好对应 1 个八进制（十六进制）数字**，
>   分组就是换算，不需要任何除法（讲义 p.19–20，详见 [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|Number Base Conversion]]）。
> - 数值校验：$568_{10}=10\,0011\,1000_2$（10 位）；按 4 位一组补零得 `0010 0011 1000` →
>   $0x238$，只有 3 个十六进制位，长度从 10 个符号降到 3 个 ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 二进制转十进制：$(10011)_2$（讲义 p.10）**
>
> 题目：把 $(10011)_2$ 转成十进制。
>
> 解：
> 1. 共 5 位，指数从 4 到 0：$1\times2^{4} + 0\times2^{3} + 0\times2^{2} + 1\times2^{1} + 1\times2^{0}$。
> 2. 展开幂：$1\times16 + 0\times8 + 0\times4 + 1\times2 + 1\times1$。
> 3. 求和：$16 + 2 + 1 = 19$。
>
> **数值校验 (Numerical check)**：$16+2+1=19$ ✓，与讲义 p.10 的 $1\times16+0\times8+0\times4+1\times2+1\times1=19$
> 完全相同；范围校验：最高位权 $16 \le 19 \le 31 = 2^{5}-1$ ✓。
>
> **Example 2 — 带小数的转换：$(10.101)_2$（讲义 p.7）**
>
> 题目：把 $(10.101)_2$ 转成十进制。
>
> 解：
> 1. 整数部分 `10`：$1\times2 + 0\times1 = 2$。
> 2. 小数部分 `101`：$1\times0.5 + 0\times0.25 + 1\times0.125 = 0.625$。
> 3. 合并：$2 + 0.625 = 2.625$。
>
> **数值校验 (Numerical check)**：$0.5+0.125 = 0.625$ ✓；
> 交叉验算：`10101` $= 21$，$21 \div 2^{3} = 21/8 = 2.625$ ✓；量级校验 $2.625$ 落在 $[2,4)$ ✓。
>
> **Example 3 — 计数：从 $1011_2$ 开始往后数 5 个数**
>
> 题目：写出 $1011_2$ 之后的 5 个二进制数（并给出十进制）。
>
> 解：
> 1. $1011 + 1 = 1100$（最低位的 1 变 0、上一位 0 变 1，进位到此为止）。
> 2. $1100 + 1 = 1101$。
> 3. $1101 + 1 = 1110$。
> 4. $1110 + 1 = 1111$。
> 5. $1111 + 1 = 1\,0000$（进位链穿过全部四位，位宽从 4 位涨到 5 位）。
>
> **数值校验 (Numerical check)**：十进制序列 $11 \to 12,13,14,15,16$ ✓（Python 复核
> `bin(11)=0b1011`、`bin(16)=0b10000`）；第 5 步说明**固定位宽下计数会回绕**：
> 若硬件只有 4 位，$1111+1$ 丢掉最高进位又回到 `0000`——这就是 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 里的溢出。
>
> **Bit patterns in a datapath · 二进制与数据通路**
>
> Binary arithmetic relies on positional weights, while digital logic manipulates the same bits as Boolean variables. For example, adding the integers represented by two words is different from applying an OR gate to each pair of corresponding bits. State the intended operation before writing a symbol such as “+”.
>
> A binary word also has an ordering convention. In the notation $b_{N-1}\ldots b_0$, the leftmost bit is the most significant bit (MSB), and the rightmost bit is the least significant bit (LSB). The subscript is a weight index. It does not by itself specify which physical pin, memory address, or serial transmission time carries that bit.
>
> **Worked application — selecting a memory word.** 存储器有 32 个 word，地址需 5 位，因为 $2^5=32$。地址 `10110` 指 word $16+4+2=22$；该地址上的内容可以是 `00011`，表示数据 3。地址 22 与数据 3 是两个不同角色，不要把数据位宽误当成地址位宽。
>
> In English: the address chooses a location; the data word is the information held at that location. A five-bit address can select 32 words regardless of whether each word contains one bit, eight bits, or another specified width.
>
> **English exam question:** Does left shifting a fixed-width binary word always multiply its numeric value by two?
>
> **Answer:** For an unsigned word, a one-bit left shift multiplies the value by two only when the discarded MSB is zero. Otherwise the stored result is $2x\bmod 2^N$, so the true value has overflowed the available width. Signed interpretation adds its own representable-range check.
>
> Continue with [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] for moving bit patterns and [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]] for addresses. The positional expansion here supplies the numeric interpretation; those notes supply the hardware behavior.

> [!example]- Octal Number System · 推导与例题
> **图示与讲义依据**
>
> ![[linux-file-permissions.svg]]
> *图 1 — 三位一组的八进制实战（Linux 文件权限）。上半部分是 `644` / `755` / `754` 三个例子：
> 每个八进制数字正对着**三个二进制位**，三个位自上而下依次对应 `r`(read, 权 4)、`w`(write, 权 2)、
> `x`(execute, 权 1)，所以 1 个八进制数字就是一组 `rwx`；数字下面标出它的 $4/2/1$ 分解
> （$6=4+2$、$7=4+2+1$、$5=4+1$）。下半部分给出 **0–7 与 `rwx` 的完整对照表**——
> 这正是 3 bit 能表示的全部 8 种组合，也是"1 个八进制位 $=$ 3 bit"最直接的证据。*
>
> **Derivation · 推导过程**
>
> **1. 八进制 → 十进制：按位权求和（讲义 p.15）**
>
> $$
> \begin{aligned}
> (2374)_8
> &= (2\times8^{3}) + (3\times8^{2}) + (7\times8^{1}) + (4\times8^{0})\\
> &= (2\times512) + (3\times64) + (7\times8) + (4\times1)\\
> &= 1024 + 192 + 56 + 4 = (1276)_{10}
> \end{aligned}
> $$
>
> - 意义：与十进制、二进制完全同一套规则，只是把 $10^{i}$ / $2^{i}$ 换成 $8^{i}$。
> - 数值校验：$1024+192=1216$，$1216+56=1272$，$1272+4=1276$ ✓；量级校验：
>   4 位八进制的上界是 $8^{4}-1 = 4095$，$1276$ 落在区间内 ✓。
>
> **2. 十进制 → 八进制：反复除以 8，**首个余数是 LSD**（讲义 p.17）**
>
> $$
> N = 8\,q_0 + r_0,\qquad r_0 = N \bmod 8 \;\Longrightarrow\; r_0 \text{ 是最低八进制位 (LSD)}
> $$
>
> 不断对商重复，直到商为 0，再把余数**从下往上**读。以 $(359)_{10}$ 为例：
>
> | 步骤 | 除法 | 商 | 余数 | 含义 |
> |---|---|---|---|---|
> | 1 | $359 \div 8$ | 44 | 7 | LSD $a_0 = 7$ |
> | 2 | $44 \div 8$ | 5 | 4 | $a_1 = 4$ |
> | 3 | $5 \div 8$ | 0 | 5 | MSD $a_2 = 5$，商为 0 停止 |
>
> 读出的结果：$(359)_{10} = (547)_8$ ✓（讲义 p.17 同一张表）。
>
> - 意义：**第一个余数是最低位**——因为它就是 $N \bmod 8$，也就是"这个数里零出来的、不够再凑一个 8 的部分"。
> - 数值校验：回代 $5\times64 + 4\times8 + 7\times1 = 320 + 32 + 7 = 359$ ✓；
>   另一种看法：$359 = 8\times44 + 7 = 8\times(8\times5+4)+7 = 5\times8^{2}+4\times8+7$ ✓（把商继续展开就得到位权形式）。
>
> **3. 八进制 ↔ 二进制：1 位 = 3 bit（讲义 p.19–20）**
>
> **八进制 → 二进制**：把每个八进制数字换成它自己的 3 位二进制（不足 3 位在左边补 0）。
>
> $$
> (7526)_8 = \underbrace{111}_{7}\;\underbrace{101}_{5}\;\underbrace{010}_{2}\;\underbrace{110}_{6}
> = (111\,101\,010\,110)_2
> $$
>
> **二进制 → 八进制**：**从最右边开始**每 3 位切一组，最左边不足 3 位就补 0，再把每组读成一位八进制。
>
> $$
> (100110011010)_2 = \underbrace{100}_{4}\;\underbrace{110}_{6}\;\underbrace{011}_{3}\;\underbrace{010}_{2} = (4632)_8
> $$
>
> - 意义：两个方向都**只做局部替换**，不涉及任何跨组的进位，所以可以逐组并行地做（硬件上就是接线）。
> - 数值校验：
>   - 方向一：$7\to111$、$5\to101$、$2\to010$、$6\to110$，拼起来 `111 101 010 110`，
>     每 3 位一读即 $7,5,2,6$ ✓；十进制侧核对 $7526_8 = 7\times512+5\times64+2\times8+6 = 3584+320+16+6 = 3926$，
>     而 $(111101010110)_2 = 2048+1024+512+256+64+16+4+2 = 3926$ ✓ **两条路同值**。
>   - 方向二：`100110011010` 共 12 位，从右每 3 位切恰好 4 组 `100 | 110 | 011 | 010`，读出 $4,6,3,2$；
>     位数不是 3 的倍数时要补零，例如 `1001100110` 从右切成 `1 | 001 | 100 | 110`，最左组补 0 成 `001`，
>     读出 $1,1,4,6 = (1146)_8$（补零只补在最左边那一组，补右边会整体错位）。
>   - 校验 $(4632)_8 = 4\times512+6\times64+3\times8+2 = 2458 = (100110011010)_2$ ✓；
>     补零的例子同法核对 $(1146)_8 = 512+64+32+6 = 614 = (1001100110)_2$ ✓。
>
> **4. 为什么是 3 位，而不是 4 位**
>
> $$
> 8 = 2^{3}\;\Rightarrow\;3\text{ bit/位};\qquad 16 = 2^{4}\;\Rightarrow\;4\text{ bit/位}
> $$
>
> - 意义：**压缩比由 $\log_2 R$ 决定**。八进制 3 bit（压缩到 1/3）、十六进制 4 bit（压缩到 1/4，
>   而且正好对齐一个半字节 nibble）；而十进制不是 2 的幂，只能走麻烦的反复除法。
> - 数值校验：十进制的 $568$ 写成二进制是 10 位 `10 0011 1000`；按 3 位分组补零 `1 000 111 000`
>   → `001 000 111 000` → $(1070)_8$（4 位数字）；按 4 位分组 → `0010 0011 1000` → $0x238$（3 位数字）✓
>   十六进制更短——这就是它最终胜出的原因。
>
> ```mermaid
> flowchart TD
>     A["Octal string"] --> B["Replace each octal digit by its three bits"]
>     B --> C["Binary string"]
>     C --> D["Group the bits from the RIGHT in threes"]
>     D --> E{"Leftmost group shorter than 3 bits?"}
>     E -- yes --> F["Pad zeros on the LEFT of that group"]
>     E -- no --> G["Read each group as one octal digit"]
>     F --> G
> ```
>
> **Worked Example · 例题**
>
> **Example 1 — 十进制转八进制：$(359)_{10} \to (\;)_{8}$（讲义 p.17）**
>
> 题目：把 $(359)_{10}$ 写成八进制。
>
> 解：
> 1. $359 \div 8 = 44$ 余 $7$ → LSD $= 7$。
> 2. $44 \div 8 = 5$ 余 $4$ → 第二位 $= 4$。
> 3. $5 \div 8 = 0$ 余 $5$ → 最高位 $= 5$，停止。
> 4. 从下往上读：$547$。
>
> **数值校验 (Numerical check)**：$5\times64 + 4\times8 + 7 = 320+32+7 = 359$ ✓。
> 注意顺序陷阱：若按"从上往下"读会得到 $(745)_8 = 7\times64+4\times8+5 = 485 \ne 359$ ✗，
> 所以必须认准"**首个余数是 LSD**"。
>
> **Example 2 — 八进制转二进制：$(7526)_8 \to (\;)_2$（讲义 p.19）**
>
> 题目：把 $(7526)_8$ 写成二进制。
>
> 解：
> 1. 逐位替换：$7\to111$、$5\to101$、$2\to010$、$6\to110$。
> 2. 拼接：`111 101 010 110`（12 位 $=3\times4$ ✓）。
>
> **数值校验 (Numerical check)**：十进制侧 $7\times512+5\times64+2\times8+6 = 3584+320+16+6 = 3926$；
> 二进制侧 $2048+1024+512+256+64+16+4+2 = 3926$ ✓ 同值。
> 再反向核对：把 `111 101 010 110` 从右切 3 位读回 $7,5,2,6$ ✓。
>
> **Example 3 — `chmod 754` 展开成 rwx 串（八进制的日常用法）**
>
> 题目：`chmod 754 file` 之后，文件所有者 / 同组用户 / 其他用户分别有什么权限？
>
> 解：
> 1. 三个八进制位分别对应三组用户：$7$ = owner、$5$ = group、$4$ = others。
> 2. 每位按 $4/2/1$ 展开成 3 bit，再按 `r/w/x` 读：
>    - $7 = 4+2+1$ → `111` → `rwx`（读 $+$ 写 $+$ 执行）
>    - $5 = 4+1$ → `101` → `r-x`（读 $+$ 执行，**没有写**）
>    - $4 = 4$ → `100` → `r--`（只读）
> 3. 拼起来：`rwxr-xr--`。
>
> **数值校验 (Numerical check)**：$7+5+4=16$ 是"数字之和"，**没有意义**；
> 正确的校验是逐位展开：$7 = 4+2+1$ ✓、$5 = 4+1$ ✓、$4 = 4$ ✓，
> 再用图 1 下半部分的 0–7 对照表回查 `111->rwx`、`101->r-x`、`100->r--` ✓。
> 对照讲义 p.22 的另外两例：`644` $= (110\,100\,100)_2$ $=$ `rw-r--r--`（owner 读写、其余只读）、
> `755` $= (111\,101\,101)_2$ $=$ `rwxr-xr-x` ✓。
>
> **Grouping around the radix point · 八进制分组与英文理解**
>
> Octal is a compact notation for binary because one octal digit represents exactly three bits. Grouping changes the notation without changing the value. Group integer bits from the radix point toward the left, and fractional bits from the point toward the right. Padding is allowed only at the outer ends of those groups.
>
> A useful English distinction is “leading zeros” versus “trailing zeros.” Leading zeros on the integer side do not change its value. Trailing zeros on the fractional side do not change its value either. Inserting a zero next to the radix point can move existing bits to different weights and therefore change the value.
>
> **Worked application — a fractional input.** 将 $11010.1011_2$ 化成八进制：整数补成 `011 010`，小数补成 `101 100`，得到 $32.54_8$。展开验证：$3\times8+2+5/8+4/64=26.6875$。二进制展开也为 $16+8+2+1/2+1/8+1/16=26.6875$。
>
> In English: the padded groups are 011, 010, 101, and 100, so the octal digits are 3, 2, 5, and 4. The final zero in the fractional group contributes zero at a new, smaller weight; it does not move the existing fractional bits.
>
> **English exam question:** Can `11010.1011` be divided into three-bit groups starting at the far left?
>
> **Answer:** No. The radix point fixes the weight alignment. Grouping from the far left can cross the point or associate digits with the wrong powers. Always create separate integer and fractional groups outward from the point.
>
> Use [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|Number Base Conversion]] to compare grouping with repeated division and multiplication. In [[Exam Review and Problem Solving]], show the groups explicitly so that the conversion can be checked without reconstructing your reasoning.

> [!example]- Hexadecimal Number System · 推导与例题
> **图示与讲义依据**
>
> ![[hex-memory-address.svg]]
> *图 1 — 按字节寻址的内存视图。左侧是地址 `0x0000`–`0x0007`，中间一列是这 8 个字节的内容
> （字符串 `ECE2050!`），右边把每个字节**拆成两个 nibble**：高 4 位（bits 7–4，MSB nibble）与
> 低 4 位（bits 3–0，LSB nibble），每一位都用二进制写出来。对照第一行 `0x45`：
> 高 nibble `0100` $=4$、低 nibble `0101` $=5$，所以 **2 个十六进制位就是 1 个字节**，
> 而 **1 个十六进制位就是 1 个 nibble**。最后一字节的地址是 `0x0007`，即"起始地址 $+$ 字节数 $-1$"。*
>
> **Derivation · 推导过程**
>
> **1. 十六进制 → 十进制：按位权求和（讲义 p.16）**
>
> $$
> \begin{aligned}
> (E5)_{16}
> &= (E\times16^{1}) + (5\times16^{0})\\
> &= (14\times16) + (5\times1) = 224 + 5 = (229)_{10}
> \end{aligned}
> $$
>
> - 意义：还是同一套通式，只是数码 `E` 必须先换成数值 $14$——**字母数码是"值"，不是"字符串"**。
> - 数值校验：$14\times16 = 224$ ✓，$224+5 = 229$ ✓；量级校验 $229 < 16^{2} = 256$ ✓（两位数不会超过 256）。
>
> **2. 十进制 → 十六进制：反复除以 16，**首个余数是 LSD**（讲义 p.18）**
>
> 余数落在 $[0,15]$，其中 $10$–$15$ 要写成 `A`–`F`。以 $(650)_{10}$ 为例：
>
> | 步骤 | 除法 | 商 | 余数 | 写作 | 含义 |
> |---|---|---|---|---|---|
> | 1 | $650 \div 16$ | 40 | 10 | `A` | LSD $a_0$ |
> | 2 | $40 \div 16$ | 2 | 8 | `8` | $a_1$ |
> | 3 | $2 \div 16$ | 0 | 2 | `2` | MSD $a_2$，商为 0 停止 |
>
> 读出的结果：$(650)_{10} = (28A)_{16}$ ✓（讲义 p.18 同一张表）。
>
> - 意义：与十进制→八进制完全同构，只是除数从 8 换成 16，并且余数 $10$–$15$ 要多做一次
>   "数字 ↔ 字母"的翻译。
> - 数值校验：回代 $2\times256 + 8\times16 + 10\times1 = 512 + 128 + 10 = 650$ ✓。
>
> **3. 十六进制 ↔ 二进制：1 位 = 4 bit（讲义 p.19–20）**
>
> **十六进制 → 二进制**：每个十六进制数字换成它自己的 4 位二进制（不足 4 位左侧补 0）。
>
> $$
> (CF8E)_{16} = \underbrace{1100}_{C}\;\underbrace{1111}_{F}\;\underbrace{1000}_{8}\;\underbrace{1110}_{E}
> = (1100\,1111\,1000\,1110)_2
> $$
>
> **二进制 → 十六进制**：从最右边开始每 4 位切一组，最左不足 4 位补 0，再把每组读成一位十六进制。
>
> $$
> (1100101001010111)_2 = \underbrace{1100}_{C}\;\underbrace{1010}_{A}\;\underbrace{0101}_{5}\;\underbrace{0111}_{7}
> = (CA57)_{16}
> $$
>
> - 意义：两个方向都是**局部替换**，可以逐组并行；4 位一组正好是 nibble，所以十六进制与字节结构天然对齐。
> - 数值校验：
>   - 方向一：$C\to1100$、$F\to1111$、$8\to1000$、$E\to1110$，拼成 16 位 ✓；
>     十进制侧 $CF8E_{16} = 12\times4096 + 15\times256 + 8\times16 + 14 = 49152 + 3840 + 128 + 14 = 53134$，
>     二进制侧 $32768+16384+2048+1024+512+256+128+8+4+2 = 53134$ ✓ **两条路同值**。
>   - 方向二：`1100 1010 0101 0111` 读出 $C,A,5,7$；十进制侧 $12\times4096+10\times256+5\times16+7 = 49152+2560+80+7 = 51799$，二进制侧 $32768+16384+2048+512+64+16+4+2+1 = 51799$ ✓。
>
> **4. 1 byte = 2 个十六进制位：$00$–$FF$**
>
> $$
> 2\ \text{hex digits} = 8\ \text{bits} = 1\ \text{byte},\qquad 16^{2} = 256 = 2^{8}
> $$
>
> - 意义：一个字节的取值范围恰好是 $0x00$–$0xFF$，即十进制 $[0,255]$。这就是**内存转储 (memory dump)**
>   的排版方式：左边一列地址、右边每字节两个十六进制位；也是**颜色码** `#RRGGBB` 的由来——
>   R、G、B 各占一个字节，`00` 最暗、`FF` 最亮（`#FF0000` 是纯红，`#FFFFFF` 是白）。
> - 数值校验：$16^{2} = 256 = 2^{8}$ ✓；`0xFF` $=15\times16+15 = 255$ ✓；
>   `#1F6F8B` 拆成三字节 `1F`$=31$、`6F`$=111$、`8B`$=139$，每个都落在 $[0,255]$ ✓。
> - 与字符的关系：内存里的字符串本来就是**字节序列**，而 [[Data Coding and Character Representation#4 · American Standard Code for Information Interchange · 字符编码|American Standard Code for Information Interchange]]
>   规定 `'E'` $=0x45$、`'C'` $=0x43$……所以图 1 里那 8 个字节读出来就是 `ECE2050!`。
>
> ```mermaid
> flowchart TD
>     A["Hexadecimal string"] --> B["Replace each hex digit by its four bits"]
>     B --> C["Binary string"]
>     C --> D["Group the bits from the RIGHT in fours"]
>     D --> E["Pad the leftmost group with zeros if needed"]
>     E --> F["Two groups = one byte, written as 0x00 to 0xFF"]
> ```
>
> **Worked Example · 例题**
>
> **Example 1 — 十进制转十六进制：$(650)_{10} \to (\;)_{16}$（讲义 p.18）**
>
> 题目：把 $(650)_{10}$ 写成十六进制。
>
> 解：
> 1. $650 \div 16 = 40$ 余 $10$ → 写作 `A`（LSD）。
> 2. $40 \div 16 = 2$ 余 $8$ → 第二位 `8`。
> 3. $2 \div 16 = 0$ 余 $2$ → 最高位 `2`，停止。
> 4. 从下往上读：`28A`。
>
> **数值校验 (Numerical check)**：$2\times256 + 8\times16 + A(=10)\times1 = 512+128+10 = 650$ ✓。
> 反方向再用除以 16 走一遍：余数序列 $10,8,2$ 倒读得 `28A` ✓（讲义 p.18 的表完全相同）。
> 若把 $10$ 直接写成数字而不是 `A`，会得到非法的 `2810`——这是本例题唯一的坑。
>
> **Example 2 — 十六进制转二进制：$(CF8E)_{16} \to (\;)_2$（讲义 p.19）**
>
> 题目：把 $(CF8E)_{16}$ 写成二进制。
>
> 解：
> 1. 四位分别查表：$C\to1100$、$F\to1111$、$8\to1000$、$E\to1110$。
> 2. 拼接：`1100 1111 1000 1110`（16 位 $=4\times4$ ✓）。
>
> **数值校验 (Numerical check)**：十进制侧 $12\times4096 + 15\times256 + 8\times16 + 14 = 49152+3840+128+14 = 53134$；
> 二进制侧 $32768+16384+2048+1024+512+256+128+8+4+2 = 53134$ ✓ 同值。
> **反向校验**：把 `1100 1111 1000 1110` 从右每 4 位读回 $C,F,8,E$ ✓；
> 练习用讲义 p.20 的另一个方向：$(1100101001010111)_2 = (CA57)_{16}$，
> 两边十进制都是 $51799$ ✓。
>
> **Example 3 — 一段 8 字节数据的十六进制地址表**
>
> 题目：把字符串 `ECE2050!` 存到从 `0x0000` 开始的内存里，写出地址表，并说明最后一个字节的地址。
>
> 解：
> 1. 先取每个字符的 ASCII 码（十六进制）：`E`$=0x45$、`C`$=0x43$、`E`$=0x45$、`2`$=0x32$、
>    `0`$=0x30$、`5`$=0x35$、`0`$=0x30$、`!`$=0x21$。
> 2. 逐字节排地址（每字节占 1 个地址）：
>
> | 地址 | `0x0000` | `0x0001` | `0x0002` | `0x0003` | `0x0004` | `0x0005` | `0x0006` | `0x0007` |
> |---|---|---|---|---|---|---|---|---|
> | 字节 | `45` | `43` | `45` | `32` | `30` | `35` | `30` | `21` |
> | 字符 | `E` | `C` | `E` | `2` | `0` | `5` | `0` | `!` |
>
> 3. 最后一字节地址 $=$ 起始地址 $+$ 字节数 $-1$ $=$ `0x0000` $+ 8 - 1 =$ `0x0007`。
>
> **数值校验 (Numerical check)**：用位权展开核对 `0x0007` $= 0\times16^{3}+0\times16^{2}+0\times16^{1}+7\times16^{0} = 7$ ✓，
> 与"第 8 个字节（从 0 开始编号）"一致：$0+8-1 = 7$ ✓。
> 总容量 $8$ 字节 $= 8\times8 = 64$ bit $= 16$ 个十六进制位（表里 8 列各 2 位）✓；
> 下一个可用地址是 `0x0008`（末尾地址 $+1$），这也是"起始地址 $+$ 长度"的由来。
>
> **Hexadecimal as a hardware reading tool · 十六进制读硬件**
>
> Hexadecimal is useful because it exposes four-bit fields without changing the underlying binary pattern. One byte occupies two hex digits. A value written as `0xA6` is still eight binary bits when the container is a byte; it does not become two physical digits inside the circuit.
>
> When a question gives a hex dump, separate address, data, and interpretation. An address locates a byte or word under the stated memory organization. Data is the stored pattern. Signedness, character encoding, and fractional scaling are additional interpretations applied to that pattern. Hex notation alone does not select any of them.
>
> **Worked application — inspect a status byte.** 状态字节 `0xA6` 展开成 `1010 0110`。若 bit 7=ready、bit 2=error、bits 1:0=mode，则 ready=1，error=1，mode=`10`=2。检验 error 可按位 AND `0x04`：`0xA6 AND 0x04 = 0x04`；mode 可取 `0xA6 AND 0x03 = 0x02`。掩码的位置由 bit 编号确定。
>
> In English: a mask keeps selected positions and clears the others. A nonzero masked result says that at least one selected bit is set; it does not necessarily equal the numeric value of the whole field unless the field is aligned to bit zero.
>
> **English exam question:** Is `0xFF` always the decimal integer 255?
>
> **Answer:** It is the unsigned numeric reading of that eight-bit pattern. As an eight-bit two's-complement word it represents −1. As a byte in a character stream its meaning depends on the encoding. The required representation must be stated.
>
> Connect the same reading method to [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|Bits and Bytes]], [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]], [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]], and [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]].

## 3 · Number Base Conversion · 整数、小数与分组

任意进制转十进制按位权展开；十进制整数转 R 进制反复除 R，余数**从最后到最先**读取。小数部分反复乘 R，整数部分**按产生顺序**读取。

八／十六进制与二进制互转，从小数点向两侧分别按 3／4 位分组；整数侧向左补 0，小数侧向右补 0。不能跨小数点混组。

> [!IMPORTANT] 精确性边界
> 一个约分后的分数能否在基数 R 中有限表示，取决于分母是否整除某个 $R^k$。二进制中分母只能含因子 2；$1/3$ 与 $1/10$ 都无限循环，截断后的表示是近似值。

> [!example]- Number Base Conversion · 推导与例题
> **Derivation · 推导过程**
>
> **① base-$R$ → decimal：按位权求和**
>
> $$
> (N)_R=\sum_i a_iR^i
> \qquad\Longrightarrow\qquad
> (N)_{10}=\sum_i a_i\times R^i
> $$
>
> - 意义：每一位的"面值" = 该位**数码 × 该位权**，各位面值相加就是数值。这是位权制的定义式，
>   不需要任何技巧，只需要会算 $R^i$。
> - 数值校验（三个进制各一例，讲义 p.10 / p.15 / p.16）：
>   $(10011)_2=1\times16+0\times8+0\times4+1\times2+1\times1=19$ ✓；
>   $(2374)_8=2\times512+3\times64+7\times8+4\times1=1024+192+56+4=1276$ ✓；
>   $(E5)_{16}=14\times16+5\times1=224+5=229$ ✓（注意 $E=14$，不是 5 也不是 15）。
>
> **② decimal → base-$R$：为什么"第一个余数就是 LSB"**
>
> 设 $N=a_{n-1}R^{n-1}+a_{n-2}R^{n-2}+\dots+a_1R+a_0$，两边对 $R$ 取余——除 $a_0$ 外每项都含因子 $R$：
>
> $$
> N \bmod R=a_0,
> \qquad
> \left\lfloor \frac{N}{R}\right\rfloor=a_{n-1}R^{n-2}+\dots+a_1
> $$
>
> - 意义：**一次除法就把最低位 (LSD) 挤出来**，商正好是"把 $N$ 右移一位"的结果；把商当新的 $N$
>   重复，依次得到 $a_1,a_2,\dots$，所以**第一个余数是 LSB，最后得到的余数是 MSB**。
> - 数值校验（$53_{10}\to$ 二进制，讲义 p.12）：$53=2\times26+\mathbf{1}$、$26=2\times13+\mathbf{0}$、
>   $13=2\times6+\mathbf{1}$、$6=2\times3+\mathbf{0}$、$3=2\times1+\mathbf{1}$、$1=2\times0+\mathbf{1}$。
>   余数按产生顺序是 $1,0,1,0,1,1$（LSB → MSB），**倒过来读**得 `110101`；
>   回代 $1\times32+1\times16+0\times8+1\times4+0\times2+1=53$ ✓
> - 同一题的**法一**（找最大的 $2$ 的幂相减）：$53-32=21$、$21-16=5$、$5-4=1$、$1-1=0$，
>   用到的幂是 $32,16,4,1$ 即 $2^5,2^4,2^2,2^0$ → `110101` ✓。两种方法必须吐出**同一个串**。
>
> **②' 小数部分：反复乘以 $R$ 取整数位**
>
> 设 $F=0.a_{-1}a_{-2}\dots$，则 $F\times R=a_{-1}+0.a_{-2}a_{-3}\dots$：乘 $R$ 把小数点右移一位，
> **整数部分就是下一位小数位**，剩下的纯小数继续乘。
>
> - 意义：整数段用除法"从 LSB 往上剥"，小数段用乘法"从 MSB 往右剥"，方向正好相反。
> - 数值校验（$0.6875_{10}$，自算）：$0.6875\times2=\mathbf{1}.375$、$0.375\times2=\mathbf{0}.75$、
>   $0.75\times2=\mathbf{1}.5$、$0.5\times2=\mathbf{1}.0$ → 取整得 $0.1011_2$；
>   回代 $2^{-1}+2^{-3}+2^{-4}=0.5+0.125+0.0625=0.6875$ ✓（余数到 0，说明这次**转完了**）。
>
> **③ base-$2^k$ ↔ binary：分组即转换**
>
> 因为 $8=2^3$、$16=2^4$，一个八进制位正好覆盖 3 个二进制位的**全部** $2^3=8$ 种组合，
> 十六进制位覆盖 $2^4=16$ 种。所以"一个 3-bit 组读出的十进制值"**就是**那一位八进制数码。
>
> **整数部分从 binary point 向左每 $k$ 位一组，最左不足时补 0；小数部分从点向右分组，最右不足时补 0。**
>
> - 意义：分组法把 $O(n)$ 次幂运算换成 $O(n/k)$ 次查表，这是八 / 十六进制便于阅读二进制位串的主要原因之一
>   （讲义 p.22：压缩二进制）。
> - 数值校验（讲义 p.20 原文例子）：$(1100\,1010\,0101\,0111)_2$ 按 4-bit 分组 $1100\to C$、
>   $1010\to A$、$0101\to 5$、$0111\to 7$ → $CA57_{16}$；按 3-bit 分组（左侧补两个 0）$001\to1$、
>   $100\to4$、$101\to5$、$001\to1$、$010\to2$、$111\to7$ → $145127_8$。
>   两条路同值：`0xCA57` $=51799=$ `0o145127` ✓
>
> ![[base-conversion-grouping.svg]]
> *图 1 — 同一串 16 位二进制 `1100 1010 0101 0111` 的两种读法：按 4 位分组得 `CA57`，
> 按 3 位分组（最左不足 3 位，补两个 0）得 `145127`。(b) 面板单独强调"最左一组补 0"——
> 本图只含整数，所以从右往左分组；小数部分应从点向右分组。*
>
> **④ base-$R$ → base-$S$：以 decimal 为中枢**
>
> 任意 $R$ 到 $S$ 的转换可通过位权值、整数除法/小数乘法完成，也可在目标进制中直接累积。
> 这里选择 decimal 作为便于人工核算的中间表示，并非理论上必须先写成十进制：
>
> $$
> (N)_R \xrightarrow{\ \text{①按位权求和}\ } (N)_{10} \xrightarrow{\ \text{②反复除以 }S\ } (N)_S
> $$
>
> - 意义：十进制是所有进制的**通用接口 (pivot)**，这也是人类只需要一套十进制直觉的原因。
> - 数值校验：$(7526)_8\to$ 十六进制。按位权求和：$7\times512+5\times64+2\times8+6=3584+320+16+6=3926$；
>   再反复除以 16：$3926=16\times245+\mathbf{6}$、$245=16\times15+\mathbf{5}$、$15=16\times0+\mathbf{15}(F)$
>   → 余数顺序 $6,5,F$ → $F56_{16}$ ✓
>   捷径复核（两边都是 2 的幂，可直接分组）：$(7526)_8=$ `111 101 010 110`，重新按 4 位分组
>   `1111 0101 0110` $=F56_{16}$ ✓。位权易错：$8^3=512$，$7\times512=3584$ 才是最高位的面值。
>
> **什么时候可以跳过十进制**
> 只要 $R$ 与 $S$ **都是 2 的幂**，就可以先把 $R$ 展开成二进制、再按 $S$ 重新分组，完全不用碰十进制。
> 经过十进制是便于手算的通用路线，不是数学上唯一的转换算法。
>
> **Worked Example · 例题**
>
> **Example 1 — $53_{10}\to$ 二进制（讲义 p.12，两种方法都要会）**
>
> 题目：把 $(53)_{10}$ 写成二进制。已知 $2^5=32\le53<64=2^6$，结果不超过 6 位。
>
> 解一（找最大的 $2$ 的幂相减）：$2^5=32$ 放得下 → $53-32=21$；$2^4=16$ 放得下 → $21-16=5$；
> $2^3=8$ 放不下 → 该位 0；$2^2=4$ 放得下 → $5-4=1$；$2^1=2$ 放不下 → 该位 0；$2^0=1$ 放得下 → $1-1=0$。
> 位串：$2^5\,2^4\,2^3\,2^2\,2^1\,2^0=1\,1\,0\,1\,0\,1$ → `110101`。
>
> 解二（反复除以 2 取余）：$53/2=26$ 余 **1** → $26/2=13$ 余 **0** → $13/2=6$ 余 **1** →
> $6/2=3$ 余 **0** → $3/2=1$ 余 **1** → $1/2=0$ 余 **1**。
> 余数按产生顺序是 `1 0 1 0 1 1`（LSB → MSB），**倒序读**得 `110101`。
>
> **数值校验 (Numerical check)**：$1\times32+1\times16+0\times8+1\times4+0\times2+1=53$ ✓；
> 两种方法给出同一串 `110101` ✓；$2^5\le53<2^6$ 与"结果 6 位"一致 ✓。
>
> **Example 2 — $359_{10}\to$ 八进制、$650_{10}\to$ 十六进制（讲义 p.17 / p.18）**
>
> 解：$359=8\times44+\mathbf{7}$、$44=8\times5+\mathbf{4}$、$5=8\times0+\mathbf{5}$ → 余数顺序 $7,4,5$
> → $(547)_8$；$650=16\times40+\mathbf{10}$、$40=16\times2+\mathbf{8}$、$2=16\times0+\mathbf{2}$
> → 余数顺序 $10,8,2$，其中 $10$ 写作 `A` → $(28A)_{16}$。
>
> **数值校验 (Numerical check)**：$5\times64+4\times8+7=320+32+7=359$ ✓；
> $2\times256+8\times16+10=512+128+10=650$ ✓；位数自检 $8^2\le359<8^3$ → 3 位八进制 ✓，
> $16^2\le650<16^3$ → 3 位十六进制 ✓。
>
> **Example 3 — 小数 $0.6875_{10}\to$ 二进制（自算）**
>
> 解（反复乘以 2 取整数位）：$0.6875\times2=1.375$ → 取整 **1**，余 $0.375$；
> $0.375\times2=0.75$ → 取整 **0**，余 $0.75$；$0.75\times2=1.5$ → 取整 **1**，余 $0.5$；
> $0.5\times2=1.0$ → 取整 **1**，余 $0$，**停止**。按顺序读：$0.1011_2$。
>
> **数值校验 (Numerical check)**：$2^{-1}+2^{-3}+2^{-4}=0.5+0.125+0.0625=0.6875$ ✓；
> 第 4 步余数变成 0，说明该数在二进制下**有限**（分母 $16=2^4$）✓。
> 反例：$0.1_{10}$ 永远乘不到 0，只能截断——小数转换必须说明"取几位"。
>
> **Example 4 — $(1101\,0110)_2$ 的三路复核**
>
> 解：**→ 十进制** $128+64+16+4+2=214$；**→ 十六进制**（4 bit 一组，从右往左）`1101`$=D$、`0110`$=6$
> → $D6_{16}$；**→ 八进制**（3 bit 一组，最左补 0）`011`$=3$、`010`$=2$、`110`$=6$ → $326_8$。
>
> **数值校验 (Numerical check)**：$D6_{16}=13\times16+6=214$ ✓；$326_8=3\times64+2\times8+6=192+16+6=214$ ✓；
> 三条路给出同一个值 214，即 `0xD6` $=$ `0o326` $=$ `214` ✓。
>
> **Conversion, encoding, and approximation · 转换、编码与近似**
>
> A radix conversion preserves the mathematical value. Changing an encoding, such as binary to BCD, preserves a specified semantic value but uses a different code structure. Truncating or rounding a fractional expansion can change the value. These three operations must not be described as if they were interchangeable.
>
> A reduced rational fraction $p/q$ has a terminating base-$R$ expansion exactly when every prime factor of $q$ is also a prime factor of $R$. In binary, the reduced denominator must be a power of two. This explains why $3/8$ terminates and $1/10$ repeats. The denominator test is a mathematical criterion; it does not assume any particular computer format.
>
> **Worked application — a repeating fraction.** 将 $0.2_{10}=1/5$ 转二进制，连续乘 2：0.4→0，0.8→0，1.6→1（留 0.6），1.2→1（留 0.2）。余数回到 0.2，故 $0.2=0.00110011\ldots_2$。保留 8 位并截断得 $0.00110011_2=51/256=0.19921875$，误差为 $0.00078125<2^{-8}$。
>
> In English: the recurrence of the same fractional remainder proves repetition. Eight-bit truncation retains the first eight fractional bits and always rounds a nonnegative value downward. Rounding to nearest uses the omitted bits as well and has a different error bound.
>
> **English exam question:** Why can an exact decimal fraction become an inexact binary fraction?
>
> **Answer:** Termination depends on the radix. A denominator containing a factor of five cannot divide a power of two, so its binary expansion repeats. A finite binary register must then approximate it, even when the decimal notation is short.
>
> Use this reasoning in [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度|Fixed-Point Numbers]] and [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|Floating-Point Numbers]]. When reading [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]], distinguish conversion of a type from a numeric resize or a change of scaling.

## 4 · Bits and Bytes · 位宽与容量

N 位有 $2^N$ 种模式，N 位无符号整数范围 $0\ldots2^N-1$；表示 M 种状态至少需要 $\lceil\log_2M\rceil$ 位。一个 byte 是 8 bit，一个 nibble 是 4 bit。

容量 = 深度（word 数）× 位宽（bit/word）。地址数、bit 数、byte 数需分别说明。SI 的 k/M 与二进制 Ki/Mi 分开计算，不能默认为相同倍率。

> [!example]- Bits and Bytes · 推导与例题
> **Derivation · 推导过程**
>
> **① 为什么是 $2^N$ 个码字：每一位翻一倍**
>
> $N$ 位的位型总数 $C(N)$ 满足 $C(N)=2\cdot C(N-1)$（新增的最高位可以取 0 或 1 两种，
> 其余 $N-1$ 位保持不动），而 $C(1)=2$（`0` / `1`），于是
>
> $$
> C(N)=2^{N},
> \qquad
> \text{range}=[0,\;2^{N}-1]
> $$
>
> - 意义：容量按指数增长（**每加一位，容量翻倍、范围上限翻倍再加一**）；范围从 0 开始，
>   所以最大值比容量小 1。
> - 数值校验（讲义 p.13 的两个例子）：3 位十进制 → $10^3=1000$ 个值、范围 $[0,999]$；
>   3 位二进制 → $2^3=8$ 个值、范围 $[0,7]$，即 `000` 到 `111` ✓。
>   再验一组：4 位 → $2^4=16$、$[0,15]$；8 位 → $2^8=256$、$[0,255]$ ✓（与下表一致）。
>
> **② nibble / byte 与十六进制是"同一件事"**
>
> 因为 $2^4=16$，**4 个二进制位的全部组合正好等于一位十六进制数码的 16 个取值**；
> 两个 nibble 拼起来就是 1 byte：
>
> $$
> 1\ \text{hex digit}=4\ \text{bit}=1\ \text{nibble},
> \qquad
> 2\ \text{hex digits}=8\ \text{bit}=1\ \text{byte}
> $$
>
> - 意义：十六进制是给人看的二进制缩写；**看到 1 byte 就写 2 位十六进制**是硬件文档的通用写法
>   （内存地址、`#RRGGBB` 颜色码、机器码）。
> - 数值校验：$1\ \text{byte}=2^8=256$ 个值，写成十六进制正好是 `00`–`FF`：从 `0x00` 数到 `0xFF`
>   是 $255-0+1=256$ 个 ✓；`0xFF` $=15\times16+15=255=2^8-1$ ✓（最大值再次比容量小 1）。
>
> **③ 大幂次的速记：$2^{10}\approx10^{3}$**
>
> $$
> 2^{10}=1024\approx10^{3}
> \qquad\Longrightarrow\qquad
> 2^{10k}\approx10^{3k}
> $$
>
> - 意义：把"二进制指数"换算成"十进制数量级"，这是估算一切存储容量的唯一工具
>   （讲义 p.25 的 kilo/mega/giga/tera/peta/exa）。
>
> | 名称 (SI 词头) | 幂 | 精确值 | 近似 |
> |---|---|---|---|
> | kilo | $2^{10}$ | $1\,024$ | $\approx10^{3}$ |
> | mega | $2^{20}$ | $1\,048\,576$ | $\approx10^{6}$ |
> | giga | $2^{30}$ | $1\,073\,741\,824$ | $\approx10^{9}$ |
> | tera | $2^{40}$ | $1\,099\,511\,627\,776$ | $\approx10^{12}$ |
> | peta | $2^{50}$ | $1\,125\,899\,906\,842\,624$ | $\approx10^{15}$ |
> | exa | $2^{60}$ | $1\,152\,921\,504\,606\,846\,976$ | $\approx10^{18}$ |
>
> - 近似误差可算：$2^{10}/10^{3}=1.024$，所以 $2^{10k}\approx1.024^{k}\times10^{3k}$。
>   $k=6$（exa）时 $1.024^{6}=1.1529$，即 $2^{60}$ 比 $10^{18}$ **高 15.3%** ——
>   数量级够用，容量对账就会出事。
>
> ![[powers-of-two-scale.svg]]
> *图 1 — 对数横轴上的 $2^{10}$–$2^{60}$：每个刻度给出幂、SI 词头、精确十进制值与对应的 IEC 前缀；
> 下方两个红色标记是讲义 p.26 要求"心算"的估算点 $2^{24}\approx16$ M 与 $2^{32}\approx4$ G。
> 横轴上相邻刻度相差约 3 个数量级，密集的位数在对数尺上其实**很稀疏**——这正是"用指数思考"的原因。*
>
> **④ IEC 与 SI：1024 与 1000 的制度性分歧**
>
> - **SI 词头**（kB、MB、GB、TB）按 1000 进位：$1\ \text{kB}=1000\ \text{B}$；
> - **IEC 词头**（KiB、MiB、GiB、TiB）按 1024 进位：$1\ \text{KiB}=1024\ \text{B}=2^{10}\ \text{B}$。
> - 后果：标称 $1\ \text{TB}$ 的硬盘有 $10^{12}\ \text{B}=10^{12}/2^{40}=0.9095\ \text{TiB}$，
>   在按 1024 计数的系统里显示为 $10^{12}/2^{30}=931.3\ \text{GiB}$ —— 这就是"买来 1 TB 只剩 931 GB"
>   的全部原因（**不是厂商偷工减料，是两套词头混用**）。
>
> **⑤ 两个必背估算点（讲义 p.26）**
>
> $$
> 2^{24}=2^{4}\times2^{20}=16\times1\,048\,576=16\,777\,216\approx16\ \text{M}
> $$
> $$
> 2^{32}=2^{2}\times2^{30}=4\times1\,073\,741\,824=4\,294\,967\,296\approx4.29\ \text{G}
> $$
>
> - 意义：$2^{24}\approx16$ M 用来估"24 位能寻址多少"（16 MB / 16 M 色）；
>   $2^{32}\approx4$ G 用来估 32 位系统：**32 位无符号整数最大 $=2^{32}-1=4\,294\,967\,295$**，
>   **32 位地址空间 $=2^{32}$ 字节 $=4$ GiB**。
> - 数值校验：$16\times1\,048\,576=16\,777\,216$ ✓（$\approx16.78$ M）；
>   $4\times1\,073\,741\,824=4\,294\,967\,296$ ✓（$\approx4.29$ G）；
>   $4\,294\,967\,296-1=4\,294\,967\,295$ ✓（最大值 = 容量 $-1$，又一次 off-by-one）。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.24 的填空三连**
>
> 题目：byte 是几位？能表示多少个值？范围是多少？nibble 呢？一个二进制位叫什么？
> 一个十六进制数码等于几个 bit、几个 nibble？两个十六进制数码等于几个 byte？
>
> 解：
> 1. **byte = 8 bit** → $2^{8}=256$ 个值 → 范围 $[0,255]$（写成十六进制 `00`–`FF`）。
> 2. **nibble = 4 bit** → $2^{4}=16$ 个值 → 范围 $[0,15]$（正好一位十六进制数码）。
> 3. **一位二进制位 = 1 bit**；**一位十六进制数码 = 4 bit = 1 nibble**；**两位十六进制数码 = 1 byte**。
>
> **数值校验 (Numerical check)**：$2^{4}=16$ ✓、$2^{8}=256$ ✓；最大值 $255=2^{8}-1$ ✓；
> `0xFF` 展开 $=1111\,1111_2=128+64+32+16+8+4+2+1=255$ ✓；4 bit 与 1 位 hex 位数匹配 ✓。
>
> **Example 2 — 估算 $2^{24}$ 与 $2^{32}$（讲义 p.26）**
>
> 题目：不查表，说出 $2^{24}$ 与 $2^{32}$ 各约等于多少；32 位无符号整数能表示到多大？
> 32 位地址空间有多大？
>
> 解：
> 1. $2^{24}=2^{4}\times2^{20}\approx16\times10^{6}=16$ M，精确值 $16\,777\,216$。
> 2. $2^{32}=2^{2}\times2^{30}\approx4\times10^{9}=4$ G，精确值 $4\,294\,967\,296$。
> 3. 32 位无符号整数范围 $[0,\,4\,294\,967\,295]$（最大 $=2^{32}-1$）。
> 4. 32 位地址空间 $=2^{32}$ 字节 $=4\,294\,967\,296\ \text{B}=4$ GiB。
>
> **数值校验 (Numerical check)**：$2^{30}\times4=1\,073\,741\,824\times4=4\,294\,967\,296$ ✓；
> $4\,294\,967\,296/2^{30}=4$ GiB ✓；估算值 16 M / 4 G 与精确值同数量级（误差 $<10\%$）✓。
>
> **Example 3 — 一个 16 位计数器能数到多少？**
>
> 题目：一个 16 位无符号计数器从 0 开始每来一个时钟加 1。它能表示多少个不同的数？
> 溢出前最后一个数是什么？再加 1 会怎样？
>
> 解：
> 1. 容量 $2^{16}=65\,536$ 个状态，范围 $[0,\,65\,535]$。
> 2. 最后一个数 $=65\,535=$ `1111 1111 1111 1111` $=$ `FFFF`$_{16}$。
> 3. 再加 1 得到 `1 0000 0000 0000 0000`，第 17 位放不进 16 位寄存器 → 低 16 位全 0，
>    计数器回绕到 **0**（这就是溢出 / overflow）。
>
> **数值校验 (Numerical check)**：$2^{16}=65\,536$ ✓；$65\,535=65\,536-1$ ✓；
> `FFFF`$_{16}=15\times4096+15\times256+15\times16+15=61\,440+3840+240+15=65\,535$ ✓；
> 回绕等价于 $\bmod 2^{16}$：$65\,536 \bmod 65\,536=0$ ✓。
>
> **Width, capacity, and addressing · 位宽、容量与寻址**
>
> The expression $2^N$ counts patterns, not automatically numbers, bytes, or addresses. Its meaning depends on what the $N$ bits represent. An $N$-bit unsigned word contains $2^N$ possible values. An $N$-bit address selects $2^N$ locations. If each location contains $W$ bits, total capacity is $2^N W$ bits.
>
> “Byte-addressable” means that consecutive addresses refer to consecutive bytes. “Word-addressable” means that an address selects a whole word. Never infer one from the other merely because the data bus has eight or sixteen wires. Capacity notation should identify both the number of words and the bits per word.
>
> **Worked application — memory size.** 一个 $256\times16$ memory 有 256 个 word，每个 16 bit。地址线需 8 根，数据线需 16 根，容量 $256\times16=4096$ bit=$512$ byte。若改成 $512\times8$，总容量相同，但地址变为 9 位、数据为 8 位。相同总容量不意味着相同接口。
>
> In English: depth determines the address width, and word width determines the data interface. The first device has 256 addressable words; calling it “512 addresses” would confuse byte capacity with word count.
>
> **English exam question:** How many bits are needed to encode twenty distinct states?
>
> **Answer:** At least five bits, because four bits provide only 16 codes whereas five provide 32. Twelve of those codes are unused under a compact binary encoding. They still exist physically and require a stated policy if recovery matters.
>
> This counting argument leads directly to [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]], [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]], and [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]]. It is also the first width check to make in [[Structural Shift Register Project]].

## 5 · 典型校验与下一步

转换后用原进制的位权展开复核；16 进制一位对应四个 bit，不改变数值也不等于四字节。掌握位宽后进入 [[Binary Arithmetic and Signed Representation]]；编码规则另见 [[Data Coding and Character Representation]]。

## Sources · 课件依据

主线课件：[Ch2 lecture](../ECE2050-Chap2.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
