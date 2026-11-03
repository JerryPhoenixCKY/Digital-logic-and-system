---
tags:
  - ECE2050
  - sequential-logic
date: 2026-09-30
aliases:
  - JK与T触发器
  - JK and T Flip-Flops
  - JK excitation table
---

# JK and T Flip-Flops · JK与T触发器

> [!SUMMARY] Quick recall · 英文速览
> JK describes hold, reset, set, and toggle. T describes hold or toggle. Characteristic tables predict next state; excitation tables find inputs that cause a required transition.

## Core Definition and Derivation · 定义与推导

在有效边沿，JK 特征式：

$$Q^+=J\bar Q+\bar KQ.$$

若 Q=0，$Q^+=J$；若 Q=1，$Q^+=\bar K$。直接由当前状态分组得到特征式，比背诵全表更容易验证。

| J | K | Action |
|---|---|---|
| 0 | 0 | Hold |
| 0 | 1 | Reset |
| 1 | 0 | Set |
| 1 | 1 | Toggle |

TFF 用 $J=K=T$，得到 $Q^+=Q\oplus T$。T=0 保持，T=1 翻转；也可用 DFF 与 XOR 实现 $D=Q\oplus T$。

## Excitation Table · 激励表

| Q | $Q^+$ | J | K | T | D |
|---|---|---|---|---|---|
| 0 | 0 | 0 | X | 0 | 0 |
| 0 | 1 | 1 | X | 1 | 1 |
| 1 | 0 | X | 1 | 1 | 0 |
| 1 | 1 | X | 0 | 0 | 1 |

X means either binary value achieves the required transition. These excitation don't-cares are justified by the current Q value. They differ from declaring an unused state globally irrelevant.

## Conversion · 元件转换

- JK using DFF: connect $D=J\bar Q+\bar KQ$.
- DFF using JK: $J=D,K=\bar D$.
- TFF using JK: $J=K=T$.
- 无使能 toggle 用 DFF：$D=\bar Q$。

使用 2:1 MUX 也能实现 JK 的 D 式：select Q，D0=J，D1=NOT K。Q=0 选 J；Q=1 选 NOT K。这里 MUX 的 select 是**当前输出 Q**，不是 clock。

## Worked Examples · 例题

**Trace.** Q 初值 0，连续有效边沿的 JK 输入为 10、11、00、01，Q 变为 1、0、0、0。最后 reset 没有产生边沿以外的动作，因为这是同步 JK 输入。

**Design one bit.** 状态要求 0→1、1→0，激励表给 0 时 J=1，1 时 K=1；选择 J=K=1 可满足两种转换。输出以输入 clock 一半频率翻转。

**Race-around boundary.** Level-sensitive JK feedback with J=K=1 can toggle repeatedly during a long enabled pulse. An edge-triggered or suitable master-slave implementation limits updating to the intended event. Do not apply the edge table blindly to a transparent feedback latch.

## Method and Review · 方法与复习

分析题：先求 J,K，再代 characteristic equation 求全部 next states。设计题：先给 desired transitions，再查 excitation table 求 J,K，最后化简。

**Exam question:** Why is K a don't-care for the transition 0→1?

**Answer:** With Q=0, the term $\bar KQ$ is zero regardless of K. The next state therefore depends only on J, and J must be 1.

## Connections · 相关笔记

[[D Latch and D Flip-Flop]], [[Multiplexer and Demultiplexer]], [[Synchronous Counter Design]], [[Karnaugh Map with Don't Cares]], [[Sequential Logic]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
