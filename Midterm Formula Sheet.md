---
tags:
  - ECE2050
  - review
date: 2026-10-20
updated: 2026-10-20
chapter: Ch1–6
aliases:
  - Midterm Formula Sheet
  - ECE2050 期中公式表
  - 数字逻辑期中公式与条件
---

# Midterm Formula Sheet · 期中公式与适用条件

> [!SUMMARY] Recall with conditions · 连同条件一起记
> 原理与范围见 [[Midterm Review Guide]]，练习见 [[Midterm Practice and Answers]]。本次考试闭卷，本表用于考前回忆。每次默写同时说明：**变量含义、位宽、编码、有效极性和成立条件**。

**统一记号：** 布尔式中 $+$ 为 OR，相乘为 AND，$\bar A$ 为 NOT，$\oplus$ 为 XOR；数值式中的加减乘除采用普通算术。位编号从最低位 0 开始，最高位为 $n-1$。$A_i,B_i\in\{0,1\}$；$C_i$ 是第 i 位的进位输入，$C_{i+1}$ 是该位的进位输出。时间单位为 s，频率 Hz，电压 V；位串与纯数字编码无量纲。

## 1 · Waveforms and Bit Counts · 波形与位宽

周期为 $T$，高电平持续时间为 $t_H$，低电平持续时间为 $t_L$：

$$T=t_H+t_L,\qquad f=\frac1T,\qquad D_H=\frac{t_H}{T}\times100\%.$$

适用于周期信号。低有效脉冲若问有效占空比，应以 $t_L$ 为分子。$t_r,t_f$ 描述边沿时间，不能代替 $T$ 或传播延迟。

$$n\text{ 位码数}=2^n,\qquad n\text{ 变量真值表行数}=2^n.$$

表示 N 种可区分状态所需最少编码位数为 $\lceil\log_2N\rceil$；表示整数 0 到 M（含两端）为：

$$n_{min}=\lceil\log_2(M+1)\rceil.$$

以上是编码的信息位数；单一常量在数学上可无编码位，实际接口通常至少保留一位。

## 2 · Radix and Integer Representations · 数制与整数

### 2.1 位权与范围

基数 $R\ge2$，数字 $a_i\in\{0,1,\ldots,R-1\}$，m 位小数、n 位整数：

$$x=\sum_{i=-m}^{n-1}a_iR^i.$$

| 解释方式（总宽 n） | 数值 | 范围与注意事项 |
|---|---|---|
| 无符号 unsigned | $U=\sum_{i=0}^{n-1}b_i2^i$ | $0\le U\le2^n-1$ |
| 原码 sign-magnitude | $x=(-1)^{b_{n-1}}\sum_{i=0}^{n-2}b_i2^i$ | $-(2^{n-1}-1)\le x\le2^{n-1}-1$，两个零 |
| 补码 two's complement | $x=-b_{n-1}2^{n-1}+\sum_{i=0}^{n-2}b_i2^i$ | $-2^{n-1}\le x\le2^{n-1}-1$，一个零 |
| 偏置 biased code | $x=U-B_{bias}$ | $-B_{bias}\le x\le2^n-1-B_{bias}$ |

补码也可由无符号码 U 解读：

$$x=\begin{cases}U,&b_{n-1}=0,\\U-2^n,&b_{n-1}=1.\end{cases}$$

扩宽时：无符号前补 0；补码前补原符号位。1 octal digit = 3 bits，1 hex digit = 4 bits，1 nibble = 4 bits，1 byte = 8 bits。

### 2.2 求负、加减与溢出

对 n 位模式 X，逐位取反为 $\bar X$；以下结果均只保留低 n 位：

$$(-X)\bmod2^n=(\bar X+1)\bmod2^n,$$
$$A-B\equiv A+\bar B+1\pmod{2^n}.$$

最小补码 $-2^{n-1}$ 的正值不能在同宽表示；求负会回到相同位串，并发生有符号溢出。

令 $a_s,b_s,r_s$ 为两个操作数与结果 R 的符号位：

$$V_{add}=\overline{a_s\oplus b_s}\,(a_s\oplus r_s),$$
$$V_{sub}=(a_s\oplus b_s)(a_s\oplus r_s).$$

