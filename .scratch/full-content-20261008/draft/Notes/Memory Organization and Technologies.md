---
tags:
  - ECE2050
  - memory
date: 2026-09-30
updated: 2026-10-09
chapter: Ch11
aliases:
  - 存储组织与存储技术
  - Memory Organization and Technologies
  - 存储组织与存储技术 · Ch11
  - Memory Arrays and Expansion
  - 存储阵列与扩展
  - Memory depth and width
  - SRAM DRAM and ROM
  - SRAM、DRAM与ROM
  - Memory technologies
---

# Memory Organization and Technologies · 存储组织与存储技术

> [!SUMMARY] Quick recall · 英文速览
> Depth and width define memory capacity. Technology explains how a bit is retained, read, written, and lost.

## 1 · Memory Arrays and Expansion · 寻址与容量

深度 D 表示可寻址 word 数，位宽 W 表示每 word 的 bit 数；容量 $C=DW$ bit。若有 $D=2^a$ 个 word，需 a 根地址线。先声明地址按 bit、byte 还是 word 编号。

### Core Definition · 核心定义

存储阵列 (memory array) 有 depth 个 word，每个 word 含 width 个 bit。N-bit address、M-bit word 的教学模型：

$$D=2^N\text{ words},\quad W=M\text{ bits/word},\quad C=2^NM\text{ bits}.$$

地址 (address) 是位置，不是所存 data value；word line 选择行，bit lines 连接各列。enable 的实际极性与读写时序取决于具体 memory interface。

### Capacity units · 容量单位与非二幂深度

本课容量例题中的 8K words 约定为 $8\times1024=8192$ words；容量用 KiB 明确二进制字节前缀。十进制 k/M 与二进制 Ki/Mi 不能混算。若实际深度 D 不是二的整数次幂，需要 $a=\lceil\log_2D\rceil$ 个地址 bit，但 $2^a-D$ 个地址模式不对应有效 word，应规定其行为。数据线数对应 W，不是 C；扩大 W 而不扩大 D 不增加逻辑地址位数。

