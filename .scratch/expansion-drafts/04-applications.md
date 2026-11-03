@@NOTE
Seven-Segment Display and Code Conversion|七段显示与码制转换|BCD display decoding|combinational-blocks|Ch6
> [!SUMMARY] Quick recall · 英文速览
> A seven-segment decoder maps a decimal digit code to seven segment commands. Segment position, bit order, output polarity, and blanking controls are separate specifications. Two BCD digits represent $10T+U$, not $16T+U$.

## Core Definition · 核心定义

七段显示器 (seven-segment display) 用七个发光段组成数字字形。BCD-to-seven-segment decoder 把一个 [[Binary Coded Decimal|BCD]] 数字映射为七个点亮命令，是 [[Decoder]] 的应用；它并非普通的 one-hot decoder，因为显示 8 时七段同时有效。

The standard labels are fixed by physical position. A decimal point, if present, is an eighth, separately controlled LED and is not segment g.

| Segment | Position · 位置 | Segment | Position · 位置 |
|---|---|---|---|
| a | Top · 上横段 | d | Bottom · 下横段 |
| b | Upper right · 右上 | e | Lower left · 左下 |
| c | Lower right · 右下 | f | Upper left · 左上 |
| g | Middle · 中横段 | dp | Decimal point · 小数点 |

本篇先定义抽象点亮量 $L_s$：段 $s$ 亮时为 1，灭时为 0。输出表固定采用 **abcdefg** 顺序；不要把它和开发板常见的 `gfedcba` 存储顺序混用。输入 $q_3q_2q_1q_0$ 是 8421 BCD，$q_3$ 为最高位。

## Truth Table and Polarity · 真值表与极性

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

## Assumptions and Validity · 适用前提

1. 合法输入仅为 0–9。`1010`–`1111` 是 invalid BCD codes，没有十进制数字意义。
2. [[Karnaugh Map with Don't Cares|Don't-care rows]] 只表示设计不约束这些输入；它们**不自动等于全灭**。若规范要求非法码 blank，必须明确实现。
3. 每段需要限流；驱动器须满足段电流和共同端总电流。单个共用限流电阻通常会使亮度随亮段数变化。
4. BCD 信号改变后需经过传播延迟才能稳定，见 [[Propagation Delay and Logic Hazards]]。译码器不会自动把非法瞬间或毛刺消除。

For an illustrative direct drive, assume $V_{CC}=3.3\ \mathrm V$, LED forward drop $V_F=2.0\ \mathrm V$, driver drop $V_D=0.1\ \mathrm V$, and desired current $I=5\ \mathrm{mA}$. Then $R=(V_{CC}-V_F-V_D)/I=240\ \Omega$ per segment. These assumed values are a calculation example, not device limits.

## Derivation · 从字形表到逻辑与控制

### Segment logic · 段逻辑

按本篇字体，a 段在数字 $0,2,3,5,6,7,8,9$ 时点亮。把 10–15 作为 don't care，可用 [[Karnaugh Map]] 得到：

$$L_a=q_3+q_1+q_2q_0+\overline{q_2}\,\overline{q_0}.$$

四项分别覆盖高位 8/9、含 2 位权的数字、5/7，以及 0/2/8。逐一代入 1=`0001` 与 4=`0100`，四项均为 0；代入 0 时最后一项为 1。其余段应从各自真值表独立推导。

If invalid BCD inputs must turn all LEDs off, derive an invalid-code detector $I_{bad}=q_3(q_2+q_1)$ and use $L_s^{safe}=\overline{I_{bad}}L_s$. This detector is 1 precisely for 10–15; the simplified segment equation alone does not provide that guarantee.

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

### Dynamic multiplexing · 动态扫描

多位动态显示复用七根段线，通过 digit enable 每次只打开一个共同端。一个扫描槽依次执行 **disable all digits → change segment code → allow settling → enable one digit**，避免旧字形出现在新位上，称为 ghosting。

Let $n$ be the number of digits and $f_{slot}$ the slot rate. Ignoring blanking time, each digit refreshes at $f_{frame}=f_{slot}/n$ with duty cycle $1/n$. Average segment current is approximately duty cycle times on-state current; permissible peak current still comes from the LED and driver ratings.

