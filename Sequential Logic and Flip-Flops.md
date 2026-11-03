---
tags:
  - ECE2050
  - sequential-logic
date: 2026-09-30
updated: 2026-10-27
chapter: Ch7
aliases:
  - 时序逻辑与触发器
  - Sequential Logic and Flip-Flops
  - 时序逻辑与触发器 · Ch7
  - Sequential Logic
  - 时序逻辑
  - Synchronous sequential circuits
  - Set-Reset Latch
  - 置位复位锁存器
  - SR latch
  - D Latch and D Flip-Flop
  - D锁存器与D触发器
  - D storage elements
  - JK and T Flip-Flops
  - JK与T触发器
  - JK excitation table
  - Register Enable and Reset
  - 寄存器使能与复位
  - Enabled and resettable registers
---

# Sequential Logic and Flip-Flops · 时序逻辑与触发器

> [!SUMMARY] Quick recall · 英文速览
> State records history. Distinguish level-sensitive storage from edge-triggered storage, then add explicit enable and reset priorities.

## 1 · Sequential Logic · 用状态连接过去与现在

时序逻辑 (sequential logic) 在有效事件处按 $Q^+=F(Q,X)$ 更新，输出由 Q 或 Q、X 决定。Q 是旧状态，不能在同一边沿逐个把新状态回灌其他触发器；组合反馈也不能自动当作受控时序电路。

### Core Definition · 核心定义

状态 (state) 是预测未来行为所需的历史信息，不一定包含全部过去输入。设当前状态 $Q[k]$、本周期输入 $X[k]$：

$$Q[k+1]=F(Q[k],X[k]).$$

Moore 输出 $Y[k]=G(Q[k])$；Mealy 输出 $Y[k]=G(Q[k],X[k])$。k 是 clock-cycle index，没有物理单位；实际 clock period T 有时间单位。

### Bistability · 双稳态的起点

讲义第 8–9 页以两个首尾相接的反相器 (cross-coupled inverters) 说明双稳态：若两个节点为 $Q$ 与 $\bar Q$，二值稳态方程 $Q=\overline{\bar Q}$、$\bar Q=\overline Q$ 同时允许 $(Q,\bar Q)=(0,1)$ 和 $(1,0)$。两种状态各存一 bit；但这个最简单的回路没有输入端，无法按需要选择或改变状态。下一节在反馈结构中加入 S、R 控制，才可有意置位或复位。物理启动及切换仍依赖器件和扰动，不能由二值稳态方程单独保证。

### Assumptions and Limits · 条件与边界

The recurrence is a functional model. Setup/hold must still be satisfied, asynchronous inputs must be handled, and reset must establish a specified starting state. Real outputs settle after clock-to-Q delay, not at exactly zero time.

不要把“不符合组合构成规则”的一切网络都称为“正常时序电路”。多驱动冲突可能是无定义连接；奇数反相回路可振荡；需逐类分析，不能套一个确定的 next-state table。

> [!example]- Sequential Logic · 推导与例题
> **Mechanism and Composition · 机制与构成**
>
> 寄存器提供边界，使组合反馈路径每经过一圈至少跨过一个状态元件。同步教学模型要求所有寄存器用同一 clock，至少有一个寄存器，组合部分无回路。组合输出在周期中可变化，寄存器状态只在指定事件更新。
>
> ```mermaid
> flowchart LR
>   Input[Current input] --> Next[Next-state combinational logic]
>   State[State register] --> Next
>   Next --> State
>   State --> Out[Output logic]
>   Input -. Mealy only .-> Out
> ```
>
> The arrows describe information flow. The feedback is broken in time by the register. An unclocked inverter loop can oscillate, and a bistable loop can store a bit; neither is automatically a reliable synchronous FSM.
>
> **Worked Examples · 例题**
>
> **Running parity.** 状态 Q 记录已接收 bit 的 odd/even parity，初值 0；$Q^+=Q\oplus X$。输入 1,0,1,1 后状态 1,1,0,1。只需记忆一个 bit，因为完整历史对未来 parity 不再必要。
>
> **Counter.** n-bit counter 的当前状态为整数 q，enabled 时 $q^+=(q+1)\bmod2^n$。当前 3 与当前 7 即使输入相同，下一个状态也不同，所以输出不能只由当前输入确定。
>
> **Simultaneous update.** 两个 DFF 有 $D_A=Q_B,D_B=Q_A$，初值 (QA,QB)=(1,0)。下一 edge 后 (0,1)，再后 (1,0)。两个右侧都必须从同一旧状态取值；先更新 QA 再用于 QB 会错误地得到 (0,0)。

