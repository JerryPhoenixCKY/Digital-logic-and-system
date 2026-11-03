---
tags:
  - ECE2050
  - timing
date: 2026-09-30
updated: 2026-10-08
chapter: Ch6
aliases:
  - 传播延迟与逻辑冒险
  - Propagation Delay and Logic Hazards
  - 传播延迟与逻辑冒险 · Ch6
  - Logic timing and glitches
---

# Propagation Delay and Logic Hazards · 传播延迟与逻辑冒险

> [!SUMMARY] Quick recall · 英文速览
> The longest path bounds settling; the shortest path bounds the earliest change. Different path delays can create glitches in an otherwise equivalent Boolean function.

## 1 · 最长路径与最短路径

最大传播延迟 $t_{pd}$ (propagation delay) 表示最迟稳定时间；最小污染延迟 $t_{cd}$ (contamination delay) 表示最早可能变化时间，单位 s 或 ns。串联路径相加，多条路径分别取最大／最小，不能混用。

> [!example]- Propagation Delay and Logic Hazards · 推导与例题
> **Worked Example 1 · 长短路径**
>
> 假设输入 A 经过 AND–AND–OR，输入 D 只经过 OR；AND 的 $(t_{pd},t_{cd})=(30,10)$ ps，OR 为 (20,8) ps。长路径=80 ps，短路径=8 ps。前提是对应路径可敏化；不应把所有并行门的延迟直接累加。
>
> The latest bound describes when the output is safe to sample after all relevant inputs have changed. The earliest bound matters when old data must remain stable, particularly for hold-time analysis. “The circuit delay” is incomplete unless it identifies which bound is needed.

## 2 · 静态冒险来自不同路径

$F=AB+\bar AC$ 在 B=C=1 时理论恒为 1；A 变化时两条路径的响应不同时可能产生短暂 0，为静态 1 冒险 (static-1 hazard)。共识项 (consensus term) BC 保持稳态等价，却可在该单输入转换条件下桥接间隙。

> [!example]- Propagation Delay and Logic Hazards · 推导与例题
> **Derivation · Static-1 hazard**
>
> 设 $F=AB+\bar AC$，B=C=1，A 由 1 变 0。稳态前后 F 都为 1，但 AB 路径可能先降到 0，NOT A 路径后升到 1，暂时两个乘积都为 0。
>
> $$F_{safe}=AB+\bar AC+BC.$$
>
> 新增 consensus term $BC$ 不改真值表，却在这次转换过程中一直为 1。验证冗余：$BC=ABC+\bar ABC$，分别已被 AB 与 $\bar AC$ 覆盖。
>
> | Hazard | Required steady value | Possible transient |
> |---|---|---|
> | Static-1 | 1 | Brief 0 |
> | Static-0 | 0 | Brief 1 |
> | Dynamic | Changes once | Multiple toggles |
>
> **Worked Example 2 · 冒险宽度**
>
> 初始 A=1、B=C=1。假设 AB 从 A 到输出项需要 2 ns，$\bar AC$ 需要 5 ns。A 下降后在 2–5 ns 内两项都为 0，因此可能出现约 3 ns 的低脉冲；末级门的惯性延迟与 rise/fall 特性可能缩短或过滤它。这是规定路径模型下的估计，不是通用脉宽公式。
>
> Adding BC covers this single-input transition. It does not guarantee immunity to arbitrary simultaneous changes of several inputs. A K-map hazard check asks whether adjacent ON cells are covered by a common implicant, under the single-input-change assumption.

## 3 · 何时加项，何时依靠采样

组合输出直接控制异步信号时，毛刺可能立即产生效果；同步接收端在满足采样稳定窗口时可避开某些瞬态，但不能因此忽视建立／保持约束。多输入同时变化和动态冒险需更完整的模型。

> [!IMPORTANT] 化简目标要写清
> 最小文字数、少门、短路径与无静态冒险可能互相冲突。添加冗余项不是布尔错误，而是为特定转换增加覆盖；验证应包含稳态和转换条件。

> [!example]- Propagation Delay and Logic Hazards · 推导与例题
> **Sampling and Applications · 采样与应用**
>
> 同步系统若在数据稳定后采样，可容忍某些组合毛刺；但用毛刺信号驱动 clock、异步 reset 或外部控制仍可出问题。[[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] 约束采样时间，不能把“有时钟”直接当作无毛刺保证。
>
> **Counter decoding.** 即使 [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] 的所有触发器使用同一 clock，clock-to-Q 不同仍可让组合 decode 短暂经过错误输出。可注册 decode，或按明确时序屏蔽转换窗口。

## Sources · 课件依据

主线课件：[Ch6 lecture](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
