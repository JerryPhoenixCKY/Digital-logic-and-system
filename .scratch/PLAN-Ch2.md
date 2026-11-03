# ECE2050 第二章「Number Systems」笔记库建设规划 (BUILD PLAN) — 冻结版

> 本文件是 **唯一权威清单**（canonical registry）。所有笔记的文件名、别名、标签、图文件名、
> 双链目标都必须与本文件一致。进度不在此文件追踪，进度由 `Notes/ECE2050 Knowledge Tree.md`
> 的 ✅ 表示（该文件即知识树，双链统一写作 `[[ECE2050 Knowledge Tree]]`）。
>
> 写作规范见 `.scratch/NOTE_SPEC.md`（必须遵守）；视觉规范见 `Tools/README.md`。
> **固定布局**：全部 Markdown（含知识树与术语表 `Notes/Glossary.md`）都在 `Notes/` 下 —— 这是作者
> 确认保留的约定，不要搬到库根目录。

素材来源：
- 讲义：`.scratch/extract/ECE2050-Chap2.txt`（ECE2050-Chap2.pdf，73 页，页序 = 页脚号）
- 课程大纲：`.scratch/extract/ECE2050-Course-Outline.txt`（章节范围 Ch1–Ch11）
- 数字校验报告：`.scratch/verify_ch2.txt`（**例题数字以此为准**）
- 原 PDF（只读，**不要**截图）：库根目录 `ECE2050-Chap2.pdf`；历年题在 `LGU_HUB_ECE2050/`

---

## 0. 命名与标签约定

- 文件名 = **英文全称**，放在 `Notes/` 下（知识树 `Notes/ECE2050 Knowledge Tree.md` 与术语表
  `Notes/Glossary.md` 也在这个目录，属固定约定）。
- `aliases` 至少三条：**中文名 + 英文全名 + 英文缩写**；无缩写时给同义英文名或常见中文别称。
- `tags` 固定为 `ECE2050` + 一个分区标签，取值仅限：
  `number-foundations` / `number-bases` / `number-conversion` / `binary-data` /
  `binary-arithmetic` / `signed-numbers` / `fractional-numbers` / `codes` / `error-codes`。
- `date: 2026-09-16`
- 图放 `Figures/`，渲染脚本放 `Tools/figures/`，两者**同名**（`xxx.svg` ↔ `xxx.py`）。

### 双链白名单（**只能**链接以下名字，其它一律纯文本）

```
Number Systems | Decimal Number System | Binary Number System | Octal Number System |
Hexadecimal Number System | Number Base Conversion | Bits and Bytes | Binary Arithmetic |
Sign-Magnitude Representation | Two's Complement Representation |
Signed Binary Multiplication and Division | Fixed-Point Numbers | Floating-Point Numbers |
Binary Coded Decimal | Gray Code | American Standard Code for Information Interchange |
Parity Bit | Cyclic Redundancy Check | Knowledge Tree | Glossary
```

### 分区一览（Knowledge Tree 的分区顺序）

| 分区 | 标签 | 笔记 |
|---|---|---|
| 1 · Foundations | `number-foundations` | N01 |
| 2 · Number Bases | `number-bases` | N02 N03 N04 N05 |
| 3 · Conversion | `number-conversion` | N06 |
| 4 · Bits and Scale | `binary-data` | N07 |
| 5 · Binary Arithmetic | `binary-arithmetic` | N08 |
| 6 · Signed Numbers ❗ | `signed-numbers` | N09 N10 N11 |
| 7 · Fractional Numbers | `fractional-numbers` | N12 N13 |
| 8 · Codes | `codes` | N14 N15 N16 |
| 9 · Error Detection Codes | `error-codes` | N17 N18 |

---

## 分区 1 · Foundations（源：p.3, 5, 6, 48, 50, 64）

### N01 | Number Systems
- file: `Notes/Number Systems.md`
- aliases: `数制` / `数制系统` / `记数制` / `Number Systems` / `Number System`
- tags: `ECE2050`, `number-foundations`
- must-cover: 数制 = 书写数字的体系（a system of writing to express numbers）；日常的 base-10/12/60、
  计算机的 base-2/8/16（p.3）；**Base-R 三要素**：base $R\ge 2$、digit $\in[0,R-1]$、weight $R^i$（p.5）；
  通式 $(N)_R=\sum_i a_iR^i$ 含整数与小数位（$i$ 从 $n-1$ 到 $-m$）；小数点/二进制点 (radix point) 的含义；
  p.6 的关键提醒：*decimal numbers mean any base-10 numbers, not just those with a decimal point*；
  **positional/weighted** vs **non-positional/non-weighted**（p.64，例子 gray code / cyclic code，链 [[Gray Code]]）；
  四种常用进制对照表（base / digits / weight / 典型用途）；
  同一串数字在不同 base 下意义不同 → 必须写下标 $_2$/$_8$/$_{16}$ 消歧；
  章节级**范围对照表**（N 位下 unsigned / sign-magnitude / two's complement 的 range，N=4/8/16/32），
  作为全章导航（链向 N07 N09 N10）。
- 图: `positional-weights.svg`（matplotlib，双面板：(a) $(568.23)_{10}$ 的位权展开柱状/分层图，
  逐位写 $5\times10^2$ 等；(b) $(10.101)_2$ 的位权展开，突出 $2^{-1},2^{-2},2^{-3}$ 与 $2.625$）
- 例题: ① 把 $(568.23)_{10}$ 按位权展开求值和（讲义 p.6）；② 判断 $1011$ 在 base-2/8/16 下的值（$11$ / $521$ / $4113$，已用 Python 复核；$(1011)_{16}=4096+16+1$）。
- 链接: `[[Decimal Number System]]`、`[[Binary Number System]]`、`[[Octal Number System]]`、
  `[[Hexadecimal Number System]]`、`[[Number Base Conversion]]`、`[[Gray Code]]`、`[[Two's Complement Representation]]`
- 注意: 本篇是全章入口，只给"框架 + 对照表"，具体进制细节交给下游四篇，不要重复展开。

---

