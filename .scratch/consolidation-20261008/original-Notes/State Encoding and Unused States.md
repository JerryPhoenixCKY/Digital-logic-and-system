---
tags:
  - ECE2050
  - finite-state-machines
date: 2026-09-30
aliases:
  - 状态编码与未用状态
  - State Encoding and Unused States
  - Binary and one-hot encoding
---

# State Encoding and Unused States · 状态编码与未用状态

> [!SUMMARY] Quick recall · 英文速览
> Encoding changes the hardware representation, not the intended behavior. Binary uses at least ceiling(log2 N) bits; one-hot uses N bits. Unused codes need an explicit policy.

## Core Definition and Derivation · 定义与推导

N 个状态由 b 位寄存器编码，需要 $2^b\ge N$，所以 $b=\lceil\log_2N\rceil$。one-hot 每状态一位，合法域恰好一个 1，需要 N 位。

| N | Minimum binary FFs | One-hot FFs | Unused binary codes |
|---|---|---|---|
| 3 | 2 | 3 | 1 |
| 4 | 2 | 4 | 0 |
| 5 | 3 | 5 | 3 |
| 10 | 4 | 10 | 6 |

One-hot often simplifies the logic because state membership is available directly as one bit. More flip-flops do not automatically mean slower logic. Area and delay depend on mapping, routing, and the target hardware.

## Worked Example · 三态循环

行为 A→B→C→A。binary 编码 A=00,B=01,C=10；给 unused 11→00 恢复：

| Q1Q0 | Next |
|---|---|
| 00 | 01 |
| 01 | 10 |
| 10 | 00 |
| 11 | 00 |

$$D_1=\bar Q_1Q_0,\qquad D_0=\bar Q_1\bar Q_0.$$

one-hot 向量 $(q_C,q_B,q_A)$：001→010→100→001，$q_A^+=q_C,q_B^+=q_A,q_C^+=q_B$。合法域下只有连线即可；但 000 会自锁，multi-hot 会循环，必须另加 reset/illegal-state recovery 才能满足完整规范。

## Don't-Care Policy · 无关项策略

把 11 标 X 可能进一步化简 binary next-state equations，但所得 implementation 对 11 有具体行为。必须把最终 equations 在 11 代入，确认它是 recover、lock 或另一个 cycle。

“Unused in normal operation” is not equivalent to “physically impossible.” Power-up, disturbances, reset inconsistencies, or design mistakes can produce an unused code. The course may allow don't-cares for minimization; engineering recovery requires additional behavior and verification.

对于 one-hot 有 $2^N-N$ 个非法码。定义 `others` 的 RTL 分支有助于描述意图，但综合可能按其 FSM优化/编码策略改变实现；要核对实际实现与约束，不能把一行 default 当作物理安全证明。

## Method and Review · 方法与复习

1. List semantic states before assigning bits.
2. Record the encoding next to the diagram and tables.
3. Re-derive each next-state bit under that encoding.
4. Check reset and every unused code.
5. Compare logic and FF costs using the actual implementation.

**Question:** Why can the same FSM have different equations in two answers?

**Answer:** Different state encodings assign different bit patterns to the same semantic states. The Boolean equations can differ while the externally specified transitions and outputs remain equivalent.

## Connections · 相关笔记

[[Bits and Bytes]], [[Karnaugh Map with Don't Cares]], [[Finite State Machine]], [[Ring and Johnson Counters]], [[Synchronous Counter Design]], [[Field-Programmable Gate Array]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
