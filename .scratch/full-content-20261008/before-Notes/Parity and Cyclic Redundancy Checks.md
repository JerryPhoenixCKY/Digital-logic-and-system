---
tags:
  - ECE2050
  - error-codes
date: 2026-09-16
updated: 2026-10-08
chapter: Ch2
aliases:
  - 奇偶校验与循环冗余校验
  - Parity and Cyclic Redundancy Checks
  - 奇偶校验与循环冗余校验 · Ch2
  - Parity Bit
  - 奇偶校验位
  - 奇偶校验
  - 校验位
  - Parity Check
  - Cyclic Redundancy Check
  - 循环冗余校验
  - CRC 校验
  - 生成多项式
  - CRC
---

# Parity and Cyclic Redundancy Checks · 奇偶校验与循环冗余校验

> [!SUMMARY] Quick recall · 英文速览
> Parity checks the number of flipped bits modulo two. CRC checks polynomial divisibility; its guarantees depend on the generator and frame length.

## 1 · Parity Bit · 用一个约束建立检错

数据位 $d_i$ 与校验位 P 均为 0/1。偶校验位为 $P=\bigoplus d_i$；奇校验位为它的补。收到的整组异或为 S：偶校验要求 S=0，奇校验要求 S=1。

> [!IMPORTANT] XOR 的两种用途
> XOR 输出 1 表示数据中有奇数个 1；把这个结果作为新增位，完整码字就有偶数个 1。生成偶校验位用 XOR，生成奇校验位用其补，不能把生成器与检查器混称。