例如四位显示以 $f_{slot}=1000\ \mathrm{Hz}$ 扫描，每槽 $1\ \mathrm{ms}$，每位每 $4\ \mathrm{ms}$ 更新一次，$f_{frame}=250\ \mathrm{Hz}$。若每槽消隐 $20\ \mu\mathrm s$，该位占空比 $D=(1.00-0.02)/4.00=0.245$；点亮时电流为 $8\ \mathrm{mA}$ 时，平均约 $1.96\ \mathrm{mA}$。

## Code Conversion · BCD 与纯二进制转换

两个 BCD 数字的十位 $T$ 与个位 $U$ 各取 0–9；纯二进制结果为：

$$N=10T+U=(T\ll3)+(T\ll1)+U,\qquad 0\le N\le99.$$

Here $\ll k$ denotes a logical left shift with enough output bits, so the value is multiplied by $2^k$. A 7-bit result is sufficient because $99<128$; concatenating the input nibbles would instead calculate $16T+U$.

### Two 4-bit adders · 两个四位加法器的构造

设 $U=2u+u_0$，其中 $u=\lfloor U/2\rfloor=(0\ U_3\ U_2\ U_1)_2$，$u_0=U_0$。于是：

$$N=2(T+u)+8T+u_0.$$

第一加法器计算 $r=T+u$；合法 BCD 时 $r\le9+4=13$，四位能完整保存。再分解 $r=4h+l$，其中 $h=(r_3r_2)_2$、$l=(r_1r_0)_2$，得到：

$$N=8(T+h)+2l+u_0.$$

第二加法器计算 $s=T+h$，$s\le9+3=12$，同样不溢出。所有位序、输入与输出连接如下；两块加法器的 carry-in 均接 0。

| Block | First 4-bit operand | Second 4-bit operand | Output |
|---|---|---|---|
| Adder 1 | $T_3T_2T_1T_0$ | $0U_3U_2U_1$ | $r_3r_2r_1r_0$ |
| Adder 2 | $T_3T_2T_1T_0$ | $00r_3r_2$ | $s_3s_2s_1s_0$ |
| Result wiring | $N_6N_5N_4N_3=s_3s_2s_1s_0$ | $N_2N_1=r_1r_0$ | $N_0=U_0$ |

Both carry-outs are zero for valid BCD digits, so they are unused **outputs**, not floating inputs. The bound depends on the valid-input assumption; this converter does not validate BCD or provide decimal error detection.

## Worked Examples · 三个实际例题

**1. Display 42.** 输入十位 `0100`、个位 `0010`。按点亮表，4 是 `0110011`，2 是 `1101101`；共阳极直接低有效驱动时分别输出 `1001100`、`0010010`。逐段检查：4 只亮 b,c,f,g，2 不亮 c,f。

The two patterns must be delivered to the corresponding enabled digit. Reversing the digit-select order shows 24 even when both individual segment codes are correct.

**2. Convert BCD 37.** $T=3,U=7,u=3,u_0=1$；第一加法器 $r=3+3=6=0110$，故 $h=01=1,l=10=2$。第二加法器 $s=3+1=4=0100$。拼输出 `0100 10 1`=`0100101`，即 $32+4+1=37$。

As a boundary check, BCD 99 gives $r=13=1101$, $h=3$, $l=1$, and $s=12=1100$. Output `1100 01 1` is `1100011`=99, with no carry overflow in either adder.

**3. Scan 0030.** 零抑制决定逻辑字形 `blank,blank,3,0`；四槽扫描仍保留四个位置，使对齐关系不变。前两槽段命令全灭；第三槽输出 3，第四槽输出 0。将 blank 编成数字 0 会重新点亮前导零。

## Pitfalls and Debugging · 易错点与排查

- **Font versus wiring:** an unusual 6/9 font is different from a missing or crossed segment. Verify the specified table first.
- **Codes versus values:** BCD `0011 0111` means 37; interpreted as an unsigned binary byte, the same bits mean 55.
- **Invalid versus blank:** a K-map X does not command darkness. State the invalid-input policy before simplifying.
- **Polarity versus assertion:** active-low segment voltage 0 can mean “LED on”; HIGH does not universally mean “visible”.
- **Timing versus Boolean correctness:** ghosting often comes from changing segment lines while a digit remains enabled; see [[Digital Logic Troubleshooting]].

## English Exam Q&A · 英文答题训练

**Q: Why are six input combinations unused in a BCD decoder?** Four bits provide sixteen codes, but one decimal digit has only ten values. Codes 1010–1111 are invalid BCD digits; their display behavior must be specified or treated as don't cares.

