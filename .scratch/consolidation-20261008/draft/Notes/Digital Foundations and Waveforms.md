---
tags:
  - ECE2050
  - foundations
date: 2026-09-30
updated: 2026-10-08
chapter: Ch1
aliases:
  - 数字基础与波形
  - Digital Foundations and Waveforms
  - 数字基础与波形 · Ch1
  - Digital Abstraction and System Design
  - 数字抽象与系统设计
  - Digital discipline
  - Digital Waveforms
  - 数字波形
  - Pulse waveform
---

# Digital Foundations and Waveforms · 数字基础与波形

> [!SUMMARY] Quick recall · 英文速览
> Digital systems interpret continuous voltages as discrete symbols. Correct function, valid voltage levels, and valid sampling time are three separate requirements.

## 1 · Digital Abstraction and System Design · 从电压到信息

数字抽象 (digital abstraction) 把一段允许的电压解释为逻辑 0/1；导线电压本身仍连续变化。先确定“信息是什么意思”，再选择表示它的位宽、电平极性和采样方式。正逻辑 (positive logic) 与低有效控制 (active-low control) 可以同时存在。

> [!IMPORTANT] 三层正确性
> 真值表保证功能；阈值与噪声容限保证电气接口；建立／保持约束保证采样。任何一层不满足，都不能由另外两层替代。

## 2 · Digital Waveforms · 再把时间加入模型

周期 $T$ 是相邻同类边沿之间的时间，高电平脉宽为 $t_H$，频率 $f$ 和占空比 $D$ 为：

$$f=1/T,\qquad D=(t_H/T)\times100\%.$$

T、$t_H$ 单位为 s，f 单位 Hz；上升／下降时间描述边沿过渡，传播延迟描述输入到输出的响应，两者都不等于脉宽。10%–90% 等测量约定不等于逻辑门的输入阈值。

**例。** $T=20\rm\,ms,t_H=5\rm\,ms$，故 $f=50\rm\,Hz,D=25\%$。10 MHz 时周期为 100 ns；30 ns 高电平对应 30% 占空比。

> [!example]- Digital Waveforms · 推导与例题
> **Pitfalls and Exam English · 易错点与英文答题**
>
> “Sketch the output in proper relation to the inputs” means use a common time axis and align events correctly. “Assume initially LOW” specifies a state before the first event; it is not a statement that a flip-flop automatically powers up at zero.
>
> - $1\text{ ms}=10^{-3}\text{ s}$；$1\text{ ns}=10^{-9}\text{ s}$；单位先统一。
> - HIGH duration determines duty cycle; it does not by itself determine frequency.
> - 延迟影响边沿位置，setup/hold 决定是否能够可靠采样。
>
> **Self-check:** A 10 MHz waveform has a 30 ns HIGH pulse. Find period and duty cycle.
>
> **Answer:** $T=100$ ns and $D=30\%$. There are 10 million full periods per second.

## 3 · 从模块到系统：先数据、后控制

层次化 (hierarchy) 隐藏细节；模块化 (modularity) 固定接口；规则性 (regularity) 复用结构。数据通路 (datapath) 处理计数和比较，控制器 (controller) 根据状态决定装载、停止、清零。

以装瓶到 12 粒为例，保存 0–12 需 $\lceil\log_2 13\rceil=4$ 位；比较器判断 count=12，状态机再关闭阀门。一个持续三个周期的高电平不能自动算成三次独立事件，输入接口必须规定“一次事件”的含义。