对于对应的 n 位加法器（减法用 $A+\bar B+1$ 实现），也可用：

$$V=C_{n-1}\oplus C_n.$$

这里 $C_{n-1}$ 是进入符号位的进位，$C_n$ 是符号位输出进位。无符号加法溢出直接看 $C_n$；有符号结果的符号看 $r_s$，不能看额外进位。采用上述加法器减法约定时，无符号减法 $C_n=1$ 表示无借位，$C_n=0$ 表示借位；其他题目若另定义 borrow 输出，应按其定义。

### 2.3 乘除的位宽与复核

两个 n 位整数的完整乘积使用至多 2n 位。无符号部分积为：

$$AB=\sum_{i=0}^{n-1}\sum_{j=0}^{n-1}(A_iB_j)2^{i+j}.$$

补码乘法不能把符号位当正权直接套此式；可先求幅值再处理符号，或使用正确的有符号部分积方法。

整数除法的复核关系（除数 B 非零）为：

$$A=BQ+R,\qquad |R|<|B|.$$

若题目采用向零截断，则非零 R 与 A 同号。商的符号由操作数是否同号决定；零和最小补码除以 −1 需独立检查。

## 3 · Fixed and Floating Point · 定点与浮点

### 3.1 课程的 U a.b / Q a.b 约定

小数位数 b，总宽 $N=a+b$；$I_u,I_s$ 分别是按无符号/补码解释的整数：

$$x=I\,2^{-b},\qquad\Delta=2^{-b}.$$

| 格式 | 范围 |
|---|---|
| U a.b | $0\le x\le2^a-2^{-b}$ |
| Q a.b（a **含符号位**） | $-2^{a-1}\le x\le2^{a-1}-2^{-b}$ |

编码：$I=\operatorname{round}(x2^b)$ 或按题意截断，再检查 I 的整数范围。最近值舍入且未越界时，绝对量化误差不超过 $\Delta/2$。向零截断的误差绝对值小于 $\Delta$；直接丢掉补码低位可能对应向负无穷取整，不能与向零截断混称。

$$x_1x_2=(I_1I_2)2^{-(b_1+b_2)}.$$

乘积小数位数相加；相加前先对齐尺度。饱和到范围 $[L,U]$：

$$\operatorname{sat}(x)=\min\bigl(U,\max(L,x)\bigr).$$

例如 Q4.4：步长 1/16，范围 [−8,7.9375]；Q1.15：[−1,1−2⁻¹⁵]。

### 3.2 IEEE 754 binary32

符号位 s、8 位无符号指数字段 E、23 位无符号小数字段 F；实际指数 e：

$$e=E-127.$$

正规数仅用于 $1\le E\le254$：

$$x=(-1)^s\left(1+\frac{F}{2^{23}}\right)2^{E-127}.$$

| 字段条件 | 解码规则 |
|---|---|
| E=0，F=0 | +0 或 −0，由 s 决定 |
| E=0，F≠0 | 次正规数：$x=(-1)^s(F/2^{23})2^{-126}$ |
| 1≤E≤254 | 正规数，隐含前导 1，e=−126…127 |
| E=255，F=0 | +∞ 或 −∞ |
| E=255，F≠0 | NaN |

正规正数区间 $[2^e,2^{e+1})$ 中相邻值间距为 $2^{e-23}$。最小正规正数 $2^{-126}$；最小次正规正数 $2^{-149}$；最大有限正数 $(2-2^{-23})2^{127}$。后面这些边界是字段公式的推导结果；课件重点是字段、偏置、规格化与特殊值。

**量级核验：** 正规数应满足 $2^e\le|x|<2^{e+1}$。−58.25 → `0xC2690000`；228 → `0x43640000`。

## 4 · BCD, Gray, Parity and CRC · 编码与检错

### 4.1 BCD 加法修正

对两位合法十进制数字 a、b（0–9）及十进制输入进位 $c\in\{0,1\}$，先作普通二进制和 $T=a+b+c$。其低四位为 $S_3S_2S_1S_0$，原始高位进位为 $C_4$：

$$K=C_4+S_3S_2+S_3S_1.$$

