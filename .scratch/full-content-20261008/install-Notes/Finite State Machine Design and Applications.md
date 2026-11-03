---
tags:
  - ECE2050
  - finite-state-machines
date: 2026-09-30
updated: 2026-10-09
chapter: Ch9
aliases:
  - 有限状态机设计与应用
  - Finite State Machine Design and Applications
  - 有限状态机设计与应用 · Ch9
  - Finite State Machine
  - 有限状态机
  - FSM
  - Moore and Mealy Machines
  - Moore与Mealy状态机
  - FSM output models
  - State Encoding and Unused States
  - 状态编码与未用状态
  - Binary and one-hot encoding
  - Sequence Detector
  - 序列检测器
  - Overlapping sequence detection
  - Traffic Light Controller
  - 交通灯控制器
  - Traffic control FSM
---

# Finite State Machine Design and Applications · 有限状态机设计与应用

> [!SUMMARY] Quick recall · 英文速览
> State summarizes the relevant past. Define state meaning before encoding, derive complete transitions, then verify traces and unused states.

## 1 · Finite State Machine · 状态保存了什么历史

有限状态机 (FSM) 为 $Q^+=F(Q,X)$。状态应代表完成任务所需的最小历史，而不是先任意列几个二进制数。流程是：规范→状态含义→转换图／表→输出→编码→方程→验证。

### Core Definition · 核心定义

有限状态机 (finite state machine) 用有限个状态概括历史。状态不只是“当前输出”，还要包含决定后续行为所需的信息。状态寄存器存 current state，组合逻辑计算 next state 与 outputs。

$$S[k+1]=F(S[k],X[k]).$$

此式适用于明确采样事件的同步 FSM。Moore/Mealy 的区别在输出函数，不在 next-state 是否依赖输入。

### Assumptions and Pitfalls · 条件与误区

- A state label such as S2 is a name, not necessarily binary 10.
- 时钟每拍更新的是编码，不是把图上的每条箭头都自动走一遍。
- 同一时钟并不保证输出完全无毛刺；实际输出 decode 仍有 delay。
- Registering a Mealy output changes its externally observed timing.

### State Meaning and Completeness · 状态含义与完备性

For each state, outgoing conditions must be mutually exclusive and cover every valid input. Missing an input case is not a legitimate don't-care unless the specification explicitly excludes it. Reset identifies a starting state and should match an actual available encoding.

设计与分析方向相反。已有电路的分析先写各 FF 输入，再由 characteristic equation 得到 Q+，把得到的 table 画成图。不能先凭外形猜“这是计数器”再填表。

> [!example]- Finite State Machine · 推导与例题
> **Design Procedure · 设计过程**
>
> 1. Identify inputs, outputs, polarity, sampling events, and reset behavior.
> 2. State what information must be remembered.
> 3. Draw a complete transition diagram.
> 4. Convert every arrow into transition/output tables.
> 5. Select an encoding and define unused-state behavior.
> 6. Derive storage-element inputs and output equations.
> 7. Verify transitions, outputs, reset, and timing.
>
> ```mermaid
> flowchart LR
>   Spec[Specification] --> Meaning[State meanings]
>   Meaning --> Table[Transition and output tables]
>   Table --> Encoding[State encoding]
>   Encoding --> Logic[Next-state equations]
>   Logic --> Verify[Trace and timing verification]
> ```
>
> **Worked Example · 按钮切换灯**
>
> 输入 X 为已同步且每次按下只一拍的 event；状态 OFF/ON，X=1 时切换，X=0 保持；Moore 输出 Y 在 ON 时 1。编码 OFF=0、ON=1。
>
> | Current Q | X | Next Q | Current Y |
> |---|---|---|---|
> | 0 | 0 | 0 | 0 |
> | 0 | 1 | 1 | 0 |
> | 1 | 0 | 1 | 1 |
> | 1 | 1 | 0 | 1 |
>
> $$D=Q\oplus X,\quad Y=Q.$$
>
> 从 OFF 输入 0,1,0,1，边沿后 Q 为 0,1,1,0。若 X 是持续三拍的 button level，电路会切换三次；这不是状态机方程错误，而是 event interface 没有实现需求。
>

### Exam English · 英文答题

**Question:** Why choose states before Boolean equations?

**Answer:** State meanings define what history must be retained and which transitions are required. Encoding is only a representation of that behavior. Deriving gates before fixing the behavior can produce a compact circuit that implements the wrong machine.

