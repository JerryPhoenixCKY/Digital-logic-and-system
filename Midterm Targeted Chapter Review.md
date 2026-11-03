---
tags:
  - ECE2050
  - review
date: 2026-10-29
updated: 2026-10-29
chapter: Ch1–6
aliases:
  - Midterm Targeted Chapter Review
  - 期中逐章重点难点与针对性复习
  - 数字逻辑期中样卷导向复习
---

# Midterm Targeted Chapter Review · 期中逐章重点、难点与针对性复习

> [!SUMMARY] Scope · 使用范围
> 本篇按本学期 Ch1–6 与四份历史样卷整理：**重点是样卷出现的能力，难点是容易丢分的推理和条件**。样卷频率只影响练习顺序，不代表考试预测，也不意味着其他课件内容可跳过。2026 年卷日期为 3 月，是历史样卷。
>
> 先按每章的“重点 → 难点 → 做题步骤 → 样卷”复习；公式完整表见 [[Midterm Formula Sheet]]，基础不清先读 [[Midterm Review Guide]]，诊断题和四卷题目地图见 [[Midterm Practice and Answers]]。总览见 [[Midterm Knowledge Outline]]。

## Priority · 时间有限时怎样排序

| 顺序 | 先掌握什么 | 为什么先练 | 验收标准 |
|---|---|---|---|
| 1 | Ch2 补码、数制、BCD 与校验 | 四卷均有数制或编码计算 | 限位宽算出数值，并独立判断溢出 |
| 2 | Ch4 标准 SOP/POS 与 K-map | 多卷把它们作为后续电路实现的入口 | 真值表、标准式、最简式能互相验证 |
| 3 | Ch5 文字需求、NAND 实现与波形 | 综合设计和故障题需要完整流程 | 先列状态再化简，逐门画出等价电路 |
| 4 | Ch6 MUX/decoder、加法器、延迟、显示 | 多份样卷有器件连接或路径题 | 根据题目给出的引脚、极性、使能逐位连接 |
| 5 | Ch3 门与电平、Ch1 基础概念 | 支撑判断题与全部后续题 | 能解释真值表、波形与噪声容限 |

此排序是对这四份卷子的学习安排：例如 MUX 实现出现在 **2024 Q6、2025 秋 Q7、2026 Q7**，2025 春卷的对应综合功能题是译码器，并非 MUX。不要把题型出现次数当成出题概率或分值保证。

## Ch1 · Digital Foundations · 数字基础

**重点。** 数字抽象 (digital abstraction) 用逻辑 0/1 解释连续变化的实际电压；组合逻辑 (combinational logic) 的稳定输出由当前输入决定，时序逻辑 (sequential logic) 含状态。正逻辑把 HIGH 对应 1，而低有效 (active-low) 描述功能在 LOW 时有效。波形要认周期 $T$、高电平时间 $t_H$、频率 $f=1/T$ 和高电平占空比 $D_H=t_H/T$。低有效脉冲的有效占空比改用低电平时间。

**难点与失分点。** 上升时间衡量某个信号的边沿变化，传播延迟衡量输入改变到输出响应；两者不相同。门或使能端带圆圈要按低有效解释，不能把 LOW 一概看作“关闭”。一位触发器有两个状态，但只保存一位。

