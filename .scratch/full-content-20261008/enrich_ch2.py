from pathlib import Path
import json, re

ROOT = Path.cwd()
BASE = ROOT / '.scratch/full-content-20261008'
OUT = BASE / 'draft/Notes'
OUT.mkdir(parents=True, exist_ok=True)
mapping = json.loads((ROOT / '.scratch/consolidation-20261008/mapping.json').read_text(encoding='utf-8-sig'))
links = json.loads((ROOT / '.scratch/consolidation-20261008/link-mapping.json').read_text(encoding='utf-8-sig'))

ADD = {}
ADD['Number Systems and Base Conversion'] = {
1: r'''
### 核心模型、适用前提与读数方法

数制是表达数的书写体系；同一个值可以用不同基数表示。日常的 10、12（一打／钟面）、60（分秒／角度）是不同场景中的约定。这里的公式针对**位权制 (positional number system)**，不涵盖一切符号编码。

| 要素 | 定义与约束 | 作用 |
|---|---|---|
| 基数 (base / radix) $R$ | 整数 $R\ge2$ | 相邻位置的位权倍率 |
| 数码 (digit) $a_i$ | 整数 $0\le a_i\le R-1$ | 在该位取几份权重 |
| 位权 (positional weight) $R^i$ | 由位置 $i$ 决定 | 数码为 0 也保留这个位置 |
| 小数点 (radix point) | 分隔 $i\ge0$ 与 $i<0$ | 左侧第一位权 1，右侧第一位权 $1/R$ |

若整数部分有 $n$ 位、小数部分有 $m$ 位，上限写成 $n-1$：

$$x=\sum_{i=-m}^{n-1}a_iR^i.$$

此处 $n,m$ 是位数，$i$ 是位置编号，所有量无量纲。没有前导零、首位非零的 $n$ 位非负整数满足 $R^{n-1}\le x<R^n$；若允许前导零，则只能保证 $0\le x<R^n$。这条范围检查比“位数乘最高位权”更准确。

**读数五步。** 确认题面指定的基数与编码 → 检查所有数码是否合法 → 从小数点逐位编号 → 累加数码乘位权 → 用范围或逆转换复核。非零项可省略书写，但编号不能跳过零位。无下标 `1011` 在 2、8、10、16 进制都合法；若题面约定普通数字默认十进制，就按该约定读，不能自行认定为二进制。

**适用边界。** 位权展开只决定数值的基数解释；位宽、signedness 和隐含小数点位置仍需另行指定。格雷码 (Gray code) 不存在通常的固定线性位权，必须解码；它并非“每一位的位置都没有作用”。BCD 的每组使用 8421 权重，组间则按十进制数字位置解释，不能整串当纯二进制读。

**常见误区。** 非法数码不能以“照算也有结果”为由接受，例如 $(19)_8$、$(102)_2$ 非法；$R^0=1$ 而非 0；decimal 指 base-10，与是否有小数点无关；位数增加改变可用模式数量，是否改善精度还取决于格式。

**Exam English.** “A radix specifies the digit set and positional weights. A code specifies how a pattern is interpreted. The same pattern can have different values under different radices or encodings.”
''',
2: r'''
### 位权、查表与硬件阅读

| $R$ | 整数位权，由右向左 | 小数位权，由左向右 | 第一次进位 |
|---|---|---|---|
| 10 | $1,10,100,1000,\ldots$ | $1/10,1/100,1/1000,\ldots$ | $9+1=(10)_{10}$ |
| 2 | $1,2,4,8,\ldots$ | $1/2,1/4,1/8,\ldots$ | $1+1=(10)_2$ |
| 8 | $1,8,64,512,4096,\ldots$ | $1/8=0.125,1/64=0.015625,\ldots$ | $7+1=(10)_8$ |
| 16 | $1,16,256,4096,\ldots$ | $1/16,1/256,\ldots$ | $F+1=(10)_{16}$ |

小数点后第一位指数是 $-1$。删除点后得到的整数除以 $R^m$，可交叉验证有 $m$ 位小数的读数：$(10.101)_2=(10101)_2/2^3=21/8=2.625$。

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $2^k$ | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |

连续 $k$ 个整数位 1 的值为 $2^k-1$。非负整数 $x$ 的最少位数为 $\lceil\log_2(x+1)\rceil$（$x=0$ 若需实际码字通常写一位 0）；568 需 10 位：$(1000111000)_2$。左移小数点 $k$ 位使显示值除以 $2^k$，右移使显示值乘以 $2^k$；若要保持值不变，必须相应修改指数或格式。

| 八进制数字 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 三位二进制 | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| Linux 权限组 rwx | --- | --x | -w- | -wx | r-- | r-x | rw- | rwx |

权限数字内部按 read/write/execute 的 $4/2/1$ 权值相加；三位权限的先后是 owner / group / others。`755` 表示 `rwxr-xr-x`，不是“r=7、w=5、x=5”。八进制在字长为 3 的倍数的场景方便，但 8 位 byte 不与 3 位组整齐对齐。

| 十六进制字母 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 数值 | 10 | 11 | 12 | 13 | 14 | 15 |
| 四位二进制 | 1010 | 1011 | 1100 | 1101 | 1110 | 1111 |

十六进制有 10 个数字符号和 6 个字母符号；$9+1=A$，而 $(10)_{16}=16$。`0x45` 的高 nibble 是 4、低 nibble 是 5，值为 $4\times16+5=69$；`0x100=256`，`0x1000=4096`，`0x80=128`，`0xFF=255`。一个固定 8 位字节写两位十六进制，16 位字写四位；普通整数 `0x0F` 和 `0xF` 同值，保留零的必要性来自题目对宽度的要求。

**字面量语法。** C/Java 的前导 0 整数字面量如 `010` 按八进制表示 8；Python 3 八进制整数写 `0o10`，不能照抄 `010`。十六进制常写 `0x28A`；Verilog 可写 `12'h28A`，VHDL 位串可写 `x"28A"`。数学值、语言语法、位宽是三个独立约定。

**二进制的硬件理由。** 实际电压连续变化，数字设计把它划成两个有效逻辑区间，在区间之间留出噪声容限 (noise margin)，并让布尔逻辑直接映射到门电路。二进制简化实现，并非所有器件只能具有两个物理状态。相关电平条件见 [[Logic Levels and Noise Margins]]。

**十进制的接口作用。** 可内部以纯二进制计数、输出时转换，也可逐位保存 BCD。选择影响存储长度、转换电路和十进制进位；并非每次 I/O 都必须先执行一条独立的转换步骤。

**误区检查。** 只对非零位求和时仍应数清零位置；整数分组从点向左、小数从点向右；完整 4 位整数从左或右分组会一致，错误在于未与最低位对齐。十六进制缩短的是写法，模式总数仍由 bit 数决定。大小写不影响 hex 数值；按字符串比较时需统一形式。十六进制也能书写小数，如 $(A.8)_{16}=10.5$，并非“十进制小数只能用 BCD 或浮点”。

**Exam English.** “Decimal describes the radix, whereas fractional describes a noninteger value. Octal and hexadecimal are compact notations for binary patterns: one digit corresponds to three and four bits respectively.”
''',
3: r'''
### 选算法、执行方向与精度条件

转换保留数学值；编码转换保留指定语义；截断或舍入则可能改变值。先写源基数 $R$、目标基数 $S$，再检查输入数码、符号、位宽和小数精度要求。

| 任务 | 操作方法 | 读取顺序与停止条件 |
|---|---|---|
| $R\to10$ | 累加 $a_iR^i$ | 从小数点编号，不能漏零位置 |
| 非负整数 $I\to S$ | $q=\lfloor I/S\rfloor$，余数 $r=I-Sq$；重复处理商 | 首个余数为最低位；商为 0 后逆序读；$I=0$ 单独写 0 |
| 纯小数 $f\to S$ | $d=\lfloor Sf\rfloor$，$f\leftarrow Sf-d$ | 数码按产生顺序读；余数到 0 或达到给定位数 |
| binary $\leftrightarrow2^k$ | 每 $k$ 位构成一个数码 | 以点为界独立分组；整数左端／小数右端补 0 |
| $R\to S$ 一般情况 | 可经十进制求值后再编码，也可直接在目标进制累积 | 十进制是手算核算的选择，并非必经步骤 |

“找最大幂相减”在 base-2 中每个幂最多取一次；任意 $S$ 进制应取商数码 $d\in\{0,\ldots,S-1\}$，再减 $dS^i$，不能把所有目标数码都限制为 0/1。若 $R,S$ 都是 2 的幂，先展开成二进制再重新分组即可，例如 $(7526)_8=(F56)_{16}$；不要求 $R$ 自身是 $S$ 的整数次幂。

既约有理数 $p/q$（$q>0$，$\gcd(p,q)=1$）在 base-$S$ 有有限表示，当且仅当存在非负整数 $m$ 使 $q\mid S^m$；等价于 $q$ 的每个质因数都出现在 $S$ 中。base-10 要求 $q=2^a5^b$，base-2/8/16 要求 $q$ 是 2 的幂（含 $q=1$）。$1/3$ 在十进制和二进制都循环，$1/10$ 只在十进制有限；不是“到了二进制正好反过来”。

保留 $m$ 位小数时，非负值截断误差满足 $0\le x-x_{trunc}<S^{-m}$；在无溢出且采用最近舍入时 $|x-x_{round}|\le\tfrac12 S^{-m}$。循环小数需说明取几位和舍入规则，不能把近似输出写成无限精度恒等式。

**收尾检查。** 余数是否合法（hex 10–15 写 A–F）→ 宽度放得下 → 转回源值或换第二条算法 → 确认补零没有改变量级。整数右端补 $k$ 个零会乘 $2^k$；小数末尾补零不改值。位串按四位分隔只是排版，实际 octal 分组仍按三位。

**Exam English.** “The first remainder from repeated division is the least significant digit. Fractional digits from repeated multiplication are read in the order generated. Conversion through decimal is convenient but not mathematically necessary.”
''',
4: r'''
### 单位、容量和边界计算

最高有效位 (most significant bit, MSB) 通常写在左，最低有效位 (least significant bit, LSB) 在右；这描述位串书写顺序，不自动决定串行发送次序或多字节的 endianness。

| 容器 | 位宽 $N$ | 物理模式数 $2^N$ | 作为无符号整数的范围 |
|---|---|---|---|
| bit · 位 | 1 | 2 | 0–1 |
| nibble · 半字节 | 4 | 16 | 0–15 |
| byte · 字节 | 8 | 256 | 0–255 |
| 本题约定的 16 位 word · 字 | 16 | 65 536 | 0–65 535 |
| 本题约定的 32 位 doubleword · 双字 | 32 | 4 294 967 296 | 0–4 294 967 295 |

word/halfword/doubleword 的宽度依架构或题目定义，不能把 word 固定等同于 16 bit。模式总数对任何 $N$ 位容器都为 $2^N$；可用数字数量再看编码：BCD 每组只用 10 个，原码两个零对应同一数值，完整 Gray 编码则使用全部 $2^N$ 个码字，不会因“非位权”而浪费容量。ASCII 是七位的完整码空间；放进八位容器时高位用途需说明。

| 十进制 SI 前缀 | 倍率 | 对应二进制前缀 | 倍率 |
|---|---|---|---|
| kilo, k | $10^3$ | kibi, Ki | $2^{10}=1\,024$ |
| mega, M | $10^6$ | mebi, Mi | $2^{20}=1\,048\,576$ |
| giga, G | $10^9$ | gibi, Gi | $2^{30}=1\,073\,741\,824$ |
| tera, T | $10^{12}$ | tebi, Ti | $2^{40}=1\,099\,511\,627\,776$ |
| peta, P | $10^{15}$ | pebi, Pi | $2^{50}=1\,125\,899\,906\,842\,624$ |
| exa, E | $10^{18}$ | exbi, Ei | $2^{60}=1\,152\,921\,504\,606\,846\,976$ |

$2^{10}\approx10^3$ 是估算，精确值始终是 1024。1 MB 为 $10^6$ B，1 MiB 为 $2^{20}$ B；不能先写 MB 再强制按 1024 计算。bit 常记 b，byte 记 B，例如 8 Mb 是 1 MB。

**容量题五步。** 判断 $N$ 表示数据位、地址位还是编码位 → 算模式数 → 根据 signedness/编码写值域 → 若是存储器，计算“深度 × 每 word 的位数” → 换单位并检查差一。例如 32 位地址可选择 $2^{32}$ 个位置，仅在**按字节寻址**时容量为 $2^{32}$ B=4 GiB；若一位置为 $W$ bit，容量为 $2^{32}W$ bit。

**边界复核。** $2^{24}=16\,777\,216$ 个模式（约 16.78 million），$2^{32}=4\,294\,967\,296$ 个模式；最大无符号值再减 1。地址跨度为 $L$ 字节、起始地址 $A$ 时，末地址为 $A+L-1$。容量不能写成无符号最大值，估数量级不能替代精确容量。

**Exam English.** “An $N$-bit container has $2^N$ patterns. An $N$-bit unsigned integer ranges from zero to $2^N-1$. Address width determines the number of locations; the size of each location determines the total memory capacity.”
''',
5: r'''
先修与本篇内部连接：位权模型 → 四种数制的读法 → 整数／小数转换 → 位宽与容量。转入 [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算|二进制算术]] 时继续保留位权和范围检查；[[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|补码]] 将最高位改为负权；[[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度|定点数]] 将整数乘固定尺度，[[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|浮点数]] 用指数存尺度。

比较编码时连接 [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码|BCD]]（逐个十进制数字）、[[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束|Gray]]（相邻变化）、[[Data Coding and Character Representation#4 · American Standard Code for Information Interchange · 字符编码|ASCII]]（字符）。容量应用连接 [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|存储器组织]]、[[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|状态编码]] 和 [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|计数器]]。
'''
}