## 分区 2 · Number Bases（源：p.4, 6–9, 15–22）

### N02 | Decimal Number System
- file: `Notes/Decimal Number System.md`
- aliases: `十进制` / `十进制数制` / `Decimal` / `Decimal Number System` / `Base-10`
- tags: `ECE2050`, `number-bases`
- must-cover: base 10、digit 0–9、weight $\dots10^2\,10^1\,10^0\,.\,10^{-1}\,10^{-2}\dots$（p.6）；
  "decimal number" 指的是 base-10（不是"带小数点的数"）；$(568.23)_{10}$ 的完整展开与求和校验；
  整数部分与小数部分 (fractional numbers) 的分界（decimal point）；
  为什么人类用十进制（十指的历史约定，不是数学必然）→ 计算机用二进制（链 [[Binary Number System]]）；
  十进制是**人机接口语言**：输入/输出转换的代价（链 [[Number Base Conversion]]、[[Binary Coded Decimal]]）。
- 图: 复用 `positional-weights.svg`（与 N01 同一张，图注从 base-10 角度写）
- 例题: ① $(568.23)_{10}$ 展开（p.6）；② 用"除以 10 取余"把 $(568)_{10}$ 写成 $5\times10^2+6\times10+8$，
  说明该算法与十进制记法自洽（数值校验：$500+60+8=568$ ✓）。
- 链接: `[[Number Systems]]`、`[[Binary Number System]]`、`[[Number Base Conversion]]`、`[[Binary Coded Decimal]]`

### N03 | Binary Number System
- file: `Notes/Binary Number System.md`
- aliases: `二进制` / `二进制数制` / `Binary` / `Binary Number System` / `Base-2`
- tags: `ECE2050`, `number-bases`
- must-cover: base 2、digit 0/1、weight $\dots2^2\,2^1\,2^0\,.\,2^{-1}\,2^{-2}\dots$（p.7）；
  binary point；$(10.101)_2=(2.625)_{10}$ 逐步展开；**powers of two 表** $2^0$–$2^{10}$（p.8，标出"值得背"）；
  counting in binary 0–15（p.9）；为什么计算机用二进制（p.21–22：二值物理器件——开关/晶体管导通与截止、
  抗噪声裕度大、布尔逻辑直接映射；链 [[Bits and Bytes]]）；
  二进制太长 → 用 8/16 进制压缩（p.22，链 [[Octal Number System]]、[[Hexadecimal Number System]]）。
- 图: `binary-powers-and-counting.svg`（matplotlib，双面板：(a) $2^0$–$2^{10}$ 的位权与十进制值；
  (b) 4 位二进制 0→15 的计数序列，标注哪一位在翻、翻多快）
- 例题: ① $(10011)_2=19$（p.10）；② $(10.101)_2=2.625$（p.7）；③ 计数题：从 $1011_2$ 开始数 5 个数（课后自测）。
- 链接: `[[Number Systems]]`、`[[Number Base Conversion]]`、`[[Bits and Bytes]]`、
  `[[Octal Number System]]`、`[[Hexadecimal Number System]]`、`[[Binary Arithmetic]]`

### N04 | Octal Number System
- file: `Notes/Octal Number System.md`
- aliases: `八进制` / `八进制数制` / `Octal` / `Octal Number System` / `Base-8`
- tags: `ECE2050`, `number-bases`
- must-cover: base 8、digit 0–7、weight（p.15）；$(2374)_8=(1276)_{10}$ 逐步展开；
  十进制→八进制：**反复除以 8，首个余数是 LSD**（p.17，$359_{10}=547_8$）；
  八进制↔二进制：1 个八进制位 = **3 bit**（p.19–20，$7526_8=111\,101\,010\,110_2$，
  $100110011010_2=4632_8$，从右往左分组、左侧补 0）；
  为什么存在八进制（p.22：压缩二进制；历史与 Unix）；**Linux 文件权限 rwx = 0–7**（$644\to rw\text{-}r\text{-}\text{-}$、
  $755\to rwxr\text{-}xr\text{-}x$）；C/Java 的 `0` 前缀字面量。
- 图: `linux-file-permissions.svg`（matplotlib：三位一组 rwx ↔ 八进制数字映射表 +
  `644`/`755`/`754` 三个实例的位图与含义）
- 例题: ① $359_{10}\to 547_8$（p.17）；② $7526_8\to$ 二进制（p.19）；③ `chmod 754` 展开成 rwx 串并说明含义（数值校验：$7+5+4$ 的位权 $4/2/1$）。
- 链接: `[[Number Base Conversion]]`、`[[Binary Number System]]`、`[[Hexadecimal Number System]]`、`[[Bits and Bytes]]`

### N05 | Hexadecimal Number System
- file: `Notes/Hexadecimal Number System.md`
- aliases: `十六进制` / `Hexadecimal` / `Hex` / `Hexadecimal Number System` / `Base-16`
- tags: `ECE2050`, `number-bases`
- must-cover: base 16、digit `0-9 A-F`（A=10 … F=15，**6 个字母字符**，p.16 的 T/F 题会考）、weight；
  $(E5)_{16}=(229)_{10}$ 展开；十进制→十六进制（反复除以 16，$650_{10}=28A_{16}$，p.18）；
  十六进制↔二进制：1 个十六进制位 = **4 bit = 1 nibble**（p.19–20，$CF8E_{16}=1100\,1111\,1000\,1110_2$，
  $1100101001010111_2=CA57_{16}$）；
  1 byte = 2 个十六进制位（$00$–$FF$）；**内存地址 / 内存转储**、`0x` 前缀、颜色码 `#RRGGBB`；
  十六进制与 ASCII 的关系（链 [[American Standard Code for Information Interchange]]）。
- 图: `hex-memory-address.svg`（matplotlib：一段按字节寻址的内存视图，地址 $0x0000,0x0001,\dots$ +
  每字节两个十六进制位拆成两个 nibble，标出 MSB/LSB）
- 例题: ① $650_{10}\to 28A_{16}$（p.18）；② $CF8E_{16}\to$ 二进制（p.19）；
  ③ 把一段 8 字节数据写成十六进制地址表并说明最后一字节地址（用 base+R 计算校验）。
