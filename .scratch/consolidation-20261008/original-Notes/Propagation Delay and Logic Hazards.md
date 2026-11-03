---
tags:
  - ECE2050
  - timing
date: 2026-09-30
aliases:
  - 传播延迟与逻辑冒险
  - Propagation Delay and Logic Hazards
  - Logic timing and glitches
---

# Propagation Delay and Logic Hazards · 传播延迟与逻辑冒险

> [!SUMMARY] Quick recall · 英文速览
> Propagation delay bounds the latest output settling time; contamination delay bounds the earliest possible change. Unequal path delays can produce glitches even when the steady-state Boolean expression is correct.

## Core Definition · 核心定义

传播延迟 (propagation delay) $t_{pd}$ 是从输入改变到输出保证稳定的最大延迟；污染延迟 (contamination delay) $t_{cd}$ 是输出最早可能开始改变的最小延迟。门的 rise/fall、不同输入路径与负载可有不同值，具体数值由题目或器件条件定义。

对无环网络，候选路径延迟是各门/连线延迟之和；取能够影响所需输出的最长路径为 $t_{pd}$，最短路径为 $t_{cd}$。功能敏化 (sensitization) 决定一个路径是否真正能传递变化。

## Worked Example 1 · 长短路径

假设输入 A 经过 AND–AND–OR，输入 D 只经过 OR；AND 的 $(t_{pd},t_{cd})=(30,10)$ ps，OR 为 (20,8) ps。长路径=80 ps，短路径=8 ps。前提是对应路径可敏化；不应把所有并行门的延迟直接累加。

The latest bound describes when the output is safe to sample after all relevant inputs have changed. The earliest bound matters when old data must remain stable, particularly for hold-time analysis. “The circuit delay” is incomplete unless it identifies which bound is needed.

## Derivation · Static-1 hazard

设 $F=AB+\bar AC$，B=C=1，A 由 1 变 0。稳态前后 F 都为 1，但 AB 路径可能先降到 0，NOT A 路径后升到 1，暂时两个乘积都为 0。

$$F_{safe}=AB+\bar AC+BC.$$

新增 consensus term $BC$ 不改真值表，却在这次转换过程中一直为 1。验证冗余：$BC=ABC+\bar ABC$，分别已被 AB 与 $\bar AC$ 覆盖。

| Hazard | Required steady value | Possible transient |
|---|---|---|
| Static-1 | 1 | Brief 0 |
| Static-0 | 0 | Brief 1 |
| Dynamic | Changes once | Multiple toggles |

## Worked Example 2 · 冒险宽度

初始 A=1、B=C=1。假设 AB 从 A 到输出项需要 2 ns，$\bar AC$ 需要 5 ns。A 下降后在 2–5 ns 内两项都为 0，因此可能出现约 3 ns 的低脉冲；末级门的惯性延迟与 rise/fall 特性可能缩短或过滤它。这是规定路径模型下的估计，不是通用脉宽公式。

Adding BC covers this single-input transition. It does not guarantee immunity to arbitrary simultaneous changes of several inputs. A K-map hazard check asks whether adjacent ON cells are covered by a common implicant, under the single-input-change assumption.

## Sampling and Applications · 采样与应用

同步系统若在数据稳定后采样，可容忍某些组合毛刺；但用毛刺信号驱动 clock、异步 reset 或外部控制仍可出问题。[[Setup and Hold Timing]] 约束采样时间，不能把“有时钟”直接当作无毛刺保证。

**Counter decoding.** 即使 [[Counters]] 的所有触发器使用同一 clock，clock-to-Q 不同仍可让组合 decode 短暂经过错误输出。可注册 decode，或按明确时序屏蔽转换窗口。

## Method and Exam English · 方法与英文

1. List paths to the requested output; include inversions.
2. Sum maximum and minimum delays separately.
3. State side-input values that make a path observable.
4. Compare steady-state truth with the actual transition sequence.
5. Evaluate whether the receiving element could capture the glitch.

**Exam answer:** “The Boolean output remains HIGH before and after the transition. Unequal delays temporarily remove both product terms, creating a static-1 hazard. The consensus term bridges the transition without changing the steady-state function.”

## Connections · 相关笔记

[[Combinational Circuit]], [[Karnaugh Map]], [[Universal Gates and Bubble Pushing]], [[Digital Waveforms]], [[Setup and Hold Timing]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