ADD['Binary Arithmetic and Signed Representation'] = {
1: r'''
### 完整法则、前提与操作步骤

| 运算 | 一位规则 | 一组数的操作 |
|---|---|---|
| 加法 (addition) | $0+0=0,0+1=1,1+0=1,1+1=(10)_2$ | 逐列带 carry-in，相加后传 carry-out |
| 减法 (subtraction) | $0-0=0,1-0=1,1-1=0$；$0-1$ 借位 | 向高一列借出的 1 等于本列的 2，同时扣减高列 |
| 乘法 (multiplication) | 只有 $1\times1=1$ | 第 $i$ 位部分积 (partial product) 左移 $i$ 位后累加 |
| 除法 (division) | 商位只能为 0 或 1 | 长除比较与条件减法；或幅值反复相减 |

本节首先按**无符号整数 (unsigned integer)** 解释操作数，$A,B\in[0,2^N-1]$。固定 $N$ 位加／减／截短乘法的结果是精确数学结果模 $2^N$ 的余数；除法不是简单“把精确除法模 $2^N$”，还要定义商和余数。对 $B>0$ 的无符号除法，$A=BQ+R,\ 0\le R<B$。

**竖式五步。** 明确位宽与解释 → LSB 对 LSB、短的零扩展 → 写每列操作数及 carry/borrow → 将该列进位／借位传到高列 → 分别报告完整值、保留低位和越界标志。$m$ 位乘 $n$ 位的完整无符号乘积最多 $m+n$ 位；加法可保留 $N+1$ 位以容纳最高进位。

| $N$ 位无符号运算 | 精确结果放得下的条件 | 标志与存储值 |
|---|---|---|
| $A+B$ | $A+B<2^N$ | carry-out $c_N=1$ 表示超出 $N$ 位；低位 $S=(A+B)\bmod2^N$ |
| $A-B$ | $A\ge B$ | borrow-out=1 表示借位；低位 $S=(A-B)\bmod2^N$ |
| $A+\bar B+1$ 实现减法 | 同上 | 在常见约定中 carry-out=1 表示**无借位**，borrow=$\bar c_N$ |
| 乘法后缩到 $N$ 位 | $AB<2^N$ | 检查被丢高位是否非零，不能只看最后一次加法的 carry |

**误区。** 不能在二进制结果写数码 2；借位时要同时扣高列；部分积不能忘记位权移位；$4\times4$ 位乘法结果只留 4 位可能严重回绕。$11+6$ 精确值是 17，四位输出 `0001` 只是 $17\bmod16$，不是数学等式 $11+6=1$。carry 表示无符号高位信息，补码 overflow 要用下一节的符号判据。

反复减除数的算法每次成功相减使商的数值加 1，运行次数与商大小有关；逐位长除每落一位最多试减一次，运行次数与被除数位数有关。两者同商同余数，但不能说反复相减“每一步都是一个商位”。

**Exam English.** “Report the retained result and the carry or borrow separately. A carry-out reconstructs the full unsigned sum; it is not, by itself, the signed overflow flag.”
''',
2: r'''
### 原码的编码、解码与专用算术

$s\in\{0,1\}$ 是独立符号字段，$M=\sum_{i=0}^{N-2}b_i2^i$ 是 $N-1$ 位无符号幅值。非零数 $s=0$ 为正、$s=1$ 为负。$2^N$ 个码字只给出 $2^N-1$ 个不同整数值，原因是 $M=0$ 有两种符号码。

| 数值 | 8 位原码 | 说明 |
|---|---|---|
| $+0$ / $-0$ | `0000 0000` / `1000 0000` | 数学上同为零，可按接口归一化 |
| $+6$ / $-6$ | `0000 0110` / `1000 0110` | 幅值相同，只改独立符号位 |
| $+127$ / $-127$ | `0111 1111` / `1111 1111` | 对称端点；不能表示 −128 |

**编码。** 先检查 $|x|\le2^{N-1}-1$，把 $|x|$ 补齐为 $N-1$ 位，再贴符号位。**解码。** 拆最左一位与余下幅值，分别读出符号与无符号数后相乘。例如 4 位 `1000` 是 −0；按补码解释才是 −8。不得对原码负值执行“取反加一”来读幅值。

| 4 位编码例 | 幅值补到三位 | 贴符号位后的原码 |
|---|---|---|
| +3 / −3 | `011` | `0011` / `1011` |
| +7 / −7 | `111` | `0111` / `1111` |

**正确加法。** 同号时幅值相加并保留共同符号，检查幅值是否溢出；异号时大幅值减小幅值，符号取较大幅值操作数的符号；异号等幅值结果为零并规定零码。专用电路可以完成这些步骤，不能把“普通整字加法不适用”概括为“原码不能运算”。判零可直接检查幅值位全零，无须必然做两次完整码字比较。

**误区。** 8 位原码的幅值是 7 位，不是 6 位；原码范围与补码范围不能互换；补到目标宽度时符号字段位置必须保持最左。IEEE 754 的独立符号位具有类似思想，但指数和有效数字有自己的编码，不等于把浮点整个字当原码整数。

**Exam English.** “Sign-magnitude stores a separate sign and an unsigned magnitude. Equal signs require magnitude addition; opposite signs require magnitude comparison and subtraction. A dedicated datapath is needed for that interpretation.”
''',
3: r'''
### 编解码、范围与独立的溢出判据

设同一 $N$ 位模式无符号读数为 $u$，补码值为

$$x=\begin{cases}u,&u<2^{N-1},\\u-2^N,&u\ge2^{N-1}.\end{cases}$$

最高位常称符号位 (sign bit)，同时具有负位权，不能像原码一样把它拆掉后直接读幅值。零只有全零一个码；负数有 $2^{N-1}$ 个，正数有 $2^{N-1}-1$ 个，另有一个零。

| 4 位码 | 值 | 4 位码 | 值 | 4 位码 | 值 | 4 位码 | 值 |
|---|---|---|---|---|---|---|---|
| 0000 | 0 | 0100 | 4 | 1000 | −8 | 1100 | −4 |
| 0001 | 1 | 0101 | 5 | 1001 | −7 | 1101 | −3 |
| 0010 | 2 | 0110 | 6 | 1010 | −6 | 1110 | −2 |
| 0011 | 3 | 0111 | 7 | 1011 | −5 | 1111 | −1 |

**编码／解码流程。** 检查目标 $N$ 位范围 → 编码可直接取 $u=x\bmod2^N$ → 写足 $N$ 位；负数也可将幅值写足 $N$ 位后 invert and add one。解码用负权或 $u-2^N$，这两种方法对最小负数也正确。求相反数 $(\bar u+1)\bmod2^N$ 永远定义了一个模式，但当 $x=-2^{N-1}$ 时该模式仍代表自身，数学相反数不可在原宽度表示。

扩展位宽先做**符号扩展 (sign extension)**：复制原 MSB，例如 4 位 −6=`1010` 扩到 8 位为 `1111 1010`。零扩展成 `0000 1010` 会变为 +10。固定位宽加／减可复用同一加法器，结果取低 $N$ 位；完整宽乘法须额外处理符号，不可由“加法可共用”推出所有乘除电路均完全相同。

设 $a_s,b_s,z_s$ 是操作数 A、B 和输出 Z 的最高位；$c_{N-1}$ 是进入最高位的进位，$c_N$ 是其输出进位：

$$V_{add}=\overline{a_s\oplus b_s}\,(a_s\oplus z_s)=c_{N-1}\oplus c_N.$$
$$V_{sub}=(a_s\oplus b_s)(a_s\oplus z_s),\qquad Z=A-B.$$

上式乘法记号表示逻辑 AND。加法同号而结果异号才发生 signed overflow；异号相加不会溢出。减法则是操作数异号且结果符号与 A 不同。对 $A+\bar B+1$ 可用实际进位链 $c_{N-1}\oplus c_N$，不要先在 $N$ 位里算 $-B$ 再丢掉它本身的溢出信息。

**符号标志与进位。** 结果 MSB 给出所存模式的符号，overflow flag 指出真值是否可表示，carry flag 描述无符号高位。三者不能互相替代。恰有一正一负相加时，carry-out=1 表示真实和非负（可能为零），carry-out=0 表示负；这只是该特定条件下的性质，通常应先按 MSB 解码。

**常见误区。** invert 只是取反，不等于取相反数；补码没有 −0，范围也不对称；弃 carry 后仍必须查 signed overflow；最小负数求幅值、取负或除 −1 前需扩大中间宽度或声明越界策略。

**Exam English.** “The carry flag and signed overflow flag describe different interpretations. Two's-complement addition overflows when equally signed operands produce an oppositely signed result. The stored sign is reliable only when the exact result is representable.”
''',
4: r'''
### 两条乘法路线与完整除法约定

对于 $N$ 位补码 A、B，$2N$ 位补码足以容纳完整乘积。乘积缩回 $N$ 位时必须另查范围。以下选择两条正确路线之一，不能混用。

**路线 A：幅值乘法。** 在足够宽的中间格式取 $|A|,|B|$ → 按全部非负权重移位相加 → 根据非零输入的符号 XOR 定乘积符号 → 若为负，在目标 $2N$ 位上取反加一 → 解码复核。最小负数的幅值 $2^{N-1}$ 可用 $N$ 位**无符号**表示，不能要求它仍落在 $N$ 位有符号范围中。

**路线 B：直接补码部分积。** 先把 A 符号扩展到 $2N$ 位，再在该宽度移位。乘数最高位具有负权，因此

$$AB=\sum_{i=0}^{N-2}b_i(A2^i)-b_{N-1}(A2^{N-1}).$$

低 $N-1$ 行是条件相加；最高行若 $b_{N-1}=1$，必须**条件相减**。另一等价实现是先对所有 $b_i$ 按正权累加，再显式减 $b_{N-1}A2^N$。符号扩展保证被乘数值正确，不能自动把乘数 MSB 的正权变成负权。直接路线所得结果已带符号，不能最后再按 XOR 取负一次。

**反例与校验。** 4 位 A=+3=`0011`、B=−2=`1110`，正确是 $0+3\times2+3\times4-3\times8=-6$，8 位 `1111 1010`。若仅符号扩展 A 并把所有乘数位都按正权相加，会得到 $3\times14=42$；仅丢高进位也不能修复 42。每行必须先扩展再移位，避免先在窄宽度左移而丢失有效位。

**截断除法 (division truncated toward zero)。** 对 $B\ne0$，先做幅值除法得到 $|A|=|B|Q_0+R_0,\ 0\le R_0<|B|$。商 Q 按输入符号 XOR 取正负（零商无负号）；非零余数 R 的符号与 A 相同。最后检查 $A=BQ+R$、$|R|<|B|$、商是否落在目标范围。$-2^{N-1}/(-1)=2^{N-1}$ 是非零除数情况下的商溢出。

幅值反复相减应写成“只要 $R\ge|B|$，减除数并加商”，停止时余数小于除数；这种先比较的算法不会出现负余数。若选择先试减再判号，失败时恢复余数，且那次不能计入商；若已经增加了商还需撤销。逐位恢复除法每次先移入下一位，再试减并决定该商位 0/1，不能把它与按商大小循环的算法混成同一流程。

**移位限制。** 算术右移复制符号位，对负补码通常对应向负无穷取整的除 $2^k$，不总等于向零截断除法：−3 算术右移一位为 −2，向零截断 −3/2 为 −1。逻辑右移补零；左移也可能溢出，位移不是绕过范围检查的工具。

**Exam English.** “Sign extension alone does not correct the negative weight of the multiplier's MSB. Subtract its partial product in a direct two's-complement multiplication. For division, specify the quotient rounding rule and verify both the identity and the remainder bound.”
''',
5: r'''
先修：[[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|位权和二进制读数]]、[[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|位宽和范围]]。原码与补码是解释同一容器的两种选择；本篇加减和 signed 乘除建立在这些选择之上。

实现连接 [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒|半加器／全加器]]、[[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径|进位结构]]、[[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路|加减器]]、[[Binary Arithmetic Circuits#4 · Combinational Multiplier · 从部分积到列加法|乘法器]] 和 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|移位寄存器]]。[[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|CRC]] 则在 GF(2) 多项式系数上计算，没有整数进位，是另一套代数。

小数应用连接 [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度|Q 格式]]（补码整数加固定缩放）和 [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围|浮点字段]]（符号与指数编码需分别读）。
'''
}

