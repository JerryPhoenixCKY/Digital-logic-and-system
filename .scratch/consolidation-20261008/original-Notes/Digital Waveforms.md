---
tags:
  - ECE2050
  - foundations
date: 2026-09-30
aliases:
  - 数字波形
  - Digital Waveforms
  - Pulse waveform
---

# Digital Waveforms · 数字波形

> [!SUMMARY] Quick recall · 英文速览
> A waveform shows logic values over time. Frequency is the reciprocal of period; duty cycle compares HIGH pulse width with the full period. Edge timing and pulse width are different quantities.

## Core Definition · 核心定义

数字波形 (digital waveform) 用时间轴展示信号变化。周期 $T$ 是相邻同类边沿之间的时间；频率 $f$ 是每秒重复次数；高电平脉宽 $t_H$ 是一次 HIGH 的持续时间。占空比 (duty cycle) 是 HIGH 占一周期的比例。

$$f=\frac1T,\qquad D=\frac{t_H}{T}\times100\%.$$

$T,t_H$ 单位为 s，$f$ 单位为 Hz。$t_H$ 不是整个周期，除非占空比为 100%；恒定直流信号没有通常意义的周期性边沿。

| Term | Typical measurement convention | 中文解释 |
|---|---|---|
| Rise time $t_r$ | 10% to 90% of amplitude | 上升沿过渡时间 |
| Fall time $t_f$ | 90% to 10% | 下降沿过渡时间 |
| Pulse width | Often between 50% crossing points | 同一脉冲的有效宽度 |
| Period | Corresponding edges of successive cycles | 完整重复时间 |
| Amplitude | Voltage or current excursion | 波形幅值 |

These percentages are measurement conventions, not universal logic thresholds. A receiving device may interpret an edge at a different voltage. State the convention when a question provides a nonideal waveform.

## Derivation and Reading Method · 推导与读图

把所有输入变化时刻合并成分界点，每个区间内输入不变，组合输出可由真值表计算。遇到触发器则只在有效边沿采样；异步复位可以在边沿之间改变状态。

1. Mark the time scale and identify the active clock edge.
2. Divide time at every input transition.
3. Evaluate combinational expressions within each interval.
4. For state elements, record the values just before each active edge.
5. Apply propagation delay only if the problem asks for it or supplies it.

## Worked Examples · 例题

**Example 1.** $T=20\text{ ms}$，$t_H=5\text{ ms}$。

$$f=1/(20\times10^{-3})=50\text{ Hz},\qquad D=5/20=25\%.$$

Check: 50 periods occupy one second. The LOW interval is 15 ms, which is three times the HIGH interval. Frequency does not become 200 Hz merely because the HIGH pulse lasts 5 ms.

**Example 2.** 三个时间区间中 $(A,B)$ 依次为 00、01、11，[[Exclusive-NOR Gate]] 输出依次为 1、0、1。若实际门有 4 ns 传播延迟，输出边沿在对应输入变化后出现；不要把 4 ns 当成脉冲宽度。

**Example 3.** 一个 [[D Latch and D Flip-Flop]] 的 D 在 clock HIGH 中途由 0 变 1：高电平透明 D latch 跟随，正沿 D flip-flop 保持到下一个正沿。相同输入图必须先确定存储元件类型。

## Pitfalls and Exam English · 易错点与英文答题

“Sketch the output in proper relation to the inputs” means use a common time axis and align events correctly. “Assume initially LOW” specifies a state before the first event; it is not a statement that a flip-flop automatically powers up at zero.

- $1\text{ ms}=10^{-3}\text{ s}$；$1\text{ ns}=10^{-9}\text{ s}$；单位先统一。
- HIGH duration determines duty cycle; it does not by itself determine frequency.
- 延迟影响边沿位置，setup/hold 决定是否能够可靠采样。

**Self-check:** A 10 MHz waveform has a 30 ns HIGH pulse. Find period and duty cycle.

**Answer:** $T=100$ ns and $D=30\%$. There are 10 million full periods per second.

## Connections · 相关笔记

[[Digital Abstraction and System Design]] explains the interpretation of the waveform. [[Logic Gates]] gives interval-by-interval functions. [[Propagation Delay and Logic Hazards]] and [[Setup and Hold Timing]] add real timing behavior.

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
