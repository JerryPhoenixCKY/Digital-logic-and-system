---
tags:
  - ECE2050
  - sequential-logic
date: 2026-09-30
updated: 2026-10-08
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

## 2 · Set-Reset Latch · 反馈产生记忆

NOR 型 SR 锁存器的 S、R 高有效：00 保持、10 置 1、01 清 0、11 禁止。NAND 型低有效 $\bar S,\bar R$：11 保持、01 置 1、10 清 0、00 禁止。禁态及其同时释放无法用普通稳态表保证结果。

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
> **NAND Variant · NAND 型**
>
> 交叉 NAND 的输入为低有效 $\bar S,\bar R$：11 保持，01 置位，10 复位，00 禁态且两个输出都 HIGH。记忆规则“都不有效时保持，两个都有效时禁态”比死记 00/11 更稳。
>
> | NOR active-high | NAND active-low | Meaning |
> |---|---|---|
> | S=0,R=0 | $\bar S=1,\bar R=1$ | Hold |
> | S=1,R=0 | $\bar S=0,\bar R=1$ | Set |
> | S=0,R=1 | $\bar S=1,\bar R=0$ | Reset |
> | S=1,R=1 | $\bar S=0,\bar R=0$ | Invalid |
>
> **Worked Example · 事件序列**
>
> NOR 型初值 Q=0，依次 (S,R)=10、00、01、00，状态依次 1、1、0、0。NAND 型等价输入依次 01、11、10、11，得到相同状态序列。
>
> If a waveform enters the invalid input condition, mark it explicitly. Do not continue the trace by choosing a convenient remembered value unless the question gives a release priority or delay assumption.

## 3 · D Latch and D Flip-Flop · 电平与边沿

D 锁存器在有效使能电平透明，其余时间保持；D 触发器只在规定有效边沿捕获 D。$Q^+=D$ 仅描述捕获事件，边沿之间保持旧 Q；异步控制另按规定优先处理。

> [!example]- D Latch and D Flip-Flop · 推导与例题
> **Derivation · 消除 SR 禁态**
>
> 由 [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]] 的高有效 SR 型，取 $S=ED,R=E\bar D$。E=0 时 S=R=0 保持；E=1 时只有一个控制有效，因此不会产生 S=R=1。
>
> Two D latches controlled on opposite clock levels form an idealized master-slave DFF. At CLK=0, the master tracks D while the slave holds. When CLK rises, the master closes and the slave opens, transferring the captured master value to Q. Practical implementation must avoid uncontrolled overlap of transparency windows.
>
> **Comparison · 对比**
>
> | Feature | D latch | Positive-edge DFF |
> |---|---|---|
> | Sensitive event | Entire enabled level | LOW→HIGH edge |
> | Q can follow D mid-HIGH | Yes | No |
> | Storage while inactive | Holds | Holds between edges |
> | Basic HDL pattern | Incomplete level conditional | `rising_edge(clk)` |
>
> **Worked Examples · 波形例题**
>
> **Example 1.** CLK 0→1 时 D=0；CLK 保持 1 时 D 变 1；CLK 1→0 时 D 仍 1。D latch：先 0，再跟随为 1，下降后保持 1。正沿 DFF：正沿采 0，中途保持 0；要等下一个正沿才可能采 1。
>
> **Example 2.** 有效正沿前 D 依次为 1,0,1,1，DFF 初值 0；边沿后 Q 为 1,0,1,1。每次值只在 clock-to-Q 延迟后出现在物理输出，不是刚改变 D 就输出。
>
> **Example 3.** DFF 的 D 接 NOT Q。每个正沿 $Q^+=\bar Q$，输出每两次 clock 才完成一个周期，所以 $f_Q=f_{clk}/2$。该连接实现无使能的 toggle function。

## 4 · JK and T Flip-Flops · 条件更新

JK 的 00 保持、01 清零、10 置位、11 翻转，$Q^+=J\bar Q+\bar KQ$。T 触发器 $Q^+=T\oplus Q$。特性表 (characteristic table) 从输入求下一态；激励表 (excitation table) 从所需 Q→Q+ 求输入，方向不同。

