---
tags:
  - ECE2050
  - counters
date: 2026-09-30
aliases:
  - 级联计数器与数字时钟
  - Cascaded Counters and Digital Clocks
  - Terminal count and frequency division
---

# Cascaded Counters and Digital Clocks · 级联计数器与数字时钟

> [!SUMMARY] Quick recall · 英文速览
> Cascaded stages form a mixed-radix counter. A higher stage advances only when the lower stage wraps. In synchronous designs, keep a common clock and propagate an enable event rather than casually using decoded pulses as new clocks.

## Core Definition · 核心定义

低位 modulus $M_0$、高位 $M_1$，每低位完整循环让高位加一，则总 modulus=$M_0M_1$。推广到 k 级为 $\prod_iM_i$，前提是正确的 wrap/enable/load 行为。

Terminal count (TC) 指定最后有效状态的 decode；carry/rollover event 表示本次 clock 接受后会 wrap 的条件。两者不一定相同：禁用计数时 TC 可一直 HIGH，但不应让高位每拍都增加。

## Derivation · 同步级联

最低位 enable E0=global enable。高一级 $E_1=E_0\land(q_0=M_0-1)$；再一级 $E_2=E_1\land(q_1=M_1-1)$。所有 q 都从 edge 前状态读取。

For a synchronous load-on-terminal scheme, decode the last legal state M−1 so the next edge loads zero. Decoding M and then synchronously clearing on a later edge can introduce an extra state and change the modulus. Asynchronous clear-on-M uses a different timing model and may create short transient states.

## Worked Example 1 · 两级十进制

个位、十位各 mod10，组成 mod100。当前 09、E=1：个位 9→0、十位 0→1，同时变 10。当前 99：两位均 wrap 到 00。当前 09、E=0：保持 09，TC 虽为 1，但不产生接受事件。

若 input=10 kHz，个位 cycle=1 kHz，总 100-state cycle=100 Hz。两个 decade 级联是 divide-by-100，不是 divide-by-10。

## Worked Example 2 · 60进制时钟

seconds 0–59、minutes 0–59；当前 12:59:59，下一次 1 Hz tick 应得 13:00:00。更新前 seconds TC 与 minutes TC 同时为 1，因此小时 enable 在同一拍有效。

One possible two-digit seconds implementation uses units 0–9 and tens 0–5. Units rollover enables tens; tens rollover at 5 only matters when units also roll at 9. Decoding tens=5 alone would repeatedly advance minutes while displaying 50–59.

教学 12-hour 系统若用 1–12，12 后应加载 1；若编码 0–11，解码显示与 roll 条件需另外定义。不能把两个约定的 terminal state 混用。

## Worked Example 3 · Preset truncated count

16-bit full binary cycle 长度 65536。要求 modulus 40000，可从 preset P=65536−40000=25536=0x63C0 开始，数到 65535 后下一事件加载 P。

Number of visited states is $65535-25536+1=40000$. The +1 includes both endpoints. Check the loading event does not add an unintended separate waiting state; the scheme's count-enable and load semantics determine the actual cycle.

## Practical Timing · 实际时序

Decode glitches can falsely trigger a higher stage if used as a clock. A common-clock enable chain lets receiving FFs sample a condition under setup/hold constraints, although the enable path still contributes to critical timing.

For an odd modulus, a terminal decode pulse has one-cycle width and duty 1/M. The output repetition frequency is $f_{clk}/M$; pulse width and 50% square-wave requirements are separate specifications.

## Method and Exam English · 方法与答题

- Define each stage's legal range, reset value, and wrap event.
- Connect a higher enable to the accepted lower rollover, not just a static display value.
- 在“59→00”与“禁用时末态保持”两种边界上验证。

**Answer pattern:** “All stages use the same clock. The next stage is enabled only when the lower stage is enabled and currently at its terminal count. The combined modulus is the product of the individual legal cycle lengths.”

## Connections · 相关笔记

[[Counters]], [[Register Enable and Reset]], [[Decoder]], [[Traffic Light Controller]], [[Propagation Delay and Logic Hazards]], [[Digital Logic Troubleshooting]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
