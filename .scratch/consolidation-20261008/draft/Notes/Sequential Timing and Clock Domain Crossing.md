---
tags:
  - ECE2050
  - timing
date: 2026-09-30
updated: 2026-10-08
chapter: Ch9
aliases:
  - 时序约束与时钟域跨越
  - Sequential Timing and Clock Domain Crossing
  - 时序约束与时钟域跨越 · Ch9
  - Setup and Hold Timing
  - 建立与保持时间
  - Register timing constraints
  - Metastability and Clock Domain Crossing
  - 亚稳态与时钟域跨越
  - CDC and synchronizers
---

# Sequential Timing and Clock Domain Crossing · 时序约束与时钟域跨越

> [!SUMMARY] Quick recall · 英文速览
> Setup limits the latest arrival; hold limits the earliest arrival. Clock-domain crossing requires a transfer protocol beyond ordinary synchronous path checks.

## 1 · Setup and Hold Timing · 建立统一时间基准

令发射时钟到捕获时钟偏斜 $s=t_{capture}-t_{launch}$，正值表示捕获晚到；$t_{pcq},t_{ccq}$ 为最大／最小 clock-to-Q，组合路径为 $t_{pd},t_{cd}$，各时间同单位。忽略抖动等额外预算时：

$$T\ge t_{pcq}+t_{pd}+t_{setup}-s,$$
$$t_{ccq}+t_{cd}\ge t_{hold}+s.$$

建立约束检查下一次捕获的最迟到达；保持约束检查同次边沿之后最早变化。正偏斜改善 setup，却恶化 hold。

> [!example]- Setup and Hold Timing · 推导与例题
> **Definitions and Assumptions · 定义与假设**
>
> - $t_{setup}$：捕获边沿前数据需稳定的时间。
> - $t_{hold}$：捕获边沿后数据需继续稳定的时间。
> - $t_{pcq}$：launch FF 的最大 clock-to-Q delay。
> - $t_{ccq}$：launch FF 的最小 clock-to-Q delay。
> - $t_{pd},t_{cd}$：中间组合逻辑的最大/最小延迟。
> - $T$：clock period，所有时间使用相同单位。
>
> The baseline model uses the same clock, zero skew, and no extra uncertainty. “Maximum frequency” is meaningful only after both setup and hold have passed.
>
> ![[setup-hold-window.svg]]
> *Figure 1 · 共同时间轴上的采样窗口：D在建立/保持区间稳定，Q在clock-to-Q延迟后改变；示意长度不代表器件保证值。*
>
> **Setup Derivation · 建立约束推导**
>
> 在 t=0 launch，最晚新数据到达时间 $t_{pcq}+t_{pd}$；下次 capture 在 T，需提前 $t_{setup}$ 稳定：
>
> $$t_{pcq}+t_{pd}\le T-t_{setup},\quad T\ge t_{pcq}+t_{pd}+t_{setup}.$$
>
> $$f_{max}=\frac1{t_{pcq}+t_{pd}+t_{setup}}.$$
>
> 此式是在该模型并满足 hold 后的上界。多条路径取最严格者。
>
> **Hold Derivation · 保持约束推导**
>
> 同一个 t=0 capture 之后，还需保留旧值 $t_{hold}$；新数据最早到达 $t_{ccq}+t_{cd}$：
>
> $$t_{ccq}+t_{cd}\ge t_{hold}.$$
>
> Hold is a same-edge check. T does not appear because the risk concerns the current capture edge, not the next one. Add delay on the short path, change the cell/path, or adjust the clock relationship as appropriate.
>
> ![[register-short-long-paths.svg]]
> *Figure 2 · 同一组合网络的最长/最短路径概念：分别用于setup与hold；上下框是路径分析示意，不是将两个门输出短接的接线图。*

## 2 · 裕量与修复方向

setup slack 为可用时间减需求，负值表示违反。减慢时钟通常改善 setup，但不会自动修复同边沿 hold；hold 可通过增加最短数据路径延迟等方式修复，随后复查 setup。

