---
tags:
  - ECE2050
  - memory
date: 2026-09-30
aliases:
  - SRAM、DRAM与ROM
  - SRAM DRAM and ROM
  - Memory technologies
---

# SRAM DRAM and ROM · SRAM、DRAM与ROM

> [!SUMMARY] Quick recall · 英文速览
> SRAM stores state with feedback; DRAM stores charge and needs refresh. Both conventional RAM types are volatile. ROM-family storage is nonvolatile, but modern reprogrammable variants have distinct write and erase rules.

## Core Definition · 核心定义

volatile 指断电后不保证保存内容；nonvolatile 指在规定条件下断电仍可保持。Static 指不需要周期 refresh，**不表示断电不丢失**。Dynamic 指 stored charge 需要恢复，并不是“动态可变编程”。

| Technology | Storage mechanism | Refresh | Power-off retention | Typical role |
|---|---|---|---|---|
| SRAM | Bistable feedback, often 6T cell | No periodic refresh | Volatile | Fast buffers/cache |
| DRAM | Capacitor charge, basic 1T1C model | Required | Volatile | Dense main memory |
| Mask ROM | Fabricated connections/data | No | Nonvolatile | Fixed lookup data |
| EEPROM/Flash | Programmable nonvolatile cells | No DRAM-style refresh | Nonvolatile within rated conditions | Persistent configuration/data |

Exact speed, density, endurance, and retention are device-specific. The comparison explains mechanisms; it is not a source of universal numerical guarantees.

## SRAM Mechanism · SRAM 机制

交叉 inverter 的两个稳定状态保存 Q，与 [[Set-Reset Latch]] 的 bistable 原理相近。access transistors 在 wordline 有效时连接 bitlines，用于读写。具体 6T SRAM 的 read/write stability 还涉及 transistor strength，不能把任意 NOR latch 直接当真实 bit-cell schematic。

As long as power and operating conditions are maintained, the feedback restores the stored logic level without periodic refresh. Losing power removes that sustaining mechanism.

## DRAM Mechanism · DRAM 机制

电容存电荷 $Q=CV$；leakage current $I$ 使近似电压损失 $\Delta V=I\Delta t/C$，因此隔一段时间需 refresh。教学读模型是 charge sharing，reading perturbs stored charge，sense amplifier 判定并 restore；外部看来一次正常 read 不应把用户数据丢掉。

**Illustrative check.** C=30 fF、leakage=1 fA、允许下降0.1 V，则 $\Delta t=C\Delta V/I=3$ s。若 I=100 fA，同样模型得30 ms。这个例子说明 leakage 与 refresh 间隔关系，不是任何 DRAM 的规定刷新时间。

## ROM and Reprogramming · ROM 与重写

Mask ROM 在制造时固定；PROM 常为一次编程；EPROM/EEPROM/Flash 可按各自机制擦写。Flash 通常按 block erase、按较小单位 program，有 endurance 限制。课程广义 ROM 类包括这些非易失存储，但它们不是“永远不可写”的同一器件。

Memory used as a truth-table lookup is conceptually separate from the technology storing its entries. A RAM initialized with a table can perform the same combinational lookup function as a ROM if its read interface supplies the required timing and the entries remain unchanged.

## Worked Examples and Review · 例题与复习

**Power loss.** SRAM 里计数值123、Flash 里参数123。断电后 SRAM 不保证保留；Flash 的保留也需符合器件条件，不是无限年承诺。

**Classification.** “DRAM must periodically refresh” is correct in the usual model. “SRAM is nonvolatile” is false. “Random access means read-only” is false; access pattern and writability are different dimensions.

**Exam answer:** “SRAM uses a stable feedback state and needs power but no periodic refresh. DRAM uses stored charge that leaks and is disturbed by sensing, so refresh and restoration preserve the data.”

## Connections · 相关笔记

[[Memory Arrays and Expansion]], [[Set-Reset Latch]], [[Read-Only Memory and Programmable Logic Arrays]], [[Field-Programmable Gate Array]], [[Digital Abstraction and System Design]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