K=1 时低四位加 `0110` 并取低四位；十进制输出进位为 K。等价数值规则：若 T≥10，则个位=T−10、十进制进位=1；否则个位=T、进位=0。别漏掉 T≥16 时低四位看似不大于 9、但 $C_4=1$ 的情况。

### 4.2 二进制与反射 Gray 码

n 位二进制 B 与 Gray 码 G：

$$G_{n-1}=B_{n-1},\qquad G_i=B_{i+1}\oplus B_i\quad(0\le i<n-1).$$

整体表示：$G=B\oplus(B\gg1)$，其中 $\gg1$ 为补 0 逻辑右移。

逆变换：

$$B_{n-1}=G_{n-1},\qquad B_i=B_{i+1}\oplus G_i
=\bigoplus_{k=i}^{n-1}G_k.$$

例：`101101` → `111011`。Gray 不用普通二进制位权直接解码，也不是普通二进制直接加 1。

### 4.3 奇偶位与检查

数据位为 $d_0,\ldots,d_{n-1}$，校验位 p；总码组奇偶目标 $q=0$ 表示偶、$q=1$ 表示奇：

$$p_{even}=\bigoplus_i d_i,\qquad
p_{odd}=\overline{\bigoplus_i d_i}.$$

接收组各位为 $r_j$（含 p），错误指示为：

$$E_{parity}=\left(\bigoplus_j r_j\right)\oplus q.$$

E=1 检出错误；E=0 未检出错误。只保证检出奇数个位翻转，不保证全部多位错误。

### 4.4 课程手算 CRC（无额外反射/初值/最终异或）

数据多项式 $D(x)$，生成多项式 $G(x)$ 的次数为 r，生成位串长 r+1，余数为 $R(x)$：

$$R(x)=x^rD(x)\bmod G(x),\qquad
T(x)=x^rD(x)\oplus R(x).$$

$$T(x)\bmod G(x)=0.$$

按 GF(2) 除法，无进位、借位；余数补足 r 位。若错误模式为 $E(x)$，接收码 $T\oplus E$ 检不出该错误的条件是 $G(x)\mid E(x)$。生成式最高项为 1、常数项为 1 且次数≥1 时，可检出所有单比特错误；r 次生成式可检出长度不超过 r 的所有非零突发错误，需要常数项为 1。课程的 G=`1010` 常数项为 0，应单独按给定除法计算，不套常用生成式的全部保证。

**已复核例：** D=`1101`、G=`101` → 余数 `10`、发送 `110110`；当前 Ch2 p.71 的 D=`11010011`、G=`1010` → 余数 `010`、发送 `11010011010`。

### 4.5 ASCII 字符编码

标准 ASCII 为 7 位，共 $2^7=128$ 个码。十进制数字 $d\in\{0,\ldots,9\}$ 对应的字符码为：

$$c_{ASCII}=\texttt{0x30}+d,\qquad d=c_{ASCII}-\texttt{0x30}.$$

逆式只适用于字符码 0x30–0x39。`'A'` 为 0x41，`'a'` 为 0x61；对应英文字母的大小写差为 0x20，不能把该偏移套到所有字符上。

## 5 · Logic Gates · 门与真值表

| A | B | AND AB | OR A+B | NAND | NOR | XOR | XNOR |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |

$$A\oplus B=\bar AB+A\bar B,\qquad
\overline{A\oplus B}=AB+\bar A\bar B.$$

$$A\oplus0=A,\quad A\oplus1=\bar A,\quad A\oplus A=0.$$

n 输入 XOR 为 $\bigoplus_i A_i$，输出 1 当且仅当 1 的个数为奇数。n 输入 XNOR 若指整个 XOR 输出取反，则为偶数性；多级二输入 XNOR 的任意串接不能一概当作同一个 n 输入 XNOR。

## 6 · Electrical Levels · 电平、静态曲线与噪声

驱动端 d、接收端 r，均取题目条件下的最坏保证值：

$$NM_H=V_{OH(min),d}-V_{IH(min),r},$$
$$NM_L=V_{IL(max),r}-V_{OL(max),d}.$$

HIGH 向下退化 $\delta_H$、LOW 向上退化 $\delta_L$（均取非负幅度，单位 V）后：

$$V_{H,recv,min}=V_{OH(min),d}-\delta_H,\qquad
V_{L,recv,max}=V_{OL(max),d}+\delta_L.$$

