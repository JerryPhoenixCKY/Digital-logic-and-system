---
tags:
  - ECE2050
  - finite-state-machines
date: 2026-09-30
aliases:
  - 交通灯控制器
  - Traffic Light Controller
  - Traffic control FSM
---

# Traffic Light Controller · 交通灯控制器

> [!SUMMARY] Quick recall · 英文速览
> A traffic-light FSM separates state transitions from output encoding. Sensor polarity, timer meaning, and yellow-light duration must be specified before deriving equations.

## Specification · 规范与模型边界

这是双道路教学模型，不是道路安全控制完整规范。状态 A=A绿/B红，B=A黄/B红，C=A红/B绿，D=A红/B黄。TA/TB=1 表示相应道路有车；reset→A。

本例 A 在 TA=1 时保持、TA=0 时到 B；B 一拍后到 C；C 在 TB=1 时保持、TB=0 时到 D；D 一拍后回 A。现实 yellow duration、all-red clearance 与 fairness 需另加 timer/state。

## Transition Table · 转换表

| State | Condition | Next |
|---|---|---|
| A | TA=1 | A |
| A | TA=0 | B |
| B | Any | C |
| C | TB=1 | C |
| C | TB=0 | D |
| D | Any | A |

Use X only for an input that genuinely has no effect in that state. The B and D rows cover all four sensor combinations; they are not missing input cases.

## Derivation · 编码与输出

取 A=00,B=01,C=10,D=11，$Q_1Q_0$ 为当前编码。逐行写每一位 next=1 的情况：

$$D_1=Q_1\oplus Q_0,$$
$$D_0=\bar Q_1\bar Q_0\bar T_A+Q_1\bar Q_0\bar T_B.$$

输出灯编码 green=00,yellow=01,red=10，则：

$$L_{A1}=Q_1,\quad L_{A0}=\bar Q_1Q_0,\quad L_{B1}=\bar Q_1,\quad L_{B0}=Q_1Q_0.$$

两位 lamp code 是功能编码，不能直接等同于三个 LED 的引脚驱动。每盏实际红黄绿灯还需 decode 和相应电气接口。

## Worked Example · 状态追踪

reset 后 A。TA=1 时两拍留 A；TA=0 时下一 edge 到 B；随后到 C；TB=1 时留 C；TB=0 时到 D；再回 A。每个 output 从**当前状态**解码，因此在 A→B 的更新之后才显示 A 黄。

Check the invariant: no legal state has both roads green. The four-state model passes that check, but it can starve the other road if the active-road sensor remains TRUE forever. Add a maximum-green timer if fairness is part of the specification.

## Timer Extension · 定时器扩展

若 yellow 要 3 s、clock event 为 1 Hz，可以增加三拍黄灯状态或单独的 timer counter。进入 yellow 时清零，达到 terminal count 才允许转换。必须定义“从进入开始算三拍”的边沿约定，避免 2 s/4 s 的 off-by-one。

If a problem defines TL=1 while a long timer is running and TL=0 when expired, expiration is NOT TL. Different diagrams may use the opposite convention. Translate the wording into a predicate rather than transferring equations between differently labeled controllers.

## Method and Exam English · 方法与答题

1. Separate semantic light states from their bit encodings.
2. Write every transition condition with explicit sensor/timer polarity.
3. Derive next-state and output equations independently.
4. Verify legal outputs and simulate sensor traces.
5. State the limits of the simplified control policy.

**Exam answer:** “The controller is Moore because its light outputs depend only on the encoded current state. The traffic sensors affect the next-state decision, while the output decoder maps each state to the required lamp codes.”

## Connections · 相关笔记

[[Finite State Machine]], [[Moore and Mealy Machines]], [[Decoder]], [[Counters]], [[Cascaded Counters and Digital Clocks]], [[Setup and Hold Timing]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
