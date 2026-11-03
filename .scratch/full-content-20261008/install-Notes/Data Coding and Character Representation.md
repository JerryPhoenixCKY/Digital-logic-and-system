---
tags:
  - ECE2050
  - codes
date: 2026-09-16
updated: 2026-10-09
chapter: Ch2
aliases:
  - 数据编码与字符表示
  - Data Coding and Character Representation
  - 数据编码与字符表示 · Ch2
  - Binary Coded Decimal
  - BCD 码
  - 二-十进制编码
  - 8421 码
  - BCD
  - Gray Code
  - 格雷码
  - 格雷编码
  - 循环码
  - Reflected Binary Code
  - American Standard Code for Information Interchange
  - ASCII 码
  - 美国信息交换标准代码
  - 字符编码
  - ASCII
---

# Data Coding and Character Representation · 数据编码与字符表示

> [!SUMMARY] Quick recall · 英文速览
> A code assigns bit patterns to meanings. BCD preserves decimal digits, Gray code preserves one-bit adjacency, and ASCII assigns codes to characters.

## 1 · 编码与数制：先决定位串的含义

数据编码 (data coding) 不是简单换进制。一个位串表示数值、逐个十进制数字或字符，需要不同的解释器；合法输入集合也随编码改变。

### 编码目的决定合法集合与解码规则

字母数字编码 (alphanumeric code) 将字母、数字字符、标点或控制动作映射为位串；数值编码则定义位串到数值的映射。BCD 存**各十进制数字**，ASCII 存**字符符号**，Gray 选择**相邻顺序**。编码并不会自动带来纠错能力。

| 语义为“5”的不同对象 | 存储表示 | 使用前需确认 |
|---|---|---|
| 无符号数值 5 | 例如 8 位 `0000 0101` | 位宽与 unsigned |
| BCD 数字 5 | `0101` | 8421 数字组及其十进制位置 |
| ASCII 字符 `'5'` | 七位 `0110101`，字节为 `0x35` | 字符编码与容器宽度 |
| 自然 binary 值 5 的 reflected Gray 码 | 4 位 `0111` | Gray 对应关系及位宽 |

数制转换使同一数学值的基数写法改变；编码转换还要选择目标字段与合法集，例如 binary 13=`1101`、BCD 13=`0001 0011`、ASCII 字符串 `"13"` 为 `0x31 0x33`，三者不能共用一个整串位权读法。

## 2 · Binary Coded Decimal · 十进制数字逐位编码

8421 BCD 用每四位表示一个十进制数字；0000–1001 合法，1010–1111 非法。十进制 14 编码为 `0001 0100`，而纯二进制 14 为 `1110`。

BCD 加法的每个数字先二进制相加；若和大于 9 或产生四位进位，则加 0110 校正。原因是 16 个二进制码中只使用 10 个，十进制进位需跳过 6 个码。

### 完整 BCD 表、适用条件与逐组流程

这里的 BCD 指 **8421 BCD**；一组四位的内部数值为 $d=8b_3+4b_2+2b_1+b_0$，$b_i\in\{0,1\}$，且必须 $0\le d\le9$。

| 十进制数字 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| 8421 | 0000 | 0001 | 0010 | 0011 | 0100 | 0101 | 0110 | 0111 | 1000 | 1001 |

`1010,1011,1100,1101,1110,1111` 是未分配给十进制数字的六个组码。$n$ 位十进制数字需 $4n$ bit；每组合法码利用率 $10/16=62.5\%$，整个 n 组的合法比例是 $(10/16)^n$。170 要 12 位 BCD，纯二进制只需 8 位。BCD 不自带符号或小数点位置，必须由字段格式另行约定；它方便十进制显示和逐位算术，但并非这些任务唯一可用的编码。

组间数值是 $\sum_j d_j10^j$，**不是** $\sum_j d_j16^j$；同串 `0001 0111 0000` 的 BCD 是 170，unsigned 是 368。8421 每组有权不等于整串具有普通二进制位权。

**编解码。** 编码逐个十进制数字查四位表并按原顺序并排；解码先确认整体四位对齐，再逐组检查 0–9，不能把非法组“照权值算出 13”当合法数字。固定字段需要保留高位零组；完整已对齐的字段从左或从右每四位切组都相同。

**每组加法。** 设两数字 a,b 与低位十进制 carry-in $c\in\{0,1\}$，保留完整五位和 $t=a+b+c$（0–19）。若 $t\ge10$，输出数字 $d=t-10$、carry-out=1；否则 $d=t$、carry-out=0。电路先得四位结果 $s_3s_2s_1s_0$ 和二进制进位 $c_4$，校正条件为

$$K=c_4\lor\bigl[s_3\land(s_2\lor s_1)\bigr].$$

K=1 时低四位加 `0110`，十进制进位为 K，继续传向高一组。若第一阶段已有 $c_4=1$，第二阶段加 6 **未必再次产生进位**，仍须保留原十进制进位。例如 $9+9=18$，第一阶段 `1 0010`，低位 `0010+0110=1000`，输出 `0001 1000`；不能因第二阶段 carry=0 而丢掉十位 1。

从最低组向最高组处理，最后解码回十进制复核。$3+4=7$ 已合法不能加 6；$13+27=40$ 应得 `0100 0000`，整串普通二进制加法得到 `0011 1010` 是错误流程。

**Exam English.** “Encode each decimal digit separately in four bits. Correct a digit sum when it exceeds nine or produces a binary carry. The decimal carry must include the first-stage carry; the corrected digit alone is insufficient.”