分别要求 $V_{H,recv,min}\ge V_{IH(min),r}$、$V_{L,recv,max}\le V_{IL(max),r}$；剩余预算为 $NM_H-\delta_H$、$NM_L-\delta_L$。同向且可能同时发生的扰动需合计。

$$NM_H+NM_L=(V_{OH}-V_{OL})-(V_{IH}-V_{IL}),$$

这里四个量仍分别来自正确的驱动/接收端。对称、轨到轨、门限为 VDD/2 的理想模型才有 $NM_H=NM_L=V_{DD}/2$；不能推广到全部真实门。

静态传输曲线的局部电压增益为 $A_v=dV_{out}/dV_{in}$，量纲为 V/V；缓冲器过渡区为正斜率，反相器为负斜率。按图示单位增益点可读输入阈值；指定保证门限时直接用指定参数。静态斜率不是传播延迟。

## 7 · Boolean Laws · 布尔定律

以下 X、Y、Z 可代表任意布尔子表达式。

| 规则 | AND / OR 及对偶形式 |
|---|---|
| 恒等 identity | $X+0=X$；$X\cdot1=X$ |
| 支配 domination | $X+1=1$；$X\cdot0=0$ |
| 幂等 idempotent | $X+X=X$；$XX=X$ |
| 互补 complement | $X+\bar X=1$；$X\bar X=0$ |
| 双反 involution | $\bar{\bar X}=X$ |
| 交换 commutative | $X+Y=Y+X$；$XY=YX$ |
| 结合 associative | $X+(Y+Z)=(X+Y)+Z$；$X(YZ)=(XY)Z$ |
| 分配 distributive | $X(Y+Z)=XY+XZ$；$X+YZ=(X+Y)(X+Z)$ |
| 吸收 absorption | $X+XY=X$；$X(X+Y)=X$ |
| 消变量 combining | $XY+X\bar Y=X$；$(X+Y)(X+\bar Y)=X$ |
| 冗余文字消去 | $X+\bar XY=X+Y$；$X(\bar X+Y)=XY$ |
| 德摩根 DeMorgan | $\overline{XY}=\bar X+\bar Y$；$\overline{X+Y}=\bar X\bar Y$ |
| 共识 consensus | $XY+\bar XZ+YZ=XY+\bar XZ$ |
| 共识对偶 | $(X+Y)(\bar X+Z)(Y+Z)=(X+Y)(\bar X+Z)$ |

求整个式子的反：改变 AND/OR，并对每个变量或子式取反。求对偶：交换 AND/OR、0/1，变量上的横线保持原样。证明可代数推导，或穷举全部 $2^n$ 个输入。

## 8 · Canonical Forms and K-Maps · 标准式与卡诺图

变量顺序为 $A_{n-1}\cdots A_0$，行号 j 的二进制位为 $j_i$：

$$m_j=\prod_{i=0}^{n-1}\begin{cases}A_i,&j_i=1,\\\bar A_i,&j_i=0,\end{cases}$$

$$M_j=\sum_{i=0}^{n-1}\begin{cases}\bar A_i,&j_i=1,\\A_i,&j_i=0.\end{cases}$$

$$F=\sum_{j:F(j)=1}m_j=\Sigma m(S_1),\qquad
F=\prod_{j:F(j)=0}M_j=\Pi M(S_0).$$

完全指定函数的 $S_1,S_0$ 互为全集 $\{0,\ldots,2^n-1\}$ 中的补集。有 X 时，X 属于未规定集合；选定其实现前不能把它同时当作强制 0 和强制 1。

例：ABC=101 对应 $m_5=A\bar BC$、$M_5=\bar A+B+\bar C$。补全缺失变量：

$$P=P(X+\bar X)=PX+P\bar X,$$
$$S=(S+X)(S+\bar X).$$

K-map 共 $2^n$ 格；合法 $2^k$ 格的一组保留 $n-k$ 个不变变量。圈 1 读乘积：固定 1 用原变量、固定 0 用反变量；圈 0 读和项：固定 0 用原变量、固定 1 用反变量。行列顺序为 Gray 顺序，允许跨边界、允许重叠、不允许对角相邻。

## 9 · Universal Gates and Common Specifications · 通用门与设计约束

