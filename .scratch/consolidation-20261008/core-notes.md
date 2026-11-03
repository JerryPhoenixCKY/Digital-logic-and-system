@@@ Digital Foundations and Waveforms
> [!SUMMARY] Quick recall · 英文速览
> Digital systems interpret continuous voltages as discrete symbols. Correct function, valid voltage levels, and valid sampling time are three separate requirements.

## 1 · Digital Abstraction and System Design · 从电压到信息

数字抽象 (digital abstraction) 把一段允许的电压解释为逻辑 0/1；导线电压本身仍连续变化。先确定“信息是什么意思”，再选择表示它的位宽、电平极性和采样方式。正逻辑 (positive logic) 与低有效控制 (active-low control) 可以同时存在。

> [!IMPORTANT] 三层正确性
> 真值表保证功能；阈值与噪声容限保证电气接口；建立／保持约束保证采样。任何一层不满足，都不能由另外两层替代。

## 2 · Digital Waveforms · 再把时间加入模型

周期 $T$ 是相邻同类边沿之间的时间，高电平脉宽为 $t_H$，频率 $f$ 和占空比 $D$ 为：

$$f=1/T,\qquad D=(t_H/T)\times100\%.$$

T、$t_H$ 单位为 s，f 单位 Hz；上升／下降时间描述边沿过渡，传播延迟描述输入到输出的响应，两者都不等于脉宽。10%–90% 等测量约定不等于逻辑门的输入阈值。

**例。** $T=20\rm\,ms,t_H=5\rm\,ms$，故 $f=50\rm\,Hz,D=25\%$。10 MHz 时周期为 100 ns；30 ns 高电平对应 30% 占空比。

## 3 · 从模块到系统：先数据、后控制

层次化 (hierarchy) 隐藏细节；模块化 (modularity) 固定接口；规则性 (regularity) 复用结构。数据通路 (datapath) 处理计数和比较，控制器 (controller) 根据状态决定装载、停止、清零。

以装瓶到 12 粒为例，保存 0–12 需 $\lceil\log_2 13\rceil=4$ 位；比较器判断 count=12，状态机再关闭阀门。一个持续三个周期的高电平不能自动算成三次独立事件，输入接口必须规定“一次事件”的含义。

## 4 · 波形分析：组合区间与时序边沿

把全部输入变化时刻作为分界；每个稳定区间按布尔函数求组合输出。遇到存储元件，只在规定的有效边沿或透明电平更新状态；异步复位另按优先级处理。先忽略延迟建立逻辑轨迹，再加入题目给出的延迟。

## 5 · 重点回忆与下一步

- 电平、逻辑值和“控制已有效”是三个不同概念。
- 频率取完整周期的倒数，脉宽用于占空比。
- 先学 [[Number Systems and Base Conversion]] 与 [[Logic Gates and Boolean Functions]]，再进入组合电路和时序电路。

@@@ Number Systems and Base Conversion
> [!SUMMARY] Quick recall · 英文速览
> A radix defines digits and positional weights. Conversion preserves numerical value; an unlabelled bit pattern does not define its own interpretation.

## 1 · Number Systems · 位权是共同模型

数制 (number system) 由基数 R、数码与位权决定：

$$x=\sum_{i=-m}^{n}a_iR^i,\qquad R\ge2,\quad0\le a_i<R.$$

数码 $a_i$ 和 R 无量纲，i 为位置；小数点右边使用负次幂。先辨认进制与表示约定，再计算数值。没有上下文的 `1011` 不能自动判定为二进制。

## 2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释

| 进制 | 数码 | 一位对应二进制位数 | 典型用途 |
|---|---|---|---|
| Decimal Number System · 十进制 | 0–9 | 无固定对应 | 人类数量 |
| Binary Number System · 二进制 | 0、1 | 1 | 逻辑与存储 |
| Octal Number System · 八进制 | 0–7 | 3 | 三位成组 |
| Hexadecimal Number System · 十六进制 | 0–9、A–F | 4 | 地址与位掩码 |

例如 $(10.101)_2=2+1/2+1/8=2.625$，$(568.23)_{10}=5\cdot10^2+6\cdot10+8+2/10+3/100$。数值与它的写法要分开。

## 3 · Number Base Conversion · 整数、小数与分组

任意进制转十进制按位权展开；十进制整数转 R 进制反复除 R，余数**从最后到最先**读取。小数部分反复乘 R，整数部分**按产生顺序**读取。

八／十六进制与二进制互转，从小数点向两侧分别按 3／4 位分组；整数侧向左补 0，小数侧向右补 0。不能跨小数点混组。

> [!IMPORTANT] 精确性边界
> 一个约分后的分数能否在基数 R 中有限表示，取决于分母是否整除某个 $R^k$。二进制中分母只能含因子 2；$1/3$ 与 $1/10$ 都无限循环，截断后的表示是近似值。

## 4 · Bits and Bytes · 位宽与容量

N 位有 $2^N$ 种模式，N 位无符号整数范围 $0\ldots2^N-1$；表示 M 种状态至少需要 $\lceil\log_2M\rceil$ 位。一个 byte 是 8 bit，一个 nibble 是 4 bit。

容量 = 深度（word 数）× 位宽（bit/word）。地址数、bit 数、byte 数需分别说明。SI 的 k/M 与二进制 Ki/Mi 分开计算，不能默认为相同倍率。

## 5 · 典型校验与下一步

转换后用原进制的位权展开复核；16 进制一位对应四个 bit，不改变数值也不等于四字节。掌握位宽后进入 [[Binary Arithmetic and Signed Representation]]；编码规则另见 [[Data Coding and Character Representation]]。

@@@ Binary Arithmetic and Signed Representation
> [!SUMMARY] Quick recall · 英文速览
> Arithmetic uses positional weights. Fixed width determines which bits are retained; signed representation determines what those bits mean.

## 1 · Binary Arithmetic · 先看无符号运算

二进制算术 (binary arithmetic) 使用进位、借位和位权。$1+1=10_2$；乘法是部分积移位相加；除法满足 $a=bq+r$。N 位运算保留低 N 位时按模 $2^N$ 回绕；进位必须与被保留的结果分开记录。

## 2 · Sign-Magnitude Representation · 符号不能直接参与加法

原码 (sign-magnitude representation) 用最高位 s 表示符号，其余位形成幅值 M：$x=(-1)^sM$。N 位范围为 $\pm(2^{N-1}-1)$，存在 +0、−0。不同符号相加要比较幅值；将整个位串直接无符号相加通常不成立。

## 3 · Two's Complement Representation · 负权建立统一加法

