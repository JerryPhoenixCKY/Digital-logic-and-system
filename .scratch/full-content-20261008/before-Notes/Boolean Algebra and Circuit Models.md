---
tags:
  - ECE2050
  - boolean-algebra
date: 2026-09-16
updated: 2026-10-08
chapter: Ch4
aliases:
  - 布尔代数与组合电路模型
  - Boolean Algebra and Circuit Models
  - 布尔代数与组合电路模型 · Ch4
  - Combinational Circuit
  - 组合电路
  - 组合逻辑电路
  - Combinational Logic
  - Boolean Equation
  - 布尔方程
  - 布尔表达式
  - Boolean Expression
  - Boolean Axioms
  - 布尔公理
  - 布尔代数公理
  - Axioms of Boolean Algebra
  - Laws and Rules of Boolean Algebra
  - 布尔代数定律与规则
  - 布尔代数规则
  - Laws of Boolean Algebra
  - Rules of Boolean Algebra
  - DeMorgan's Theorems
  - 德摩根定理
  - 德摩根定律
  - De Morgan's Law
  - Proof by Perfect Induction
  - 完全归纳法
  - 穷举证明
  - Perfect Induction
  - Proof by Exhaustion
---

# Boolean Algebra and Circuit Models · 布尔代数与组合电路模型

> [!SUMMARY] Quick recall · 英文速览
> Define a valid combinational model before manipulating equations. Boolean laws preserve a function, while composition rules constrain the physical topology.

## 1 · Combinational Circuit · 先确认可以使用的模型

组合电路 (combinational circuit) 的稳态输出只由当前输入决定。构成要求：各元件组合；每个内部／输出节点恰有一个驱动；信号依赖无环。扇出 (fan-out) 是一个输出接多个输入，不能与多个输出并接混淆。