ADD['Fixed-Point and Floating-Point Numbers'] = {
1: r'''
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
''',
2: r'''
### 尺度传播、量化与越界处理

对 $x=n_x2^{-b_x}$、$y=n_y2^{-b_y}$，先决定输出小数位数 $b_z$。加减可在公共尺度 $b_c=\max(b_x,b_y)$ 下左移较粗代码；符号扩展并保留中间高位后相加，最后按输出尺度缩放与舍入。不能直接对不同 b 的代码相加。

乘法先计算完整整数积 $p=n_xn_y$，其尺度为 $2^{-(b_x+b_y)}$，再求

$$n_z=\operatorname{round}_{mode}\!\left(p\,2^{b_z-b_x-b_y}\right).$$

因此 Q4.4 × Q4.4 的完整 16 位代码有 8 个小数位；若输出仍为 Q4.4，要除 $2^4$ 再舍入，最后查 8 位 signed 范围。不能只截取低八位，那会破坏尺度；右移负代码时也需匹配向零／向负无穷／最近舍入约定。

最近舍入且无饱和／溢出时，量化误差 $|\hat x-x|\le\Delta/2$；向零截断时 $|\hat x-x|<\Delta$。舍入模式作用于正负两侧的方向应清楚，不能笼统把负数右移称作向零截断。

**回绕 (wrap-around)** 保留低 $N$ 位；**饱和 (saturation)** 将越界值钳到格式的最小或最大可表示值。它们是可选规范，不是所有定点装置必然不会报错或必然需要饱和。U4.4 的 $12+7.5=19.5$：回绕为 3.5，饱和为 15.9375；两者误差远大于量化一步，不能与“精度损失”混淆。
''',
3: r'''
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
''',
4: r'''
### 精度边界、特殊值与格式误用

对正正规 binary32 区间 $[2^e,2^{e+1})$，相邻值间距为 $\operatorname{ULP}=2^{e-23}$。相对分辨率在量级上近似固定，绝对分辨率随指数变，不是精确“相对精度常数”。在 $[2^{24},2^{25})$ 中间距为 2，因此整数 $2^{24}+1$ 不可精确存储；round-to-nearest, ties-to-even 将它舍入为 $2^{24}$。在 $10^8$ 附近 ULP=8，该模式下加 1 后仍为 $10^8$。

binary32 的 $0.1$ 为 `0x3DCCCCCD`，真实存储值约 0.10000000149011612；分母含 5，不能在有限二进制中精确表示。binary64 的 `0.1+0.2==0.3` 通常为假，严格逐步 binary32 最近舍入时可为真，必须同时说明格式和舍入。

NaN 的 IEEE 数值相等比较为假，包括与自身；使用 `isnan` 检查更清楚。+0 与 −0 相等，但在允许 IEEE 非陷阱除法结果的模式中，$1/(+0)=+\infty$、$1/(-0)=-\infty$。语言、硬件或配置可能对除零抛出异常，应把数值规则与执行环境区分。

自定义 16 位格式须重新给出 sign/exponent/fraction 位数、bias、隐含位和特殊码约定。课内补充的 1/4/11、bias 7 模型不等于 IEEE binary16 的 1/5/10、bias 15。已有折叠例子 s=1、E=9、F=512 按该自定义正规公式为 −5；不能套 binary32 的 bias 127。
''',
5: r'''
先修连接 [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|二进制位权]]、[[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组|小数转换与有限表示条件]]、[[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|位宽]]，以及 [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法|补码]]。Q 格式继承补码的负权和非对称范围；浮点符号独立、指数偏置，并非“整字都换为补码或偏移码”。两种表示都先约定格式再解释模式。

定点运算连接 [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确|中间宽度与移位规则]]；读原始浮点位串的大小连接 [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|比较器解释]]。
'''
}

