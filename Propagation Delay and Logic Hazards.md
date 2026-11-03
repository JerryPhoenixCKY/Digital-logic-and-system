---
tags:
  - ECE2050
  - timing
date: 2026-09-30
updated: 2026-10-13
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

讲义对应：[PDF p.47–54](../ECE2050-Chap6.pdf#page=47)。本篇先给一般路径规则，再单独还原 p.50 的网络与 p.52–53 的毛刺例题；不同例题的变量名和拓扑不能混用。

## 1 · 最长路径与最短路径

最大传播延迟 $t_{pd}$ (propagation delay) 表示最迟稳定时间；最小污染延迟 $t_{cd}$ (contamination delay) 表示最早可能变化时间，单位 s 或 ns。串联路径相加，多条路径分别取最大／最小，不能混用。

### Core Definition · 核心定义

传播延迟 (propagation delay) $t_{pd}$ 是从输入改变到输出保证稳定的最大延迟；污染延迟 (contamination delay) $t_{cd}$ 是输出最早可能开始改变的最小延迟。门的 rise/fall、不同输入路径与负载可有不同值，具体数值由题目或器件条件定义。

对无环网络，候选路径延迟是各门/连线延迟之和；取能够影响所需输出的最长路径为 $t_{pd}$，最短路径为 $t_{cd}$。功能敏化 (sensitization) 决定一个路径是否真正能传递变化。

> [!example]- Propagation Delay and Logic Hazards · 推导与例题
> **Worked Example 1 · 长短路径**
>
> 假设输入 A 经过 AND–AND–OR，输入 D 只经过 OR；AND 的 $(t_{pd},t_{cd})=(30,10)$ ps，OR 为 (20,8) ps。长路径=80 ps，短路径=8 ps。前提是对应路径可敏化；不应把所有并行门的延迟直接累加。
>
> The latest bound describes when the output is safe to sample after all relevant inputs have changed. The earliest bound matters when old data must remain stable, particularly for hold-time analysis. “The circuit delay” is incomplete unless it identifies which bound is needed.

### Lecture Critical and Short Paths · 逐门追踪原图，p.50

关键路径 (critical path) 是到所研究输出的最长有效延迟路径；短路径 (short path) 决定最早可能变化。讲义原图的节点定义为 $n_1=AB,n_2=n_1+C,Y=n_2D$，所以：

$$Y=D(AB+C).$$

| Input-to-output path · 路径 | Gates in order · 门顺序 | Maximum delay | Minimum delay |
|---|---|---|---|
| A 或 B → Y | AND → OR → AND | $2t_{pd,AND}+t_{pd,OR}$ | $2t_{cd,AND}+t_{cd,OR}$ |
| C → Y | OR → AND | $t_{pd,OR}+t_{pd,AND}$ | $t_{cd,OR}+t_{cd,AND}$ |
| D → Y | AND | $t_{pd,AND}$ | $t_{cd,AND}$ |

在各 AND 使用相同参数、忽略连线延迟且路径可敏化的讲义模型下，$t_{pd}=2t_{pd,AND}+t_{pd,OR}$，$t_{cd}=t_{cd,AND}$。让 A 的变化可见可取 B=D=1、C=0；让 D 的变化可见需令 $AB+C=1$。

**Self-calculated check：** AND 的 $(t_{pd},t_{cd})=(30,10)\ \mathrm{ps}$、OR 的 $(20,8)\ \mathrm{ps}$，原图得到 $t_{pd}=80\ \mathrm{ps}$、$t_{cd}=10\ \mathrm{ps}$。前面 Worked Example 1 的短支路只有 OR，因此是 8 ps；两者数值不同来自拓扑不同。

The delay comes from resistance, capacitance, finite signal propagation, and device switching. Rise/fall direction, input arc, loading, voltage and temperature can change the bounds; the lecture's temperature remark is qualitative and cannot replace specified operating-corner limits.

### Method and Exam English · 方法与英文

1. List paths to the requested output; include inversions.
2. Sum maximum and minimum delays separately.
3. State side-input values that make a path observable.
4. Compare steady-state truth with the actual transition sequence.
5. Evaluate whether the receiving element could capture the glitch.

**Exam answer:** “The Boolean output remains HIGH before and after the transition. Unequal delays temporarily remove both product terms, creating a static-1 hazard. The consensus term bridges the transition without changing the steady-state function.”

### Connections · 概念关系与应用

[[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|Combinational Circuit]] 的无环模型允许逐路径求延迟；[[Karnaugh Map Minimization#1 · Karnaugh Map · 为什么相邻格能够合并|Karnaugh Map]] 的邻格共同覆盖可检查单输入静态冒险；[[Universal Gates and Bubble Pushing]] 改变实现路径，[[Digital Foundations and Waveforms#2 · Digital Waveforms · 再把时间加入模型|Digital Waveforms]] 描述瞬态，最终采样窗口由 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] 约束。

## 2 · 静态冒险来自不同路径

毛刺 (glitch) 是输入转换后出现的短暂额外输出变化。冒险 (hazard) 是电路在某类转换下可能产生错误瞬态的性质；一次具体转换是否出现可见毛刺还取决于路径延迟和门的脉冲响应。

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

### Lecture Glitch Example · $Y=\bar A\bar B+BC$，p.52–53

讲义使用 $n_1=\bar A\bar B$、$n_2=BC$、$Y=n_1+n_2$。固定 A=0、C=1，让 **B 从 1 降为 0**。转换前 n2=1，转换后 n1=1，所以稳态 Y 前后均为 1；若 n2 已下降、n1 尚未上升，就出现静态 1 冒险。它与上面的通用例题同理，但变化输入是 B，新增项也须相应改变。

> [!example]- Consensus and timing trace · 从原图到数值时序
> ![[ch6-hazard-consensus.png]]
> *讲义 p.53 原图：$\bar AC$ 同时覆盖 C=1 行上 AB=00 与 01 两个相邻格，并通过第三条 AND 支路保持输出。*
>
> 共识项 (consensus term) 为 $\bar AC$：
>
> $$Y_{safe}=\bar A\bar B+BC+\bar AC.$$
> $$\bar AC=\bar A\bar BC+\bar ABC.$$
>
> 右侧两项分别被 $\bar A\bar B$ 与 BC 覆盖，因而不改变稳态真值表。A=0、C=1 且只有 B 变化时，新增支路始终为 1，桥接原来的路径间隙。卡诺图检查是“相邻 ON 格是否存在共同覆盖项”，不是只问每个 1 是否已被覆盖。
>
> **Self-calculated timing model：** 初始 A=0、B=1、C=1 已稳定；t=0 时 B 下降。假定反相器延迟 $1\ \mathrm{ns}$、AND 延迟 $2\ \mathrm{ns}$、OR 延迟 $1\ \mathrm{ns}$，均用不滤短脉冲的传输延迟 (transport delay) 模型，且忽略连线延迟：
>
> | Event · 事件 | Time |
> |---|---|
> | B 下降 | 0 ns |
> | $\bar B$ 上升 | 1 ns |
> | $n_2=BC$ 下降 | 2 ns |
> | $n_1=\bar A\bar B$ 上升 | 3 ns |
> | 原 Y 下降，再上升 | 3 ns、4 ns |
> | $Y_{safe}$ | 始终为 1 |
>
> ![[ch6-static-hazard-timing.svg]]
> *按上述自设延迟绘制：原输出有 1 ns 低脉冲；修正输出在这一单输入转换中维持 HIGH。横轴为时间，图中 n1/n2 与讲义变量一致。*
>
> 这不是芯片保证波形。真实门的惯性延迟 (inertial delay) 可能过滤足够短的脉冲，rise/fall 延迟也可能不同；稳态 Boolean 仿真本身无法证明没有毛刺。

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

讲义 p.54 的“glitches don't cause problems”依赖其同步设计约定 (synchronous design conventions)：组合输出作为数据，在接收寄存器的有效边沿及建立/保持窗口内已经稳定，且不直接作为时钟或异步控制。它不表示组合电路不再产生毛刺。添加共识项的保证也以两级实现、其余输入稳定和单输入变化为前提；多输入同时变化不由这项结论覆盖。

## Sources · 课件依据

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 6: Combinational Building Blocks*，[本次讲义](../ECE2050-Chap6.pdf#page=47)，PDF p.47–49：延迟定义与成因；p.50：$D(AB+C)$ 的长短路径；p.51–53：$\bar A\bar B+BC$ 的毛刺与共识项 $\bar AC$；p.54：同步采样与多输入转换的边界。PDF 页序与页脚编号一致。
- [库中原参考讲义](../LGU_HUB_ECE2050/ECE2050-Chap6.pdf)。通用 $AB+\bar AC$ 例子、路径数值和 1/2/1 ns 时序图为笔记补充；自设参数不代表器件保证值。

---
索引：[[ECE2050.1]] · [[Glossary]]