> [!example]- JK and T Flip-Flops · 推导与例题
> **Excitation Table · 激励表**
>
> | Q | $Q^+$ | J | K | T | D |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | X | 0 | 0 |
> | 0 | 1 | 1 | X | 1 | 1 |
> | 1 | 0 | X | 1 | 1 | 0 |
> | 1 | 1 | X | 0 | 0 | 1 |
>
> X means either binary value achieves the required transition. These excitation don't-cares are justified by the current Q value. They differ from declaring an unused state globally irrelevant.
>
> **Conversion · 元件转换**
>
> - JK using DFF: connect $D=J\bar Q+\bar KQ$.
> - DFF using JK: $J=D,K=\bar D$.
> - TFF using JK: $J=K=T$.
> - 无使能 toggle 用 DFF：$D=\bar Q$。
>
> 使用 2:1 MUX 也能实现 JK 的 D 式：select Q，D0=J，D1=NOT K。Q=0 选 J；Q=1 选 NOT K。这里 MUX 的 select 是**当前输出 Q**，不是 clock。
>
> **Worked Examples · 例题**
>
> **Trace.** Q 初值 0，连续有效边沿的 JK 输入为 10、11、00、01，Q 变为 1、0、0、0。最后 reset 没有产生边沿以外的动作，因为这是同步 JK 输入。
>
> **Design one bit.** 状态要求 0→1、1→0，激励表给 0 时 J=1，1 时 K=1；选择 J=K=1 可满足两种转换。输出以输入 clock 一半频率翻转。
>
> **Race-around boundary.** Level-sensitive JK feedback with J=K=1 can toggle repeatedly during a long enabled pulse. An edge-triggered or suitable master-slave implementation limits updating to the intended event. Do not apply the edge table blindly to a transparent feedback latch.

## 5 · Register Enable and Reset · 控制优先级

使能 E 的 D 寄存器：$Q^+=ED+\bar EQ$。同步复位只在有效边沿执行；异步复位可在边沿之间改变 Q，释放仍要满足器件恢复／移除等时序条件。复位、置位、装载、保持同时有效时，必须由规范规定优先级。

> [!IMPORTANT] 波形题先列事件表
> 明确有效边沿、透明电平、初态、控制极性和优先级；使用边沿前的值计算所有 Q+，再一起更新。上电初态不能默认是 0。

> [!example]- Register Enable and Reset · 推导与例题
> **Reset and Set · 复位与置位**
>
> 高有效 synchronous reset R：只在有效边沿执行，$Q^+=0$ if R=1，否则正常 load/hold。高有效 asynchronous reset：R=1 时不用等 clock 就把 Q 强制为 0。set/preset 对称地强制为 1。
>
> If reset has priority over enable, the next-state rule is:
>
> $$Q^+=\begin{cases}0,&R=1\\D,&R=0,EN=1\\Q,&R=0,EN=0.\end{cases}$$
>
> This recurrence describes edge behavior for synchronous reset. For asynchronous reset, add the between-edge reset action to the waveform model; an edge-only table is not the whole behavior.
>
> **Worked Examples · 例题**
>
> **Example 1.** 四位 Q 初值 1010，边沿时 EN=0,D=0011，Q 保持 1010；下次 EN=1，Q 变 0011；再下次 R=1,EN=1，reset priority 使 Q=0000。
>
> **Example 2.** 在两个正沿之间 R 从 0 到 1：异步复位输出随 reset 延迟变 0；同步复位仍保持旧值，直到下一个正沿。两种设计的 HDL sensitivity list 与 if 条件位置不同。
>
> **Example 3.** 高有效 synchronous set：$D_{effective}=S+D$，因为 S=1 时输入固定 1，S=0 时保留 D。仅在 capture edge 生效；这不等同于修改内部 FF 的 asynchronous preset pin。

## 6 · 从单元到系统

存储单元加入移位输入形成 [[Shift Registers and Ring Counters]]；组合下一态网络形成 [[Finite State Machine Design and Applications]]。可靠捕获还需 [[Sequential Timing and Clock Domain Crossing]]。

> [!example]- Register Enable and Reset · 推导与例题
> **Timing Boundary · 时序边界**
>
> Reset assertion and release have different concerns. An asynchronous assertion can establish a state without the clock, but release near a clock edge may violate recovery/removal constraints. A synchronously released reset is often used to make restart consistent; this is an implementation practice, not a proof that every reset circuit is safe.
>
> EN 与同步控制也是待采样的数据路径，需要满足 setup/hold。若同时要求 LOAD、EN、CLR，按 function table 的 priority 写分段式，再作波形；不能自行选择顺序。

## Sources · 课件依据

主线课件：[Ch7 lecture](../LGU_HUB_ECE2050/ECE2050-Chap7.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