> [!example]- Parity Bit · 推导与例题
> **图示与讲义依据**
>
> ![[parity-bit-format.svg]]
> *图 1 — (a) 同一个 7 位数据字 `110 1001` 在偶校验下补 $P=0$、奇校验下补 $P=1$，两种约定都把
> "1 的个数"钉在固定的奇偶性上；(b) 盲区：两位同时翻转（一位 $1\to0$、另一位 $0\to1$）后
> 总 1 数仍然是 4，$S=0$，校验位**完全看不出**出错。*
>
> **Derivation · 推导过程**
>
> **1. 为什么 XOR 就是校验位的算法**
>
> 先把 XOR 的性质列清楚：$a \oplus b$ 在 $a\ne b$ 时为 1，因此
>
> $$
> d_1 \oplus d_2 \oplus \cdots \oplus d_n = 1
> \iff \text{数据中 1 的个数为奇数}
> $$
>
> - 意义：**异或链就是"1 的个数的奇偶性指示器"**。所以偶校验位直接取异或结果，奇校验位取它的反。
> - 数值校验：`110 1001` → $1\oplus1=0$，$0\oplus0=0$，$0\oplus1=1$，$1\oplus0=1$，$1\oplus0=1$，$1\oplus1=0$；
>   得到 0，说明 1 的个数是偶数（4 个）✓，与直接数数一致 ✓。
> - 硬件视角：全部用 XOR 门（或一棵 XOR 树），深度 $\lceil \log_2 n\rceil$，非常便宜。
>
> **2. 接收端判据：整组异或为 0**
>
> 对偶校验，把 $P$ 也一起异或进来：
>
> $$
> S = d_1 \oplus \cdots \oplus d_n \oplus P = 0 \;\Longrightarrow\; \text{1 的个数为偶数（符合约定）}
> $$
>
> - 意义：$S$ 就是"1 的总个数 mod 2"。$S=0$ 说明约定被满足；$S=1$ 说明约定被破坏。
> - 数值校验：`1101 0010` → 4 个 1 → $S = 0$ ✓；把第 3 位 $0\to1$ 得到 `1111 0010`（5 个 1）→ $S=1$ → 检出 ✓。
> - 奇校验系统则相反：接收端要求 $S=1$（总 1 数为奇），$S=0$ 才是出错。
>
> **3. 能力边界：为什么偶数个错误一定漏**
>
> 设错误模式 $e = e_1e_2\cdots e_{n+1}$（$e_i=1$ 表示第 $i$ 位翻转），收到 $S' = S \oplus (e_1\oplus\cdots\oplus e_{n+1})$。
>
> $$
> S' = S \oplus (\text{翻转位数} \bmod 2)
> $$
>
> - 意义：**校验子只反映"错误个数的奇偶性"**。翻转 1、3、5…位 → $S$ 取反 → 检出；
>   翻转 2、4、6…位 → $S$ 不变 → 漏检（图 1(b)）。
> - 数值校验（盲区示例）：发送 `1101 0010`（4 个 1）。让第 1 位 $1\to0$、第 6 位 $0\to1$，
>   收到 `0101 0110` —— 1 的个数仍是 4 ✓，$S = 0$ → 校验通过，**错误被完整地漏掉** ✓。
> - 量化：对包含校验位的 $L$ 位字，共有 $2^L-1$ 个非零错误掩码。奇数重有 $2^{L-1}$ 个，
>   非零偶数重有 $2^{L-1}-1$ 个。若所有非零掩码等概率，则漏检率为 $(2^{L-1}-1)/(2^L-1)$，
>   接近 50%；8 位例子为 $127/255$。这不是任意错误分布下的上限，若只出现双比特错误则全部漏检。
>
> **4. 提高能力的方向**
>
> | 方案 | 冗余 | 能力 | 代价 |
> |---|---|---|---|
> | 单组奇偶校验 | 1 bit / 组 | 检出奇数个错误 | 偶数个错误全盲、不能定位 |
> | 二维/块校验 (row + column parity) | 每行每列各 1 bit | 定位并纠正 1 位错误 | 冗余约 $2/\sqrt{N}$，需矩阵存储 |
> | 汉明码 (Hamming) | 多位 | 纠正 1 位、检出 2 位 | 需要多个校验方程（超本课范围，仅作了解） |
> | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|Cyclic Redundancy Check]] | 4–32 bit | 检出错位位置相关的多类错误 | 需要移位寄存器与模 2 除法 |
>
> - 数值校验（块校验为什么能定位）：把 8 字节排成 $8\times 8$ 矩阵，每行每列各加 1 位偶校验，
>   共 $8+8=16$ 位冗余；若恰好 1 位翻转，则**它所在的行与列同时报错**，交点即错误位置 → 取反即纠正 ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.70 原题：奇校验系统收到五组码，哪几组出错？**
>
> 题目：一个奇校验系统 (odd parity system) 收到 `10110`、`11010`、`110011`、`110101110100`、
> `1100010101010`，判断哪些组有错。
>
> 解：奇校验要求每组 1 的个数为**奇数**，逐个统计：
>
> | 收到的码组 | 位数 | 1 的个数 | 奇校验判定 |
> |---|---|---|---|
> | `10110` | 5 | 3 | 奇数 → 合格 |
> | `11010` | 5 | 3 | 奇数 → 合格 |
> | `110011` | 6 | 4 | 偶数 → **出错** |
> | `110101110100` | 12 | 7 | 奇数 → 合格 |
> | `1100010101010` | 13 | 6 | 偶数 → **出错** |
>
> 所以出错的是第 **3** 组 `110011` 与第 **5** 组 `1100010101010`（与讲义结论一致）。
>
> **数值校验 (Numerical check)**：
> - `10110`：$1+0+1+1+0$ 的异或 $= 1\oplus0\oplus1\oplus1\oplus0 = 1$，$S=1$ 符合奇校验 ✓。
> - `110011`：$1\oplus1\oplus0\oplus0\oplus1\oplus1 = 0$，$S=0$ 违反奇校验约定 → 报错 ✓。
> - 计数复核：$3,3,4,7,6$ 中只有 4 与 6 是偶数，恰好对应第 3、5 组 ✓。
>
> **Example 2 — 给定数据 `1101001` 求偶校验位与奇校验位**
>
> 题目：数据位为 `110 1001`（7 位），分别求偶校验位与奇校验位，并写出完整码字。
>
> 解：
> 1. 数 1 的个数：`1 1 0 1 0 0 1` → 4 个 1（偶数）。
> 2. 偶校验：需要总数为偶数 → $P_{\text{even}} = 0$，码字 `1101 0010`。
> 3. 奇校验：需要总数为奇数 → $P_{\text{odd}} = 1$，码字 `1101 0011`。
>
> **数值校验 (Numerical check)**：
> - 异或链：$1\oplus1=0$，$0\oplus0=0$，$0\oplus1=1$，$1\oplus0=1$，$1\oplus0=1$，$1\oplus1=0$ → $P_{\text{even}}=0$ ✓。
> - `1101 0010` 的 1 个数 = 4（偶）✓；`1101 0011` 的 1 个数 = 5（奇）✓。
> - 两个码字只差最后一位（$0$ 与 $1$）✓，即奇校验位就是偶校验位取反。
>
> **Example 3 — 制造一个 2 位错误，说明为什么检不出来**
>
> 题目：偶校验码字 `1101 0010` 在传输中被翻转了第 1 位与第 6 位，验证接收端会误判为"正确"。
>
> 解：
> 1. 翻转第 1 位（`1 → 0`）：`0101 0010`（1 的个数 3）。
> 2. 再翻转第 6 位（`0 → 1`）：`0101 0110`（1 的个数 4）。
> 3. 接收端计算校验子：$S = 0$ → 判定"无错"，把错误数据交给上层。
>
> **数值校验 (Numerical check)**：
> - 发送码字 1 的个数 = 4；接收码字 1 的个数 = 4，两者相同 ✓（一加一减互相抵消）。
> - $S' = S \oplus (\text{翻转位数} \bmod 2) = 0 \oplus (2 \bmod 2) = 0$ ✓ —— 这就是"盲区"的代数解释。
> - 对照：只翻转第 1 位时 1 的个数变 3，$S = 1$ → 能检出 ✓；说明**不是"能不能查错"，而是"错误个数是否为奇数"**。