> [!example]- Binary Coded Decimal · 推导与例题
> **图示与讲义依据**
>
> ![[bcd-8421-encoding.svg]]
> *图 1 — (a) 0–15 全部 16 个 4 位码字：前 10 个（`0000`–`1001`）是合法 BCD 数字，后 6 个（`1010`–`1111`）
> 是非法码，列头标出各位权值 8/4/2/1。(b) 十进制 → BCD 是**逐位翻译**：$170$ 的 3 个数字变成 3 个 4 位组
> `0001 0111 0000`，$2469$ 的 4 个数字变成 4 个 4 位组 `0010 0100 0110 1001`。*
>
> **Derivation · 推导过程**
>
> **1. 十进制 → BCD：逐位翻译，没有除法、没有进位**
>
> $$
> (d_{n-1}d_{n-2}\dots d_1d_0)_{10} \;\longrightarrow\; \mathrm{BCD}(d_{n-1}) \,\|\, \mathrm{BCD}(d_{n-2}) \,\|\, \dots \,\|\, \mathrm{BCD}(d_0)
> $$
>
> - 意义：每个数字独立查上面那张表，**高位数字的 4 位在左边**；翻译过程不影响邻居，也不产生进位。
> - 数值校验：$170 \to 1|7|0 \to 0001\,|\,0111\,|\,0000$ = `0001 0111 0000` ✓；
>   $2469 \to 2|4|6|9 \to 0010\,|\,0100\,|\,0110\,|\,1001$ = `0010 0100 0110 1001` ✓。
> - 与 [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|Number Base Conversion]] 的对比：那里要"反复除以 2"或"找最大的 $2^k$"，因为整个数是一个**数值**；
>   这里没有数值运算，只有 10 项查表。
>
> **2. BCD → 十进制：从右往左每 4 位一组（讲义 p.65）**
>
> - 从**最右**开始，每 4 位一组（*Starting from the right-most bit and divide the code into groups of four bits*）；
> - 每组查 8421 表得到一个 0–9 的数字，按顺序拼起来就是十进制数；
> - 若任何一组 `> 1001`，这串码就不是合法 BCD（要么写错，要么数据出错）。
> - 数值校验：`0010 0100 0110 1001` → 2、4、6、9 → $2469$ ✓；
>   `0001 0111 0000` → 1、7、0 → $170$ ✓。
>
> **3. 为什么要加 6：6 个被跳过的码字**
>
> BCD 数数的方式与二进制不同（以一个 nibble 为单位）：
>
> | 计数 | … | 8 | 9 | 10 | 11 | … |
> |---|---|---|---|---|---|---|
> | BCD | … | `1000` | `1001` | `0001 0000` | `0001 0001` | … |
> | 纯二进制 | … | `1000` | `1001` | `1010` | `1011` | … |
>
> 二进制加法器并不知道"BCD 在 `1001` 之后要跳过 6 个码字"：它从 `1001` 加 1 直接得到 `1010` 继续数下去。
> 于是当一组 nibble 的真值 $s \ge 10$ 时，二进制算出的进位权重是 **16**，而十进制要的进位权重是 **10** ——
> 两者正好差 6（这 6 就是被跳过的 `1010`…`1111`）。把这个差补上，两边就对齐了：
>
> $$
> s + 6 \;=\; 16 + (s-10) \qquad (10 \le s \le 19)
> $$
>
> - 意义：$+0110$ 把"非法的 4 位和"变成"**进到下一位十进制数字的 1** + 正确的数字 $s-10$"。
> - 数值校验：$s = 13$：$13+6 = 19 = 16+3$ → 进位 1、数字 3，正是 $8+5 = 13$ 的 `0001 0011` ✓；
>   $s = 18$：$18+6 = 24 = 16+8$ → 进位 1、数字 8，正是 $9+9 = 18$ 的 `0001 1000` ✓。
> - 反过来看更直白：$16-10 = 6$，就是每个 nibble 被跳过的码字个数 ✓。
>
> **讲义 p.66 的第 2 条要补一句**
> 讲义写 *If a 4-bit sum $\le 9$ → Valid BCD number*，严格说还要**同时看有没有进位出组**：
> 只要这一组产生了进位，即使低 4 位 $\le 1001$ 也必须 $+0110$。
> 反例就是 $9+9$：二进制和 `1 0010` 的低 4 位是 `0010`（看起来合法），
> 但直接读成"1 和 2"得到 12，正确答案是 18 —— 补上 $+0110$ 后 `0010` 变 `1000` ✓。
>
> **4. 多位 BCD 的进位传播**
>
> 每一组独立判定、独立修正；该组的十进制进位（初始二进制 carry 或校正阶段 carry）送到**左边相邻的那一组**
> （也就是更高一位的十进制数字）。
>
> 数值校验 $27 + 15$：
>
> 1. 个位组：`0111 + 0101 = 1100`（$=12 > 9$）→ `1100 + 0110 = 1 0010` → 个位 = 2，进位 = 1；
> 2. 十位组：`0010 + 0001 + 1(进位) = 0100`（$=4 \le 9$，合法，**不修正**）→ 十位 = 4；
> 3. 结果 `0100 0010` → 4 和 2 → $42$；而 $27+15 = 42$ ✓。
>
> ![[bcd-addition-correction.svg]]
> *图 2 — 两列并排的 BCD 加法修正过程。(a) $8+5$：二进制和 `1101` 命中非法码（$13 > 9$），
> 判定点在这里，加 `0110` 后得到 `1 0011` → `0001 0011` = 13。(b) $9+9$：这一组**有进位出组**，
> 同样是判定点；低 4 位 `0010` 看着合法，加 `0110` 后才是 `1000` → `0001 1000` = 18。
> 两例的 $+0110$ 之所以是 **6**，正是因为 BCD 跳过了 6 个码字。*
>
> **Worked Example · 例题**
>
> **Example 1 — 把 170 与 2469 编码成 BCD（讲义 p.65）**
>
> 题目：写出 $170_{10}$ 与 $2469_{10}$ 的 8421 BCD 码，并说明各占多少位。
>
> 解：逐位查表并并排 —— $170$：1, 7, 0 → `0001 0111 0000`（$3\times4 = 12$ 位）；
> $2469$：2, 4, 6, 9 → `0010 0100 0110 1001`（$4\times4 = 16$ 位）。
>
> **数值校验 (Numerical check)**：
> - 反读：`0001` → 1，`0111` → $4+2+1 = 7$，`0000` → 0，拼起来 $170$ ✓；
>   `0010` → 2，`0100` → 4，`0110` → $4+2 = 6$，`1001` → $8+1 = 9$，拼起来 $2469$ ✓。
> - 位宽校验：12 位 = 3 个 nibble ✓；16 位 = 4 个 nibble ✓；没有任何一组 > `1001` ✓。
> - 与二进制对照：$170_{10} = 1010\,1010_2$（8 位），BCD 要 12 位；
>   $2469_{10} = 1001\,1010\,0101_2$（12 位），BCD 要 16 位 —— BCD 更长，这是它的代价 ✓。
>
> **Example 2 — $8+5$ 的 BCD 加法与 $+6$ 修正（讲义 p.66）**
>
> 题目：用 BCD 计算 $8+5$。
>
> 解：
> 1. 编码：$8 \to$ `1000`，$5 \to$ `0101`。
> 2. 按二进制相加：`1000 + 0101 = 1101`（这一步不产生进位）。
> 3. 判定：$1101 = 13 > 1001$（9），是 6 个非法码之一 → 必须修正。
> 4. 修正：`1101 + 0110 = 1 0011`（$13 + 6 = 19 = 16+3$）。
> 5. 分组：新出现的进位 1 是十位数字，`0011` 是个位数字 → 结果 `0001 0011`。
>
> **数值校验 (Numerical check)**：
> - 解码结果：`0001 0011` → 1 和 3 → $13$ ✓，与 $8+5 = 13$ 一致 ✓。
> - 修正算式：$s+6 = 13+6 = 19 \ge 16$ → 进位 1、数字 $19-16 = 3$ ✓；若不加 6，`1101` 既不是合法 BCD 码也读不出 13 ✓。
>
> **Example 3 — $9+9$：有进位时也要修正（自算，讲义只给了 $8+5$）**
>
> 题目：用 BCD 计算 $9+9$，并说明为什么"低 4 位 ≤ 9 就合法"是不完整的。
>
> 解：
> 1. 编码：`1001`、`1001`。
> 2. 二进制相加：`1001 + 1001 = 1 0010`（这一组**有进位出组**，低 4 位是 `0010`）。
> 3. 判定：有进位 → 仍然要修正（即使 `0010` 看上去合法）。
> 4. 修正：`1 0010 + 0110 = 1 1000`（$18+6 = 24 = 16+8$）。
> 5. 解码：进位 1 = 十位，`1000` = 8 → `0001 1000`。
>
> **数值校验 (Numerical check)**：
> - $9+9 = 18$ ✓，而结果 `0001 1000` 解码 = 1、8 = 18 ✓。
> - 不做修正会得到 "12"，与真值 18 恰好差 6（每个 nibble 跳过的码字数）✓；低 4 位从 `0010` 到 `1000` 也正好差 $0110$ ✓。
>
> **Example 4 — 合法性判断与多位进位传播**
>
> 题目 (a)：下列 4 位码哪些是合法 BCD：`0110`、`1010`、`1001`、`1111`、`0000`？
>
> 答：`0110`（6 ✓）、`1001`（9 ✓）、`0000`（0 ✓）合法；`1010`（10）与 `1111`（15）落在 `1010`–`1111` 区间 → 非法。
>
> 题目 (b)：用 BCD 计算 $27+15$，写出每一步的判定与进位。
>
> 解：
> 1. 个位组：`0111 + 0101 = 1100` = 12 > 9 → 修正 `1100 + 0110 = 1 0010` → 个位 2、进位 1；
> 2. 十位组：`0010 + 0001 + 1 = 0100` = 4 ≤ 9 → 合法，不修正 → 十位 4；
> 3. 结果 `0100 0010`。
>
> **数值校验 (Numerical check)**：`0100 0010` 解码 = 4、2 = 42，而 $27+15 = 42$ ✓；
> 两组都没有非法码 ✓。若把第一步漏掉的进位丢掉不算，十位会得到 `0011` = 3 → 32 ✗ —— 进位必须传播。
>
> **BCD validity and decimal carries · BCD 合法性与英文理解**
>
> Packed BCD places two decimal digits in one byte, but neither nibble may represent 10–15. A binary sum that produces such a nibble is an intermediate result rather than a valid BCD digit. The correction adds six because a four-bit binary column wraps at sixteen whereas a decimal digit must wrap at ten; the two radices differ by six.
>
> The correction condition uses both the four-bit sum and its carry-out. Checking only whether the low nibble exceeds nine misses sums such as $9+9=18$, whose low nibble is 2 even though a decimal carry is required. The corrected carry must feed the next decimal digit.
>
> **Worked application — multi-digit sum.** 计算 BCD $47+38$：个位 $7+8=15$，二进制中间 nibble `1111` 非法，加 `0110` 得 `1 0101`，个位 5、进到十位 1。十位 $4+3+1=8$，合法不用修正，故 `1000 0101`=85。校验 $47+38=85$；按普通二进制直接加 `0x47+0x38=0x7F`，不能当作合法 BCD。
>
> In English: correction is applied per decimal digit, starting at the least significant digit. A decimal carry is propagated once to the next digit. A legal intermediate nibble with no carry must be left unchanged.
>
> **English exam question:** May the six invalid BCD inputs be treated as don't-cares in a display decoder?
>
> **Answer:** Only when the input specification guarantees that those codes do not occur, or explicitly permits any output for them. If invalid digits must blank the display or signal an error, that behavior is part of the function and cannot be discarded during minimization.
>
> Continue with [[Seven-Segment Display and Code Conversion]], [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]], and [[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转|Cascaded Counters and Digital Clocks]]. For 0–9 counters, define the transition after 9 separately from the arithmetic correction.

