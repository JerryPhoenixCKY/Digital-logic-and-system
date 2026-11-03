---
tags:
  - ECE2050
  - combinational-design
date: 2026-09-30
aliases:
  - 数字逻辑故障诊断
  - Digital Logic Troubleshooting
  - Stuck-at fault testing
---

# Digital Logic Troubleshooting · 数字逻辑故障诊断

> [!SUMMARY] Quick recall · 英文速览
> A useful test both activates a fault and propagates its effect to an observable output. A correct output on one input vector does not prove a circuit fault-free. Floating-input behavior requires an electrical model; it is not a universal Boolean constant.

## Core Definition · 核心定义

故障诊断 (troubleshooting) 是把“预期行为”与“实测行为”比较，选择能区分假设的试验，再定位原因。故障检测 (fault detection) 只证明至少有一个故障；故障定位 (fault diagnosis) 还需要区分哪个节点或元件出错。

A Boolean fault model is a simplified hypothesis, not a complete description of physical damage. A **stuck-at-0** node is modeled as always 0; a **stuck-at-1** node is always 1. Opens, bridges, excessive delay, and power faults may require different models.

先读 [[Combinational Circuit]] 确定节点与驱动者，再用 [[Boolean Equation]] 建立每个内部节点的预期函数；实际电压是否可解释为 0/1，要由 [[Logic Levels]] 和 [[Noise Margin]] 判断。

## Assumptions and Validity · 模型与适用条件

本篇布尔推导假设单一故障、输入处于有效逻辑电平、组合逻辑已稳定、测量不改变电路功能。多个故障可能互相掩盖，时序错误可能仅在高速或特定转换时出现。

An open input is **undriven**, not automatically HIGH. The observed level depends on input technology, internal bias, external pull resistors, leakage, coupling, and probe loading. If an exam explicitly states “an open input is read as 1,” use that assumption for that problem only.

CMOS 悬空输入可能在噪声作用下变化或停留在阈值附近；一些特定 TTL 输入在开路时表现为 HIGH，也不能推广到所有器件。未知浮空电压不能仅用布尔代数推出确定的真值表。

| Observation or hypothesis | Appropriate model | What it does not prove |
|---|---|---|
| Node always below valid LOW threshold | Stuck-at-0 candidate | Exact physical root cause |
| Node always above valid HIGH threshold | Stuck-at-1 candidate | Which upstream device failed |
| Input wire open | Undriven input with stated bias | A universal HIGH/LOW value |
| Wrong value only near transitions | Delay, glitch, sampling hypothesis | A static stuck-at fault |
| Both ends appear connected | Connectivity evidence | Adequate voltage or timing |

## Derivation · 故障激活与传播

设正常输出为 $F(\mathbf x)$，故障输出为 $F_f(\mathbf x)$，其中 $\mathbf x$ 是测试输入向量。检测条件是：

$$D_f(\mathbf x)=F(\mathbf x)\oplus F_f(\mathbf x)=1.$$

This is a comparison of good and faulty behavior under **the same input vector**. To detect an internal fault, first make the good node differ from the forced faulty value; then prevent downstream gates from hiding that difference.

故障敏化 (sensitization) 分为两步：**激活 (activation)** 和 **传播 (propagation)**。AND 的控制值 (controlling value) 是 0，OR 的控制值是 1；它们会覆盖另一输入的变化。传播路径上的旁路输入应取 non-controlling value：AND 取 1，OR 取 0。

| Gate on the propagation path | Set side input to | Reason |
|---|---|---|
| AND / NAND | 1 | A changing input still changes the output |
| OR / NOR | 0 | A changing input still changes the output |
| XOR / XNOR | Either fixed value | The output changes with the tested input |

这里说 XOR “两种固定值都能传播”只适用于旁路信号被控制住的情况。若故障同时影响两个 XOR 输入，两条路径的变化可能抵消；这称为 reconvergent masking，需要比较完整函数。

### Boolean sensitivity · 布尔敏感度

把内部节点 $n$ 视作局部变量，$F(n=0)\oplus F(n=1)$ 表示输出是否对 $n$ 敏感。这不是连续微积分导数；它用两个离散条件函数比较可观察性。

For $F=n+C$, sensitivity to n is $C\oplus1=\overline C$. Therefore C must be 0 to observe either stuck-at fault on n. Setting C=1 masks the fault, even when n itself has the wrong value.

## Worked Example 1 · AND–OR 网络的测试向量

正常电路 $n=AB$、$Y=n+C=AB+C$。假设内部节点 n stuck-at-0，故障输出 $Y_f=C$。按 C 分情况：C=1 时正常与故障都为 1；C=0 时差异就是 AB。所以：

$$D_{n/0}=AB\overline C.$$

The detecting vector is ABC=110. The good node n is 1, the faulty node is 0, and C=0 allows the difference to reach Y. ABC=111 activates the fault at n but masks it at the final OR gate.

若 n stuck-at-1，则 $Y_f=1$；要正常输出为 0，必须 C=0 且 AB=0。因此：

$$D_{n/1}=\overline C\,\overline{AB}=\overline C(\overline A+\overline B).$$

检测向量为 000、010、100，任选一个即可检测该假设；例如 000 时正常 Y=0、故障 Y=1。两向量集合 `{110,000}` 能分别检测 n 的两种 stuck-at 假设，却不能证明整个网络所有位置无故障。