## 2 · 门级发生器、检查器与错误边界

四位数据的平衡树：$P=(A_0\oplus A_1)\oplus(A_2\oplus A_3)$，三个二输入 XOR、两级逻辑。接收端将收到的四数据位 $r_i$ 和收到的校验位 $p_r$ 全部异或得到检错输出 E，需要四个二输入 XOR。

偶校验字 10100 单比特翻转成 00100 时 E=1；两比特翻转成 01100 时 E=0。相对合法字，所有奇数次翻转检出，所有非零偶数次翻转漏检；E=0 只表示未检出错误，不证明数据正确。

> [!example]- Parity Bit · 推导与例题
> **Parity generation, checking, and limits · 生成、校验与边界**
>
> Even-parity generation chooses $P=\bigoplus d_i$, so XOR of the full transmitted word is zero. Odd-parity generation chooses its complement, so XOR of the full transmitted word is one. A checker compares the received total parity against the selected convention. Avoid memorizing “XOR means odd parity” without saying whether it describes a data reduction, generated bit, or received-word check.
>
> A zero error indication means that no error was detected, not that the data is certainly correct. Every nonzero error mask with even Hamming weight preserves parity. The probability of missing an error therefore depends on the error distribution. It can be 100% if errors always flip exactly two bits; one-half is not a universal worst-case bound.
>
> **Worked application — odd parity for BCD data.** 数据 `00010100`（BCD 14）有两个 1。奇校验要整组有奇数个 1，故 P=1，发送组有三个 1。若给出的解答同时写“该断言正确”与 P=0，后者和定义冲突；直接数 1 可独立核验。接收后翻转两个位，会保持总 parity，仍能漏检。
>
> In English: compute the parity over the actual data bits, not over the decimal value written alongside them. Include the transmitted parity bit when checking the received word.
>
> **English exam question:** Does a parity failure identify the corrupted bit?
>
> **Answer:** No. It indicates an odd number of bit flips relative to a valid parity word, but provides no position information. Different single-bit and odd-weight error masks can produce the same parity failure.
>
> Continue with [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]], [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-NOR Gate]], [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|Cyclic Redundancy Check]], and [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]]. A useful parity testbench includes single-bit flips and a two-bit counterexample, not only clean data.
>
> **Gate-Level Parity Circuits · 门级校验电路，Ch5 p.11–14**
>
> **校验位发生器 (parity-bit generator)** 对数据求校验位；**校验检查器 (parity checker)** 对收到的数据和收到的校验位共同判断。课件所说 2-bit、3-bit、4-bit generator 指原始数据位数；4 位数据加 1 位校验才形成 5 位码字 (codeword)。
>
> **Two and Three Data Bits · 两位与三位数据**
>
> 两位数据 $A,B$ 的偶校验位 $P=A\oplus B$。三位数据顺序为 ABC，根据 p.12 真值表：
>
> $$
> \begin{aligned}
> P&=\bar A\bar BC+\bar AB\bar C+A\bar B\bar C+ABC\\
>  &=\bar A(\bar BC+B\bar C)+A(\bar B\bar C+BC)\\
>  &=\bar A(B\oplus C)+A\overline{(B\oplus C)}\\
>  &=A\oplus B\oplus C.
> \end{aligned}
> $$
>
> 令 $T=B\oplus C$，倒数第二行就是 $\bar AT+A\bar T$，恰好是 $A\oplus T$。卡诺图的四个 1 分别是 $m_1,m_2,m_4,m_7$，互不相邻；普通 SOP 不能把它们圈成更大的组，但可识别 XOR 结构，用两个二输入 XOR 实现。
>
> | $ABC$ | Data 1-count | $P$ | Total 1-count in $ABCP$ |
> |---|---|---|---|
> | 000 | 0 | 0 | 0 |
> | 001 | 1 | 1 | 2 |
> | 010 | 1 | 1 | 2 |
> | 011 | 2 | 0 | 2 |
> | 100 | 1 | 1 | 2 |
> | 101 | 2 | 0 | 2 |
> | 110 | 2 | 0 | 2 |
> | 111 | 3 | 1 | 4 |
>
> An XOR reduction reports odd parity in the **data**. Appending that result makes the **complete codeword** even. Thus XOR implements an even-parity generator; XNOR would generate the odd-parity bit instead.
>
> **Four-Input Generator and Five-Input Checker · 四位发生器与五位检查器**
>
> 四位发送数据为 $A_3A_2A_1A_0$；偶校验位为 $P$。课件 p.13 的平衡异或树 (balanced XOR tree) 是：
>
> $$
> t_0=A_0\oplus A_1,\qquad t_1=A_2\oplus A_3,\qquad
> P=t_0\oplus t_1.
> $$
>
> 它使用三个二输入 XOR，数据到 P 的最长路径是两级；串联实现也用三个门，但最长为三级。这里只比较逻辑级数；实际延迟需给出器件参数与负载条件。
>
> 收到的数据写为 $r_3r_2r_1r_0$，收到的校验位写为 $p_r$，所有符号取值均为无量纲 0/1。p.14 检查器重算数据奇偶性 $Q$，再比较收到的校验位：
>
> $$
> Q=(r_0\oplus r_1)\oplus(r_2\oplus r_3),\qquad E=Q\oplus p_r.
> $$
>
> 这里 $E=1$ 是高有效检错输出，$E=0$ 表示未检出错误。检查器需四个二输入 XOR；收到的数据到 E 最长三级，收到的校验位在图示结构中只经末级 XOR。
>
> ![[parity-generator-checker.svg]]
> *图 2 — (a) 四位发送数据生成 P；(b) 对四位收到的数据与收到的校验位 $p_r$ 求检错输出 E。每根输入线独立，发送与接收变量明确分开。*
>
> | $Q$ | Received $p_r$ | $E=Q\oplus p_r$ | Meaning |
> |---|---|---|---|
> | 0 | 0 | 0 | 收到的整组有偶数个 1，未检出错 |
> | 0 | 1 | 1 | 整组有奇数个 1，校验失败 |
> | 1 | 0 | 1 | 整组有奇数个 1，校验失败 |
> | 1 | 1 | 0 | 整组有偶数个 1，未检出错 |
>
> **Worked check.** 发送数据 1010，$P=1\oplus0\oplus1\oplus0=0$，完整字 10100 的 $E=0$。只翻转首位得到 00100，$E=1$；同时翻转前两位得到 01100，$E=0$，但收到的数据已改变。位序在这个例题中从左至右为 $A_3A_2A_1A_0P$。
>
> **Source wording and detection limit · 课件措辞与能力边界**
> p.14 将 E=1 简述为“有错误”、E=0 为“无错误”。精确结论是：相对于合法偶校验字，奇数个翻转产生 E=1；非零偶数个翻转仍产生 E=0。因此 0 只能说明 **no error detected**，不能证明数据正确。