## 3 · Gray Code · 相邻变化约束

格雷码 (Gray code) 的相邻码字仅一位变化。二进制位 $b_{n-1}\ldots b_0$ 转为格雷位：

$$g_{n-1}=b_{n-1},\quad g_i=b_{i+1}\oplus b_i;\qquad b_i=\bigoplus_{j=i}^{n-1}g_j.$$

也可写 $g=b\oplus(b\gg1)$。例如二进制 1011 得格雷码 1110。格雷码不按通常二进制位权直接相加；单比特相邻性也不保证任意异步多位传输安全。

### 汉明距离、反射构造与使用条件

等长码字 u,v 的**汉明距离 (Hamming distance)** 为不同位数：

$$d_H(u,v)=\sum_i(u_i\oplus v_i)=\operatorname{popcount}(u\oplus v).$$

此处求和是整数计数，$u_i,v_i\in\{0,1\}$。reflected binary Gray code 的指定相邻序列（含首尾回绕）满足 $d_H=1$，任意两码字不一定如此。也不能把一切数学上的 cyclic code 都等同于 Gray code。

| 序号 k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 四位 reflected Gray | 0000 | 0001 | 0011 | 0010 | 0110 | 0111 | 0101 | 0100 |

| 序号 k | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| 四位 reflected Gray | 1100 | 1101 | 1111 | 1110 | 1010 | 1011 | 1001 | 1000 |

