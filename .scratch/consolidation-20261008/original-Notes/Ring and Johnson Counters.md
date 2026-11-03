---
tags:
  - ECE2050
  - registers
date: 2026-09-30
aliases:
  - 环形与约翰逊计数器
  - Ring and Johnson Counters
  - Shift register counters
---

# Ring and Johnson Counters · 环形与约翰逊计数器

> [!SUMMARY] Quick recall · 英文速览
> A ring counter feeds the last bit back unchanged; a Johnson counter feeds it back inverted. An n-stage one-hot ring has n states; an initialized Johnson cycle has 2n states. Initialization is part of the design.

## Core Definition and Model · 定义与模型

按 $Q_3Q_2Q_1Q_0$ 排列、right shift：ring 用 $Q^+=\{Q_0,Q_3,Q_2,Q_1\}$；Johnson 用 $Q^+=\{\bar Q_0,Q_3,Q_2,Q_1\}$。两者都用 FF 保存状态，与 [[Counters]] 的 binary increment 结构不同。

## Ring Derivation · 环形序列

one-hot seed 1000 旋转：1000→0100→0010→0001→1000，n=4 得 modulus 4。一周期内每个输出 HIGH 一拍，因此输出重复频率 $f_{clk}/4$、占空比 25%。

All-zero ring state stays all zero. A ring with two initial ones does not become one-hot by itself. Modulus n refers to the intended seeded cycle, not every possible state of the hardware.

one-cold seed 1110 也可扫描低有效按键线路：1110→0111→1011→1101→1110。这是有效极性改变，仍只有一个扫描位置 active。

## Johnson Derivation · 扭环序列

从 0000 开始：

| Step | State |
|---|---|
| 0 | 0000 |
| 1 | 1000 |
| 2 | 1100 |
| 3 | 1110 |
| 4 | 1111 |
| 5 | 0111 |
| 6 | 0011 |
| 7 | 0001 |
| 8 | 0000 |

先连续填入 n 个 1，再连续填入 n 个 0，共 2n 个状态。它不是 n-bit binary counter 的 $2^n$ 个状态；n=4 时是 8 而不是 16。

## Worked Examples · 例题

**Frequency.** 5-stage Johnson，input clock=1 MHz，完整序列重复=100 kHz；各 Q 位在合法周期中 HIGH 5 拍、LOW 5 拍，50% duty。one-hot 5-stage ring 的各位 duty=20%。

**Illegal cycle.** 四位 Johnson 从 0101 出发，按上述 recurrence 得到 0101→0010→1001→0100→1010→1101→0110→1011→0101，共 8 态，且与预期的 0000 cycle 分离。不要因为“Johnson modulus 8”就认为所有状态都落入 intended 0000 cycle。reset 可建立预期起点。

**Keyboard scan.** n=8、scan edge rate=5 kHz，完整扫描周期 $8/5000=1.6$ ms。同一个 row 每 1.6 ms 被访问一次。整个扫描频率是 625 Hz，不是每行都 5 kHz。

## Method and Review · 方法与复习

Write the exact feedback bit and inversion, declare the initial state, then enumerate until the first repeat. The modulus is the length of that cycle. A state decoding expression is valid only for the state domain used to derive it.

**Question:** Why must a one-hot ring be seeded with one 1?

**Answer:** Feedback preserves the number of ones. Starting at all zeros cannot create an active stage, so the intended rotating-one sequence never starts.

## One-cold scan application · 独冷扫描应用

An eight-stage ring initialized to `11111110` moves one zero around an active-low row interface. Its selected-row identity is valid only while the one-cold invariant holds. The same feedback wiring initialized to all ones cannot create a zero by itself.

扫描逻辑与采样控制见 [[Keyboard Scanning and Encoding]]。行选择、编码与捕获之间必须有稳定窗口，不能仅凭环形序列正确就宣布键盘接口完整。

## Connections · 相关笔记

[[Shift Registers]], [[Register Enable and Reset]], [[Encoder and Priority Encoder]], [[Counters]], [[State Encoding and Unused States]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
