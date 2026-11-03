---
tags:
  - ECE2050
  - registers
date: 2026-09-30
updated: 2026-10-09
chapter: Ch8
aliases:
  - 单稳态与脉冲应用
  - One-Shots and Pulse Applications
  - 单稳态与脉冲应用 · Ch8
  - Monostable and astable circuits
---

# One-Shots and Pulse Applications · 单稳态与脉冲应用

> [!SUMMARY] Quick recall · 英文速览
> A one-shot produces a timed excursion after a trigger. A registered edge detector instead produces an event pulse measured in clock cycles.

## 1 · 稳态数量决定类别

单稳态 (monostable / one-shot) 有一个稳定状态，触发后暂时离开再返回；无稳态 (astable) 持续振荡；双稳态 (bistable) 可保存一位。不要把名称与具体触发极性混在一起。

### Core Definition · 核心定义

单稳态 (monostable) 接受一次 trigger 后进入暂态，再回到稳定状态；脉冲宽度由时间机制决定。无稳态 (astable) 自动周期变化；双稳态 (bistable) 如 SR latch 可存储一位。

| Circuit | Stable states | Trigger behavior | Use |
|---|---|---|---|
| Bistable | 2 | Changes/holds state | Memory |
| Monostable | 1 | Produces one pulse | Pulse shaping/delay |
| Astable | 0 | Repeats autonomously | Oscillation |

Retriggerable one-shots can restart or extend their interval on a new trigger. Nonretriggerable ones ignore triggers during the active interval under their specified operating conditions. Read the device's rule before drawing pulses.

### Exam English and Connections · 答题与关联

**Question:** Is a one-shot an astable multivibrator?

**Answer:** No. A one-shot is monostable and produces one timed output pulse per accepted trigger. An astable circuit oscillates without returning permanently to a stable state.

[[Digital Foundations and Waveforms#2 · Digital Waveforms · 再把时间加入模型|Digital Waveforms]], [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]], [[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界|Metastability and Clock Domain Crossing]], [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]], [[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转|Cascaded Counters and Digital Clocks]].

## 2 · RC 阈值决定脉宽

一阶充电模型 $V_C(t)=V_f+(V_0-V_f)e^{-t/(RC)}$，到阈值 $V_T$ 的时间：
$$t=-RC\ln[(V_T-V_f)/(V_0-V_f)].$$
R 单位 Ω、C 单位 F，因此 RC 单位 s；阈值必须落在该转换实际经过的范围。系数由电路阈值决定，不应把某芯片的经验系数推广到所有单稳态。

> [!example]- One-Shots and Pulse Applications · 推导与例题
> **Derivation · RC timing boundary**
>
> RC 充电的理想式：
>
> $$V_C(t)=V_\infty+(V_0-V_\infty)e^{-t/(RC)}.$$
>
> 若在 $V_{th}$ 终止脉冲：
>
> $$t_p=-RC\ln\frac{V_\infty-V_{th}}{V_\infty-V_0}.$$
>
> R 为 Ω，C 为 F，RC 为 s。比例系数取决于阈值、初值与拓扑；不能对所有 one-shot 都写 $t_p=RC$ 或照用某个 IC 的系数。
>
> **Worked Examples · 例题**
>
> **Ideal threshold.** $V_0=0,V_\infty=5$ V、$V_{th}=2.5$ V、R=10 kΩ、C=100 nF，RC=1 ms，$t_p=0.693$ ms。阈值改为 $2V_\infty/3$ 时系数为 $\ln3\approx1.099$，可见阈值决定时长。
>
> **Digital pulse.** 要在 1 MHz clock 域生成 10 μs pulse，可在 trigger 被接受后计数 10 个完整周期。输出进入 active 时刻与停止边沿要定义清楚；若计数 0–9，则 ten states 对应十拍。
>
> **Debounce.** 假定开关在 2 ms 内反复跳变，nonretriggerable 脉冲宽度取 3 ms 可屏蔽这次假定范围内的额外 trigger，但不能凭该数值保证任意开关都不抖动。也可要求输入持续稳定指定拍数再接受。

## 3 · 数字事件脉冲与按键捕获

同步信号 x 与其一周期延迟 $x_d$ 的上升沿检测为 $p=x\bar x_d$，通常产生一周期脉冲；异步输入应先处理跨域与去抖。延迟捕获按键需保证采样时数据已经稳定。

> [!IMPORTANT] 时间单位来自实现
> RC 脉宽由模拟参数决定，寄存器事件脉宽由时钟周期决定。可重触发性、初态、输入最小宽度和边沿语义需另行给出。

> [!example]- One-Shots and Pulse Applications · 推导与例题
> **Edge Detection · 边沿检测**
>
> 同步后的 level X，令延迟状态 $X_d^+=X$，组合 pulse $P=X\bar X_d$，在 X 第一次变 HIGH 的周期出现脉冲。异步输入须先同步，否则组合 edge detector 可能传播不受控短脉冲。
>
> A delayed gate path can create a narrow transition spike in a teaching circuit. Its width depends on physical delay and operating conditions, so it should not be treated as a robust general clock source. Use a specified clock and synchronous enable when building ordinary FPGA logic.
>
> **Delayed key capture · 延迟捕获按键**
>
> In the course's keyboard example, one-shots delay the accepted capture event and temporarily inhibit scanning. This keeps the row identity aligned with the column code while the key-code register loads. The chosen pulse width must suit the stated settling model.
>
> 完整路径见 [[Keyboard Scanning and Encoding]]。相同threshold模型下增加R或C会延长pulse；
> 不能据此推定任意机械开关都去抖成功。shared-clock实现可用计数器和enable替代异步脉冲时钟。

## Sources · 课件依据

主线课件：[Ch8 lecture](../LGU_HUB_ECE2050/ECE2050-Chap8.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050.1]] · [[Glossary]]