- 链接: `[[Number Base Conversion]]`、`[[Binary Number System]]`、`[[Octal Number System]]`、
  `[[Bits and Bytes]]`、`[[American Standard Code for Information Interchange]]`

---

## 分区 3 · Conversion（源：p.10–13, 17–20）

### N06 | Number Base Conversion
- file: `Notes/Number Base Conversion.md`
- aliases: `数制转换` / `进制转换` / `Number Base Conversion` / `Base Conversion` / `Radix Conversion`
- tags: `ECE2050`, `number-conversion`
- must-cover: 四个方向的完整算法与适用条件：
  ① **base-R → decimal**：按位权求和（$10011_2=19$，$(2374)_8=1276$，$(E5)_{16}=229$）；
  ② **decimal → base-R**：法一"找最大 $R$ 的幂相减"（$53\to110101_2$，p.12），
     法二"反复除以 $R$，余数依次是下一位（**先得 LSB**）"（$53\to110101$、$359\to547_8$、$650\to28A_{16}$）；
  ③ **base-$R^k$ ↔ binary**：整体分组（八进制 3 bit、十六进制 4 bit），**从右往左**，最左不足补 0；
  ④ 一般 base-$R$ → base-$S$：以十进制为中枢（pivot）；
  延伸（讲义未展开但必须会）：**小数部分**用"反复乘 $R$ 取整数位"（$0.625\to.101_2$），说明为什么可能不终止。
  进制的**歧义与下标约定**；常见错误：把余数顺序写反。
- 图: `base-conversion-grouping.svg`（matplotlib：同一串二进制 $1100101001010111$ 上叠加 3-bit / 4-bit
  分组框，分别读出 $145\,127_8$ 与 $CA57_{16}$，说明"分组即转换"；
  注意 $1100\,1010\,0101\,0111$ 的正确分组是 $001|100|101|001|010|111$，漏补最左的 0 会读出错误的 $145\,227_8$）
- Mermaid: 决策流程图（源/目标各是什么 → 走哪条算法）
- 例题: ① $53_{10}\to$ 二进制（两种方法都要写，p.12）；② $359_{10}\to$ 八进制（p.17）；
  ③ 小数 $0.6875_{10}\to$ 二进制（自算复核）；④ 混合：$(1101\,0110)_2\to$ 十进制、八进制、十六进制（三路复核）。
- 链接: `[[Number Systems]]`、`[[Decimal Number System]]`、`[[Binary Number System]]`、
  `[[Octal Number System]]`、`[[Hexadecimal Number System]]`、`[[Bits and Bytes]]`

---

## 分区 4 · Bits and Scale（源：p.13, 21–26, 48）

### N07 | Bits and Bytes
- file: `Notes/Bits and Bytes.md`
- aliases: `位与字节` / `比特与字节` / `位/字节/半字节` / `Bits and Bytes` / `Bit and Byte`
- tags: `ECE2050`, `binary-data`
- must-cover: **bit**（1 个二进制位）、**nibble**（4 bit → 16 个值，$[0,15]$）、**byte**（8 bit → 256 个值，$[0,255]$）；
  1 hex digit = 4 bit = 1 nibble、2 hex digits = 1 byte（p.24 填空三连）；MSB 在左、LSB 在右；
  N 位的**容量 $2^N$ 与范围 $[0,2^N-1]$**（p.13，十进制类比 $10^N$）；
  word/halfword/doubleword 术语（超出讲义，标注为约定术语）；
  **大幂次**（p.25）：$2^{10}\approx10^3$ kilo、$2^{20}\approx10^6$ mega、$2^{30}\approx10^9$ giga、
  $2^{40}$ tera、$2^{50}$ peta、$2^{60}$ exa，给出精确值 $1024$、$1\,048\,576$、$1\,073\,741\,824$；
  IEC 前缀 KiB/MiB/GiB（1024）与 SI 前缀 kB/MB/GB（1000）的差别（硬盘标称容量"缩水"的原因）；
  **估算**（p.26）：$2^{24}=16\times2^{20}\approx$ 16 million、$2^{32}\approx$ 4 billion，
  进而 32 位无符号整数范围 $[0,4\,294\,967\,295]$、32 位地址空间 $4$ GiB。
- 图: `powers-of-two-scale.svg`（matplotlib：对数横轴上标出 $2^{10}$–$2^{60}$ 的位置与
  kilo/mega/giga/tera/peta/exa 名称、精确十进制值，并标出 $2^{24}$、$2^{32}$ 两个估算点）
- 例题: ① 8 bit / 4 bit 的容量与范围（p.24 填空）；② 估算 $2^{24}$ 与 $2^{32}$（p.26）；
  ③ 一个 16 位计数器能计到多少、溢出前最后一个数是什么（数值校验：$2^{16}=65\,536$）。
- 链接: `[[Binary Number System]]`、`[[Number Systems]]`、`[[Octal Number System]]`、
  `[[Hexadecimal Number System]]`、`[[Two's Complement Representation]]`、`[[Fixed-Point Numbers]]`

---

## 分区 5 · Binary Arithmetic（源：p.28–33）

### N08 | Binary Arithmetic
- file: `Notes/Binary Arithmetic.md`
- aliases: `二进制算术运算` / `二进制四则运算` / `Binary Arithmetic` / `Binary Addition and Subtraction`
- tags: `ECE2050`, `binary-arithmetic`
- must-cover: **加法法则**（$0+0=0$、$0+1=1$、$1+0=1$、$1+1=10$ 进位）与竖式逐列进位链（p.28–29，$1011_2+0110_2=1\,0001_2$）；
  **减法法则**与借位（$0-1$ 借 1 得 $10-1=1$）（p.31）；
  **乘法法则**（只有 $1\times1=1$）→ 移位相加的部分积 (partial product)（p.32），
  自算例题 $1011_2\times1101_2=1000\,1111_2$（$11\times13=143$，用 Python 复核）；
  **除法**（p.33：$(1001)_2\div(11)_2=11_2$；长除法与"反复相减"两种视角）；
  **溢出 (overflow)**（p.30）：数字系统位宽固定，结果超出可表示范围时发生；
  4 位无符号加法 $11+6=17$ 需要 5 位 → 4 位结果 $0001$ 是错的（丢弃进位得到 $1$，误差 $16$）；
  无符号加法的进位 (carry) 与减法的借位 (borrow) 标志；定点宽度的模运算语义（$\bmod 2^N$）。
