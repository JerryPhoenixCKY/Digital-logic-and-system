---
tags:
  - ECE2050
  - memory
date: 2026-09-30
aliases:
  - 存储阵列与扩展
  - Memory Arrays and Expansion
  - Memory depth and width
---

# Memory Arrays and Expansion · 存储阵列与扩展

> [!SUMMARY] Quick recall · 英文速览
> N address bits select $2^N$ words. M data bits determine word width. Increasing width and increasing depth require different connections; capacity in bits is depth times width.

## Core Definition · 核心定义

存储阵列 (memory array) 有 depth 个 word，每个 word 含 width 个 bit。N-bit address、M-bit word 的教学模型：

$$D=2^N\text{ words},\quad W=M\text{ bits/word},\quad C=2^NM\text{ bits}.$$

地址 (address) 是位置，不是所存 data value；word line 选择行，bit lines 连接各列。enable 的实际极性与读写时序取决于具体 memory interface。

## Derivation · 行列与译码

每个地址模式对应一行，[[Decoder]] 将 binary address 转为 one-hot row selection；被选行向 M 个数据端输出/接收 word。若芯片有 row/column multiplexed address，外部引脚数与完整地址位数可能不一样，不能机械套用“引脚数=N”。

Random access means locations can be directly selected by address. It does not mean random contents or that all accesses have identical latency in every modern memory organization.

## Worked Example 1 · 容量与地址

8K×16 表示 8192 words，每 word=16 bit。N=13；capacity=$8192\times16=131072$ bit=16384 byte=16 KiB。word 地址范围 0x0000–0x1FFF。若系统 byte-addressed，则映射整个 16 KiB 区域需要考虑每 word 两个 byte，不能直接把 word address 当 byte address。

**Small lookup.** $2^2\times3$ memory 有 4 words、每 word3位、总12 bit；地址10只选择第三行，不表示“读数值 2”。

## Width Expansion · 位宽扩展

两片 8K×8 组成 8K×16：共享同一 address 与正确读写控制，一片数据接低8位，一片接高8位，两片一起选中。depth 不变，width 加倍。

Do not connect both chips to the same eight data wires when the goal is width expansion. That creates two drivers on each wire instead of a sixteen-bit word.

## Depth Expansion · 深度扩展

两片 8K×8 组成 16K×8：低13位地址同时接两片；第14位地址选择 chip；数据线共用，但仅被选片可驱动。depth 加倍，width 不变。

四片 8K×8 构造 16K×16：两个 bank，每 bank 两片并排扩宽；地址高位选 bank，各 bank 内两片同步工作。所需数量=(16K/8K)×(16/8)=4。

## Interface and Timing · 接口与时序

读操作不一定是组合 read：异步 memory 可在地址稳定后输出；同步 memory 可能在 clock 边沿采地址并在稍后输出。Write enable、chip select、output enable 与 tri-state bus rules 必须一起检查。

For depth expansion, inactive chips must release a shared read bus or be selected through explicit multiplexing. A correct capacity calculation alone does not specify a working bus interface.

## Method and Review · 方法与复习

1. Normalize K/M prefixes into the specified word counts.
2. Calculate address bits from depth, not capacity in bits.
3. Calculate bit capacity and convert to bytes if divisible by eight.
4. Draw bank/width grouping and chip-select conditions.
5. Check bus ownership and read/write timing.

**Exam question:** Does doubling the word width require another address bit?

**Answer:** No. The same number of words is still addressed. Doubling depth requires one additional binary address bit for a power-of-two organization; doubling width increases the number of data bits instead.

## Connections · 相关笔记

[[Bits and Bytes]], [[Hexadecimal Number System]], [[Decoder]], [[Tri-State Buffers and Bus Drivers]], [[SRAM DRAM and ROM]], [[Read-Only Memory and Programmable Logic Arrays]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