**针对练习。** 对照 [2024 Q1(1)](../Midterm2024withSolutions%281%29.pdf#page=1) 做概念判断；做 [[Midterm Practice and Answers]] 第 1–2 题，自己解释每个错误选项。周期 20 ns、高电平 5 ns 时，先算 $f=50\,\mathrm{MHz}$，再算 $D_H=25\%$。

**样卷较少展开，仍要覆盖：** 抽象、层次和模块化，常用 IC 与组合/时序模块的作用。详细阅读 [[Digital Foundations and Waveforms]]。

## Ch2 · Number Representation and Coding · 数值表示与编码

### 重点 1：进制、补码与位宽

二进制/八进制/十六进制互转先按 3/4 位分组；其他进制使用位权。$n$ 位补码范围为 $[-2^{n-1},2^{n-1}-1]$；无符号范围为 $[0,2^n-1]$。减法用 $A+\bar B+1$，按题意保留固定位宽。加法中**同号相加、结果异号**才是有符号溢出；额外进位不能代替符号或溢出判断。

**解题步骤。** 写清位宽与编码 → 分别解码估计结果 → 执行二进制运算并保留指定位 → 判断符号与溢出 → 十进制反算。示例：6 位 `010001 + 011001` 为 17+25=42，保留结果 `101010` 表示 −22，故发生有符号溢出；这正是 [2025 秋 Q3(2)](../Midterm2025-fall%281%29.pdf#page=3) 的类型。

**针对练习。** [2024 Q3](../Midterm2024withSolutions%281%29.pdf#page=3) 加减乘除；[2026 Q2–3](../Midterm2026%20%281%29.pdf#page=2) 定宽减法和溢出；[[Midterm Practice and Answers]] 第 3–7 题。特别注意最小补码求相反数、$-128/(-1)$ 的同宽溢出，以及乘法完整乘积需要足够位宽。阅读 [[Binary Arithmetic and Signed Representation]]、[[Number Systems and Base Conversion]]。

### 重点 2：定点与浮点

本课 $Q a.b$ 的 $a$ 含符号位；总宽 $a+b$，补码整数值为 $I$ 时真实值为 $x=I2^{-b}$，步长 $2^{-b}$。先乘 $2^b$ 得整数码，再编码并检查范围。例：$-12.25$ 的 Q5.2 码 $I=-49$，七位补码是 `1001111`；对照 [2026 Q2(3)](../Midterm2026%20%281%29.pdf#page=2)。

IEEE 754 binary32 先分符号位 $s$、指数 E、23 位小数 F；正规数 $x=(-1)^s(1+F/2^{23})2^{E-127}$，只适用于 $1\le E\le254$。E=0 或 255 要分别检查零/次正规、无穷/NaN，不能套隐含 1。自定义格式先按题目给定的字段宽度与 bias 解码，而不是自动照搬 binary32。练 [2025 春 Q8](../Midterm2025-spring%281%29.pdf#page=10)，再做自测 8–9；阅读 [[Fixed-Point and Floating-Point Numbers]]。

### 重点 3：BCD、Gray、奇偶与 CRC

- **BCD：** 每个十进制数字单独用 4 位；相加所得某一位超过 9 或有进位时加 `0110` 修正。练 [2025 秋 Q2(2)](../Midterm2025-fall%281%29.pdf#page=2)。
- **Gray：** 二进制转 Gray 保留最高位，其他位为相邻二进制位 XOR；逆向从高位累积 XOR。练 [2024 Q2(2)](../Midterm2024withSolutions%281%29.pdf#page=2)。
- **Parity：** 偶校验位 $p=d_0\oplus\cdots\oplus d_{n-1}$；接收组（包括校验位）异或为 1 表示偶校验不通过。生成器与检查器输入数目不同，不能把两张真值表混在一起。练 [2025 秋 Q6](../Midterm2025-fall%281%29.pdf#page=6)。
- **CRC：** 生成码长度为 $r+1$、次数为 $r$ 时，数据补 $r$ 个零后做模 2 长除，余数补足 $r$ 位并接在数据之后；模 2 减法就是 XOR。练 [2025 春 Q3](../Midterm2025-spring%281%29.pdf#page=3)、[2026 Q2(4)](../Midterm2026%20%281%29.pdf#page=2)。题面若指定不同补零/帧格式，按题面处理。

**闭卷过关：** 能独立做一题进制、小数和补码溢出，再做 BCD/Gray/奇偶/CRC 各一题；每题以逆变换、位权或除尽检查。专题 [[Data Coding and Character Representation]]、[[Parity and Cyclic Redundancy Checks]]，自测 10–13。

## Ch3 · Logic Gates and Electrical Interfaces · 逻辑门与电平接口

**重点。** 熟练转换 NOT、AND、OR、NAND、NOR、XOR、XNOR 的真值表、表达式、符号和波形；二输入 XOR 为“不同”，多输入 XOR 为输入中 1 的个数为奇数。逐时间区间计算门的输出，再计算后级，标注题目是否忽略传播延迟。

**难点。** NAND/NOR 输出有反相；多输入 XOR 不是“所有输入都不同”。电平题不能只看名义电源：发送端的 $V_{OH(min)}$、$V_{OL(max)}$ 与接收端的 $V_{IH(min)}$、$V_{IL(max)}$ 各自有不同含义。高、低噪声容限分别为

$$NM_H=V_{OH(min)}-V_{IH(min)},\qquad NM_L=V_{IL(max)}-V_{OL(max)}.$$

这些是给定发送端和接收端之间的静态保证差值；交换器件方向须重新计算。若输入落在未保证区，不能断言一定读成 0 或 1。

**针对练习。** [2024 Q5](../Midterm2024withSolutions%281%29.pdf#page=5)、[2026 Q5](../Midterm2026%20%281%29.pdf#page=6) 逐门画波形；自测 14–15。四份样卷未集中考察噪声容限计算，但它在课程笔记/课件主线上，仍应补练。阅读 [[Logic Gates and Boolean Functions]]、[[Logic Levels and Noise Margins]]。

## Ch4 · Boolean Algebra and Karnaugh Maps · 布尔代数与卡诺图

**重点。** 布尔定律、德摩根律；最小项 (minterm) 与最大项 (maxterm)；标准积之和 (canonical SOP) 与标准和之积 (canonical POS)；卡诺图 (Karnaugh map, K-map) 的 1/0/X 分组。

**难点 1：标准式与最简式。** 先写变量顺序；标准 SOP 从输出为 1 的行写 minterm，某位为 1 用原变量、0 用反变量；标准 POS 从输出为 0 的行写 maxterm，某位为 0 用原变量、1 用反变量。标准式的每一项都含全部变量；最简式通常不是标准式。练 [2024 Q4](../Midterm2024withSolutions%281%29.pdf#page=4)、[2025 春 Q4](../Midterm2025-spring%281%29.pdf#page=4)、[2025 秋 Q3](../Midterm2025-fall%281%29.pdf#page=3)。

**难点 2：正确圈图。** 横纵轴按 Gray 顺序 00、01、11、10；只圈 $2^k$ 个相邻格，可跨边界和重叠，不可对角相邻。求 SOP 圈 1；求 POS 圈 0。X 可取最有利的值，但不是必须覆盖的 1。无效 BCD 码是否是 X 由规格决定：不能在题目要求无效输入输出 0 时擅自把它们当 X。

**针对练习。** 先做自测 17–20，再做 [2024 Q6、Q8](../Midterm2024withSolutions%281%29.pdf#page=7) 和 [2026 Q4](../Midterm2026%20%281%29.pdf#page=4)。自测标准：用全部指定输入逐行验证所得式，确认要求的是 standard 还是 minimum。阅读 [[Boolean Forms and Algebraic Simplification]]、[[Karnaugh Map Minimization]]。

## Ch5 · Combinational Logic Design · 组合逻辑分析与设计

**重点。** 电路分析：给中间节点命名 → 按门逐级写表达式 → 化简 → 结合输入波形核验。电路设计：文字需求 → 输入/输出及极性 → 完整真值表 → 化简 → 按允许门型实现 → 核验。

**难点 1：文字规范。** exactly 2 只包括恰好两个有效；至少 2 还包括 3、4 个有效。并行四位中检测连续 `110` 可检查 ABC 与 BCD 两个窗口；对稳定并行输入这是组合逻辑，若输入依次串行到来则需要另行考虑状态。练 [2025 春 Q6](../Midterm2025-spring%281%29.pdf#page=6)、[2025 秋 Q4/Q8](../Midterm2025-fall%281%29.pdf#page=4)。

**难点 2：仅用 NAND/NOR。** SOP 常用 NAND-NAND，POS 常用 NOR-NOR；反变量若题目没有提供，必须用自接输入的 NAND/NOR 反相器产生。德摩根变换要保留括号和每个反相范围。检查门输入个数和只允许的器件。练 [2025 春 Q5](../Midterm2025-spring%281%29.pdf#page=5)、[2025 秋 Q6](../Midterm2025-fall%281%29.pdf#page=6) 与自测 21–24。

**针对练习：2025 秋 Q8。** 令 A、B、C=1 表示故障。黄灯 $Z_1=1$ 对应恰好 1 个或 3 个故障，故 $Z_1=A\oplus B\oplus C$；红灯 $Z_2=1$ 对应恰好 2 个或 3 个，故 $Z_2=AB+AC+BC$。标准 POS 分别从零行 $\Pi M(0,3,5,6)$ 和 $\Pi M(0,1,2,4)$ 写出。74HC138 若已正确使能，且 $L_i$ 为第 i 路低有效输出，则 $Z_1=\overline{L_1L_2L_4L_7}$，$Z_2=\overline{L_3L_5L_6L_7}$；芯片的输入位序、使能和允许门型仍以题图为准。

**波形/故障。** 先做无故障电路，再将固定故障代入原节点；若要检测故障，输入应使故障被激活且差异传播到输出。阅读 [[Combinational Logic Analysis and Design]]、[[Universal Gates and Bubble Pushing]]、[[Digital Logic Troubleshooting]]。

## Ch6 · Combinational Building Blocks and Timing · 功能块与时间行为

### 加法器、乘法器与比较器

半加器：$S=A\oplus B$、$C=AB$；全加器：$S=A\oplus B\oplus C_{in}$、$C_{out}=AB+AC_{in}+BC_{in}$。两个 HA 加一个 OR 能构成 FA；同权重输入相加后 sum 保持该权、carry 进入高一权重。74HC283 扩成 8 位时，低位块 carry-out 接高位块 carry-in，并明确最低位输入进位。练 [2026 Q6](../Midterm2026%20%281%29.pdf#page=7)、自测 25。

本课 CLA 采用 $G_i=A_iB_i$、$P_i=A_i+B_i$，$C_{i+1}=G_i+P_iC_i$；和位仍是 $A_i\oplus B_i\oplus C_i$，不要将 OR 传播量当成 XOR 传播量。练 [2024 Q7](../Midterm2024withSolutions%281%29.pdf#page=10)、自测 26。部分积与 carry 以列权排列，FA 的不用输入可按题意接 0；[2025 春 Q7](../Midterm2025-spring%281%29.pdf#page=8) 的具体关键路径取决于所画结构，不能把参考解答 8.1t 当所有乘法器的通用值。

比较器先判是否 signed；无符号数从最高不同位决定大小，级联时低位结果送高位块，最低块初始 EQ=1、GT=LT=0。自测 27；阅读 [[Binary Arithmetic Circuits]]、[[Comparison Decoding and Selection]]。

### MUX 与 decoder 的电路实现

**MUX 解题四步：** ① 确定选择端顺序及高低位；② 每组固定选择位，在真值表中读余下变量两种取值的输出；③ 将数据端写为 0、1、变量或反变量；④ 检查使能及正/反相输出。对于 [2026 Q7](../Midterm2026%20%281%29.pdf#page=9) 的原真值表，若以 ABC 为选择位（A 为最高位）、D 为剩余变量，数据端 $I_0\ldots I_7$ 为 **D、$\bar D$、1、1、0、0、1、0**；选择位若重新分配，答案也会改变。以原题图核对芯片引脚及有效极性。另练 [2024 Q6](../Midterm2024withSolutions%281%29.pdf#page=7)、[2025 秋 Q7](../Midterm2025-fall%281%29.pdf#page=7)、自测 29。

**Decoder：** 先判断使能与输出极性。高有效输出是所选 minterm，可用 OR 合成；低有效输出是对应 minterm 的反，可用 NAND 合成。优先编码器同时有多路请求时必须按优先级选择。练 [2025 春 Q6](../Midterm2025-spring%281%29.pdf#page=6)、[2025 秋 Q8](../Midterm2025-fall%281%29.pdf#page=8)、自测 28。

### 七段显示、三态和时序

**七段显示：** 先写每个数字哪些段点亮，再转换为芯片输出电平。共阳、低有效输出时 LOW 点亮；[2026 Q4](../Midterm2026%20%281%29.pdf#page=4) 的 g 段对合法 BCD 数字 0、1、7 输出 1，其余合法数字输出 0。原题解将非法码 10–15 当 X；按此约定可得 $g=\bar A\bar B\bar C+BCD$。若无效输入另有要求，不可继续使用该化简。灯测试、逐级消隐的优先关系按器件表；阅读 [[Seven-Segment Display and Code Conversion]]。

**DEMUX 与时序：** [2026 Q8](../Midterm2026%20%281%29.pdf#page=12) 先写 `1357` 的 BCD，各十进制位先发最低位数字 7、每位内部 LSB 先发；再逐时刻依据选择线、数据输入和使能判各低有效输出。输出 $Z$ 是高阻，不是 0；共享总线应至多一个驱动有效。阅读 [[Tri-State Buffers and Bus Drivers]]。

**延迟与冒险：** 按题目给出的门级模型，沿每条相关可激活路径求门延迟之和；$t_{pd}$ 取最大、$t_{cd}$ 取最小。别把所有支路的门统统相加。练 [2025 秋 Q5](../Midterm2025-fall%281%29.pdf#page=5) 和自测 31；对静态 1 冒险，从相邻 1 覆盖与共识项入手，练自测 32。阅读 [[Propagation Delay and Logic Hazards]]。

## Targeted plan · 针对性复习安排

1. **第一轮：补码和布尔基础。** 做 2026 Q2–3、2025 秋 Q2–3、2024 Q4；每题记录位宽、溢出、变量顺序、标准/最简。
2. **第二轮：组合实现。** 做 2025 春 Q5–6、2025 秋 Q6–8、2026 Q4/Q7；画真值表、标极性、按题意连接器件。2025 秋卷未附解答，可用本篇 Q8 的独立结果与原理核对。
3. **第三轮：时序与综合。** 做 2024 Q5/Q7、2025 秋 Q5、2026 Q5/Q6/Q8；补做春季 Q7–8 的乘法器/浮点。解释关键路径与每项假设。
4. **限时模拟。** 四份卷面均标 90 分钟、8 题；可用 2025 秋卷先做一轮，之后查错。样卷自身的作答要求可参考，实际考试规则以课程最新公告为准。

**最终自测：** 闭卷写出补码范围与溢出条件；用真值表写 SOP/POS、K-map 化简；用 NAND 和 MUX/decoder 实现；解释加法器进位、段输出极性和最慢/最快路径。把错题归为“定义、计算、位序/极性、题目条件”，隔天不看答案重做。

## Sources · 来源与边界

- 样卷：[2024 年 3 月](../Midterm2024withSolutions%281%29.pdf)、[2025 年春季](../Midterm2025-spring%281%29.pdf)、[2025 年秋季](../Midterm2025-fall%281%29.pdf)、[2026 年 3 月](../Midterm2026%20%281%29.pdf)。题号与 PDF 页序标在各题链接；2025 秋文件未附答案，本篇 Q8 的公式为独立推导。
- 课程原理、章节范围及课件更正见 [[Midterm Review Guide]]；逐章大纲见 [[Midterm Knowledge Outline]]；公式及适用前提见 [[Midterm Formula Sheet]]；对应自测见 [[Midterm Practice and Answers]]。
- Ch7–11 的详细状态机、时序与存储器设计不纳入已确认的本次复习范围；Ch1 的相关模块只需理解基础功能。历史卷不能证明本次考试必考或排除其他 Ch1–6 知识。

---
索引：[[ECE2050.1]] · [[Glossary]]