ADD['Data Coding and Character Representation'] = {
1: r'''
### 编码目的决定合法集合与解码规则

字母数字编码 (alphanumeric code) 将字母、数字字符、标点或控制动作映射为位串；数值编码则定义位串到数值的映射。BCD 存**各十进制数字**，ASCII 存**字符符号**，Gray 选择**相邻顺序**。编码并不会自动带来纠错能力。

| 语义为“5”的不同对象 | 存储表示 | 使用前需确认 |
|---|---|---|
| 无符号数值 5 | 例如 8 位 `0000 0101` | 位宽与 unsigned |
| BCD 数字 5 | `0101` | 8421 数字组及其十进制位置 |
| ASCII 字符 `'5'` | 七位 `0110101`，字节为 `0x35` | 字符编码与容器宽度 |
| 自然 binary 值 5 的 reflected Gray 码 | 4 位 `0111` | Gray 对应关系及位宽 |

数制转换使同一数学值的基数写法改变；编码转换还要选择目标字段与合法集，例如 binary 13=`1101`、BCD 13=`0001 0011`、ASCII 字符串 `"13"` 为 `0x31 0x33`，三者不能共用一个整串位权读法。
''',
2: r'''
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
''',
3: r'''
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
''',
4: r'''
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
''',
5: r'''
先修是 [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型|位权与编码之别]]、[[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|十进制／二进制／hex]] 和 [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|位宽、nibble 与 byte]]。本篇内部可依 BCD→Gray→ASCII 对照“逐位十进制语义／相邻性／符号映射”。

应用连接 [[Seven-Segment Display and Code Conversion|BCD 显示]]、[[Karnaugh Map Minimization|Gray 排序的 K-map]]、[[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界|Gray 与异步传输条件]]、[[Keyboard Scanning and Encoding|键盘字符编码]]。检错连接 [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错|ASCII 外层奇偶位]] 和 [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数|CRC]]，别把相邻 Gray 性质当作检错保证。
'''
}