- 图: `binary-addition-carries.svg`（matplotlib：双面板 (a) $1011+0110$ 的竖式进位链，
  逐列标出 carry-in/carry-out 与最终 $1\,0001$；(b) 位宽 4 时丢弃进位得到 $0001=1$ 的错误结果，
  并与真值 17 对比）
- 例题: ① $11+6$（p.29）；② $1011_2\times1101_2$（自算，含部分积表）；③ $1001_2\div11_2$（p.33）；
  ④ 判断哪些和会溢出（给定 4 位无符号）。
- 链接: `[[Binary Number System]]`、`[[Bits and Bytes]]`、`[[Two's Complement Representation]]`、
  `[[Sign-Magnitude Representation]]`、`[[Signed Binary Multiplication and Division]]`、`[[Cyclic Redundancy Check]]`

---

## 分区 6 · Signed Numbers（源：p.35–48）❗

### N09 | Sign-Magnitude Representation
- file: `Notes/Sign-Magnitude Representation.md`
- aliases: `原码` / `符号数值表示法` / `符号-幅值表示` / `Sign-Magnitude Representation` / `Sign and Magnitude`
- tags: `ECE2050`, `signed-numbers`
- must-cover: 结构 = 1 个符号位（**最高位**，0 正 1 负）+ $N-1$ 个幅值位（p.36）；$\pm6$ 的 4 位例子（$0110$ / $1110$）；
  范围 $[-(2^{N-1}-1),\,2^{N-1}-1]$（4 位 $[-7,7]$）；
  **两个致命问题**（p.37）：① 加法不成立——$1110+0110=1\,0100$（十进制 20，不是 0）；
  ② **两个零**（$0000$ 与 $1000$）；需要额外的符号判断与比较电路；
  为什么它仍然存在（浮点数的符号位、ADC/传感器符号位、人类可读）→ 链 [[Floating-Point Numbers]]。
- 图: `sign-magnitude-zero.svg`（matplotlib：4 位原码的 16 个码字在数轴上的排布，
  标出 $\pm0$ 两个码、范围端点 $0111/1111$，并在下方画出 $(-6)+(+6)$ 竖式得到 $1\,0100$ 的失败结果）
- 例题: ① 写出 $-6$ 的 4 位原码并说明符号位（p.36）；② 用 $(-6)+(+6)$ 演示失败（p.37，数值校验 $20\ne0$）；
  ③ 原码范围题：8 位原码能表示的最大/最小数（$\pm127$）。
- 链接: `[[Two's Complement Representation]]`、`[[Binary Arithmetic]]`、`[[Floating-Point Numbers]]`、`[[Number Systems]]`

### N10 | Two's Complement Representation ❗
- file: `Notes/Two's Complement Representation.md`
- aliases: `补码` / `二进制补码` / `二的补码` / `Two's Complement Representation` / `2's Complement`
- tags: `ECE2050`, `signed-numbers`
- must-cover: 定义与**权重视角**：MSB 的权重是 $-2^{N-1}$（p.39），其余位正权 → 直接解释了非对称范围；
  4 位码表 $-8\dots+7$；MSB 仍然指示符号（1 负 0 正）；
  范围 $[-2^{N-1},\,2^{N-1}-1]$（p.39）；**唯一零**；
  **取反符号 (reverse the sign)**：invert bits + 1（p.40–41，$3\to1101$；$1001_2\to-7$），
  并解释为什么成立（$x+\bar{x}=2^N-1=-1 \pmod{2^N}$）；
  命名的历史包袱：讲义强调"taking the two's complement"这个说法容易混，统一叫 reverse the sign；
  **加法成立**（p.42–44）：三步法（转补码 → 相加 → 看符号判溢出），进位丢弃；
  **进位判别符号的规则**：异号相加时 carry-out=1 → 结果为正，carry-out=0 → 结果为负（$15+(-6)$ 有进位得 $+9$；
  $16+(-24)$ 无进位得 $-8$）；
  **溢出判据**（p.43）：同号相加而结果符号相反 → 溢出（$1000\,0011+1100\,0110=1\,0100\,1001$，
  $-125+(-58)=-183$ 超出 $[-128,127]$）；
  **减法 = 加上相反数**（p.45，$8-3=8+(-3)$ 丢弃进位；$3-5=3+(-5)$）；
  符号扩展 (sign extension) 与位宽扩展的正确做法；为什么硬件喜欢补码（一个加法器搞定加减）。
- 图: `nbit-range.svg` + `twos-complement-wheel.svg` + `overflow-detection.svg`
  - `nbit-range.svg`（matplotlib：4 位下 unsigned / sign-magnitude / two's complement 三种表示的
    数轴与范围对照，标出 $\pm0$ 与 $-8$ 的"多余"码字）
  - `twos-complement-wheel.svg`（matplotlib：16 格圆盘/时钟图，顺时针每格 +1，标 $0000$–$1111$
    与对应十进制 $-8\dots7$，展示"加 $k$ 就是转 $k$ 格"与回绕 $-8$）
  - `overflow-detection.svg`（matplotlib：8 位数轴 $[-128,127]$，画出 $(-125)+(-58)=-183$ 越界，
    以及合法加法 $(-5)+(-9)=-14$ 的对比）
- 例题: ① $-6$ 的 4 位补码 + 反符号验证（p.41）；② $15+(-6)$ 与 $16+(-24)$（p.44，含进位判别）；
  ③ $(-125)+(-58)$ 判断溢出（p.43）；④ $3-5$ 用加法实现（p.45）；⑤ 8 位补码范围与 $-128$ 的特殊性。