### Method and Review · 方法与复习

- Identify the state variables and initial values.
- Write input equations for every storage element.
- Substitute the characteristic equation to obtain next state.
- 从同一当前状态求全部 $Q^+$，随后统一更新。
- Check the active edge, asynchronous controls, and output type separately.

**Exam question:** Why is a sequence detector sequential when a four-bit pattern detector is combinational?

**Answer:** A serial detector receives one symbol at a time and must remember earlier symbols. A four-bit detector receives the entire relevant pattern simultaneously, so its output can be computed from current inputs alone.

### Connections · 概念关系与应用

与 [[Boolean Algebra and Circuit Models#1 · Combinational Circuit · 先确认可以使用的模型|Combinational Circuit]] 比较是否需要历史；[[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]] 的反馈和 [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]] 的捕获提供状态单元，再组成 [[Finite State Machine Design and Applications#1 · Finite State Machine · 状态保存了什么历史|Finite State Machine]]、[[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]] 与 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]]。

## 2 · Set-Reset Latch · 反馈产生记忆

NOR 型 SR 锁存器的 S、R 高有效：00 保持、10 置 1、01 清 0、11 禁止。NAND 型低有效 $\bar S,\bar R$：11 保持、01 置 1、10 清 0、00 禁止。禁态及其同时释放无法用普通稳态表保证结果。

### Core Definition · 核心定义

锁存器 (latch) 利用双稳态 (bistability) 保存一位 Q。对交叉 NOR、S 和 R 高有效：$Q=\overline{R+\bar Q}$，$\bar Q=\overline{S+Q}$。这里 $\bar Q$ 是互补输出标签；禁态时它并不保证等于 NOT Q。

| S | R | Action | Q next |
|---|---|---|---|
| 0 | 0 | Hold | Previous Q |
| 1 | 0 | Set | 1 |
| 0 | 1 | Reset | 0 |
| 1 | 1 | Invalid | Both outputs forced 0 while asserted |

### NAND Variant · NAND 型

交叉 NAND 的输入为低有效 $\bar S,\bar R$：11 保持，01 置位，10 复位，00 禁态且两个输出都 HIGH。记忆规则“都不有效时保持，两个都有效时禁态”比死记 00/11 更稳。

| NOR active-high | NAND active-low | Meaning |
|---|---|---|
| S=0,R=0 | $\bar S=1,\bar R=1$ | Hold |
| S=1,R=0 | $\bar S=0,\bar R=1$ | Set |
| S=0,R=1 | $\bar S=1,\bar R=0$ | Reset |
| S=1,R=1 | $\bar S=0,\bar R=0$ | Invalid |

> [!example]- Set-Reset Latch · 推导与例题
> **Derivation · 为什么能保持**
>
> S=R=0 时，Q 与另一个输出互相取反，(Q,other)=(0,1) 与 (1,0) 都自洽。输入不指定新的状态，反馈保持已有状态。S=1 强迫另一输出为 0，随后 Q=1；R=1 对称地强迫 Q=0。
>
> The invalid input is not merely a harmless unused truth-table row. Both NOR outputs are LOW, and when both controls are released together, delay imbalance may determine the final state. It can become unpredictable or temporarily metastable.
>
> 在排除 S=R=1 的合法域内，特征式为：
>
> $$Q^+=S+\bar RQ.$$
>
> 不能用此式给禁态制造“优先级”。原 NOR latch 的禁态行为由电路决定，不等于具有 set priority 的新设计。
>
> **Worked Example · 事件序列**
>
> NOR 型初值 Q=0，依次 (S,R)=10、00、01、00，状态依次 1、1、0、0。NAND 型等价输入依次 01、11、10、11，得到相同状态序列。
>
> If a waveform enters the invalid input condition, mark it explicitly. Do not continue the trace by choosing a convenient remembered value unless the question gives a release priority or delay assumption.

### Method and Review · 方法与复习

1. Identify NOR versus NAND and input bubbles.
2. Translate voltage levels into asserted/unasserted controls.
3. Segment the waveform at every S or R transition.
4. Apply set/reset/hold and preserve the initial state.
5. Label invalid assertion and uncertain release behavior.

**Exam question:** Is Q=0 necessarily an invalid state?

**Answer:** No. Q=0 is the valid reset state when the complementary output is 1. Invalidity concerns the control combination and loss of complementary outputs, not the stored value zero.

### Connections · 概念关系与应用

[[Logic Gates and Boolean Functions#3 · NAND Gate and NOR Gate · 输出取补与气泡|NOR Gate]] 与 [[Logic Gates and Boolean Functions#3 · NAND Gate and NOR Gate · 输出取补与气泡|NAND Gate]] 决定控制极性；反馈是 [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]] 的最小存储例子，受控输入形成 [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]]。禁态释放的不确定性与 [[Sequential Timing and Clock Domain Crossing#3 · Metastability and Clock Domain Crossing · 异步输入的边界|Metastability and Clock Domain Crossing]] 的物理问题相联系。

## 3 · D Latch and D Flip-Flop · 电平与边沿

D 锁存器在有效使能电平透明，其余时间保持；D 触发器只在规定有效边沿捕获 D。$Q^+=D$ 仅描述捕获事件，边沿之间保持旧 Q；异步控制另按规定优先处理。

### Core Definition · 核心定义

高电平透明 D latch 用 E 使能：E=1 时 Q 跟随 D，E=0 时保持。对合法二值稳态模型：

$$Q^+=ED+\bar EQ.$$

正沿 DFF 则在 rising edge 上 $Q^+=D$，边沿之间保持。三角形 clock 符号表示边沿触发；若三角形前有气泡，通常表示 falling edge。

### Assumptions and Pitfalls · 条件与误区

The input must satisfy setup and hold around the capture event. For a latch, the closing event is important; while open, propagation from D to Q is also relevant. A transparent latch cannot be treated as an edge-triggered register by merely drawing its output changes at edges.

- Rising-edge triggering is a symbol/HDL property, not a universal property of every FF.
- 没有 reset 时，实际初态未必已知；例题初态须声明。
- “Sequential statements” in VHDL does not automatically mean sequential hardware.

### Edge pulse · 由传播延迟产生边沿脉冲

讲义第 21 页展示正边沿脉冲检测 (positive-edge pulse detector)：一条路径直接传递 CLK，另一条经反相器延迟，再送入 NAND。CLK 上升后、反相信号尚未变低的短暂区间内，两路暂时均为高，NAND 输出产生短暂**低脉冲**；稳定后输出恢复高电平。讲义图中后级反相缓冲器又把它变成短暂高脉冲。脉宽取决于实际路径延迟和器件阈值，并非理想固定值。它说明延迟可以把边沿转换成脉冲，但不是对所有 DFF 内部实现的描述；不应将这种未约束的组合脉冲当作可靠时钟或通用脉宽保证。参见 [[Propagation Delay and Logic Hazards]]。

### Comparison · 对比

| Feature | D latch | Positive-edge DFF |
|---|---|---|
| Sensitive event | Entire enabled level | LOW→HIGH edge |
| Q can follow D mid-HIGH | Yes | No |
| Storage while inactive | Holds | Holds between edges |
| Basic HDL pattern | Incomplete level conditional | `rising_edge(clk)` |

> [!example]- D Latch and D Flip-Flop · 推导与例题
> **Derivation · 消除 SR 禁态**
>
> 由 [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]] 的高有效 SR 型，取 $S=ED,R=E\bar D$。E=0 时 S=R=0 保持；E=1 时只有一个控制有效，因此不会产生 S=R=1。
>
> Two D latches controlled on opposite clock levels form an idealized master-slave DFF. At CLK=0, the master tracks D while the slave holds. When CLK rises, the master closes and the slave opens, transferring the captured master value to Q. Practical implementation must avoid uncontrolled overlap of transparency windows.
>
> **Worked Examples · 波形例题**
>
> **Example 1.** CLK 0→1 时 D=0；CLK 保持 1 时 D 变 1；CLK 1→0 时 D 仍 1。D latch：先 0，再跟随为 1，下降后保持 1。正沿 DFF：正沿采 0，中途保持 0；要等下一个正沿才可能采 1。
>
> **Example 2.** 有效正沿前 D 依次为 1,0,1,1，DFF 初值 0；边沿后 Q 为 1,0,1,1。每次值只在 clock-to-Q 延迟后出现在物理输出，不是刚改变 D 就输出。
>
> **Example 3.** DFF 的 D 接 NOT Q。每个正沿 $Q^+=\bar Q$，输出每两次 clock 才完成一个周期，所以 $f_Q=f_{clk}/2$。该连接实现无使能的 toggle function。

### Exam English · 英文答题

**Question:** Why does Q remain unchanged when D changes while CLK is HIGH in a positive-edge DFF?

**Answer:** The flip-flop samples only on the LOW-to-HIGH clock transition. A later data change is outside that capture event, so the stored state remains unchanged until the next active edge, provided no asynchronous control is asserted.

### Connections · 概念关系与应用

用 [[Digital Foundations and Waveforms#2 · Digital Waveforms · 再把时间加入模型|Digital Waveforms]] 追踪透明窗口与边沿；[[Sequential Logic and Flip-Flops#5 · Register Enable and Reset · 控制优先级|Register Enable and Reset]] 增加控制，[[Sequential Logic and Flip-Flops#4 · JK and T Flip-Flops · 条件更新|JK and T Flip-Flops]] 给出其他更新规则；采样必须满足 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]]，可用 [[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] 描述并组成 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]]。

## 4 · JK and T Flip-Flops · 条件更新

JK 的 00 保持、01 清零、10 置位、11 翻转，$Q^+=J\bar Q+\bar KQ$。T 触发器 $Q^+=T\oplus Q$。特性表 (characteristic table) 从输入求下一态；激励表 (excitation table) 从所需 Q→Q+ 求输入，方向不同。

### Core Definition and Derivation · 定义与推导

在有效边沿，JK 特征式：

$$Q^+=J\bar Q+\bar KQ.$$

若 Q=0，$Q^+=J$；若 Q=1，$Q^+=\bar K$。直接由当前状态分组得到特征式，比背诵全表更容易验证。

| J | K | Action |
|---|---|---|
| 0 | 0 | Hold |
| 0 | 1 | Reset |
| 1 | 0 | Set |
| 1 | 1 | Toggle |

TFF 用 $J=K=T$，得到 $Q^+=Q\oplus T$。T=0 保持，T=1 翻转；也可用 DFF 与 XOR 实现 $D=Q\oplus T$。

### Excitation Table · 激励表

| Q | $Q^+$ | J | K | T | D |
|---|---|---|---|---|---|
| 0 | 0 | 0 | X | 0 | 0 |
| 0 | 1 | 1 | X | 1 | 1 |
| 1 | 0 | X | 1 | 1 | 0 |
| 1 | 1 | X | 0 | 0 | 1 |

X means either binary value achieves the required transition. These excitation don't-cares are justified by the current Q value. They differ from declaring an unused state globally irrelevant.

### Conversion · 元件转换

- JK using DFF: connect $D=J\bar Q+\bar KQ$.
- DFF using JK: $J=D,K=\bar D$.
- TFF using JK: $J=K=T$.
- 无使能 toggle 用 DFF：$D=\bar Q$。

使用 2:1 MUX 也能实现 JK 的 D 式：select Q，D0=J，D1=NOT K。Q=0 选 J；Q=1 选 NOT K。这里 MUX 的 select 是**当前输出 Q**，不是 clock。

> [!example]- JK and T Flip-Flops · 推导与例题
>
> **Worked Examples · 例题**
>
> **Trace.** Q 初值 0，连续有效边沿的 JK 输入为 10、11、00、01，Q 变为 1、0、0、0。最后 reset 没有产生边沿以外的动作，因为这是同步 JK 输入。
>
> **Design one bit.** 状态要求 0→1、1→0，激励表给 0 时 J=1，1 时 K=1；选择 J=K=1 可满足两种转换。输出以输入 clock 一半频率翻转。
>
> **Race-around boundary.** Level-sensitive JK feedback with J=K=1 can toggle repeatedly during a long enabled pulse. An edge-triggered or suitable master-slave implementation limits updating to the intended event. Do not apply the edge table blindly to a transparent feedback latch.

### Method and Review · 方法与复习

分析题：先求 J,K，再代 characteristic equation 求全部 next states。设计题：先给 desired transitions，再查 excitation table 求 J,K，最后化简。

**Exam question:** Why is K a don't-care for the transition 0→1?

**Answer:** With Q=0, the term $\bar KQ$ is zero regardless of K. The next state therefore depends only on J, and J must be 1.

### Connections · 概念关系与应用

通过 [[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]] 与 [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]] 实现相同特征函数；[[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励|Synchronous Counter Design]] 反向查激励表，[[Karnaugh Map Minimization#4 · Karnaugh Map with Don't Cares · 无关项是许可而非义务|Karnaugh Map with Don't Cares]] 化简有根据的 X；所有 next states 仍遵守 [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]] 的统一旧状态更新。

## 5 · Register Enable and Reset · 控制优先级

使能 E 的 D 寄存器：$Q^+=ED+\bar EQ$。同步复位只在有效边沿执行；异步复位可在边沿之间改变 Q，释放仍要满足器件恢复／移除等时序条件。复位、置位、装载、保持同时有效时，必须由规范规定优先级。

> [!IMPORTANT] 波形题先列事件表
> 明确有效边沿、透明电平、初态、控制极性和优先级；使用边沿前的值计算所有 Q+，再一起更新。上电初态不能默认是 0。

### Core Definition · 核心定义

寄存器 (register) 由多位状态元件组成，通常共享 clock。对每一位，高有效 EN 的 enabled DFF：

$$Q^+=EN\cdot D+\overline{EN}\cdot Q.$$

EN=0 的保持用输出反馈到输入的 MUX 实现。不是把 clock 用普通 AND 随意截断；clock gating 的可靠实现需要专门时序约束。

### Reset and Set · 复位与置位

高有效 synchronous reset R：只在有效边沿执行，$Q^+=0$ if R=1，否则正常 load/hold。高有效 asynchronous reset：R=1 时不用等 clock 就把 Q 强制为 0。set/preset 对称地强制为 1。

If reset has priority over enable, the next-state rule is:

$$Q^+=\begin{cases}0,&R=1\\D,&R=0,EN=1\\Q,&R=0,EN=0.\end{cases}$$

This recurrence describes edge behavior for synchronous reset. For asynchronous reset, add the between-edge reset action to the waveform model; an edge-only table is not the whole behavior.

### Timing Boundary · 时序边界

Reset assertion and release have different concerns. An asynchronous assertion can establish a state without the clock, but release near a clock edge may violate recovery/removal constraints. A synchronously released reset is often used to make restart consistent; this is an implementation practice, not a proof that every reset circuit is safe.

EN 与同步控制也是待采样的数据路径，需要满足 setup/hold。若同时要求 LOAD、EN、CLR，按 function table 的 priority 写分段式，再作波形；不能自行选择顺序。

### Reset timing · 复位输入与释放窗口

同步复位 (synchronous reset) 与 EN 一样，通过有效捕获边沿发挥作用，其路径检查是 setup/hold。异步复位 (asynchronous reset) 断言 (assertion) 可独立于 clock 清零，但解除断言 (deassertion) 必须避开器件规定的释放窗口：恢复时间 (recovery time) 是有效时钟边沿前所需的释放提前量；移除时间 (removal time) 是有效时钟边沿后所需的继续保持量，类比 setup/hold，却检查异步控制端。

这些是具体器件的时序要求，不是从“异步”一词推出的零延迟保证；还须满足最小复位脉宽。异步断言、同步释放 (asynchronous assertion, synchronous deassertion) 的结构须按每个目标时钟域实现并验证，保证各位一致退出复位。

> [!example]- Register Enable and Reset · 推导与例题
>
> **Worked Examples · 例题**
>
> **Example 1.** 四位 Q 初值 1010，边沿时 EN=0,D=0011，Q 保持 1010；下次 EN=1，Q 变 0011；再下次 R=1,EN=1，reset priority 使 Q=0000。
>
> **Example 2.** 在两个正沿之间 R 从 0 到 1：异步复位输出随 reset 延迟变 0；同步复位仍保持旧值，直到下一个正沿。两种设计的 HDL sensitivity list 与 if 条件位置不同。
>
> **Example 3.** 高有效 synchronous set：$D_{effective}=S+D$，因为 S=1 时输入固定 1，S=0 时保留 D。仅在 capture edge 生效；这不等同于修改内部 FF 的 asynchronous preset pin。

### Method and Exam English · 方法与答题

1. List control polarity and synchronous/asynchronous behavior.
2. Write the priority from highest to lowest.
3. Record control values just before each edge.
4. Apply asynchronous events immediately when asserted.
5. Confirm that “hold” retains every bit, rather than loading zero.

**Question:** Does EN=0 force Q=0?

**Answer:** No. Enable LOW normally inhibits loading and retains the previous value. Reset is a separate control with its own polarity, timing, and priority.

### Connections · 概念关系与应用

[[Sequential Logic and Flip-Flops#3 · D Latch and D Flip-Flop · 电平与边沿|D Latch and D Flip-Flop]] 提供采样元件，[[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]] 在 D 路径选择 load/feedback；控制应用于 [[Shift Registers and Ring Counters#1 · Shift Registers · 位序与输入模式|Shift Registers]] 与 [[Counter Design and Digital Clocks#1 · Counters · 模数与时钟结构|Counters]]，且 EN、同步控制须满足 [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]]；[[VHDL Modeling and Verification#1 · VHDL Language and Modeling · 接口与实现|VHDL Language and Modeling]] 用分支位置表达复位语义。

## 6 · 从单元到系统

存储单元加入移位输入形成 [[Shift Registers and Ring Counters]]；组合下一态网络形成 [[Finite State Machine Design and Applications]]。可靠捕获还需 [[Sequential Timing and Clock Domain Crossing]]；讲义 p.32 的判断题及理由见 [[Exam Review and Problem Solving#Chapter 7 Review · 状态元件与判断题，p.31–32|Chapter 7 Review]]。

## Sources · 课件依据

主线课件：[ECE2050 Chapter 7: Sequential Logic Design](../ECE2050-Chap7.pdf)，Tinghuan Chen；页码指 PDF 页码。第 4–9 页为状态与双稳态，第 11–14 页为 SR latch，第 16–17 页为 D latch，第 19–22 页为 DFF、边沿脉冲和比较，第 24 页为 JK，第 26–30 页为寄存器、使能、复位与置位，第 32 页为自测。原有参考资料：[旧版 Chapter 7 讲义](../LGU_HUB_ECE2050/ECE2050-Chap7.pdf)，与本次讲义是不同文件。文中另外给出的数字例题和拓展（如 T 触发器、激励表、亚稳态）为辅助推导或延伸，不均来自本次讲义。

---
索引：[[ECE2050.1]] · [[Glossary]]