ADD['Parity and Cyclic Redundancy Checks'] = {
1: r'''
### 保护对象、协议条件与完整生成流程

**奇偶校验 (parity check)** 为 n 个数据位增加一个冗余位，使发送的 n+1 位中 1 的总数具有指定奇偶性。P 是检查值，不是新的信息数据位，但同样占带宽。接收的**数据位和校验位**都参与校验子 (syndrome) 计算。

设 $t=0$ 表示 even parity，$t=1$ 表示 odd parity；全部异或为 S，则统一的报错输出为 $E=S\oplus t$。E=1 表示奇偶约束被破坏；E=0 表示未检出错误。奇校验下原始 S=1 是合法，不能未经约定就称 S=1 为报错。

**六步操作。** 约定 n、even/odd、校验位位置和帧边界 → 数据异或（奇校验再取反）→ 按协议附上 P → 接收全组异或 → 比较目标 t → 用一位与两位翻转验证检错边界。数据 `1101001` 有四个 1，偶校验 P=0，奇校验 P=1；长字串可四位分段计数，例如 `1101 0111 0100` 为 $3+3+1=7$ 个 1。

**适用条件。** 收发分组和奇偶约定必须一致；发送 even、接收 odd 时，无错误帧会全部被拒绝。确定性检错结论只假设同长度组中的比特翻转，不要求各翻转统计独立；校验位翻转也在错误模型中。位插入／丢失、帧同步错误需要外层协议分析。

冗余占发送帧的比例为 $1/(n+1)$；以原数据为分母的附加开销为 $1/n$。7 数据位加 1 校验位分别为 12.5% 和约 14.29%；8 数据位时分别为约 11.11% 和 12.5%，需明确分母。较大分组减少这一比例，但并不自动改善保护；漏检率还取决于信道错误模型和保护长度。

**Exam English.** “Parity counts the parity of the entire protected word, including the parity bit. All odd-weight bit-flip patterns are detected; all nonzero even-weight patterns are undetected. A passing parity check does not prove that the data is correct.”
''',
2: r'''
### 两位、三位与四位电路及调试

| 受保护的数据位数 | 偶校验发生器 | 最少二输入 XOR 门数 | 接收检查 |
|---|---|---|---|
| 2 | $P=A\oplus B$ | 1 | $E=r_A\oplus r_B\oplus p_r$，2 门 |
| 3 | $P=A\oplus B\oplus C$ | 2 | 再 XOR 收到的 P，共 3 门 |
| 4 | $P=(A_0\oplus A_1)\oplus(A_2\oplus A_3)$ | 3，平衡结构 2 级 | 四数据位和 P，共 4 门，可 3 级 |

一般 n 位发生器需 n−1 个二输入 XOR，n+1 位检查器需 n 个；奇校验生成或统一 E 还需取反／常量异或（门的实际实现由库决定）。不能把“发生器用三门”直接抄成四位数据加 P 的检查器也三门。

**设计／验证步骤。** 明确 P 位与 E 的极性 → 写中间节点方程 → 数门和最长 XOR 级数 → 无错误输入检查 E=0 → 各位单独翻转检查 E=1 → 两位翻转得到 E=0 说明能力边界。发生器只取数据；检查器必须纳入收到的校验位。若正常帧全部报错，先检查 even/odd、极性、位序和分组定义，再查门连接。

E 只有一位，无法指出错误位置，不能自行“猜一位并修正”。增加二维行列校验或汉明码等冗余才可能在规定错误模型下定位纠错；两维校验也有矩形四角错误等盲区。Gray 改善指定相邻变化的编码，不改变 parity 的奇偶盲区。
''',
3: r'''
### 标准多项式定义、课件特例与逐步算法

**循环冗余校验 (cyclic redundancy check, CRC)** 把位串视为 GF(2) 上的多项式，生成码 (generator code) 是除数 G 的位串。次数 (degree) r 是最高非零项的指数，G 要用 r+1 位，标准余数／frame check sequence (FCS) 用 r 位；余数次数严格小于 r。

| 约定 | 数据 D | 生成码 G | 补零位数 | 余数栏 | 发送帧 |
|---|---|---|---|---|---|
| 标准三阶教学算法 | `11010011` | `1010`，$x^3+x$ | 3 | `010` | `11010011010` |
| 课件四位扩展演示 | `11010011` | 同上 | 4 | `0100`（三位余数 100 左补 0） | `110100110100` |
| 标准末项为 1 的例子 | `1101` | `1011`，$x^3+x+1$ | 3 | `001` | `1101001` |

标准算法默认 k=r；课件扩展将数据乘 $x^4$ 并用四位余数栏，虽然同样可令帧被 G 整除，也不等于一般标准 CRC 定义。若指定 k≥r，$R=[x^kD]\bmod G$ 可左补到 k 位填入低栏；收发必须沿用相同帧格式。**余数有效长度由 degree r 约束，不能说剩余 k 位都是任意校验信息。** G=`1010` 常数项为 0，不能套末项为 1 的完整突发检错保证。

**标准七步。** 检查 D、G、r 和参数 → 在 D 后补 r 个 0 → 找当前最高位 1 → 将 G 对齐并逐位 XOR，消掉最高位 → 重复至余数 degree<r → 左补到 r 位并附在原 D 后 → 接收端除包含 CRC 的整帧，检查规定 residue。无初值／反射／final XOR 的课内模型 residue=0；实际协议可能指定非零 residue，需按完整定义实现。

模 2 的每个系数独立加减，所以 $1\oplus1=0$，无整数 carry 或 borrow；`1101 XOR 1010=0111`，不等于整数差 `0011`。普通 additive checksum 是带进位的算术累加，CRC 是位置敏感的多项式余数，不能互称同一算法。

**协议前提。** 除 G，还要一致约定位序、保护帧范围、initial value、是否反射 (reflection)、补零和 final XOR。仅说 CRC-32 或指定“32位”并不足以唯一确定协议。CRC 可用于随机传输／存储错误检测，不是加密、认证或防恶意篡改；公开算法允许修改数据后重算校验。

**Exam English.** “For a degree-$r$ generator, append $r$ zeros, perform modulo-two division, and append the $r$-bit remainder. At the receiver, divide the entire codeword. The zero-remainder test belongs to the specified zero-initialized textbook model.”
''',
4: r'''
### 检错保证的精确条件

接收码字为 $C(x)+E(x)$，其中 E 是非零错误多项式、系数为翻转位置。在线性、零初值教学模型中，syndrome 为 $E\bmod G$，因此**漏检当且仅当 $G\mid E$**，独立于具体数据内容。

| 错误类别 | 充分检测条件 | 不能省略的限制 |
|---|---|---|
| 单比特 $E=x^i$ | 非常数 G 且常数项 1 | 课件 G=`1010` 的单比特也能检出，但不能由末项 0 推出一般标准保证 |
| 所有奇数重错误 | $(x+1)\mid G$ | 奇数重 E 满足 $E(1)=1$；不是所有 CRC 都具有该因子 |
| 长度 $L\le r$ 的非零突发 | degree r、G 首末系数 1 | burst 长度是首末错误位间跨度（包括中间未错的位），不是错误位个数 |
| 双比特 $E=x^j(x^k+1)$ | 在允许帧长内对所有位差 k 有 $G\nmid(x^k+1)$ | 取决于 G 和最大帧长，不应称所有 CRC 全检双错 |

“CRC 比 parity 强”是设计目标和规定条件下的比较，不代表任意生成式、任意帧长、任意错误模式都严格更强。parity 检出全部奇数重；若 CRC 缺少 $x+1$ 因子，某些奇数重也可漏检。折叠穷举表仅针对 12 位帧和 G=`1010`，其比例不是通用概率；要转成概率还必须指定错误模式的分布。

**调试与边界检查。** 合法整帧先验算 residue → 枚举单错验证声明 → 取可放入帧中的 $E=Gx^j$ 构造明确漏检例 → 对短 burst 检验 G 的常数项条件 → 核对串行反馈模型求的确实是同一个生成式。已保留四级网络使用 $H=xG=x^4+x^2$，三位余数模型使用 G 本身，不能互换。

CRC 报非零余数只表示约束被破坏；不提供一般错误定位／纠错规则，也不能把余数零称作“确认正确”。恢复可由外层重传或纠错码完成。
''',
5: r'''
先修连接 [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|bit 与字节]]、[[Data Coding and Character Representation#4 · American Standard Code for Information Interchange · 字符编码|七位 ASCII]] 和 [[Logic Gates and Boolean Functions|XOR 逻辑]]；比较 [[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束|Gray 的相邻变化目标]] 与本篇的已发生错误检测。

从低开销 parity 转入 CRC，是从一个奇偶约束到多项式余数约束；都需要明确保护长度、冗余位与未检出边界。串行 CRC 连接 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|移位寄存器]]、[[Sequential Logic and Flip-Flops|触发器状态]] 和 [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|独立多项式参照验证]]。二维校验、汉明码和 ARQ 为扩展方向，不能自动作为 CRC 自身能力。
'''
}

