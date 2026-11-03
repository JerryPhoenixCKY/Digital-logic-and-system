---
tags:
  - ECE2050
  - glossary
date: 2026-09-30
updated: 2026-10-09
aliases:
  - ECE2050 术语表
  - Glossary
  - 术语表
  - 词汇表
---

# ECE2050 Glossary · 术语表

> [!NOTE] How to use · 用法
> 按章节找英文名、中文名或缩写；链接直接进入主线笔记的对应小节。完整推导、适用条件与例题留在专题中；学习顺序见 [[ECE2050 Knowledge Tree]]。

## Ch1 · Digital Foundations · 数字基础

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 数字抽象与系统设计 | Digital Abstraction and System Design | — | Discrete information, continuous voltages, hierarchy, modularity, and controller/datapath design · 数字抽象与系统设计。 | [[Digital Foundations and Waveforms#1 · Digital Abstraction and System Design · 从电压到信息\|Digital Abstraction and System Design]] |
| 数字波形 | Digital Waveforms | — | Period, frequency, duty cycle, rise/fall time, and interval-by-interval waveform reading · 波形读图。 | [[Digital Foundations and Waveforms#2 · Digital Waveforms · 再把时间加入模型\|Digital Waveforms]] |

## Ch2 · Number Representation and Coding · 数值表示与编码

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 数制 | Number System | — | 书写与表示数字的体系，由基数、数码集合与位权规则共同定义 | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 基数 / 进制 | Base / Radix | $R$ | 数制中可用的数码个数，$R\ge2$；$R$ 进制写作 base-$R$ | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 数码 | Digit | $a_i$ | 某一位上允许出现的符号，取值范围 $[0,R-1]$ | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 位权 | Weight | $R^i$ | 第 $i$ 位所代表的实际倍率，整数位 $i\ge0$、小数位 $i<0$ | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 按位权展开 | Positional Expansion | — | $(N)_R=\sum_i a_iR^i$，把位串还原成数值的标准求和式 | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 位权计数制 | Positional / Weighted Number System | — | 符号的值由其所处**位置**决定；二/八/十/十六进制都属于此类 | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 非位权计数制 | Non-positional / Non-weighted Number System | — | 数值不能按固定数位权简单相加；格雷码属非位权编码，不宜与传统非位权记数法混同 | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 小数点 / 进制点 | Radix Point | — | 分隔整数位与小数位的记号；二进制下叫 binary point，十六进制下叫 hex point | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 下标记号 | Subscript Notation | $(N)_R$ | 用下标标明基数，消除"同一串数字在不同进制下含义不同"的歧义 | [[Number Systems and Base Conversion#1 · Number Systems · 位权是共同模型\|Number Systems]] |
| 十进制 | Decimal / Base-10 | — | 基数为 10、数码 $0$–$9$ 的数制；"decimal number" 泛指 base-10 数，不限于带小数点者 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Decimal Number System]] |
| 二进制 | Binary / Base-2 | — | 基数为 2、数码只有 $0$ 与 $1$ 的数制，是数字系统的内部语言 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Binary Number System]] |
| 二进制点 | Binary Point | — | 二进制数中隐含的整数/小数分界，权值为 $2^0$ 与 $2^{-1}$ 之间 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Binary Number System]] |
| 二的幂 | Power of Two | $2^n$ | 二进制各位的权值序列；$2^{10}=1024$；Ki 表示 1024，十进制 k 表示 1000 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Binary Number System]] |
| 二进制计数 | Counting in Binary | — | 从 $0000$ 逐次加 1 的计数过程，可看出各位翻转频率相差一倍 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Binary Number System]] |
| 八进制 | Octal / Base-8 | Oct | 基数为 8、数码 $0$–$7$；1 位 = 3 bit，Unix 文件权限用它表示 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Octal Number System]] |
| 文件权限码 | File Permission Code | rwx | 每 3 bit 表示读/写/执行，合成 1 个八进制位；如 `755` = rwxr-xr-x | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Octal Number System]] |
| 十六进制 | Hexadecimal / Base-16 | Hex | 基数为 16、数码 $0$–$9$ 与 `A`–`F`；1 位 = 4 bit = 1 nibble | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Hexadecimal Number System]] |
| 十六进制字母数码 | Hexadecimal Alphabetic Digits | A–F | 表示 $10$–$15$ 的 6 个字母字符，是十六进制独有的数码 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Hexadecimal Number System]] |
| 十六进制前缀 | Hex Prefix | `0x` | C/汇编等语言里标记十六进制字面量的前缀 | [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释\|Hexadecimal Number System]] |
| 数制转换 | Number Base Conversion | — | 同一数值在不同基数表示之间的换算，含四类基本算法 | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 反复除法 | Repeated Division | — | 十进制转任意进制：不断除以基数，余数**从下往上**读（首个余数是 LSB） | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 反复乘法 | Repeated Multiplication | — | 小数部分转进制：不断乘基数，整数位**从上往下**读（可能不终止） | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 最大幂相减法 | Largest-Power Subtraction | — | 十进制转二进制的手算法：每次减去能容纳的最大 $2^k$ | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 分组法 | Grouping Method | — | 二进制 ↔ 八/十六进制：从小数点向两侧每 3（4）位分组；整数向左补 0，小数向右补 0 | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 十进制中枢 | Decimal Pivot | — | 任意进制互转的通用路径：先转十进制，再转目标进制 | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 余数 | Remainder | R | 反复除法中每一步的余数，决定目标进制的一位 | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 最高有效位 | Most Significant Bit | MSB | 位串最左边、权值最大的位；有符号数里它兼作符号位 | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 最低有效位 | Least Significant Bit | LSB | 位串最右边、权值为 1（或 $2^{-b}$）的位 | [[Number Systems and Base Conversion#3 · Number Base Conversion · 整数、小数与分组\|Number Base Conversion]] |
| 位 / 比特 | Bit | b | 1 个二进制位，数字系统中的最小信息单位 | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 半字节 | Nibble | — | 4 bit，可表示 16 个值 $[0,15]$，正好对应 1 个十六进制位 | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 字节 | Byte | B | 8 bit，可表示 256 个值 $[0,255]$，是存储与寻址的基本单位 | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 字 | Word | — | 处理器一次处理的数据宽度（16/32/64 位），本课程只作术语了解 | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 位宽容量 | Capacity of $N$ bits | $2^N$ | $N$ 位可表示的状态总数，取值范围 $[0,2^N-1]$ | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 二进制前缀 | Binary Prefix | Ki/Mi/Gi | 以 $2^{10}$ 为步长的前缀（KiB = 1024 B），区别于十进制前缀 kB = 1000 B | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 大幂次速记 | Large Powers of Two | — | $2^{10}\approx10^3$ kilo、$2^{20}\approx10^6$ mega、$2^{30}\approx10^9$ giga、$2^{40}$ tera、$2^{50}$ peta、$2^{60}$ exa | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 幂次估算 | Estimating Powers of Two | — | 把指数拆成 $2^{10}$ 的倍数再乘余项，如 $2^{24}=16\times2^{20}\approx16$ M | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 地址空间 | Address Space | — | 用 $N$ 位地址可寻址的单元数 $2^N$；32 位按字节寻址 = 4 GiB | [[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量\|Bits and Bytes]] |
| 二进制算术运算 | Binary Arithmetic | — | 加、减、乘、除四种位运算规则及其竖式实现 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 进位 | Carry | C | 某列二进制相加达到 2 时向高位的传递量；$1+1=10$ 产生进位 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 借位 | Borrow | — | 减法中低位不够减时向高位借 1，等于借来 2 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 部分积 | Partial Product | — | 乘法中每个乘数位与被乘数相乘得到的移位结果，最后相加 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 移位相加 | Shift and Add | — | 二进制乘法只用"移位 + 相加"实现，因为乘数位非 0 即 1 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 长除法 | Long Division | — | 二进制除法：逐位比较、相减、落下下一位，与十进制同构 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 溢出 | Overflow | — | 数学结果超出当前表示范围；需区分无符号进位与有符号溢出，并遵循回绕／饱和规范 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 模运算语义 | Modulo Arithmetic | $\bmod 2^N$ | $N$ 位运算等价于对 $2^N$ 取模，最高位的进位被丢弃 | [[Binary Arithmetic and Signed Representation#1 · Binary Arithmetic · 先看无符号运算\|Binary Arithmetic]] |
| 有符号数 | Signed Number | — | 用最高位表示正负的二进制表示法统称 | [[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法\|Sign-Magnitude Representation]] |
| 原码 / 符号-幅值 | Sign-Magnitude | — | 1 个符号位 + $N-1$ 个幅值位；有 $\pm0$；直接按无符号加法会错，需符号/幅值专门处理 | [[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法\|Sign-Magnitude Representation]] |
| 符号位 | Sign Bit | — | 最高位，0 表示正、1 表示负 | [[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法\|Sign-Magnitude Representation]] |
| 正零与负零 | Positive / Negative Zero | $\pm0$ | 原码中 `0000` 与 `1000` 都表示 0，浪费一个码字且比较麻烦 | [[Binary Arithmetic and Signed Representation#2 · Sign-Magnitude Representation · 符号不能直接参与加法\|Sign-Magnitude Representation]] |
| 补码 | Two's Complement | 2's C | MSB 权值为 $-2^{N-1}$ 的表示法；唯一零、加法成立、范围 $[-2^{N-1},2^{N-1}-1]$ | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 反码 | One's Complement | 1's C | 逐位取反的结果，$\bar x=2^N-1-x$；常作为求补码的中间步骤 | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 取反符号 | Reverse the Sign | — | 求相反数：逐位取反再加 1（讲义刻意避免叫 "take the two's complement"） | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 补码码表 | Two's Complement Code Table | — | 4 位下 `1000`–`0111` 对应 $-8$–$+7$ 的完整映射 | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 进位判别 | Carry-out Sign Rule | — | **异号**相加时：有进位出 → 结果为正，无进位出 → 结果为负 | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 补码溢出判据 | Two's Complement Overflow | — | 同号相加而结果符号相反（或异号相减而结果符号错误）即溢出 | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 符号扩展 | Sign Extension | — | 拓宽位宽时把符号位复制到新增高位，数值不变 | [[Binary Arithmetic and Signed Representation#3 · Two's Complement Representation · 负权建立统一加法\|Two's Complement Representation]] |
| 真值形式 | True (Uncomplemented) Form | — | 未取补的原码形式；补码乘法要求操作数统一处理后再定符号 | [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确\|Signed Binary Multiplication and Division]] |
| 反复相减除法 | Division by Repeated Subtraction | — | 被除数反复减去除数，商 = 相减次数，直到余数为 0 或变负 | [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确\|Signed Binary Multiplication and Division]] |
| 恢复余数除法 | Restoring Division | — | 减成负数说明多减一次，把除数加回（restore）且商不增的除法实现 | [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确\|Signed Binary Multiplication and Division]] |
| 截断除法 | Truncated Division | — | 余数与被除数同号的整数除法约定（本课程采用） | [[Binary Arithmetic and Signed Representation#4 · Signed Binary Multiplication and Division · 位宽决定算法是否正确\|Signed Binary Multiplication and Division]] |
| 定点数 | Fixed-Point Number | — | 小数点位置固定（隐含），整数位与小数位数必须事先约定 | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| 浮点数 | Floating-Point Number | — | 用符号、有效数和指数表示数值；范围与精度分别由格式决定，零、次正规数与特殊码另行分类 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| U 格式 | Unsigned Fixed-Point Format | $\text{U}a.b$ | 无符号定点：$a$ 个整数位 + $b$ 个小数位，范围 $[0,2^a-2^{-b}]$ | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| Q 格式 | Signed Fixed-Point Format | $Qa.b$ | 本笔记采用 $a$ 包含符号位、$b$ 为小数位的补码定点约定，范围 $[-2^{a-1},2^{a-1}-2^{-b}]$；其他Q记法须另声明 | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| Q1.15 格式 | Q15 Format | Q1.15 | DSP 常用：16 位里 1 位符号 + 15 位小数，范围 $[-1,1-2^{-15}]$ | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| 分辨率 | Resolution | $2^{-b}$ | 定点数能分辨的最小步长（1 LSB 的权值），U4.4 为 0.0625 | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| 饱和运算 | Saturating Arithmetic | — | 溢出时钳位到最大/最小值而不是回绕，避免音频爆音、视频亮点 | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| 回绕 | Wrap-around | — | 固定宽运算丢弃超出位宽的部分，结果按模回绕；是否允许由规范决定，计数器常有意使用回绕 | [[Fixed-Point and Floating-Point Numbers#1 · Fixed-Point Numbers · 把整数乘以固定尺度\|Fixed-Point Numbers]] |
| 科学计数法 | Scientific Notation | $\pm M\times B^{E}$ | 把一个数写成尾数 $\times$ 基数 $^$ 指数 的规范化形式 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 尾数 / 有效数字 | Mantissa / Significand | $M$ | 浮点数的有效数部分；binary32正规数有隐含前导1、共24 bit精度，次正规数没有该隐含1 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 阶码 | Exponent | $E$ | 浮点数中决定数量级的部分 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 偏移阶码 | Biased Exponent | bias 127 | binary32正规数存储阶码 $E=e+127$，e为实际指数；E=0与255的解释需按特殊码规则处理 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 隐含前导 1 | Implicit Leading One | — | 二进制正规数的前导1可不存储；零和次正规数不使用该规则 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 规格化 | Normalization | — | 通过移动小数点使尾数落在 $[1,2)$ 并相应调整阶码 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 非规格化数 | Denormal / Subnormal | — | 阶码全 0 而尾数非 0 的数，用于表示极接近 0 的值（超出讲义，了解即可） | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 浮点特殊值 | Special Values | 0 / ±∞ / NaN | 阶码全 0 且尾数全 0 → 0；阶码全 1 尾数全 0 → $\pm\infty$；阶码全 1 尾数非 0 → NaN | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| IEEE 754 单精度 | Single Precision (binary32) | fp32 | 1 符号 + 8 阶码 + 23 尾数的 32 位浮点格式，十进制约 7 位有效数字 | [[Fixed-Point and Floating-Point Numbers#3 · Floating-Point Numbers · 用指数扩展范围\|Floating-Point Numbers]] |
| 编码 | Code | — | 用位串表示十进制数字、字符等非二进制信息的规则 | [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码\|Binary Coded Decimal]] |
| 二-十进制编码 | Binary Coded Decimal | BCD | 每个十进制位单独用 4 位 $8421$ 编码，如 $170\to0001\,0111\,0000$ | [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码\|Binary Coded Decimal]] |
| 8421 码 | 8421 Code | 8421 | BCD 的自然有权码形式，各位权值为 8/4/2/1 | [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码\|Binary Coded Decimal]] |
| 非法码 | Invalid Code | — | BCD 中未使用的 6 个 4 位码 $1010$–$1111$，是 $+6$ 修正的根源 | [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码\|Binary Coded Decimal]] |
| BCD 加法修正 | BCD Addition Correction | $+0110$ | 4 位和 $>9$ 或产生进位时加 6，跨过被跳过的 6 个码并进位 | [[Data Coding and Character Representation#2 · Binary Coded Decimal · 十进制数字逐位编码\|Binary Coded Decimal]] |
| 格雷码 | Gray Code | — | 相邻码字只差1 bit的非位权编码，常见为反射二进制格雷码；其循环相邻性不等同于CRC循环检错码 | [[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束\|Gray Code]] |
| 反射构造法 | Reflection Construction | — | 由 $n-1$ 位码表生成 $n$ 位码表：前半加前导 0、后半镜像加前导 1 | [[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束\|Gray Code]] |
| 汉明距离 | Hamming Distance | $d$ | 两个等长码字之间不同比特的个数；格雷码相邻距离恒为 1 | [[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束\|Gray Code]] |
| 循环性 | Cyclic Property | — | 格雷码首尾两个码字同样只差 1 位 | [[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束\|Gray Code]] |
| 字母数字码 | Alphanumeric Code | — | 表示字母、数字与符号的编码统称，ASCII 是最常见的一种 | [[Data Coding and Character Representation#4 · American Standard Code for Information Interchange · 字符编码\|American Standard Code for Information Interchange]] |
| 美国信息交换标准代码 | American Standard Code for Information Interchange | ASCII | 7 位字符编码，128 个码字；`0x30`–`0x39` 数字、`0x41`–`0x5A` 大写、`0x61`–`0x7A` 小写 | [[Data Coding and Character Representation#4 · American Standard Code for Information Interchange · 字符编码\|American Standard Code for Information Interchange]] |
| 控制字符 | Control Character | — | ASCII 中 `0x00`–`0x1F` 与 `0x7F`，不可打印，用于控制设备与格式 | [[Data Coding and Character Representation#4 · American Standard Code for Information Interchange · 字符编码\|American Standard Code for Information Interchange]] |
| 奇偶校验 | Parity Check | — | 附加 1 位使一组比特中 1 的个数恒为偶数（偶校验）或奇数（奇校验） | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |
| 校验位 | Parity Bit | P | 为满足奇偶约束而附加的一位；位置与位序由编码或协议规定 | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |
| 偶校验 / 奇校验 | Even / Odd Parity | — | 两种约定：1 的总数为偶 / 为奇；两端必须一致，否则永远报错 | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |
| 检错与纠错 | Error Detection / Correction | — | Detection reports an inconsistency when found; 未检出不保证无错；纠错还要定位并恢复，单个奇偶位不提供一般纠错 | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |
| 检错盲区 | Detection Blind Spot | — | 偶校验对偶数个比特错误完全失明（两次翻转互相抵消） | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |
| 循环冗余校验 | Cyclic Redundancy Check | CRC | 用模 2 长除的余数作校验和，能检测多位与突发错误的检错方法 | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数\|Cyclic Redundancy Check]] |
| 生成码 / 生成多项式 | Generator Code / Generator Polynomial | $G(x)$ | 收发双方约定的除数位串（如 $1010$ 对应 $x^3+x$） | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数\|Cyclic Redundancy Check]] |
| 模 2 运算 | Modulo-2 Arithmetic | XOR | 无进位的加法，$1\oplus1=0$；减法与加法相同 | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数\|Cyclic Redundancy Check]] |
| 校验和 / 帧校验序列 | Checksum / Frame Check Sequence | FCS | 发送端算出的余数，附加在数据后一起传输 | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数\|Cyclic Redundancy Check]] |
| 突发错误 | Burst Error | — | Error pattern from first to last changed bit; 常数项为1等条件下，degree-r CRC检测跨度≤r的突发错误 | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数\|Cyclic Redundancy Check]] |
| 校验位发生器 | Parity-Bit Generator | — | 偶校验位取数据 XOR，奇校验位取其补；位数指原始数据位数 | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |
| 校验检查器 | Parity Checker | — | 对收到的数据和收到的校验位共同判断；未检出错误不保证数据正确 | [[Parity and Cyclic Redundancy Checks#1 · Parity Bit · 用一个约束建立检错\|Parity Bit]] |

## Ch3 · Gates and Electrical Interfaces · 逻辑门与电气接口

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 逻辑门 | Logic Gate | — | 执行一个基本逻辑函数（NOT/AND/OR/NAND/NOR/XOR/XNOR）的电路单元 | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型\|Logic Gates]] |
| 反相器 / 非门 | Inverter / NOT Gate | — | 单输入门，输出取反 $Y=\bar A$；符号上的小圆圈叫 negating circle | [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算\|Inverter]] |
| 缓冲器 | Buffer | BUF | 输出等于输入 $Y=A$，用来驱动负载、整形与隔离 | [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算\|Inverter]] |
| 与门 | AND Gate | — | 全部输入为 1 时输出 1：$Y=AB$ | [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算\|AND Gate]] |
| 或门 | OR Gate | — | 任一输入为 1 时输出 1：$Y=A+B$ | [[Logic Gates and Boolean Functions#2 · Inverter, AND Gate and OR Gate · 三种基本运算\|OR Gate]] |
| 与非门 | NAND Gate | — | AND 之后取反：$Y=\overline{AB}$ | [[Logic Gates and Boolean Functions#3 · NAND Gate and NOR Gate · 输出取补与气泡\|NAND Gate]] |
| 或非门 | NOR Gate | — | OR 之后取反：$Y=\overline{A+B}$ | [[Logic Gates and Boolean Functions#3 · NAND Gate and NOR Gate · 输出取补与气泡\|NOR Gate]] |
| 异或门 | Exclusive-OR Gate | XOR | 两输入不同时输出 1：$Y=A\oplus B=A\bar B+\bar AB$；多输入时"奇数个 1"为 1 | [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性\|Exclusive-OR Gate]] |
| 同或门 | Exclusive-NOR Gate | XNOR | 两输入时检测相等，$Y=\overline{A\oplus B}$；多输入XOR归约的补表示偶数个1，不表示全部输入相等 | [[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性\|Exclusive-NOR Gate]] |
| 真值表 | Truth Table | — | 列出每种输入组合及其输出的表；$n$ 输入共 $2^n$ 行 | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型\|Logic Gates]] |
| 时序图 | Timing Diagram | — | 把两个或多个波形按时间画在一起，用来看逻辑关系与延迟 | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型\|Logic Gates]] |
| 逻辑表达式 | Logic Expression | — | 用代数式描述门的功能，取反用变量上的横线表示 | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型\|Logic Gates]] |
| 负逻辑 | Negative Logic | — | 电平到布尔值的映射为LOW→1、HIGH→0；与控制端低有效不是同一个概念 | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型\|Logic Gates]] |
| 反相气泡 | Inversion Bubble | — | 门符号边界上的圆圈表示取补；气泡推移须同时处理全部相应输入 | [[Universal Gates and Bubble Pushing#3 · Bubble Pushing · 全部气泡同步移动\|Bubble Pushing]] |
| 逻辑电平 | Logic Level | — | 用离散电压区间表示 1 与 0，而不是某个精确电压值 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 输入低电平上限 | Input Low Voltage | $V_{IL}$ | 能被可靠识别为 0 的最高输入电压 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 输入高电平下限 | Input High Voltage | $V_{IH}$ | 能被可靠识别为 1 的最低输入电压 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 输出低电平上限 | Output Low Voltage | $V_{OL}$ | 输出为 0 时保证不超过的电压 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 输出高电平下限 | Output High Voltage | $V_{OH}$ | 输出为 1 时保证不低于的电压 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 过渡带 | Transition / Indeterminate Band | — | $V_{IL,max}<V_{in}<V_{IH,min}$ 的输入区间没有逻辑解释保证；噪声容限需另用输出保证与输入接受范围计算 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 供电电压缩放 | $V_{DD}$ Scaling | — | 不同工艺／接口使用不同额定供电；降低供电不能自动保证输入耐压、电平兼容或时序满足 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 逻辑门家族 | Logic Family | — | TTL / CMOS / LVTTL / LVCMOS 等，用 $V_{IL},V_{IH},V_{OL},V_{OH}$ 四参数刻画兼容性 | [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围\|Logic Levels]] |
| 噪声 | Noise | — | 任何使信号退化的因素：电阻压降、电源波动、邻线耦合等 | [[Logic Levels and Noise Margins#3 · Noise Margin · 接口的预算\|Noise Margin]] |
| 噪声容限 | Noise Margin | $NM_H,NM_L$ | 还能容忍多少噪声：$NM_H=V_{OH}-V_{IH}$、$NM_L=V_{IL}-V_{OL}$ | [[Logic Levels and Noise Margins#3 · Noise Margin · 接口的预算\|Noise Margin]] |
| 高/低噪声容限 | High / Low Noise Margin | $NM_H/NM_L$ | 高电平方向与低电平方向各自剩余的电压余量 | [[Logic Levels and Noise Margins#3 · Noise Margin · 接口的预算\|Noise Margin]] |
| 直流传输特性 | DC Transfer Characteristic | VTC | 输出电压对输入电压的曲线 $V_{out}(V_{in})$；理想为阶跃 | [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力\|DC Transfer Characteristic]] |
| 开关阈值 | Switching Threshold | $V_M$ | VTC上 $V_{in}=V_{out}$ 的点；不能直接代替输入保证阈值，曲线斜率也不足以单独决定噪声容限 | [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力\|DC Transfer Characteristic]] |

## Ch4 · Boolean Algebra and Minimization · 布尔代数与化简

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 组合电路 | Combinational Circuit | — | 无记忆、输出只由当前输入决定的逻辑电路 | [[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型\|Combinational Circuit]] |
| 组合构成规则 | Rules of Combinational Composition | — | 元件皆组合、每个节点要么是输入要么只接一个输出、无环路 | [[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型\|Combinational Circuit]] |
| 布尔方程 | Boolean Equation | — | 用输入变量表达输出的功能规范 | [[Boolean Algebra and Circuit Models#2 · Boolean Equation · 从需求写函数\|Boolean Equation]] |
| 布尔公理 | Boolean Axioms | A1–A5 | 布尔代数的最小假设集合；每条都有对偶式 | [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则\|Boolean Axioms]] |
| 对偶性 | Duality | — | 把 AND↔OR、0↔1 互换得到对偶式，定理与其对偶同时成立 | [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则\|Boolean Axioms]] |
| 布尔定律 | Laws of Boolean Algebra | — | 交换律、结合律、分配律 | [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则\|Laws and Rules of Boolean Algebra]] |
| 布尔规则 | Rules of Boolean Algebra | 12 条 | 化简常用恒等式；第 10–12 条（$A+AB=A$、$A+\bar AB=A+B$、$(A+B)(A+C)=A+BC$）最常用 | [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则\|Laws and Rules of Boolean Algebra]] |
| 完全归纳法 | Perfect Induction | — | 穷举全部输入组合来证明两式相等，也称 proof by exhaustion | [[Boolean Algebra and Circuit Models#5 · Proof by Perfect Induction · 穷举与代数验证\|Proof by Perfect Induction]] |
| 德摩根定理 | DeMorgan's Theorems | — | $\overline{XY}=\bar X+\bar Y$、$\overline{X+Y}=\bar X\bar Y$ | [[Boolean Algebra and Circuit Models#4 · DeMorgan's Theorems · 取补必须覆盖整个子式\|DeMorgan's Theorems]] |
| 逻辑化简 | Logic Simplification | — | 用公理与规则把表达式化成门数/级数更少的形式 | [[Boolean Forms and Algebraic Simplification#4 · Boolean Expression Simplification · 保持函数再比较代价\|Boolean Expression Simplification]] |
| 补变量 | Complement | $\bar A$ | 变量取反后的形式 | [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项\|Minterm and Maxterm]] |
| 文字 | Literal | — | 一个变量或它的补（$A$ 或 $\bar A$） | [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项\|Minterm and Maxterm]] |
| 蕴含项 | Implicant | — | 若干文字的乘积 | [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项\|Minterm and Maxterm]] |
| 最小项 | Minterm | $m_i$ | 含全部输入变量的乘积，只在一行取 1 | [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项\|Minterm and Maxterm]] |
| 最大项 | Maxterm | $M_i$ | 含全部输入变量的和，只在一行取 0；$M_i=\bar m_i$ | [[Boolean Forms and Algebraic Simplification#1 · Minterm and Maxterm · 一行对应一个项\|Minterm and Maxterm]] |
| 与或式 | Sum-of-Products | SOP | 积之和；由真值表取输出为 1 的行 | [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式\|Sum-of-Products Form]] |
| 或与式 | Product-of-Sums | POS | 和之积；由真值表取输出为 0 的行 | [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式\|Product-of-Sums Form]] |
| 标准与或式 | Standard SOP | — | 每一项都含**全部**输入变量的 SOP（可编号成 $\sum m(\cdot)$） | [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式\|Sum-of-Products Form]] |
| 标准或与式 | Standard POS | — | 每一项都含**全部**输入变量的 POS（可编号成 $\prod M(\cdot)$） | [[Boolean Forms and Algebraic Simplification#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式\|Product-of-Sums Form]] |
| 变量域 | Domain | — | 函数涉及的全部输入变量集合，决定标准形式要补哪些变量 | [[Boolean Forms and Algebraic Simplification#2 · Truth Table and Boolean Expression · 用真值表定义全集\|Truth Table and Boolean Expression]] |
| 卡诺图 | Karnaugh Map | K-Map | 把真值表按格雷码排成方格的图形化简法 | [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并\|Karnaugh Map]] |
| 相邻格 | Adjacent Cells | — | 只差一个变量的两格；卡诺图靠行列 Gray 码保证这一点 | [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并\|Karnaugh Map]] |
| 圈组 | Grouping / Circling | — | 把相邻的 1（或 0）圈成 2 的幂大小的矩形，读出积项（和项） | [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并\|Karnaugh Map]] |
| 无关项 | Don't Care | X | 输出取值无所谓的输入组合；只在能让圈变大时才圈 | [[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务\|Karnaugh Map with Don't Cares]] |
| 最小与或式 | Minimum SOP | — | 覆盖全部指定 1、避开指定 0，按项数及文字数比较的最小积之和 | [[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并\|Karnaugh Map]] |
| 最小或与式 | Minimum POS | — | 覆盖全部指定 0、避开指定 1，按项数及文字数比较的最小和之积 | [[Karnaugh Map Minimization#3 · POS Minimization with Karnaugh Map · 圈 0 读和项\|POS Minimization with Karnaugh Map]] |

## Ch5 · Combinational Analysis and Design · 组合逻辑分析与设计

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 与或逻辑与与或非逻辑 | AND-OR and AND-OR-Invert Logic | — | SOP 门级实现及其整体取补；区分传感器电平与报警事件 | [[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构\|AND-OR and AND-OR-Invert Logic]] |
| 与或逻辑 | AND-OR Logic | — | 第一层产生乘积项，第二层 OR 合并，实现 SOP | [[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构\|AND-OR and AND-OR-Invert Logic]] |
| 与或非逻辑 | AND-OR-Invert Logic | AOI | $Y=\overline{P_1+\cdots+P_k}$，经德摩根变换可写成 POS | [[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构\|AND-OR and AND-OR-Invert Logic]] |
| 组合逻辑设计 | Combinational Logic Design | — | 从规范建立完整真值表、化简、选门并穷举核验；注意 exactly / at least | [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门\|Combinational Logic Design]] |
| 组合逻辑分析 | Combinational Logic Analysis | — | 从连接逐节点写方程，再用德摩根、吸收律或卡诺图恢复并化简函数 | [[Combinational Logic Analysis and Design#5 · Combinational Logic Analysis · 从连接恢复函数\|Combinational Logic Analysis]] |
| 两级逻辑 | Two-Level Logic | — | 主 AND→OR 或 OR→AND 结构的两级；通常不计输入反相器，不代表仅两个门 | [[Combinational Logic Analysis and Design#2 · AND-OR and AND-OR-Invert Logic · 形式落到结构\|AND-OR and AND-OR-Invert Logic]] |
| 通用门与气泡推移 | Universal Gates and Bubble Pushing | — | NAND/NOR 功能完备；交换 AND/OR 门体并同步移动全部取补 | [[Universal Gates and Bubble Pushing]] |
| 气泡推移 | Bubble Pushing | — | 用德摩根定理重画等价门符号，同一路径连续的两个逻辑补可抵消 | [[Universal Gates and Bubble Pushing]] |
| 输入反相的或门 | Negative-OR | — | $\bar A+\bar B=\overline{AB}$，是 NAND 的等价符号 | [[Universal Gates and Bubble Pushing]] |
| 输入反相的与门 | Negative-AND | — | $\bar A\bar B=\overline{A+B}$，是 NOR 的等价符号 | [[Universal Gates and Bubble Pushing]] |
| 数字逻辑故障诊断 | Digital Logic Troubleshooting | — | Activate a stuck-at fault, propagate its effect, choose distinguishing tests, and check physical-model boundaries · 故障敏化与诊断。 | [[Digital Logic Troubleshooting]] |
| 粘连故障 | Stuck-at fault | SA0/SA1 | A node is modeled constantly0/1; 是逻辑故障模型。 | [[Digital Logic Troubleshooting]] |
| 故障敏化 | Fault activation | — | Drive the healthy node opposite to its faulty value; 再令差异传播到可观察输出。 | [[Digital Logic Troubleshooting]] |

## Ch6 · Combinational Building Blocks · 组合功能块

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 半加器 | Half Adder | HA | 用 XOR 得 Sum、AND 得 Carry 的两位相加电路 | [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒\|Half Adder and Full Adder]] |
| 七段译码器 | Seven-Segment Decoder | — | Map BCD to segment commands; 非法码策略与极性须规定 | [[Seven-Segment Display and Code Conversion]] |
| 优先电路 | Priority Circuit | — | 按优先级只断言最高有效输入对应的获胜线路 | [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码\|Encoder and Priority Encoder]] |
| 独热获胜掩码 | One-Hot Winner Mask | — | 每个获胜输入对应一条输出；最多一位为 1，区别于二进制位置码 | [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码\|Encoder and Priority Encoder]] |
| 三态缓冲器与总线驱动 | Tri-State Buffers and Bus Drivers | — | Enable, high impedance, bus ownership and contention · 三态与总线驱动。 | [[Tri-State Buffers and Bus Drivers]] |
| 半加器与全加器 | Half Adder and Full Adder | — | Sum/parity and carry/majority equations, truth tables, conservation and cascading · 加法单元。 | [[Binary Arithmetic Circuits#1 · Half Adder and Full Adder · 位权守恒\|Half Adder and Full Adder]] |
| 串行进位与超前进位加法器 | Ripple Carry and Carry Look-Ahead Adders | — | Propagate/generate conventions, expanded carry equations, arithmetic and path delay · RCA/CLA。 | [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径\|Ripple Carry and Carry Look-Ahead Adders]] |
| 二进制减法器与加减器 | Binary Subtractors and Adder-Subtractors | — | Difference/borrow derivation, mode-controlled inversion, carry versus signed overflow · 减法与加减器。 | [[Binary Arithmetic Circuits#3 · Binary Subtractors and Adder-Subtractors · 共用数据通路\|Binary Subtractors and Adder-Subtractors]] |
| 组合乘法器 | Combinational Multiplier | — | AND partial products, weighted column addition, complete 3×3 design and signed boundary · 组合乘法器。 | [[Binary Arithmetic Circuits#4 · Combinational Multiplier · 从部分积到列加法\|Combinational Multiplier]] |
| 数值比较器 | Magnitude Comparator | — | Highest unequal bit, equality gating and cascade · 多位比较器。 | [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小\|Magnitude Comparator]] |
| 编码器与优先编码器 | Encoder and Priority Encoder | — | One-hot/one-cold coding, priority, multiple inputs and valid output · 编码与优先级。 | [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码\|Encoder and Priority Encoder]] |
| 译码器 | Decoder | — | Minterm generation, active-low output combination, enables and expansion · 译码器。 | [[Comparison Decoding and Selection#2 · Decoder · 代码变线路\|Decoder]] |
| 多路选择器与分配器 | Multiplexer and Demultiplexer | — | Shannon expansion, cofactors, selection and routing · MUX/DEMUX。 | [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配\|Multiplexer and Demultiplexer]] |
| 传播延迟与逻辑冒险 | Propagation Delay and Logic Hazards | — | Longest/shortest paths, static hazards, consensus and sampling boundaries · 延迟与冒险。 | [[Propagation Delay and Logic Hazards]] |
| 七段显示与码制转换 | Seven-Segment Display and Code Conversion | — | Segment/polarity table, blanking and zero suppression, scanning, and two-adder BCD conversion · 显示综合。 | [[Seven-Segment Display and Code Conversion]] |
| 高阻 | High impedance | Z | Driver released; 不是强制0或未知X。 | [[Tri-State Buffers and Bus Drivers]] |
| 有效指示 | Valid indicator | V | Separates a meaningful code from no input; 区分零编号与无输入。 | [[Comparison Decoding and Selection#3 · Encoder and Priority Encoder · 线路变代码\|Encoder and Priority Encoder]] |
| 进位传播 | Carry propagate | P | Carries an incoming carry under the declared OR/XOR convention; sum仍用XOR。 | [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径\|Ripple Carry and Carry Look-Ahead Adders]] |
| 进位产生 | Carry generate | G | Both operand bits are1, producing carry independent of carry-in; 本位独立产生进位。 | [[Binary Arithmetic Circuits#2 · Ripple Carry and Carry Look-Ahead Adders · 进位决定路径\|Ripple Carry and Carry Look-Ahead Adders]] |
| 消隐 | Blanking | BI | Force display off; 与无效输入的don’t-care不同。 | [[Seven-Segment Display and Code Conversion]] |
| 零抑制 | Zero suppression | RBI/RBO | Hide insignificant zeros through a controlled chain; 保留内部有意义的0。 | [[Seven-Segment Display and Code Conversion]] |
| 最小污染延迟 | Contamination delay | t_cd | Earliest possible output change after an input change; 最短路径用于hold检查。 | [[Propagation Delay and Logic Hazards]] |

## Ch7 · State and Storage Elements · 状态与存储元件

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 时序逻辑 | Sequential Logic | — | Old state → next state, common-clock discipline, feedback and initialization · 时序逻辑模型。 | [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在\|Sequential Logic]] |
| 置位复位锁存器 | Set-Reset Latch | — | NOR/NAND polarity, bistability, hold/set/reset and forbidden condition · SR锁存器。 | [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆\|Set-Reset Latch]] |
| D锁存器与D触发器 | D Latch and D Flip-Flop | — | Transparent level versus active edge, master–slave idea and waveform tracing · D存储元件。 | [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿\|D Latch and D Flip-Flop]] |
| JK与T触发器 | JK and T Flip-Flops | — | Characteristic/excitation tables, toggle and FF conversion · JK/T触发器。 | [[Sequential Logic and Flip-Flops#4 · JK and T Flip-Flops · 条件更新\|JK and T Flip-Flops]] |
| 寄存器使能与复位 | Register Enable and Reset | — | Data hold/load, synchronous/asynchronous reset, priority and reset release · 寄存器控制。 | [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级\|Register Enable and Reset]] |
| 有效低 | Active-low | _N / bar | Asserted at logic LOW; 电平0表示控制已有效。 | [[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级\|Register Enable and Reset]] |
| 下一状态 | Next state | Q+ | State captured at next specified event; 由旧Q和当前输入计算。 | [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在\|Sequential Logic]] |
| 激励表 | Excitation table | — | Required FF inputs for a current-to-next transition; 与characteristic table方向不同。 | [[Sequential Logic and Flip-Flops#4 · JK and T Flip-Flops · 条件更新\|JK and T Flip-Flops]] |

## Ch8 · Shift and Pulse Applications · 移位与脉冲应用

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 移位寄存器实现 | Shift-Register Implementation | LFSR | Serial state update with XOR taps; 位宽与抽头由生成多项式及输入约定决定，见 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式\|Shift Registers]] | [[Parity and Cyclic Redundancy Checks#3 · Cyclic Redundancy Check · 改用多项式余数\|Cyclic Redundancy Check]] |
| 移位寄存器 | Shift Registers | — | SISO/SIPO/PISO/PIPO, universal modes, explicit left/right order, delay and serial conversion · 移位寄存器。 | [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式\|Shift Registers]] |
| 环形与约翰逊计数器 | Ring and Johnson Counters | — | Feedback sequences, n versus 2n states, duty cycle and illegal initialization · 环形/Johnson。 | [[Shift Registers and Ring Counters#3 · Ring and Johnson Counters · 同样的移位，不同的反馈\|Ring and Johnson Counters]] |
| 单稳态与脉冲应用 | One-Shots and Pulse Applications | — | Monostable/astable behavior, RC threshold derivation and registered event pulses · 单稳态与脉冲。 | [[One-Shots and Pulse Applications]] |
| 键盘扫描与编码 | Keyboard Scanning and Encoding | — | One-cold scan, row/column encoding, debounce, valid capture and six-bit key register · 键盘综合。 | [[Keyboard Scanning and Encoding]] |
| 扫描槽频率 | Scan slot rate | f_slot | Rate of one selected position update; 完整frame rate为slot rate除以位置数。 | [[Keyboard Scanning and Encoding]] |
| 独冷编码 | One-cold encoding | — | Exactly one bit LOW in a valid code; 课程键盘扫描使用。 | [[Keyboard Scanning and Encoding]] |
| 单稳态 | Monostable | One-shot | One stable state; trigger produces a timed excursion and return。 | [[One-Shots and Pulse Applications]] |

## Ch9 · State Machines and Timing · 状态机与时序

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 建立与保持时间 | Setup and Hold Timing | — | Maximum/minimum arrival derivations, slack, skew, hold repair and frequency limits · 建立/保持时间。 | [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准\|Setup and Hold Timing]] |
| 亚稳态与时钟域跨越 | Metastability and Clock Domain Crossing | — | Single-bit synchronizer, pulse/multi-bit boundaries and coherent transfer · 亚稳态与CDC补充。 | [[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界\|Metastability and Clock Domain Crossing]] |
| 有限状态机 | Finite State Machine | — | State meaning, diagram/table/equations, output logic and verification · FSM设计。 | [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史\|Finite State Machine]] |
| Moore与Mealy状态机 | Moore and Mealy Machines | — | State-only versus state/input outputs, response timing and alignment · Moore/Mealy比较。 | [[Finite State Machine Design and Applications#2 · Moore and Mealy Machines · 输出依赖与时间对齐\|Moore and Mealy Machines]] |
| 状态编码与未用状态 | State Encoding and Unused States | — | Binary/one-hot choices, don't-cares, initialization and recovery · 编码与未用状态。 | [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复\|State Encoding and Unused States]] |
| 序列检测器 | Sequence Detector | — | Longest reusable suffix, overlap, state equations and serial trace · 序列检测。 | [[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀\|Sequence Detector]] |
| 交通灯控制器 | Traffic Light Controller | — | Traffic states, sensor-controlled transitions, output coding and timer extension · 交通灯控制。 | [[Finite State Machine Design and Applications#5 · Traffic Light Controller · 安全条件进入状态模型\|Traffic Light Controller]] |
| 建立时间 | Setup time | t_setup | Required stability before capture; 最迟到达须早于capture减setup。 | [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准\|Setup and Hold Timing]] |
| 保持时间 | Hold time | t_hold | Required stability after capture; same-edge earliest-arrival约束。 | [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准\|Setup and Hold Timing]] |
| 时钟到输出延迟 | Clock-to-Q delay | t_cq | Capture edge to changed Q; 区分最小t_ccq与最大t_pcq。 | [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准\|Setup and Hold Timing]] |
| 时钟偏斜 | Clock skew | s | Difference in clock arrival; 本库s为capture比launch晚。 | [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准\|Setup and Hold Timing]] |
| 时间裕量 | Timing slack | — | Available time minus required time under the stated check; 负值表示违反。 | [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准\|Setup and Hold Timing]] |
| 亚稳态 | Metastability | — | Storage element temporarily lacks a valid stable logic output; 同步器降低传播风险。 | [[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界\|Metastability and Clock Domain Crossing]] |
| 独热编码 | One-hot encoding | — | Exactly one bit asserted in a valid state; 需初始化与非法态策略。 | [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复\|State Encoding and Unused States]] |

## Ch10 · Counters and Digital Clocks · 计数器与数字时钟

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 计数器 | Counters | — | Modulus, ripple/common-clock behavior, up/down toggling and control semantics · 计数基础。 | [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构\|Counters]] |
| 同步计数器设计 | Synchronous Counter Design | — | D/JK excitation synthesis, modulo-3 recovery and a specified eight-state cycle · 同步计数设计。 | [[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励\|Synchronous Counter Design]] |
| 级联计数器与数字时钟 | Cascaded Counters and Digital Clocks | — | Accepted rollover, mixed radix, 59→00, frequency/pulse duty and preset truncation · 级联与数字时钟。 | [[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转\|Cascaded Counters and Digital Clocks]] |
| 模数 | Modulus | M | Number of distinct states in repeating cycle; 不是任意序列最大数值加1。 | [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构\|Counters]] |
| 末态 | Terminal count | TC | Decode of designated last state; 接受的rollover还需要enable。 | [[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转\|Cascaded Counters and Digital Clocks]] |

## Ch11 · Memory and Programmable Logic · 存储与可编程逻辑

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 存储阵列与扩展 | Memory Arrays and Expansion | — | Depth/width/capacity, address units, bank selection and chip expansion · 存储组织。 | [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量\|Memory Arrays and Expansion]] |
| SRAM、DRAM与ROM | SRAM DRAM and ROM | — | Feedback versus charge, refresh/volatility, nonvolatile variants and mechanism examples · 存储技术。 | [[Memory Organization and Technologies#3 · SRAM DRAM and ROM · 保存机制决定操作\|SRAM DRAM and ROM]] |
| ROM与可编程逻辑阵列 | Read-Only Memory and Programmable Logic Arrays | — | Multi-output truth-table lookup, LUTs and programmable AND/OR arrays · ROM/LUT/PLA/PAL。 | [[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积\|Read-Only Memory and Programmable Logic Arrays]] |
| 现场可编程门阵列 | Field-Programmable Gate Array | — | LUT/FF/routing, simulation/synthesis/implementation and clock/I/O constraints · FPGA流程。 | [[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现\|Field-Programmable Gate Array]] |
| 存储深度 | Memory depth | D | Number of addressable words; 与每word位宽分开。 | [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量\|Memory Arrays and Expansion]] |
| 易失性 | Volatility | — | Contents are not retained after loss of sustaining power; SRAM和DRAM均通常易失。 | [[Memory Organization and Technologies#3 · SRAM DRAM and ROM · 保存机制决定操作\|SRAM DRAM and ROM]] |
| 查找表 | Lookup table | LUT | Inputs address fixed truth bits during logic operation; user state另由FF保存。 | [[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积\|Read-Only Memory and Programmable Logic Arrays]] |
| 时序收敛 | Timing closure | — | Mapped constrained design satisfies timing requirements; 功能仿真通过不能单独证明。 | [[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现\|Field-Programmable Gate Array]] |

## HDL · VHDL and Project Verification · VHDL 与项目验证

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| VHDL语言与建模 | VHDL Language and Modeling | — | Entity/architecture, types, concurrent/process semantics, signal/variable and reset patterns · VHDL语言。 | [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现\|VHDL Language and Modeling]] |
| 结构化双向移位寄存器项目 | Structural Shift Register Project | — | Complete DFF + structural bidirectional register, explicit bit order and implementation checks · 结构化项目。 | [[Structural Shift Register Project]] |
| 测试平台与功能验证 | Testbench and Functional Verification | — | Complete directed testbench, independent reference model, delta cycles and coverage · 测试与验证。 | [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照\|Testbench and Functional Verification]] |
| 实体与体系结构 | Entity / architecture | — | Interface / implementation in VHDL; 硬件端口与实现分离。 | [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现\|VHDL Language and Modeling]] |
| 端口映射 | Port map | — | Connect instance ports to actual signals; named association明确连接。 | [[Structural Shift Register Project]] |
| 零时间调度周期 | Delta cycle | — | Simulation updates without elapsed physical time; 不等于真实门延迟。 | [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现\|VHDL Language and Modeling]] |
| 被测设计 | Design under test | DUT | Implementation driven and checked by the testbench; 参考模型来自规范。 | [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照\|Testbench and Functional Verification]] |

## Review · Integrated Review · 综合复习

| Chinese term | English term | Abbreviation | Definition · 中文释义 | Note |
|---|---|---|---|---|
| 考试复习与解题方法 | Exam Review and Problem Solving | — | Question wording, representation/polarity/timing decisions, worked mini-problems and English answer patterns · 考试复习。 | [[Exam Review and Problem Solving]] |

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