**构造。** 从一位序列 `0,1` 起，对旧序列前半照原顺序加前缀 0，后半照反序加前缀 1。两半内部保留相邻性，中间只改前缀，首尾也只改前缀。完整 N 位 reflected Gray 与 N 位 binary 是一一对应，所有 $2^N$ 码字都有用途。

**编解码操作。** 先确定两端共同位宽和 reflected 编码 → binary 到 Gray 用逻辑右移（最高补 0），$g=b\oplus(b\gg1)$ → Gray 到 binary 最高位照抄，再从高到低用**已求得的 binary 高位**异或当前 Gray 位 → 正反往返复核。`0011` 解码得 `0010`=2，不能直接按 binary 读成 3；`1011` binary 编成 `1110` Gray，解码不能再次使用同一个右移公式。

**边界。** 单位距离优势要求物理变化或发送码字沿相邻序列进行；随机跳数可能同时改变多位。编码器可减少过渡读数歧义，通信星座图可使相邻符号误判只影响一位映射，K-map 用 Gray 排序保持相邻项只变一个变量。它不是检错／纠错码，也不保证任意异步总线直接采样安全；CDC 仍需满足编码生成、同步和时序约束。

**Exam English.** “Gray code guarantees a one-bit difference between consecutive code words in the specified sequence, not between every pair. Decode using prefix XOR before ordinary arithmetic. Its unit-distance property does not provide error correction.”