补码 (two's complement) 的最高位是负权：

$$x=-b_{N-1}2^{N-1}+\sum_{i=0}^{N-2}b_i2^i.$$

范围 $-2^{N-1}\ldots2^{N-1}-1$。求相反数是在固定位宽内取反加 1；扩展到更多位时复制符号位。最小负数的正数超出原位宽范围，不能按一般例子处理。

> [!IMPORTANT] Carry 与 Overflow 分别检查
> 无符号加法看最高位进位；补码加法看“同号相加却变号”。两者判断的问题不同。减法先写 $A-B=A+\bar B+1$，再按题目约定解释进位／借位。

**例。** 四位 `0111+0001=1000`：无符号 7+1=8 未溢出，但补码范围最大为 7，因此有符号溢出。`1111+0001=0000` 有进位，却表示补码 −1+1=0，无有符号溢出。

## 4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确

N 位乘 N 位的完整乘积一般需 2N 位；移位前确定符号扩展和部分积宽度。带符号除法还需声明向零截断等商约定，使余数满足 $a=bq+r$；除数不能为 0。算术右移复制符号，逻辑右移补 0。

## 5 · 解题与实现的连接

先写数学结果和允许范围，再编码、运算、解码复核。位串相同不代表 signed / unsigned 数值相同。门级加减乘结构见 [[Binary Arithmetic Circuits]]；小数的缩放另见 [[Fixed-Point and Floating-Point Numbers]]。

@@@ Fixed-Point and Floating-Point Numbers
> [!SUMMARY] Quick recall · 英文速览
> Fixed point applies a fixed scale to an integer. Floating point stores a sign, exponent, and fraction; its range and precision are different properties.

## 1 · Fixed-Point Numbers · 把整数乘以固定尺度

定点数 (fixed-point number) 若整数代码为 n、小数位数为 b，则 $x=n2^{-b}$，分辨率 $\Delta=2^{-b}$。n 的有符号／无符号解释仍由 [[Binary Arithmetic and Signed Representation]] 决定。

总宽 N 的无符号范围 $0\ldots(2^N-1)2^{-b}$；补码范围 $-2^{N-1-b}\ldots(2^{N-1}-1)2^{-b}$。Q 格式的名称有不同约定，必须声明整数位是否包含符号位。

**例。** U4.4 中 `1010 1000` 对应整数 168，数值 $168/16=10.5$。增加小数位改善分辨率，但固定总宽下会缩小范围。

## 2 · 定点运算：先对齐，再舍入

加减法先对齐二进制小数点；乘法结果小数位数相加，输出截断／舍入前检查中间宽度。回绕 (wrap-around) 与饱和 (saturation) 是不同溢出策略，应由规范选择。

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

## 4 · 编码例与精度边界

$10.5=(1010.1)_2=(1.0101)_2\times2^3$，因此 s=0、E=130、F 的前四位为 0101，单精度模式为 `0x41280000`。指数增加，绝对间距也增加；扩大动态范围不等于所有数都更精确。

> [!IMPORTANT] 格式先于数值
> 相同位串可代表不同定点尺度或不同浮点格式。自定义 16 位格式必须重新给出字段长度、偏置和特殊码规则，不能直接套用单精度公式。

## 5 · 重点回忆

定点：范围、分辨率、缩放和中间宽度。浮点：规格化、偏置、隐含位、特殊码与舍入。有限表示误差是表示法的问题，不能只靠增加算术模块消除。

@@@ Data Coding and Character Representation
> [!SUMMARY] Quick recall · 英文速览
> A code assigns bit patterns to meanings. BCD preserves decimal digits, Gray code preserves one-bit adjacency, and ASCII assigns codes to characters.

## 1 · 编码与数制：先决定位串的含义

数据编码 (data coding) 不是简单换进制。一个位串表示数值、逐个十进制数字或字符，需要不同的解释器；合法输入集合也随编码改变。

## 2 · Binary Coded Decimal · 十进制数字逐位编码

8421 BCD 用每四位表示一个十进制数字；0000–1001 合法，1010–1111 非法。十进制 14 编码为 `0001 0100`，而纯二进制 14 为 `1110`。

BCD 加法的每个数字先二进制相加；若和大于 9 或产生四位进位，则加 0110 校正。原因是 16 个二进制码中只使用 10 个，十进制进位需跳过 6 个码。

## 3 · Gray Code · 相邻变化约束

格雷码 (Gray code) 的相邻码字仅一位变化。二进制位 $b_{n-1}\ldots b_0$ 转为格雷位：

$$g_{n-1}=b_{n-1},\quad g_i=b_{i+1}\oplus b_i;\qquad b_i=\bigoplus_{j=i}^{n-1}g_j.$$

也可写 $g=b\oplus(b\gg1)$。例如二进制 1011 得格雷码 1110。格雷码不按通常二进制位权直接相加；单比特相邻性也不保证任意异步多位传输安全。

## 4 · American Standard Code for Information Interchange · 字符编码

ASCII 为七位字符编码：字符 `'0'` 是 0x30，字符 `'A'` 是 0x41；数值 0 与字符 `'0'` 不相同。数字字符减去 `'0'` 才得到数值 0–9，前提是先确认字符处于 `'0'`–`'9'`。

基本 ASCII 范围为 0–127，装进八位字节时高位可为 0；把高位用于奇偶校验或扩展编码时，必须明确协议。Unicode 的字符与 UTF-8 的字节数不能混为一谈。

## 5 · 重点与应用

| 目的 | 选择 | 易错点 |
|---|---|---|
| 十进制显示与逐位计算 | BCD | 把整串当纯二进制 |
| 位置变化或相邻编码 | Gray | 把相邻性当作纠错能力 |
| 文本接口 | ASCII / specified encoding | 把字符与数值混用 |

显示应用见 [[Seven-Segment Display and Code Conversion]]；错误检测见 [[Parity and Cyclic Redundancy Checks]]。

@@@ Parity and Cyclic Redundancy Checks
> [!SUMMARY] Quick recall · 英文速览
> Parity checks the number of flipped bits modulo two. CRC checks polynomial divisibility; its guarantees depend on the generator and frame length.

## 1 · Parity Bit · 用一个约束建立检错

数据位 $d_i$ 与校验位 P 均为 0/1。偶校验位为 $P=\bigoplus d_i$；奇校验位为它的补。收到的整组异或为 S：偶校验要求 S=0，奇校验要求 S=1。

> [!IMPORTANT] XOR 的两种用途
> XOR 输出 1 表示数据中有奇数个 1；把这个结果作为新增位，完整码字就有偶数个 1。生成偶校验位用 XOR，生成奇校验位用其补，不能把生成器与检查器混称。

## 2 · 门级发生器、检查器与错误边界

四位数据的平衡树：$P=(A_0\oplus A_1)\oplus(A_2\oplus A_3)$，三个二输入 XOR、两级逻辑。接收端将收到的四数据位 $r_i$ 和收到的校验位 $p_r$ 全部异或得到检错输出 E，需要四个二输入 XOR。

偶校验字 10100 单比特翻转成 00100 时 E=1；两比特翻转成 01100 时 E=0。相对合法字，所有奇数次翻转检出，所有非零偶数次翻转漏检；E=0 只表示未检出错误，不证明数据正确。

## 3 · Cyclic Redundancy Check · 改用多项式余数

CRC 将消息位串解释为二元多项式 $M(x)$；生成式 $G(x)$ 的次数为 r。运算在 GF(2) 上，减法与加法都是 XOR，不进位。

$$R(x)=[x^rM(x)]\bmod G(x),\qquad C(x)=x^rM(x)+R(x).$$

发送端补 r 个 0 后除 G，附上 r 位余数；接收端对包含 CRC 的整组再除 G，零余数表示未检出错。错误模式 $E(x)$ 恰好是 G 的倍数时仍会漏检。

## 4 · 例题与保证必须分开

取消息 1101、生成码 1011，即 $G=x^3+x+1$：对 1101000 做模 2 除法，余数为 001，码字为 1101001；整组再除 1011 的余数为 000。

次数 r、首末系数为 1 的生成式能检测长度不超过 r 的非零突发错误。检测所有奇数重错误还要求包含因子 $x+1$；其他保证依赖生成式和帧长。抽象课内算法与真实协议的初值、反射、最终异或约定需区分。

## 5 · 选用与复习

奇偶校验成本低，不能定位错误；CRC 通过更多约束检测多类错误，也不等于自动纠错。先按规范完整计算，再用单比特和多比特反例测试检错边界。

@@@ Logic Gates and Boolean Functions
> [!SUMMARY] Quick recall · 英文速览
> A logic gate maps input bits to an output bit. Start with the truth table, then connect the algebraic expression, symbol, and waveform.

## 1 · Logic Gates · 统一的布尔模型

逻辑门 (logic gates) 在稳态下实现布尔函数，n 个输入需 $2^n$ 行真值表。所有逻辑量无量纲；$+$ 是 OR，相乘是 AND，横线是 NOT，$\oplus$ 是 XOR。物理电压的有效条件见 [[Logic Levels and Noise Margins]]。

## 2 · Inverter, AND Gate and OR Gate · 三种基本运算

| 输入 AB | NOT A | AND | OR | NAND | NOR | XOR | XNOR |
|---|---|---|---|---|---|---|---|
| 00 | 1 | 0 | 0 | 1 | 1 | 0 | 1 |
| 01 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 10 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 11 | 0 | 1 | 1 | 0 | 0 | 0 | 1 |

反相器 (inverter) 输出 $\bar A$。AND 要求所有条件同时成立，OR 表示至少一个条件成立；OR 的“或”包含两者都成立。n 输入 AND 仅全 1 时输出 1；n 输入 OR 仅全 0 时输出 0。

缓冲器 (buffer / BUF) 为 $Y=A$，保留逻辑值，可承担驱动或接口功能。正逻辑用较高电压表示 1；控制的 active-high／active-low 则说明哪种电平断言事件，必须结合规范解释。

## 3 · NAND Gate and NOR Gate · 输出取补与气泡

NAND 为 $\overline{AB}$，NOR 为 $\overline{A+B}$。输出气泡表示对整个门函数取反；输入气泡只反相对应输入。

$$\overline{AB}=\bar A+\bar B,\qquad\overline{A+B}=\bar A\bar B.$$

因此 NAND 的等价符号是 negative-OR，NOR 的是 negative-AND。通用性与多级气泡推移集中见 [[Universal Gates and Bubble Pushing]]。

## 4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性

$$A\oplus B=A\bar B+\bar AB,\qquad\overline{A\oplus B}=AB+\bar A\bar B.$$

两输入 XOR 检测不同，XNOR 检测相同。多输入 XOR 检测奇数个 1，其整体补检测偶数个 1；它们并不检测“所有输入相同”。多个二输入 XNOR 串联不能直接替代“XOR 全部输入后取一次补”。

> [!IMPORTANT] XOR 不统计“至少一个”
> $1+1=1$ 是布尔 OR；$1\oplus1=0$ 是异或；算术 $1+1=10_2$ 则包含进位。半加器需要 XOR 给和位、AND 给进位。

## 5 · 从真值表到波形与应用

在每个输入稳定区间查表，传播延迟只移动响应边沿。AND 用于许可与门控；OR 合并事件；XOR 用于受控反相、奇偶校验；XNOR 后再 AND 可比较整个字。静态功能正确后，还应检查毛刺与采样时序。

@@@ Logic Levels and Noise Margins
> [!SUMMARY] Quick recall · 英文速览
> Output guarantees and input acceptance limits define compatibility. Noise margin is the difference between those limits, not the nominal supply voltage.

## 1 · Logic Levels · 保证值与接受范围

逻辑电平 (logic levels) 把模拟电压分为有效 LOW、有效 HIGH 与不确定区。输入阈值为 $V_{IL(max)},V_{IH(min)}$；输出保证为 $V_{OL(max)},V_{OH(min)}$，单位均为 V。

高输出必须达到接收端 HIGH 的下限，低输出必须不超过 LOW 的上限。符号中的输入／输出、最大／最小不能互换；不确定区不代表器件自动选择最近的逻辑值。

## 2 · DC Transfer Characteristic · 由传输曲线理解恢复能力

直流传输特性 (DC transfer characteristic) 是稳态 $V_{out}(V_{in})$，输入／输出轴都为 V。缓冲器与反相器方向相反；过渡区的斜率、切换点和逻辑阈值用途不同。

局部斜率 −1、切换点 $V_{out}=V_{in}$ 等是特定静态模型的定义条件；不能把某曲线读出的典型点替代数据手册保证范围，也不能由 DC 曲线推出传播延迟。

## 3 · Noise Margin · 接口的预算

$$NM_H=V_{OH(min),driver}-V_{IH(min),receiver},$$
$$NM_L=V_{IL(max),receiver}-V_{OL(max),driver}.$$

高电平向下受扰，低电平向上受扰，所以两种余量分开计算。最小余量决定较弱的一侧；正余量只是必要条件，还需核对输入额定范围、驱动电流、负载和时序。

**例。** 驱动保证 HIGH≥2.4 V、LOW≤0.4 V，接收 HIGH≥2.0 V、LOW≤0.8 V，则两侧容限均 0.4 V；不能用电源电压代替这些保证值。

## 4 · 重点与失效边界

> [!IMPORTANT] 先建立驱动—接收关系，再代公式
> 相同电源电压不保证逻辑族兼容；把典型值当最坏条件，会高估容限。悬空输入、总线冲突和阈值附近噪声应回到电气模型判断。

@@@ Boolean Algebra and Circuit Models
> [!SUMMARY] Quick recall · 英文速览
> Define a valid combinational model before manipulating equations. Boolean laws preserve a function, while composition rules constrain the physical topology.

## 1 · Combinational Circuit · 先确认可以使用的模型

组合电路 (combinational circuit) 的稳态输出只由当前输入决定。构成要求：各元件组合；每个内部／输出节点恰有一个驱动；信号依赖无环。扇出 (fan-out) 是一个输出接多个输入，不能与多个输出并接混淆。

## 2 · Boolean Equation · 从需求写函数

布尔方程 (Boolean equation) 先定义输入事件、极性、输出断言条件和变量顺序。$Y=F(\mathbf x)$ 的各分量均为 0/1；规范中的 exactly、at least、active-low 会改变函数，先列条件再选门。

## 3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则

| 规则 | OR 形式 | AND 对偶 |
|---|---|---|
| 单位与控制值 | $A+0=A,\ A+1=1$ | $A1=A,\ A0=0$ |
| 幂等 | $A+A=A$ | $AA=A$ |
| 互补 | $A+\bar A=1$ | $A\bar A=0$ |
| 吸收 | $A+AB=A$ | $A(A+B)=A$ |
| 分配 | $A(B+C)=AB+AC$ | $A+BC=(A+B)(A+C)$ |

交换、结合与双重反相同样成立。对偶 (duality) 交换 AND／OR 与 0／1，但不等于把整个函数取反；布尔加法也不是普通实数加法。

## 4 · DeMorgan's Theorems · 取补必须覆盖整个子式

$$\overline{XY}=\bar X+\bar Y,\qquad\overline{X+Y}=\bar X\bar Y.$$

移过外层横线时，对每项取补并交换运算；如 $\overline{AB+C}=(\bar A+\bar B)\bar C$。单变量上的横线不能顺便移到无关项。

## 5 · Proof by Perfect Induction · 穷举与代数验证

完全归纳／穷举证明 (proof by perfect induction) 比较 n 变量全部 $2^n$ 行。找到一行不同即可反驳等价；选几个示例一致不能证明全部。代数证明则逐步注明所用规则。

> [!IMPORTANT] 三个边界
> 对偶不等于取补；逻辑等价不等于电压／时序等价；布尔方程有解不等于任意反馈连接都满足组合构成规则。

下一步用 [[Boolean Forms and Algebraic Simplification]] 统一函数形式，再用 [[Karnaugh Map Minimization]] 减少实现代价。

@@@ Boolean Forms and Algebraic Simplification
> [!SUMMARY] Quick recall · 英文速览
> Canonical forms record truth-table rows exactly. Simplification removes unnecessary literals while preserving every specified output.

## 1 · Minterm and Maxterm · 一行对应一个项

固定变量顺序 $ABC$，行编号 $i=4A+2B+C$。最小项 (minterm) $m_i$ 仅在第 i 行为 1：取 1 的变量原写，取 0 的变量取补。最大项 (maxterm) $M_i=\bar m_i$ 仅在第 i 行为 0，文字极性相反。

例如 i=2 对应 010：$m_2=\bar AB\bar C$，$M_2=A+\bar B+C$。两种项都包含变量域中的每个变量。

## 2 · Truth Table and Boolean Expression · 用真值表定义全集

n 个变量有 $2^n$ 行。输出为 1 的 ON set、为 0 的 OFF set 和允许任意输出的 don't-care set 需分别列出；只有规范允许时才能把某行标 X。

## 3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式

标准 SOP 取 ON 行的最小项相或；标准 POS 取 OFF 行的最大项相与：

$$F=\sum_{i\in ON}m_i=\prod_{i\in OFF}M_i.$$

简化 SOP／POS 不一定每项包含全部变量。SOP 对应 AND→OR，POS 对应 OR→AND；“标准”“最小”与“门级实现最优”不是同一个条件。

## 4 · Boolean Expression Simplification · 保持函数再比较代价

典型动作是提公共因子、合并互补项和吸收冗余项：$XY+X\bar Y=X$，$X+\bar XY=X+Y$。为展开成标准 SOP，可乘 $(Z+\bar Z)=1$；标准 POS 可用 $P=(P+Z)(P+\bar Z)$ 补变量。

**例。** $AB+A\bar B=A$；而 $AB+\bar AC$ 不能随意删掉 A。每次改写先保证变量域与所有指定行不变。

## 5 · 重点与检查顺序

> [!IMPORTANT] 先固定变量顺序
> $\sum m(\cdot)$ 与 $\prod M(\cdot)$ 的索引都由同一行编号定义，但取 ON／OFF 集不同。漏变量、反写最大项极性与误用无关项是三类高频错误。

代数不易识别的合并用 [[Karnaugh Map Minimization]]；实现的级数与极性在 [[Combinational Logic Analysis and Design]] 核对。

@@@ Karnaugh Map Minimization
> [!SUMMARY] Quick recall · 英文速览
> Gray-code adjacency makes a group eliminate changing variables. Group 1s for SOP, 0s for POS, and use don't-cares only when the specification permits them.

## 1 · Karnaugh Map · 为什么相邻格能够合并

卡诺图 (Karnaugh map) 用 Gray 顺序 00、01、11、10 排列，每对相邻格只差一个变量。图的首尾边相邻，四角可成组；对角线不相邻。组为 $2^k$ 格矩形，变化的 k 个变量被消去。

## 2 · SOP 圈 1：覆盖与最小性

覆盖所有指定 1，禁止包含指定 0。优先使用最大组，允许重叠；必要时跨边连接。圈内保持 1 的变量原写，保持 0 的变量取补。不能只追求“圈数量少”而忽略文字数与必要蕴含项。

## 3 · POS Minimization with Karnaugh Map · 圈 0 读和项

圈内保持 0 的变量原写，保持 1 的变量取补，再把所得和项相与。相邻 1/0 的拓扑相同，但读出文字极性的规则相反。检查每个和项在其零圈上确为 0。

## 4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务

X 可视为 0 或 1，选择能扩大有用组的取值；无需覆盖全部 X。BCD 非法输入能否标 X，要由无效输入处理规范决定。优先电路输入端的 X 只是压缩真值表，不等于未指定输出。

## 5 · 从分组到证明：两个边界例

四变量函数 $F=\sum m(0,1,8,9,12)$，四格跨边组给 $\bar B\bar C$，两格组给 $A\bar C\bar D$，二者在 $m_8$ 重叠。结果 $F=\bar B\bar C+A\bar C\bar D$。

恰好三个输入为 1 的 $\{7,11,13,14\}$ 互不相邻，没有无关项时只能保留四个四文字最小项；不能用 XOR 替代，因为 XOR 还包含恰好一个 1。

> [!IMPORTANT] 最终检查
> 写出变量顺序、各组覆盖、消去变量和最终方程；穷举指定行验证。最小稳态方程仍可能存在逻辑冒险，见 [[Propagation Delay and Logic Hazards]]。

@@@ Combinational Logic Analysis and Design
> [!SUMMARY] Quick recall · 英文速览
> Analysis derives a function from a circuit; design implements a specification. Both meet at a complete truth table and independently verified equations.

## 1 · Combinational Logic Design · 需求先于门

规范明确输入事件、有效极性、变量顺序、输出条件和无效输入。先建立完整真值表，再写 SOP／POS、化简、选择硬件，最后比较所有指定输入。稳态变量均为无量纲 0/1。

## 2 · AND-OR and AND-OR-Invert Logic · 形式落到结构

AND-OR 计算 $AB+CD$；AOI 计算 $\overline{AB+CD}=(\bar A+\bar B)(\bar C+\bar D)$。AND→OR 的两级描述不限制门数，也通常不计输入反相器；实际门数与延迟由器件输入数、反变量是否可用决定。

## 3 · 先处理极性：储罐报警

三个传感器高电平表示过低，至少两个过低的高有效报警为 $H=AB+AC+BC$，包含 111。若 LOW 表示过低，报警为 $L=\bar A\bar B+\bar A\bar C+\bar B\bar C=\overline{AB+AC+BC}$。报警器低有效时再对 L 取补。

## 4 · 精确处理量词：四个输入中恰好三个为 1

变量顺序 ABCD，$i=8A+4B+2C+D$：

$$X=\bar ABCD+A\bar BCD+AB\bar CD+ABC\bar D=\sum m(7,11,13,14).$$

1111 与 0001 均输出 0。四个 ON 格互不相邻，所以最小两级 SOP 仍有四项。at least three 包含 1111；四输入 XOR 还包含恰好一个 1，这两个函数都不符合本题。

## 5 · Combinational Logic Analysis · 从连接恢复函数

逐节点命名，按门写方程，再向输出代入。课件 p.18：$n=\overline{\bar A\bar B\bar C}=A+B+C$，$X=nC+n+D=n+D=A+B+C+D$，关键是直通分支对 nC 的吸收。

课件 p.19：
$$X=A\bar B\bar C+AB\bar C\bar D+\bar A\bar B\bar CD+\bar A\bar B\bar C\bar D=\bar B\bar C+A\bar C\bar D.$$
原始 ON set 为 $\{0,1,8,9,12\}$；最大四格组与必要两格组可重叠。完整步骤和图示在下方对应推导中。

## 6 · 更一般的分类与匹配

同时给出的 ABCD 检测连续 110：$Y=AB\bar C+BC\bar D$，ON set 为 $\{6,12,13,14\}$。跨时钟的串行匹配需要状态，见 [[Finite State Machine Design and Applications]]。五位分类分别枚举 prime、square 和 divisible 条件；0 是平方数和 15 的倍数，却不是素数。

## 7 · 验证、实现与易错重点

> [!IMPORTANT] 原始模型必须独立保留
> 先按原连线求内部节点，再与简化式比较；只拿最终式生成真值表，会漏掉抄图错误。规范等价、门数减少和时序正确应分别检查。

NAND／NOR 实现见 [[Universal Gates and Bubble Pushing]]；优先掩码与二进制位置码见 [[Comparison Decoding and Selection]]；检错见 [[Digital Logic Troubleshooting]]。课件十道判断题放入下方复习练习。

@@@ Universal Gates and Bubble Pushing
> [!SUMMARY] Quick recall · 英文速览
> NAND and NOR are complete construction sets. DeMorgan's theorem moves complements between gate inputs and outputs while exchanging the gate body.

## 1 · 功能完备：先构成 NOT、AND、OR

通用门 (universal gate) 能仅靠自身实现任意布尔函数。定义 $N(A,B)=\overline{AB}$、$R(A,B)=\overline{A+B}$，所有量为 0/1。

| 功能 | 仅 NAND | 仅 NOR |
|---|---|---|
| NOT A | $N(A,A)$ | $R(A,A)$ |
| AND | $t=N(A,B),N(t,t)$ | $R(R(A,A),R(B,B))$ |
| OR | $N(N(A,A),N(B,B))$ | $t=R(A,B),R(t,t)$ |

无现成反变量时门数分别为 NAND：1、2、3；NOR：1、3、2。再反相一次即可构成对方的 NOR／NAND。并接输入构成 NOT，不是把两个输出短接。

## 2 · 从标准形式选择实现

SOP：$Y=P_1+P_2=\overline{\bar P_1\bar P_2}$，因此 NAND–NAND；POS：$Y=S_1S_2=\overline{\bar S_1+\bar S_2}$，因此 NOR–NOR。补输入、门输入数和共享中间节点必须计入具体门数。

## 3 · Bubble Pushing · 全部气泡同步移动

NAND 等价输入带气泡的 OR；NOR 等价输入带气泡的 AND。移动输出气泡到全部输入时交换门体；反向处理同理。仅相同信号路径上连续的两个补能抵消，分叉线路需逐支路保持解释。

## 4 · 三级门链：从输出向输入化简

$$n_1=\overline{A+B},\quad n_2=\overline{n_1C},\quad Y=\overline{n_2D}=n_1C+\bar D=\bar A\bar BC+\bar D.$$

D=0 时 Y 必为 1；D=1 时仅 ABC=001 得 1。末级 D 输入气泡没有相邻气泡抵消，不能省略。

## 5 · 重点检查

> [!IMPORTANT] 符号等价不省略物理代价
> 两次反相在布尔层面抵消，但仍可能带来延迟与负载。先核对函数，再分别统计实际门数、最大输入数和路径延迟。

@@@ Digital Logic Troubleshooting
> [!SUMMARY] Quick recall · 英文速览
> A fault test must activate the fault and propagate its effect. Detection and unique diagnosis are different goals.

## 1 · 故障模型：先解释实际电压

故障检测 (fault detection) 说明存在故障；故障定位 (fault diagnosis) 区分原因。stuck-at-0／1 将节点固定为 0／1；开路、桥接、过大延迟需要其他模型。输入悬空不自动等于 HIGH。

## 2 · 激活后再传播

正常输出 $F(\mathbf x)$ 与故障输出 $F_f(\mathbf x)$ 对同一输入比较：$D_f=F\oplus F_f$，取 1 即检出。激活时让正常节点与故障强制值相反；传播时避免旁路输入遮蔽。

AND／NAND 的旁路取 1，OR／NOR 的旁路取 0；固定的 XOR／XNOR 旁路取 0 或 1 都可，但重汇合路径可能互相抵消。

## 3 · 从函数选择有区分力的测试

$n=AB,Y=n+C$。n/0 的检测条件为 $AB\bar C$，向量 110 可检出，111 被 C 遮蔽。n/1 的检测条件为 $\bar C(\bar A+\bar B)$，000、010、100 均可。

MUX 为 $Y=\bar SD_0+SD_1$。S/0 需要 $S(D_0\oplus D_1)=1$；两路数据相同，即使选择路径错误也不能检测。先令两路相反，再切换选择。

## 4 · 从输出症状到内部测量

显示 8 变成 0 只说明 g 段未点亮，不能单凭外观区分译码、连线或发光元件故障。依次检查使能、驱动节点、段电压／电流路径；转换器位故障则选择能令该位正常输出相反值的合法输入。

## 5 · 排查与验收

先确认电源、地、时钟、复位与使能，再建立好电路模型、选择区分向量、逐节点测量。静态量用合适阈值判断，毛刺与高速故障查看波形。修正后重测失败条件及边界转换。

> [!IMPORTANT] 检出不等于唯一定位
> B/0 与 n/0 在 $Y=AB+C$ 的唯一输出上均给 $Y_f=C$；它们对所有输入不可区分，需要新增观测点。

@@@ Binary Arithmetic Circuits
> [!SUMMARY] Quick recall · 英文速览
> Build arithmetic from one-bit cells. Carry logic sets adder delay; inversion plus carry-in reuses an adder for subtraction.

## 1 · Half Adder and Full Adder · 位权守恒

半加器 (half adder) $S=A\oplus B,C=AB$，满足算术 $A+B=2C+S$。全加器 (full adder) 加入 $C_{in}$：

$$S=A\oplus B\oplus C_{in},\qquad C_{out}=AB+AC_{in}+BC_{in}.$$

这里布尔输出均为 0/1；守恒式的加号是整数加法。两半加器加一个 OR 可构成全加器。

## 2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径

串行进位 (ripple carry) 逐位传递。定义 $G_i=A_iB_i$、$P_i=A_i\oplus B_i$，则 $C_{i+1}=G_i+P_iC_i$。展开得 $C_2=G_1+P_1G_0+P_1P_0C_0$；更多位同理。

超前进位 (carry look-ahead) 并行生成展开条件，用更多门和负载换较少级数。若采用 OR 传播定义，须明确方程约定；和位仍使用 XOR。RCA 估算按完整进位链，不能只算一级全加器。

## 3 · Binary Subtractors and Adder-Subtractors · 共用数据通路

半减法器 $D=A\oplus B,B_{out}=\bar AB$。全减法器加入借位输入：$D=A\oplus B\oplus B_{in}$，$B_{out}=\bar AB+\overline{A\oplus B}B_{in}$。

模式 M=0 加法、M=1 减法：每位 $B'_i=B_i\oplus M$，最低进位 $C_0=M$，因此 $A+B'+M$。unsigned subtraction 的进位／无借位解释与 signed overflow 分开。

## 4 · Combinational Multiplier · 从部分积到列加法

n×m 无符号乘法有 $p_{ij}=a_ib_j$，位权 $2^{i+j}$，完整结果宽 n+m。逐列用半／全加器加权相加；三位乘三位需六位结果。若是补码，须处理符号扩展或专门的有符号部分积结构。

> [!IMPORTANT] 验证顺序
> 对小位宽穷举并按整数守恒核对；再检查最高位、进位、借位、溢出和路径时延。算对低位不能证明完整乘积正确。

@@@ Comparison Decoding and Selection
> [!SUMMARY] Quick recall · 英文速览
> Compare values, decode codes into lines, select one winning request, then route data. Codes, winner masks, and active polarity are different interfaces.

## 1 · Magnitude Comparator · 最高不同位决定大小

数值比较器 (magnitude comparator) 对声明为 unsigned 的字从最高位向下比较。相等信号 $E=\prod_i\overline{A_i\oplus B_i}$；较大条件是在某位 $A_i\bar B_i$ 成立且更高位全相等。signed 比较先考虑符号，不能直接沿用无符号位权。

## 2 · Decoder · 代码变线路

n-to-$2^n$ 译码器 (decoder) 为每种输入生成一个最小项。高有效输出 OR ON 行；低有效输出需按德摩根选择末级门。使能 (enable) 决定输出是否参与，扩展时高地址位选择芯片，低地址位送各片。

## 3 · Encoder and Priority Encoder · 线路变代码

普通编码器假设至多一条请求有效。优先编码器选最高优先请求，四路输入 $D_3>D_2>D_1>D_0$ 的获胜掩码：

$$W_3=D_3,\ W_2=\bar D_3D_2,\ W_1=\bar D_3\bar D_2D_1,\ W_0=\bar D_3\bar D_2\bar D_1D_0.$$

二位位置码为 $Y_1=D_3+D_2,Y_0=D_3+\bar D_2D_1$，有效指示 $V=\sum_iD_i$。输入 0110 给掩码 0100、代码 10；0000 和 0001 的代码都可为 00，必须用 V 区分。

> [!IMPORTANT] X 的含义
> 1XXX 表示低优先输入任意变化仍给同一获胜输出；所有输入组合的输出仍已指定，不是可随便化简的输出无关项。

## 4 · Multiplexer and Demultiplexer · 选择与分配

2:1 MUX 为 $Y=\bar SD_0+SD_1$，是香农展开 (Shannon expansion) $F=\bar SF|_{S=0}+SF|_{S=1}$ 的硬件。DEMUX 把一个数据输入按选择送至一条线路，其他线路输出由有效极性规定。

实现布尔函数时，选部分变量作为选择端，逐组计算剩余变量的余因子 (cofactor)；数据端可能为 0、1、变量或其补，不能只填最终表达式的某个系数。

## 5 · 模块边界与测试

先规定输入编码、优先级和全部有效极性，再列完整真值表。测试重叠请求、无请求、使能关闭和相反数据；只测试 one-hot 输入会漏掉优先级错误。

@@@ Seven-Segment Display and Code Conversion
> [!SUMMARY] Quick recall · 英文速览
> Segment truth tables describe lit shapes; electrical polarity maps those commands to levels. BCD-to-binary conversion preserves the decimal value.

## 1 · 字形先于电平

七段显示 (seven-segment display) 先以 a–g 是否亮定义字形，再按共阳／共阴映射驱动极性。定义 BCD 位序、非法码行为与小数点是否独立；同一个字形表的高低有效电平表可能互补。

位置约定：a 为上横，b／c 为右上／右下，d 为下横，e／f 为左下／左上，g 为中横；小数点 dp 独立控制。每段需按电压与目标电流限流，共同端驱动还要承受所有亮段的总电流。新增晶体管可能再次反相，须沿真实电流路径判断驱动极性。

## 2 · 字形表到组合逻辑

每段是独立布尔输出，按对应 ON／OFF 行化简。无效 BCD 输入只有规范允许时才能作为 X。显示 8 应点亮七段，显示 0 应关闭 g 段，这两个输入有助于定位 g 的故障。

## 3 · Blanking and Zero Suppression · 控制输出可见性

消隐 (blanking) 强制关闭显示；零抑制 (zero suppression) 隐藏前导零，却需保留数值中间的零。BI、RBI、RBO 等信号的极性与优先级须按给定器件／题目模型解释。

## 4 · 动态扫描与共同端

共享段线、逐位开启共同端；换位前先关闭显示，更新段数据后再开启下一位，以减少重影。完整帧频率等于扫描槽频率除以位数，不能把时钟频率直接当作每位刷新率。

## 5 · Code Conversion · 数值守恒与位权

两位 BCD 数字 T、U 满足 $N=10T+U=8T+2T+U$，结果范围 0–99，需七位纯二进制。两个四位加法器的连接需逐位检查进位和权重，不能把 BCD 字节当纯二进制直接送出。

> [!IMPORTANT] 三张表要一致
> 数字→点亮段；段命令→电平；BCD→数值。分别核对规范、极性与使能，再检查扫描时序。

@@@ Tri-State Buffers and Bus Drivers
> [!SUMMARY] Quick recall · 英文速览
> High impedance releases a shared line. It is neither a driven zero nor an unknown Boolean value; bus ownership prevents competing drivers.

## 1 · 三态与使能

三态缓冲器 (tri-state buffer) 在使能时传递输入，关闭时输出高阻抗 Z (high impedance)。Z 描述驱动状态，X 描述逻辑值未知，二者不同；接收端读到什么电压还取决于其他驱动和偏置。

## 2 · 总线共享与冲突

共享总线 (bus) 的各驱动使能需互斥，通常满足任意时刻至多一者开启。两个驱动一个送 1、另一个送 0 会产生冲突，不能用普通 OR 函数解释。

## 3 · 切换与实际边界

切换所有者应先释放旧驱动再开启新驱动，遵守使能／关闭延迟。所有驱动关闭时需规定默认偏置或允许的无效状态。FPGA 内部共享数据通常综合为 MUX，实际 I/O 三态需由目标资源支持。

## 4 · 重点测试

> [!IMPORTANT] 单驱动与定义明确
> 检查互斥使能、全关闭、所有者切换与每个数据模式。悬空输入不能自动假定为 HIGH；波形有冲突时先检查驱动权，而不是改布尔方程。

@@@ Propagation Delay and Logic Hazards
> [!SUMMARY] Quick recall · 英文速览
> The longest path bounds settling; the shortest path bounds the earliest change. Different path delays can create glitches in an otherwise equivalent Boolean function.

## 1 · 最长路径与最短路径

最大传播延迟 $t_{pd}$ (propagation delay) 表示最迟稳定时间；最小污染延迟 $t_{cd}$ (contamination delay) 表示最早可能变化时间，单位 s 或 ns。串联路径相加，多条路径分别取最大／最小，不能混用。

## 2 · 静态冒险来自不同路径

$F=AB+\bar AC$ 在 B=C=1 时理论恒为 1；A 变化时两条路径的响应不同时可能产生短暂 0，为静态 1 冒险 (static-1 hazard)。共识项 (consensus term) BC 保持稳态等价，却可在该单输入转换条件下桥接间隙。

## 3 · 何时加项，何时依靠采样

组合输出直接控制异步信号时，毛刺可能立即产生效果；同步接收端在满足采样稳定窗口时可避开某些瞬态，但不能因此忽视建立／保持约束。多输入同时变化和动态冒险需更完整的模型。

> [!IMPORTANT] 化简目标要写清
> 最小文字数、少门、短路径与无静态冒险可能互相冲突。添加冗余项不是布尔错误，而是为特定转换增加覆盖；验证应包含稳态和转换条件。

@@@ Sequential Logic and Flip-Flops
> [!SUMMARY] Quick recall · 英文速览
> State records history. Distinguish level-sensitive storage from edge-triggered storage, then add explicit enable and reset priorities.

## 1 · Sequential Logic · 用状态连接过去与现在

时序逻辑 (sequential logic) 在有效事件处按 $Q^+=F(Q,X)$ 更新，输出由 Q 或 Q、X 决定。Q 是旧状态，不能在同一边沿逐个把新状态回灌其他触发器；组合反馈也不能自动当作受控时序电路。

## 2 · Set-Reset Latch · 反馈产生记忆

NOR 型 SR 锁存器的 S、R 高有效：00 保持、10 置 1、01 清 0、11 禁止。NAND 型低有效 $\bar S,\bar R$：11 保持、01 置 1、10 清 0、00 禁止。禁态及其同时释放无法用普通稳态表保证结果。

## 3 · D Latch and D Flip-Flop · 电平与边沿

D 锁存器在有效使能电平透明，其余时间保持；D 触发器只在规定有效边沿捕获 D。$Q^+=D$ 仅描述捕获事件，边沿之间保持旧 Q；异步控制另按规定优先处理。

## 4 · JK and T Flip-Flops · 条件更新

JK 的 00 保持、01 清零、10 置位、11 翻转，$Q^+=J\bar Q+\bar KQ$。T 触发器 $Q^+=T\oplus Q$。特性表 (characteristic table) 从输入求下一态；激励表 (excitation table) 从所需 Q→Q+ 求输入，方向不同。

## 5 · Register Enable and Reset · 控制优先级

使能 E 的 D 寄存器：$Q^+=ED+\bar EQ$。同步复位只在有效边沿执行；异步复位可在边沿之间改变 Q，释放仍要满足器件恢复／移除等时序条件。复位、置位、装载、保持同时有效时，必须由规范规定优先级。

> [!IMPORTANT] 波形题先列事件表
> 明确有效边沿、透明电平、初态、控制极性和优先级；使用边沿前的值计算所有 Q+，再一起更新。上电初态不能默认是 0。

## 6 · 从单元到系统

存储单元加入移位输入形成 [[Shift Registers and Ring Counters]]；组合下一态网络形成 [[Finite State Machine Design and Applications]]。可靠捕获还需 [[Sequential Timing and Clock Domain Crossing]]。

@@@ Shift Registers and Ring Counters
> [!SUMMARY] Quick recall · 英文速览
> A shift register moves old-state bits simultaneously. Ring and Johnson counters choose the feedback path to create cyclic patterns.

## 1 · Shift Registers · 位序与输入模式

移位寄存器 (shift register) 可串／并输入与输出；方向必须用显式位方程表示。以 $Q_3Q_2Q_1Q_0$ 为显示顺序，向右移为 $Q^+=(s_R,Q_3,Q_2,Q_1)$，向左移为 $(Q_2,Q_1,Q_0,s_L)$；并行装载与保持另由模式指定。

## 2 · 串行输入与时延

N 位链中每个边沿使用全部旧 Q，串入一位后数据经过 N 次移位才从末级串出。题目里“延迟 N 个周期”与从第一级 Q 到末级 Q 的边沿差 N−1 要按观测点区分。

## 3 · Ring and Johnson Counters · 同样的移位，不同的反馈

环形计数器 (ring counter) 将末级原值反馈，合法独热序列有 N 态；必须初始化为独热，全零会锁死。Johnson 计数器将末级取补反馈，合法循环通常为 2N 态，需要检查未用状态的恢复。

四位 Johnson 从 0000 出发，在规定方向下依次扩展 1 再扩展 0，周期八态；序列顺序由反馈端和显示位序决定，不能只背一个字符串。

> [!IMPORTANT] 三项不变量
> 所有位同步读旧状态；方向显式定义；循环长度在合法初始化条件下计算。one-hot／one-cold 码可驱动扫描，但不等于普通二进制计数。

@@@ One-Shots and Pulse Applications
> [!SUMMARY] Quick recall · 英文速览
> A one-shot produces a timed excursion after a trigger. A registered edge detector instead produces an event pulse measured in clock cycles.

## 1 · 稳态数量决定类别

单稳态 (monostable / one-shot) 有一个稳定状态，触发后暂时离开再返回；无稳态 (astable) 持续振荡；双稳态 (bistable) 可保存一位。不要把名称与具体触发极性混在一起。

## 2 · RC 阈值决定脉宽

一阶充电模型 $V_C(t)=V_f+(V_0-V_f)e^{-t/(RC)}$，到阈值 $V_T$ 的时间：
$$t=-RC\ln[(V_T-V_f)/(V_0-V_f)].$$
R 单位 Ω、C 单位 F，因此 RC 单位 s；阈值必须落在该转换实际经过的范围。系数由电路阈值决定，不应把某芯片的经验系数推广到所有单稳态。

## 3 · 数字事件脉冲与按键捕获

同步信号 x 与其一周期延迟 $x_d$ 的上升沿检测为 $p=x\bar x_d$，通常产生一周期脉冲；异步输入应先处理跨域与去抖。延迟捕获按键需保证采样时数据已经稳定。

> [!IMPORTANT] 时间单位来自实现
> RC 脉宽由模拟参数决定，寄存器事件脉宽由时钟周期决定。可重触发性、初态、输入最小宽度和边沿语义需另行给出。

@@@ Keyboard Scanning and Encoding
> [!SUMMARY] Quick recall · 英文速览
> Scan one line, sense the other dimension, encode a valid position, then capture once per qualified key event.

## 1 · 扫描先建立坐标

矩阵键盘 (matrix keyboard) 用行／列组合表示位置；逐槽只驱动一条扫描线，读另一维。one-cold 扫描表示一条线 LOW 有效；未选线驱动与外部偏置决定电气模型。

## 2 · 编码与有效条件

八行、八列分别需要三位代码，拼成六位位置码；独立 valid 指示本次扫描确有按键。行列字段顺序和高低有效规则需一致。没有 valid 时，位置 0 会与“未按键”混淆。

## 3 · 去抖、稳定与一次捕获

去抖 (debounce) 后生成明确的按下事件；先让扫描与感应信号稳定，再把行列代码装载进寄存器。持续按下是否重复输入，应由用户接口规范决定，不能由电平采样次数自动决定。

## 4 · 边界与复习

多键可能产生鬼影 (ghosting)，优先编码只决定哪个输入胜出，不能消除矩阵电气歧义。帧频率是槽频率除以扫描线数；若八条线用 8 kHz 槽频率，完整扫描为 1 kHz。

> [!IMPORTANT] 一条完整因果链
> 扫描选择→电压稳定→感应有效→位置编码→去抖事件→一次装载。逐级检查，避免数据码先于 valid 稳定时被错误捕获。

@@@ Finite State Machine Design and Applications
> [!SUMMARY] Quick recall · 英文速览
> State summarizes the relevant past. Define state meaning before encoding, derive complete transitions, then verify traces and unused states.

## 1 · Finite State Machine · 状态保存了什么历史

有限状态机 (FSM) 为 $Q^+=F(Q,X)$。状态应代表完成任务所需的最小历史，而不是先任意列几个二进制数。流程是：规范→状态含义→转换图／表→输出→编码→方程→验证。

## 2 · Moore and Mealy Machines · 输出依赖与时间对齐

Moore 输出 $Y=G(Q)$，Mealy 输出 $Y=G(Q,X)$。Mealy 可在当前输入到达时响应，但可能受输入毛刺影响；Moore 的响应与进入状态对齐。比较两者时必须标明哪个周期的输出。

## 3 · State Encoding and Unused States · 编码与恢复

M 态二进制编码至少 $\lceil\log_2M\rceil$ 位，独热编码使用 M 位。初始化必须进入合法状态；未用状态可否当 X 取决于规范，若要求恢复，需定义实际下一态而非任意删去。

## 4 · Sequence Detector · 最长可复用后缀

检测串行 110，定义 S0 无匹配、S1 已见末尾 1、S2 已见末尾 11。S0 在 1→S1、0→S0；S1 在 1→S2、0→S0；S2 在 1→S2、0 时断言检测并回 S0。重叠检测用匹配后的最长有效后缀决定回退。

检测 101 后若允许重叠，应保留末尾 1，因此 10101 可触发两次。并行字中出现某模式则属于组合逻辑，不能照搬串行状态机。

## 5 · Traffic Light Controller · 安全条件进入状态模型

交通灯状态规定哪条路通行以及黄色过渡；传感器决定是否保持／转移，定时器决定最短或最长持续时间。给每个状态完整输出，使冲突方向不会同时绿灯；复位状态、请求优先级和异常恢复必须明确。

## 6 · 方程与验证的接口

用所选触发器求每位激励；对全部状态×输入检查下一态和输出。测试覆盖状态、每条转移、重叠、复位、无效态与规定的输出时间。逻辑证明之外，路径还需满足时序约束。

> [!IMPORTANT] 先证明状态含义正确，再优化编码
> 少一个状态位不一定少逻辑；不能为了化简牺牲未用态恢复、安全输出或输入周期对齐。

@@@ Sequential Timing and Clock Domain Crossing
> [!SUMMARY] Quick recall · 英文速览
> Setup limits the latest arrival; hold limits the earliest arrival. Clock-domain crossing requires a transfer protocol beyond ordinary synchronous path checks.

## 1 · Setup and Hold Timing · 建立统一时间基准

令发射时钟到捕获时钟偏斜 $s=t_{capture}-t_{launch}$，正值表示捕获晚到；$t_{pcq},t_{ccq}$ 为最大／最小 clock-to-Q，组合路径为 $t_{pd},t_{cd}$，各时间同单位。忽略抖动等额外预算时：

$$T\ge t_{pcq}+t_{pd}+t_{setup}-s,$$
$$t_{ccq}+t_{cd}\ge t_{hold}+s.$$

建立约束检查下一次捕获的最迟到达；保持约束检查同次边沿之后最早变化。正偏斜改善 setup，却恶化 hold。

## 2 · 裕量与修复方向

setup slack 为可用时间减需求，负值表示违反。减慢时钟通常改善 setup，但不会自动修复同边沿 hold；hold 可通过增加最短数据路径延迟等方式修复，随后复查 setup。

## 3 · Metastability and Clock Domain Crossing · 异步输入的边界

亚稳态 (metastability) 可能因采样窗口被违反而产生。两级同步器让第一级有更多解析时间，降低传播概率，不保证绝对消除。第一级不能随意扇出给其他逻辑；同步器中间通常不插组合逻辑。

## 4 · 按信息类型选跨域方法

单比特慢电平可用同步器；窄脉冲可能被漏采，需展宽、toggle 或握手；多位数据逐位同步可能得到不一致的组合，需稳定数据＋握手、适当 Gray 指针或异步 FIFO。

> [!IMPORTANT] 波形稳定不等于传输完整
> 亚稳态风险、事件是否被看见、多个位是否来自同一次更新，是三个不同问题。先规定协议和速率，再选同步结构。

@@@ Counter Design and Digital Clocks
> [!SUMMARY] Quick recall · 英文速览
> A counter is a specified state sequence. Derive next state from old state, recover from invalid states, and enable higher digits on accepted rollover.

## 1 · Counters · 模数与时钟结构

计数器 (counter) 循环经过 M 个不同状态，模数 (modulus) 是状态数量，不一定等于最大显示数字加 1。异步纹波计数器由前级输出触发后级；同步计数器共享时钟，靠激励逻辑决定更新。

## 2 · Synchronous Counter Design · 从转换表求激励

二进制向上计数的 $T_i=E\prod_{j<i}Q_j$，最低位空乘积为 1。D 触发器直接取下一态方程；JK 按激励表求 J/K，不能把 J 简单当成下一态。

模 3 例：00→01→10→00，若规定 11→00 恢复，则 $D_1=\bar Q_1Q_0,D_0=\bar Q_1\bar Q_0$。指定非顺序计数应按给定序列逐行列下一态。

## 3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转

十进制级联中，高位使能为 $E_H=E_L\cdot TC_L$，其中 TC 指低位处于末态；两级在同一时钟读旧状态并更新。只解码“末态”而不与允许计数的 E 相与，会在暂停时误触发高位。

## 4 · 混合进制与预置截断

秒／分的 59→00 同时令上一级增加；个位模 10、十位模 6，满量程为 60 状态。预置计数要数实际经过的状态，并说明端点是否包含；分频输出的频率与高电平占空比也分别计算。

> [!IMPORTANT] 初态与控制优先级进入验证
> 检查使能关闭、装载、复位、末态、非法态与级联进位；不能只测试连续加 1。

@@@ Memory Organization and Technologies
> [!SUMMARY] Quick recall · 英文速览
> Depth and width define memory capacity. Technology explains how a bit is retained, read, written, and lost.

## 1 · Memory Arrays and Expansion · 寻址与容量

深度 D 表示可寻址 word 数，位宽 W 表示每 word 的 bit 数；容量 $C=DW$ bit。若有 $D=2^a$ 个 word，需 a 根地址线。先声明地址按 bit、byte 还是 word 编号。

## 2 · 扩展先宽度，后深度

并联数据位可扩展 W，地址与片选相同；增加深度用高位地址译码选 bank，低位地址送各片。扩展到目标深度与宽度所需片数分别相乘，并检查输出三态／使能避免多片同时驱动。

## 3 · SRAM DRAM and ROM · 保存机制决定操作

SRAM 靠双稳态反馈保持，通常不需刷新；DRAM 靠电荷保存，需刷新且读操作涉及恢复；二者通常均易失。ROM 用非易失结构保存内容，不同可编程类型的擦写方式和限制不同。

## 4 · 从物理存储到功能模型

“不刷新”不等于“掉电保存”；“只读”描述正常接口操作，不代表所有 ROM 类型永不可编程。存储技术、电气时序与逻辑组织是不同维度。

> [!IMPORTANT] 所有容量问题带单位
> 地址位数对应深度，数据线数对应位宽；总 bit 数除以 8 才是 byte 数。芯片数不能只按总容量凑数而忽略接口组织。

@@@ Programmable Logic and FPGA
> [!SUMMARY] Quick recall · 英文速览
> A ROM or LUT stores a truth table. A PLA shares product terms. An FPGA combines programmable logic, state elements, routing, and constrained physical implementation.

## 1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积

n 输入、m 输出的任意组合函数可用 $2^n\times m$ 的 ROM 表示，输入是地址、内容是输出；这是功能存储量，不含器件附加开销。PLA 采用可编程 AND／OR 阵列，允许多输出共享乘积项；PAL 的可编程范围需按结构声明。

## 2 · LUT：查表实现组合逻辑

k 输入 LUT 存储 $2^k$ 个真值 bit。配置内容在逻辑运行时作为固定函数使用；用户的运行状态另由 FF 等资源保存。查找表和通用读写存储的角色不同。

## 3 · Field-Programmable Gate Array · 从函数到物理实现

FPGA 由 LUT、触发器、可编程连线和 I/O 等构成。设计流程：行为建模→功能仿真→综合→布局布线→约束下的时序分析→上板验证。

## 4 · 约束与可靠运行

时钟、输入／输出时延、电气标准和引脚分配要明确。仿真正确只证明所测模型功能；布局后的时序收敛 (timing closure) 和实际接口条件仍需验证。异步输入、复位释放和共享总线问题不会由综合工具自动替规范作出决定。

> [!IMPORTANT] 状态与配置分开
> LUT 定义函数，FF 保存运行状态，约束定义外部承诺。读到一个逻辑真值表，不能据此断定整个系统无状态。

@@@ VHDL Modeling and Verification
> [!SUMMARY] Quick recall · 英文速览
> VHDL describes concurrent hardware. A testbench drives the design and checks an independent reference model; simulation success is one layer of evidence.

## 1 · VHDL Language and Modeling · 接口与实现

entity 定义端口，architecture 描述实现。`std_logic` 可表示多值逻辑；数值运算使用明确的 `unsigned`／`signed` 类型并声明位宽，不能把位向量的显示形式当作整数语义。

## 2 · 并发、过程与更新时机

architecture 中各并发语句与 process 并行存在；process 内顺序执行不意味着硬件逐条耗时。signal 的赋值通过 delta cycle 更新，variable 在当前过程立即更新；连续给同一 signal 赋值不能当作软件累加器。

## 3 · 组合与时钟建模

组合 process 完整覆盖所有分支与相关输入，避免无意锁存；时钟 process 在 `rising_edge(clk)` 更新寄存器，复位的敏感列表和位置体现同步／异步语义。使能关闭时保持状态应与硬件规范一致。

## 4 · Testbench and Functional Verification · 规范作为独立参照

testbench 为 DUT 产生时钟、复位、模式和数据；参考模型从规范建立，不复制 DUT 的内部表达式。对小组合模块穷举，对时序模块测试初态、所有模式、方向切换、复位优先级、边界和长序列。

## 5 · 断言、采样与覆盖

在时钟边沿后等待规定的仿真更新，再用 assertion 比较预期输出。delta cycle 不等于真实门延迟。零错误只代表已覆盖条件一致；综合可行性、约束时序和物理接口仍需分别检查。

> [!IMPORTANT] 保留完整可运行例子
> 下方实现与 testbench 包含库、类型、时钟和检查逻辑；实际项目结构化端口连接见 [[Structural Shift Register Project]]。不要只保存一个无法解释上下文的赋值片段。

@@@ Structural Shift Register Project
> [!SUMMARY] Quick recall · 英文速览
> Structural design instantiates reusable state cells and explicitly connects next-state logic. Bit order, shift direction, and control priority define correctness.

## 1 · 规范先写成位方程

本教学实现为 **4 位双向移位寄存器**：状态读作 q(3 downto 0)，正沿采样，高有效异步复位。R=1 时向低位右移、SR 进入 q3；R=0 时左移、SL 进入 q0。先写每位下一态，再实例化 DFF，避免凭“左／右”文字接反。此实现每拍移位；保持与并行装载是另加选择分支的扩展功能。

## 2 · 复用 DFF 与连接顶层

基础 DFF 只在有效边沿采样，复位方式与规范相符。顶层组合选择 next-state，端口映射 (port map) 将每个实例的 D、Q、clock、reset 明确连到实际信号。共时钟下各实例使用旧 Q。

## 3 · 运行轨迹与独立验证

从复位后的 0000 开始，R=1、SR 依次输入 1、0、1、1，状态依次为 1000、0100、1010、1101。再 R=0、SL=0 得 1010；下一拍 SL=1 得 0101。预期模型使用位方程而非复制连线。覆盖 16 个旧状态、2 个方向、4 组双串行输入，并检查边沿间异步复位与方向改变。

## 4 · 综合与实现

完整源代码、实例化与测试要求在下方展开；功能通过后检查目标 FPGA 引脚、时钟、I/O 电气和时序。实际资源优化可以改变门的形状，但不能改变约定的寄存器行为。

> [!IMPORTANT] 两个常见错误
> 信号赋值的更新不即时，不能当软件循环移位；方向端改变也会改变 D 输入，必须满足采样条件，外部按钮信号需先处理同步与去抖。

@@@ Exam Review and Problem Solving
> [!SUMMARY] Quick recall · 英文速览
> Read the specification, choose the model, derive independently, and test the boundaries. A familiar-looking answer is not evidence of correctness.

## 1 · 用先修链组织复习

数制与表示→逻辑门与接口→布尔形式与化简→组合功能块→存储与时序→状态机／计数器→存储／HDL。先闭卷写 governing equation，再做典型例题，最后检查条件和反例。

## 2 · 读题先标六项约束

变量顺序、位宽、signed／unsigned、有效极性、有效边沿／初态、exactly／at least 与 invalid-state 策略。并行字匹配与串行序列识别需不同模型；复位并不自动发生在上电。

## 3 · 数制、算术与表示

转换用位权复核；补码先算数学结果再检查范围；定点明确缩放；浮点先分类特殊码。carry、borrow、signed overflow 和 rounding 分别解释。

## 4 · 布尔与组合设计

先列 ON／OFF／don't-care，再给分组、方程与实现；核对输出极性与额外反相器。最小表达式不保证无冒险。优先输出先判断是独热掩码还是紧凑代码。

## 5 · 时序、状态与计数

逐边沿读旧状态、同时计算下一态；setup 取最长路径，hold 取最短路径；偏斜按统一符号加入。FSM 用状态含义解释转移，计数器检查实际状态数、末态和暂停时的级联行为。

## 6 · 存储与 HDL

容量拆成深度×位宽；ROM 地址与数据按真值表编程。VHDL 区分 signal／variable、组合／时钟过程与 delta cycle；testbench 的参考结果独立来自规范。

## 7 · 重点自查与答句

> [!IMPORTANT] 最有效的反例
> exactly 与 at least 用全 1 区分；XOR 与 exactly-three 用 0001 区分；优先编码用重叠请求；校验用双比特错误；时序用最早与最迟到达；计数器用暂停在末态。

“With the declared variable order, the ON set is … . The reduced expression agrees on every specified row. The implementation additionally requires … under the stated polarity and timing assumptions.”

下方保留跨章综合例题与英文答题练习；遇到薄弱环节从 [[ECE2050 Knowledge Tree]] 回到对应主线笔记。