> [!example]- Combinational Circuit · 推导与例题
> **图示与讲义依据**
>
> ![[ch4-combinational-nodes.png]]
> *图 1 — 讲义 p.5 原图：输入节点 A、B、C，输出节点 Y、Z，内部节点 n1，以及三个元件 E1/E2/E3；
> 注意图中每个元件的**输出**都只接到一条线上，n1 这一根线同时喂给两个元件的输入（fan-out）。*
>
> **Derivation · 推导过程**
>
> **1. 先给每个节点找"驱动者"**
>
> 对每个节点问一个问题：**谁在驱动它？** 答案只有三种：
>
> - 外部世界 → 它是输入节点；
> - 恰好一个元件的输出 → 它是内部节点或输出节点；
> - 零个或两个以上元件输出 → **违反规则 2**。
>
> **2. 扇出 (fan-out) 是允许的，两个驱动者是不允许的**
>
> 一个元件的输出可以同时喂给很多个输入（图 2(a) 里 $n_1$ 同时喂给 E2 和 E3），这叫 **fan-out**，
> 节点仍然只有**一个**驱动者，合法。反过来，两个元件的输出短接在同一个节点上时，这个节点有了**两个**驱动者：
> 一个想把电平拉高、另一个想拉低，节点电平就不确定了 —— 违反规则 2。
>
> **3. 无环 = 无记忆**
>
> 如果存在回路（例如把 E2 的输出接回 E1 的输入），当前输出就会反过来影响自己的输入。
> 此时不能按无环组合网络直接逐级求值。合适的反馈能保存状态，但反相反馈也可能振荡；
> 需结合实际拓扑判断，不能仅凭有环就保证稳定记忆。
>
> ![[combinational-rules.svg]]
> *图 2 — (a) 合法构成：E1(AND) 驱动内部节点 n1，n1 再扇出到 E2(OR) 与 E3(NOT)；每个节点恰好一个驱动者。
> (b) 非法构成：E4(NOT) 与 E5(AND) 的输出被短接在同一个节点上，该节点有两个驱动者，
> 它们的值可能相反，节点电平（以及 Y）因此没有定义。*
>
> **Worked Example · 例题**
>
> **Example 1 — 给讲义 p.5 的电路补上元件功能并逐行枚举（讲义 p.5 的节点图）**
>
> 题目：讲义 p.5 只标出节点 $A,B,C$、$n_1$、$Y,Z$ 与元件 $E_1,E_2,E_3$，没有说每个元件是什么。
> 下面自设一组：$E_1=\text{AND}(A,B)$，$E_2=\text{OR}(n_1,C)$，$E_3=\text{NOT}(n_1)$，检查它是否合法并求输出。
>
> 解：
>
> 1. 节点清单：输入 $A,B,C$；内部 $n_1$；输出 $Y,Z$。
> 2. 规则 1：AND / OR / NOT 都是组合元件 ✓。
> 3. 规则 2：$n_1$ 只被 $E_1$ 驱动（$E_2,E_3$ 只是**读**它）✓；$Y$ 只被 $E_2$ 驱动 ✓；$Z$ 只被 $E_3$ 驱动 ✓。
> 4. 规则 3：$A,B,C\to E_1\to n_1\to E_2/E_3$，没有任何线往回走 ✓。
> 5. 写方程：$n_1=AB$，$Y=n_1+C=AB+C$，$Z=\overline{n_1}=\overline{AB}$。
>
> **数值校验 (Numerical check)**：把 $A,B,C$ 的 8 种组合全部代入（Python 逐行枚举）：
>
> | $A$ | $B$ | $C$ | $n_1=AB$ | $Y=n_1+C$ | $Z=\overline{n_1}$ |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 1 |
> | 0 | 0 | 1 | 0 | 1 | 1 |
> | 0 | 1 | 0 | 0 | 0 | 1 |
> | 0 | 1 | 1 | 0 | 1 | 1 |
> | 1 | 0 | 0 | 0 | 0 | 1 |
> | 1 | 0 | 1 | 0 | 1 | 1 |
> | 1 | 1 | 0 | 1 | 1 | 0 |
> | 1 | 1 | 1 | 1 | 1 | 0 |
>
> 每一行的 $n_1$ 只有一个值 ✓（两个驱动者的话这一列就会出现"既是 0 又是 1"），
> $Y$ 与 $Z$ 也各自唯一 ✓ —— 这就是"电路是组合的"在数值上的样子。
>
> **Example 2 — 违反规则 2：两个输出短接（自算，讲义 p.7 的"违反规则会怎样"）**
>
> 题目：把 $E_4=\text{NOT}(A)$ 与 $E_5=\text{AND}(B,C)$ 的输出短接成同一个节点，再引到输出 $Y$。
> 这个电路合法吗？输出会怎样？
>
> 解：该节点有两个驱动者，$E_4$ 想输出 $\bar A$，$E_5$ 想输出 $BC$，两者只在某些输入下一致。
>
> **数值校验 (Numerical check)**：8 行枚举，比较两个驱动者：
>
> | $A$ | $B$ | $C$ | $E_4=\bar A$ | $E_5=BC$ | 节点 |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 1 | 0 | 冲突 |
> | 0 | 0 | 1 | 1 | 0 | 冲突 |
> | 0 | 1 | 0 | 1 | 0 | 冲突 |
> | 0 | 1 | 1 | 1 | 1 | 一致 |
> | 1 | 0 | 0 | 0 | 0 | 一致 |
> | 1 | 0 | 1 | 0 | 0 | 一致 |
> | 1 | 1 | 0 | 0 | 0 | 一致 |
> | 1 | 1 | 1 | 0 | 1 | 冲突 |
>
> **8 行里有 4 行两个驱动者给出相反的值**（$A=0,B=0,C=0$；$A=0,B=0,C=1$；$A=0,B=1,C=0$；$A=1,B=1,C=1$），
> 这 4 行里 $Y$ 究竟是多少**没有定义** —— 电路的行为不再是一个函数，规则 2 不是"风格建议"而是"有没有意义"的分界。
>
> **Example 3 — 规则 3：接成回路会怎样（自设反例）**
>
> 题目：把 Example 1 里的 $E_2$ 输出接回 $E_1$ 的第二个输入（$n_1=A\cdot Y$），电路还是组合的吗？
>
> 答：不是。此时 $Y=n_1+C=A\cdot Y+C$：$Y$ 通过 $n_1$ 依赖自己。取 $A=1,C=0$，方程变成 $Y=Y$，
> $Y=0$ 和 $Y=1$ 都满足 —— 输出不再由输入唯一决定，而是取决于"上一次留下的值"，这正是**记忆**。
> 稳定反馈的存储机制见 [[Sequential Logic and Flip-Flops#2 · Set-Reset Latch · 反馈产生记忆|Set-Reset Latch]]；时序设计主线见 [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]]。
>
> **Composition and state boundaries · 构成规则与状态边界**
>
> The composition rules establish a single-driver, acyclic Boolean network. They are sufficient conditions for the course's combinational model, not a classifier that turns every invalid connection into a valid sequential circuit. Shorted ordinary outputs can produce contention. An inverter loop can oscillate. A carefully designed bistable feedback circuit can store state. These outcomes require different physical and functional models.
>
> Separate fan-out from multiple drivers. One output feeding three inputs is still one driver; three outputs tied together are three drivers. A deliberately managed tri-state bus needs an ownership protocol and released outputs, as explained in [[Tri-State Buffers and Bus Drivers]]. It is not justified merely by drawing one wire.
>
> **Worked application.** 对 $n=AB,Y=n+C$，A/B/C 改变后需要门延迟才能得到稳定 Y，但不需要保存上一拍的 n。若改为 $n=AY$，A=1,C=0 时允许 Y=0 或1，说明仅凭当前输入不能唯一决定该反馈系统状态；是否真的稳定存储还要检查电路实现。
>
> **English exam question:** Does a circuit without a clock necessarily have combinational behavior?
>
> **Answer:** No. A latch can store a value without a clock edge, and an unstable feedback loop can oscillate. Determine whether the output is uniquely specified by current inputs under the stated model, then inspect state and feedback. Continue with [[Combinational Logic Analysis and Design#1 · Combinational Logic Design · 需求先于门|Combinational Logic Design]] or [[Sequential Logic and Flip-Flops#1 · Sequential Logic · 用状态连接过去与现在|Sequential Logic]] according to the required behavior.

## 2 · Boolean Equation · 从需求写函数

布尔方程 (Boolean equation) 先定义输入事件、极性、输出断言条件和变量顺序。$Y=F(\mathbf x)$ 的各分量均为 0/1；规范中的 exactly、at least、active-low 会改变函数，先列条件再选门。

> [!example]- Boolean Equation · 推导与例题
> **Derivation · 推导过程**
>
> **1. 讲义 p.9：全加器的两个方程，逐项读**
>
> $$
> S=A\oplus B\oplus C_{in},\qquad C_{out}=AB+AC_{in}+BC_{in}
> $$
>
> - $S$（sum 位）：三个输入**异或**。$A\oplus B\oplus C_{in}=1$ 当且仅当 $A,B,C_{in}$ 中**有奇数个 1**
>   （1 个或 3 个）。这正是"三个 1 bit 相加后，留在本位的和"。
> - $C_{out}$（carry 位）：三个**两两乘积**再 OR。三项分别代表：
>   - $AB=1$ —— $A$ 和 $B$ 都是 1（这两个相加就已经满了）；
>   - $AC_{in}=1$ —— $A$ 和进位输入都是 1；
>   - $BC_{in}=1$ —— $B$ 和进位输入都是 1。
>   三项合起来的意思就是"**至少两个输入是 1**"，也就是"三个 bit 相加达到 2 或 3，要向下一位进 1"。
> - 两项的分工：$S$ 数的是**奇偶**（1 的个数模 2），$C_{out}$ 数的是**有没有到 2**。两者拼起来就是完整的加法结果
>   $A+B+C_{in}=2C_{out}+S$。
>
> **2. 从一段文字到方程的四个动作**
>
> 1. **先定输出**：这段话在问哪件事？（"能不能去公园" → $P$）
> 2. **把每个前提起一个字母**：Raining → $R$，Sandwiches → $S$，Hat → $H$……
> 3. **按连接词翻译**：and → 相乘，or → 相加，"not/没有" → 加横线。注意"but not" 也是 and-not。
> 4. **用优先级和括号还原语序**：先 AND 后 OR；如果原句的意思是先 OR，就必须加括号。
>
> **3. 讲义 p.10–14 的五个例子**
>
> | 讲义页 | 文字条件 | 布尔方程 | 备注 |
> |---|---|---|---|
> | p.10 | 不下雨 **并且** 有三明治 ($S$) 才去公园 ($P$) | $P=\bar R S$ | 抽取文本横线丢失；按句子语义（$R=1$ 表示下雨）取 $\bar R$，见下方 WARNING |
> | p.11 | 给你一百万 ($M$) **或** 一个小记事本 ($N$)，你就是赢家 ($W$) | $W=M+N$ | 只要有一个为 1 就出 1 |
> | p.12 | 自己做饭 ($M$)，**或** 有私人厨师 ($C$) **并且** 他/她有天赋 ($T$) **并且** 不贵 ($\bar X$) | $E=M+CT\bar X$ | AND 先算，所以 $M+(CT\bar X)$；括号不能写成 $(M+C)T\bar X$ |
> | p.13 | 有帽子 ($H$) **并且** 穿鞋 ($S$)，**或者** 有帽子 ($H$) | $E=HS+H$ | 用 Rule 10 得 $E=H$：有帽子就能进，鞋是废话 |
> | p.14 | 有帽子**并且**穿鞋，**或者** 有帽子**并且**没穿鞋 | $E=HS+H\bar S$ | 用分配律 + Rule 7 得 $E=H$：与 p.13 殊途同归 |
>
> 最后两例的意义：**两段听起来不同的规则写成了不同的式子，化简后却是同一个 $H$** —— 这就是第 4 章后面要干的事，
> 化简规则见 [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则|Laws and Rules of Boolean Algebra]]。
>
> **讲义抽取文本里的横线会丢，横线位置以句子语义为准**
> 纯文本抽取会把公式的上横线丢掉：p.10 只剩下 `P = RS`，p.14 只剩下 `E = HS + HS`（实际是 $HS+H\bar S$），
> p.12 的 `E = M + CTX` 也丢掉了 $\bar X$。本篇按**句子语义**还原：$R=1$ 表示"在下雨"，
> "不下雨"就是 $\bar R$，所以 $P=\bar R S$。
> 如果老师把变量 $R$ 定义成"不下雨"这件事本身，同一个方程就写成 $P=RS$ ——
> **横线的位置取决于变量怎么定义**，这正是下面误区 5 要强调的：动手前先声明"1 代表什么"。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.9 的全加器方程逐行核对**
>
> 题目：验证 $S=A\oplus B\oplus C_{in}$ 与 $C_{out}=AB+AC_{in}+BC_{in}$ 真的是"三个 1 bit 相加"。
>
> 解：把三个输入相加得到十进制和 $A+B+C_{in}\in\{0,1,2,3\}$，它应当等于 $2C_{out}+S$。
>
> **数值校验 (Numerical check)**（8 行全部枚举）：
>
> | $A$ | $B$ | $C_{in}$ | $AB$ | $AC_{in}$ | $BC_{in}$ | $C_{out}$ | $S$ | $A+B+C_{in}$ | $2C_{out}+S$ |
> |---|---|---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 ✓ |
> | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 ✓ |
> | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 ✓ |
> | 0 | 1 | 1 | 0 | 0 | **1** | 1 | 0 | 2 | 2 ✓ |
> | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 ✓ |
> | 1 | 0 | 1 | 0 | **1** | 0 | 1 | 0 | 2 | 2 ✓ |
> | 1 | 1 | 0 | **1** | 0 | 0 | 1 | 0 | 2 | 2 ✓ |
> | 1 | 1 | 1 | **1** | **1** | **1** | 1 | 1 | 3 | 3 ✓ |
>
> 8 行全部满足；$C_{out}$ 恰好是"A 与 B 中至少两个为 1"的 8 行真值，$S$ 恰好是"1 的个数为奇数"。
>
> **Example 2 — 五个文字例子写成方程（讲义 p.10–14）**
>
> 题目：写出 $P$（去公园）、$W$（赢家）、$E$（吃美食）、$E$（进楼，两版）的方程。
>
> 解：按上表 ——
>
> $$
> P=\bar R S,\qquad W=M+N,\qquad E=M+CT\bar X,\qquad E=HS+H,\qquad E=HS+H\bar S
> $$
>
> **数值校验 (Numerical check)**：
> - $P=\bar RS$：下雨天（$R=1$）→ $\bar R=0$ → $P=0$，无论有没有三明治 ✓；不下雨且有三明治 → $1\cdot1=1$ ✓。
> - $W=M+N$：$M=0,N=0$ → $W=0$（两样都没给）✓；$M=0,N=1$ → $W=1$ ✓。
> - $E=M+CT\bar X$：取 $M=0,C=1,T=1,X=0$（不做饭、厨师有天赋且不贵）→ $E=0+(1\cdot1\cdot1)=1$ ✓；
>   改成 $X=1$（太贵）→ $E=0+(1\cdot1\cdot0)=0$ ✓ —— 横线 $\bar X$ 一票否决整条厨师分支。
> - 括号的数值意义：若把 p.12 写成 $(M+C)T\bar X$，取 $M=1,C=0,T=0,X=0$ 得 $0$，
>   而正确写法 $M+CT\bar X$ 得 $1$（自己做饭当然能吃上）；两种括号在 16 行里有 **6 行**结果不同 ✓。
>
> **Example 3 — p.13 与 p.14 的例子其实是同一个方程**
>
> 题目：证明 $E=HS+H$ 与 $E=HS+H\bar S$ 都等于 $H$。
>
> 解：
>
> $$
> \begin{aligned}
> E&=HS+H=H(1+S)=H\cdot 1=H &&\text{(分配律 + Rule 3 + Rule 2)}\\
> E&=HS+H\bar S=H(S+\bar S)=H\cdot 1=H &&\text{(分配律 + Rule 7 + Rule 2)}
> \end{aligned}
> $$
>
> **数值校验 (Numerical check)**（4 行全枚举）：
>
> | $H$ | $S$ | $HS$ | $H\bar S$ | $HS+H$ | $HS+H\bar S$ | $H$ |
> |---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 ✓ |
> | 0 | 1 | 0 | 0 | 0 | 0 | 0 ✓ |
> | 1 | 0 | 0 | 1 | 1 | 1 | 1 ✓ |
> | 1 | 1 | 1 | 0 | 1 | 1 | 1 ✓ |
>
> 两列 $HS+H$ 与 $HS+H\bar S$ 都与 $H$ 逐行相同 —— "戴帽子就能进"这句话里**鞋子完全不影响结果**。
>
> **Example 4 — 自己写一个（自算）**
>
> 题目：晚上复习 ($R$)，如果你有咖啡 ($C$) 并且没有停电 ($\bar P$)，或者你有同桌的笔记 ($N$)，就能坚持复习。
> 写出方程并判断 $C=1,P=1,N=0$ 时的结果。
> 解：$R=C\bar P+N$。代入：$C\bar P=1\cdot0=0$，$N=0$ → $R=0$：停电了又没有笔记，咖啡救不了 ✓。
>
> **Specification before implementation · 方程先描述需求**
>
> A Boolean equation states what the output must mean. It does not uniquely determine a gate topology. The same equation can be implemented with basic gates, NAND-only gates, a multiplexer, a decoder, or a lookup table. Keep the specification independent of the chosen implementation so there is an external reference for verification.
>
> Declare the input meanings and polarity before writing algebra. If L=1 means “level is low”, a positive L term expresses an asserted low-level event even though the physical sensor could use a LOW voltage. An electrical LOW, a Boolean zero, and a deasserted alarm need not have the same meaning.
>
> **Worked application.** 许可条件 E、故障 F、按钮 P：只在 E=1,F=0,P=1 时启动，故 $RUN=E\bar FP$。若故障输入针脚 FAULT_N=0 表示故障，则“无故障”为 FAULT_N=1，方程变为 $RUN=E\,FAULT\_N\,P$；不是把字母名字中的 N 当作另一次代数取反。
>
> **English exam question:** Why should the variable order be declared for a minterm list?
>
> **Answer:** The order defines each input's binary weight and therefore the row index. A correct truth condition can receive a different minterm number after the variables are reordered. Use [[Boolean Forms and Algebraic Simplification 1#2 · Truth Table and Boolean Expression · 用真值表定义全集|Truth Table and Boolean Expression]], then compare implementation choices in [[Comparison Decoding and Selection#2 · Decoder · 代码变线路|Decoder]] and [[Comparison Decoding and Selection#4 · Multiplexer and Demultiplexer · 选择与分配|Multiplexer and Demultiplexer]].

## 3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则

| 规则 | OR 形式 | AND 对偶 |
|---|---|---|
| 单位与控制值 | $A+0=A,\ A+1=1$ | $A1=A,\ A0=0$ |
| 幂等 | $A+A=A$ | $AA=A$ |
| 互补 | $A+\bar A=1$ | $A\bar A=0$ |
| 吸收 | $A+AB=A$ | $A(A+B)=A$ |
| 分配 | $A(B+C)=AB+AC$ | $A+BC=(A+B)(A+C)$ |

交换、结合与双重反相同样成立。对偶 (duality) 交换 AND／OR 与 0／1，但不等于把整个函数取反；布尔加法也不是普通实数加法。

> [!example]- Boolean Axioms · 推导与例题
> **Derivation · 推导过程**
>
> **1. 为什么只有五条就够**
>
> A1 把变量锁进 $\{0,1\}$ 两个值里；A2 定义了一元运算 NOT；A3–A5 用**真值组合**（$00,11,01$）把二元运算 AND/OR 在
> 所有输入上钉死。三个符号 $\cdot$、$+$、$'$ 在全部输入组合上的行为都有了规定 —— 于是布尔代数**没有任何自由度**，
> 任何式子的值都可以推算出来，也都可以用真值表穷举验证（这就是 perfect induction 能当证明用的原因）。
>
> **2. 对偶是"机械替换"，为什么这样换不会出错**
>
> 观察 p.17 的表：每一行的左右两列互为对偶，而且**两列都是公理**。例如 A3 的左列 $0\cdot0=0$ 与右列 $1+1=1$：
> 把左列的 $\cdot$ 换成 $+$、$0$ 换成 $1$，正好得到右列。既然公理本身关于对偶对称，
> 那么用公理做的每一次替换，它的"镜像替换"也同样是公理 —— 整个推导链都可以镜像过来，结论（等式）自然也对偶成立。
>
> **3. 从公理到定理：对偶把定理配对**
>
> 第 4-04 的 12 条规则也是成对的，配对方式与公理一模一样：
>
> | 规则 | 对偶规则 |
> |---|---|
> | Rule 7：$A+\bar A=1$ | Rule 8：$A\bar A=0$ |
> | Rule 1：$A+0=A$ | Rule 2：$A\cdot1=A$ |
> | Rule 10：$A+AB=A$ | 吸收律：$A(A+B)=A$ |
> | Rule 12：$(A+B)(A+C)=A+BC$ | 分配律：$A(B+C)=AB+AC$ |
>
> - 意义：**只需要记住一半**，另一半用对偶机械得到。
> - 数值校验：Rule 7 在 $A=0,1$ 两行分别给出 $0+\bar0=0+1=1$ ✓、$1+\bar1=1+0=1$ ✓；
>   它的对偶 Rule 8 在同样两行给出 $0\cdot\bar0=0\cdot1=0$ ✓、$1\cdot\bar1=1\cdot0=0$ ✓ —— 两条都恒成立。
>
> **Worked Example · 例题**
>
> **Example 1 — 写出 A1–A5 的对偶式（讲义 p.17）**
>
> 题目：逐条给出 A1–A5 的对偶。
>
> 解（把 $\cdot\leftrightarrow+$、$0\leftrightarrow1$ 机械替换）：
>
> | 公理 | 对偶式 |
> |---|---|
> | A1：$B=0$ if $B\ne1$ | $B=1$ if $B\ne0$ |
> | A2：$0'=1$ | $1'=0$ |
> | A3：$0\cdot0=0$ | $1+1=1$ |
> | A4：$1\cdot1=1$ | $0+0=0$ |
> | A5：$0\cdot1=1\cdot0=0$ | $1+0=0+1=1$ |
>
> **数值校验 (Numerical check)**：对只有一个变量 $B$ 的情况枚举 $B=0,1$：
> A1 左列在 $B=0$ 时给出 $0=0$ ✓、$B=1$ 时前提 $B\ne1$ 不成立（不作断言）✓；
> A3 左列 $0\cdot0=0$ 与右列 $1+1=1$ 都是常量等式 ✓；A5 的 $0\cdot1=1\cdot0=0$ 两边相等 ✓。
> Python 逐行枚举确认：**A3–A5 及其对偶式在全部 2 行上恒真**。
>
> **Example 2 — 自检题：随手写一条的对偶**
>
> 题目 (a)：写出 $A+\bar B C=1$ 的对偶式。
> 题目 (b)：写出 $(A+B)(\bar A+C)$ 的对偶式。
>
> 解：
>
> (a) $\cdot\to+$（$\bar BC$ 里的省略乘号是 $\cdot$）、$+\to\cdot$、$1\to0$：
>
> $$
> A+\bar BC=1 \quad\Longrightarrow\quad A(\bar B+C)=0
> $$
>
> (b) 只有运算符要换，变量与横线照抄：
>
> $$
> (A+B)(\bar A+C) \quad\Longrightarrow\quad AB+\bar A C
> $$
>
> **数值校验 (Numerical check)**：
> (a) 先看原式 $A+\bar BC=1$：$A=1$ 时 $1+\bar BC=1$ ✓ 成立；$A=0,B=1,C=0$ 时 $0+\bar1\cdot0=0\ne1$ ✗ 不成立。
> 再看对偶式 $A(\bar B+C)=0$：$A=0$ 时 $0\cdot(\dots)=0$ ✓ 成立；$A=1,B=0,C=0$ 时 $1\cdot(1+0)=1\ne0$ ✗ 不成立。
> 两式**互为对偶但都不是恒等式** —— 对偶原理保证的是："原式若对**所有**输入成立，则对偶式也对所有输入成立"，
> 而这里原式本来就不是恒等式（第 4-04 的 12 条规则才是恒等式）。
> (b) 枚举 4 行可见两式**不是同一个式子**：$A=1,B=0,C=1$ 时 $(A+B)(\bar A+C)=(1+0)(0+1)=1$，
> 而对偶式 $AB+\bar AC=1\cdot0+0\cdot1=0$ ✓（值不同）；再把对偶式取一次对偶：
> $AB+\bar AC\to(A+B)(\bar A+C)$ ✓ 回到原式，验证了对合性。
>
> **Example 3 — 用对偶把 Rule 7 变成 Rule 8**
>
> 题目：已知 $A+\bar A=1$ 恒成立，不另做真值表，直接写出并验证它的对偶式。
>
> 解：对偶式 $=A\cdot\bar A=0$（把 $+$ 换成 $\cdot$、$1$ 换成 $0$，变量与横线不动）。
>
> **数值校验 (Numerical check)**：
>
> | $A$ | $\bar A$ | $A+\bar A$ | $A\bar A$ |
> |---|---|---|---|
> | 0 | 1 | 1 ✓ | 0 ✓ |
> | 1 | 0 | 1 ✓ | 0 ✓ |
>
> 两行都对：$A+\bar A=1$ 与其对偶 $A\bar A=0$ 同时成立 ✓。这正是第 4-04 里 Rule 7 与 Rule 8 的配对。
>
> **Example 4 — 对偶 ≠ 取反（辨析，自算）**
>
> 题目：$F=A+0$ 的对偶式与反函数分别是什么？
>
> 解：对偶式 $F^{D}=A\cdot1=A$（只换运算符与常量，变量不动）；
> 反函数 $\bar F=\overline{A+0}=\bar A\cdot\bar 0=\bar A\cdot1=\bar A$（把整个式子取反，变量要变）。
>
> **数值校验 (Numerical check)**：
>
> | $A$ | $F=A+0$ | $F^{D}=A\cdot1$ | $\bar F$ |
> |---|---|---|---|
> | 0 | 0 | 0 | 1 |
> | 1 | 1 | 1 | 0 |
>
> 两行都有 $F^{D}\ne\bar F$ ✓：**对偶式与反函数是两个不同的东西**。前者是"另一条同类等式"（这里恰好与原式相等，
> 因为 $A+0=A$ 本身是恒等式），后者是"同一个函数的补"。
> 把 $F^{D}=A$ 误当成 $\bar F$ 会在下一步化简时把整个函数取反，结果全错。
>
> **Duality and logical meaning · 对偶与逻辑含义**
>
> Boolean variables take values zero and one. AND and OR are logical operations, so ordinary numerical cancellation and division are generally unavailable. For example, A+A=A is valid Boolean idempotence; it does not imply A=0 by subtracting A as though the plus sign denoted real addition.
>
> Duality exchanges AND with OR and zero with one while preserving the variables and their complements. Complementing a complete expression is a different operation: DeMorgan's law also complements the operands. Keeping these transformations separate prevents a common exam error.
>
> **Worked application.** 恒等式 $A+0=A$ 的对偶是 $A\cdot1=A$，不是 $\bar A+1=\bar A$。后一式在 A=1 时左侧为1、右侧为0，立即失败。若对原等式两边取补，则应得 $\overline{A+0}=\bar A$，并经 DeMorgan 化为 $\bar A\cdot1=\bar A$。
>
> **English exam question:** Can a useful Boolean rewrite be accepted because it works for one input pattern?
>
> **Answer:** One passing row is an example, not a proof. Derive the rewrite from valid axioms and laws, or check every input combination with [[Boolean Algebra and Circuit Models#5 · Proof by Perfect Induction · 穷举与代数验证|Proof by Perfect Induction]]. These identities become hardware transformations in [[Universal Gates and Bubble Pushing]].

> [!example]- Laws and Rules of Boolean Algebra · 推导与例题
> **Derivation · 推导过程**
>
> **1. 规则从公理来：以 Rule 5 ($A+A=A$) 为例**
>
> 一条"看起来显然"的规则也可以由公理推出来（讲义 p.20 的 Method 2）：
>
> $$
> \begin{aligned}
> A+A&=(A+A)\cdot1 &&\text{Rule 2（}X=X\cdot1\text{）}\\
> &=(A+A)(A+\bar A) &&\text{Rule 7（}1=A+\bar A\text{）}\\
> &=A+A\bar A &&\text{Rule 12 反向（}(X+Y)(X+Z)=X+YZ\text{）}\\
> &=A+0 &&\text{Rule 8（}A\bar A=0\text{）}\\
> &=A &&\text{Rule 1（}X+0=X\text{）}
> \end{aligned}
> $$
>
> - 意义：每条规则都不是"新假设"，而是公理的推论；想确认某一步合不合法，就去追它来自哪条公理/规则。
> - 数值校验：$A=0$ 时上式每一行都是 $0$（$0+0=0$、$0\cdot1=0$、$(0+0)(0+1)=0$、$0+0\cdot1=0$、$0+0=0$）✓；
>   $A=1$ 时每一行都是 $1$ ✓ —— 5 步分别成立，整条链成立。
>
> **2. 为什么 Rule 12 值得单独记**
>
> 对 $A(B+C)=AB+AC$ 我们很熟；Rule 12 是它的**另一种展开**：
>
> $$
> (A+B)(A+C)=AA+AC+AB+BC=A+AC+AB+BC=A(1+C+B)+BC=A\cdot1+BC=A+BC
> $$
>
> 它把"两个和式相乘"变成"一个和 + 一个积"，是化简里**合并项**的关键（也正是 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Product-of-Sums Form]] 化简的入口）。
>
> **3. 布尔加法/乘法的两个"取值问题"（讲义 p.18）**
>
> - **和项 (sum term)** $=0$ 的条件：和项就是一个 OR，$=0$ 意味着**每一项都是 0**。
>   对 $\bar A+\bar B+C+\bar D=0$ 来说：$\bar A=0\Rightarrow A=1$，$\bar B=0\Rightarrow B=1$，$C=0$，$\bar D=0\Rightarrow D=1$。
> - **积项 (product term)** $=1$ 的条件：积项就是一个 AND，$=1$ 意味着**每一项都是 1**。
>   对 $A\bar B C\bar D=1$ 来说：$A=1$，$\bar B=1\Rightarrow B=0$，$C=1$，$\bar D=1\Rightarrow D=0$。
>
> **讲义 p.18 的抽取文本丢了横线**
> `.scratch/extract/ECE2050-Chap4.txt` 里 p.18 的两个式子只剩 `A + B + C + D = 0` 与 `A B C D = 1`，
> 横线全部丢失。本篇按**自洽原则**写出：和项取整条 OR 的否定形式、积项取交替形式，
> 使答案唯一且可枚举验证（见例题 4）。原文的横线位置以课堂讲义为准。
>
> **Worked Example · 例题**
>
> **Example 1 — 用 Rule 12 + 7 + 2 化简（自算，讲义 p.31 例 1 的同型题）**
>
> 题目：化简 $Y=A\bar B+A B$。
>
> 解：
>
> $$
> \begin{aligned}
> Y&=A\bar B+AB &&\\
> &=A(\bar B+B) &&\text{分配律反向（提取 }A\text{）}\\
> &=A\cdot1 &&\text{Rule 7（}\bar B+B=1\text{）}\\
> &=A &&\text{Rule 2（}A\cdot1=A\text{）}
> \end{aligned}
> $$
>
> **数值校验 (Numerical check)**（4 行全枚举）：
>
> | $A$ | $B$ | $A\bar B$ | $AB$ | $Y$ | $A$ |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 ✓ |
> | 0 | 1 | 0 | 0 | 0 | 0 ✓ |
> | 1 | 0 | 1 | 0 | 1 | 1 ✓ |
> | 1 | 1 | 0 | 1 | 1 | 1 ✓ |
>
> 化简前后 4 行完全一致 ✓ —— "有 $A$ 就行，$B$ 随便"。
>
> **Example 2 — 用 Rule 11 消掉反变量**
>
> 题目：化简 $Y=A+\bar AB$，并说明它的意思。
>
> 解：
>
> $$
> \begin{aligned}
> Y&=A+\bar AB &&\\
> &=(A+\bar A)(A+B) &&\text{Rule 12 反向（}X+YZ=(X+Y)(X+Z)\text{）}\\
> &=1\cdot(A+B) &&\text{Rule 7（}A+\bar A=1\text{）}\\
> &=A+B &&\text{Rule 2（}1\cdot X=X\text{）}
> \end{aligned}
> $$
>
> - 意义：$A$ 成立时结果为 1；$A$ 不成立时第一项为 0、第二项变成 $B$ —— 所以 $\bar AB$ 里的 $\bar A$ 条件可以省掉，答案就是 $A+B$。
> - **数值校验 (Numerical check)**：
>
> | $A$ | $B$ | $A$ | $\bar A B$ | $A+\bar AB$ | $A+B$ |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 ✓ |
> | 0 | 1 | 0 | 1 | 1 | 1 ✓ |
> | 1 | 0 | 1 | 0 | 1 | 1 ✓ |
> | 1 | 1 | 1 | 0 | 1 | 1 ✓ |
>
> **Example 3 — 真/假判断
>
> 题目：判断下列说法。
>
> | 命题 | 判断 | 理由 |
> |---|---|---|
> | 布尔加法等价于 OR | **真** | 讲义 p.18：Boolean addition = OR operation |
> | 布尔加法等价于 NOR | **假** | NOR 是 OR 再取反（见 [[Logic Gates and Boolean Functions#3 · NAND Gate and NOR Gate · 输出取补与气泡|NOR Gate]]），布尔加法不含取反 |
> | $1+1=2$ | **假** | Rule 3：$A+1=1$，取 $A=1$ 得 $1+1=1$ |
> | $A+A=2A$ | **假** | Rule 5：$A+A=A$，布尔代数没有系数 |
> | 交换律、结合律、分配律都是布尔代数的定律 | **真** | 讲义 p.19 三条定律 |
> | $A\cdot0=0$ 与 $A+1=1$ 互为对偶 | **真** | 把 $\cdot\leftrightarrow+$、$0\leftrightarrow1$ 互换即得（第 4-03） |
>
> **数值校验 (Numerical check)**：把 $A=0/1$ 代入 —— $1+1=1$ ✓；$0+0=0$ ✓；$1\cdot0=0$ ✓；$1+1=1$ ✓；
> 六条判断与两行真值表全部一致。
>
> **Example 4 — 讲义 p.18：让和项为 0、积项为 1（附枚举）**
>
> 题目 (a)：求使 $\bar A+\bar B+C+\bar D=0$ 的 $(A,B,C,D)$。
> 题目 (b)：求使 $A\bar B C\bar D=1$ 的 $(A,B,C,D)$。
>
> 解：
>
> (a) 和项（OR）为 0 ⟺ 每一项为 0：$\bar A=0\to A=1$；$\bar B=0\to B=1$；$C=0$；$\bar D=0\to D=1$。
> (b) 积项（AND）为 1 ⟺ 每一项为 1：$A=1$；$\bar B=1\to B=0$；$C=1$；$\bar D=1\to D=0$。
>
> **数值校验 (Numerical check)**：对 4 个变量枚举全部 $2^4=16$ 行 ——
> $\bar A+\bar B+C+\bar D=0$ 只在 $(1,1,0,1)$ 这一行成立（唯一解）✓；
> $A\bar B C\bar D=1$ 只在 $(1,0,1,0)$ 这一行成立（唯一解）✓。
>
> **Choose the rule by structure · 看结构选择化简规则**
>
> Name the pattern before applying a rule. Absorption removes a more restrictive condition already covered by a broader condition: A+AB=A. The product AB cannot be true when A is false, so it adds no new ON rows. This reasoning is often clearer than treating the identity as an isolated formula to memorize.
>
> The consensus term in AB+NOT A·C+BC is redundant for the steady-state Boolean function. Its removal does not necessarily preserve transient behavior: BC can bridge a path-delay gap during a change of A. Minimal literal count and hazard-free operation are different design objectives.
>
> **Worked application.** 门控报警 $Y=A+AB+\bar AC$：先 absorption 得 $A+\bar AC$；再用 $X+\bar XY=X+Y$ 得 $A+C$。A=0 时两个式子都等于 C，A=1 时都为1，形成完整的两类逻辑解释。
>
> **English exam question:** Why might a physically useful term be Boolean redundant?
>
> **Answer:** Boolean algebra compares stable output values. A redundant term can still provide an additional physical path that suppresses a glitch while another path changes. Check [[Boolean Forms and Algebraic Simplification 1#4 · Boolean Expression Simplification · 保持函数再比较代价|Boolean Expression Simplification]] for equivalence and [[Propagation Delay and Logic Hazards]] for the timing requirement before choosing the final circuit.

## 4 · DeMorgan's Theorems · 取补必须覆盖整个子式

$$\overline{XY}=\bar X+\bar Y,\qquad\overline{X+Y}=\bar X\bar Y.$$

移过外层横线时，对每项取补并交换运算；如 $\overline{AB+C}=(\bar A+\bar B)\bar C$。单变量上的横线不能顺便移到无关项。

> [!example]- DeMorgan's Theorems · 推导与例题
> **图示与讲义依据**
>
> ![[demorgan-gate-equivalence.svg]]
> *图 1 — (a) NAND 门与"输入带反相的 OR 门"等价：$\overline{AB}=\bar A+\bar B$；
> (b) NOR 门与"输入带反相的 AND 门"等价：$\overline{A+B}=\bar A\bar B$。
> 中间的等号表示两个门在全部 4 种输入组合下输出完全相同。*
>
> **Derivation · 推导过程**
>
> **1. 用 perfect induction 证明第一条：$\overline{XY}=\bar X+\bar Y$**
>
> | $X$ | $Y$ | $XY$ | $\overline{XY}$ | $\bar X$ | $\bar Y$ | $\bar X+\bar Y$ | 比较 |
> |---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 1 | 1 | 1 | 1 | ✓ |
> | 0 | 1 | 0 | 1 | 1 | 0 | 1 | ✓ |
> | 1 | 0 | 0 | 1 | 0 | 1 | 1 | ✓ |
> | 1 | 1 | 1 | 0 | 0 | 0 | 0 | ✓ |
>
> 4 行全等 → 成立 ✓。**只有 $X=Y=1$ 这一行左边为 0**，而右边也只有在 $\bar X=\bar Y=0$ 时为 0，两者同步。
>
> **2. 用 perfect induction 证明第二条：$\overline{X+Y}=\bar X\bar Y$**
>
> | $X$ | $Y$ | $X+Y$ | $\overline{X+Y}$ | $\bar X$ | $\bar Y$ | $\bar X\bar Y$ | 比较 |
> |---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 1 | 1 | 1 | 1 | ✓ |
> | 0 | 1 | 1 | 0 | 1 | 0 | 0 | ✓ |
> | 1 | 0 | 1 | 0 | 0 | 1 | 0 | ✓ |
> | 1 | 1 | 1 | 0 | 0 | 0 | 0 | ✓ |
>
> 第二条也可以**由第一条取对偶**直接得到（第 4-03 的对偶原理），不必再枚举一次 —— 这是对偶性省力的典型例子。
>
> **3. 多变量推广**
>
> $$
> \overline{XYZ}=\bar X+\bar Y+\bar Z,\qquad\qquad \overline{X+Y+Z}=\bar X\,\bar Y\,\bar Z
> $$
>
> - **分组证明（不用真值表）**：把三变量乘积当成"两项"的乘积：
>
> $$
> \overline{XYZ}=\overline{(XY)Z}=\overline{XY}+\bar Z=(\bar X+\bar Y)+\bar Z=\bar X+\bar Y+\bar Z
> $$
>
>   第一步把 $XY$ 看成 A、$Z$ 看成 B，用两变量版本；第二步再用一次两变量版本；这本质上是数学归纳法，
>   所以对任意多个变量都成立（和项同理，取对偶即可）。
>
> - **数值校验 (Numerical check)**：对 $(X,Y,Z)$ 的 8 种组合枚举，$\overline{XYZ}$ 与 $\bar X+\bar Y+\bar Z$ 8 行全等 ✓；
>   $\overline{X+Y+Z}$ 与 $\bar X\bar Y\bar Z$ 8 行全等 ✓。检验点：只有 $(1,1,1)$ 那行 $\overline{XYZ}=0$，
>   也只有那行 $\bar X+\bar Y+\bar Z=0$；只有 $(0,0,0)$ 那行 $\overline{X+Y+Z}=1$，也只有那行 $\bar X\bar Y\bar Z=1$。
>
> **4. 两个用途**
>
> 1. **把 NAND/NOR 电路改写成 AND/OR 形式**：整个电路只有 NAND 时，反复用第一条定理把横线"外推"，
>    最后得到 SOP 形式。例：$Y=\overline{\overline{AB}\cdot\overline{CD}}=\overline{\overline{AB}}+\overline{\overline{CD}}=AB+CD$。
> 2. **求反函数 (complement)**：想得到 $\bar Y$，就对 $Y$ 整体取反再用 DeMorgan 拆开 ——
>    展开后 SOP 会变成 POS（反之亦然），这就是 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Sum-of-Products Form]] 与 [[Boolean Forms and Algebraic Simplification 1#3 · Sum-of-Products Form and Product-of-Sums Form · 标准形式|Product-of-Sums Form]] 之间的桥：
>
> $$
> Y=AB+CD\ \Longrightarrow\ \bar Y=\overline{AB+CD}=(\bar A+\bar B)(\bar C+\bar D)
> $$
>
>    注意右边是**和之积**：乘积项取反后整体变号，得到的是 POS。
>
> **Worked Example · 例题**
>
> **Example 1 — 讲义 p.28 的两条定理（perfect induction）**
>
> 题目：用穷举证明两条 DeMorgan 定理。
>
> 解：见上面推导 1 与推导 2 的两张 4 行真值表，两列 $\overline{XY}$ 与 $\bar X+\bar Y$（以及 $\overline{X+Y}$ 与 $\bar X\bar Y$）
> **8 个比较点全部相同** ✓。
>
> **数值校验 (Numerical check)**：4 行 ×2 条定理 = 8 组比较，全部 ✓；第二条也可由第一条取对偶得到，
> 两条独立方法与对偶原理三者互相印证。
>
> **Example 2 — 讲义 p.29 的同型例题：把带长横线的式子拆开（自算）**
>
> 题目：化简 $Y=\overline{A+\bar B C}$。
>
> 解：最外层横线盖住一个**和** $A+\bar BC$ → 拆成"各项取反后相乘"：
>
> $$
> Y=\overline{A+\bar BC}=\bar A\cdot\overline{\bar BC}=\bar A\,(B+\bar C)
> $$
>
> 再用分配律展开：$Y=\bar A B+\bar A\bar C$。
>
> **数值校验 (Numerical check)**（8 行全枚举）：
>
> | $A$ | $B$ | $C$ | $\bar BC$ | $A+\bar BC$ | $Y=\overline{A+\bar BC}$ | $\bar A(B+\bar C)$ | $\bar AB+\bar A\bar C$ |
> |---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 ✓ |
> | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 ✓ |
> | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 ✓ |
> | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 ✓ |
> | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 ✓ |
> | 1 | 0 | 1 | 1 | 1 | 0 | 0 | 0 ✓ |
> | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 ✓ |
> | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 ✓ |
>
> 三个式子在 8 行上完全一致 ✓。第二、三次取反时注意 $\overline{\bar B}=B$（Rule 9）、$\overline{\bar C}=C$。
>
> **Example 3 — 把 NAND-only 电路化成 AND/OR（自算，典型考试题）**
>
> 题目：化简 $Y=\overline{\overline{AB}\cdot\overline{CD}}$。
>
> 解：最外层盖住一个**积**（两个 NAND 输出的乘积）→ 拆成相加，再对每一项用一次 DeMorgan：
>
> $$
> Y=\overline{\overline{AB}\cdot\overline{CD}}=\overline{\overline{AB}}+\overline{\overline{CD}}=AB+CD
> $$
>
> **数值校验 (Numerical check)**：对 4 个变量枚举 $2^4=16$ 行 —— 原式与 $AB+CD$ 16 行全等 ✓。
> 抽查：$A=B=1,C=D=0$ → $\overline{AB}=0$、$\overline{CD}=1$ → 原式 $\overline{0\cdot1}=1$，$AB+CD=1$ ✓；
> $A=B=C=D=1$ → 原式 $\overline{0\cdot0}=1$，$AB+CD=1+1=1$ ✓。
>
> **Example 4 — 陷阱对照：$\overline{XY}$ 不等于 $\bar X\bar Y$**
>
> 题目：判断 $\overline{XY}=\bar X\bar Y$ 是否成立。
>
> 解：不成立。右边是"两个都取反再相乘"，左边是"相乘后取反"，两者只在部分行为上巧合相同。
>
> **数值校验 (Numerical check)**：
>
> | $X$ | $Y$ | $\overline{XY}$ | $\bar X\bar Y$ | 比较     |
> | --- | --- | --------------- | -------------- | ------ |
> | 0   | 0   | 1               | 1              | 巧合相同   |
> | 0   | 1   | 1               | 0              | **不同** |
> | 1   | 0   | 1               | 0              | **不同** |
> | 1   | 1   | 0               | 0              | 巧合相同   |
>
> 4 行里有 **2 行不同** ✓ —— 所以 $\overline{XY}=\bar X\bar Y$ 是错的；正确的展开是 $\overline{XY}=\bar X+\bar Y$（第一条定理）。
>
> **Example 5 — 求反函数（自算）**
>
> 题目：求 $Y=A\bar B+C$ 的反函数 $\bar Y$，并给出 POS 形式。
>
> 解：
>
> $$
> \bar Y=\overline{A\bar B+C}=\overline{A\bar B}\cdot\bar C=(\bar A+B)\bar C=\bar A\bar C+B\bar C
> $$
>
> **数值校验 (Numerical check)**：对 3 个变量枚举 8 行 ——
> $A=1,B=0,C=0$：$Y=1\cdot1+0=1$，$\bar Y=0$；而 $(\bar A+B)\bar C=(0+0)\cdot1=0$ ✓。
> $A=1,B=1,C=0$：$Y=0+0=0$，$\bar Y=1$；$(\bar A+B)\bar C=(0+1)\cdot1=1$ ✓。
> $A=0,B=0,C=1$：$Y=0+1=1$，$\bar Y=0$；$(1+0)\cdot0=0$ ✓。8 行全部一致 ✓。
>
> **Move the outer complement carefully · 外层取补怎样分配**
>
> Apply DeMorgan's law to the operation enclosed by the outermost bar. Change AND to OR or OR to AND, and complement every operand at that level. If an operand is itself a compound expression, keep its parentheses and repeat the transformation there. This is a recursive operation, not a global exchange of every symbol at once.
>
> For a NAND implementation, the output is the complement of a product. Its equivalent negative-OR symbol has complemented inputs. The gate body and bubbles must change together; moving only one bubble changes the function.
>
> **Worked application.** $Y=\overline{(A+B)C}$，第一步为 $\overline{A+B}+\bar C$，第二步为 $\bar A\bar B+\bar C$。A=0,B=1,C=1 时原式0，正确式0；错误式 $\bar A+\bar B+\bar C$ 却为1。
>
> **English exam question:** Does the dual of an expression equal its complement?
>
> **Answer:** Generally no. Duality exchanges the operations and constants but leaves each literal unchanged. Complementation must invert the literals under DeMorgan's laws. Use [[Boolean Algebra and Circuit Models#3 · Boolean Axioms and Laws and Rules of Boolean Algebra · 运算规则|Boolean Axioms]] for that distinction and [[Universal Gates and Bubble Pushing]] to carry the algebra into a gate diagram.

## 5 · Proof by Perfect Induction · 穷举与代数验证

完全归纳／穷举证明 (proof by perfect induction) 比较 n 变量全部 $2^n$ 行。找到一行不同即可反驳等价；选几个示例一致不能证明全部。代数证明则逐步注明所用规则。

> [!IMPORTANT] 三个边界
> 对偶不等于取补；逻辑等价不等于电压／时序等价；布尔方程有解不等于任意反馈连接都满足组合构成规则。

下一步用 [[Boolean Forms and Algebraic Simplification 1]] 统一函数形式，再用 [[Karnaugh Map Minimization]] 减少实现代价。

> [!example]- Proof by Perfect Induction · 推导与例题
> **Derivation · 推导过程**
>
> **1. Method 1 的流程**
>
> 1. 数变量：$n$ 个 → 准备 $2^n$ 行。
> 2. 按二进制顺序（$00,01,10,11$）填输入列。
> 3. 分别算出等号左边与右边的中间量。
> 4. 逐行比较：**只要有一行不等，等式就被推翻**；全部 $2^n$ 行都相等，等式成立。
>
> **2. Method 2 的流程**
>
> 1. 挑选"更复杂"的那一侧作为起点（把它往简单的一侧改）。
> 2. 每一步只做一件事：提取公因子、吸收、用 $A+\bar A=1$、消双重否定……
> 3. 每步在右边写清楚用了哪条规则（讲义 p.32 的写法规范）。
> 4. 当两侧形状一致时收工；如果两边都难改，可以**两边同时化简到同一个中间式**。
> 5. 收尾用 Method 1 抽查（或全查）一次，防止中途抄错符号。
>
> **3. 什么时候用哪一种**
>
> | 情形 | 建议方法 | 原因 |
> |---|---|---|
> | 变量数 $\le 3$（4–8 行） | Method 1 穷举 | 行数少、无需记规则、几乎不可能出错 |
> | 变量数 $\ge 5$ | Method 2 代数 | $2^n$ 行爆炸（32 行以上），代数只要几步 |
> | 需要证明的是"化简结果对不对" | Method 1 抽查关键行 + 全查 | 化简容易抄错横线，逐行比对最可靠 |
> | 证明的是**规则本身**（如 Rule 10–12） | 两种都用 | 穷举说明"是什么"，代数说明"为什么"（讲义 p.22–27 正是这么做的） |
> | 式子里有大量重复结构 | Method 2 代数 | 提取公因子能一次消掉一片 |
>
> ![[perfect-induction-rule10.svg]]
> *图 1 — Rule 10（$A+AB=A$）的两种证法并排。(a) 完全归纳法：4 行穷举，第 4 列与第 5 列逐行相同，
> 于是 $A+AB=A$；(b) 代数法：$A+AB=A\cdot1+AB=A(1+B)=A\cdot1=A$，每一步标注所用规则。
> 两种证法得到同一个结论 —— 左图回答"每一行都对吗"，右图回答"为什么必然对"。*
>
> **Worked Example · 例题**
>
> **Example 1 — Rule 10：$A+AB=A$（讲义 p.22–23）**
>
> **Method 1（perfect induction，4 行）**：
>
> | $A$ | $B$ | $AB$ | $A+AB$ | $A$ | 比较 |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | ✓ |
> | 0 | 1 | 0 | 0 | 0 | ✓ |
> | 1 | 0 | 0 | 1 | 1 | ✓ |
> | 1 | 1 | 1 | 1 | 1 | ✓ |
>
> 4 行全等 → $A+AB=A$ ✓（这就是图 1(a)）。
>
> **Method 2（代数）**：
>
> $$
> \begin{aligned}
> A+AB&=A\cdot1+AB &&\text{Rule 2 反向：}A=A\cdot1\\
> &=A(1+B) &&\text{分配律反向（提取 }A\text{）}\\
> &=A\cdot1 &&\text{Rule 3：}1+B=1\\
> &=A &&\text{Rule 2：}A\cdot1=A
> \end{aligned}
> $$
>
> **数值校验 (Numerical check)**：把代数证明的每一步单独对 4 行枚举 ——
> $A\cdot1+AB$ 与 $A+AB$ 4 行全等 ✓；$A(1+B)$ 与 $A\cdot1+AB$ 4 行全等 ✓；$A\cdot1$ 与 $A(1+B)$ 4 行全等 ✓。
> 每一步都是恒等式，串起来就得到整条证明 ✓。
>
> - 直觉：$A=1$ 时两项都是 1，$A+AB=1$；$A=0$ 时两项都是 0。**$B$ 根本不影响结果** —— 这就是"吸收"。
>
> **Example 2 — Rule 11：$A+\bar AB=A+B$（讲义 p.24–25）**
>
> **Method 1（perfect induction，4 行）**：
>
> | $A$ | $B$ | $\bar A$ | $\bar AB$ | $A+\bar AB$ | $A+B$ | 比较 |
> |---|---|---|---|---|---|---|
> | 0 | 0 | 1 | 0 | 0 | 0 | ✓ |
> | 0 | 1 | 1 | 1 | 1 | 1 | ✓ |
> | 1 | 0 | 0 | 0 | 1 | 1 | ✓ |
> | 1 | 1 | 0 | 0 | 1 | 1 | ✓ |
>
> **Method 2（代数，用 Rule 12 反向）**：
>
> $$
> \begin{aligned}
> A+\bar AB&=(A+\bar A)(A+B) &&\text{Rule 12 反向：}X+YZ=(X+Y)(X+Z)\\
> &=1\cdot(A+B) &&\text{Rule 7：}A+\bar A=1\\
> &=A+B &&\text{Rule 2：}1\cdot X=X
> \end{aligned}
> $$
>
> **数值校验 (Numerical check)**：对 4 行分别验证每一步 ——
> $(A+\bar A)(A+B)$ 与 $A+\bar AB$：$A=0,B=1$ 时左边 $(0+1)(0+1)=1$、右边 $0+1\cdot1=1$ ✓；
> $A=1,B=0$ 时左边 $(1+0)(1+0)=1$、右边 $1+0\cdot0=1$ ✓。其余两行 0、1 同样吻合 ✓。
> 第二步 $1\cdot(A+B)$ 第三步 $A+B$ 分别是 Rule 7 与 Rule 2，逐行代入也成立 ✓。
>
> - 直觉：$A=0$ 时第一项消失，式子退化成 $\bar AB=B$；$A=1$ 时结果本来就是 1，与 $A+B$ 一致 ——
>   所以 $\bar A$ 这个条件可以**省掉**。
>
> **Example 3 — Rule 12：$(A+B)(A+C)=A+BC$（讲义 p.26–27）**
>
> **Method 1（perfect induction，$2^3=8$ 行）**：
>
> | $A$ | $B$ | $C$ | $A+B$ | $A+C$ | $(A+B)(A+C)$ | $A+BC$ | 比较 |
> |---|---|---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ✓ |
> | 0 | 0 | 1 | 0 | 1 | 0 | 0 | ✓ |
> | 0 | 1 | 0 | 1 | 0 | 0 | 0 | ✓ |
> | 0 | 1 | 1 | 1 | 1 | 1 | 1 | ✓ |
> | 1 | 0 | 0 | 1 | 1 | 1 | 1 | ✓ |
> | 1 | 0 | 1 | 1 | 1 | 1 | 1 | ✓ |
> | 1 | 1 | 0 | 1 | 1 | 1 | 1 | ✓ |
> | 1 | 1 | 1 | 1 | 1 | 1 | 1 | ✓ |
>
> 8 行全等 → 等式成立 ✓。注意 $A=1$ 的 4 行两边都是 1，$A=0$ 的 4 行两边都等于 $BC$ ——
> 这正是"$A$ 为真时整式恒真，否则看 $BC$"的另一种读法。
>
> **Method 2（代数，展开后吸收）**：
>
> $$
> \begin{aligned}
> (A+B)(A+C)&=AA+AC+AB+BC &&\text{分配律（逐项相乘）}\\
> &=A+AC+AB+BC &&\text{Rule 6：}AA=A\\
> &=A(1+C+B)+BC &&\text{分配律反向（把前 3 项里的 }A\text{ 提出来）}\\
> &=A\cdot1+BC &&\text{Rule 3：}1+C+B=1\\
> &=A+BC &&\text{Rule 2：}A\cdot1=A
> \end{aligned}
> $$
>
> **数值校验 (Numerical check)**：分步枚举 8 行 ——
> $AA+AC+AB+BC$ 与 $(A+B)(A+C)$ 8 行全等 ✓；$A+AC+AB+BC$ 与上一步 8 行全等（只用了 $AA=A$）✓；
> $A(1+C+B)+BC$ 与 $A+AC+AB+BC$ 8 行全等 ✓；最后 $A\cdot1+BC=A+BC$ ✓。
> 例：$A=0,B=1,C=1$ → 展开式 $0+0+0+1=1$，右式 $0+1=1$ ✓；$A=1,B=0,C=0$ → $1+0+0+0=1$，右式 $1+0=1$ ✓。
>
> **Example 4 — 该用哪一种？（自算的判断练习）**
>
> 题目：分别选择方法并说明理由。
> (a) 证明 $\bar{\bar A}=A$；(b) 证明 $WXYZ+\bar WXYZ=XYZ$；(c) 证明 $A+\bar AB=A+B$。
>
> 解：
>
> - (a) 1 个变量 → **Method 1**，2 行：$A=0\to\bar{\bar0}=\bar1=0$ ✓；$A=1\to\bar{\bar1}=\bar0=1$ ✓。也可以直接引 Rule 9。
> - (b) 4 个变量 → 16 行太多，用 **Method 2**：$WXYZ+\bar WXYZ=XYZ(W+\bar W)=XYZ\cdot1=XYZ$
>   （分配律反向 + Rule 7 + Rule 2），3 步搞定。
> - (c) 2 个变量 → 两者都行；讲义 p.24–25 用的是 Method 2（3 步），但 4 行穷举同样可以（Example 2）。
>
> **数值校验 (Numerical check)**：(b) 用 16 行枚举验证 $WXYZ+\bar WXYZ$ 与 $XYZ$ 全等 ✓；
> (a) 2 行 ✓；(c) 见 Example 2 的 4 行表 ✓。
>
> **Exhaustive proof and counterexamples · 穷举证明与反例**
>
> For n independent Boolean inputs, a complete truth table contains 2^n rows. Comparing both expressions on all rows proves equivalence over that domain. Checking only the rows where one expression is one does not establish that the other expression has no additional ON rows.
>
> One mismatching row is enough to disprove an identity. It is useful to test all-zero, all-one, and boundary rows first, but those quick checks cannot replace the full proof when they pass. For a design with don't-cares, compare only the explicitly specified rows and state that limited domain.
>
> **Worked application.** 声称 $AB+AC=A(B+C)$，四个变量组合类别由 A决定：A=0 时两侧0；A=1 时两侧B+C。也可列8行。声称 $A+B=AB$ 则在 A=1,B=0 得1≠0，一行反例足够否定。
>
> **English exam question:** Can exhaustive testing of one-step state equations verify a long state sequence?
>
> **Answer:** If every state-input pair matches the specified transition and output tables, repeated application preserves the specified behavior from a defined initial state. Initialization and unreachable-state policy still need checking. This connects the method to [[Counter Design and Digital Clocks#2 · Synchronous Counter Design · 从转换表求激励|Synchronous Counter Design]], [[Finite State Machine Design and Applications#4 · Sequence Detector · 最长可复用后缀|Sequence Detector]], and [[VHDL Modeling and Verification#4 · Testbench and Functional Verification · 规范作为独立参照|Testbench and Functional Verification]].

## Sources · 课件依据

主线课件：[Ch4 lecture](../ECE2050-Chap4.pdf)。正文的讲义页码保留原编号；自算例题另行标注。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