> [!example]- Gray Code · 推导与例题
> **图示与讲义依据**
>
> ![[gray-code-sequence.svg]]
> *图 1 — (a) 16 个码字依次排列（蛇形两行），每个间隔标出汉明距离，**全部是 1**；右侧竖箭头是
> $k=7 \to k=8$ 的衔接，左侧双向箭头是首尾相接（`1000` 回到 `0000`，同样只差 1 位）。(b) 对比计数时
> 每一位的翻转代价：自然二进制在进位处会一次翻多位（`0111 -> 1000` 一次翻 4 位），格雷码每一步恒为 1 位；
> 小方框给出反射构造法。*
>
> **Derivation · 推导过程**
>
> **1. 反射构造法 (reflection)：为什么相邻只差 1 位**
>
> $$
> G_1 = \texttt{0},\ \texttt{1};
> \qquad
> G_n = \underbrace{\texttt{0}\!+\!G_{n-1}}_{\text{原序列，前面加 0}}
> \ \Big\|\
> \underbrace{\texttt{1}\!+\!\mathrm{reverse}(G_{n-1})}_{\text{镜像，前面加 1}}
> $$
>
> - 意义：$n$ 位格雷码 = "前半段照抄 $n-1$ 位序列并在最高位补 0" + "后半段把 $n-1$ 位序列倒过来并在最高位补 1"。
> - 三处相邻关系都要成立，所以它必然只变 1 位：
>   ① 前半段内部：就是 $G_{n-1}$，按归纳假设只变 1 位；
>   ② 后半段内部：$G_{n-1}$ 的镜像，镜像不改变相邻距离，仍然只变 1 位；
>   ③ 接缝处：`0…` 与 `1…` 只差**新增的最高位**（后面的位是同一个 $G_{n-1}$ 的末项），$d = 1$ ✓。
> - 数值校验：$G_1 = 0, 1$ → $G_2 = \texttt{00},\texttt{01}\ |\ \texttt{11},\texttt{10}$ ✓（`01→11` 只差最高位）；
>   $G_3 = \texttt{000},\texttt{001},\texttt{011},\texttt{010}\ |\ \texttt{110},\texttt{111},\texttt{101},\texttt{100}$ ✓；
>   $G_4$ 就是本篇的 16 项序列表 ✓。
> - 首尾为什么也相连：$G_n$ 的第一项是 `00…0`，最后一项是 `10…0`（镜像的末项），只差最高位 → $d = 1$ ✓（循环性）。
>
> **2. 二进制 → 格雷码：$g = b \oplus (b \gg 1)$**
>
> $$
> g = b \oplus (b \gg 1), \qquad g_{N-1} = b_{N-1},\quad g_i = b_{i+1}\oplus b_i
> $$
>
> - 意义：每一位格雷码是"二进制本位"与"它左边一位"的异或 —— 相邻两位相同时写 0，不同时写 1；
>   最高位没有左邻，直接抄下来。
> - 为什么能消掉多位跳变：二进制计数在进位时（如 `0111 → 1000`）有多位同时翻转；
>   异或取"相邻位之差"后，**这一整串翻转在格雷码里只表现为最高位的一次翻转** ✓。
> - 数值校验：$b = 1011$：$b \gg 1 = 0101$，$1011 \oplus 0101 = 1110$ → $g = 1110$ ✓；
>   $b = 011$（3）：$011 \oplus 001 = 010$ → $g = 010$ ✓（与 verify 报告一致）。
>
> **3. 格雷码 → 二进制：前缀异或**
>
> $$
> b_{N-1} = g_{N-1}, \qquad b_i = b_{i+1} \oplus g_i
> \qquad\Longleftrightarrow\qquad
> b = g \oplus (g \gg 1) \oplus (g \gg 2) \oplus \cdots
> $$
>
> - 意义：从最高位往右逐位"累积异或"（prefix XOR）：每往右走一位，就把目前得到的二进制位与当前格雷位异或一次。
> - 数值校验：$g = 1110$：$b_3 = 1$；$b_2 = 1\oplus 1 = 0$；$b_1 = 0\oplus 1 = 1$；$b_0 = 1\oplus 0 = 1$ → $b = 1011$ ✓
>   （与前一节的编码结果 $1011 \to 1110$ 首尾闭环）。
> - 再验一个小的：$g = 010$（3 位）：$b_2 = 0$，$b_1 = 0\oplus1 = 1$，$b_0 = 1\oplus0 = 1$ → $b = 011 = 3$ ✓
>   （即 $k=3$ 的码字确实是 `010`，与上文序列一致）。
>
> **4. 为什么通信与位置检测偏爱它（讲义 p.68）**
>
> 讲义的判据：*the probability of making a symbol detection error is inversely proportional to the
> symbol distance* —— 接收端把噪声污染后的符号判错的概率，与符号之间的距离成反比。
> 格雷码把所有**相邻**符号的距离都做到最小（1 bit），于是"差一点点就判错"的那种错误只会赔上 1 个 bit。
>
> ![[gray-code-symbol-mapping.svg]]
> *图 2 — 4-PSK 星座图的两种标注。(a) 自然二进制 `00 01 10 11`：四个相邻对里有两个相差 2 bit，
> 噪声把接收点推到隔壁判决区时会一次错 2 bit。(b) 格雷码 `00 01 11 10`：四个相邻对全部相差 1 bit，
> 任何"判到隔壁"的错误都只错 1 bit —— 这正是格雷码在数字通信里的价值。*
>
> 同一个道理在**物理位置检测**上更直观：旋转编码器的码盘读数在相邻格之间变化时，
> 如果多位同时要翻转，各 bit 的翻转时刻不可能严格同时，中间会短暂出现一个**谁也不是的伪码**。
>
> - 讲义 p.68 的例子（不用格雷码）：从 $011$ 走到 $100$ 要同时翻 3 位；
>   由于翻转有先后，中间可能瞬时读到 `010`、`001`、`101`、`110`、`111` 中的任意一个 —— 都是完全错误的读数。
> - 用格雷码：$011$ 的下一格是 $010$（3 位序列 `000 001 011 010 …` 中 $k=2$ 与 $k=3$），
>   `011 → 010` 只翻最低位，**不存在"多位同时翻转"的危险窗口** ✓。
> - 其它应用：K-map（卡诺图）的行列排列按格雷码排，使相邻格只差一个变量（Ch4 内容）；
>   数字通信的星座图映射；FIFO/异步接口里的指针编码（超出本讲义）。
>
> **Worked Example · 例题**
>
> **Example 1 — 写出 4 位格雷码序列并核对相邻距离（讲义 p.67）**
>
> 题目：给出 4 位格雷码的 16 个码字，并逐对核对相邻距离（含首尾）。
>
> 解：用反射构造法从 $G_3$ 生成 $G_4$：
>
> 1. 前半段 = `0` + $G_3$ = `0000 0001 0011 0010 0110 0111 0101 0100`；
> 2. 后半段 = `1` + reverse($G_3$) = `1100 1101 1111 1110 1010 1011 1001 1000`；
> 3. 接起来就是表里的 16 项。
>
> **数值校验 (Numerical check)**：
> - 相邻异或：`0000⊕0001 = 0001`（1 位）、`0001⊕0011 = 0010`（1 位）、… 15 组全部 popcount = 1 ✓；
> - 首尾：`1000 ⊕ 0000 = 1000` → popcount = 1 ✓（循环性成立）；
> - 反向确认：把序列按"前缀异或"解码，正好还原 $0,1,2,\dots,15$ ✓（第 $k$ 项对应 $k$）。
>
> **Example 2 — $1011$ 与 $1110$ 的双向互算（公式练习）**
>
> 题目：二进制 $1011$ 的格雷码是多少？格雷码 $1110$ 还原成二进制是多少？
>
> 解：
> 1. 编码：$b = 1011$，$b \gg 1 = 0101$，$g = 1011 \oplus 0101 = 1110$。
> 2. 解码：$b_3 = g_3 = 1$；$b_2 = b_3 \oplus g_2 = 1\oplus1 = 0$；$b_1 = b_2 \oplus g_1 = 0\oplus1 = 1$；$b_0 = b_1 \oplus g_0 = 1\oplus0 = 1$。
>
> **数值校验 (Numerical check)**：
> - 编码结果 $g = 1110$ → 查序列表，`1110` 是 $k=11$ 的码字，代表 11；而 $1011_2 = 11$ ✓；
> - 解码结果 $b = 1011 = 11$ ✓ —— 两个方向首尾闭环，说明公式互为逆运算；
> - 距离校验：$1011 \oplus 1110 = 0101$ → popcount = 2（编码前后距离为 2，这很正常：
>   公式保证的是**相邻二进制数**的像相邻，而不是"任意数与它的格雷码"相邻）✓。
>
> **Example 3 — $011 \to 100$：翻转位数对比（讲义 p.68）**
>
> 题目：计数器从 3 走到 4。比较自然二进制与格雷码两种方案下，这一刻要翻转多少位，以及可能出现什么中间态。
>
> 解：
> 1. 自然二进制：$011 \to 100$，$011 \oplus 100 = 111$ → popcount = **3**，三位同时要变。
>    若三位翻转有先后，中间会瞬时读到 `010`、`001`、`101`、`110`、`111` 之一（讲义列的 5 个中间态）。
> 2. 格雷码：$g(3) = 011 \oplus 001 = 010$，$g(4) = 100 \oplus 010 = 110$；
>    $010 \to 110$ 只翻最高位 → popcount = **1**，没有中间态。
>
> **数值校验 (Numerical check)**：
> - $011 \oplus 100 = 111$，popcount $= 3$ ✓（自然二进制这一步要改 3 位）；
> - $010 \oplus 110 = 100$，popcount $= 1$ ✓（格雷码只改 1 位）；
> - 序列核对：3 位格雷码序列 `000 001 011 010 110 111 101 100` 里，`010` 是 $k=3$、`110` 是 $k=4$，
>   两者相邻 ✓，正好对应计数 3 → 4。
>
> **Gray code across logic and timing · 格雷码、逻辑与时序**
>
> Reflected binary Gray code preserves one-bit changes between adjacent entries of its defined sequence. It does not guarantee that arbitrary jumps between nonadjacent values change only one bit. That condition is essential when explaining why a position encoder can avoid mixed intermediate binary readings during a one-step movement.
>
> Gray code is not a fixed-weight sum. Decode it to binary before performing ordinary numeric arithmetic. For bits indexed from MSB to LSB, $g_{N-1}=b_{N-1}$ and $g_i=b_{i+1}\oplus b_i$. The inverse keeps the MSB and then accumulates XORs from the most significant side.
>
> **Worked application — reading an encoder.** binary 7=`0111`，8=`1000`，跨一步会有 4 位改变。对应 Gray 为 `0100` 与 `1100`，只有 MSB 改变。若跳过一个位置由 7 到 9，Gray 9=`1101`，与 Gray 7 相差 2 位；可见 single-bit-change 只保证相邻状态。将 `1100` 反解：binary MSB=1，依次 $1\oplus1=0$、$0\oplus0=0$、$0\oplus0=0$，得到 8。
>
> In English: a one-bit transition reduces the ambiguity of sampling adjacent position codes. It does not remove metastability or validate arbitrary multi-bit transfers between clock domains. Physical synchronization and transition assumptions still matter.
>
> **English exam question:** Why are K-map headings ordered 00, 01, 11, 10?
>
> **Answer:** Successive headings differ in one variable, including the wraparound pair 10 and 00. Adjacent cells can therefore be combined by eliminating exactly the changing variable. Ordinary binary order would place some two-bit changes next to each other.
>
> This connects the same code property to [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并|Karnaugh Map]], [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]], and [[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界|Metastability and Clock Domain Crossing]]. Distinguish Gray sequence design from generic state encoding in [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]].