- 链接: `[[Sign-Magnitude Representation]]`、`[[Binary Arithmetic]]`、`[[Bits and Bytes]]`、
  `[[Signed Binary Multiplication and Division]]`、`[[Fixed-Point Numbers]]`、`[[Number Systems]]`

### N11 | Signed Binary Multiplication and Division
- file: `Notes/Signed Binary Multiplication and Division.md`
- aliases: `有符号二进制乘除法` / `补码乘除法` / `Signed Binary Multiplication and Division` /
  `Two's Complement Multiplication and Division`
- tags: `ECE2050`, `signed-numbers`
- must-cover: **乘法**（p.46，EXAMPLE 2–22）：符号由操作数决定（同号为正、异号为负）；
  直接累加太慢且必须用真值 (uncomplemented) 形式；**部分积 (partial product)** 方法；
  补码部分积的符号扩展规则；例题 $59\times83=4897$，$4897_{10}=1001100100001_2$，
  $-4897$ 的 14 位补码 $=10110011011111_2$（p.46 讲义原数，已在 verify 报告核对）；
  **除法**（p.47，EXAMPLE 2–23）：用**反复相减**实现，商 = 相减次数，停止条件 = 余数为 0 或变负；
  符号规则同乘法（同号为正、异号为负）；例题 $(01100100)_2\div(00011001)_2=100\div25$：
  减 4 次得商 $0100_2$、余数 0；$100\div(-25)$ 先按 $100\div25=4$ 再取负 → $-4=1111\,1100_2$；
  余数符号约定、商的位宽与符号扩展；为什么硬件实现是"移位 + 加减"（链接到 Ch6 adder / Ch8 shift register，
  用纯文本提及）。
- 图: `signed-multiplication-partial-products.svg`（matplotlib：$59\times83$ 的 8 位部分积阶梯图——
  逐行移位、标注每行权值，最后一行把和取补码变成 $-4897$ 的 14 位形式）
- 例题: ① $59\times83$ 的部分积 + 符号处理（p.46）；② $100\div25$ 的反复相减表与商（p.47）；
  ③ $100\div(-25)$ 与 $(-100)\div(-25)$ 的符号讨论（自算复核）。
- 链接: `[[Two's Complement Representation]]`、`[[Binary Arithmetic]]`、`[[Sign-Magnitude Representation]]`

---

## 分区 7 · Fractional Numbers（源：p.50–62）

### N12 | Fixed-Point Numbers
- file: `Notes/Fixed-Point Numbers.md`
- aliases: `定点数` / `定点表示法` / `Fixed-Point Numbers` / `Fixed-Point Representation` / `Q 格式`
- tags: `ECE2050`, `fractional-numbers`
- must-cover: 小数点的两种处理（p.51）：fixed-point（小数点固定/隐含）与 floating-point（浮动）；
  fixed-point 的**约定前提**：整数位数与小数位数必须事先约定（p.52）；
  $6.75$ 在 4 整数位 + 4 小数位下 $=0110.1100$；
  **Ua.b**（无符号，$a$ 整数位 + $b$ 小数位，p.53）：$6.75$ 写成 U4.4 `01101100`、
  U3.5 `11011000`、U6.2 `00011011`；分辨率 $2^{-b}$、范围 $[0,\,2^a-2^{-b}]$（U4.4 为 $[0,15.9375]$）；
  $8/16/32$ 位常见；U8.8 常用于传感器/音频/像素，U16.16 用于更高精度信号处理；
  **Qa.b**（有符号补码，$a$ 含符号位，p.54）：$-6.75$ 在 Q4.4 的求法（取补）$=10010100$；
  Q1.15 (Q15) 在 DSP 中常见——**注意**：讲义写 $(1,-1]$ 不严谨，正确范围是 $[-1,\,1-2^{-15}]$，
  $1$ 恰好不可表示（$1.0$ 会溢出成 $-1$），必须注明；
  **饱和运算 (saturating arithmetic)**（p.55）：定点溢出会产生刺眼/刺耳伪影
  （视频亮点中的一个黑点、音频的爆音 click），因此溢出时钳位到最大/最小值；
  讲义例子 U4.4 中 $12+7.5=19.5$ 超出最大值 $15.9375$：真实和需要 9 位，
  8 位回绕得 $0011\,1000=3.5$（严重错误），饱和则钳到 `11111111` $=15.9375$；
  讲义把该式简写成 `11000000 + 01111000 = 11111111`（省略了回绕中间步），正文要说明这一点。
- 图: `fixed-point-format.svg` + `saturating-arithmetic.svg`
  - `fixed-point-format.svg`（matplotlib：双面板 (a) U4.4 的位权刻度 $2^3\dots2^{-4}$ + 隐含小数点 +
    $6.75$ 的位串；(b) Q4.4 的位权（MSB 为 $-2^3$）+ $-6.75$ 的位串，并对照 U3.5/U6.2 的同一数值）
  - `saturating-arithmetic.svg`（matplotlib：U4.4 加法器的输入和 → 输出曲线，画出"回绕 wrap"
    与"饱和 saturate"两条折线，标出 $12+7.5$ 的工作点：回绕 $3.5$ vs 饱和 $15.9375$）
- 例题: ① $6.75$ 的三种 U 格式（p.53）；② $-6.75$ 的 Q4.4（p.54）；③ $12+7.5$ 的饱和与回绕对比（p.55）。
- 链接: `[[Floating-Point Numbers]]`、`[[Two's Complement Representation]]`、
  `[[Number Base Conversion]]`、`[[Bits and Bytes]]`