CORRECTIONS = {
 'Number Systems and Base Conversion': [
  (r'$$x=\sum_{i=-m}^{n}a_iR^i,\qquad R\ge2,\quad0\le a_i<R.$$', r'$$x=\sum_{i=-m}^{n-1}a_iR^i,\qquad R\in\mathbb Z,\ R\ge2,\quad a_i\in\{0,\ldots,R-1\}.$$'),
  ('**没有下标就没有数值**。三位数字完全一样', '**没有基数约定就不能唯一确定值**。四位数字完全一样'),
  ('三个结果的数量级都低于各自的最高位权（$16$、$8^{4}=4096$、$16^{4}=65536$）', '三个结果都低于四位整数的上界（$2^4=16$、$8^4=4096$、$16^4=65536$）'),
  ('图 1 里的虚线柱', '图 1 里的虚线柱'),
  ('它正好是 1 K', '它恰好是 $2^{10}$，作为数量倍率是 1 Ki（不是 SI 的 1 k）'),
  ('唯一的例外是 `0111 -> 1000`，它一次翻了全部四位', '例如 `0111 -> 1000` 一次翻全部四位；其他进位边界也可能翻多位'),
  ('（讲义 p.25 的 kilo/mega/giga/tera/peta/exa）', '（讲义 p.25 使用的数量级标签；精确二进制前缀为 kibi/mebi/gibi/tebi/pebi/exbi）'),
  ('这是估算一切存储容量的唯一工具', '这是估算存储容量的方便工具'),
  ('| 名称 (SI 词头) | 幂 | 精确值 | 近似 |', '| 二进制词头（IEC） | 幂 | 精确倍率 | 对应十进制数量级 |'),
  ('| kilo | $2^{10}$', '| kibi (Ki) | $2^{10}$'),
  ('| mega | $2^{20}$', '| mebi (Mi) | $2^{20}$'),
  ('| giga | $2^{30}$', '| gibi (Gi) | $2^{30}$'),
  ('| tera | $2^{40}$', '| tebi (Ti) | $2^{40}$'),
  ('| peta | $2^{50}$', '| pebi (Pi) | $2^{50}$'),
  ('| exa | $2^{60}$', '| exbi (Ei) | $2^{60}$'),
  ('每个刻度给出幂、SI 词头、精确十进制值与对应的 IEC 前缀', '每个刻度给出二进制幂、精确十进制值与 IEC 前缀；图中旧式 kilo/mega 等标注只用作近似数量级，严格 SI 倍率见正文表'),
  ('的全部原因（**不是厂商偷工减料，是两套词头混用**）', '的单位换算原因；实际可用空间还可能受格式化、分区和系统保留空间影响'),
  ('**32 位地址空间 $=2^{32}$ 字节 $=4$ GiB**', '**32 位按字节寻址的地址空间 $=2^{32}$ 字节 $=4$ GiB**'),
  ('32 位地址空间有多大？', '32 位按字节寻址的地址空间有多大？'),
  ('32 位地址空间 $=2^{32}$ 字节', '32 位按字节寻址的地址空间 $=2^{32}$ 字节'),
 ],
 'Binary Arithmetic and Signed Representation': [
  ('所以“反复相减、数相减次数”与“长除法”给出同一个商，只是前者在二进制里每一步只减一次。', '反复相减计成功减法次数，逐位长除计商位，二者给出同商同余数但运行组织不同。'),
  ('所以"反复相减、数相减次数"与"长除法"给出同一个商，只是前者在二进制里每一步只减一次。', '反复相减计成功减法次数，逐位长除计商位，二者给出同商同余数但运行组织不同。'),
  ('| 逐位和 | $1$（并产生向 $2^{4}$ 的进位 $1$） | $0$ | $0$ | $0$ |', '| 四位保留和 | $0$（另有向 $2^4$ 的进位 1） | $1$ | $0$ | $0$ |'),
  ('| 结果 | $1$ | $0$ | $1$ | $0$ |', '| 完整五位结果 | 最高列外进位 1；本列 0 | $1$ | $0$ | $0$ |'),
  ('得到的是两个幅值之和的两倍', '得到的是把符号字段也按正位权计入的无符号和（本例 $8+6+6=20$）'),
  ('**一次加法要比较三次**，这就是原码被淘汰的原因。', '这需要额外的符号判断、幅值比较和加减选择，解释了其普通整字算术不如补码直接。'),
  ('判零电路要写成 `(code == 0000) or (code == 1000)`，而不是一次比较；', '判零可比较码字 `0000` / `1000`，更简洁地只检查幅值位是否全零；'),
  ('原码 = **"能读不能算"**。', '原码 = **独立符号与幅值，算术须专用处理**。'),
  ('有进位** → 结果为正', '有进位** → 在本例异号相加时结果非负'),
  ('两条进位规则都被本例验证：有进位 → 正，无进位 → 负', '本例恰有一正一负：有进位 → 和非负，无进位 → 和为负；不作一般 signed overflow 判据'),
  ('另一路核对：`1111 1110` 取反加 1 → `0000 0001` $+1$ 的前一步 `0000 0001`，即 `0000 0010` $=2$', '另一路核对：`1111 1110` 先取反得 `0000 0001`，再加 1 得 `0000 0010` $=2$'),
  ('最高位的权值变成 $+2^7$，', '原 4 位 MSB 在 8 位零扩展后成为普通的 $+2^3$ 位，而新 bit 7 为 0，'),
  ('1. **修正项法**：先按无符号算出 $\\sum b_iA2^i$，再减去最高位那一行的"错算量"（在 $2n$ 位宽度下表现为丢弃最高进位）；', '1. **显式修正项法**：先以有符号 A 计算 $\\sum_{i=0}^{n-1}b_iA2^i$，再减 $b_{n-1}A2^n$；该修正不能靠丢弃最高进位替代。'),
  ('2. **符号扩展法**（硬件常用）：把每个部分积**符号扩展**到 $2n$ 位后再相加 —— 符号位的负权值被自动带上，', '2. **负权部分积法**：先将 A 符号扩展到 $2n$ 位再移位；低 $n-1$ 行相加，最高行必须条件相减，'),
  ('不需要显式减法。**手算推荐这一种**。', '等价硬件也可对负权行取反加一并相加。只做符号扩展不够。'),
  ('**每一行都比上一行多一个前导符号位**；符号位那一行照常参与相加，', '**所有部分积在 $2n$ 位宽中保持正确符号**；乘数符号位那一行以负权参与，'),
  ('**Example 1 — 4 位乘法 $1011_2\\times1101_2$**', '**Example 1 — 4 位无符号幅值乘法 $1011_2\\times1101_2$**'),
  ('若某一步减完变负（多减了一次），', '上述先比较的算法不会减成负；若改用先试减后判号的算法，失败时'),
  ('$4897<2^{13}=8192$，需要 $13$ 位幅值位 + $1$ 位符号 = $14$ 位：', '$4897$ 的普通二进制需要 13 位，但作为正补码需额外符号位，故用 14 位：'),
 ],
 'Fixed-Point and Floating-Point Numbers': [
  ('同样的位宽，浮点用阶码买到约 $76.5$ 个数量级的范围', '此处比较的是 32 位 binary32 和 8 位 U4.4，不是相同位宽；binary32 正规幅值覆盖约 $76.5$ 个数量级'),
  ('浮点单精度的动态范围约为 U4.4 的 **32 倍**', '覆盖的十进制数量级数约为 U4.4 的 **32 倍**；幅值上限／下限之比本身不只是 32 倍'),
  ('下方红色窄条是 Q4.4 这类定点，只有', '下方红色窄条的数值区间对应 U4.4 的非零幅值，约有'),
  ('最左端是 $0$（阶码全 0），越出 $3.40\\times10^{38}$ 后阶码字段饱和为全 1，进入 $\\pm\\infty$/NaN。', '对数轴不包含零；指数全 0 还包括次正规数。大数 overflow 的结果由舍入模式决定，NaN 则用于无效运算等情况。'),
  ('**相对精度恒定、绝对精度浮动**', '**相对分辨率数量级近似固定、绝对分辨率随指数变化**'),
  ('$1.0$ 附近最小间隔是 $2^{-23}$', '$1.0$ 及其上方正规区间的相邻间隔是 $2^{-23}$（下方区间间隔为 $2^{-24}$）'),
 ],
 'Data Coding and Character Representation': [
  ('每一组独立判定、独立修正；某组 $+0110$ 之后新产生的进位，要送到**左边相邻的那一组**', '每一组独立判定、独立修正；该组的十进制进位（初始二进制 carry 或校正阶段 carry）送到**左边相邻的那一组**'),
 ],
 'Parity and Cyclic Redundancy Checks': [
  ('**0（进位被丢弃）**', '**0（GF(2) 的系数相加，不存在整数进位）**'),
  ('CRC 每一列都不低于它。', '本表所用 G 与帧长下，CRC 各栏检出数均不低于 parity；不能推广到任意 G。'),
 ]
}

