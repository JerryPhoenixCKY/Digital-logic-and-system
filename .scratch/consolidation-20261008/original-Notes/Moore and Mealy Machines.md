---
tags:
  - ECE2050
  - finite-state-machines
date: 2026-09-30
aliases:
  - Moore与Mealy状态机
  - Moore and Mealy Machines
  - FSM output models
---

# Moore and Mealy Machines · Moore与Mealy状态机

> [!SUMMARY] Quick recall · 英文速览
> Moore outputs depend on state; Mealy outputs depend on state and current input. Compare output timing using an explicit sampling convention, rather than saying one model is universally one clock faster.

## Core Definition · 核心定义

$$\text{Moore: }Y=G(S),\qquad \text{Mealy: }Y=G(S,X).$$

两者均有 $S^+=F(S,X)$。Moore 在节点中标输出；Mealy 在边上写 input/output。Mealy 可在 edge 之间响应 input，Moore 的组合 decode 也并非物理上绝对无毛刺。

## Worked Example · 检测最近两位 01

串行输入 x，每个正沿采一位，可重叠。Mealy 状态 A=尚无末尾 0，B=末尾为 0：

| State | x=0 | x=1 |
|---|---|---|
| A | B / 0 | A / 0 |
| B | B / 0 | A / 1 |

编码 B=1、A=0：$D=\bar x$，$Y=Qx$。当前 Q=1 且 x=1，就表示前位是 0、当前位是 1。

Moore 用 A=no match、B=末尾 0、C=刚检出 01；A:0→B,1→A；B:0→B,1→C；C:0→B,1→A；仅 C 的输出 1。把匹配事件编码到状态，需要此处第三个状态。

## Output Timing · 输出时间对齐

定义 x[k] 在第 k 个捕获边沿前稳定，S[k] 是该边沿前状态。Mealy 的 pre-edge 输出为 $G(S[k],x[k])$；Moore 的 post-edge 输出为 $G(S[k+1])$。两者可以对应同一个刚结束的输入位，只是有效窗口不同。

For input 0 then 1, Mealy can assert while the second bit is present before its capture edge. Moore asserts after that edge updates the machine into the detection state. Describing this as “one-cycle later” is meaningful only if the reference point is the arrival of the second input, not if both outputs are compared after the same capture edge.

Mealy 若 next state 在 edge 后立即回 A，输出会随着 Q 改变而撤销；接收者若也在该 edge 采样，可采到 edge 前的检测值，但必须满足 timing。不要画一个未经说明的固定整拍 pulse。

## Tradeoffs · 取舍

| Dimension | Moore | Mealy |
|---|---|---|
| Input in output cone | No direct input | Yes |
| State count | May be larger | Often smaller |
| Within-cycle input response | Through state update | Can respond immediately |
| Input glitch exposure | Less direct | Direct combinational path |
| Absolute glitch-free guarantee | No | No |

## Additional Example · 同一状态不同输出

一个 vending controller 当前等待付款。Mealy 输出 dispense 可依赖“当前 coin 使金额刚好达标”；Moore 则进入 DISPENSE state 后输出。该例只说明 output placement；具体零钱、输入同步和脉冲宽度应另定规范。

## Method and Review · 方法与复习

Check whether the output equation contains current input. Do not classify a diagram merely by the presence of arrows or number of states. Both state machines have input-dependent transitions.

**Exam answer:** “This is Mealy because its output is labeled on transitions and depends on current input as well as state. A Moore implementation places the detection indication in a state and changes the timing of that indication.”

## Connections · 相关笔记

[[Finite State Machine]], [[Sequence Detector]], [[Traffic Light Controller]], [[Setup and Hold Timing]], [[Testbench and Functional Verification]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