**Q: How does ripple blanking suppress leading zeros?** A blanked zero asserts the ripple blanking output, enabling blanking in the next lower digit. A nonzero digit releases that signal, so meaningful zeros after it remain visible.

**Q: Why is BCD-to-binary conversion not simple concatenation?** The tens digit has weight ten. The required value is $10T+U$, whereas concatenating two four-bit fields assigns weight sixteen to the upper field.

## Method and Review · 复习检查

Start from [[Binary Coded Decimal]], then use [[Truth Table and Boolean Expression]] and [[Karnaugh Map with Don't Cares]] to derive segment logic. [[Half Adder and Full Adder]] supplies the arithmetic conversion; [[Counters]] and [[Register Enable and Reset]] supply display position and stored data.

检查顺序：段位 a–g → bit order → 0–9 字形 → 电流路径与输出极性 → invalid/blank/LT/RBI policy → scan timing。每一步验证一个独立接口，避免“显示不对”时同时猜所有环节。

索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]

@@NOTE
Digital Logic Troubleshooting|数字逻辑故障诊断|Stuck-at fault testing|combinational-design|Ch5
> [!SUMMARY] Quick recall · 英文速览
> A useful test both activates a fault and propagates its effect to an observable output. A correct output on one input vector does not prove a circuit fault-free. Floating-input behavior requires an electrical model; it is not a universal Boolean constant.

## Core Definition · 核心定义

故障诊断 (troubleshooting) 是把“预期行为”与“实测行为”比较，选择能区分假设的试验，再定位原因。故障检测 (fault detection) 只证明至少有一个故障；故障定位 (fault diagnosis) 还需要区分哪个节点或元件出错。

A Boolean fault model is a simplified hypothesis, not a complete description of physical damage. A **stuck-at-0** node is modeled as always 0; a **stuck-at-1** node is always 1. Opens, bridges, excessive delay, and power faults may require different models.

先读 [[Combinational Circuit]] 确定节点与驱动者，再用 [[Boolean Equation]] 建立每个内部节点的预期函数；实际电压是否可解释为 0/1，要由 [[Logic Levels]] 和 [[Noise Margin]] 判断。

## Assumptions and Validity · 模型与适用条件

本篇布尔推导假设单一故障、输入处于有效逻辑电平、组合逻辑已稳定、测量不改变电路功能。多个故障可能互相掩盖，时序错误可能仅在高速或特定转换时出现。

An open input is **undriven**, not automatically HIGH. The observed level depends on input technology, internal bias, external pull resistors, leakage, coupling, and probe loading. If an exam explicitly states “an open input is read as 1,” use that assumption for that problem only.

CMOS 悬空输入可能在噪声作用下变化或停留在阈值附近；一些特定 TTL 输入在开路时表现为 HIGH，也不能推广到所有器件。未知浮空电压不能仅用布尔代数推出确定的真值表。

| Observation or hypothesis | Appropriate model | What it does not prove |
|---|---|---|
| Node always below valid LOW threshold | Stuck-at-0 candidate | Exact physical root cause |
| Node always above valid HIGH threshold | Stuck-at-1 candidate | Which upstream device failed |
| Input wire open | Undriven input with stated bias | A universal HIGH/LOW value |
| Wrong value only near transitions | Delay, glitch, sampling hypothesis | A static stuck-at fault |
| Both ends appear connected | Connectivity evidence | Adequate voltage or timing |

## Derivation · 故障激活与传播

设正常输出为 $F(\mathbf x)$，故障输出为 $F_f(\mathbf x)$，其中 $\mathbf x$ 是测试输入向量。检测条件是：

$$D_f(\mathbf x)=F(\mathbf x)\oplus F_f(\mathbf x)=1.$$

This is a comparison of good and faulty behavior under **the same input vector**. To detect an internal fault, first make the good node differ from the forced faulty value; then prevent downstream gates from hiding that difference.

故障敏化 (sensitization) 分为两步：**激活 (activation)** 和 **传播 (propagation)**。AND 的控制值 (controlling value) 是 0，OR 的控制值是 1；它们会覆盖另一输入的变化。传播路径上的旁路输入应取 non-controlling value：AND 取 1，OR 取 0。

| Gate on the propagation path | Set side input to | Reason |
|---|---|---|
| AND / NAND | 1 | A changing input still changes the output |
| OR / NOR | 0 | A changing input still changes the output |
| XOR / XNOR | Either fixed value | The output changes with the tested input |

这里说 XOR “两种固定值都能传播”只适用于旁路信号被控制住的情况。若故障同时影响两个 XOR 输入，两条路径的变化可能抵消；这称为 reconvergent masking，需要比较完整函数。

### Boolean sensitivity · 布尔敏感度

把内部节点 $n$ 视作局部变量，$F(n=0)\oplus F(n=1)$ 表示输出是否对 $n$ 敏感。这不是连续微积分导数；它用两个离散条件函数比较可观察性。

For $F=n+C$, sensitivity to n is $C\oplus1=\overline C$. Therefore C must be 0 to observe either stuck-at fault on n. Setting C=1 masks the fault, even when n itself has the wrong value.

## Worked Example 1 · AND–OR 网络的测试向量

正常电路 $n=AB$、$Y=n+C=AB+C$。假设内部节点 n stuck-at-0，故障输出 $Y_f=C$。按 C 分情况：C=1 时正常与故障都为 1；C=0 时差异就是 AB。所以：

$$D_{n/0}=AB\overline C.$$

The detecting vector is ABC=110. The good node n is 1, the faulty node is 0, and C=0 allows the difference to reach Y. ABC=111 activates the fault at n but masks it at the final OR gate.

若 n stuck-at-1，则 $Y_f=1$；要正常输出为 0，必须 C=0 且 AB=0。因此：

$$D_{n/1}=\overline C\,\overline{AB}=\overline C(\overline A+\overline B).$$

检测向量为 000、010、100，任选一个即可检测该假设；例如 000 时正常 Y=0、故障 Y=1。两向量集合 `{110,000}` 能分别检测 n 的两种 stuck-at 假设，却不能证明整个网络所有位置无故障。

| ABC | Good n | Good Y | n/0 output | n/1 output | Interpretation |
|---|---|---|---|---|---|
| 000 | 0 | 0 | 0 | 1 | Detect n/1 |
| 110 | 1 | 1 | 0 | 1 | Detect n/0 |
| 111 | 1 | 1 | 1 | 1 | Both output effects masked |

Moreover, B stuck-at-0 also produces Y=C. At the single observed output, this fault is indistinguishable from n stuck-at-0 for every input. Additional access to B or n, or electrical measurements, is needed for unique diagnosis.

## Worked Example 2 · MUX 的选择故障

一个 [[Multiplexer and Demultiplexer|2:1 MUX]] 满足 $Y=\overline S D_0+SD_1$。若选择端 S stuck-at-0，故障输出一直为 $D_0$。差异只在命令 S=1 且两个数据不同的时候出现：

$$D_{S/0}=S(D_0\oplus D_1).$$

Choose $(S,D_0,D_1)=(1,0,1)$. Good Y=1 and faulty Y=0. The vector (1,1,1) changes the selected route but gives the same data on both routes, so it cannot reveal a selection fault.

若只测试 `D0=D1=0` 和 `D0=D1=1`，会验证输出能高能低，却完全没有检查“选择是否正确”。实际测试应包括两路相反的数据，再交替选择。

For S stuck-at-1, use S=0 and unequal data. Exhaustive tests of all eight combinations also reveal data-input faults, but a failed output still needs a fault hypothesis before locating the cause.

## Worked Example 3 · 显示与转换器的故障症状

**Display symptom.** [[Seven-Segment Display and Code Conversion|七段显示]] 设定为 8，却看起来像 0。按标准字形，唯一差别为 g 段。因此候选原因包括 g 输出无效、g 连线/限流电阻开路、g 段损坏；一个外观症状无法区分这三者。

Command 0 and then 8 while holding the digit-select timing fixed. Segment g should change from off to on. Measure the driver output, then the segment voltage/current path; lamp test can help separate normal digit decoding from a segment-path failure.

若动态扫描每个数字都暗，先检查共同端与 digit enable；若只有一个数字异常，优先比较该位的共同端。若只有换位时有短暂重影，检查消隐时序，不能仅靠静态真值表找原因。

**Converter symptom.** 合法两位 BCD 转换器应输出 $N=10T+U$。从 00 递增测试，若纯二进制结果位 $N_5$（位权 32）stuck-at-0，00–31 都可能正确，第一次在 BCD 32 时可检测：正常 `0100000`，故障 `0000000`。

This example explains why testing only the largest value is weak: a particular fault may be masked by its expected bit value. A walking-bit or structured input set must be chosen from the function and fault model; not every converter bit can be independently controlled by arbitrary invalid BCD codes.

## Method and Steps · 实际排查流程

1. **State the symptom precisely.** Which output, which input vector or transition, and what expected value? Distinguish a repeatable failure from an intermittent one.
2. **Check the operating foundation.** 电源、地、时钟、复位与使能先确认；它们出错会让许多逻辑节点同时异常。
3. **Establish a good model.** 标节点，逐级写方程；有状态电路先指定初态与采样边沿，见 [[Sequential Logic]]。
4. **Choose a discriminating test.** 激活候选故障，把旁路输入设为不遮蔽值，再观察有效输出或中间节点。
5. **Measure from cause toward symptom.** Compare expected and measured values at successive nodes, respecting probe loading and instrument bandwidth.
6. **Verify the correction.** 重测原失败向量、相邻边界与关键转换；修好某个输入下的结果不是全部验证。

逻辑探针适合稳定的 HIGH/LOW，示波器适合电压幅度、边沿、毛刺与时延，逻辑分析仪适合多路数字时序。使用逻辑分析仪的数字判决结果前，仍需检查阈值是否适合被测电路。

## Common Errors · 常见误区

- A correct static truth table does not prove setup/hold timing or freedom from glitches; use [[Setup and Hold Timing]].
- 开路输出后的**接收输入**和开路之前的**驱动输出**是两个不同节点，不能继续当成同一根导线。
- Fault detection is not unique diagnosis. Two hypotheses with identical output functions need another observation point.
- 测到中间电压时应先承认逻辑值不确定；不要把所有结果强塞成 0/1，再做错误的布尔证明。
- Test vectors are meaningful only with the assumed input order, active polarity, and initial state stated explicitly.

## English Exam Q&A · 英文答题训练

**Q: Why must the side input of an OR gate be LOW when propagating a fault?** HIGH is the controlling value of OR and forces the output HIGH. LOW allows the tested input to determine the output.

**Q: Is an open input equivalent to stuck-at-1?** Only if the problem specifies that the undriven input is reliably interpreted as 1. In physical hardware, floating-input behavior depends on the device and bias network.

**Q: Can a test detect a fault without identifying its location?** Yes. Different faults may produce the same observable function. Detection proves a mismatch; diagnosis needs observations that distinguish the competing hypotheses.

## Method and Review · 复习检查

Use [[Proof by Perfect Induction]] to enumerate good and faulty functions, [[Laws and Rules of Boolean Algebra]] to derive detecting conditions, and [[Propagation Delay and Logic Hazards]] to separate static faults from transition problems.

每次结论应能补完一句：“在假设 ___ 下，输入 ___ 使正常节点为 ___、故障节点为 ___，并通过 ___ 路径到输出，所以可检测；但仍不能区分 ___。”

索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]