> [!example]- Memory Arrays and Expansion · 推导与例题
> **Derivation · 行列与译码**
>
> 每个地址模式对应一行，[[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 将 binary address 转为 one-hot row selection；被选行向 M 个数据端输出/接收 word。若芯片有 row/column multiplexed address，外部引脚数与完整地址位数可能不一样，不能机械套用“引脚数=N”。
>
> Random access means locations can be directly selected by address. It does not mean random contents or that all accesses have identical latency in every modern memory organization.
>
> **Worked Example 1 · 容量与地址**
>
> 8K×16 表示 8192 words，每 word=16 bit。N=13；capacity=$8192\times16=131072$ bit=16384 byte=16 KiB。word 地址范围 0x0000–0x1FFF。若系统 byte-addressed，则映射整个 16 KiB 区域需要考虑每 word 两个 byte，不能直接把 word address 当 byte address。
>
> **Small lookup.** $2^2\times3$ memory 有 4 words、每 word3位、总12 bit；地址10只选择第三行，不表示“读数值 2”。

### Method and Review · 方法与复习

1. Normalize K/M prefixes into the specified word counts.
2. Calculate address bits from depth, not capacity in bits.
3. Calculate bit capacity and convert to bytes if divisible by eight.
4. Draw bank/width grouping and chip-select conditions.
5. Check bus ownership and read/write timing.

**Exam question:** Does doubling the word width require another address bit?

**Answer:** No. The same number of words is still addressed. Doubling depth requires one additional binary address bit for a power-of-two organization; doubling width increases the number of data bits instead.

### Connections · 概念关系与应用

[[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|Bits and Bytes]] 与 [[Number Systems and Base Conversion#2 · Decimal, Binary, Octal and Hexadecimal · 四种进制的统一解释|Hexadecimal Number System]] 提供容量单位和地址范围；[[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 选行/选 bank，[[Tri-State Buffers and Bus Drivers]] 管共享读总线；[[Memory Organization and Technologies#3 · SRAM DRAM and ROM · 保存机制决定操作|SRAM DRAM and ROM]] 解释保存机制，[[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积|Read-Only Memory and Programmable Logic Arrays]] 把组织用于真值表实现。

## 2 · 扩展先宽度，后深度

并联数据位可扩展 W，地址与片选相同；增加深度用高位地址译码选 bank，低位地址送各片。扩展到目标深度与宽度所需片数分别相乘，并检查输出三态／使能避免多片同时驱动。

### Width Expansion · 位宽扩展

两片 8K×8 组成 8K×16：共享同一 address 与正确读写控制，一片数据接低8位，一片接高8位，两片一起选中。depth 不变，width 加倍。

Do not connect both chips to the same eight data wires when the goal is width expansion. That creates two drivers on each wire instead of a sixteen-bit word.

### Depth Expansion · 深度扩展

两片 8K×8 组成 16K×8：低13位地址同时接两片；第14位地址选择 chip；数据线共用，但仅被选片可驱动。depth 加倍，width 不变。

四片 8K×8 构造 16K×16：两个 bank，每 bank 两片并排扩宽；地址高位选 bank，各 bank 内两片同步工作。所需数量=(16K/8K)×(16/8)=4。

## 3 · SRAM DRAM and ROM · 保存机制决定操作

SRAM 靠双稳态反馈保持，通常不需刷新；DRAM 靠电荷保存，需刷新且读操作涉及恢复；二者通常均易失。ROM 用非易失结构保存内容，不同可编程类型的擦写方式和限制不同。

### Core Definition · 核心定义

volatile 指断电后不保证保存内容；nonvolatile 指在规定条件下断电仍可保持。Static 指不需要周期 refresh，**不表示断电不丢失**。Dynamic 指 stored charge 需要恢复，并不是“动态可变编程”。

| Technology | Storage mechanism | Refresh | Power-off retention | Typical role |
|---|---|---|---|---|
| SRAM | Bistable feedback, often 6T cell | No periodic refresh | Volatile | Fast buffers/cache |
| DRAM | Capacitor charge, basic 1T1C model | Required | Volatile | Dense main memory |
| Mask ROM | Fabricated connections/data | No | Nonvolatile | Fixed lookup data |
| EEPROM/Flash | Programmable nonvolatile cells | No DRAM-style refresh | Nonvolatile within rated conditions | Persistent configuration/data |

Exact speed, density, endurance, and retention are device-specific. The comparison explains mechanisms; it is not a source of universal numerical guarantees.

> [!example]- SRAM DRAM and ROM · 推导与例题
> **SRAM Mechanism · SRAM 机制**
>
> 交叉 inverter 的两个稳定状态保存 Q，与 [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]] 的 bistable 原理相近。access transistors 在 wordline 有效时连接 bitlines，用于读写。具体 6T SRAM 的 read/write stability 还涉及 transistor strength，不能把任意 NOR latch 直接当真实 bit-cell schematic。
>
> As long as power and operating conditions are maintained, the feedback restores the stored logic level without periodic refresh. Losing power removes that sustaining mechanism.
>
> **DRAM Mechanism · DRAM 机制**
>
> 电容存电荷 $Q=CV$；leakage current $I$ 使近似电压损失 $\Delta V=I\Delta t/C$，因此隔一段时间需 refresh。教学读模型是 charge sharing，reading perturbs stored charge，sense amplifier 判定并 restore；外部看来一次正常 read 不应把用户数据丢掉。
>
> **Illustrative check.** C=30 fF、leakage=1 fA、允许下降0.1 V，则 $\Delta t=C\Delta V/I=3$ s。若 I=100 fA，同样模型得30 ms。这个例子说明 leakage 与 refresh 间隔关系，不是任何 DRAM 的规定刷新时间。
>
> **ROM and Reprogramming · ROM 与重写**
>
> Mask ROM 在制造时固定；PROM 常为一次编程；EPROM/EEPROM/Flash 可按各自机制擦写。Flash 通常按 block erase、按较小单位 program，有 endurance 限制。课程广义 ROM 类包括这些非易失存储，但它们不是“永远不可写”的同一器件。
>
> Memory used as a truth-table lookup is conceptually separate from the technology storing its entries. A RAM initialized with a table can perform the same combinational lookup function as a ROM if its read interface supplies the required timing and the entries remain unchanged.

### Connections · 概念关系与应用

逻辑组织见 [[Memory Organization and Technologies#1 · Memory Arrays and Expansion · 寻址与容量|Memory Arrays and Expansion]]；SRAM 的双稳态与 [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]] 相近。[[Programmable Logic and FPGA#1 · Read-Only Memory and Programmable Logic Arrays · 真值表与共享乘积|Read-Only Memory and Programmable Logic Arrays]] 使用存储作函数表，[[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现|Field-Programmable Gate Array]] 区分配置与运行状态；器件机制与 [[Digital Foundations and Waveforms#1 · Digital Abstraction and System Design · 从电压到信息|Digital Abstraction and System Design]] 的功能抽象要分开。

## 4 · 从物理存储到功能模型

“不刷新”不等于“掉电保存”；“只读”描述正常接口操作，不代表所有 ROM 类型永不可编程。存储技术、电气时序与逻辑组织是不同维度。

> [!IMPORTANT] 所有容量问题带单位
> 地址位数对应深度，数据线数对应位宽；总 bit 数除以 8 才是 byte 数。芯片数不能只按总容量凑数而忽略接口组织。

### Interface and Timing · 接口与时序

读操作不一定是组合 read：异步 memory 可在地址稳定后输出；同步 memory 可能在 clock 边沿采地址并在稍后输出。Write enable、chip select、output enable 与 tri-state bus rules 必须一起检查。

For depth expansion, inactive chips must release a shared read bus or be selected through explicit multiplexing. A correct capacity calculation alone does not specify a working bus interface.

> [!example]- SRAM DRAM and ROM · 推导与例题
> **Worked Examples and Review · 例题与复习**
>
> **Power loss.** SRAM 里计数值123、Flash 里参数123。断电后 SRAM 不保证保留；Flash 的保留也需符合器件条件，不是无限年承诺。
>
> **Classification.** “DRAM must periodically refresh” is correct in the usual model. “SRAM is nonvolatile” is false. “Random access means read-only” is false; access pattern and writability are different dimensions.
>
> **Exam answer:** “SRAM uses a stable feedback state and needs power but no periodic refresh. DRAM uses stored charge that leaks and is disturbed by sensing, so refresh and restoration preserve the data.”

## Sources · 课件依据

主线课件：[Ch11 lecture](../LGU_HUB_ECE2050/ECE2050-Chap11.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
