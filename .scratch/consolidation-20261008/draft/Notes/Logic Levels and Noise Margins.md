---
tags:
  - ECE2050
  - logic-levels
date: 2026-09-16
updated: 2026-10-08
chapter: Ch3
aliases:
  - 逻辑电平与噪声容限
  - Logic Levels and Noise Margins
  - 逻辑电平与噪声容限 · Ch3
  - Logic Levels
  - 逻辑电平
  - 逻辑电平与电压范围
  - Logic Level
  - DC Transfer Characteristic
  - 直流传输特性
  - 电压传输特性
  - VTC
  - Noise Margin
  - 噪声容限
  - 噪声裕度
  - Noise Margins
---

# Logic Levels and Noise Margins · 逻辑电平与噪声容限

> [!SUMMARY] Quick recall · 英文速览
> Output guarantees and input acceptance limits define compatibility. Noise margin is the difference between those limits, not the nominal supply voltage.

## 1 · Logic Levels · 保证值与接受范围

逻辑电平 (logic levels) 把模拟电压分为有效 LOW、有效 HIGH 与不确定区。输入阈值为 $V_{IL(max)},V_{IH(min)}$；输出保证为 $V_{OL(max)},V_{OH(min)}$，单位均为 V。

高输出必须达到接收端 HIGH 的下限，低输出必须不超过 LOW 的上限。符号中的输入／输出、最大／最小不能互换；不确定区不代表器件自动选择最近的逻辑值。

