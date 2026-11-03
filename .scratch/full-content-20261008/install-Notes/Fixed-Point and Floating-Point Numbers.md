---
tags:
  - ECE2050
  - fractional-numbers
date: 2026-09-16
updated: 2026-10-09
chapter: Ch2
aliases:
  - 定点数与浮点数
  - Fixed-Point and Floating-Point Numbers
  - 定点数与浮点数 · Ch2
  - Fixed-Point Numbers
  - 定点数
  - 定点表示法
  - Fixed-Point Representation
  - Q 格式
  - Floating-Point Numbers
  - 浮点数
  - 浮点表示法
  - IEEE 754
  - Floating-Point Representation
---

# Fixed-Point and Floating-Point Numbers · 定点数与浮点数

> [!SUMMARY] Quick recall · 英文速览
> Fixed point applies a fixed scale to an integer. Floating point stores a sign, exponent, and fraction; its range and precision are different properties.

## 1 · Fixed-Point Numbers · 把整数乘以固定尺度

定点数 (fixed-point number) 若整数代码为 n、小数位数为 b，则 $x=n2^{-b}$，分辨率 $\Delta=2^{-b}$。n 的有符号／无符号解释仍由 [[Binary Arithmetic and Signed Representation]] 决定。

总宽 N 的无符号范围 $0\ldots(2^N-1)2^{-b}$；补码范围 $-2^{N-1-b}\ldots(2^{N-1}-1)2^{-b}$。Q 格式的名称有不同约定，必须声明整数位是否包含符号位。

**例。** U4.4 中 `1010 1000` 对应整数 168，数值 $168/16=10.5$。增加小数位改善分辨率，但固定总宽下会缩小范围。

### 格式约定、有效范围与编解码

小数点是接口预先约定的**隐含二进制点 (implied binary point)**，位串本身不携带它。这里明确采用课件约定：U$a.b$ 为无符号，Q$a.b$ 为补码且 $a$ **包含符号位**，总位数 $N=a+b$。符号、整数位和小数位必须在通信／计算两端一致。

| 格式 | 整数代码 $n$ 的解释 | 数值范围 | 固定步长 |
|---|---|---|---|
| U$a.b$ | $N$ 位 unsigned | $[0,2^a-2^{-b}]$ | $2^{-b}$ |
| Q$a.b$ | $N$ 位 two's complement | $[-2^{a-1},2^{a-1}-2^{-b}]$ | $2^{-b}$ |
| U4.4 | 8 位 unsigned | $[0,15.9375]$ | $1/16$ |
| Q4.4 | 8 位 signed | $[-8,7.9375]$ | $1/16$ |
| Q1.15 | 16 位 signed | $[-1,1-2^{-15}]$ | $2^{-15}$ |

Q1.15 的 +1 不能精确表示，最大值为 0.999969482421875。将 +1 直接缩放并取低 16 位会存 `1000 0000 0000 0000`，回读成 −1，这属于回绕而非微小量化误差。最小值 −1 则恰好可表示。

同模式 `0110 1100` 的整数读数为 108，在 U4.4/Q4.4 中为 6.75，在 U6.2 中为 27，在 U1.7 中为 0.84375。若要**保持同一个值 6.75**并改格式，则 U3.5 代码为 216=`1101 1000`，U6.2 代码为 27=`0001 1011`。改变格式解释与重新编码保持数值是两种操作。

**编码五步。** 指定 U/Q、$a,b$、舍入和溢出策略 → 算缩放实数 $x2^b$ → 按给定规则得到整数 $n=\operatorname{round}_{mode}(x2^b)$ → **再查 n 是否落在整数代码范围** → 按 $N$ 位 unsigned／补码写码并回读 $\hat x=n2^{-b}$。近似输入回读得到的是 $\hat x$，只有 $x2^b$ 为整数且无越界时才要求 $\hat x=x$。

负数可用 $n\bmod2^N$ 直接编码；若用幅值再取反加一，应先对 $|x|2^b$ 做对应舍入，不要把已得到的负 n 又取负一次。解码先依据 U/Q 读整数 n，再除 $2^b$；负权／$u-2^N$ 方法对最小负数也成立。

**前提与误区。** 定点能够表示小数，但仅能精确表示指定步长的整数倍；固定总宽增加 b 提高分辨率同时缩小范围。`1100 0000` 在 U4.4 为 12，在 Q4.4 为 −4；不知道格式不能报值。Q 的最负端不应加一个步长。接口即使同为 8 bit，只要尺度不同也会读错。

**Exam English.** “A fixed-point pattern is an integer code multiplied by an agreed scale. The binary point is implied. Quantization changes the value when the scaled input is not an integer; overflow is a separate range failure.”

