---
tags:
  - ECE2050
  - registers
date: 2026-09-30
updated: 2026-10-08
chapter: Ch8
aliases:
  - 移位寄存器与环形计数器
  - Shift Registers and Ring Counters
  - 移位寄存器与环形计数器 · Ch8
  - Shift Registers
  - 移位寄存器
  - SISO SIPO PISO PIPO
  - Ring and Johnson Counters
  - 环形与约翰逊计数器
  - Shift register counters
---

# Shift Registers and Ring Counters · 移位寄存器与环形计数器

> [!SUMMARY] Quick recall · 英文速览
> A shift register moves old-state bits simultaneously. Ring and Johnson counters choose the feedback path to create cyclic patterns.

## 1 · Shift Registers · 位序与输入模式

移位寄存器 (shift register) 可串／并输入与输出；方向必须用显式位方程表示。以 $Q_3Q_2Q_1Q_0$ 为显示顺序，向右移为 $Q^+=(s_R,Q_3,Q_2,Q_1)$，向左移为 $(Q_2,Q_1,Q_0,s_L)$；并行装载与保持另由模式指定。

> [!example]- Shift Registers · 推导与例题
> **Derivation · Universal register**
>
> 本篇 mode=$S_1S_0$：00 hold、01 right、10 left、11 parallel load。每个 D 输入前的 MUX 选择旧自身、相邻旧位、另侧旧位或并行输入。reset 若有则明确优先级。
>
> All flip-flops share the clock. Their outputs change together logically, after physical clock-to-Q delays. Updating the stages one at a time with new values would incorrectly propagate a bit through the whole register in one edge.
>
> **Worked Example 1 · 左右混合**
>
> 初态 Q=1011，SR=0，SL=1：
>
> | Edge | Mode | New $Q_3Q_2Q_1Q_0$ |
> |---|---|---|
> | 0 | Initial | 1011 |
> | 1 | Right | 0101 |
> | 2 | Right | 0010 |
> | 3 | Left | 0101 |
> | 4 | Hold | 0101 |
> | 5 | Load 1100 | 1100 |
>
> 检查 right step：1011 无符号是 11，右移补 0 得 floor(11/2)=5。left shift 有限位宽会丢掉 MSB，不能总当作精确乘 2。
>
> **Applications and Review · 应用与复习**
>
> PISO load 1011，若每次先观察 Q0 再 right shift，则发送 1,1,0,1（LSB first）。若输出取 Q3 并 left shift，则可以 MSB first；两种都能工作，但协议必须一致。
>
> For a serial link, wire count is reduced at the cost of several bit intervals per word. A UART adds framing and sampling rules; a bare shift register alone is not a complete UART.
>
> **Exam answer:** “I define the stored word as Q3Q2Q1Q0. At each active edge I compute all four new bits from the pre-edge state and the sampled direction input, then update the entire word.”

## 2 · 串行输入与时延

N 位链中每个边沿使用全部旧 Q，串入一位后数据经过 N 次移位才从末级串出。题目里“延迟 N 个周期”与从第一级 Q 到末级 Q 的边沿差 N−1 要按观测点区分。

> [!example]- Shift Registers · 推导与例题
> **Worked Example 2 · 串入和时延**
>
> 初值 0000，right shift serial input 按时间为 1,0,1,1，状态为 1000、0100、1010、1101。最早输入的 bit 最终到 Q0，所以按 Q3…Q0 阅读得到输入时间顺序的反向。
>
> An n-stage pipeline whose recurrence is $Q_0[k+1]=X[k]$, $Q_i[k+1]=Q_{i-1}[k]$ gives $Q_{n-1}[k+n]=X[k]$. From the first capture edge to the last-stage capture edge there are n−1 edge intervals. Calling its discrete input-to-output delay n cycles uses the stated pre-edge input indexing; define the timing reference to avoid an off-by-one claim.
>
> ![[serial-shift-trace.svg]]
> *Figure · 以Q3Q2Q1Q0读状态，串入1、0、1、1；每个正沿都用旧状态生成四位新状态。图中的shifted out是该边沿前的旧Q0。*
>
> **Serial interfaces and matrix scanning · 串行接口与矩阵扫描**
>
> SIPO converts a defined serial bit sequence into a parallel word; PISO does the reverse. A complete UART additionally defines framing, bit timing, sampling, and any parity/stop fields. A shift register is one building block, not a complete asynchronous communication protocol.
>
> 串入顺序决定字节位序；例如从Q3串入四位1011，最终为1101，不能自动当成1011。按目标bit order安排输入，或在输出解释中明确重排。课程的 [[Keyboard Scanning and Encoding]] 用环形寄存器移动one-cold行选择，再由编码器与key-code register保存位置。