## 3 · Cyclic Redundancy Check · 改用多项式余数

CRC 将消息位串解释为二元多项式 $M(x)$；生成式 $G(x)$ 的次数为 r。运算在 GF(2) 上，减法与加法都是 XOR，不进位。

$$R(x)=[x^rM(x)]\bmod G(x),\qquad C(x)=x^rM(x)+R(x).$$

发送端补 r 个 0 后除 G，附上 r 位余数；接收端对包含 CRC 的整组再除 G，零余数表示未检出错。错误模式 $E(x)$ 恰好是 G 的倍数时仍会漏检。

> [!example]- Cyclic Redundancy Check · 推导与例题
> **图示与讲义依据**
>
> ![[crc-modulo2-division.svg]]
> *图 1 — (a) 发送端：把 $D'$ = `1101 0011 0000` 用模 2 长除一步步除以 $G$ = `1010`。每一级做三件事：
> 把 $G$ 对齐到当前最高位的 1、逐位 XOR（**没有借位、没有进位**）、消掉那一位；阶梯共 5 步
> （消去 $x^{11},x^{10},x^9,x^7,x^4$），最后留下余数 `100`，写成 4 位校验和 `0100`。
> (b) 接收端把整帧再除一次：干净帧余 `000`（未检出错误），末位翻转后余 `001`（非 0 → 检测到错误）。*
>
> **Derivation · 推导过程**
>
> **1. 模 2 运算：加法不进位，减法就是加法**
>
> | 运算 | 结果 | 运算 | 结果 |
> |---|---|---|---|
> | $0 \oplus 0$ | 0 | $1 \oplus 0$ | 1 |
> | $0 \oplus 1$ | 1 | $1 \oplus 1$ | **0（进位被丢弃）** |
>
> - 意义：模 2 下 $1+1=0$，故 $-1=+1$（每个数的相反数就是它自己），**减法与加法完全相同**：$A-B=A\oplus B$。
> - 数值校验：算术上 $1101_2-1010_2=0011_2$；模 2 上 $1101\oplus1010=0111$（$1\oplus1=0,1\oplus0=1,0\oplus1=1,1\oplus0=1$）✓。
>   CRC 长除用的必须是后者。
> - 多项式视角：位串 $a_{n-1}\cdots a_0 \leftrightarrow \sum a_ix^i$，于是 `1010` $\leftrightarrow x^3+x$，
>   `11010011` $\leftrightarrow x^7+x^6+x^4+x+1$，位串 XOR 就是多项式的加法（系数在 GF(2) 上）。
>
> **2. 发送端：补零 → 长除 → 取余**
>
> $$
> R(x) = D(x)\cdot x^{k} \bmod G(x),\qquad k=\text{校验和位数}
> $$
>
> - 意义：把数据"抬高" $k$ 位，腾出的低位正好由余数填满，使整帧成为 $G(x)$ 的倍数。
> - 逐级长除（与图 1(a) 一致，每级消掉当前最高位的 1）：
>
> | 级 | 当前位串 | 对齐的 $G$ | XOR 后 | 消去的位 |
> |---|---|---|---|---|
> | 1 | `110100110000` | `1010` | `011100110000` | $x^{11}$ |
> | 2 | `011100110000` | ` 1010` | `001000110000` | $x^{10}$ |
> | 3 | `001000110000` | `  1010` | `000010110000` | $x^{9}$ |
> | 4 | `000010110000` | `    1010` | `000000010000` | $x^{7}$ |
> | 5 | `000000010000` | `      1010` | `000000000100` | $x^{4}$ |
>
> - 数值校验：最后一行只剩低位 `100` = $x^2$ ✓；回代成整帧 $1101\,0011\,0100 \div 1010$ 余 `000` ✓
>   ——这正是"附上余数后整帧可被 $G$ 整除"的定义。
>
> **3. 接收端：整帧再除一次**
>
> $$
> T(x) = D(x)\cdot x^{k} + R(x) \;\equiv\; 0 \pmod{G(x)}
> $$
>
> - 意义：合法帧一定被 $G$ 整除；接收端再算一次余数，非 0 就说明帧被改动过。
> - 数值校验：干净帧 `1101 0011 0100` → 余 `000` ✓；末位翻转 `1101 0011 0101` → 余 `001` ✓
>   ——余数本身就是"错误模式的指纹"。
>
> **4. 为什么比奇偶校验强：错误模式 $E(x)$**
>
> 设收到 $T \oplus E$（$E$ 是错误模式）。因为 $T \equiv 0$，接收端算出的是
>
> $$
> (T \oplus E) \bmod G = E(x) \bmod G(x)
> \qquad\Longrightarrow\qquad
> \text{漏检} \iff G(x) \mid E(x)
> $$
>
> - 意义：**CRC 漏检当且仅当错误模式本身是 $G(x)$ 的倍数**，于是"能查哪些错"变成纯代数问题：
>   **单比特** $E=x^i$ 除不尽 $G$ → 全检出（本例 12 位帧实测 12/12 ✓）；
>   **奇数个错误**：若 $(x+1)\mid G$，奇数重模式有 $E(1)=1$ 而 $G(1)=0$ → 全检出（实测 2048/2048 ✓）；
>   **突发错误 (burst)**：长度 $b$ 的突发 $E=x^iB(x)$，若 $G$ 末尾是 1（$x\nmid G$）则须 $G\mid B$，
>   而 $b\le r$ 时 $\deg B<r$ 不可能 → **长度不超过阶数 $r$ 的突发全检出**。
> - 数值校验（对照 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]]）：同一个 12 位帧穷举 4095 个非零错误模式——奇偶校验漏检 2047 个（50%，全是偶数重模式）；
>   CRC 漏检 511 个（12.5%），且漏掉的全是 $G$ 的倍数（包括移位，也包括多个移位项的 XOR 组合），而不是整整一半。
>
> **5. 能力对照（同一帧上穷举，数字来自图 3）**
>
> | 错误类型 | 模式个数 | 奇偶校验检出 | CRC 检出（$G=1010$） |
> |---|---|---|---|
> | 单比特 | 12 | 12（100%） | 12（100%） |
> | 双比特 | 66 | 0（0%） | 41（62%） |
> | 奇数个比特 | 2048 | 2048（100%） | 2048（100%） |
> | 偶数个比特 | 2047 | 0（0%） | 1536（75%） |
> | 跨度 ≤ 3 位的突发 | 43 | 22（51%） | 34（79%） |
> | 跨度 ≥ 4 位的突发 | 4052 | 2026（50%） | 3550（88%） |
>
> - 读表要点：奇偶校验的每一列只由"错误个数的奇偶性"决定（0%、50% 或 100%）；CRC 每一列都不低于它。
>   讲义 $G=1010$ 是玩具：末尾是 0，所以"长度 ≤ 阶数的突发全检出"不再严格成立（如 `101` 突发在非最低位时正好等于 $x^{i-1}\cdot G$，会漏掉）。
>
> **6. 硬件：移位寄存器 + XOR 反馈**
>
> 除法可以一位一位在线完成："当前最高位是 1 → XOR 掉"等价于一个**带反馈抽头的移位寄存器**。
> 下面保留的四级教学图实际对应扩展多项式 $H(x)=xG(x)=x^4+x^2$（位串 `10100`）。其寄存器次态是
>
> $$
> D_0 \leftarrow D_{in},\qquad D_1 \leftarrow Q_0,\qquad D_2 \leftarrow Q_1 \oplus Q_3,\qquad D_3 \leftarrow Q_2
> $$
>
> - 意义：当前最高级 **$Q_3$** 在移位时经反馈与 $Q_1$ 异或，进入 $D_2$，对应 $H$ 的 $x^2$ 项。
>   四级网络求 $H$ 余数；本例三条输入序列恰好也得到 $G$ 余数，但不代表任意输入都等价。
>   例如输入 `1000` 时四级寄存器为 `1000`，直接除 $G=1010$ 的余数却是 `010`。
> - 数值校验（按四式逐拍模拟 $D'=110100110000$）：寄存器终值 = `0100` ✓，与长除余数 `100`（补成 4 位）一致；
>   喂干净帧 `110100110100` 得 `0000` ✓，喂末位翻转帧得 `0001` ✓。
> - 工程延伸：CRC-8、CRC-16-IBM、CRC-32（$0x04C11DB7$）都是"末尾为 1"的多项式，正是为了让上面的保证严格成立；
>   以太网、ZIP、PNG 都用 CRC-32。
>
> ![[crc-shift-register.svg]]
> *图 2 — CRC 编码器的串行硬件：4 级 D 触发器（$D_0$–$D_3$，上升沿时钟，整体左移）串联，图中 $D_{in}$ 从左侧 $D_0$ 喂入；
> 最高位级 $Q_3$ 经反馈线送回 XOR 门，与 $Q_1$ 异或后进入 $D_2$，实际是 $H=xG=x^4+x^2$ 的四级形态。
> 12 个时钟后，寄存器里留下的正是图 1 长除的余数。*
>
> ![[binary-parity-vs-crc.svg]]
> *图 3 — 把两种码放在同一帧（`1101 0011 0100`，4095 个非零错误模式）上穷举对比：奇偶校验只统计"翻了几位"，
> 偶数个错误一律漏掉；CRC 统计"翻在哪些位置"，只在错误模式恰好是 $G(x)$ 的倍数时失手。这张图就是"为什么需要 CRC"的答案。*
>
> **Degree-three serial divider · 三阶生成式的串行模型**
>
> For $G=x^3+x$ itself, use three remainder bits $R_2R_1R_0$, zero initialization, and MSB-first input. Appending one bit d shifts the old polynomial; the outgoing $R_2x^3$ is reduced by $x^3+x$, yielding:
>
> $$R_2^+=R_1,\qquad R_1^+=R_0\oplus R_2,\qquad R_0^+=d.$$
>
> Feed data followed by **three** zeros to compute the conventional three-bit checksum. 数据11010011给出010，发送11010011010；题目数据10110010给出110，发送10110010110。接收整帧后寄存器000表示整除、未检出错误。
>
> The preserved four-stage diagram instead uses $H=xG$ and the explicitly described four-bit extension. The two networks are not interchangeable for arbitrary input; `1000` is a simple counterexample. Compare [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] and [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]] to verify the recurrence against direct polynomial division.

