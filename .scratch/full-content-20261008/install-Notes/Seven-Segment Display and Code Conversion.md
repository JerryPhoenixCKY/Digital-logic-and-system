---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
updated: 2026-10-09
chapter: Ch6
aliases:
  - 七段显示与码制转换
  - Seven-Segment Display and Code Conversion
  - 七段显示与码制转换 · Ch6
  - BCD display decoding
---

# Seven-Segment Display and Code Conversion · 七段显示与码制转换

> [!SUMMARY] Quick recall · 英文速览
> Segment truth tables describe lit shapes; electrical polarity maps those commands to levels. BCD-to-binary conversion preserves the decimal value.

## 1 · 字形先于电平

七段显示 (seven-segment display) 先以 a–g 是否亮定义字形，再按共阳／共阴映射驱动极性。定义 BCD 位序、非法码行为与小数点是否独立；同一个字形表的高低有效电平表可能互补。

位置约定：a 为上横，b／c 为右上／右下，d 为下横，e／f 为左下／左上，g 为中横；小数点 dp 独立控制。每段需按电压与目标电流限流，共同端驱动还要承受所有亮段的总电流。新增晶体管可能再次反相，须沿真实电流路径判断驱动极性。

### Core Definition · 核心定义

七段显示器 (seven-segment display) 用七个发光段组成数字字形。BCD-to-seven-segment decoder 把一个 [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码|BCD]] 数字映射为七个点亮命令，是 [[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 的应用；它并非普通的 one-hot decoder，因为显示 8 时七段同时有效。

The standard labels are fixed by physical position. A decimal point, if present, is an eighth, separately controlled LED and is not segment g.

| Segment | Position · 位置 | Segment | Position · 位置 |
|---|---|---|---|
| a | Top · 上横段 | d | Bottom · 下横段 |
| b | Upper right · 右上 | e | Lower left · 左下 |
| c | Lower right · 右下 | f | Upper left · 左上 |
| g | Middle · 中横段 | dp | Decimal point · 小数点 |

本篇先定义抽象点亮量 $L_s$：段 $s$ 亮时为 1，灭时为 0。输出表固定采用 **abcdefg** 顺序；不要把它和开发板常见的 `gfedcba` 存储顺序混用。输入 $q_3q_2q_1q_0$ 是 8421 BCD，$q_3$ 为最高位。

### Assumptions and Validity · 适用前提

1. 合法输入仅为 0–9。`1010`–`1111` 是 invalid BCD codes，没有十进制数字意义。
2. [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Don't-care rows]] 只表示设计不约束这些输入；它们**不自动等于全灭**。若规范要求非法码 blank，必须明确实现。
3. 每段需要限流；驱动器须满足段电流和共同端总电流。单个共用限流电阻通常会使亮度随亮段数变化。
4. BCD 信号改变后需经过传播延迟才能稳定，见 [[Propagation Delay and Logic Hazards]]。译码器不会自动把非法瞬间或毛刺消除。

For an illustrative direct drive, assume $V_{CC}=3.3\ \mathrm V$, LED forward drop $V_F=2.0\ \mathrm V$, driver drop $V_D=0.1\ \mathrm V$, and desired current $I=5\ \mathrm{mA}$. Then $R=(V_{CC}-V_F-V_D)/I=240\ \Omega$ per segment. These assumed values are a calculation example, not device limits.

### Truth Table and Polarity · 真值表与极性

The following table uses active-high **light commands**, independent of the voltage polarity required by a particular driver. The chosen font lights a on 6 and d on 9; other fonts must be specified explicitly.

| Digit | BCD | a | b | c | d | e | f | g | abcdefg |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0000 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1111110 |
| 1 | 0001 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0110000 |
| 2 | 0010 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1101101 |
| 3 | 0011 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1111001 |
| 4 | 0100 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0110011 |
| 5 | 0101 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 1011011 |
| 6 | 0110 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1011111 |
| 7 | 0111 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1110000 |
| 8 | 1000 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1111111 |
| 9 | 1001 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1111011 |

共阴极 (common cathode, CC)：各段阴极接共同低电位，段阳极获得合适的正向电压与电流时点亮。直接驱动的抽象模型中，输出 HIGH 对应亮段。

共阳极 (common anode, CA)：各段阳极接共同高电位，驱动器把相应阴极拉低并吸收电流 (sink current) 时点亮。直接低有效驱动时，物理输出 $P_s=\overline{L_s}$；例如 1 的物理 **abcdefg** 模式为 `1001111`。

An added transistor can invert this relationship. Always trace the driver and LED current path before assigning a voltage-level truth table. “Common anode” describes the LED connection, not every possible upstream control signal.

### Method and Review · 复习检查

Start from [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码|Binary Coded Decimal]], then use [[Boolean Forms and Algebraic Simplification#2 · Truth Table and Boolean Expression · 用真值表定义全集|Truth Table and Boolean Expression]] and [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]] to derive segment logic. [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|Half Adder and Full Adder]] supplies the arithmetic conversion; [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] and [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]] supply display position and stored data.

检查顺序：段位 a–g → bit order → 0–9 字形 → 电流路径与输出极性 → invalid/blank/LT/RBI policy → scan timing。每一步验证一个独立接口，避免“显示不对”时同时猜所有环节。

## 2 · 字形表到组合逻辑

每段是独立布尔输出，按对应 ON／OFF 行化简。无效 BCD 输入只有规范允许时才能作为 X。显示 8 应点亮七段，显示 0 应关闭 g 段，这两个输入有助于定位 g 的故障。

### Segment logic · 段逻辑

按本篇字体，a 段在数字 $0,2,3,5,6,7,8,9$ 时点亮。把 10–15 作为 don't care，可用 [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并|Karnaugh Map]] 得到：

$$L_a=q_3+q_1+q_2q_0+\overline{q_2}\,\overline{q_0}.$$

四项分别覆盖高位 8/9、含 2 位权的数字、5/7，以及 0/2/8。逐一代入 1=`0001` 与 4=`0100`，四项均为 0；代入 0 时最后一项为 1。其余段应从各自真值表独立推导。

If invalid BCD inputs must turn all LEDs off, derive an invalid-code detector $I_{bad}=q_3(q_2+q_1)$ and use $L_s^{safe}=\overline{I_{bad}}L_s$. This detector is 1 precisely for 10–15; the simplified segment equation alone does not provide that guarantee.

## 3 · Blanking and Zero Suppression · 控制输出可见性

消隐 (blanking) 强制关闭显示；零抑制 (zero suppression) 隐藏前导零，却需保留数值中间的零。BI、RBI、RBO 等信号的极性与优先级须按给定器件／题目模型解释。

### Blanking and zero suppression · 消隐与零抑制

消隐 (blanking) 是强制全灭。灯测试 (lamp test, LT) 是强制全亮。零抑制 (zero suppression) 只隐藏数值表示中不必要的前导或末尾 0，不能任意删除数字内部的 0。

For the **active-low decoder model used here**, $\overline{LT}=0$ with $\overline{BI}/\overline{RBO}=1$ lights every segment. External $\overline{BI}=0$ blanks the display. With normal lamp-test and blanking conditions, digit=0 and $\overline{RBI}=0$ blank that zero and assert $\overline{RBO}=0$.

这里 $\overline{RBI}$ 是 ripple blanking input，$\overline{RBO}$ 是 ripple blanking output。当前位抑制 0 后，把 LOW 送到下一位，允许继续抑制；遇到非零位时，RBO 释放为 HIGH，后续 0 便正常显示。这些控制属于特定器件功能；仅凭“七段译码器”名称不能推定它们存在。

| Normal-mode condition | Display action | $\overline{RBO}$ role |
|---|---|---|
| BCD=0, $\overline{RBI}=0$ | Blank zero | Assert LOW to continue |
| BCD=0, $\overline{RBI}=1$ | Display 0 | Release HIGH |
| BCD=1–9 | Display digit | Release HIGH |

前导零链从最高位走向较低位。`0030` 的前两位 0 消隐，3 终止传播，最后一位 0 保留，所以得到 `30`。若所有数字为 0 而仍要显示一个 0，可令最低位 RBI 不接受消隐链。

Trailing-zero suppression on a fractional field runs from the least significant fractional digit toward the decimal point. For `0.5700`, suppress the two rightmost zeros but keep the integer 0 and decimal-point placement under separate control. Never connect one chain indiscriminately across the decimal boundary.

BI/RBO 可能共用引脚且具有特殊输出结构；输出与外部强制电平的连接必须按该器件接口处理。逻辑 LOW/HIGH 的功能表不能证明 push-pull 输出可以直接短接。

## 4 · 动态扫描与共同端

共享段线、逐位开启共同端；换位前先关闭显示，更新段数据后再开启下一位，以减少重影。完整帧频率等于扫描槽频率除以位数，不能把时钟频率直接当作每位刷新率。

### Dynamic multiplexing · 动态扫描

多位动态显示复用七根段线，通过 digit enable 每次只打开一个共同端。一个扫描槽依次执行 **disable all digits → change segment code → allow settling → enable one digit**，避免旧字形出现在新位上，称为 ghosting。

Let $n$ be the number of digits and $f_{slot}$ the slot rate. Ignoring blanking time, each digit refreshes at $f_{frame}=f_{slot}/n$ with duty cycle $1/n$. Average segment current is approximately duty cycle times on-state current; permissible peak current still comes from the LED and driver ratings.

例如四位显示以 $f_{slot}=1000\ \mathrm{Hz}$ 扫描，每槽 $1\ \mathrm{ms}$，每位每 $4\ \mathrm{ms}$ 更新一次，$f_{frame}=250\ \mathrm{Hz}$。若每槽消隐 $20\ \mu\mathrm s$，该位占空比 $D=(1.00-0.02)/4.00=0.245$；点亮时电流为 $8\ \mathrm{mA}$ 时，平均约 $1.96\ \mathrm{mA}$。

> [!example]- Seven-Segment Display and Code Conversion · 推导与例题
> **Pitfalls and Debugging · 易错点与排查**
>
> - **Font versus wiring:** an unusual 6/9 font is different from a missing or crossed segment. Verify the specified table first.
> - **Codes versus values:** BCD `0011 0111` means 37; interpreted as an unsigned binary byte, the same bits mean 55.
> - **Invalid versus blank:** a K-map X does not command darkness. State the invalid-input policy before simplifying.
> - **Polarity versus assertion:** active-low segment voltage 0 can mean “LED on”; HIGH does not universally mean “visible”.
> - **Timing versus Boolean correctness:** ghosting often comes from changing segment lines while a digit remains enabled; see [[Digital Logic Troubleshooting]].

### English Exam Q&A · 英文答题训练

**Q: Why are six input combinations unused in a BCD decoder?** Four bits provide sixteen codes, but one decimal digit has only ten values. Codes 1010–1111 are invalid BCD digits; their display behavior must be specified or treated as don't cares.

**Q: How does ripple blanking suppress leading zeros?** A blanked zero asserts the ripple blanking output, enabling blanking in the next lower digit. A nonzero digit releases that signal, so meaningful zeros after it remain visible.

**Q: Why is BCD-to-binary conversion not simple concatenation?** The tens digit has weight ten. The required value is $10T+U$, whereas concatenating two four-bit fields assigns weight sixteen to the upper field.

## 5 · Code Conversion · 数值守恒与位权

两位 BCD 数字 T、U 满足 $N=10T+U=8T+2T+U$，结果范围 0–99，需七位纯二进制。两个四位加法器的连接需逐位检查进位和权重，不能把 BCD 字节当纯二进制直接送出。

> [!IMPORTANT] 三张表要一致
> 数字→点亮段；段命令→电平；BCD→数值。分别核对规范、极性与使能，再检查扫描时序。

> [!example]- Seven-Segment Display and Code Conversion · 推导与例题
> **Code Conversion · BCD 与纯二进制转换**
>
> 两个 BCD 数字的十位 $T$ 与个位 $U$ 各取 0–9；纯二进制结果为：
>
> $$N=10T+U=(T\ll3)+(T\ll1)+U,\qquad 0\le N\le99.$$
>
> Here $\ll k$ denotes a logical left shift with enough output bits, so the value is multiplied by $2^k$. A 7-bit result is sufficient because $99<128$; concatenating the input nibbles would instead calculate $16T+U$.
>
> **Two 4-bit adders · 两个四位加法器的构造**
>
> 设 $U=2u+u_0$，其中 $u=\lfloor U/2\rfloor=(0\ U_3\ U_2\ U_1)_2$，$u_0=U_0$。于是：
>
> $$N=2(T+u)+8T+u_0.$$
>
> 第一加法器计算 $r=T+u$；合法 BCD 时 $r\le9+4=13$，四位能完整保存。再分解 $r=4h+l$，其中 $h=(r_3r_2)_2$、$l=(r_1r_0)_2$，得到：
>
> $$N=8(T+h)+2l+u_0.$$
>
> 第二加法器计算 $s=T+h$，$s\le9+3=12$，同样不溢出。所有位序、输入与输出连接如下；两块加法器的 carry-in 均接 0。
>
> | Block | First 4-bit operand | Second 4-bit operand | Output |
> |---|---|---|---|
> | Adder 1 | $T_3T_2T_1T_0$ | $0U_3U_2U_1$ | $r_3r_2r_1r_0$ |
> | Adder 2 | $T_3T_2T_1T_0$ | $00r_3r_2$ | $s_3s_2s_1s_0$ |
> | Result wiring | $N_6N_5N_4N_3=s_3s_2s_1s_0$ | $N_2N_1=r_1r_0$ | $N_0=U_0$ |
>
> Both carry-outs are zero for valid BCD digits, so they are unused **outputs**, not floating inputs. The bound depends on the valid-input assumption; this converter does not validate BCD or provide decimal error detection.
>
> **Worked Examples · 三个实际例题**
>
> **1. Display 42.** 输入十位 `0100`、个位 `0010`。按点亮表，4 是 `0110011`，2 是 `1101101`；共阳极直接低有效驱动时分别输出 `1001100`、`0010010`。逐段检查：4 只亮 b,c,f,g，2 不亮 c,f。
>
> The two patterns must be delivered to the corresponding enabled digit. Reversing the digit-select order shows 24 even when both individual segment codes are correct.
>
> **2. Convert BCD 37.** $T=3,U=7,u=3,u_0=1$；第一加法器 $r=3+3=6=0110$，故 $h=01=1,l=10=2$。第二加法器 $s=3+1=4=0100$。拼输出 `0100 10 1`=`0100101`，即 $32+4+1=37$。
>
> As a boundary check, BCD 99 gives $r=13=1101$, $h=3$, $l=1$, and $s=12=1100$. Output `1100 01 1` is `1100011`=99, with no carry overflow in either adder.
>
> **3. Scan 0030.** 零抑制决定逻辑字形 `blank,blank,3,0`；四槽扫描仍保留四个位置，使对齐关系不变。前两槽段命令全灭；第三槽输出 3，第四槽输出 0。将 blank 编成数字 0 会重新点亮前导零。

## Sources · 课件依据

主线课件：[Ch6 lecture](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