### N13 | Floating-Point Numbers ❗
- file: `Notes/Floating-Point Numbers.md`
- aliases: `浮点数` / `浮点表示法` / `IEEE 754` / `Floating-Point Numbers` / `Floating-Point Representation`
- tags: `ECE2050`, `fractional-numbers`
- must-cover: 二进制点"浮动到最高位 1 的右边"（p.51, p.57）；与十进制科学计数法类比
  $273=2.73\times10^2$；通式 $\pm M\times B^{E}$（mantissa/base/exponent，p.57）；
  **IEEE 754 单精度**（p.59）：1 位符号 + 8 位阶码 + 23 位尾数；规格化后**隐含前导 1**（implicit leading 1）
  → 有效精度 24 位；**偏移阶码 (biased exponent)**：$\text{stored}=E+127$（bias 127），
  字段范围 $[0,255]$ → 实际指数 $[-127,+128]$；
  **为什么用偏移**（p.60）：① 阶码永远非负，浮点数的**大小比较可以按无符号整数比较**；
  ② 全 0 阶码腾出来表示 0 与非规格化数；
  例题：$228_{10}=1110\,0100_2=1.11001\times2^7$ → 阶码 $127+7=134=1000\,0110_2$，
  位串 `0 10000110 11001000000000000000000` $=0x43640000$（已核对）；
  $-58.25_{10}=111010.01_2=1.1101001\times2^5$ → 阶码 $132=1000\,0100_2$，
  `1 10000100 11010010000000000000000` $=0xC2690000$（已核对）；
  **特殊值**（p.62）：$0$（阶码全 0、尾数全 0，符号任意）、$\pm\infty$（阶码全 1、尾数全 0）、
  NaN（阶码全 1、尾数非 0）；
  精度与舍入：$23$ 位尾数 ≈ 7 位十进制有效数字，$1.0$ 处的间隔是 $2^{-23}\approx1.19\times10^{-7}$；
  动态范围：最小规格化数 $2^{-126}\approx1.18\times10^{-38}$、最大 $\approx3.40\times10^{38}$；
  扩展/坑：$0.1$ 无法精确表示、浮点相等比较、大数吃小数、NaN 不等于自身；
  denormal（阶码 0、尾数非 0）标注为超出讲义但要知道存在。
- 图: `ieee754-single-format.svg` + `floating-point-dynamic-range.svg`
  - `ieee754-single-format.svg`（matplotlib：32 位字段布局图 + 两个已核对例题（228 / −58.25）的
    位串与十六进制结果，标出隐含的 $1.$）
  - `floating-point-dynamic-range.svg`（matplotlib：对数数轴上标出单精度的可表示幅值区间
    （$2^{-126}$ 到 $\approx3.4\times10^{38}$）、$228$ 与 $58.25$ 的位置，两端标 $0$、$\pm\infty$、NaN 的
    字段编码，并与 Q4.4 这类定点的窄区间对比）
- 例题: ① $228\to$ IEEE 754（p.59）；② $-58.25\to$ IEEE 754（p.61）；
  ③ 反解：把 `0x43640000` 拆字段还原成十进制（含符号、阶码、隐含 1 的还原）；
  ④ 精度题：为什么 $0.1$ 不能精确表示（写出前几位并算误差）。
- 链接: `[[Fixed-Point Numbers]]`、`[[Bits and Bytes]]`、`[[Two's Complement Representation]]`、
  `[[Sign-Magnitude Representation]]`

---

## 分区 8 · Codes（源：p.64–69）

### N14 | Binary Coded Decimal
- file: `Notes/Binary Coded Decimal.md`
- aliases: `BCD 码` / `二-十进制编码` / `8421 码` / `Binary Coded Decimal` / `BCD`
- tags: `ECE2050`, `codes`
- must-cover: 每个十进制数字单独用 4 位编码（p.65）；**8421 有权码**（权重 $8/4/2/1$，即自然二进制权重）；
  $170_{10}\to0001\,0111\,0000$、$2469_{10}\to0010\,0100\,0110\,1001$；
  16 个 4 位码只用 10 个，**6 个非法码**（$1010$–$1111$）→ 这是后面 +6 修正的根源；
  BCD↔十进制：从右往左每 4 位一组（p.65）；
  **BCD 加法**（p.66）：① 按二进制相加；② 若 4 位和 $\le 9$ 且无进位 → 合法；
  ③ 否则加 $0110$ 修正（并处理进位）；
  **为什么加 6**：二进制在 $1001$ 之后会经过 6 个跳过的码才进位，加 6 相当于"跳过"这 6 个码；
  自算例题 $8+5$（$1000+0101=1101>9$，$+0110=1\,0011\to0001\,0011$）与 $9+9$（得 $0001\,1000$）；
  多位 BCD 的进位传播；BCD 的代价与应用（每位浪费 6 个码、运算更慢、需要专门电路；
  但适合十进制显示、计算器、金额/仪器）；
  **BCD ≠ 二进制**（$13_{10}$ 的 BCD 是 $0001\,0011$，二进制是 $1101$）。
- 图: `bcd-8421-encoding.svg` + `bcd-addition-correction.svg`
  - `bcd-8421-encoding.svg`（matplotlib：(a) 0–15 的 4 位码表，合法 BCD 与 6 个非法码用 GOOD/BAD 着色；
    (b) $170$、$2469$ 的 BCD 分组图）
  - `bcd-addition-correction.svg`（matplotlib：$8+5$ 与 $9+9$ 两列的修正过程，
    标出"和 > 9 或产生进位"的判定点与 $+0110$ 的位置）
- 例题: ① $170$、$2469$ 的 BCD 编码（p.65）；② $8+5$ 的 BCD 加法与 +6 修正（p.66）；
  ③ $9+9$ 的进位修正（自算）；④ 判断给定 4 位码是否为合法 BCD。
- 链接: `[[Decimal Number System]]`、`[[Number Base Conversion]]`、
  `[[American Standard Code for Information Interchange]]`、`[[Bits and Bytes]]`