> [!example]- Logic Levels · 推导与例题
> **图示与讲义依据**
>
> ![[logic-level-ranges.svg]]
> *图 1 — (a) 一条竖直电压轴上的四个参数与中间的过渡带（斜率填充区）：$V_{OH}$ 之上是驱动器保证的 1，
> $V_{OL}$ 之下是保证的 0，$V_{IL}$ 与 $V_{IH}$ 之间是接收器无法判定的过渡带；TTL 5 V 的具体数字标在右侧。
> (b) 用讲义 p.23 的实测值画出两个真实家族：TTL(5 V) 与 LVCMOS(3.3 V) 的四个数与各自的过渡带宽度
> （TTL 1.2 V = $V_{DD}$ 的 24%，LVCMOS 0.9 V = 27%）。*
>
> **Derivation · 推导过程**
>
> **1. 为什么单点不行，必须用区间**
>
> 真实门的电压传输特性是**连续曲线**（见 [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力|DC Transfer Characteristic]]），增益有限，曲线在 $V_{DD}/2$
> 附近有一段过渡区。把这条曲线"翻译"成数字接口，就得到两个输入门槛：曲线左端平台对应 $V_{IL}$ 以下
> （一定读成 0），右端平台对应 $V_{IH}$ 以上（一定读成 1）。输出侧同理给出 $V_{OL}$ 与 $V_{OH}$。
> 于是"逻辑值"在电压轴上变成三段：**0 区间 / 过渡带 / 1 区间**（图 1a）。
>
> - 意义：接口规范只需要四个数就能描述一条曲线，因为曲线两端是平的、中间是陡的。
> - 数值校验（用讲义 p.23 的 TTL 行）：0 区间 $[0,\,0.4]$ V、过渡带 $[0.8,\,2.0]$ V、
>   1 区间 $[2.4,\,5]$ V；三段之外还剩下 $[0.4,0.8]$ 与 $[2.0,2.4]$ 两条缝，那正是两个噪声容限。
>
> **2. 两个范围之间的缝隙 = 噪声预算**
>
> 接收端的要求（$V_{IH}$）比发送端的保证（$V_{OH}$）**低**，差额
>
> $$
> NM_H = V_{OH}-V_{IH}, \qquad NM_L = V_{IL}-V_{OL}
> $$
>
> 就是信号在传输途中允许"退化"的额度。数值校验（讲义 p.23 的 TTL 行）：
> $NM_H = 2.4-2.0 = 0.4$ V、$NM_L = 0.8-0.4 = 0.4$ V，都是正数 —— 这就是不等式
> $V_{OL}<V_{IL}<V_{IH}<V_{OH}$ 的工程含义。完整推导见 [[Logic Levels and Noise Margins#3 · Noise Margin · 接口的预算|Noise Margin]]。
>
> **3. $V_{DD}$ 缩放：从 5 V 到 1.0 V（讲义 p.21–p.22）**
>
> 七十、八十年代 $V_{DD}=5$ V，此后一路降到 3.3 / 2.5 / 1.8 / 1.5 / 1.2 / 1.0 V，讲义给的两个理由：
>
> - **避免烧毁微小的晶体管 (avoid frying tiny transistors)**：特征尺寸缩小后栅氧更薄，
>   5 V 的电场会把栅氧击穿、并加速热载流子退化，可靠性不允许。
> - **省功耗 (save power)**：CMOS 动态功耗 $P = C\,V_{DD}^{2}f$，与 $V_{DD}$ **平方**成正比。
>
> 数值校验（代入具体数字）：
>
> - $5\ \text{V}\to1.0\ \text{V}$：电压降到 $1.0/5 = 0.2$，功耗降到 $0.2^{2} = 0.04$，
>   即同样电路**省 96%、约 25 倍**。
> - $5\ \text{V}\to3.3\ \text{V}$：$(3.3/5)^{2} = 0.4356$，省 $1-0.4356 = 56.4\%$。
> - $5\ \text{V}\to1.8\ \text{V}$：$(1.8/5)^{2} = 0.1296$，省 $87.0\%$。
>
> 代价是**噪声容限的绝对值一起变小**：3.3 V 的 LVCMOS 只有 $NM_H=0.9$ V、$NM_L=0.54$ V，而 5 V 的
> TTL 已经"只有" 0.4 V。讲义 p.21 因此特别提醒：*Be careful connecting chips with different supply
> voltages* —— 不同供电的芯片互连必须先查表（例 2）。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.15 的两个提问：4.99 V 与 3.2 V 是什么？**
>
> 题目：一个 5 V 系统里，接收到的电压是 4.99 V 或 3.2 V，它们分别是 1 还是 0？再问：同样两个电压送到
> 3.3 V 的 LVCMOS 输入端呢？
>
> 解：
>
> 1. 5 V TTL 输入：$V_{IH}=2.0$ V。$4.99 \ge 2.0$ → **1**；$3.2 \ge 2.0$ → **1**。
> 2. 5 V CMOS 输入：$V_{IH}=3.15$ V。$4.99 \ge 3.15$ → **1**；$3.2 \ge 3.15$ → 勉强 **1**。
> 3. LVCMOS 3.3 V 输入：$V_{IH}=1.8$ V，两者都 $\ge 1.8$ → 都是 **1**（该器件 $V_{DD}=3.3$ V，
>    4.99 V 已超电源，实际会打到输入保护二极管，这里只做门限判断）。
>
> **数值校验 (Numerical check)**：把三个 $V_{IH}$ 与两个电压逐一代入 ——
> $4.99-2.0 = 2.99$ V ✓、$4.99-3.15 = 1.84$ V ✓、$4.99-1.8 = 3.19$ V ✓；
> $3.2-2.0 = 1.20$ V ✓、$3.2-3.15 = 0.05$ V（只有 50 mV！）、$3.2-1.8 = 1.40$ V ✓。
> 结论：**同一个 3.2 V 对 TTL 有 1.20 V 余量，对 5 V CMOS 只剩 0.05 V** —— 逻辑值取决于接收端的表，
> 不取决于电压本身。
>
> **Example 2 — 讲义 p.23 的互连检查：3.3 V 器件能驱动 5 V 器件吗？**
>
> 题目：LVCMOS（3.3 V，$V_{OH}=2.7$、$V_{OL}=0.36$）分别驱动 (i) 5 V TTL 输入、(ii) 5 V CMOS 输入、
> (iii) 另一个 LVCMOS 输入。判断是否兼容并给出余量。
>
> 解：
>
> 1. (i) 5 V TTL：需要 $V_{IH}=2.0$、$V_{IL}=0.8$。高电平 $2.7\ge2.0$ ✓、低电平 $0.36\le0.8$ ✓ → **兼容**。
> 2. (ii) 5 V CMOS：需要 $V_{IH}=3.15$。高电平 $2.7\ge3.15$ ✗ → **不兼容**（差 0.45 V）：
>    驱动器连"最低的高电平"都到不了对方的门限，必须加电平转换。
> 3. (iii) LVCMOS 输入：需要 $V_{IH}=1.8$、$V_{IL}=0.9$。$2.7\ge1.8$ ✓、$0.36\le0.9$ ✓ → **兼容**。
>
> **数值校验 (Numerical check)**：(i) $NM_H = 2.7-2.0 = 0.7$ V、$NM_L = 0.8-0.36 = 0.44$ V，均为正 ✓；
> (ii) $2.7-3.15 = -0.45$ V < 0 ✗；(iii) $NM_H = 2.7-1.8 = 0.9$ V、$NM_L = 0.9-0.36 = 0.54$ V，
> 正好复现讲义 p.23 表里 LVCMOS 行的两个噪声容限 ✓。
>
> **Example 3 — $V_{DD}$ 缩放的收益与代价（讲义 p.21–p.22）**
>
> 题目：把 5 V 系统换成 1.0 V 系统，动态功耗变化多少？若阈值按 $V_{DD}$ 比例缩放，3.3 V 的 LVCMOS
> 搬到 1.8 V 后噪声容限还剩多少？
>
> 解：
>
> 1. 功耗：$P\propto V_{DD}^{2}$，$(1.0/5)^{2} = 0.04$ → 省 96%（约 25 倍）。
> 2. 比例缩放因子 $k = 1.8/3.3 = 0.5455$。
> 3. 阈值缩放：$V_{IL} = 0.9k = 0.491$、$V_{IH} = 1.8k = 0.982$、$V_{OL} = 0.36k = 0.196$、
>    $V_{OH} = 2.7k = 1.473$（V）。
>
> **数值校验 (Numerical check)**：$NM_H = 1.473-0.982 = 0.491$ V，与 $0.9\times0.5455 = 0.491$ V 一致 ✓；
> $NM_L = 0.491-0.196 = 0.295$ V，与 $0.54\times0.5455 = 0.295$ V 一致 ✓。
> 即**噪声预算从 0.9 V 缩到约 0.49 V**（低压版本的 $NM$ 不是数据手册数字，此处只演示"按比例缩放"这一
> 假设；$\text{LVCMOS}$ 的真实门槛由 JEDEC 按 $V_{DD}$ 的百分比另行规定）。
>
> **Electrical validity and logical assertion · 电气有效与逻辑有效**
>
> A logic threshold belongs to a receiving interface, while a guaranteed output level belongs to a driving interface. Connecting two devices requires comparing those guarantees. Equal supply voltages are neither a proof of compatibility nor a necessary condition for compatibility; the relevant output and input limits must match under the stated operating conditions.
>
> The undefined input band does not mean that a gate has a stable third Boolean state. It means the Boolean interpretation is not guaranteed there. A simulator's X is a model of uncertainty, and a tri-state Z describes a disconnected output driver. Neither is a new arithmetic digit between zero and one.
>
> **Worked application — level compatibility.** 假设 driver 保证 $V_{OH(min)}=2.9$ V、$V_{OL(max)}=0.3$ V，receiver 要求 $V_{IH(min)}=2.0$ V、$V_{IL(max)}=0.8$ V。HIGH 余量 0.9 V、LOW 余量 0.5 V，静态兼容。若另一 receiver 的 $V_{IH(min)}=3.5$ V，则 HIGH 余量 −0.6 V，不能保证高电平被识别；不能只写“都是数字器件所以能接”。
>
> In English: these are assumed interface limits for this example, not specifications for an unnamed logic family. The compatibility check concerns static voltage levels; timing, output-current capability, and permissible input voltage remain separate requirements.
>
> **English exam question:** Does a 1.5 V input always represent logic 0?
>
> **Answer:** No. Its interpretation depends on the receiver's specified thresholds. It could be a valid LOW, a valid HIGH, or lie in the undefined band. A voltage without interface limits is insufficient to assign a guaranteed Boolean value.
>
> Connect [[Logic Levels and Noise Margins#3 · Noise Margin · 接口的预算|Noise Margin]], [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力|DC Transfer Characteristic]], [[Tri-State Buffers and Bus Drivers]], and [[Digital Logic Troubleshooting]] to keep static validity, disconnection, and fault observations distinct.

## 2 · DC Transfer Characteristic · 由传输曲线理解恢复能力

直流传输特性 (DC transfer characteristic) 是稳态 $V_{out}(V_{in})$，输入／输出轴都为 V。缓冲器与反相器方向相反；过渡区的斜率、切换点和逻辑阈值用途不同。

局部斜率 −1、切换点 $V_{out}=V_{in}$ 等是特定静态模型的定义条件；不能把某曲线读出的典型点替代数据手册保证范围，也不能由 DC 曲线推出传播延迟。

> [!example]- DC Transfer Characteristic · 推导与例题
> **Derivation · 推导过程**
>
> **1. 理想缓冲器：阶跃，两段余量正好铺满 $V_{DD}$**
>
> 讲义 p.19 的理想缓冲器就是把过渡区压缩成一个点：
>
> $$
> V_{out}=0\ (V_{in}<V_{DD}/2),\qquad V_{out}=V_{DD}\ (V_{in}>V_{DD}/2)
> \ \Longrightarrow\
> V_{OL}=0,\quad V_{OH}=V_{DD},\quad V_{IL}=V_{IH}=V_M=\frac{V_{DD}}{2}
> $$
>
> 代入两个噪声容限的定义：
>
> $$
> NM_H = V_{OH}-V_{IH} = V_{DD}-\frac{V_{DD}}{2} = \frac{V_{DD}}{2},\qquad
> NM_L = V_{IL}-V_{OL} = \frac{V_{DD}}{2}-0 = \frac{V_{DD}}{2}
> \ \Longrightarrow\
> NM_H = NM_L = \frac{V_{DD}}{2},\quad NM_H+NM_L = V_{DD}
> $$
>
> - 意义：理想缓冲器把整个供电电压**平分成两份**噪声预算（讲义 p.19 的第一行标注）。
> - 数值校验：$V_{DD}=5$ V → $NM_H = NM_L = 2.5$ V，$2.5+2.5 = 5.0 = V_{DD}$ ✓；
>   $V_{DD}=3.3$ V → $NM_H = NM_L = 1.65$ V，$1.65+1.65 = 3.3 = V_{DD}$ ✓。
>
> **2. 实际缓冲器：过渡区吃掉一块预算**
>
> 真实门的过渡区有宽度 $W=V_{IH}-V_{IL}>0$（讲义 p.19 的 real buffer：*NM_H, NM_L < V_DD/2*）。
> 把两个容限相加：
>
> $$
> NM_H+NM_L = (V_{OH}-V_{IH})+(V_{IL}-V_{OL}) = \underbrace{(V_{OH}-V_{OL})}_{\text{输出摆幅}} - \underbrace{(V_{IH}-V_{IL})}_{W}
> $$
>
> - 意义：$V_{DD}$ 这块预算被三样东西分掉 —— **输出摆幅的损失**（$V_{OH}$ 掉下 $V_{DD}$、$V_{OL}$ 抬离 0）、
>   **过渡带** $W$、**两个噪声余量**。曲线的陡坡越宽，留给噪声的就越少。
> - 数值校验：$V_{DD}=5$ V、轨到轨（$V_{OH}=5$、$V_{OL}=0$）、$V_{IL}=2.0$、$V_{IH}=3.0$（$W=1.0$）→
>   $NM_H = 5-3.0 = 2.0$ V、$NM_L = 2.0-0 = 2.0$ V，和 $=4.0$ V，而 $V_{DD}-W = 5-1 = 4.0$ V ✓；
>   每个 $2.0$ V 都 $< V_{DD}/2 = 2.5$ V ✓，与讲义 p.19 的结论一致。
> - 若输出也不轨到轨（$V_{OH}=4.8$、$V_{OL}=0.2$）：$(4.8-0.2)-1.0 = 3.6$ V，再扣掉 $0.4$ V 摆幅损失 ✓。
>
> ![[dc-transfer-buffer.svg]]
> *图 1 — (a) 理想缓冲器：VTC 是在 $V_{in}=V_{DD}/2$ 处的一级台阶，$V_{IL}=V_{IH}=V_M=2.5$ V，
> 两个箭头就是 $NM_L = 2.5$ V 与 $NM_H = 2.5$ V，下方的预算条正好拼满 $V_{DD}=5$ V。
> (b) 实际缓冲器（$V_{IL}=2.0$、$V_{IH}=3.0$）：过渡区是一条有宽度的陡坡（虚线），
> $V_M=2.5$ V 是它与 $V_{out}=V_{in}$ 直线的交点；此时 $NM_L = NM_H = 2.0$ V，
> 预算条多出一段 $W=1.0$ V 的过渡带，于是 $NM_H+NM_L = V_{DD}-W = 4.0$ V $<V_{DD}$。*
>
> **3. 增益与过渡带宽度：为什么"陡"就是"抗噪"**
>
> 在过渡区内把曲线近似成一条直线，斜率就是增益 $\lvert A\rvert$，它要在宽度 $W$ 内走完整个摆幅
> $V_{OH}-V_{OL}\approx V_{DD}$：
>
> $$
> \lvert A\rvert \approx \frac{V_{DD}}{W}
> \qquad\Longrightarrow\qquad
> W \approx \frac{V_{DD}}{\lvert A\rvert},
> \qquad
> NM_H+NM_L \approx V_{DD}\left(1-\frac{1}{\lvert A\rvert}\right)
> $$
>
> - 意义：**增益越大 → 过渡带越窄 → 两个噪声余量之和越大**（讲义 p.20 关注的正是过渡区的陡度）。
>   这就是"数字电路要努力把反相器做陡"的原因。
> - 数值校验：$V_{DD}=3.3$ V、$\lvert A\rvert = 20$ → $W = 3.3/20 = 0.165$ V，对称时 $NM_H = NM_L = (3.3-0.165)/2 = 1.5675$ V ✓；
>   $\lvert A\rvert$ 掉到 $5$ → $W = 0.66$ V、每个余量 $1.32$ V —— 增益降低 4 倍，噪声容限就掉 $0.2475$ V（约 16%）✓。
>
> **4. 实际反相器的 VTC 与 $V_M$（讲义 p.20）**
>
> 反相器的曲线是缓冲器的"上下颠倒"版，但同样分三段：
>
> | 区间 | 输入 | 器件状态 | 输出 |
> |---|---|---|---|
> | 饱和区（左） | $V_{in}<V_{IL}$ | $n$ 管关断、$p$ 管导通 | $V_{out}=V_{OH}\approx V_{DD}$ |
> | 增益区（中） | $V_{IL}\le V_{in}\le V_{IH}$ | 两管都导通，电流急剧变化 | 从 $V_{OH}$ 陡降到 $V_{OL}$，斜率 $=\lvert A\rvert$ 最大 |
> | 饱和区（右） | $V_{in}>V_{IH}$ | $p$ 管关断、$n$ 管导通 | $V_{out}=V_{OL}\approx0$ |
>
> - $V_M$ 是曲线穿过 $V_{out}=V_{in}$ 的那一点：对称反相器 $V_M=V_{DD}/2$（讲义 p.20 标注的 switch point）。
>   $V_M$ 上移意味着"更容易被判成 1"，高电平方向的余量被吃掉。
> - 读数规则不变：$V_{IL}$、$V_{IH}$ 仍是过渡区的两个单位增益点，$V_{OL}$、$V_{OH}$ 仍是两端的平台。
>
> **5. $V_{DD}$ 缩放对 VTC 的影响**
>
> $V_{DD}$ 降低时，VTC 的**横轴、纵轴一起压缩**：曲线整体变小。若门限按 $V_{DD}$ 的固定比例定义，
> 噪声容限的**绝对值**也按同一比例缩小：
>
> - 门限比例（讲义 p.23 的表）：CMOS 5 V 是 $1.35/5 = 0.27$、$3.15/5 = 0.63$；LVCMOS 3.3 V 是 $0.9/3.3 = 0.273$、$1.8/3.3 = 0.545$。
> - 数值校验（按比例外推到 1.8 V，因子 $1.8/3.3 = 0.5455$）：$NM_H = 0.9\times0.5455 = 0.491$ V、
>   $NM_L = 0.54\times0.5455 = 0.295$ V，与逐项缩放门限的差 $1.473-0.982$、$0.491-0.196$ 一致 ✓。
> - 结论：电压越低，曲线越"矮"，留给噪声的**伏特数**越少，低压设计必须重做噪声预算。
>
> **Worked Example · 例题**
>
> **Example 1 — 理想缓冲器（讲义 p.19 第一行）**
>
> 题目：$V_{DD}=5$ V 的理想缓冲器，求 $V_{IL}$、$V_{IH}$、$V_{OL}$、$V_{OH}$、$V_M$、$NM_H$、$NM_L$ 与 $NM_H+NM_L$；若 $V_{DD}$ 改成 3.3 V 呢？
>
> 解：
>
> 1. 阶跃位置由对称性给出：$V_M = V_{IL} = V_{IH} = V_{DD}/2 = 2.5$ V。
> 2. 平台：$V_{OL} = 0$、$V_{OH} = V_{DD} = 5$ V。
> 3. 余量：$NM_H = 5-2.5 = 2.5$ V、$NM_L = 2.5-0 = 2.5$ V。
> 4. $V_{DD}=3.3$ V：$V_M = 1.65$ V、$NM_H = NM_L = 1.65$ V。
>
> **数值校验 (Numerical check)**：$NM_H+NM_L = 2.5+2.5 = 5.0 = V_{DD}$ ✓（3.3 V 时 $1.65+1.65 = 3.3$ ✓）；
> 用第 2 节的恒等式复核：$(V_{OH}-V_{OL})-W = (5-0)-0 = 5.0$ ✓（理想阶跃 $W=0$）。
>
> **Example 2 — 实际缓冲器：过渡区如何吃掉预算（讲义 p.19 第二行）**
>
> 题目：$V_{DD}=5$ V 的缓冲器，$V_{IL}=2.0$ V、$V_{IH}=3.0$ V、输出轨到轨。求 $V_M$、$W$、两个余量、
> 总和，并检验"每个余量 $<V_{DD}/2$"。若输出只能到 $V_{OH}=4.8$ V、$V_{OL}=0.2$ V 呢？
>
> 解：
>
> 1. $W = V_{IH}-V_{IL} = 3.0-2.0 = 1.0$ V；$V_M = (V_{IL}+V_{IH})/2 = 2.5$ V（曲线对称）。
> 2. $NM_H = V_{OH}-V_{IH} = 5.0-3.0 = 2.0$ V；$NM_L = V_{IL}-V_{OL} = 2.0-0 = 2.0$ V。
> 3. 总和 $= 4.0$ V；与 $V_{DD}-W = 5.0-1.0 = 4.0$ V 相同。
> 4. 输出不轨到轨时：$NM_H = 4.8-3.0 = 1.8$ V、$NM_L = 2.0-0.2 = 1.8$ V，总和 $3.6$ V
>    $= (4.8-0.2)-1.0$ ✓。
>
> **数值校验 (Numerical check)**：每个余量 $2.0 < V_{DD}/2 = 2.5$ ✓（讲义 p.19 的 *NM_H, NM_L < V_DD/2*）；
> 第 4 步再损失 $0.2+0.2 = 0.4$ V 摆幅，$4.0-3.6 = 0.4$ ✓。
> 对照讲义 p.23 的真实家族：TTL 的过渡带 $W = 2.0-0.8 = 1.2$ V，占 $V_{DD}$ 的 $1.2/5 = 24\%$；
> LVCMOS 是 $1.8-0.9 = 0.9$ V，占 $0.9/3.3 = 27.3\%$ —— 真实门的过渡带都要吃掉约四分之一电源。
>
> **Example 3 — 反相器的增益、$V_M$ 与噪声容限（讲义 p.20）**
>
> 题目：$V_{DD}=3.3$ V 的反相器，过渡区近似线性，$V_M=V_{DD}/2$。求 $\lvert A\rvert=20$ 与
> $\lvert A\rvert=5$ 两种情况下 $W$、$NM_H$、$NM_L$，并说明"陡"意味着什么。
>
> 解：
>
> 1. $\lvert A\rvert=20$：$W = V_{DD}/\lvert A\rvert = 3.3/20 = 0.165$ V；
>    $V_{IL} = 1.65-0.0825 = 1.5675$ V、$V_{IH} = 1.65+0.0825 = 1.7325$ V。
> 2. 于是 $NM_L = 1.5675-0 = 1.5675$ V、$NM_H = 3.3-1.7325 = 1.5675$ V（对称，各占 $V_{DD}$ 的 47.5%）。
> 3. $\lvert A\rvert=5$：$W = 0.66$ V，$V_{IL} = 1.32$ V、$V_{IH} = 1.98$ V → $NM_L = NM_H = 1.32$ V。
>
> **数值校验 (Numerical check)**：$1.65\pm0.0825$ 给出 $1.5675$ / $1.7325$ ✓、$3.3-1.7325 = 1.5675$ ✓
> （与 $NM_L$ 相等，正是 $V_M=V_{DD}/2$ 的对称性）；$1.5675/3.3 = 47.5\%$ ✓、$1.32/3.3 = 40\%$ ✓。
> 增益从 20 掉到 5，过渡带涨 4 倍（$0.165\to0.66$ V），每个噪声容限掉 $0.2475$ V（相对损失 $15.8\%$）
> —— **曲线越陡，抗噪越好**。
>
> **What a static curve can establish · 静态曲线能证明什么**
>
> A DC transfer characteristic relates settled output voltage to settled input voltage. It helps identify valid logic regions and voltage restoration. It does not provide propagation delay, setup time, or the transient pulse shape after a fast transition. Those quantities require a dynamic model or measurement.
>
> The switching voltage $V_M$, often defined by the intersection $V_{out}=V_{in}$ for an inverter, is not automatically equal to either guaranteed input limit. $V_{IL}$ and $V_{IH}$ bound recognized input regions; $V_M$ describes a crossing on a particular curve. Keeping these definitions separate prevents use of a nominal midpoint as a guaranteed interface threshold.
>
> **Worked application — read distinct thresholds.** 假设某反相器静态曲线给出 $V_M=1.65$ V，但接口规定 $V_{IL(max)}=0.9$ V、$V_{IH(min)}=2.0$ V。输入 1.4 V 虽低于 $V_M$，仍处于 0.9–2.0 V 的未保证区，不能据此认定有效 LOW。若 $V_{OH(min)}=3.0$ V、$V_{OL(max)}=0.2$ V，则噪声容限分别为 1.0 V 与 0.7 V。
>
> In English: the nominal crossing and the guaranteed logic regions answer different questions. A steep transition supports regeneration, but interface decisions should use the appropriate guaranteed limits rather than a visually estimated crossing.
>
> **English exam question:** Can an inverter's DC curve determine the clock frequency at which a register chain will work?
>
> **Answer:** No. The curve describes settled voltage behavior. Clock frequency requires clock-to-Q delay, combinational propagation delay, setup time, and the relevant clock timing assumptions. A valid voltage interface is necessary but does not complete the timing proof.
>
> Continue with [[Logic Levels and Noise Margins#3 · Noise Margin · 接口的预算|Noise Margin]], [[Propagation Delay and Logic Hazards]], and [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]]. These form a progression from static voltage interpretation to transient settling to reliable sampling.

## 3 · Noise Margin · 接口的预算

$$NM_H=V_{OH(min),driver}-V_{IH(min),receiver},$$
$$NM_L=V_{IL(max),receiver}-V_{OL(max),driver}.$$

高电平向下受扰，低电平向上受扰，所以两种余量分开计算。最小余量决定较弱的一侧；正余量只是必要条件，还需核对输入额定范围、驱动电流、负载和时序。

**例。** 驱动保证 HIGH≥2.4 V、LOW≤0.4 V，接收 HIGH≥2.0 V、LOW≤0.8 V，则两侧容限均 0.4 V；不能用电源电压代替这些保证值。

> [!example]- Noise Margin · 推导与例题
> **图示与讲义依据**
>
> ![[noise-margin.svg]]
> *图 1 — 四条保证线画在同一根竖直电压轴上：驱动器的 $V_{OH}/V_{OL}$（实线）与接收器的 $V_{IH}/V_{IL}$
> （虚线）。绿色阴影带 + 双向箭头就是两个噪声容限。(a) TTL 5 V：$NM_H = NM_L = 0.4$ V，
> 两个带子一样宽；(b) LVCMOS 3.3 V：$NM_H = 0.9$ V 明显大于 $NM_L = 0.54$ V，说明"能容忍多少噪声"
> 两个方向并不对称。中间的斜线区是过渡带，不对应任何逻辑值。*
>
> **Derivation · 推导过程**
>
> **1. 从讲义 p.17 的例子看"退化"与"读错"的距离**
>
> 讲义给的例子：驱动器输出 $5$ V，长线电阻后接收端只有 $4.5$ V。先把两件事分开：
>
> - **能不能读对**：接收端看到 $4.5$ V，只要 $4.5 \ge V_{IH}$ 就仍被读成 1。
>   对讲义 p.23 的三个家族都成立：$4.5\ge2.0$（TTL）✓、$4.5\ge3.15$（CMOS 5 V）✓、
>   $4.5\ge1.8$（LVCMOS）✓ —— 这个例子里的信号**没有**被读错。
> - **还有多少余量**：设计余量不能用"典型 5 V"算，必须用 $V_{OH}(\min)$。
>   TTL 的 $V_{OH}(\min)=2.4$ V，所以允许的下降量只有 $2.4-2.0 = 0.4$ V：
>
> $$
> \underbrace{5.0}_{\text{典型输出}} - \underbrace{4.5}_{\text{接收端}} = 0.5\ \text{V}
> \;>\; \underbrace{0.4\ \text{V}}_{NM_H(\text{TTL})}
> \quad\Longrightarrow\quad \text{若输出恰好落在 }V_{OH}(\min)\text{，这个压降就会读错}
> $$
>
> - 意义：同一个 0.5 V 压降，用典型值看很安全（$5\to4.5$ 只掉 10%），
>   用最坏情况看已经超出 TTL 的 $NM_H$。**噪声容限是保证，不是测量值。**
> - 数值校验：$4.5-2.0 = 2.5$ V（用实测值算的"余量"）、$2.4-2.0 = 0.4$ V（手册保证的余量）、
>   $0.5 > 0.4$ ✓ —— 三个数放一起就能看出为什么必须用第二个。
>
> **2. 为什么 $NM_H$ 与 $NM_L$ 要分开看**
>
> 逻辑 1 与逻辑 0 的**破坏机制不同**：1 被拉低（对地漏电、负载电流在电阻上的压降、耦合到相邻的低电平线），
> 0 被抬高（耦合到相邻的高电平线、地弹、衬底噪声）。同时，输出级的上下管强度、输入级的开关阈值
> 也都不是对称的，于是：
>
> $$
> NM_H = V_{OH}-V_{IH} \ne NM_L = V_{IL}-V_{OL}
> $$
>
> - 数值校验（讲义 p.23）：TTL $0.4/0.4$（对称）、LVTTL $0.4/0.4$（与 TTL 相同的门限，但电源只有 3.3 V）、
>   CMOS 5 V $3.84-3.15 = 0.69$ 与 $1.35-0.33 = 1.02$（**不对称**，低电平余量反而更大）、
>   LVCMOS 3.3 V $2.7-1.8 = 0.9$ 与 $0.9-0.36 = 0.54$。
>   只报一个数（例如只说"TTL 噪声容限 0.4 V"）会漏掉另一半风险。
>
> **3. 两个容限之和与 $V_{DD}$ 的关系**
>
> 把两个定义相加：
>
> $$
> NM_H+NM_L = (V_{OH}-V_{OL}) - (V_{IH}-V_{IL})
> $$
>
> - 意义：$V_{DD}$ 这块"电压预算"被三样东西分掉 —— 输出摆幅的损失、过渡带宽度、两个噪声余量。
>   接口越理想（输出轨到轨、过渡带极窄），留给噪声的比例越大；完整讨论见 [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力|DC Transfer Characteristic]]。
> - 数值校验（TTL）：$(2.4-0.4)-(2.0-0.8) = 2.0-1.2 = 0.8 = 0.4+0.4$ ✓；
>   （LVCMOS）：$(2.7-0.36)-(1.8-0.9) = 2.34-0.9 = 1.44 = 0.9+0.54$ ✓。
>
> **4. 相对余量：把 $NM$ 换算成 $V_{DD}$ 的百分比**
>
> 低压器件必须看比例，因为噪声（串扰、地弹）未必按比例缩小：
>
> | 家族 | $V_{DD}$ | $NM_H$ | $NM_L$ | $NM_H/V_{DD}$ | $NM_L/V_{DD}$ |
> |---|---|---|---|---|---|
> | TTL | 5 V | 0.4 V | 0.4 V | 8.0% | 8.0% |
> | CMOS | 5 V | 0.69 V | 1.02 V | 13.8% | 20.4% |
> | LVTTL | 3.3 V | 0.4 V | 0.4 V | 12.1% | 12.1% |
> | LVCMOS | 3.3 V | 0.9 V | 0.54 V | 27.3% | 16.4% |
>
> - 意义：LVTTL 的绝对 $NM$ 与 TTL 完全相同（都是 0.4 V），但电源从 5 V 降到 3.3 V，
>   相对余量从 8.0% 提高到 12.1% —— 这就是 $V_{DD}$ 缩放时代"门限值不完全跟着电源缩小"的结果。
> - 数值校验：$0.4/5 = 8.0\%$ ✓、$0.4/3.3 = 12.12\%$ ✓、$0.9/3.3 = 27.27\%$ ✓、$0.54/3.3 = 16.36\%$ ✓。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.17 的 5 V→4.5 V 例子：会发生什么？**
>
> 题目：一个 TTL 驱动器经长线接到 TTL 接收器，驱动器典型输出 5 V，接收端实测 4.5 V。
> (i) 逻辑值对吗？(ii) 这个网络还有多少设计余量？(iii) 如果压降再增加到 0.5 V 会怎样？
>
> 解：
>
> 1. 接收端 $4.5$ V，TTL 的 $V_{IH}=2.0$ V，$4.5 \ge 2.0$ → 仍读成 **1** ✓（不是故障）。
> 2. 设计余量取驱动器的最差输出 $V_{OH}(\min)=2.4$ V：允许的退化只有 $2.4-2.0 = 0.4$ V。
>    实测压降 $5.0-4.5 = 0.5$ V。
> 3. 若驱动器真的落在 $V_{OH}(\min)$，接收端只拿到 $2.4-0.5 = 1.9$ V $<2.0$ V → 读错。
>
> **数值校验 (Numerical check)**：$2.4-0.5 = 1.9$ V、$V_{IH}-1.9 = 0.1$ V，缺口 $0.1$ V ✓；
> 反过来核对余量 $NM_H = 0.4$ V、压降 $0.5$ V，$0.4-0.5 = -0.1$ V —— 与"缺口 0.1 V"完全一致 ✓。
> TTL 的 $NM_L$ 同样是 $0.8-0.4 = 0.4$ V，所以低电平方向也一样不宽裕。
>
> **Example 2 — 讲义 p.23 四个家族的噪声容限（数值校验表）**
>
> 题目：用讲义 p.23 的逻辑门家族表逐行算出 $NM_H$ 与 $NM_L$。
>
> 解（四行依次代入 $NM_H = V_{OH}-V_{IH}$、$NM_L = V_{IL}-V_{OL}$）：
>
> | 家族 | $V_{DD}$ | $V_{IL}$ | $V_{IH}$ | $V_{OL}$ | $V_{OH}$ | $NM_H$ | $NM_L$ |
> |---|---|---|---|---|---|---|---|
> | TTL | 5 V (4.75–5.25) | 0.8 | 2.0 | 0.4 | 2.4 | $2.4-2.0=0.4$ V | $0.8-0.4=0.4$ V |
> | CMOS | 5 V (4.5–6) | 1.35 | 3.15 | 0.33 | 3.84 | $3.84-3.15=0.69$ V | $1.35-0.33=1.02$ V |
> | LVTTL | 3.3 V (3–3.6) | 0.8 | 2.0 | 0.4 | 2.4 | $2.4-2.0=0.4$ V | $0.8-0.4=0.4$ V |
> | LVCMOS | 3.3 V (3–3.6) | 0.9 | 1.8 | 0.36 | 2.7 | $2.7-1.8=0.9$ V | $0.9-0.36=0.54$ V |
>
> **数值校验 (Numerical check)**：$2.4-2.0 = 0.4$ ✓、$0.8-0.4 = 0.4$ ✓；
> $3.84-3.15 = 0.69$ ✓、$1.35-0.33 = 1.02$ ✓；$2.7-1.8 = 0.9$ ✓、$0.9-0.36 = 0.54$ ✓。
> 一致性自查：$NM_H+NM_L$ 应等于 $(V_{OH}-V_{OL})-(V_{IH}-V_{IL})$ ——
> TTL $(2.4-0.4)-(2.0-0.8) = 2.0-1.2 = 0.8 = 0.4+0.4$ ✓；
> CMOS $(3.84-0.33)-(3.15-1.35) = 3.51-1.80 = 1.71 = 0.69+1.02$ ✓；
> LVCMOS $(2.7-0.36)-(1.8-0.9) = 2.34-0.90 = 1.44 = 0.9+0.54$ ✓。
>
> **Example 3 — 噪声预算：这个网络该选哪个家族？**
>
> 题目：某 5 V 单板上的网络，最坏情况下高电平方向的退化有：导线与接触电阻压降 0.30 V、
> 邻线串扰 $+0.15$ V、电源噪声 $0.10$ V。分别用 TTL、CMOS(5 V)、LVCMOS(3.3 V) 的 $NM_H$ 判断是否通过。
>
> 解：
>
> 1. 噪声预算（同方向相加）：$0.30+0.15+0.10 = 0.55$ V。
> 2. TTL：$NM_H = 0.4$ V，$0.55 > 0.4$ → **不通过**（缺口 0.15 V）。
> 3. CMOS 5 V：$NM_H = 0.69$ V，$0.55 < 0.69$ → **通过**，余量 $0.69-0.55 = 0.14$ V。
> 4. LVCMOS 3.3 V：$NM_H = 0.9$ V，$0.55 < 0.9$ → **通过**，余量 $0.9-0.55 = 0.35$ V
>    （但还要核对它能否驱动 5 V 输入，见 [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围|Logic Levels]] 例 2）。
>
> **数值校验 (Numerical check)**：$0.30+0.15+0.10 = 0.55$ ✓；
> $0.55-0.4 = +0.15$ V（超出 → 失败）、$0.69-0.55 = 0.14$ V ✓、$0.9-0.55 = 0.35$ V ✓；
> 相对余量：TTL 的 $0.4/5 = 8.0\%$ 小于噪声 $0.55/5 = 11\%$，而 LVCMOS 的 $0.9/3.3 = 27.3\%$
> 远大于 $0.55/3.3 = 16.7\%$ —— 两种看法给出同一个结论。
>
> **Noise margins are interface budgets · 噪声容限是接口预算**
>
> High noise margin is the guaranteed driver's minimum HIGH voltage minus the receiver's minimum recognized HIGH input. Low noise margin is the receiver's maximum recognized LOW input minus the driver's maximum LOW voltage. The driver and receiver may be different devices, so do not select all four quantities automatically from one transfer curve.
>
> A positive margin is a static voltage budget. It does not guarantee correct sampling of a short pulse or immunity to arbitrary disturbances. Pulse duration, path delay, and the sampling event belong to the dynamic model. Negative margin already fails the guaranteed static interface, before timing is considered.
>
> **Worked application — asymmetric disturbance.** 假设 $V_{OH(min)}=3.0$ V、$V_{IH(min)}=2.2$ V，则 $NM_H=0.8$ V；$V_{IL(max)}=0.7$ V、$V_{OL(max)}=0.2$ V，则 $NM_L=0.5$ V。HIGH 上叠加 −0.6 V 后为 2.4 V，仍有效；LOW 上叠加 +0.6 V 后为 0.8 V，已超过 LOW 保证范围。平均余量 0.65 V 不能代替逐极性检查。
>
> In English: the less tolerant polarity limits a common symmetric disturbance specification. The two budgets remain separate when disturbances have different directions or amplitudes.
>
> **English exam question:** Why should worst-case guaranteed voltages be used instead of typical output voltages?
>
> **Answer:** Typical values do not guarantee every allowed device and operating condition. Noise margin is intended to establish a reliable interface, so it uses the specified output and input bounds for the conditions under analysis. A typical-value calculation is only an estimate.
>
> Use [[Logic Levels and Noise Margins#1 · Logic Levels · 保证值与接受范围|Logic Levels]] for the voltage meanings, [[Logic Levels and Noise Margins#2 · DC Transfer Characteristic · 由传输曲线理解恢复能力|DC Transfer Characteristic]] for curve interpretation, and [[Sequential Timing and Clock Domain Crossing#1 · Setup and Hold Timing · 建立统一时间基准|Setup and Hold Timing]] for the independent dynamic constraint. [[Digital Logic Troubleshooting]] connects a measured voltage to a possible interface failure.

## 4 · 重点与失效边界

> [!IMPORTANT] 先建立驱动—接收关系，再代公式
> 相同电源电压不保证逻辑族兼容；把典型值当最坏条件，会高估容限。悬空输入、总线冲突和阈值附近噪声应回到电气模型判断。

## Sources · 课件依据

主线课件：[Ch3 lecture](../ECE2050-Chap3.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
