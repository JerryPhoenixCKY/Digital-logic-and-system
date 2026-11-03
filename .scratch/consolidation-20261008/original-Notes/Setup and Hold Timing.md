---
tags:
  - ECE2050
  - timing
date: 2026-09-30
aliases:
  - 建立与保持时间
  - Setup and Hold Timing
  - Register timing constraints
---

# Setup and Hold Timing · 建立与保持时间

> [!SUMMARY] Quick recall · 英文速览
> Setup constrains the latest arrival before the next capture edge. Hold constrains the earliest arrival after the current capture edge. Lowering frequency can repair a setup violation but does not normally repair a hold violation.

## Definitions and Assumptions · 定义与假设

- $t_{setup}$：捕获边沿前数据需稳定的时间。
- $t_{hold}$：捕获边沿后数据需继续稳定的时间。
- $t_{pcq}$：launch FF 的最大 clock-to-Q delay。
- $t_{ccq}$：launch FF 的最小 clock-to-Q delay。
- $t_{pd},t_{cd}$：中间组合逻辑的最大/最小延迟。
- $T$：clock period，所有时间使用相同单位。

The baseline model uses the same clock, zero skew, and no extra uncertainty. “Maximum frequency” is meaningful only after both setup and hold have passed.

![[setup-hold-window.svg]]
*Figure 1 · 共同时间轴上的采样窗口：D在建立/保持区间稳定，Q在clock-to-Q延迟后改变；示意长度不代表器件保证值。*

## Setup Derivation · 建立约束推导

在 t=0 launch，最晚新数据到达时间 $t_{pcq}+t_{pd}$；下次 capture 在 T，需提前 $t_{setup}$ 稳定：

$$t_{pcq}+t_{pd}\le T-t_{setup},\quad T\ge t_{pcq}+t_{pd}+t_{setup}.$$

$$f_{max}=\frac1{t_{pcq}+t_{pd}+t_{setup}}.$$

此式是在该模型并满足 hold 后的上界。多条路径取最严格者。

## Hold Derivation · 保持约束推导

同一个 t=0 capture 之后，还需保留旧值 $t_{hold}$；新数据最早到达 $t_{ccq}+t_{cd}$：

$$t_{ccq}+t_{cd}\ge t_{hold}.$$

Hold is a same-edge check. T does not appear because the risk concerns the current capture edge, not the next one. Add delay on the short path, change the cell/path, or adjust the clock relationship as appropriate.

![[register-short-long-paths.svg]]
*Figure 2 · 同一组合网络的最长/最短路径概念：分别用于setup与hold；上下框是路径分析示意，不是将两个门输出短接的接线图。*

## Worked Example · 同时检查两条约束

给 $t_{ccq}=30$ ps、$t_{pcq}=50$ ps、setup=60 ps、hold=70 ps；长路径为三个门，每门 $t_{pd}=35$ ps；短路径一个门，$t_{cd}=25$ ps。

$$T_{min}=50+3(35)+60=215\text{ ps},\quad f=4.651\text{ GHz}.$$

但是 hold：$30+25=55<70$ ps，失败。不能宣布“以 4 GHz 就能运行”；即使降到 1 MHz，当前边沿附近仍有相同问题。

短路径增加一个 minimum delay=25 ps 的 buffer 后，hold 到达时间为 80 ps，slack=10 ps。仍要重新检查最长路径，确认该 buffer 是否也影响 setup；不可以默认修复没有代价。

## Skew Extension · 偏斜扩展

定义 capture clock 比 launch **晚** $s$：同一对应边沿在 capture 端时刻 s。忽略 jitter 时：

$$T\ge t_{pcq}+t_{pd}+t_{setup}-s,$$
$$t_{ccq}+t_{cd}\ge t_{hold}+s.$$

Positive capture skew helps setup but hurts hold. Never memorize a skew sign without defining which clock arrives later. Extra uncertainty reduces available margin; its application depends on the timing model supplied.

## Method and Review · 方法与复习

1. Separate maximum and minimum path calculations.
2. Define the launch and capture edges.
3. Compute setup slack and hold slack independently.
4. State the repair and rerun both constraints.

**Exam answer:** “The setup bound permits a 215 ps period, but the 15 ps hold violation prevents reliable operation at any period under the stated zero-skew model. A short-path delay element can repair hold if the revised setup bound still passes.”

## Connections · 相关笔记

[[Propagation Delay and Logic Hazards]], [[D Latch and D Flip-Flop]], [[Sequential Logic]], [[Metastability and Clock Domain Crossing]], [[Field-Programmable Gate Array]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