### 9.1 全 NAND / 全 NOR

| 目标 | 只用 NAND | 只用 NOR |
|---|---|---|
| NOT A | $\operatorname{NAND}(A,A)$ | $\operatorname{NOR}(A,A)$ |
| A AND B | NAND(A,B) 后接同输入 NAND 反相 | NOR(NOR(A,A),NOR(B,B)) |
| A OR B | NAND(NAND(A,A),NAND(B,B)) | NOR(A,B) 后接同输入 NOR 反相 |

$$AB+CD=\overline{\overline{AB}\cdot\overline{CD}},$$
$$ (A+B)(C+D)=\overline{\overline{A+B}+\overline{C+D}}.$$

前者可用三只二输入 NAND，后者用三只二输入 NOR。三输入以上的门若需拆成二输入门，必须处理反相；NAND/NOR 不满足普通 AND/OR 那样的结合律。

### 9.2 恰好、至少与优先

四个高有效输入 ABCD：

$$F_{exactly\,3}=\bar ABCD+A\bar BCD+AB\bar CD+ABC\bar D
=\Sigma m(7,11,13,14),$$
$$F_{at\,least\,3}=ABC+ABD+ACD+BCD.$$

三输入多数函数为 $F_{majority}=AB+AC+BC$。

四路高有效优先编码，$D_3$ 最高，输出二位二进制 $E_1E_0$ 与有效位 V：

$$E_1=D_3+D_2,\qquad E_0=D_3+\bar D_2D_1,$$
$$V=D_3+D_2+D_1+D_0.$$

V=0 时 E 代码没有“第 0 路已有效”的含义。该式不是 74HC147 的物理低有效引脚方程；移到具体芯片须重新解释输入/输出极性。

## 10 · Adders and Multipliers · 加法器与乘法器

### 10.1 HA / FA 与位权

$$S_{HA}=A\oplus B,\qquad C_{HA}=AB,$$
$$S_{FA}=A\oplus B\oplus C_{in},$$
$$C_{FA}=AB+AC_{in}+BC_{in}=AB+(A\oplus B)C_{in}.$$

普通整数意义下：$A+B=S_{HA}+2C_{HA}$；$A+B+C_{in}=S_{FA}+2C_{FA}$。FA=两个 HA+一个 OR。n 位无符号全和是 $C_nS_{n-1}\cdots S_0$；若结果声明 n 位，则保留 sum 并另行检查溢出。

### 10.2 本课 OR 传播的 CLA

$$G_i=A_iB_i,\qquad P_i=A_i+B_i,\qquad C_{i+1}=G_i+P_iC_i.$$

$$C_1=G_0+P_0C_0,$$
$$C_2=G_1+P_1G_0+P_1P_0C_0,$$
$$C_3=G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0,$$
$$C_4=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0+P_3P_2P_1P_0C_0.$$

四位块：

$$P_{blk}=P_3P_2P_1P_0,\qquad
G_{blk}=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0,$$
$$C_4=G_{blk}+P_{blk}C_0.$$

**sum 始终为** $S_i=A_i\oplus B_i\oplus C_i$。若另定义 $P_i^{xor}=A_i\oplus B_i$，同样可用于进位关系，且这时才有 $S_i=P_i^{xor}\oplus C_i$。

### 10.3 串行进位延迟模型

各级相同、A/B 已就绪、进位传播时间为 $t_C$、进位到 sum 时间为 $t_S$，仅沿 $C_0$ 传播时：

$$t_{C_0\to C_n}\approx n t_C,\qquad
t_{C_0\to S_{n-1}}\approx(n-1)t_C+t_S.$$

这是指定路径和输入到达条件下的模型。完整最坏延迟还需比较 A/B 到首级进位、其他数据到输出等路径，不能对任何加法器无条件套用 n 倍一个“门延迟”。

### 10.4 二位无符号乘法器

令 $p_{ij}=A_iB_j$：

$$Z_0=p_{00},\quad Z_1=p_{10}\oplus p_{01},\quad k=p_{10}p_{01},$$
$$Z_2=p_{11}\oplus k,\qquad Z_3=p_{11}k.$$