> [!example]- Fixed-Point Numbers · 推导与例题
> **图示与讲义依据**
>
> ![[fixed-point-format.svg]]
> *图 1 — (a) U4.4 的八条位权 $2^{3}\dots2^{-4}$：同一个 $6.75$ 在 U4.4 里是 `0110.1100`，把隐含小数点
> 左移一位（U3.5）位串整体左移一位变成 `110.11000`，右移两位（U6.2）变成 `000110.11` —— 数值不变，
> 步长从 $2^{-4}$ 变成 $2^{-5}$ / $2^{-2}$。(b) Q4.4 只改了一件事：最高位权重从 $+2^{3}$ 变成 $-2^{3}$，
> 于是 $6.75$ 的 `0110 1100` 取反加一即得 $-6.75$ 的 `1001 0100`；回读 $-8+1+0.25 = -6.75$。*
>
> **Derivation · 推导过程**
>
> **1. 从位权到"整数缩放"：为什么 $x = n/2^{b}$**
>
> 把 $a+b$ 位串按位置 $k=a-1,\dots,-b$ 编号，第 $k$ 位的权重是 $2^{k}$；把整串当无符号整数读得
> $n=\sum_k d_k 2^{k+b}$（整数读法等于把小数点"当成在第 0 位之后"）。两式相除：
>
> $$
> x=\sum_{k=-b}^{a-1} d_k 2^{k} = \frac{1}{2^{b}}\sum_{k=-b}^{a-1} d_k 2^{k+b} = \frac{n}{2^{b}}
> $$
>
> - 意义：**定点数 = 整数 + 固定的 $2^{b}$ 缩放因子**。同格式的定点加法与整数加法是同一条电路；
>   定点乘法才需要额外右移 $b$ 位（本课不展开）。
> - 数值校验：$6.75 \to n = 6.75\times16 = 108 = 0110\,1100_2$ ✓，回读 $108/16 = 6.75$ ✓。
>
> **2. 同一数值、不同约定：U4.4 / U3.5 / U6.2**
>
> 给定 $x$ 与格式 $\text{U}a.b$，只需 **$n = \mathrm{round}(x\cdot 2^{b})$**，再写成 $a+b$ 位：
>
> $$
> 6.75\times 2^{4} = 108 \Rightarrow \texttt{0110 1100}\ (a{=}4),\qquad
> 6.75\times 2^{5} = 216 \Rightarrow \texttt{1101 1000}\ (a{=}3),\qquad
> 6.75\times 2^{2} = 27 \Rightarrow \texttt{0001 1011}\ (a{=}6)
> $$
>
> - 意义：$(a,b)$ 决定"哪些位是整数、哪些位是小数"，不改变数值，只改变步长与范围。
> - 数值校验：$108/16 = 6.75$ ✓、$216/2^{5} = 216/32 = 6.75$ ✓、$27/2^{2} = 27/4 = 6.75$ ✓。
> - 规律：$b$ 每减 1，$n$ 就右移 1 位（同时引入 1 bit 的取整风险）；$n$ 必须装得进 $a+b$ 位 ——
>   $6.75$ 不能写成 U2.6，因为 $6.75\times2^{6} = 432 > 2^{8}-1 = 255$。
>
> **3. Q 格式的负数：取反加一，与补码同源**
>
> 最小位权是 $-2^{a-1}$，所以整串的总值就是补码值。求 $-x$ 的做法与 [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]]
> 的 *reverse the sign* 完全一样（讲义 p.54）：**invert the bits，add one to the LSB**。
>
> $$
> 6.75 = \texttt{0110 1100} \xrightarrow{\text{invert}} \texttt{1001 0011}
> \xrightarrow{+1} \texttt{1001 0100} = -6.75
> $$
>
> - 意义：定点负号复用补码硬件，"取负"不需要单独的取绝对值/比较电路。
> - 数值校验：按位权回读 `1001 0100`：$-2^{3}+2^{0}+2^{-2} = -8+1+0.25 = -6.75$ ✓；
>   再取一次负号：`1001 0100` → invert `0110 1011` → $+1$ → `0110 1100` $= 108/16 = 6.75$ ✓。
>
> **4. 溢出：回绕 (wrap) 与饱和 (saturate)**
>
> U4.4 的两个操作数是 $12 = \texttt{1100 0000}$（整数 $192$）与 $7.5 = \texttt{0111 1000}$（整数 $120$）：
>
> $$
> 192+120 = 312 = 1\,\texttt{0011 1000}_2 \quad(\text{需要 9 位，器件只有 8 位})
> $$
>
> - **回绕**：丢弃第 9 位，保留低 8 位 `0011 1000` $= 56$，回读 $56/16 = 3.5$。真实和 $19.5$，误差 $16.0$ ——
>   不是"精度差一点"，而是量级完全错（音频里是爆音 click，视频亮区里是一个黑点，讲义 p.55）。
> - **饱和**：检测到溢出后直接把结果钳到最大码 `1111 1111` $= 255/16 = 15.9375$，误差 $3.5625$，
>   但**方向不变、没有跳变**（峰值被削平，而不是翻转成一个小值）。
> - 讲义 p.55 的简写要注意：讲义写 $\texttt{1100 0000} + \texttt{0111 1000} = \texttt{1111 1111}$ 与
>   $12+7.5 = 15.9375$。这两行**只有按饱和加法读才成立**：普通二进制加法的真实结果是 9 位的
>   $1\,\texttt{0011 1000}$，讲义省略了"溢出 → 钳位"这一步，也没有写出真实和 $19.5$。照抄成普通加法会得到
>   $3.5$（回绕）或 $19.5$（无限位宽），都无法解释 `1111 1111`。
>
> ![[saturating-arithmetic.svg]]
> *图 2 — 横轴是"真实和"，纵轴是 U4.4 读回来的值：只有和不超过 $15.9375$ 时两条曲线重合（输出 $=$ 输入）；
> 超过之后回绕曲线（红色）断崖式跌回 $3.5$，饱和曲线（绿色）走平在 $15.9375$。工作点 $12+7.5 = 19.5$ 上的
> 红/绿两个圆点就是"爆音 vs. 削顶"的区别，与例题 3 的算式一一对应。*
>
> **Worked Example · 例题**
>
> **Example 1 — $6.75$ 的三种无符号格式（讲义 p.53）**
>
> 题目：把 $6.75$ 分别写成 U4.4、U3.5、U6.2。
>
> 解：
> 1. $6.75 = 4+2+0.5+0.25 = 110.11_2$（整数部分 $6 = 110_2$，小数部分 $0.75 = 0.11_2$）。
> 2. U4.4：$n = 6.75\times16 = 108$，8 位 `0110 1100`，小数点在第 4 位后 → `0110.1100`。
> 3. U3.5：$n = 6.75\times32 = 216$，8 位 `1101 1000`，小数点在第 3 位后 → `110.11000`。
> 4. U6.2：$n = 6.75\times4 = 27$，8 位 `0001 1011`，小数点在第 6 位后 → `000110.11`。
>
> **数值校验 (Numerical check)**：$108/16 = 6.75$ ✓，$216/32 = 6.75$ ✓，$27/4 = 6.75$ ✓；
> 按位权展开 U4.4：$0\cdot8+1\cdot4+1\cdot2+0\cdot1+1\cdot0.5+1\cdot0.25+0+0 = 6.75$ ✓。
> 三者步长为 $0.0625$ / $0.03125$ / $0.25$，最大值为 $15.9375$ / $7.96875$ / $63.75$。
>
> **Example 2 — $-6.75$ 的 Q4.4（讲义 p.54）**
>
> 题目：写出 $-6.75$ 的 Q4.4 编码，并回读验证。
>
> 解：
> 1. 先编 $+6.75$：$n = 108 = \texttt{0110 1100}$。
> 2. 取反：`1001 0011`；LSB 加 1：`1001 0011 + 1 = 1001 0100`。
> 3. 小数点放在 4 位之后：`1001.0100`，数值 $-6.75$。
>
> **数值校验 (Numerical check)**：按位权回读 $-2^{3}+2^{0}+2^{-2} = -8+1+0.25 = -6.75$ ✓；
> 再取一次负号 → `0110 1100` $= 108/16 = 6.75$ ✓（往返一致）。量级自检：$-6.75/0.0625 = -108$ 是整数 ✓。
>
> **Example 3 — $12+7.5$ 的回绕与饱和（讲义 p.55）**
>
> 题目：两个 U4.4 数 $12$ 与 $7.5$ 相加，硬件只有 8 位。分别给出回绕结果与饱和结果。
>
> 解：
> 1. 编码：$12\times16 = 192 = \texttt{1100 0000}$；$7.5\times16 = 120 = \texttt{0111 1000}$。
> 2. 真实和：$192+120 = 312 = 19.5\times16$，二进制 $1\,\texttt{0011 1000}$ —— **需要 9 位**。
> 3. 回绕：丢弃第 9 位，得 `0011 1000` $= 56$，回读 $56/16 = 3.5$。
> 4. 饱和：溢出标志置位 → 输出最大码 `1111 1111` $= 255$，回读 $255/16 = 15.9375$。
>
> **数值校验 (Numerical check)**：$312 = 256+56 \Rightarrow$ 低 8 位 $= 312-256 = 56$，$56/16 = 3.5$ ✓；
> $255/16 = 16-1/16 = 15.9375$ ✓。误差对比：回绕 $|3.5-19.5| = 16$，饱和 $|15.9375-19.5| = 3.5625$ ——
> 饱和误差小 $16/3.5625 = 4.49$ 倍，更重要的是**误差方向单调**，不会把亮区翻成黑点。
>
> **Example 4 — Q1.15 里为什么没有 $+1.0$（讲义 p.54 的范围纠正）**
>
> 题目：$Q1.15$（Q15）讲义标注范围为 $(1,-1]$。检验 $x = 1.0$ 能否表示。
>
> 解：
> 1. $n = 1.0\times2^{15} = 32768$，16 位写法是 `1000 0000 0000 0000`。
> 2. 寄存器只有 16 位，这一串在补码里是 $-32768$。
> 3. 回读：$-32768/2^{15} = -1.0$ —— 想写 $+1.0$，得到 $-1.0$。
>
> **数值校验 (Numerical check)**：最大可表示码是 `0111 1111 1111 1111` $= 32767$，
> $32767/32768 = 0.999969482421875 = 1-2^{-15}$ ✓，故范围为 $[-1,\ 1-2^{-15}]$，**不是** $[-1,+1]$；
> $+1.0$ 恰好越界并回绕到 $-1.0$ ✓ —— 这正是图 2 的回绕在音频 DSP 里的经典事故。
>
> **Scaling belongs to the representation · 定点缩放与英文理解**
>
> A fixed-point word is an integer code with an agreed scale. If the stored signed integer is $q$ and there are $F$ fractional bits, the represented value is $x=q2^{-F}$. The hardware does not store a physical dot. The dot is part of the interface contract between the producer and consumer of the bits.
>
> Addition requires compatible scales. Multiplication adds the fractional-bit counts: multiplying codes with $F_A$ and $F_B$ fractional bits creates a product with $F_A+F_B$ fractional bits. Reducing that product to a target format requires a shift plus a stated rounding rule and a range check. A cast or assignment does not automatically preserve the physical value.
>
> **Worked application — coefficient multiplication.** 采用本篇含符号位的 Q4.4 约定，$1.5$ 存 $q_A=24$=`00011000`，$-0.75$ 存 $q_B=-12$=`11110100`。16 位乘积 code $=-288$，有 8 位小数，故真值 $-288/256=-1.125$。回到 Q4.4，应除 code 以 16，得 −18，编码 `11101110`，$-18/16=-1.125$，本例恰好无舍入误差。
>
> In English: the intermediate product is wider and has twice the fractional precision. Rescaling removes four fractional positions in this example. The exact divisibility makes the result independent of whether truncation or round-to-nearest is selected here; that is not true for every input pair.
>
> **English exam question:** Does adding more fractional bits always improve a fixed-width format?
>
> **Answer:** It improves resolution by reducing the least significant step, but leaves fewer integer positions and narrows the representable range. A suitable format must cover both the expected amplitude and the required resolution.
>
> See [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确|Signed Binary Multiplication and Division]], [[Binary Arithmetic Circuits#4 · Combinational Multiplier · 从部分积到列加法|Combinational Multiplier]], and [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] for width, signed type, and resize behavior. Always state the Q-format convention before counting sign and integer bits.

## 2 · 定点运算：先对齐，再舍入

加减法先对齐二进制小数点；乘法结果小数位数相加，输出截断／舍入前检查中间宽度。回绕 (wrap-around) 与饱和 (saturation) 是不同溢出策略，应由规范选择。

### 尺度传播、量化与越界处理

对 $x=n_x2^{-b_x}$、$y=n_y2^{-b_y}$，先决定输出小数位数 $b_z$。加减可在公共尺度 $b_c=\max(b_x,b_y)$ 下左移较粗代码；符号扩展并保留中间高位后相加，最后按输出尺度缩放与舍入。不能直接对不同 b 的代码相加。

乘法先计算完整整数积 $p=n_xn_y$，其尺度为 $2^{-(b_x+b_y)}$，再求

$$n_z=\operatorname{round}_{mode}\!\left(p\,2^{b_z-b_x-b_y}\right).$$

因此 Q4.4 × Q4.4 的完整 16 位代码有 8 个小数位；若输出仍为 Q4.4，要除 $2^4$ 再舍入，最后查 8 位 signed 范围。不能只截取低八位，那会破坏尺度；右移负代码时也需匹配向零／向负无穷／最近舍入约定。

最近舍入且无饱和／溢出时，量化误差 $|\hat x-x|\le\Delta/2$；向零截断时 $|\hat x-x|<\Delta$。舍入模式作用于正负两侧的方向应清楚，不能笼统把负数右移称作向零截断。

**回绕 (wrap-around)** 保留低 $N$ 位；**饱和 (saturation)** 将越界值钳到格式的最小或最大可表示值。它们是可选规范，不是所有定点装置必然不会报错或必然需要饱和。U4.4 的 $12+7.5=19.5$：回绕为 3.5，饱和为 15.9375；两者误差远大于量化一步，不能与“精度损失”混淆。

## 3 · Floating-Point Numbers · 用指数扩展范围

浮点数 (floating-point number) 的 IEEE 754 单精度有 s 1 位、E 8 位、F 23 位。正规数 $1\le E\le254$ 为：

$$x=(-1)^s\left(1+F/2^{23}\right)2^{E-127}.$$

E 是存储的偏置指数，F 是存储的尾数字段整数；隐含前导 1 只用于正规数。s、E、F 均无量纲。

| 字段条件 | 含义 |
|---|---|
| E=0,F=0 | 带符号零 |
| E=0,F≠0 | 次正规数，$x=(-1)^s(F/2^{23})2^{-126}$ |
| 1≤E≤254 | 正规数 |
| E=255,F=0 | 无穷 |
| E=255,F≠0 | NaN |

### 浮点模型与完整字段处理方法

浮点 (floating point) 是科学计数法：$x=(-1)^sM2^e$，$M$ 为有效数字 (significand，课件亦称 mantissa)，$e$ 为实际指数 (exponent)。正规二进制数令 $1\le M<2$，存小数部分，前导 1 隐含。把尺度 e 放入字段，使动态范围显著扩大；它不消除有限位量化。

| binary32 字段 | 位号 | 解释 |
|---|---|---|
| sign $s$ | 31 | 独立正负号，不是整字补码 |
| biased exponent $E$ | 30–23 | 8 位 unsigned，正规数实际指数 $e=E-127$ |
| fraction $F$ | 22–0 | 23 位 unsigned，正规有效数字 $M=1+F/2^{23}$ |

本文主公式用 E 表示存储字段、e 表示实际指数；折叠课件推导里写“E+127”时 E 是课件的实际指数符号，应据上下文区分。正规数有 24 位有效二进制精度，实际指数为 −126 至 +127。字段 0、255 留作特殊值，不能直接将 $E-127=-127$、128 代入正规公式。

**编码。** 先确认格式与 rounding mode → 确定符号、处理零与非有限输入 → 非零绝对值写成二进制并规格化为 $1.f\times2^e$ → 算 $E=e+127$ → 将有效数字舍入到 24 位精度。短的 f 才补零至 23 位；超过长度不能一律截断。若舍入使有效数字成为 2，要右移一位并使指数加 1；指数到达边界还需按规则处理 subnormal、underflow 或 overflow。

**解码。** 拆字段 → **先查 E=0/255** → 正规值恢复隐含 1、算 e → 次正规值用隐含 0 和固定指数 −126 → 用符号合成数值。正规非零幅值满足 $2^e\le|x|<2^{e+1}$，作为量级复核。零、NaN 和 infinity 不接受普通规格化步骤。

**次正规数 (subnormal / denormal)** 的间距恒为 $2^{-149}$，最小正值为 $2^{-149}$，逐渐趋近零时有效位数减少；这属于扩展说明。overflow 到 infinity、有限最大值或其他状态取决于规定的舍入模式；NaN 通常来自无效操作，如 $0/0$，不是“幅值过大就变 NaN”。

**比较条件。** 同符号正有限值的原始位串按 unsigned 排序与数值排序一致；负有限值方向相反；异号先看符号，+0 和 −0 数学比较相等，NaN 单独处理。对舍入计算结果使用精确 `==` 还是绝对／相对容差，由问题语义决定，不能规定所有浮点比较都禁止相等判断。

**Exam English.** “A biased exponent is an unsigned stored field; subtract the format's bias to recover the normal exponent. Restore the implicit leading one only for normal values. Check reserved exponent fields before applying the normal-value formula.”

> [!example]- Floating-Point Numbers · 推导与例题
> **图示与讲义依据**
>
> ![[ieee754-single-format.svg]]
> *图 1 — 32 位字段布局：bit 31 是符号、bits 30…23 是偏移阶码（存 $E+127$）、bits 22…0 是 23 位尾数；
> 虚线小框标出那个**不存进位串**的前导 $1.$。下面两行是已核对的例题：$228$ 的
> `0 10000110 11001000000000000000000` $= 0x43640000$，$-58.25$ 的 `1 10000100 11010010000000000000000` $= 0xC2690000$。*
>
> **Derivation · 推导过程**
>
> **1. 为什么需要浮点：定点的范围太窄**
>
> U4.4 的可表示幅值只有 $[0.0625,\ 15.9375]$（$255$ 个码、约 $2.4$ 个十进制数量级）；binary32 的规格化数覆盖
> $2^{-126}\approx1.18\times10^{-38}$ 到 $(2-2^{-23})\times2^{127}\approx3.40\times10^{38}$：
>
> $$
> \log_{10}\frac{3.4028\times10^{38}}{1.1755\times10^{-38}} = 38.53+37.93 = 76.46\ \text{decades}
> $$
>
> - 意义：此处比较的是 32 位 binary32 和 8 位 U4.4，不是相同位宽；binary32 正规幅值覆盖约 $76.5$ 个数量级，代价是**绝对**精度随量级浮动。
> - 数值校验：$\log_{10}(255) = 2.406$，$76.46/2.406 \approx 31.8$ —— 覆盖的十进制数量级数约为 U4.4 的 **32 倍**；幅值上限／下限之比本身不只是 32 倍 ✓。
>
> ![[floating-point-dynamic-range.svg]]
> *图 2 — 对数幅值数轴：binary32 的规格化区间从 $2^{-126}=1.18\times10^{-38}$ 直到 $3.40\times10^{38}$
> （约 $76.5$ 个数量级），例 1、例 2 的 $228$ 与 $58.25$ 都挤在中间；下方红色窄条的数值区间对应 U4.4 的非零幅值，约有
> $2.4$ 个数量级。对数轴不包含零；指数全 0 还包括次正规数。大数 overflow 的结果由舍入模式决定，NaN 则用于无效运算等情况。*
>
> **2. 规格化：把二进制点搬到最高位 1 的右边**
>
> 以 $228$ 与 $58.25$ 为例（讲义 p.58–61）：
>
> $$
> 228_{10} = 1110\,0100_2 = 1.11001_2\times2^{7},
> \qquad
> 58.25_{10} = 111010.01_2 = 1.1101001_2\times2^{5}
> $$
>
> - 整数部分用"除以 2 取余"（[[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|Number Base Conversion]]）：$228 = 128+64+32+4 = 1110\,0100_2$；
>   小数部分用"乘 2 取整"：$0.25\times2 = 0.5\to0$、$0.5\times2 = 1.0\to1$，故 $0.25 = 0.01_2$ ✓。
> - **规格化 = 把点左移到最高位 1 的右边**，移了几位就是阶码：$1110\,0100$ 移 7 位 → $E = 7$；
>   $111010.01$ 移 5 位 → $E = 5$。
> - 数值校验：$1.11001_2 = 1.78125$，$\times2^{7} = 228$ ✓；$1.1101001_2 = 1.8203125$，$\times2^{5} = 58.25$ ✓。
>
> **3. 为什么可以不存前导 1**
>
> 规格化后尾数一定是 $1.f_{22}\dots f_{0}$，整数部分**恒为 1**，无需浪费一位（讲义 p.59：
> *So, no need to store it: implicit leading 1*）。
>
> $$
> \text{有效精度} = 1\ (\text{隐含}) + 23\ (\text{存储}) = 24\ \text{位}
> $$
>
> - 意义：白赚 1 位精度，代价是"$0$ 与很小的数"必须另开一档（denormal）来表示。
> - 数值校验：$24$ 位有效精度对应 $24\log_{10}2 = 7.22$ 位十进制有效数字 ✓ —— 这就是 `float` 常说的"约 7 位有效数字"。
>
> **4. 偏移阶码：为什么存的是 $E+127$**
>
> $$
> E_{\text{stored}} = E + \text{bias} = E + 127,\qquad
> E = 7 \Rightarrow 134 = \texttt{1000 0110}_2,\qquad
> E = 5 \Rightarrow 132 = \texttt{1000 0100}_2
> $$
>
> - 数值校验：$127+7 = 134$ ✓、$127+5 = 132$ ✓；反向 $134-127 = 7$、$132-127 = 5$ ✓。
> - **为什么用偏移（讲义 p.60）**，两个理由：
>   1. **阶码永远非负** —— 8 位字段可直接当无符号整数用，因此**正有限浮点数**可按无符号位串排序；负值需反转排序，零与 NaN 需按浮点语义处理。校验：$228 \to 0x43640000 = 1\,130\,627\,072$、$58.25 \to 0x42690000 = 1\,114\,177\,536$，前者更大而 $228 > 58.25$ ✓（若阶码用补码存，负阶码最高位是 1，无符号比较立刻失效）。
>   2. **为特殊值统一留出端点** —— bias 是编码约定；IEEE 754 把最小字段
>      让给 $0$ 与 denormal、最大字段让给 $\pm\infty$ 与 NaN，普通数占 $[-126,+127]$，两端刚好不浪费。
>
> **5. 精度与动态范围**
>
> $$
> \text{ULP}(1.0) = 2^{-23}\approx1.19\times10^{-7},\qquad
> x_{\min}^{\text{normal}} = 2^{-126}\approx1.18\times10^{-38},\qquad
> x_{\max} = (2-2^{-23})\times2^{127}\approx3.40\times10^{38}
> $$
>
> - 意义：**相对分辨率数量级近似固定、绝对分辨率随指数变化**。$1.0$ 及其上方正规区间的相邻间隔是 $2^{-23}$（下方区间间隔为 $2^{-24}$）；到 $2^{20}$ 附近间隔变成
>   $2^{-3} = 0.125$ —— 这就是"大数吃小数"（$10^{8}+1 = 10^{8}$，该处 ULP $\approx 8$）。
> - 数值校验：$2^{-23} = 1.1920928955078125\times10^{-7}$ ✓；$2^{-126} = 1.1754943508222875\times10^{-38}$ ✓；
>   $(2-2^{-23})\times2^{127} = 3.4028234663852886\times10^{38}$ ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — $228$ 的 IEEE 754 单精度（讲义 p.59）**
>
> 题目：用 32 位浮点表示 $228_{10}$。
>
> 解：
> 1. $228 = 128+64+32+4 = 1110\,0100_2$，$S = 0$（正数）。
> 2. 规格化：$1110\,0100 = 1.11001\times2^{7}$，故 $E = 7$、$F = 11001$。
> 3. 阶码字段：$127+7 = 134 = \texttt{1000 0110}_2$。
> 4. 尾数字段：`11001` 后补 18 个 0 → `11001000000000000000000`。
> 5. 拼接：`0 10000110 11001000000000000000000` = `0100 0011 0110 0100 …` $= 0x43640000$。
>
> **数值校验 (Numerical check)**：回读 $1.11001_2 = 1.78125$，$1.78125\times2^{7} = 228$ ✓；
> 阶码 $134-127 = 7$ ✓；十六进制字段拆解与第 5 步逐位一致 ✓。
>
> **Example 2 — $-58.25$ 的 IEEE 754 单精度（讲义 p.61）**
>
> 题目：写出 $-58.25_{10}$ 的 binary32 编码。
>
> 解：
> 1. 绝对值：$58 = 111010_2$，$0.25 = 0.01_2$ → $58.25 = 111010.01_2$，$S = 1$。
> 2. 规格化：$111010.01 = 1.1101001\times2^{5}$，$E = 5$、$F = 1101001$。
> 3. 阶码字段：$127+5 = 132 = \texttt{1000 0100}_2$。
> 4. 尾数字段：`1101001` 后补 16 个 0 → `11010010000000000000000`。
> 5. 拼接：`1 10000100 11010010000000000000000` = `1100 0010 0110 1001 …` $= 0xC2690000$。
>
> **数值校验 (Numerical check)**：$1.1101001_2 = 1.8203125$，$1.8203125\times2^{5} = 58.25$ ✓，符号位 1 → $-58.25$ ✓；
> $132-127 = 5$ ✓；与例 1 对比，$228$ 的阶码字段 $134 > 132$ 也正确反映了量级 ✓。
>
> **Example 3 — 反解：`0x43640000` 是多少？**
>
> 题目：把 `0x43640000` 拆字段还原成十进制。
>
> 解：
> 1. 二进制：`0100 0011 0110 0100 0000 0000 0000 0000` → `0 | 10000110 | 11001000000000000000000`。
> 2. $S = 0$（正）；阶码字段 $= 134$ → $E = 134-127 = 7$。
> 3. 尾数 $= 1.11001$（补上隐含的 1）。
> 4. 值 $= 1.78125\times2^{7} = 228.0$。
>
> **数值校验 (Numerical check)**：$228 \to 0x43640000 \to 228.0$ 往返一致 ✓（讲义 p.59 的原例就是 $228$）。
> 若忘记隐含的 1（把尾数当 $0.11001$），会算成 $0.78125\times128 = 100$，与 $228$ 相差 $2.28$ 倍 —— 这就是最经典的错法。
>
> **Example 4 — 为什么 $0.1$ 存不精确**
>
> 题目：写出 $0.1$ 的 binary32 编码，并算出存储误差。
>
> 解：
> 1. $0.1 = 0.0001100110011\dots_2$（因为 $0.1 = 1.6\times2^{-4}$，而 $1.6 = 1.1001100110011\dots_2$ 无限循环）。
> 2. 规格化：$1.10011001100110011001101\times2^{-4}$（23 位尾数按就近舍入，末位进 1）。
> 3. 阶码字段：$127+(-4) = 123 = \texttt{0111 1011}_2$。
> 4. 拼接：`0 01111011 10011001100110011001101` $= 0x3DCCCCCD$。
>
> **数值校验 (Numerical check)**：该位串的真实值是 $0.10000000149011612$，误差 $1.49011612\times10^{-9}$；
> 此处 ULP $= 2^{-4-23} = 2^{-27} = 7.4505806\times10^{-9}$，误差 $\approx 0.2$ ULP ✓（符合"就近舍入"）；
> 相对误差 $1.49\times10^{-8}\approx2^{-26}$，落在 $2^{-24}$ 之内 ✓。结论：`0.1` 打印成 `0.1` 只是
> 最短十进制输出对该存储值的显示。binary64 中 `0.1 + 0.2 == 0.3` 为假；
> 若每步严格按 binary32 round-to-nearest 舍入，该比较可为真，不能把这个反例当成所有格式的定律。
>
> **Decode the format before the fields · 先确认格式再读字段**
>
> Floating-point decoding has two levels. First identify the format: field widths, bias, normalization rule, and special encodings. Then decode the fields under that format. The bias 127 belongs to binary32; it is not a universal property of every biased system or every custom floating-point word.
>
> The significand controls relative precision, while the exponent changes the scale. In the interval $[2^e,2^{e+1})$, adjacent normal binary32 values differ by $2^{e-23}$. Consequently a fixed increment that is visible near one can disappear at a much larger magnitude. More range does not imply that every integer within that range is represented exactly.
>
> **Worked application — changing spacing.** 在 $1\le x<2$ 内，binary32 spacing 为 $2^{-23}$；在 $2^{24}\le x<2^{25}$ 内，spacing 为 $2^{24-23}=2$。因此 $2^{24}$ 与 $2^{24}+2$ 可表示，而中间整数 $2^{24}+1$ 不可精确表示。round-to-nearest, ties-to-even 把该中点取成 $2^{24}$。这来自相邻数间距，不是加法器漏掉一次进位。
>
> In English: the stored precision is fixed in significant bits, so absolute spacing grows with the exponent. To assess rounding, locate the two neighboring representable values and apply the stated rounding rule.
>
> **English exam question:** A generic eight-bit biased field stores `10000010` with bias 63. Must its decoded value be 3 because binary32 uses bias 127?
>
> **Answer:** No. The specified bias is 63, so the value is $130-63=67$. With binary32's bias 127 the same exponent field would decode to 3 for a normal value. The complete floating-point number would also require its sign and fraction fields.
>
> For ordering, positive finite bit patterns increase with value; negative finite patterns increase with magnitude and therefore reverse numeric order. NaNs need separate handling. Compare [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型|Number Systems]] for bias and [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] for the distinction between raw-code and numeric comparisons.
>
> **Custom 16-bit format · 自定义十六位格式**
>
> The supplied custom format has one sign bit, four exponent bits, eleven fraction bits, and bias seven. It is **not IEEE binary16**, which uses one sign bit, five exponent bits, ten fraction bits, and bias fifteen. Field width alone does not identify a format.
>
> For a normal value in the custom model, $x=(-1)^s(1+F/2^{11})2^{E-7}$; use only the special-value rules explicitly specified for that format. IEEE zero/subnormal/infinity conventions cannot be inferred from the word “16-bit”.
>
> **Worked check.** 取s=1、E=1001₂=9、F=01000000000₂=512，值为 $-(1+512/2048)2^{9-7}=-1.25\times4=-5$。把bias错用15会得到−0.01953125，错误来自format，不是补码符号处理。

## 4 · 编码例与精度边界

$10.5=(1010.1)_2=(1.0101)_2\times2^3$，因此 s=0、E=130、F 的前四位为 0101，单精度模式为 `0x41280000`。指数增加，绝对间距也增加；扩大动态范围不等于所有数都更精确。

> [!IMPORTANT] 格式先于数值
> 相同位串可代表不同定点尺度或不同浮点格式。自定义 16 位格式必须重新给出字段长度、偏置和特殊码规则，不能直接套用单精度公式。

### 精度边界、特殊值与格式误用

对正正规 binary32 区间 $[2^e,2^{e+1})$，相邻值间距为 $\operatorname{ULP}=2^{e-23}$。相对分辨率在量级上近似固定，绝对分辨率随指数变，不是精确“相对精度常数”。在 $[2^{24},2^{25})$ 中间距为 2，因此整数 $2^{24}+1$ 不可精确存储；round-to-nearest, ties-to-even 将它舍入为 $2^{24}$。在 $10^8$ 附近 ULP=8，该模式下加 1 后仍为 $10^8$。

binary32 的 $0.1$ 为 `0x3DCCCCCD`，真实存储值约 0.10000000149011612；分母含 5，不能在有限二进制中精确表示。binary64 的 `0.1+0.2==0.3` 通常为假，严格逐步 binary32 最近舍入时可为真，必须同时说明格式和舍入。

NaN 的 IEEE 数值相等比较为假，包括与自身；使用 `isnan` 检查更清楚。+0 与 −0 相等，但在允许 IEEE 非陷阱除法结果的模式中，$1/(+0)=+\infty$、$1/(-0)=-\infty$。语言、硬件或配置可能对除零抛出异常，应把数值规则与执行环境区分。

自定义 16 位格式须重新给出 sign/exponent/fraction 位数、bias、隐含位和特殊码约定。课内补充的 1/4/11、bias 7 模型不等于 IEEE binary16 的 1/5/10、bias 15。已有折叠例子 s=1、E=9、F=512 按该自定义正规公式为 −5；不能套 binary32 的 bias 127。

## 5 · 重点回忆

定点：范围、分辨率、缩放和中间宽度。浮点：规格化、偏置、隐含位、特殊码与舍入。有限表示误差是表示法的问题，不能只靠增加算术模块消除。

先修连接 [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|二进制位权]]、[[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|小数转换与有限表示条件]]、[[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|位宽]]，以及 [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|补码]]。Q 格式继承补码的负权和非对称范围；浮点符号独立、指数偏置，并非“整字都换为补码或偏移码”。两种表示都先约定格式再解释模式。

定点运算连接 [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确|中间宽度与移位规则]]；读原始浮点位串的大小连接 [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|比较器解释]]。

## Sources · 课件依据

主线课件：[Ch2 lecture](../ECE2050-Chap2.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
