---
tags:
  - ECE2050
  - counters
date: 2026-09-30
aliases:
  - 计数器
  - Counters
  - Binary and decade counters
---

# Counters · 计数器

> [!SUMMARY] Quick recall · 英文速览
> A counter stores and advances through a specified sequence. Modulus is the number of distinct states in its repeating cycle, not necessarily the maximum binary value plus one for an arbitrary sequence.

## Core Definition · 核心定义

计数器 (counter) 是有指定状态序列的 [[Finite State Machine]]。n 位 binary counter 的完整计数范围 0–$2^n-1$，modulus=$2^n$。十进制 BCD decade counter 走 0–9，modulus=10，需要 4 位但不是 mod16。

$$q^+=\begin{cases}(q+1)\bmod M,&\text{up}\\(q-1)\bmod M,&\text{down}.\end{cases}$$

此整数式定义规则计数，不描述不规则序列的通用 next-state logic。q 是编码/整数值；M 是完整循环的状态数。

## Asynchronous versus Synchronous · 异步与同步

异步 ripple counter：只有第一级直接由外部 clock 驱动，后级用前级输出边沿驱动；变化逐级 ripple。同步 counter：所有 FF 使用同一 clock，组合条件决定某一位是否翻转。

| Feature | Ripple counter | Synchronous counter |
|---|---|---|
| Clock inputs | Cascade from preceding stages | Common clock |
| Intermediate transition codes | Often significant | Still possible from clock-to-Q mismatch |
| Delay model | Can accumulate through stages | Clock-to-Q plus control/decode logic |
| Typical design analysis | Check edge polarity and Q/NOT Q connections | Derive all next states from old state |

“Synchronous” does not imply zero physical delay or glitch-free decoding. It describes the clock relationship. Enable and load behavior can also differ from chip to chip.

## Derivation · 同步二进制翻转条件

up counter 的 bit0 每拍翻转；bit1 在旧 bit0=1 时翻转；biti 在全部较低位都是 1 时翻转。因此：

$$T_0=1,\qquad T_i=\prod_{j=0}^{i-1}Q_j\quad(i\ge1),\qquad Q_i^+=Q_i\oplus T_i.$$

down counter 把条件改为较低位全 0：$T_i=\prod_{j=0}^{i-1}\bar Q_j$。可用 JK with J=K=T 实现。

## Worked Examples · 例题

**3-bit up.** 011→100：旧低位 Q0=Q1=1，所以 T0=T1=T2=1，三位都翻转。100→101 时低位旧 Q0=0，只有 T0=1，其余为 0。

**Ripple delay.** n=4、每级 clock-to-Q worst case=8 ns，在需贯穿所有级的 rollover 事件中，最终状态可在 32 ns 后才到达。哪些转换会达到该延迟，取决于各级触发边沿与 Q/NOT Q 接法；普通对应 up ripple 模型中的 0111→1000、1111→0000 会贯穿四级。

**Frequency.** 完整 binary ripple counter 的 bit i 输出重复频率为 $f_{clk}/2^{i+1}$，50% duty 在完整稳态周期中成立。mod3 的 decode pulse 可每三拍重复，但 duty 可能为 1/3，不是自动 50%。

## Control Inputs · 控制输入

Clear、load、enable、direction 与 terminal-count 控制应由 function table 指定。若同步 load LOW 优先于 count enable，则 LOAD=0 时即使 count disabled 也会在下一边沿加载；若器件另有条件，不得移植该假设。

For a modulo-10 down counter, 0000 decrements to 1001, not to 1111. For a full four-bit binary down counter, 0000 goes to 1111. The word “decade” changes the sequence.

## Method and Exam English · 方法与答题

1. Determine intended state sequence and initial state.
2. Identify synchronous versus ripple clocks.
3. Write each FF input and active edge.
4. Compute next states, including control priority.
5. Count the distinct states before the first repeated state.

**Exam answer:** “The modulus is the length of the repeating state cycle reached from the specified initial state. Although four flip-flops can represent sixteen codes, this decade counter uses only ten of them.”

## Connections · 相关笔记

[[JK and T Flip-Flops]], [[Synchronous Counter Design]], [[Ring and Johnson Counters]], [[Cascaded Counters and Digital Clocks]], [[Propagation Delay and Logic Hazards]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