实现需四个 AND、两个 HA；检验 $Z_3Z_2Z_1Z_0=AB$。更大乘法器按相同列权规则加入 HA/FA，不能把 carry 留在原权重列。

## 11 · Comparators · 比较器

令 $e_i=\overline{A_i\oplus B_i}$ 表示第 i 位相等。无符号数比较：

$$EQ=\prod_{i=0}^{n-1}e_i,$$
$$GT=\sum_{i=0}^{n-1}A_i\bar B_i\prod_{k=i+1}^{n-1}e_k,\qquad
LT=\sum_{i=0}^{n-1}\bar A_iB_i\prod_{k=i+1}^{n-1}e_k.$$

空乘积按 1 处理。两位例：

$$GT=A_1\bar B_1+e_1A_0\bar B_0,\quad
LT=\bar A_1B_1+e_1\bar A_0B_0,\quad EQ=e_1e_0.$$

分成高位块 H、低位块 L 的级联：

$$GT=GT_H+EQ_HGT_L,\quad LT=LT_H+EQ_HLT_L,\quad EQ=EQ_HEQ_L.$$

74HC85 最低块初值 $(GT_{in},EQ_{in},LT_{in})=(0,1,0)$。这些大小公式按无符号解释；补码异号时先比较符号，同号时可使用同宽位串的无符号大小关系。

## 12 · Decoders and Displays · 译码与显示

### 12.1 译码与编码

n-to-2ⁿ 译码器输入 A、正逻辑有效条件 EN，j 号高有效输出 $D_j$、低有效输出 $L_j$：

$$D_j=EN\,m_j(A),\qquad L_j=\overline{EN\,m_j(A)}.$$

使能时：

$$F=\sum_{j\in S_1}D_j=\overline{\prod_{j\in S_1}L_j}.$$

低有效最小项接 **NAND** 得原函数；接 AND 会得到其反。74HC154 外部两个低有效片选 $\overline{CS_1},\overline{CS_2}$ 所对应的电平为 $c_1,c_2$ 时，内部 $EN=\bar c_1\bar c_2$，即两脚都为 0 才使能。

普通 4-to-2 高有效 one-hot 编码器：$E_1=D_2+D_3$、$E_0=D_1+D_3$，只在输入满足 one-hot 规格时解释为线路代码。多路同时有效应使用优先规则，见第 9 节。

### 12.2 七段常见字形

段位 a 为顶、b 右上、c 右下、d 底、e 左下、f 左上、g 中。下表列出应点亮的段；采用常见字形，题目另给字形时以题目为准。

| 数字 | 点亮段 | 数字 | 点亮段 |
|---|---|---|---|
| 0 | abcdef | 5 | acdfg |
| 1 | bc | 6 | acdefg |
| 2 | abdeg | 7 | abc |
| 3 | abcdg | 8 | abcdefg |
| 4 | bcfg | 9 | abcdfg |

对合法 BCD 输入 ABCD（8、4、2、1），取 10–15 为 don't-care，段 a 的**高有效点亮函数**可化简为：

$$a_{on}=A+C+BD+\bar B\bar D.$$

低有效段输出则为 $a_{out}=\overline{a_{on}}$。该式描述普通译码，不含 LT、BI、RBI 等覆盖条件；消零与灯测按芯片控制表处理。

## 13 · MUX, DEMUX and Tri-State · 选择、分配与三态

二选一 MUX，选择 S，数据 $D_0,D_1$，高有效输出：

$$Y=\bar SD_0+SD_1.$$

四选一，$S_1$ 高位、$S_0$ 低位：

$$Y=\bar S_1\bar S_0D_0+\bar S_1S_0D_1+S_1\bar S_0D_2+S_1S_0D_3.$$

一般 $2^s$ 选一：$Y=\sum_{j=0}^{2^s-1}m_j(S)D_j$。有输出使能或反相输出时必须再按器件规格处理。

香农展开 (Shannon expansion)，$F_{S=0}$、$F_{S=1}$ 是固定 S 后的余因子：

$$F=\bar S F_{S=0}+S F_{S=1}.$$

固定所有选择变量后，剩余一变量 X 的输出对 $(F(0),F(1))$ 与数据接法为：

| 输出对 | 数据端 |
|---|---|
| 00 | 0 |
| 01 | X |
| 10 | $\bar X$ |
| 11 | 1 |