> [!example]- Setup and Hold Timing · 推导与例题
> **Worked Example · 同时检查两条约束**
>
> 给 $t_{ccq}=30$ ps、$t_{pcq}=50$ ps、setup=60 ps、hold=70 ps；长路径为三个门，每门 $t_{pd}=35$ ps；短路径一个门，$t_{cd}=25$ ps。
>
> $$T_{min}=50+3(35)+60=215\text{ ps},\quad f=4.651\text{ GHz}.$$
>
> 但是 hold：$30+25=55<70$ ps，失败。不能宣布“以 4 GHz 就能运行”；即使降到 1 MHz，当前边沿附近仍有相同问题。
>
> 短路径增加一个 minimum delay=25 ps 的 buffer 后，hold 到达时间为 80 ps，slack=10 ps。仍要重新检查最长路径，确认该 buffer 是否也影响 setup；不可以默认修复没有代价。
>
> **Skew Extension · 偏斜扩展**
>
> 定义 capture clock 比 launch **晚** $s$：同一对应边沿在 capture 端时刻 s。忽略 jitter 时：
>
> $$T\ge t_{pcq}+t_{pd}+t_{setup}-s,$$
> $$t_{ccq}+t_{cd}\ge t_{hold}+s.$$
>
> Positive capture skew helps setup but hurts hold. Never memorize a skew sign without defining which clock arrives later. Extra uncertainty reduces available margin; its application depends on the timing model supplied.

## 3 · Metastability and Clock Domain Crossing · 异步输入的边界

亚稳态 (metastability) 可能因采样窗口被违反而产生。两级同步器让第一级有更多解析时间，降低传播概率，不保证绝对消除。第一级不能随意扇出给其他逻辑；同步器中间通常不插组合逻辑。

> [!example]- Metastability and Clock Domain Crossing · 推导与例题
> **Mechanism · 两级同步器**
>
> 第一级采异步输入；第二级在下一个目标 clock 边沿采第一级，让第一级获得接近一个周期的解析时间。下游只能使用第二级输出。
>
> ```mermaid
> flowchart LR
>   Async[Asynchronous level] --> FF1[First destination-clock FF]
>   FF1 --> FF2[Second destination-clock FF]
>   FF2 --> Logic[Destination logic]
> ```
>
> This block diagram shows a single-bit level synchronizer. Place the stages close and avoid combinational logic between them when applying this pattern. Exact reliability depends on clock/data rates, device parameters, and available resolution time; no universal MTBF number follows from “two stages”.

## 4 · 按信息类型选跨域方法

单比特慢电平可用同步器；窄脉冲可能被漏采，需展宽、toggle 或握手；多位数据逐位同步可能得到不一致的组合，需稳定数据＋握手、适当 Gray 指针或异步 FIFO。

> [!IMPORTANT] 波形稳定不等于传输完整
> 亚稳态风险、事件是否被看见、多个位是否来自同一次更新，是三个不同问题。先规定协议和速率，再选同步结构。

> [!example]- Metastability and Clock Domain Crossing · 推导与例题
> **Validity Boundaries · 适用边界**
>
> - 单位 level：若保持足够久，可让目标域采到稳定值。
> - Narrow pulse：可能整个脉冲落在采样边沿之间，完全漏掉。
> - Multi-bit word：逐位同步可能采出混合新旧值，不能保证 atomicity。
> - Mechanical button：同步减少亚稳传播，debounce 处理多次接触跳变，是不同问题。
>
> For event transfer, use a specified pulse-stretching, toggle, or handshake scheme. For multi-bit data, use a stable-data handshake or an asynchronous FIFO as appropriate. These are extensions beyond the basic one-bit classroom circuit.
>
> **Worked Examples · 例题**
>
> **Pulse loss.** 目标周期 T=10 ns，输入脉冲在 2–5 ns 为 HIGH，采样边沿在 0、10、20 ns。即使脉冲很干净，所有采样看到 LOW，事件漏掉。两级同步器不能恢复一个从未采到的 pulse。
>
> **Mixed binary count.** 异步读取 0111→1000 的四位，路径不同可混成 0000 或 1111。[[Data Coding and Character Representation#3 · Gray Code · 相邻变化约束|Gray Code]] 每次合法相邻变化只改一位，减少混合码问题，但仍要同步和保证采样/传输约束，不能直接当作万能 CDC 方案。
>
> **Button.** 50 MHz clock 下，机械抖动 2 ms 相当于 100,000 周期。两级 FF 只提供几十 ns 的同步过程，不会自动消除 2 ms 的多次翻转。计数稳定时间的 debounce logic 才处理这个规格。

## Sources · 课件依据

主线课件：[Ch9 lecture](../LGU_HUB_ECE2050/ECE2050-Chap9.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