### N15 | Gray Code
- file: `Notes/Gray Code.md`
- aliases: `格雷码` / `格雷编码` / `循环码` / `Gray Code` / `Reflected Binary Code`
- tags: `ECE2050`, `codes`
- must-cover: 定义：相邻码字**只变 1 位**（p.67），也叫 cyclic code / reflected binary code；
  4 位完整序列（已核对）：`0000 0001 0011 0010 0110 0111 0101 0100 1100 1101 1111 1110 1010 1011 1001 1000`，
  且**首尾也只差 1 位**（循环性）；
  反射构造法 (reflection)：$G_n$ = `0`+$G_{n-1}$ 与 `1`+$\mathrm{reverse}(G_{n-1})$；
  二进制 ↔ 格雷码公式：$g=b\oplus(b\gg1)$；反变换 $b_{N-1}=g_{N-1}$、$b_i=b_{i+1}\oplus g_i$；
  **为什么有用**（p.68）：接收端判决错误概率与符号距离成反比，相邻符号只差 1 位
  → 判错到相邻符号时**只有 1 个比特错**，后续纠错/检错代价最小；
  讲义例子：直接二进制从 $011\to100$ 要同时翻转 3 位，中间可能经过 $010,001,101,110,111$ 等
  任意中间态；用格雷码则每次只有 1 位跳变，不存在"多位同时翻转"的危险窗口；
  应用：旋转编码器/位置检测（消除多位跳变导致的错误读数）、K-map 的排列（Ch4 内容，纯文本提及）、
  数字通信星座图映射；
  **非位权码**：格雷码是 non-positional/non-weighted 的典型例子（链 [[Number Systems]]）。
- 图: `gray-code-sequence.svg` + `gray-code-symbol-mapping.svg`
  - `gray-code-sequence.svg`（matplotlib：(a) 4 位格雷码序列，相邻码字之间标注 Hamming 距离全为 1，
    并与自然二进制的距离（在进位处跳变多位）对比；(b) 反射构造法示意）
  - `gray-code-symbol-mapping.svg`（matplotlib：4-PSK 星座图两个版本——自然二进制标注 vs 格雷码标注
    `00 01 11 10`，标出相邻符号的位差）
- 例题: ① 写出 4 位格雷码序列并核对相邻距离（p.67，数值校验：每步 XOR 的 popcount = 1）；
  ② 二进制 $1011$ → 格雷码（$1110$）与格雷码 $1110$ → 二进制（$1011$）双向互算；
  ③ 计数 $011\to100$ 的位翻转次数对比（p.68）。
- 链接: `[[Number Systems]]`、`[[Binary Coded Decimal]]`、`[[Parity Bit]]`、
  `[[Cyclic Redundancy Check]]`、`[[Bits and Bytes]]`

### N16 | American Standard Code for Information Interchange
- file: `Notes/American Standard Code for Information Interchange.md`
- aliases: `ASCII 码` / `美国信息交换标准代码` / `字符编码` / `American Standard Code for Information Interchange` / `ASCII`
- tags: `ECE2050`, `codes`
- must-cover: 字母数字码 (alphanumeric code) 的用途（p.69）：把字符映射成位串；
  ASCII 是 **7 位码** → 128 个码字；分区结构：`0x00–0x1F` 控制字符、`0x20` 空格、
  `0x30–0x39` 数字、`0x41–0x5A` 大写、`0x61–0x7A` 小写、`0x7F` DEL；可打印字符 `0x20–0x7E` 共 95 个；
  关键码表（十六进制/十进制/二进制三列）：`'0'=0x30`、`'9'=0x39`、`'A'=0x41`、`'a'=0x61`；
  **结构规律**：数字码低 4 位就是数字值（`'7' = 0x37`）；大小写相差 `0x20`（只有第 5 位不同）；
  字母码的低 5 位与字母序号对应（`'A'+k`）；
  8 位扩展（`0x80–0xFF`，Latin-1 等）与 Unicode/UTF-8 的关系（UTF-8 对 ASCII 向后兼容）；
  实践：内存里的字符串就是 ASCII/UTF-8 字节序列（链 [[Hexadecimal Number System]] 的十六进制视图）；
  坑：`'9'` 与 `9` 不同（`0x39` vs `0x09`）、`'A'=65` 只在 ASCII 系成立、不要用 `c - 'A'` 之外的隐式算术。
- 图: `ascii-code-structure.svg`（matplotlib：高 4 位 × 低 4 位的 16×16 ASCII 表格网格，
  控制字符/数字/大写/小写/符号分色（GOOD/BAD/ACCENT/HILITE/FILL），标出 `0x30`、`0x41`、`0x61` 三个锚点）
- 例题: ① 写出字符串 `ECE2050` 的 ASCII（十六进制）字节串并转成二进制（自算复核）；
  ② 由码值反推字符：`0x4A`、`0x6A`、`0x35`（考大小写与数字规律）；
  ③ 计算"把 `'a'` 变成 `'A'` 需要做什么运算"（XOR `0x20` / 减 32）。
- 链接: `[[Hexadecimal Number System]]`、`[[Binary Coded Decimal]]`、`[[Parity Bit]]`、`[[Bits and Bytes]]`

---

## 分区 9 · Error Detection Codes（源：p.70–71）

### N17 | Parity Bit
- file: `Notes/Parity Bit.md`
- aliases: `奇偶校验位` / `奇偶校验` / `校验位` / `Parity Bit` / `Parity Check`
- tags: `ECE2050`, `error-codes`
- must-cover: 定义（p.70）：附加 1 位使一组比特中 1 的个数**恒为偶数（偶校验）或恒为奇数（奇校验）**；
  发送端计算方法（数据位 XOR，偶校验 = XOR 结果；奇校验 = 取反）；
  例题（p.70 原题）：奇数校验系统收到 `10110`、`11010`、`110011`、`110101110100`、`1100010101010`，
  各组 1 的个数 $3,3,4,7,6$ → 偶数个 1 的 `110011` 与 `1100010101010` 出错；
  **检测能力**：能发现任意**奇数个**比特错误；对**偶数个**比特错误完全失明（两位翻转互相抵消）；
  只能检错、**不能纠错**（不知道是哪一位错）；开销 $1/(n+1)$；
  提高能力的方向：二维/块校验（行 + 列）可定位并纠正 1 位错误、与 CRC/汉明码的关系（链 [[Cyclic Redundancy Check]]）；
  与 [[Gray Code]] 的对比：一个管"错误传播"，一个管"错误检测"。
- 图: `parity-bit-format.svg`（matplotlib：双面板 (a) 偶/奇校验的位串与 1 的计数，
  含"发送—接收—判定"流程；(b) 两比特翻转的盲区示例，标出为何检不出）