## 4 · 例题与保证必须分开

取消息 1101、生成码 1011，即 $G=x^3+x+1$：对 1101000 做模 2 除法，余数为 001，码字为 1101001；整组再除 1011 的余数为 000。

次数 r、首末系数为 1 的生成式能检测长度不超过 r 的非零突发错误。检测所有奇数重错误还要求包含因子 $x+1$；其他保证依赖生成式和帧长。抽象课内算法与真实协议的初值、反射、最终异或约定需区分。

> [!example]- Cyclic Redundancy Check · 推导与例题
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.71 全流程：$D = 11010011$、$G = 1010$**
>
> 题目：按讲义步骤求校验和与发送帧，并验证接收端判定。
>
> 解：
> 1. **补零**：$D' = D \,\|\, 0000 = 1101\,0011\,0000$。
> 2. **长除**（对齐 → XOR → 消最高位，重复 5 次，见表与图 1(a)）：
>    `110100110000` → `011100110000` → `001000110000` → `000010110000` → `000000010000` → `000000000100`。
> 3. **余数** $R=100$ → 4 位校验和 `0100`；**发送** $T = 1101\,0011\,0100$（8 位数据 + 4 位校验和）。
> 4. **接收端复算**：$1101\,0011\,0100 \div 1010$ 余 `000` → 判定无错。
>
> **数值校验 (Numerical check)**：
> - 逐级各消掉一个最高位 1，共消去 5 个（$x^{11},x^{10},x^9,x^7,x^4$），最后一个 1 停在 $x^2$ → 余数 $=x^2=100$ ✓。
> - 整除性自检：把 `0100` 附到数据后整帧再除 $G$ 得 `000` ✓（这正是发送端算法的目的）；位数自检：$8+4=12$ 位 ✓。
> - 严格多项式约定：补 3 个 0 → `1101 0011 000` 除 `1010` 余 `010`，帧 = `1101 0011 010`，接收端余数同样是 `000` ✓。
>
> **Example 2 — 本例全部单比特错误都检得出来**
>
> 题目：把 Example 1 的帧末位翻转，验证接收端能检出；并说明 12 个单比特错误是否全部可检出。
>
> 解：
> 1. 传输中末位翻转：$T' = 1101\,0011\,0101$。
> 2. 接收端长除：$1101\,0011\,0101 \div 1010$ → 余数 `001` ≠ `000` → **检测到错误**，请求重传。
> 3. 穷举 12 种单比特翻转（每一位各翻一次）：余数可以重复，但全部非零，**12/12 全部检出**。
>
> **数值校验 (Numerical check)**：
> - 末位翻转对应 $E = x^0$，$\deg E = 0 < r = 3$ → $G \nmid E$ → 必被检出 ✓（与图 1(b) 的 `001` 一致）。
> - 余数可当"错误指纹"读：干净帧 `000`、末位翻转 `001` ✓，两者不同即已证明可区分（这正是 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|Parity Bit]] 做不到的）。
>
> **Example 3 — 什么样的错误 CRC 会漏掉（玩具生成码的盲区）**
>
> 题目：$G=1010$ 时构造一个检不出的双比特错误，并解释原因。
>
> 解：
> 1. 取错误模式 $E = 0101\,0000\,0000$（把帧的第 2、4 位各翻一次，属双比特错误）。
> 2. 接收端长除 $E$：$0101\,0000\,0000 \div 1010$ 余 `000` → **判为无错，漏检**。
> 3. 原因：$E(x) = x^{10}+x^{8} = x^{7}(x^{3}+x) = x^{7}\cdot G(x)$，恰好是 $G$ 的倍数。
>
> **数值校验 (Numerical check)**：
> - 余数公式 $\text{rem} = E \bmod G$：$x^7G \bmod G = 0$ ✓，与长除结果 `000` 一致 ✓。
> - 规模：12 位帧上 4095 个非零错误模式中有 511 个是 $G$ 的倍数 = 12.5%（都会漏检）✓；奇偶校验漏检 2047 个 = 50% ✓。
> - 修法：让 $G$ 末尾为 1（如 CRC-32 的 $0x04C11DB7$），则 $\deg E<r$ 的模式都无法被整除，
>   常数项为 1 且含至少两个非零项时可检出全部单比特错误，并支持长度不超过 $r$ 的突发检出；双比特保证还需检查位间距与帧长。
>
> **Standard exam algorithm and guarantees · 标准算法与检错边界**
>
> For the elementary zero-initialized, MSB-first polynomial convention used in these exam questions, a generator of length $r+1$ has degree $r$. Append exactly $r$ zeros to the data, divide using XOR, and append the $r$-bit remainder to the original data. Divide the complete received frame for checking. A named practical CRC can add initialization, reflection, or final-XOR conventions, so identify that format before transferring the elementary calculation.
>
> **Worked application — short exam frame.** $D=1101$、$G=101$，$r=2$。补零得 `110100`。先 XOR 对齐 `101000` 得 `011100`，再 XOR `010100` 得 `001000`，再 XOR `001010` 得 `000010`。余数必须写足 2 位=`10`，发送 `110110`。接收端除以 `101` 得余 `00`，表示校验通过。
>
> In English: the remainder has fewer than $r+1$ significant bits but occupies an $r$-bit field, including leading zeros. A zero remainder proves divisibility by the generator. It does not prove that no transmission error occurred.
>
> For an error polynomial $E(x)$, detection fails exactly when $G(x)$ divides $E(x)$. A nonzero multiple of the generator is always a counterexample if it fits in the frame. A constant term of one supports short-burst guarantees, but does not alone guarantee detection of all double-bit errors. For two flipped bits separated by $j$, the relevant question is whether $G(x)$ divides $x^j+1$.
>
> **English exam question:** Why can a CRC detect an error that even parity misses?
>
> **Answer:** Even parity depends only on the number of flipped bits modulo two. CRC also depends on their positions through polynomial division. Some even-weight masks have a nonzero CRC remainder, though generator multiples still remain undetectable.
>
> For the degree-three toy generator $G=1010$, a direct three-stage serial remainder register starting at zero obeys $Q_0^+=D_{in}$, $Q_1^+=Q_0\oplus Q_2$, $Q_2^+=Q_1$ when input bits are fed MSB-first. This follows from shifting the remainder and reducing its $x^3$ term by $x^3+x$. The earlier four-stage illustration uses the extended divisor $H=xG$ and must not be assumed identical on arbitrary streams.
>
> Follow [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]], [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-OR Gate]], and [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]] for the stateful implementation and verification against the long-division model.

## 5 · 选用与复习

奇偶校验成本低，不能定位错误；CRC 通过更多约束检测多类错误，也不等于自动纠错。先按规范完整计算，再用单比特和多比特反例测试检错边界。

## Sources · 课件依据

主线课件：[Ch2 lecture](../ECE2050-Chap2.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 2*, PDF p.70：既有奇偶校验定义与判断码组例题；[第二章课件](../ECE2050-Chap2.pdf#page=70)。
- 同课程 *Chapter 5: Combinational Logic Design*, PDF p.11–14：2/3/4 位偶校验发生器与 5 位检查器；[第五章课件](../ECE2050-Chap5.pdf#page=11)。逐节点方程、门数／级数和双比特漏检例子为推导与复核。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