## 4 · American Standard Code for Information Interchange · 字符编码

ASCII 为七位字符编码：字符 `'0'` 是 0x30，字符 `'A'` 是 0x41；数值 0 与字符 `'0'` 不相同。数字字符减去 `'0'` 才得到数值 0–9，前提是先确认字符处于 `'0'`–`'9'`。

基本 ASCII 范围为 0–127，装进八位字节时高位可为 0；把高位用于奇偶校验或扩展编码时，必须明确协议。Unicode 的字符与 UTF-8 的字节数不能混为一谈。

### ASCII 结构表、锚点与字符处理步骤

ASCII 的 128 个码字包含 95 个可打印字符（空格在内，`0x20`–`0x7E`）和 33 个控制码（`0x00`–`0x1F` 及 DEL）。通常在字节中保存一个 ASCII 码；第八位是容器位，若放校验位则已属于外层协议。

| 区间 | 类别与数量 | 可用于心算的规律 |
|---|---|---|
| `00`–`1F` | 32 个控制码 | LF=`0A`，CR=`0D`，ESC=`1B` |
| `20` | 空格 SP | 十进制 32 |
| `21`–`2F`,`3A`–`40`,`5B`–`60`,`7B`–`7E` | 32 个标点／符号 | 需查表，不能套字母规律 |
| `30`–`39` | 10 个数字字符 | `'d'` 的码值为 $0x30+d$ |
| `41`–`5A` | 26 个大写字母 | $0x41+k$，$k=0\ldots25$ |
| `61`–`7A` | 26 个小写字母 | $0x61+k$，与对应大写差 `0x20` |
| `7F` | DEL | 十进制 127，不是可打印字符 |

| 锚点 | 十六进制 | 十进制 | 七位二进制 |
|---|---|---|---|
| `'0'` / `'9'` | `30` / `39` | 48 / 57 | `0110000` / `0111001` |
| `'A'` / `'Z'` | `41` / `5A` | 65 / 90 | `1000001` / `1011010` |
| `'a'` / `'z'` | `61` / `7A` | 97 / 122 | `1100001` / `1111010` |
| SP / DEL | `20` / `7F` | 32 / 127 | `0100000` / `1111111` |

**编码。** 先判断字符块，数字／字母以块起点加索引，标点和控制码查表；需要字节时七位前补 0。**解码。** 先拒绝“基本 ASCII”范围外的码值，再按控制／空格／数字／字母／符号分类，块内相减得索引。两位十六进制码 v 可用“高 nibble ×16 +低 nibble”读其整数值。

**字符运算须带范围检查。** `'0'\le c\le'9'` 才可求 $d=c-0x30$ 或提取低 nibble；转换字母大小写前确认范围，`XOR 0x20` 是切换已确认字母的大小写。`'9'+1=0x3A=':'`，不是 A。比较 raw ASCII 字节时 `'Z'<'a'`，因此 `"Zebra"<"apple"`；无视大小写的字母排序须先归一化或使用规定的排序规则。

**字符、码点和字节。** 字符 A 的码值由编码约定决定：ASCII/Unicode U+0041 是 65，EBCDIC 可为 C1。Unicode 定义码点 (code point)，UTF-8 定义其字节序列；U+0000–U+007F 在 UTF-8 中为与 ASCII 相同的一字节，其他 Unicode 标量用 2–4 字节。é 为 `C3 A9`，中为 `E4 B8 AD`。因此仅限纯 ASCII 字符串时“字符数=字节数”；一般文本还要区分码点数、字节数和显示字符数。

`0x80`–`0xFF` 不属于基本 ASCII，可在指定单字节代码页中表示别的字符，也可作为 UTF-8 等多字节编码的一部分；GB2312 并非简单“一个高位字节表示一个中文字符”的 ASCII 扩展。

**Exam English.** “The character '9' has ASCII code 57, not numeric value nine. Subtract '0' only after confirming that the character is a digit. Seven-bit code width and eight-bit storage width are different quantities.”