高有效 DEMUX、输入数据 D：$Y_j=D\,m_j(S)$。三态缓冲器的高有效使能 EN：

$$Y=\begin{cases}D,&EN=1,\\Z,&EN=0.\end{cases}$$

Z 是高阻电气状态，不能作为普通 0/1 代入布尔式。共享总线的有效驱动数应≤1；驱动数为 0 时还要考虑偏置/保持条件。

## 14 · Delay and Hazards · 延迟与冒险

给定一条路径 p，门传播/污染延迟为 $t_{pd,g},t_{cd,g}$：

$$t_{pd,circuit}=\max_p\sum_{g\in p}t_{pd,g},\qquad
t_{cd,circuit}=\min_p\sum_{g\in p}t_{cd,g}.$$

这是题目采用门延迟、忽略或已计入连线延迟的模型；实际需按能被激活的路径与相应工作条件计算。输入变化后的最早可能改变受 $t_{cd}$ 限定，保证最终稳定受 $t_{pd}$ 限定。若题目专门给平均延迟 $(t_{PLH}+t_{PHL})/2$，那是平均口径，不能代替最坏上界。

静态 1 冒险的共识桥：

$$F=XY+\bar XZ\quad\longrightarrow\quad F_{safe}=XY+\bar XZ+YZ.$$

对偶静态 0：

$$F=(X+Y)(\bar X+Z)\quad\longrightarrow\quad
F_{safe}=(X+Y)(\bar X+Z)(Y+Z).$$

稳态函数不变；消除对应**单输入变化**造成的静态冒险，须在原两级逻辑与覆盖条件下理解。课件例：$\bar A\bar B+BC$ 加 $\bar AC$。不能由共识项保证所有多输入变化或多级动态冒险均消失。

## 15 · Supplement · 大纲或旧卷中的补充量

下列内容用于补全概念；当前六章课件没有像主线公式那样展开完整模型。扇出定义见旧卷 2023 Q1(8)，Power 列于本学期课程大纲 Ch3。

相同输入负载、仅按稳态电流限制时，扇出上限估算为：

$$FO_{DC}=\left\lfloor\min\left(\frac{|I_{OH,max}|}{|I_{IH}|},\frac{|I_{OL,max}|}{|I_{IL}|}\right)\right\rfloor.$$

I 为 A；分子是保持输出保证电压的可用驱动电流，分母为每个负载相应输入电流。负载电容、频率和边沿速度仍可能进一步限制实际扇出。

电源平均功耗的基本定义：$P=V_{DD}I_{avg}$。理想 CMOS 电容开关估算：

$$P_{switch}\approx\alpha_{01}C_LV_{DD}^2f,$$

其中 $C_L$ 为 F，$f$ 为 Hz，$\alpha_{01}$ 是每个时钟周期的平均 0→1 充电次数。结果单位 W；它只估计充放电开关部分，不包含漏电与短路电流。若 activity 定义为双向翻转次数，系数需相应换算，不能机械套同一个 alpha。

## Sources · 公式依据与详细推导

主线公式按 [Ch1](../ECE2050-Chap1(1).pdf)、[Ch2](../ECE2050-Chap2.pdf)、[Ch3](../ECE2050-Chap3.pdf)、[Ch4](../ECE2050-Chap4.pdf)、[Ch5](../ECE2050-Chap5.pdf)、[Ch6](../ECE2050-Chap6.pdf) 及本学期 [HW1](../HW1.pdf)、[HW2](../HW2.pdf) 整理。全章页码映射及经复核的源文件笔误见 [[Midterm Review Guide]]。补码溢出、范围、余因子、比较器级联等是由相应模型展开的公式，不代表课件逐字给出。

详细解释：[[Binary Arithmetic and Signed Representation]] · [[Fixed-Point and Floating-Point Numbers]] · [[Parity and Cyclic Redundancy Checks]] · [[Boolean Forms and Algebraic Simplification]] · [[Karnaugh Map Minimization]] · [[Binary Arithmetic Circuits]] · [[Comparison Decoding and Selection]] · [[Logic Levels and Noise Margins]] · [[Propagation Delay and Logic Hazards]]。

---
索引：[[ECE2050.1]] · [[Glossary]]