### Connections · 概念关系与应用

[[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]] 提供状态递推模型；[[Finite State Machine Design and Applications#2 · Moore and Mealy Machines · 输出依赖与时间对齐|Moore and Mealy Machines]] 指定输出依赖，[[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]] 指定表示与恢复。[[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀|Sequence Detector]]、[[Finite State Machine Design and Applications#5 · Traffic Light Controller · 安全条件进入状态模型|Traffic Light Controller]] 与 [[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励|Synchronous Counter Design]] 是不同状态语义的应用，最后通过 [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] 实现。

## 2 · Moore and Mealy Machines · 输出依赖与时间对齐

Moore 输出 $Y=G(Q)$，Mealy 输出 $Y=G(Q,X)$。Mealy 可在当前输入到达时响应，但可能受输入毛刺影响；Moore 的响应与进入状态对齐。比较两者时必须标明哪个周期的输出。

### Core Definition · 核心定义

$$\text{Moore: }Y=G(S),\qquad \text{Mealy: }Y=G(S,X).$$

两者均有 $S^+=F(S,X)$。Moore 在节点中标输出；Mealy 在边上写 input/output。Mealy 可在 edge 之间响应 input，Moore 的组合 decode 也并非物理上绝对无毛刺。

### Output Timing · 输出时间对齐

定义 x[k] 在第 k 个捕获边沿前稳定，S[k] 是该边沿前状态。Mealy 的 pre-edge 输出为 $G(S[k],x[k])$；Moore 的 post-edge 输出为 $G(S[k+1])$。两者可以对应同一个刚结束的输入位，只是有效窗口不同。

For input 0 then 1, Mealy can assert while the second bit is present before its capture edge. Moore asserts after that edge updates the machine into the detection state. Describing this as “one-cycle later” is meaningful only if the reference point is the arrival of the second input, not if both outputs are compared after the same capture edge.

Mealy 若 next state 在 edge 后立即回 A，输出会随着 Q 改变而撤销；接收者若也在该 edge 采样，可采到 edge 前的检测值，但必须满足 timing。不要画一个未经说明的固定整拍 pulse。

### Tradeoffs · 取舍

| Dimension | Moore | Mealy |
|---|---|---|
| Input in output cone | No direct input | Yes |
| State count | May be larger | Often smaller |
| Within-cycle input response | Through state update | Can respond immediately |
| Input glitch exposure | Less direct | Direct combinational path |
| Absolute glitch-free guarantee | No | No |

> [!example]- Moore and Mealy Machines · 推导与例题
> **Worked Example · 检测最近两位 01**
>
> 串行输入 x，每个正沿采一位，可重叠。Mealy 状态 A=尚无末尾 0，B=末尾为 0：
>
> | State | x=0 | x=1 |
> |---|---|---|
> | A | B / 0 | A / 0 |
> | B | B / 0 | A / 1 |
>
> 编码 B=1、A=0：$D=\bar x$，$Y=Qx$。当前 Q=1 且 x=1，就表示前位是 0、当前位是 1。
>
> Moore 用 A=no match、B=末尾 0、C=刚检出 01；A:0→B,1→A；B:0→B,1→C；C:0→B,1→A；仅 C 的输出 1。把匹配事件编码到状态，需要此处第三个状态。
>
> **Additional Example · 同一状态不同输出**
>
> 一个 vending controller 当前等待付款。Mealy 输出 dispense 可依赖“当前 coin 使金额刚好达标”；Moore 则进入 DISPENSE state 后输出。该例只说明 output placement；具体零钱、输入同步和脉冲宽度应另定规范。

### Method and Review · 方法与复习

Check whether the output equation contains current input. Do not classify a diagram merely by the presence of arrows or number of states. Both state machines have input-dependent transitions.

**Exam answer:** “This is Mealy because its output is labeled on transitions and depends on current input as well as state. A Moore implementation places the detection indication in a state and changes the timing of that indication.”

### Connections · 概念关系与应用

在 [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]] 框架中比较输出函数；[[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀|Sequence Detector]] 与 [[Finite State Machine Design and Applications#5 · Traffic Light Controller · 安全条件进入状态模型|Traffic Light Controller]] 给出时序窗口和控制应用；接收输出须满足 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]]，[[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]] 应分别检查 edge 前与 edge 后的有效窗口。

## 3 · State Encoding and Unused States · 编码与恢复

M 态二进制编码至少 $\lceil\log_2M\rceil$ 位，独热编码使用 M 位。初始化必须进入合法状态；未用状态可否当 X 取决于规范，若要求恢复，需定义实际下一态而非任意删去。

### Core Definition and Derivation · 定义与推导

N 个状态由 b 位寄存器编码，需要 $2^b\ge N$，所以 $b=\lceil\log_2N\rceil$。one-hot 每状态一位，合法域恰好一个 1，需要 N 位。

| N | Minimum binary FFs | One-hot FFs | Unused binary codes |
|---|---|---|---|
| 3 | 2 | 3 | 1 |
| 4 | 2 | 4 | 0 |
| 5 | 3 | 5 | 3 |
| 10 | 4 | 10 | 6 |

One-hot often simplifies the logic because state membership is available directly as one bit. More flip-flops do not automatically mean slower logic. Area and delay depend on mapping, routing, and the target hardware.

### Don't-Care Policy · 无关项策略

把 11 标 X 可能进一步化简 binary next-state equations，但所得 implementation 对 11 有具体行为。必须把最终 equations 在 11 代入，确认它是 recover、lock 或另一个 cycle。

“Unused in normal operation” is not equivalent to “physically impossible.” Power-up, disturbances, reset inconsistencies, or design mistakes can produce an unused code. The course may allow don't-cares for minimization; engineering recovery requires additional behavior and verification.

对于 one-hot 有 $2^N-N$ 个非法码。定义 `others` 的 RTL 分支有助于描述意图，但综合可能按其 FSM优化/编码策略改变实现；要核对实际实现与约束，不能把一行 default 当作物理安全证明。

> [!example]- State Encoding and Unused States · 推导与例题
> **Worked Example · 三态循环**
>
> 行为 A→B→C→A。binary 编码 A=00,B=01,C=10；给 unused 11→00 恢复：
>
> | Q1Q0 | Next |
> |---|---|
> | 00 | 01 |
> | 01 | 10 |
> | 10 | 00 |
> | 11 | 00 |
>
> $$D_1=\bar Q_1Q_0,\qquad D_0=\bar Q_1\bar Q_0.$$
>
> one-hot 向量 $(q_C,q_B,q_A)$：001→010→100→001，$q_A^+=q_C,q_B^+=q_A,q_C^+=q_B$。合法域下只有连线即可；但 000 会自锁，multi-hot 会循环，必须另加 reset/illegal-state recovery 才能满足完整规范。
>

### Method and Review · 方法与复习

1. List semantic states before assigning bits.
2. Record the encoding next to the diagram and tables.
3. Re-derive each next-state bit under that encoding.
4. Check reset and every unused code.
5. Compare logic and FF costs using the actual implementation.

**Question:** Why can the same FSM have different equations in two answers?

**Answer:** Different state encodings assign different bit patterns to the same semantic states. The Boolean equations can differ while the externally specified transitions and outputs remain equivalent.

### Connections · 概念关系与应用

[[Number Systems and Base Conversion#4 · Bits and Bytes · 位宽与容量|Bits and Bytes]] 给出编码容量；[[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]] 只能使用规范许可的 X；[[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]] 的语义在不同编码中应一致。[[Shift Registers and Ring Counters#3 · Ring and Johnson Counters · 同样的移位，不同的反馈|Ring and Johnson Counters]] 与 [[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励|Synchronous Counter Design]] 展示非法循环/恢复，[[Programmable Logic and FPGA#3 · Field-Programmable Gate Array · 从函数到物理实现|Field-Programmable Gate Array]] 的映射决定实际资源与时延。

## 4 · Sequence Detector · 最长可复用后缀

检测串行 110，定义 S0 无匹配、S1 已见末尾 1、S2 已见末尾 11。S0 在 1→S1、0→S0；S1 在 1→S2、0→S0；S2 在 1→S2、0 时断言检测并回 S0。重叠检测用匹配后的最长有效后缀决定回退。

检测 101 后若允许重叠，应保留末尾 1，因此 10101 可触发两次。并行字中出现某模式则属于组合逻辑，不能照搬串行状态机。

### Specification · 明确规范

本篇检测串行 110，高有效 input x，一位每正沿，Mealy 输出 z，允许重叠。状态表示已匹配的最长前缀：A=none、B=1、C=11。reset→A。

### Encoded Equations · 编码方程

令 A=00,B=01,C=10；规定 11 对任意 x 恢复 A 且 z=0：

$$D_1=x(Q_1\oplus Q_0),\qquad D_0=x\bar Q_1\bar Q_0,\qquad z=Q_1\bar Q_0\bar x.$$

检查 C=10,x=1 得 D=10；C,x=0 得 D=00,z=1。编码域 11 时 XOR=0、两个 D=0，z=0，符合恢复规定。输出是在 current state 与 current input 的组合窗口内有效。

> [!example]- Sequence Detector · 推导与例题
>
> **Derivation · 最长后缀原则**
>
> - A 收 0：没有前缀可保留，留 A；收 1：到 B。
> - B 收 0：10 的后缀没有前缀 1，回 A；收 1：到 C。
> - C 收 1：111 的最长相关后缀仍是 11，留 C。
> - C 收 0：110 匹配，输出 1；110 的后缀没有以 1 开始的可用前缀，回 A。
>
> | State | x=0 next / z | x=1 next / z |
> |---|---|---|
> | A | A / 0 | B / 0 |
> | B | A / 0 | C / 0 |
> | C | A / 1 | C / 0 |
>
> ```mermaid
> stateDiagram-v2
>   [*] --> A
>   A --> A: 0 / 0
>   A --> B: 1 / 0
>   B --> A: 0 / 0
>   B --> C: 1 / 0
>   C --> C: 1 / 0
>   C --> A: 0 / 1
> ```
>
> **Worked Example · 追踪 1110110**
>
> | Bit number | Input | Pre-state | z | Post-state |
> |---|---|---|---|---|
> | 1 | 1 | A | 0 | B |
> | 2 | 1 | B | 0 | C |
> | 3 | 1 | C | 0 | C |
> | 4 | 0 | C | 1 | A |
> | 5 | 1 | A | 0 | B |
> | 6 | 1 | B | 0 | C |
> | 7 | 0 | C | 1 | A |
>
> 匹配结束于第 4、7 位。111 中保持 C 是为了不丢掉最近两个 1；若每次多一个 1 就 reset，会漏掉第 4 位结束的匹配。
>
> **Overlap Example · 101 的重叠**
>
> 对于 101，检测完成后最后一个 1 可以作为下一次的首位，故返回“已看到 1”的状态，而不是无匹配状态。输入 10101 有两个 match，结束于位 3、5。110 的完成后没有这样的非空可复用后缀，所以本例回 A 仍正确。

### Method and Exam English · 方法与答题

For each state and input, append the new symbol and keep the longest suffix that is also a prefix of the target pattern. This rule handles repeated symbols and overlap systematically.

- 明确 simultaneous word detection 与 serial detection，见 [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]]。
- 标注 Mealy 输出在 edge 前窗口还是 registered post-edge pulse。
- 最少测试 exact match、near miss、重复前缀、连续匹配和 reset。

**Exam answer:** “Each state represents the longest suffix that remains useful for matching the target. On a completed match, I retain any suffix that can start another match, so overlapping occurrences are not lost.”

### Connections · 概念关系与应用

先按 [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]] 定义有用历史，再按 [[Finite State Machine Design and Applications#2 · Moore and Mealy Machines · 输出依赖与时间对齐|Moore and Mealy Machines]] 规定检测窗口，以 [[Finite State Machine Design and Applications#3 · State Encoding and Unused States · 编码与恢复|State Encoding and Unused States]] 编码；[[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] 是保存全部最近符号的另一思路；重叠、复位和边界由 [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]] 核对。

## 5 · Traffic Light Controller · 安全条件进入状态模型

交通灯状态规定哪条路通行以及黄色过渡；传感器决定是否保持／转移，定时器决定最短或最长持续时间。给每个状态完整输出，使冲突方向不会同时绿灯；复位状态、请求优先级和异常恢复必须明确。

### Specification · 规范与模型边界

这是双道路教学模型，不是道路安全控制完整规范。状态 A=A绿/B红，B=A黄/B红，C=A红/B绿，D=A红/B黄。TA/TB=1 表示相应道路有车；reset→A。

本例 A 在 TA=1 时保持、TA=0 时到 B；B 一拍后到 C；C 在 TB=1 时保持、TB=0 时到 D；D 一拍后回 A。现实 yellow duration、all-red clearance 与 fairness 需另加 timer/state。

### Transition Table · 转换表

| State | Condition | Next |
|---|---|---|
| A | TA=1 | A |
| A | TA=0 | B |
| B | Any | C |
| C | TB=1 | C |
| C | TB=0 | D |
| D | Any | A |

Use X only for an input that genuinely has no effect in that state. The B and D rows cover all four sensor combinations; they are not missing input cases.

### Derivation · 编码与输出

取 A=00,B=01,C=10,D=11，$Q_1Q_0$ 为当前编码。逐行写每一位 next=1 的情况：

$$D_1=Q_1\oplus Q_0,$$
$$D_0=\bar Q_1\bar Q_0\bar T_A+Q_1\bar Q_0\bar T_B.$$

输出灯编码 green=00,yellow=01,red=10，则：

$$L_{A1}=Q_1,\quad L_{A0}=\bar Q_1Q_0,\quad L_{B1}=\bar Q_1,\quad L_{B0}=Q_1Q_0.$$

两位 lamp code 是功能编码，不能直接等同于三个 LED 的引脚驱动。每盏实际红黄绿灯还需 decode 和相应电气接口。

### Timer Extension · 定时器扩展

若 yellow 要 3 s、clock event 为 1 Hz，可以增加三拍黄灯状态或单独的 timer counter。进入 yellow 时清零，达到 terminal count 才允许转换。必须定义“从进入开始算三拍”的边沿约定，避免 2 s/4 s 的 off-by-one。

If a problem defines TL=1 while a long timer is running and TL=0 when expired, expiration is NOT TL. Different diagrams may use the opposite convention. Translate the wording into a predicate rather than transferring equations between differently labeled controllers.

### Safe recovery · 安全恢复的范围

本四态二进制教学例已使用 00–11 全部编码，因此没有可供“其余码”恢复的二进制状态；reset→A 是该模型的规定起点，并不等于真实交通系统必须选择的安全重启状态。若新增 all-red、计时状态或采用 one-hot 编码，应分别规定非法编码时的灯输出和下一态，核对是否能进入安全状态并继续运行。

完整验证同时检查输出不冲突、最短黄灯/清空时长、最大绿灯/公平性、输入事件与复位恢复。综合后的 FSM 编码与恢复逻辑也要与这些要求一致；仅在 RTL 中写 `others` 不能证明物理系统的全部安全性质。

> [!example]- Traffic Light Controller · 推导与例题
>
> **Worked Example · 状态追踪**
>
> reset 后 A。TA=1 时两拍留 A；TA=0 时下一 edge 到 B；随后到 C；TB=1 时留 C；TB=0 时到 D；再回 A。每个 output 从**当前状态**解码，因此在 A→B 的更新之后才显示 A 黄。
>
> Check the invariant: no legal state has both roads green. The four-state model passes that check, but it can starve the other road if the active-road sensor remains TRUE forever. Add a maximum-green timer if fairness is part of the specification.
>

### Method and Exam English · 方法与答题

1. Separate semantic light states from their bit encodings.
2. Write every transition condition with explicit sensor/timer polarity.
3. Derive next-state and output equations independently.
4. Verify legal outputs and simulate sensor traces.
5. State the limits of the simplified control policy.

**Exam answer:** “The controller is Moore because its light outputs depend only on the encoded current state. The traffic sensors affect the next-state decision, while the output decoder maps each state to the required lamp codes.”

### Connections · 概念关系与应用

状态与输出分别依 [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]]、[[Finite State Machine Design and Applications#2 · Moore and Mealy Machines · 输出依赖与时间对齐|Moore and Mealy Machines]] 建模；[[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] 把灯编码映射为控制，[[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] 与 [[Counter Design and Digital Clocks#3 · Cascaded Counters and Digital Clocks · 进位是被接受的翻转|Cascaded Counters and Digital Clocks]] 提供时长事件；所有采样与输出接收仍受 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] 约束。

## 6 · 方程与验证的接口

用所选触发器求每位激励；对全部状态×输入检查下一态和输出。测试覆盖状态、每条转移、重叠、复位、无效态与规定的输出时间。逻辑证明之外，路径还需满足时序约束。

> [!IMPORTANT] 先证明状态含义正确，再优化编码
> 少一个状态位不一定少逻辑；不能为了化简牺牲未用态恢复、安全输出或输入周期对齐。

## Sources · 课件依据

主线课件：[Ch9 lecture](../LGU_HUB_ECE2050/ECE2050-Chap9.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