> [!example]- Digital Abstraction and System Design · 推导与例题
> **Derivation · 从抽象到系统**
>
> 1. 外界传感器输出电压；阈值把它转为 Boolean event。
> 2. [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] 保存事件个数；组合逻辑比较当前计数和目标。
> 3. [[Comparison Decoding and Selection#1 · Magnitude Comparator · 最高不同位决定大小|Magnitude Comparator]] 得到“已装满”；[[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]] 决定关阀、移动、清零。
> 4. 数量运算由 datapath 完成，动作时序由 controller 完成。二者分开，能够分别验证。
>
> ```mermaid
> flowchart LR
>   Sensor[Sensor event] --> Count[Counter / datapath]
>   Target[Target quantity] --> Compare[Comparator]
>   Count --> Compare
>   Compare --> Control[FSM / controller]
>   Control --> Actuator[Valve and conveyor]
>   Control --> Count
> ```
>
> This is a dependency diagram, not a wiring schematic. The controller feedback crosses clocked state elements; a combinational loop would require a different model.
>
> **Worked Examples · 实际例题**
>
> **Bottle filling.** 目标 12 粒，计数器初值 0，每个有效传感器事件加 1。需要至少 $n=\lceil\log_2(12+1)\rceil=4$ 位来保存 0 至 12。第 12 次事件后 count=12，比较器相等输出有效，控制器进入停止状态。3 位只能到 7，不够。
>
> An input pulse must be converted into exactly one count event. Sampling a HIGH level for three cycles must not count one tablet three times. Synchronization, edge detection, and the event specification belong in the input interface.
>
> **Digital audio.** ADC 把幅值量化成代码，数字部分存储和运算，DAC 再生成模拟输出。数字存储可以抗一定噪声，但量化会产生误差；数字系统不是“没有模拟部分”。采样理论不是本课程逻辑模型的全部内容。

## 4 · 波形分析：组合区间与时序边沿

把全部输入变化时刻作为分界；每个稳定区间按布尔函数求组合输出。遇到存储元件，只在规定的有效边沿或透明电平更新状态；异步复位另按优先级处理。先忽略延迟建立逻辑轨迹，再加入题目给出的延迟。

> [!example]- Digital Waveforms · 推导与例题
> **Derivation and Reading Method · 推导与读图**
>
> 把所有输入变化时刻合并成分界点，每个区间内输入不变，组合输出可由真值表计算。遇到触发器则只在有效边沿采样；异步复位可以在边沿之间改变状态。
>
> 1. Mark the time scale and identify the active clock edge.
> 2. Divide time at every input transition.
> 3. Evaluate combinational expressions within each interval.
> 4. For state elements, record the values just before each active edge.
> 5. Apply propagation delay only if the problem asks for it or supplies it.
>
> **Worked Examples · 例题**
>
> **Example 1.** $T=20\text{ ms}$，$t_H=5\text{ ms}$。
>
> $$f=1/(20\times10^{-3})=50\text{ Hz},\qquad D=5/20=25\%.$$
>
> Check: 50 periods occupy one second. The LOW interval is 15 ms, which is three times the HIGH interval. Frequency does not become 200 Hz merely because the HIGH pulse lasts 5 ms.
>
> **Example 2.** 三个时间区间中 $(A,B)$ 依次为 00、01、11，[[Logic Gates and Boolean Functions#4 · Exclusive-OR Gate and Exclusive-NOR Gate · 比较与奇偶性|Exclusive-NOR Gate]] 输出依次为 1、0、1。若实际门有 4 ns 传播延迟，输出边沿在对应输入变化后出现；不要把 4 ns 当成脉冲宽度。
>
> **Example 3.** 一个 [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]] 的 D 在 clock HIGH 中途由 0 变 1：高电平透明 D latch 跟随，正沿 D flip-flop 保持到下一个正沿。相同输入图必须先确定存储元件类型。

## 5 · 重点回忆与下一步

- 电平、逻辑值和“控制已有效”是三个不同概念。
- 频率取完整周期的倒数，脉宽用于占空比。
- 先学 [[Number Systems and Base Conversion]] 与 [[Logic Gates and Boolean Functions]]，再进入组合电路和时序电路。

## Sources · 课件依据

主线课件：[Ch1 lecture](../ECE2050-Chap1%281%29.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