## 3 · Ring and Johnson Counters · 同样的移位，不同的反馈

环形计数器 (ring counter) 将末级原值反馈，合法独热序列有 N 态；必须初始化为独热，全零会锁死。Johnson 计数器将末级取补反馈，合法循环通常为 2N 态，需要检查未用状态的恢复。

四位 Johnson 从 0000 出发，在规定方向下依次扩展 1 再扩展 0，周期八态；序列顺序由反馈端和显示位序决定，不能只背一个字符串。

> [!IMPORTANT] 三项不变量
> 所有位同步读旧状态；方向显式定义；循环长度在合法初始化条件下计算。one-hot／one-cold 码可驱动扫描，但不等于普通二进制计数。

> [!example]- Ring and Johnson Counters · 推导与例题
> **Ring Derivation · 环形序列**
>
> one-hot seed 1000 旋转：1000→0100→0010→0001→1000，n=4 得 modulus 4。一周期内每个输出 HIGH 一拍，因此输出重复频率 $f_{clk}/4$、占空比 25%。
>
> All-zero ring state stays all zero. A ring with two initial ones does not become one-hot by itself. Modulus n refers to the intended seeded cycle, not every possible state of the hardware.
>
> one-cold seed 1110 也可扫描低有效按键线路：1110→0111→1011→1101→1110。这是有效极性改变，仍只有一个扫描位置 active。
>
> **Johnson Derivation · 扭环序列**
>
> 从 0000 开始：
>
> | Step | State |
> |---|---|
> | 0 | 0000 |
> | 1 | 1000 |
> | 2 | 1100 |
> | 3 | 1110 |
> | 4 | 1111 |
> | 5 | 0111 |
> | 6 | 0011 |
> | 7 | 0001 |
> | 8 | 0000 |
>
> 先连续填入 n 个 1，再连续填入 n 个 0，共 2n 个状态。它不是 n-bit binary counter 的 $2^n$ 个状态；n=4 时是 8 而不是 16。
>
> **Worked Examples · 例题**
>
> **Frequency.** 5-stage Johnson，input clock=1 MHz，完整序列重复=100 kHz；各 Q 位在合法周期中 HIGH 5 拍、LOW 5 拍，50% duty。one-hot 5-stage ring 的各位 duty=20%。
>
> **Illegal cycle.** 四位 Johnson 从 0101 出发，按上述 recurrence 得到 0101→0010→1001→0100→1010→1101→0110→1011→0101，共 8 态，且与预期的 0000 cycle 分离。不要因为“Johnson modulus 8”就认为所有状态都落入 intended 0000 cycle。reset 可建立预期起点。
>
> **Keyboard scan.** n=8、scan edge rate=5 kHz，完整扫描周期 $8/5000=1.6$ ms。同一个 row 每 1.6 ms 被访问一次。整个扫描频率是 625 Hz，不是每行都 5 kHz。
>
> **One-cold scan application · 独冷扫描应用**
>
> An eight-stage ring initialized to `11111110` moves one zero around an active-low row interface. Its selected-row identity is valid only while the one-cold invariant holds. The same feedback wiring initialized to all ones cannot create a zero by itself.
>
> 扫描逻辑与采样控制见 [[Keyboard Scanning and Encoding]]。行选择、编码与捕获之间必须有稳定窗口，不能仅凭环形序列正确就宣布键盘接口完整。

## Sources · 课件依据

主线课件：[Ch8 lecture](../LGU_HUB_ECE2050/ECE2050-Chap8.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