# Explicitly retained original subsections use their canonical source callout.
# Missing definitions, conditions, methods, pitfalls and connections are fused
# into the visible thematic explanations above rather than pasted as 18 notes.
source_position = {
 'Number Systems':1, 'Decimal Number System':2, 'Binary Number System':2,
 'Octal Number System':2, 'Hexadecimal Number System':2, 'Number Base Conversion':3,
 'Bits and Bytes':4, 'Binary Arithmetic':1, 'Sign-Magnitude Representation':2,
 "Two's Complement Representation":3, 'Signed Binary Multiplication and Division':4,
 'Fixed-Point Numbers':1, 'Floating-Point Numbers':3, 'Binary Coded Decimal':2,
 'Gray Code':3, 'American Standard Code for Information Interchange':4,
 'Parity Bit':1, 'Cyclic Redundancy Check':3,
}

CORRECTED_RESTORED = {
 'Decimal Number System': {'Core Definition':'无下标1011不能默认属于二进制。','Assumptions':'1/3在十进制和二进制都循环；有限表示按既约分母判定。'},
 'Octal Number System': {'Core Definition':'Python 3八进制整数用0o前缀。','Assumptions':'八进制与十六进制可经二进制重新分组。'},
 'Hexadecimal Number System': {'Assumptions':'十六进制可写小数；整数/小数从点向两侧分组。','Method':'前导零是否必须保留由固定位宽要求决定。','Pitfalls':'完整对齐组左右切分一致；关键是最低位及点对齐。'},
 'Number Base Conversion': {'Core Definition':'经过十进制是可选核算路线。','Method':'一般目标进制的最大幂法可取0至S−1数码；小数按独立算法。'},
 'Bits and Bytes': {'Assumptions':'物理模式数始终2^N；完整Gray编码不浪费码字。','Method':'模式数与unsigned/dense编码条件区分。','Pitfalls':'MB按10^6、MiB按2^20，容量精确计算不能混用。'},
 'Binary Arithmetic': {'Core Definition':'反复相减计商数值，逐位长除计商位。','Assumptions':'固定宽度取模适用于加减/截短乘法，不能统称除法。','Method':'乘法缩宽查高位，不使用单一末次carry判所有运算。'},
 "Two's Complement Representation": {'Assumptions':'signed overflow、stored sign和unsigned carry不同；完整乘除不自动与unsigned相同。','Method':'最小负数用负权或u−2^N解码；明确取负例外。'},
 'Signed Binary Multiplication and Division': {'Core Definition':'停止条件为余数小于除数，失败试减需恢复且不能计商。','Method':'直接补码乘法先扩展、再移位，乘数MSB行按负权；不二次定符号。'},
 'Fixed-Point Numbers': {'Assumptions':'回绕、饱和、报错依规范选择；Q1.15上限不含+1。','Method':'先按指定规则量化，再检查整数代码范围；负代码不重复取反。'},
 'Floating-Point Numbers': {'Method':'先检查特殊字段；长fraction需舍入，舍入进位可改指数。','Pitfalls':'ULP、NaN与除零结果须带格式/舍入/异常前提。'},
 'Binary Coded Decimal': {'Method':'十进制进位需保留第一阶段carry，不能只取校正后新carry。','Pitfalls':'完整已对齐字段的分组方向不改变各组，不能泛称从左切必错。'},
 'Gray Code': {'Core Definition':'reflected Gray可首尾相邻，但不是所有cyclic code的同义词。','Assumptions':'码字在规定对应关系下完整表达数值，不能普通位权读并非没有信息。'},
 'American Standard Code for Information Interchange': {'Assumptions':'基本ASCII、单字节代码页和多字节编码区分。','Method':'字符数等于字节数限定纯ASCII；算术转换带字符块检查。'},
 'Parity Bit': {'Assumptions':'确定性翻转检错不要求独立；冗余开销说明分母。','Pitfalls':'Gray影响指定相邻变化/符号误判，不能保证减少所有错误概率。'},
 'Cyclic Redundancy Check': {'Core Definition':'标准r位定义与课件四位扩展例分开。','Method':'按degree补零取余；实际协议residue和参数须完整指定。'},
}