- 例题: ① 讲义 p.70 五组判定；② 给定数据 `1101001` 求偶校验位与奇校验位（自算复核）；
  ③ 制造一个 2 位错误，说明为什么检不出来。
- 链接: `[[Cyclic Redundancy Check]]`、`[[American Standard Code for Information Interchange]]`、
  `[[Bits and Bytes]]`、`[[Gray Code]]`

### N18 | Cyclic Redundancy Check
- file: `Notes/Cyclic Redundancy Check.md`
- aliases: `循环冗余校验` / `CRC 校验` / `生成多项式` / `Cyclic Redundancy Check` / `CRC`
- tags: `ECE2050`, `error-codes`
- must-cover: 定义（p.71）：能检测数据块中**多个**错误的检错方法；发送端在数据后附加一个校验和 (checksum/FCS)，
  接收端重新计算并比对，余数为 0 判定无错；
  **模 2 运算 (modulo-2 / XOR)**：加法无进位、减法等于加法（$1\oplus1=0$）；
  算法步骤（p.71 原例，全部已核对）：数据 $D=11010011$、生成码 $G=1010$ →
  ① 在 $D$ 后补 $0000$ 得 $D'=110100110000$；② 用 $G$ 做模 2 长除，余数 $=0100$；
  ③ 发送 $110100110100$；④ 接收端整帧除以 $G$ 余数为 $000$ → 无错；
  ⑤ 任一位翻转（如末位）→ 余数 $001\ne0$ → 检测到错误；
  **为什么比奇偶校验强**：能发现所有单比特、双比特、奇数位错误以及长度 $\le$ 阶数的突发错误 (burst error)；
  多项式视角：$G$ 对应生成多项式 $G(x)$，余数是 $D(x)\cdot x^{k} \bmod G(x)$（时间域→域上除法）；
  硬件实现：**移位寄存器 + XOR**（链到 Ch8 shift register，纯文本提及），
  标准生成多项式 CRC-8 / CRC-16 / CRC-32（如 `0x04C11DB7`，标注为延伸）；
  坑：XOR 与算术减法的区别、补零个数 = 生成码位数 − 1（讲义例子里补了 4 位并保留 4 位余数，
  是"4 位校验和"约定）、位序（MSB-first / LSB-first）与初值约定必须两端一致、
  CRC 不是加密也不能纠错。
- 图: `crc-modulo2-division.svg` + `crc-shift-register.svg`
  - `crc-modulo2-division.svg`（matplotlib：模 2 长除的阶梯图——每一行对齐的 XOR 消去最高位，
    标出被消去的位、最终余数 $0100$；再画接收端余数 $000$ 与单比特错误的 $001$）
  - `crc-shift-register.svg`（schemdraw：CRC 编码器的串行移位寄存器结构，4 级 D-FF + 根据 $G=1010$
    的 XOR 反馈抽头，标注 $D_{in}$ / 时钟 / 输出；(b) XOR 门符号与模 2 加法说明）
- 例题: ① 讲义 p.71 全流程（补零、长除、余数、发送、接收校验）；② 单比特错误检测（自算）；
  ③ 给定 $D$、$G$ 手算余数并说明为什么余数不为 0 就报错（数值校验：接收端整帧余数为 0）。
- 链接: `[[Parity Bit]]`、`[[Binary Arithmetic]]`、`[[Bits and Bytes]]`、`[[Gray Code]]`

---

## 图清单（24 张，脚本与 SVG 同名）

| # | 图 | 工具 | 归属笔记 |
|---|---|---|---|
| 1 | `positional-weights.svg` | matplotlib | N01（N02 复用） |
| 2 | `binary-powers-and-counting.svg` | matplotlib | N03 |
| 3 | `linux-file-permissions.svg` | matplotlib | N04 |
| 4 | `hex-memory-address.svg` | matplotlib | N05 |
| 5 | `base-conversion-grouping.svg` | matplotlib | N06 |
| 6 | `powers-of-two-scale.svg` | matplotlib | N07 |
| 7 | `binary-addition-carries.svg` | matplotlib | N08 |
| 8 | `sign-magnitude-zero.svg` | matplotlib | N09 |
| 9 | `nbit-range.svg` | matplotlib | N10 |
| 10 | `twos-complement-wheel.svg` | matplotlib | N10 |
| 11 | `overflow-detection.svg` | matplotlib | N10 |
| 12 | `signed-multiplication-partial-products.svg` | matplotlib | N11 |
| 13 | `fixed-point-format.svg` | matplotlib | N12 |
| 14 | `saturating-arithmetic.svg` | matplotlib | N12 |
| 15 | `ieee754-single-format.svg` | matplotlib | N13 |
| 16 | `floating-point-dynamic-range.svg` | matplotlib | N13 |
| 17 | `bcd-8421-encoding.svg` | matplotlib | N14 |
| 18 | `bcd-addition-correction.svg` | matplotlib | N14 |
| 19 | `gray-code-sequence.svg` | matplotlib | N15 |
| 20 | `gray-code-symbol-mapping.svg` | matplotlib | N15 |
| 21 | `ascii-code-structure.svg` | matplotlib | N16 |
| 22 | `parity-bit-format.svg` | matplotlib | N17 |
| 23 | `crc-modulo2-division.svg` | matplotlib | N18 |
| 24 | `crc-shift-register.svg` | **schemdraw** | N18 |

> 位域/位串类图统一约定：bit 格用 `FILL` 填充 + `INK` 边框；被强调的位（符号位、进位、校验位、
> 非法码）用 `HILITE`/`BAD`；正确结果用 `GOOD`。二进制串按 4 位一组显示。

---

## 术语表分区（Glossary 的 section 标题）

`1 · Foundations` / `2 · Number Bases` / `3 · Conversion` / `4 · Bits and Scale` /
`5 · Binary Arithmetic` / `6 · Signed Numbers` / `7 · Fractional Numbers` /
`8 · Codes` / `9 · Error Detection Codes`