| ABC | Good n | Good Y | n/0 output | n/1 output | Interpretation |
|---|---|---|---|---|---|
| 000 | 0 | 0 | 0 | 1 | Detect n/1 |
| 110 | 1 | 1 | 0 | 1 | Detect n/0 |
| 111 | 1 | 1 | 1 | 1 | Both output effects masked |

Moreover, B stuck-at-0 also produces Y=C. At the single observed output, this fault is indistinguishable from n stuck-at-0 for every input. Additional access to B or n, or electrical measurements, is needed for unique diagnosis.

## Worked Example 2 · MUX 的选择故障

一个 [[Multiplexer and Demultiplexer|2:1 MUX]] 满足 $Y=\overline S D_0+SD_1$。若选择端 S stuck-at-0，故障输出一直为 $D_0$。差异只在命令 S=1 且两个数据不同的时候出现：

$$D_{S/0}=S(D_0\oplus D_1).$$

Choose $(S,D_0,D_1)=(1,0,1)$. Good Y=1 and faulty Y=0. The vector (1,1,1) changes the selected route but gives the same data on both routes, so it cannot reveal a selection fault.

若只测试 `D0=D1=0` 和 `D0=D1=1`，会验证输出能高能低，却完全没有检查“选择是否正确”。实际测试应包括两路相反的数据，再交替选择。

For S stuck-at-1, use S=0 and unequal data. Exhaustive tests of all eight combinations also reveal data-input faults, but a failed output still needs a fault hypothesis before locating the cause.

## Worked Example 3 · 显示与转换器的故障症状

**Display symptom.** [[Seven-Segment Display and Code Conversion|七段显示]] 设定为 8，却看起来像 0。按标准字形，唯一差别为 g 段。因此候选原因包括 g 输出无效、g 连线/限流电阻开路、g 段损坏；一个外观症状无法区分这三者。

Command 0 and then 8 while holding the digit-select timing fixed. Segment g should change from off to on. Measure the driver output, then the segment voltage/current path; lamp test can help separate normal digit decoding from a segment-path failure.

若动态扫描每个数字都暗，先检查共同端与 digit enable；若只有一个数字异常，优先比较该位的共同端。若只有换位时有短暂重影，检查消隐时序，不能仅靠静态真值表找原因。

**Converter symptom.** 合法两位 BCD 转换器应输出 $N=10T+U$。从 00 递增测试，若纯二进制结果位 $N_5$（位权 32）stuck-at-0，00–31 都可能正确，第一次在 BCD 32 时可检测：正常 `0100000`，故障 `0000000`。

This example explains why testing only the largest value is weak: a particular fault may be masked by its expected bit value. A walking-bit or structured input set must be chosen from the function and fault model; not every converter bit can be independently controlled by arbitrary invalid BCD codes.

## Method and Steps · 实际排查流程

1. **State the symptom precisely.** Which output, which input vector or transition, and what expected value? Distinguish a repeatable failure from an intermittent one.
2. **Check the operating foundation.** 电源、地、时钟、复位与使能先确认；它们出错会让许多逻辑节点同时异常。
3. **Establish a good model.** 标节点，逐级写方程；有状态电路先指定初态与采样边沿，见 [[Sequential Logic]]。
4. **Choose a discriminating test.** 激活候选故障，把旁路输入设为不遮蔽值，再观察有效输出或中间节点。
5. **Measure from cause toward symptom.** Compare expected and measured values at successive nodes, respecting probe loading and instrument bandwidth.
6. **Verify the correction.** 重测原失败向量、相邻边界与关键转换；修好某个输入下的结果不是全部验证。

逻辑探针适合稳定的 HIGH/LOW，示波器适合电压幅度、边沿、毛刺与时延，逻辑分析仪适合多路数字时序。使用逻辑分析仪的数字判决结果前，仍需检查阈值是否适合被测电路。

## Common Errors · 常见误区

- A correct static truth table does not prove setup/hold timing or freedom from glitches; use [[Setup and Hold Timing]].
- 开路输出后的**接收输入**和开路之前的**驱动输出**是两个不同节点，不能继续当成同一根导线。
- Fault detection is not unique diagnosis. Two hypotheses with identical output functions need another observation point.
- 测到中间电压时应先承认逻辑值不确定；不要把所有结果强塞成 0/1，再做错误的布尔证明。
- Test vectors are meaningful only with the assumed input order, active polarity, and initial state stated explicitly.

## English Exam Q&A · 英文答题训练

**Q: Why must the side input of an OR gate be LOW when propagating a fault?** HIGH is the controlling value of OR and forces the output HIGH. LOW allows the tested input to determine the output.

**Q: Is an open input equivalent to stuck-at-1?** Only if the problem specifies that the undriven input is reliably interpreted as 1. In physical hardware, floating-input behavior depends on the device and bias network.

**Q: Can a test detect a fault without identifying its location?** Yes. Different faults may produce the same observable function. Detection proves a mismatch; diagnosis needs observations that distinguish the competing hypotheses.

## Method and Review · 复习检查

Use [[Proof by Perfect Induction]] to enumerate good and faulty functions, [[Laws and Rules of Boolean Algebra]] to derive detecting conditions, and [[Propagation Delay and Logic Hazards]] to separate static faults from transition problems.

每次结论应能补完一句：“在假设 ___ 下，输入 ___ 使正常节点为 ___、故障节点为 ___，并通过 ___ 路径到输出，所以可检测；但仍不能区分 ___。”

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
