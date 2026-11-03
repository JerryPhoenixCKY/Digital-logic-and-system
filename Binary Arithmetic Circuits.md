---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
updated: 2026-10-13
chapter: Ch6
aliases:
  - 二进制算术电路
  - Binary Arithmetic Circuits
  - 二进制算术电路 · Ch6
  - Half Adder and Full Adder
  - 半加器与全加器
  - HA and FA
  - Ripple Carry and Carry Look-Ahead Adders
  - 串行进位与超前进位加法器
  - RCA and CLA
  - Binary Subtractors and Adder-Subtractors
  - 二进制减法器与加减器
  - Full subtractor
  - Combinational Multiplier
  - 组合乘法器
  - Array multiplier
  - Parallel Binary Adder
  - 并行二进制加法器
  - 74HC283
  - 74LS283
---

# Binary Arithmetic Circuits · 二进制算术电路

> [!SUMMARY] Quick recall · 英文速览
> Build arithmetic from one-bit cells. Carry logic sets adder delay; inversion plus carry-in reuses an adder for subtraction.

本篇第 1–2 节对应 [Chapter 6, PDF p.5–17](../ECE2050-Chap6.pdf#page=5)。第 3 节的减法器与第 4 节的乘法器实现是保留的扩展推导；讲义 p.55 提出用 HA/FA 设计乘法器，但未给出完整设计。

## 1 · Half Adder and Full Adder · 位权守恒

半加器 (half adder) $S=A\oplus B,C=AB$，满足算术 $A+B=2C+S$。全加器 (full adder) 加入 $C_{in}$：

$$S=A\oplus B\oplus C_{in},\qquad C_{out}=AB+AC_{in}+BC_{in}.$$

这里布尔输出均为 0/1；守恒式的加号是整数加法。两半加器加一个 OR 可构成全加器。

### Core Definition · 核心定义

半加器 (half adder) 输入 $A,B$，输出 sum $S$、carry $C$。全加器 (full adder) 另有输入进位 $C_{in}$。用整数守恒解释位权：

$$A+B=S+2C,\qquad A+B+C_{in}=S+2C_{out}.$$

等号两边这里是普通整数加法；下述 Boolean 式中的 $+$ 是 OR。不能混用两种含义。

### Derivation · 推导

总和的最低位是奇偶性：$S=A\oplus B$（HA），$S=A\oplus B\oplus C_{in}$（FA）。总和至少为 2 时需要进位，即至少两个输入为 1：

$$C=AB,\qquad C_{out}=AB+AC_{in}+BC_{in}=AB+(A\oplus B)C_{in}.$$

The first half adder gives $p=A\oplus B$ and $g=AB$. The second adds $p$ and $C_{in}$, giving $S=p\oplus C_{in}$ and $h=pC_{in}$. OR the two carry signals: $C_{out}=g+h$. They cannot both be 1 because $AB=1$ forces $p=0$.

| A | B | $C_{in}$ | S | $C_{out}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

> [!example]- Half Adder and Full Adder · 推导与例题
>
> **Worked Examples · 例题**
>
> **All HIGH.** $1+1+1=3=11_2$，因此 $S=1,C_{out}=1$。全加器不是“输入全 1 时 sum=0”，那只适用于没有 carry-in 的半加器。
>
> **Four-bit addition.** $A=1100,B=1100,C_0=0$。从 LSB 起，前两位各为 0；第 2 位 $1+1+0$ 得 $S_2=0,C_3=1$；最高位 $1+1+1$ 得 $S_3=1,C_4=1$。总输出 `1 1000`=24，低四位为 8。
>
> For unsigned interpretation, carry-out indicates that the four-bit result is insufficient. For two's complement, both inputs represent −4 and the four-bit result 1000 represents −8, so there is no signed overflow. The same physical adder supports both interpretations.
>
> **Decoder implementation.** 若 ABC 中 C 表示 carry-in，$S=\Sigma m(1,2,4,7)$，$C_{out}=\Sigma m(3,5,6,7)$。高有效 [[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 输出用 OR 合并；低有效输出则用 NAND 合并相应 minterms。

### Method and Review · 方法与复习

- Keep the initial carry explicit; tie it to 0 only for ordinary addition.
- Name every intermediate carry in a wider adder.
- 用 $A+B+C_{in}=S+2C_{out}$ 逐行校验，能够同时检查两个输出。
- The full-adder sum is a three-input parity function, not an “exactly one HIGH” detector.

**Exam question:** Can a full adder be made from two half adders alone?

**Answer:** Two half adders produce the partial sums and carries; an OR function is also needed to combine the carries. Omitting that function leaves the carry-out incomplete.

### Connections · 概念关系与应用

[[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 提供位宽与数值核对；[[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]] 与 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]] 解释 sum 的奇偶性；单元级 carry 连接成 [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径|Ripple Carry and Carry Look-Ahead Adders]]，相同单元也压缩 [[Binary Arithmetic Circuits#4 · Combinational Multiplier · 从部分积到列加法|Combinational Multiplier]] 的同权列。

## 2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径

### Parallel Binary Adders · 并行加法器的级联，p.9–10

并行二进制加法器 (parallel binary adder) 同时接收各位操作数，并不意味着内部进位没有延迟。74HC283/74LS283 在讲义中是四位加法器；两片通过进位级联 (carry cascading) 形成八位加法器。讲义用 $A_1$ 表示最低位、$A_4$ 表示最高位，本篇公式用 $A_0$ 到 $A_3$；接线时须先换好下标。

> [!example]- Two four-bit adders · 从低半字向高半字传进位
> ![[ch6-adder-cascade.png]]
> *讲义 p.10 原图：低位片的 carry-out 接高位片的 carry-in；图中电源与引脚号属于该器件示意。*
>
> 对本篇的零起始位序，低位片接 $A[3:0],B[3:0]$，高位片接 $A[7:4],B[7:4]$。普通加法令低位 $C_0=0$，并连接 $C_4\to$ 高位片输入进位；完整输出是 $C_8S_7\ldots S_0$。
>
> **Worked example / 自算例题：** $A=0011\ 1111_2=63$，$B=0000\ 0001_2=1$。低四位 $1111+0001=1\ 0000$，所以 $C_4=1$；高四位 $0011+0000+1=0100$。结果 $0100\ 0000_2=64$，$C_8=0$。若高位 carry-in 错接为 0，会得到 48。
>
> Keep both the final carry and the retained sum. The internal carry is an arithmetic connection, while supply pins and logic-level compatibility are separate electrical requirements; HC and LS names do not make their electrical limits interchangeable.

### Voting System · 全加器作为人数计数单元，p.11

讲义的投票系统 (voting system) 为六个位置分别统计 YES 与 NO。每个位置还可处于中立状态 (neutral position)；按讲义开关模型，一个人的 YES/NO 至多一者为 1。

> [!example]- Six-position voting system · 保持输出位权
> ![[ch6-voting-system.png]]
> *讲义 p.11 原图：两个三输入全加器与一个并行加法器构成一路六票计数；YES 与 NO 各有一路。*
>
> 令一路六个有效电平为 $x_0,\ldots,x_5$。第一组三个投票输入进入一个 FA，得到 $(C_a,S_a)$；第二组得到 $(C_b,S_b)$。由全加器整数守恒：
>
> $$x_0+x_1+x_2=2C_a+S_a,\qquad x_3+x_4+x_5=2C_b+S_b.$$
> $$N=2C_a+S_a+2C_b+S_b=(0\ 0\ C_a\ S_a)_2+(0\ 0\ C_b\ S_b)_2.$$
>
> 将两组的 sum 接各操作数的最低位，carry 接次低位，其余高位和输入进位接逻辑 0。两位小计各为 0–3，相加为 0–6，三位计数结果足够；补一个最高位 0 便形成合法的四位 8421 BCD，可送入 [[Seven-Segment Display and Code Conversion]]。
>
> **Self-calculated check：** YES 输入 `101101` 有四票；两组三票各得小计 2=`10`，总数 `100`=4。若 NO 有一票，则中立有 $6-4-1=1$ 人。存在中立状态时，NO 不能直接用 $6-\text{YES}$ 代替。
>
> Each FA counts three equal-weight requests. Its carry has weight two; treating sum and carry as two equal-weight votes breaks conservation. The stable-input model counts levels and does not itself debounce the mechanical switches.

### Carry Recurrence · 逐位递推

串行进位加法器 (ripple carry adder, RCA) 逐位传递。定义 $G_i=A_iB_i$、$P_i=A_i\oplus B_i$，则 $C_{i+1}=G_i+P_iC_i$。展开得 $C_2=G_1+P_1G_0+P_1P_0C_0$；更多位同理。

超前进位加法器 (carry look-ahead adder, CLA) 并行生成展开条件，用更多门和负载换较少级数。若采用 OR 传播定义，须明确方程约定；和位仍使用 XOR。RCA 估算按完整进位链，不能只算一级全加器。

### Core Definition · 核心定义

第 $i$ 位输入 $A_i,B_i$，$C_i$ 为该位输入进位，$C_{i+1}$ 为输出进位。采用 XOR propagate：

$$G_i=A_iB_i,\quad P_i=A_i\oplus B_i,\quad C_{i+1}=G_i+P_iC_i,\quad S_i=P_i\oplus C_i.$$

$G_i$ (generate) 表示不管前级如何都产生进位；$P_i$ (propagate) 表示前级进位能够传到后级。

OR propagate $P_i^{OR}=A_i+B_i$ 也可用于同一个 carry recurrence，因为 $G_i=1$ 时已经保证 carry=1。但是 OR propagate 不能直接替代 sum 式中的 XOR。Neither convention changes the arithmetic result.

### Lecture Notation and Block Carry · 讲义采用 OR 传播，p.13–17

讲义写进位产生 (carry generation) $C_{g}=AB$、进位传播 (carry propagation) $C_{p}=A+B$；本篇上面的 $P_i$ 则采用 XOR。二者都可用于 carry 递推，必须声明约定，不能把同名 $P$ 混进 sum 方程。

| $A_iB_i$ | $G_i$ | $P_i^{OR}$ | $P_i^{XOR}$ | Carry behavior · 进位行为 |
|---|---|---|---|---|
| 00 | 0 | 0 | 0 | 进位抑制 (carry kill)：$C_{i+1}=0$ |
| 01 / 10 | 0 | 1 | 1 | Propagate：$C_{i+1}=C_i$ |
| 11 | 1 | 1 | 0 | Generate：$C_{i+1}=1$ |

OR 约定在 11 行同时令 generate 和 propagate 为 1；generate 已保证输出进位，因此不影响结果。若 $A=B=1,C_i=0$，sum 应为 0，说明 $S_i$ 仍需 $A_i\oplus B_i\oplus C_i$。

> [!example]- Four-bit block generate/propagate · 块内超前、块间串行
> 以下统一采用 $P_i=P_i^{OR}$，位序 $i=0,1,2,3$。把四位展开式整理为块传播 (block propagate) 与块产生 (block generate)：
>
> $$P_{blk}=P_3P_2P_1P_0,$$
> $$G_{blk}=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0,$$
> $$C_4=G_{blk}+P_{blk}C_0.$$
>
> 讲义 p.15 使用 1–4 下标：$C_{in1}\leftrightarrow C_0$，$C_{out1}\leftrightarrow C_1$，$C_{out4}\leftrightarrow C_4$。先对应位权，再比较展开式。
>
> p.17 将两个四位 CLA 的输出进位串接：**块内是 look-ahead，块间仍是 ripple**。设低块 L、高块 H，则：
>
> $$C_8=G_H+P_HC_4=G_H+P_HG_L+P_HP_LC_0.$$
>
> 右侧是再增加一级块间超前逻辑的代数基础；仅把两个芯片串接，不会自动实现这个并行的块间网络。两种结构必须按真实路径比较延迟。
>
> **Lecture timing example / p.12：** 图示每一级进位延迟假设为 $8\ \mathrm{ns}$，四级共 $32\ \mathrm{ns}$。这是该图的简化最坏进位链模型，不是 74HC283/74LS283 的保证参数；指定最终 sum 输出时还需使用相应 sum 路径的延迟。
>
> A generate or kill condition can settle a carry without waiting for the incoming carry. Ripple dependence describes the worst propagating chain, not an unconditional dependency in every input row. “Immediately available” in p.14 means generated in parallel from A/B, not zero physical gate delay.

> [!example]- Ripple Carry and Carry Look-Ahead Adders · 推导与例题
> **Derivation · 展开进位链**
>
> $$C_1=G_0+P_0C_0,$$
> $$C_2=G_1+P_1G_0+P_1P_0C_0,$$
> $$C_3=G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0,$$
> $$C_4=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0+P_3P_2P_1P_0C_0.$$
>
> 每一步把前级 $C_i$ 代入并展开。所有输入已经稳定后，CLA 能并行生成 carry，而 RCA 必须逐级等待。大 fan-in 的 AND/OR 门未必与二输入门一样快，所以“只需两层”是有条件的门模型。
>
> **Worked Examples · 例题**
>
> **Carry propagation.** $A=1111,B=0000,C_0=1$。每位 $G_i=0,P_i=1$，所以 $C_1=C_2=C_3=C_4=1$，sum=0000，总和 16。这是典型贯穿全链的 carry 条件。
>
> **Generate and kill.** $A=1010,B=0111,C_0=0$。按 $i=0,1,2,3$，$G=(0,1,0,0)$，$P=(1,0,1,1)$，得到 $C=(C_0,C_1,C_2,C_3,C_4)=(0,0,1,1,1)$，sum=0001；10+7=17。
>
> **Timing model.** 假定每级 carry delay=450 ps，4-bit RCA 到最终 carry 的延迟是 $4\times450=1800$ ps，前提是 A/B 已经到达。若还需要最终 sum 的 XOR，计算该输出时应另加其延迟。不能把 carry-out 的延迟当成所有输出的延迟。
>
> A simplified look-ahead path may pass through propagate/generate logic, an AND layer, and an OR layer. Add the delays on the actual path; do not compare a four-stage RCA with a CLA model that silently assumes unlimited fan-in.

### Method and Exam English · 求解与答题

1. Declare bit order and the propagate convention.
2. Compute each $G_i$ and $P_i$ from the operands.
3. Expand carry expressions from the recurrence.
4. Identify the path to the requested output and sum its delays.
5. Check both the full arithmetic value and the retained width.

**Self-check:** Can OR propagate be used in $S_i=P_i\oplus C_i$?

**Answer:** No. When A=B=1 and carry-in=0, OR propagate is 1, but the correct sum is 0. Use XOR propagate for the sum even if the carry network uses OR propagate.

### Connections · 概念关系与应用

从 [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]] 的单级 carry 递推展开；[[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]] 决定有符号结果解释；[[Propagation Delay and Logic Hazards]] 给出路径延迟模型，[[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] 把加法路径纳入寄存器间的时间预算。

## 3 · Binary Subtractors and Adder-Subtractors · 共用数据通路

半减法器 $D=A\oplus B,B_{out}=\bar AB$。全减法器加入借位输入：$D=A\oplus B\oplus B_{in}$，$B_{out}=\bar AB+\overline{A\oplus B}B_{in}$。

模式 M=0 加法、M=1 减法：每位 $B'_i=B_i\oplus M$，最低进位 $C_0=M$，因此 $A+B'+M$。unsigned subtraction 的进位／无借位解释与 signed overflow 分开。

### Core Definition · 核心定义

半减器 (half subtractor) 算 $A-B$；全减器再减输入借位 $B_{in}$。本篇 $B$ 是 subtrahend bit，$B_{in}$ 是 borrow-in，$B_{out}$ 是 borrow-out；名称不同，避免全部写成 B。

$$A-B-B_{in}=D-2B_{out}.$$

这是普通整数守恒：借 1 相当于从高位借来 2 个本位单位。差分位为模 2 结果。

### Derivation · 推导

$$D=A\oplus B\quad(HA\text{-style subtractor}),\qquad B_{out}=\bar AB\quad\text{when }B_{in}=0.$$

全减器：

$$D=A\oplus B\oplus B_{in},$$
$$B_{out}=\bar AB+\bar A B_{in}+BB_{in}.$$

For A=0, either B or borrow-in requires borrowing. For A=1, borrowing is needed only when both B and borrow-in are 1. This yields the same equation without guessing from the adder carry formula.

| A | B | $B_{in}$ | D | $B_{out}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |

> [!example]- Binary Subtractors and Adder-Subtractors · 推导与例题
>
> **Adder-Subtractor · 共用加法器**
>
> 对 n 位加减器，mode $M=0$ 加法，$M=1$ 减法：
>
> $$S=A+(B\oplus\{n\{M\}\})+M\pmod{2^n}.$$
>
> 符号 $\{n\{M\}\}$ 表示 n 个相同 M 位的掩码。$M=1$ 时每个 $B_i$ 反相，初始进位为 1；$M=0$ 时 B 不变且初始 carry=0。
>
> For unsigned subtraction implemented this way, carry-out=1 means no borrow, and carry-out=0 means borrow, under the stated equal-width convention. Signed overflow still requires the signed criterion; carry-out alone is insufficient.
>
> **Worked Examples · 例题**
>
> **Borrow.** $A=0,B=1,B_{in}=1$，原式为 −2；$D=0,B_{out}=1$，右侧 $0-2=-2$，正确。
>
> **Four-bit subtraction.** $3-5$: `0011 + 1010 + 1 = 1110`。无符号解释保留值为 14，存在借位；补码解释为 −2。$7-3$: `0111 + 1100 + 1 = 1 0100`，carry=1，无借位，结果 4。
>
> **Decoder.** 变量顺序 $(B_{in},A,B)$ 时，difference 的 ON set 为 $\{1,2,4,7\}$，borrow 的 ON set 为 $\{1,4,5,7\}$。换变量顺序后索引会变，必须重编表。

### Pitfalls and Review · 易错点与复习

- A sum bit and difference bit both use XOR, but carry and borrow do not have the same equation.
- 补码减法必须“反相并加 1”；只反相是 one's complement。
- “Perform signed subtraction” requires stating the signed values and testing range overflow.

**Exam answer:** “The difference bit is the parity of A, B, and borrow-in. The borrow output is asserted exactly when B plus borrow-in exceeds A.”

### Connections · 概念关系与应用

用 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 的整数守恒校验 borrow；[[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|Two's Complement Representation]] 使减法复用 [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]]；也可把真值表交给 [[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 实现。

## 4 · Combinational Multiplier · 从部分积到列加法

n×m 无符号乘法有 $p_{ij}=a_ib_j$，位权 $2^{i+j}$，完整结果宽 n+m。逐列用半／全加器加权相加；三位乘三位需六位结果。若是补码，须处理符号扩展或专门的有符号部分积结构。

> [!IMPORTANT] 验证顺序
> 对小位宽穷举并按整数守恒核对；再检查最高位、进位、借位、溢出和路径时延。算对低位不能证明完整乘积正确。

### Core Definition and Derivation · 定义与推导

设 $A=\sum_{i=0}^{m-1}a_i2^i$，$B=\sum_{j=0}^{n-1}b_j2^j$，且本节为 unsigned：

$$AB=\sum_i\sum_j(a_ib_j)2^{i+j}.$$

partial product $p_{ij}=a_i b_j$ 用 AND 门产生，其权为 $2^{i+j}$。相同权列的两个位用 HA，三个位用 FA，carry 进入下一权列。乘法器是组合逻辑，不需要因为“有很多加法步骤”就引入 clock。

> [!example]- Combinational Multiplier · 推导与例题
> **Worked Example · 3×3 位乘法**
>
> $A=101_2=5$，$B=111_2=7$。六位对齐的三行部分积为：
>
> | Multiplier bit | Row | Decimal value |
> |---|---|---|
> | $b_0=1$ | 000101 | 5 |
> | $b_1=1$ | 001010 | 10 |
> | $b_2=1$ | 010100 | 20 |
> | Total | 100011 | 35 |
>
> To design the network rather than merely calculate the product, name the column signals. $z_0=p_{00}$. A half adder combines $p_{10},p_{01}$ into $z_1,c_2$. At weight 4, a full adder combines $p_{20},p_{11},c_2$ into $s_2,c_3$, then a half adder combines $s_2,p_{02}$ into $z_2,d_3$. At weight 8, add $p_{21},p_{12},c_3$, then combine the sum with $d_3$. At weight 16, add $p_{22}$ and both carries from the previous weight; its sum and carry form $z_4,z_5$.
>
> 该列压缩方案需要 9 个 AND、3 个 HA、3 个 FA；它是一个有效拓扑，并非唯一最优电路。给每个中间 carry 命名，避免同一 carry 被遗漏或重复。
>
> **Timing and Signed Boundary · 时序与有符号边界**
>
> The longest delay is the longest sensitizable path through the actual AND and adder network. Count both carry and sum arcs using the problem's delay model. Multiplying the number of all adders by one delay overestimates parallel sections and may underestimate a sum path.
>
> Signed multiplication needs sign treatment: the MSB has negative weight in two's complement. Do not multiply raw negative patterns as unsigned and merely add a sign bit afterward. [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确|Signed Binary Multiplication and Division]] derives sign extension and wider results.
>
> **Practical Examples and Review · 应用与复习**
>
> **Maximum value.** 两个 3-bit unsigned 最大值相乘：$7\times7=49=110001_2$，需要 6 位；5 位只能到 31。不是所有乘积都用满 6 位，但输出设计应覆盖最大情况。
>
> **Signed case.** 4-bit `1011` 是 −5，`1010` 是 −6，乘积 +30，8-bit `00011110`。把两个原始码当 11 与 10 会得到 110，改变了问题。
>
> **Exam question:** Why are partial products shifted before addition?
>
> **Answer:** The multiplier bit at position j has weight $2^j$. Its AND-generated row represents A multiplied by that weight, so each row must be aligned j positions to the left before addition.

### Connections · 概念关系与应用

[[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|Binary Arithmetic]] 决定结果位宽，[[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算|AND Gate]] 形成部分积，[[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]] 合并同权列；[[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径|Ripple Carry and Carry Look-Ahead Adders]] 提供加法子结构，最长路径仍按 [[Propagation Delay and Logic Hazards]] 的规则计算。

## Sources · 课件依据

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 6: Combinational Building Blocks*，[本次讲义](../ECE2050-Chap6.pdf#page=5)，PDF p.5–8：HA/FA；p.9–11：并行加法器、74HC283/74LS283 级联、六位置投票；p.12–17：RCA、OR 传播定义、CLA 展开与块间级联；p.55：HA/FA 乘法器设计问题。PDF 页序与页脚编号一致。
- [库中原参考讲义](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。减法、乘法网络与标为 self-calculated 的例题属于笔记扩展推导；延迟示例的假设值不代表器件额定值。

---
索引：[[ECE2050.1]] · [[Glossary]]