def canonicalize(text):
    def change(match):
        embed, body = match.group(1), match.group(2)
        base, sep, alias = body.partition('|')
        name, anchor_sep, anchor = base.partition('#')
        name = name.removesuffix('.md')
        entry = links.get(name)
        if embed or not entry or entry['target'] == name:
            return match.group(0)
        target = entry['target'] + '#' + entry['heading']
        return '[[' + target + '|' + (alias if sep else name) + ']]'
    return re.sub(r'(!?)\[\[([^\]]+)\]\]', change, text)

coverage = {'chapter':'Ch2', 'sources':[], 'verification':{}}
for group in [g for g in mapping['groups'] if g['chapter'] == 'Ch2']:
    target = group['target']
    text = (ROOT / 'Notes' / (target+'.md')).read_text(encoding='utf-8-sig')
    corrections = []
    for old, new in CORRECTIONS[target]:
        if old in text and old != new:
            text = text.replace(old,new)
            corrections.append({'before':old,'after':new})
    headings = re.findall(r'^## ([^\n]+)', text, re.M)
    thematic = headings[:5]
    # Place new visible material immediately before the existing fold, so the
    # original derivations, code, equations, examples and illustrations remain.
    for position in sorted(ADD[target], reverse=True):
        heading = thematic[position-1]
        start = text.index('## '+heading)
        next_heading = text.find('\n## ',start+4)
        if next_heading < 0:
            next_heading=len(text)
        fold = text.find('\n> [!example]-', start, next_heading)
        insertion = fold if fold >= 0 else next_heading
        text=text[:insertion].rstrip()+'\n\n'+ADD[target][position].strip()+'\n\n'+text[insertion:].lstrip('\n')
    text=canonicalize(text)
    (OUT/(target+'.md')).write_text(text.rstrip()+'\n',encoding='utf-8')
    for source in group['sources']:
        old = (ROOT / '.scratch/consolidation-20261008/original-Notes' / (source+'.md')).read_text(encoding='utf-8-sig')
        entries=[]
        current_parent=''
        original_headings=list(re.finditer(r'^(#{2,3}) ([^\n]+)',old,re.M))
        for index,h in enumerate(original_headings):
            level=len(h[1]); title=h[2]
            if level==2: current_parent=title
            pos=source_position[source]
            if title.startswith('Connections'): pos=5
            if title.startswith('Gate-Level') or (current_parent.startswith('Gate-Level') and level==3):pos=2
            if title.startswith('Sources'): section='Sources · 课件依据'
            else: section=thematic[pos-1]
            restore=level==2 and title.startswith(('Core Definition','Assumptions','Method','Pitfalls','Connections'))
            next_same_or_higher=next((hh.start() for hh in original_headings[index+1:] if len(hh[1])<=level),len(old))
            original_body=old[h.start():next_same_or_higher]
            text_corrections=[c['after'] for c in corrections if c['before'] in original_body]
            correction_note=next((reason for prefix,reason in CORRECTED_RESTORED.get(source,{}).items() if title.startswith(prefix)),None)
            corrected=bool(text_corrections or correction_note)
            status='corrected' if corrected else ('restored' if restore else 'covered')
            location=target+'#'+section
            details='恢复并融合到可见正文的定义、条件、步骤、误区或语义连接。' if restore else '原小节的独有内容保留在对应来源的折叠推导／例题中；正文新增简明方法和边界。'
            if source=='Parity Bit' and current_parent.startswith('Gate-Level'):
                details='两位／三位发生器、四位平衡树和五位检查器原门级推导及图示均保留，正文补门数和验证步骤。'
            if title.startswith('Sources'): details='原来源合并到文末 Ch2 与 Ch5 的课件依据。'
            visible_subheads=re.findall(r'^### (.+)',ADD[target][pos],re.M) if pos in ADD[target] else []
            entries.append({'original_heading':title,'original_level':level,'status':status,'restored':restore,'covered':not restore,'corrected':corrected,'correction_note':correction_note,'text_corrections':text_corrections,'target_section':location,'target_subsection':visible_subheads[0] if restore and visible_subheads else None,'coverage':details,'omitted':False})
        assets=re.findall(r'!\[\[([^\]]+)\]\]',old)
        missing_assets=[a for a in assets if '![[%s]]'%a not in text]
        coverage['sources'].append({'original_note':source,'target_note':target,'sections':entries,'original_assets':assets,'missing_assets':missing_assets})
    coverage['verification'][target]={'bytes':len(text.encode('utf-8')),'new_visible_sections':len(ADD[target]),'existing_corrections':corrections,'original_note_count':len(group['sources'])}

(BASE/'coverage-ch2.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'drafts':len(ADD),'sources':len(coverage['sources']),'sections':sum(len(s['sections']) for s in coverage['sources']),'missing_assets':sum(len(s['missing_assets']) for s in coverage['sources'])},ensure_ascii=False))