@@NOTE
Exam Review and Problem Solving|考试复习与解题方法|Digital logic exam review|review|Review
> [!SUMMARY] Quick recall · 英文速览
> Read the specification before choosing a technique. Record representation, width, variable order, active polarity, clock edge, and initial state. Derive intermediate results, then use an independent check rather than relying on a printed solution.

## Core Definition · 核心目标

这篇是复习导航与解题模板，不替代各概念的详细推导。数字逻辑题通常要求完成一条可验证的链：**文字规范 → 数学/状态模型 → 电路或代码 → 功能与时序检查**。

An answer should state what the circuit means before showing how it is built. “Simplify,” “canonical,” “implement,” “trace,” and “design” request different deliverables; a correct simplified expression can still be the wrong answer to a canonical-form question.

## Learning Path · 按先修关系复习

| Stage | Prerequisite → next topic | Exit question · 自查问题 |
|---|---|---|
| 1. Representation | [[Number Systems]] → [[Number Base Conversion]] → [[Two's Complement Representation]] | Can I explain the value of these bits at this width? |
| 2. Boolean meaning | [[Logic Gates]] → [[Truth Table and Boolean Expression]] → [[Minterm and Maxterm]] | Can I identify exactly which rows produce 1/0? |
| 3. Simplification | [[Laws and Rules of Boolean Algebra]] → [[Karnaugh Map]] → [[POS Minimization with Karnaugh Map]] | Is the result equivalent on every required row? |
| 4. Building blocks | [[Combinational Logic Design]] → [[Decoder]] / [[Multiplexer and Demultiplexer]] / [[Half Adder and Full Adder]] | Can I connect all inputs with correct polarity? |
| 5. Stored state | [[Sequential Logic]] → [[D Latch and D Flip-Flop]] → [[Register Enable and Reset]] → [[Shift Registers]] | Which values are sampled, held, or updated? |
| 6. State design | [[Finite State Machine]] → [[Moore and Mealy Machines]] → [[State Encoding and Unused States]] | Does every state/input pair have a defined transition? |
| 7. System use | [[Counters]] → [[Memory Arrays and Expansion]] / [[Read-Only Memory and Programmable Logic Arrays]] → [[VHDL Language and Modeling]] | Can I connect function, state, storage, and implementation? |

先补最早断开的依赖，不要直接背后续式子。看不懂 counter 激励表时，先回 [[JK and T Flip-Flops]]；看不懂 ROM 地址宽度时，先回 [[Bits and Bytes]] 与 [[Binary Number System]]。

For each topic, practice four passes: explain it in one English sentence, derive one result in Chinese, solve a small example without notes, and check the answer using another representation. Review the resulting error pattern rather than rereading every page equally.

## Read the Question · 先把题意变成约束

在草稿第一行记录六项：**representation / width / bit order / polarity / clock edge / initial state**。不适用的项目写“combinational”或“unsigned”，不要留下可能改变答案的空白。

Words such as **exactly**, **at least**, **highest priority**, **overlapping**, **synchronous**, and **asynchronous** change the model. Underline them and translate them into a table or equation before drawing gates.

“至少两个为 1”在三输入时是 $AB+AC+BC$，包含 111；“恰好两个为 1”是 $AB\overline C+A\overline BC+\overline ABC$，不包含 111。先列边界反例能防止把两种要求混同。

## Number Problems · 数制与算术题

1. 确定位串是 unsigned、two's complement、sign magnitude、BCD 还是浮点；同一位串可能有不同值。
2. 对 signed arithmetic 先写十进制预期符号与大致大小，再按固定宽度计算。扩位时 two's complement 要 sign extension。
3. 区分 carry 与 signed overflow。负数加正数不会因最终 carry=1 就自动 overflow。
4. Binary↔octal/hex grouping begins at the binary point. Pad zeros only at the outside ends; never move the point.
5. For [[Cyclic Redundancy Check]], divide with XOR, append degree-many zeros, and transmit exactly degree-many remainder bits.

**Mini-example — signed multiplication.** 4 位 two's complement `1011`=-5、`1101`=-3，乘积 +15。若要求完整 8 位结果，应写 `00001111`；`1111` 在 4 位 signed 模型下是 -1。数学值正确仍需满足输出宽度。

**Mini-example — fractional grouping.** `10.101101₂`：向三位分组得 `010.101 101`，故 $2.55_8$；向四位分组得 `0010.1011 0100`，故 $2.B4_{16}$。二者都等于 $2+45/64=2.703125$。

## Boolean Forms and K-maps · 标准式与卡诺图

Canonical SOP lists minterms for every 1 row; canonical POS lists maxterms for every 0 row. Each canonical term contains every variable once. A simplified SOP/POS need not contain every variable in each term.

对变量顺序 ABC，$F=AB+C$ 在编号 1,3,5,6,7 为 1，所以：

$$F=\Sigma m(1,3,5,6,7)=\Pi M(0,2,4).$$

若要求完整 standard POS，应展开为 $(A+B+C)(A+\overline B+C)(\overline A+B+C)$。最简 POS $(A+C)(B+C)$ 与它等价，但不是 canonical POS。

K-map procedure: label axes in Gray-code order; fill cells from the specification; group 1s for SOP or 0s for POS; use power-of-two rectangular groups and wraparound adjacency; remove changing variables; check all required cells afterward.

Don't cares 可以选用，也可以不选；组必须帮助覆盖 required 1/0，不能单独圈一组 X 当成必需项。规范要求 unused states recover 时，不能把其 next-state rows 全部丢成 X。

A quick consistency check uses the original truth table, not the drawing alone. For $F=AB+C$, C=1 must produce F=1 for all A/B, and C=0 must reduce to AB. These two cofactors catch many misplaced K-map groups.

## Gate and Block Implementation · 门与功能块实现

**NAND only.** 先得 SOP，再应用 [[DeMorgan's Theorems]]。对 $F=AB+C$，令 $n_1=\overline{AB}=\operatorname{NAND}(A,B)$，$n_2=\overline C=\operatorname{NAND}(C,C)$，最终 $F=\operatorname{NAND}(n_1,n_2)$。三个门，输入反相信号由实际 NAND 生成。

Draw each inversion explicitly. If complementary inputs are unavailable, account for the inverter gates and their delay. Bubble pushing preserves a function only when the gate operation changes consistently with the moved inversions; use [[Universal Gates and Bubble Pushing]].

**MUX.** 固定选择顺序 $(S_1,S_0)=(A,B)$，把每组 AB 下的 F 写成剩余变量 C 的函数：00→C，01→C，10→C，11→1。故 4:1 MUX 的 $(D_0,D_1,D_2,D_3)=(C,C,C,1)$。

For a decoder, first identify whether the outputs are minterms $m_i$ or active-low complements $\overline{m_i}$. OR the selected active-high lines; NAND the selected active-low lines. Set enable inputs to their asserted levels rather than leaving them unspecified.

**Adders and comparators.** 从最低位处理 carry/borrow，从最高位判断无符号大小。检查最终 carry、sum width 与 signed interpretation；器件级联输入也属于功能规范，见 [[Ripple Carry and Carry Look-Ahead Adders]] 与 [[Magnitude Comparator]]。

## Timing Problems · 时序约束题

先把 launch register → combinational path → capture register 的方向标清。忽略 clock skew 时：

$$T\ge t_{pcq}+t_{pd,comb}+t_{setup},\qquad t_{ccq}+t_{cd,comb}\ge t_{hold}.$$

$t_{pcq}$、$t_{pd,comb}$ 是最大延迟；$t_{ccq}$、$t_{cd,comb}$ 是最小延迟。Setup 用最长路径，hold 用最短路径，两者不是把同一组数字代两次。详细 skew 约定见 [[Setup and Hold Timing]]。

**Mini-example.** $t_{pcq}=2\ \mathrm{ns}$、最长组合延迟 $7\ \mathrm{ns}$、setup $1\ \mathrm{ns}$：$T_{min}=10\ \mathrm{ns}$，$f_{max}=100\ \mathrm{MHz}$。若 $t_{ccq}=0.5\ \mathrm{ns}$、最短组合延迟 $0.2\ \mathrm{ns}$、hold $1\ \mathrm{ns}$，则 $0.7<1$，hold 失败。

Increasing the clock period can resolve a setup violation but does not fix the stated hold violation. A hold repair needs extra minimum data-path delay or an appropriate clock-path change, verified under a defined timing model.

## State Tracing and FSM Design · 状态追踪与状态机设计

追踪同步电路时，每个有效时钟边沿前先计算**全部** next-state/激励输入，再同时更新全部触发器。不可更新 $Q_0$ 后立刻把新 $Q_0$ 用于同一边沿的 $Q_1$；那会把同步电路误算成连锁的软件赋值。

For a three-bit shift register with $Q_2^+=Q_1$, $Q_1^+=Q_0$, $Q_0^+=d$, initial 000 and serial data 1,0,1,1, the post-edge states are 001,010,101,011. The displayed word order and serial input position are stated explicitly.

FSM design proceeds through meaning of states → transitions → output rules → encoding → next-state table → flip-flop inputs → implementation. Moore output depends on current state; Mealy output depends on state and current input. Determine whether an observed output is before or after a clock edge.

For D flip-flops, $D_i=Q_i^+$. For J-K flip-flops, use the excitation table for the requested $Q_i\to Q_i^+$ transition; its don't cares are different from unspecified functional states. Include reset and unused-state behavior before minimization.

### Word matching versus serial matching · 并行字匹配与串行序列

四个同时输入 ABCD 表示一个四位字，要求字中含连续 `110` 时，只有两种位置：ABC=110 或 BCD=110。

$$Y=AB\overline C+BC\overline D=\Sigma m(6,12,13,14).$$

例：0110、1100、1101、1110 为 1，1011 为 0。对应 POS 是 $Y=B(A+C)(\overline C+\overline D)$。用 consensus theorem 可知展开后多出的 $AB\overline D$ 不改变函数，也可枚举全部 16 个字校验。

This is combinational substring matching. A serial detector receives one bit per clock and must remember a suffix of earlier inputs; use [[Sequence Detector]]. “Sequence 110” alone does not tell you which interface is intended.

## Counter and ROM Problems · 计数器与查表存储

**Counter.** 写出 requested cycle 而不是只猜 toggle 式；计算模数为周期内不同状态数。同步 modulus-3 例：00→01→10→00，并规定 unused 11→00，可得：

$$D_1=\overline Q_1Q_0,\qquad D_0=\overline Q_1\,\overline Q_0.$$

这四个状态代入分别得到 01、10、00、00。某个状态解码输出每三拍重复一次，频率 $f_{clk}/3$，但脉宽只一拍时 duty cycle 是 1/3，不是 50%。模数不等于电路所有可能编码数。

For a binary counter DOWN transition from 1000, the next four-bit word is 0111. For a BCD decade counter, define its legal range and wrap rule separately; the word “counter” does not select a number representation.

**ROM.** $a$ address bits give $2^a$ words; word width w gives capacity $2^aw$ bits. 一个把三位 ABC 中 1 的个数输出为两位二进制的 ROM，需要 $8\times2=16$ bits，其地址 000–111 的数据为 `00,01,01,10,01,10,10,11`。

Use input combinations as addresses and the complete output word as stored data. A ROM implements a truth table; it does not need a separate OR gate for each output when the lookup contents already encode the result.

## VHDL Problems · 从行为到硬件

Read the **entity** as an interface and the **architecture** as a hardware description. Concurrent assignments coexist; a clocked process updates registers on its specified edge. Signal assignments in one process do not behave like immediate updates to ordinary programming variables.

组合过程应给每个输出在所有分支赋值，防止意外 latch；时序过程必须明确 reset/enable 的优先级。算术先确认 `unsigned`/`signed` 与位宽，不能仅因为 `std_logic_vector` 长得像二进制数就假定其数值语义。

**Mini-example — unintended latch.** `if en='1' then y <= a; end if;` 放在组合过程时，en=0 分支没有给 y 新值，描述了保存旧值。若目标为组合选择器，应补 `else y <= '0';`；若目标为保存数据，应在时钟过程里描述 enable register。

Check simulation against the same truth/state table used for the hand derivation, using [[Testbench and Functional Verification]]. Test reset, hold/enable, boundary inputs, and several clock edges; one attractive waveform is not proof of complete coverage.

## Checking Reference Solutions · 如何使用参考答案

参考答案适合比较方法，但每个结论仍需符合题意、位宽与图中极性。教材剪贴页中的“negative edge”说明可能属于旁边另一个示例；如果实际题目指定 positive-edge，必须按本题边沿计算。

One supplied CRC example uses data `10110010` and generator `1010` but appends four zeros and reports a twelve-bit code. The generator has degree three, so the conventional systematic CRC model needs three appended zeros and a three-bit remainder.

按该模型，$10110010000\div1010$ 的 XOR 余数为 `110`，正确发送码为 **`10110010110`**（8+3=11 bits）；再除一次余数为 0。生成式常数项为 0 还意味着它不具备常用 CRC 生成多项式的一般选择特性，但不改变这里的除法位数。

Check answers independently: evaluate all rows for small Boolean functions, decode arithmetic results back to decimal, trace state cycles, verify timing inequalities, and divide the transmitted CRC word again. A successful check should use the original specification rather than repeating the same possibly wrong intermediate equation.

## English Exam Q&A · 常用完整答句

**Q: How do canonical and simplified forms differ?** Every term in a canonical form contains all variables. Simplification removes unnecessary literals while preserving the function on the specified input combinations.

**Q: Why does a synchronous state trace use old values?** All registers sample their inputs at the same active edge. Their new outputs appear only after clock-to-Q delay, so the next-state equations are evaluated from the pre-edge state.

**Q: Why can a slower clock leave a failure unresolved?** Hold time constrains the earliest arrival of new data after the capture edge. Changing the cycle period does not, by itself, delay that earliest arrival.

## Method and Review · 考前自查

- I can name the representation and justify the required width.
- I can distinguish canonical forms, minimal forms, and a physical implementation.
- I can translate an active-low pin into asserted/inactive behavior.
- I can evaluate next-state logic before updating the current state.
- I can explain why my test vectors cover the requirement and state what remains untested.

把每道错题归到“概念/题意/符号/推导/验证”中的一类，回到对应的 canonical note 修正理解。需要电路故障敏化时转到 [[Digital Logic Troubleshooting]]；需要 display/BCD 综合题时转到 [[Seven-Segment Display and Code Conversion]]。

索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