> [!example]- American Standard Code for Information Interchange · 推导与例题
> **图示与讲义依据**
>
> ![[ascii-code-structure.svg]]
> *图 1 — 16×16 的 ASCII 码图：行 = 高 4 位、列 = 低 4 位，所以"查表"就是"读十六进制"。控制字符（红）、
> 符号（浅灰）、数字（绿）、大写（蓝）、小写（深红）各自成块，`0x30`/`0x41`/`0x61` 三个锚点被圈出；
> 下半区（`0x80`–`0xFF`，斜纹）不是 ASCII，而是 Latin-1/代码页等 8 位扩展。*
>
> **Derivation · 推导过程**
>
> **1. 为什么是 7 位**
>
> 需要表示的符号量级：26 大写 + 26 小写 + 10 数字 + 约 30 个标点 + 若干控制动作 $\approx 100$ 个。
>
> - 6 位只有 $2^{6}=64$ 个码字，不够；7 位有 $2^{7}=128$ 个，刚好够且留有富余 ✓。
> - 8 位要给汉字/图形留空间也远不够（汉字常用 6763 个），所以后来是 16 位/21 位的 Unicode，而不是把 ASCII 简单加宽 1 位。
>
> **2. 三条结构规律（可直接算，不必查表）**
>
> **(a) 数字：码值 = `0x30` + 数字值**
>
> $$
> \text{code}('d') = \texttt{0x30} + d,\qquad d=0,\dots,9
> $$
>
> - 意义：数字字符的低 4 位就是它的十进制值，高 3 位固定是 `011`。
> - 数值校验：`'7'` → `0x30 + 7 = 0x37`，二进制 `011 0111`，低 4 位 `0111` = 7 ✓；
>   `'0'` → `0x30` = `011 0000` ✓；`'9'` → `0x39` = `011 1001` ✓。
> - 推论：`c - '0'` 就是数字值；反过来 `'0' + 5 = 0x35 = '5'` ✓。
>
> **(b) 字母：码值 = 起点 + 序号**
>
> $$
> \text{code}('A'+k) = \texttt{0x41}+k,\qquad
> \text{code}('a'+k) = \texttt{0x61}+k,\qquad k=0,\dots,25
> $$
>
> - 意义：字母在各自块内连续排列，低 5 位 = $k+1$（低 5 位从 1 开始计）。
> - 数值校验：`'E'` 是第 5 个字母 ($k=4$) → `0x41 + 4 = 0x45` = `100 0101` ✓；
>   `'C'` ($k=2$) → `0x43` ✓；`'J'` ($k=9$) → `0x4A` = `100 1010`，低 5 位 `01010` = 10 = $k+1$ ✓。
>
> **(c) 大小写：只差第 5 位（权值 `0x20` = 32）**
>
> $$
> \text{code}('a') - \text{code}('A') = \texttt{0x61}-\texttt{0x41} = \texttt{0x20} = 32_{10} = 010\,0000_2
> $$
>
> - 意义：把第 5 位（权值 32 的那一位）取反，就在大写和小写之间切换：
>   `'A'` = `100 0001`，`'a'` = `110 0001`，二者只差 bit 5 ✓。
> - 数值校验：`'a' XOR 0x20 = 0x61 XOR 0x20 = 0x41 = 'A'` ✓；
>   `'Z' XOR 0x20 = 0x5A XOR 0x20 = 0x7A = 'z'` ✓。
>
> **3. 从字符到字节：字符串就是字节序列**
>
> 一串文本在机器里就是一个字节序列（每个 ASCII 字符 1 字节），用十六进制查看就是**内存转储**的样子：
>
> $$
> \texttt{"ECE2050"} \;\longrightarrow\; \texttt{45 43 45 32 30 35 30}_{16}
> $$
>
> - 数值校验（逐字符用上面的规律复核）：
>   `'E'` = `0x41+4` = `0x45` ✓；`'C'` = `0x41+2` = `0x43` ✓；`'2'` = `0x30+2` = `0x32` ✓；
>   `'0'` = `0x30+0` = `0x30` ✓；`'5'` = `0x30+5` = `0x35` ✓ —— 7 个字符 → 7 字节 ✓。
> - 这一步是后面所有"文本处理"的基础：字符串长度 = 字节数（纯 ASCII 时成立；UTF-8 下中文一个字 3 字节）。
>
> **4. 8 位扩展与 Unicode 的分工**
>
> | 层次 | 范围 | 编码宽度 | 说明 |
> |---|---|---|---|
> | ASCII | `0x00`–`0x7F` | 7 bit | 英文、数字、标点、控制 |
> | 8 位扩展 / 代码页 | `0x80`–`0xFF` | 8 bit | Latin-1 重音字母、西里尔字母、制表符等 |
> | Unicode 码点 | U+0000–U+10FFFF | 抽象编号 | 为全世界字符编号，不是存储格式 |
> | UTF-8 | 1–4 字节 | 变长 | U+0000–U+007F 与 ASCII 完全一致（向后兼容） |
>
> - 数值校验：`'A'` 的码点 U+0041 ≤ U+007F → UTF-8 用 1 字节 `0x41`，与 ASCII 相同 ✓；
>   `'中'` U+4E2D > U+007F → UTF-8 用 3 字节 `0xE4 0xB8 0xAD`（不是 ASCII）✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 把字符串 `ECE2050` 写成 ASCII 十六进制与二进制**
>
> 题目：给出 `ECE2050` 的 ASCII 码（十六进制字节串与 8 位二进制），并说明为什么它正好是 7 字节。
>
> 解：
> 1. 逐字符定块：`E`、`C` 是大写字母块；`2`、`0`、`5` 是数字块。
> 2. 用规律算码值：
>    - `'E'` = `0x41 + 4` = `0x45`，`'C'` = `0x41 + 2` = `0x43`；
>    - `'2'` = `0x30 + 2` = `0x32`，`'0'` = `0x30`，`'5'` = `0x30 + 5` = `0x35`。
> 3. 十六进制字节串：`45 43 45 32 30 35 30`。
> 4. 二进制（每字节 8 位）：`0100 0101  0100 0011  0100 0101  0011 0010  0011 0000  0011 0101  0011 0000`。
>
> **数值校验 (Numerical check)**：
> - `'E'`：`0x45` = `0100 0101`，十进制 $64+4+1=69$ ✓（`'A'` = 65，加 4 = 69 ✓）。
> - `'2'`：`0x32` = `0011 0010`，低 4 位 `0010` = 2 ✓（数字规律）。
> - `'5'`：`0x35`，低 4 位 `0101` = 5 ✓。
> - 长度：7 个字符 → 7 字节 = 56 bit ✓（若按 7 位紧凑存放只有 $7\times 7=49$ bit；多出的 7 位就是"每字符补 0 到 1 字节"的代价）。
>
> **Example 2 — 由码值反推字符：`0x4A`、`0x6A`、`0x35`**
>
> 题目：已知这是 ASCII，写出对应字符并说明用到的规律。
>
> 解：
> 1. `0x4A`：落在 `0x41`–`0x5A` → 大写；`0x4A - 0x41 = 9` → 第 10 个字母 = **`J`**。
> 2. `0x6A`：落在 `0x61`–`0x7A` → 小写；`0x6A - 0x61 = 9` → **`j`**；
>    也可以直接由 `0x6A = 0x4A + 0x20` 得到（大小写只差第 5 位）✓。
> 3. `0x35`：落在 `0x30`–`0x39` → 数字；`0x35 - 0x30 = 5` → **`'5'`**。
>
> **数值校验 (Numerical check)**：
> - `0x4A` = `100 1010`，低 5 位 `01010` = 10 = $k+1$ → $k=9$ → `'A'+9 = 'J'` ✓。
> - `0x6A XOR 0x20 = 0x4A` ✓（两个字符确实只差 bit 5）。
> - `0x35` 与 `0x25` 对比：`0x25` 是 `%`（符号块），`0x35` 是 `'5'` —— 相差的正是 bit 4（`0x10`），别混 ✓。
>
> **Example 3 — 把 `'a'` 变成 `'A'` 需要做什么运算**
>
> 题目：给出至少两种做法，并说明什么时候会出错。
>
> 解：
> 1. 做法一（异或）：`'a' XOR 0x20` = `110 0001 XOR 010 0000` = `100 0001` = `'A'` ✓。
> 2. 做法二（减法）：`'a' - 32 = 97 - 32 = 65 = 'A'` ✓（等价，因为差的正是权值 32 的那一位）。
>
> **数值校验 (Numerical check)**：
> - `'a'` = `0x61` = `0110 0001`，`'A'` = `0x41` = `0100 0001`，逐位比较只有 bit 5 不同 ✓。
> - 反向：`'A' XOR 0x20 = 0x61 = 'a'` ✓ —— 同一个运算两个方向都成立。
> - 边界反例：`'0'` = `0x30`，`0x30 XOR 0x20 = 0x10` = 控制字符 DLE，**不是**任何字母 ✗
>   → 必须先判断 `0x41 <= c <= 0x5A` 或 `0x61 <= c <= 0x7A` 才能做这个运算。
>
> **Character processing as a datapath · 字符怎样进入数据通路**
>
> ASCII codes represent characters, while an arithmetic datapath usually needs numeric values. Converting a digit character to an integer therefore has two steps: verify that the character belongs to the digit range, then subtract the code for '0'. Subtraction without the range check can turn a punctuation character into an apparently plausible number.
>
> For a string of decimal digits, accumulate the numeric value from left to right. If the value already accumulated is $v$ and the next digit value is $d$, the next value is $10v+d$. This is the positional expansion evaluated incrementally. The accumulator width must accommodate the final value, not merely one character code.
>
> **Worked application — parse a two-digit setting.** 输入字符 `"42"`，codes 是 `0x34,0x32`。分别检查在 `0x30`–`0x39` 内，取 $d_1=0x34-0x30=4$，$d_2=0x32-0x30=2$，累加 $v=10\times4+2=42$。输出给普通二进制寄存器应为 `00101010`；若显示电路要 BCD，应为 `0100 0010`，不应原封不动写入 ASCII `0x34 0x32`。
>
> In English: character decoding, numeric accumulation, and display encoding are three distinct operations. Their bit widths and meanings differ even though they all use binary storage.
>
> **English exam question:** Is extracting the low nibble a complete ASCII digit decoder?
>
> **Answer:** No. The low nibble gives the digit value only after the byte is known to lie between `0x30` and `0x39`. Other ASCII characters can have the same low nibble. A valid-range check is required to distinguish digits from those characters.
>
> The validation can use [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]]. The numeric result then connects to [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码|Binary Coded Decimal]], [[Seven-Segment Display and Code Conversion]], and [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]] for storing strings versus numeric settings.

## 5 · 重点与应用

| 目的 | 选择 | 易错点 |
|---|---|---|
| 十进制显示与逐位计算 | BCD | 把整串当纯二进制 |
| 位置变化或相邻编码 | Gray | 把相邻性当作纠错能力 |
| 文本接口 | ASCII / specified encoding | 把字符与数值混用 |

显示应用见 [[Seven-Segment Display and Code Conversion]]；错误检测见 [[Parity and Cyclic Redundancy Checks]]。

先修是 [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型|位权与编码之别]]、[[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|十进制／二进制／hex]] 和 [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|位宽、nibble 与 byte]]。本篇内部可依 BCD→Gray→ASCII 对照“逐位十进制语义／相邻性／符号映射”。

应用连接 [[Seven-Segment Display and Code Conversion|BCD 显示]]、[[Karnaugh Map Minimization|Gray 排序的 K-map]]、[[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界|Gray 与异步传输条件]]、[[Keyboard Scanning and Encoding|键盘字符编码]]。检错连接 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|ASCII 外层奇偶位]] 和 [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|CRC]]，别把相邻 Gray 性质当作检错保证。

## Sources · 课件依据

主线课件：[Ch2 lecture](../ECE2050-Chap2.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
