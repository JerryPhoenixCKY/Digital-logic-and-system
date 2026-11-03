# ECE2050 Ch3 + Ch4 建设规划 (BUILD PLAN) — 冻结版

> 权威清单：文件名、aliases、tags、图名、双链目标都以此为准。进度看知识树的 ✅。
> 写作规范 `.scratch/NOTE_SPEC.md`；视觉规范 `Tools/README.md`；**讲义裁剪图** `Tools/pdfcrop.py`（已登记，勿手改 PNG）。
> 素材：`.scratch/extract/ECE2050-Chap3.txt`（25 页）、`.scratch/extract/ECE2050-Chap4.txt`（63 页）。
> 页码 = 讲义页序（与 `========== PAGE n ==========` 一致）。

---

## 0. 命名、标签、配图策略

- 文件名 = **英文全称**，放 `Notes/`；`aliases` ≥3 条（中文名 + 英文全名 + 缩写/别称）。
- tags = `ECE2050` + 一个分区标签，取值仅限：
  **Ch3**：`logic-gates`（门电路）、`logic-levels`（电平 / 噪声 / VTC）
  **Ch4**：`boolean-algebra`（公理·定理·化简）、`boolean-forms`（SOP/POS/真值表）、`karnaugh-map`
- **配图策略（作者确认的混合策略，务必遵守）**：
  - **裁剪**（`Figures/ch3-*.png` / `ch4-*.png`，由 `Tools/pdfcrop.py` 生成）：讲义里的**符号块、器件总表、例题图**
    —— 嵌入写 `![[ch3-two-input-gates.png]]`，图注必须写清"讲义 p.N 原图"。
  - **重画 SVG**（`Tools/figures/<name>.py` → `Figures/<name>.svg`）：凡是**需要推导、精确标注或轴刻度**的图
    —— 时序图、逻辑电平区间、噪声容限、VTC 曲线、卡诺图圈组、门级等价。
  - 真值表一律用 **Markdown 表格**（既不裁剪也不画图）。
- 已登记的裁剪图（**可直接嵌入，不要重新裁剪**）：
  `ch3-inverter-symbol`(p.4) `ch3-single-input-gates`(p.5) `ch3-xor-xnor`(p.10) `ch3-xor-adder`(p.11)
  `ch3-two-input-gates`(p.12) `ch3-multiple-input-gates`(p.13)
  `ch4-combinational-nodes`(p.5) `ch4-kmap-3var-basic`(p.50) `ch4-kmap-3var-example`(p.51)
  `ch4-kmap-4var`(p.52) `ch4-kmap-pos-example`(p.55) `ch4-kmap-pos-to-sop`(p.56)
  `ch4-kmap-dont-care`(p.59) `ch4-seven-segment-kmap`(p.61)
- 白名单（只能链接这些）：Ch2 的 18 篇 + 本文件下面 25 篇 + `ECE2050 Knowledge Tree` + `Glossary`。
  尚未建的概念写纯文本（例：`shift register（Ch8 内容）`）。

---

## Ch3 · Logic Gates（讲义 25 页）

### 3-01 | Logic Gates
- file `Notes/Logic Gates.md` · aliases `逻辑门` / `门电路` / `Logic Gates` / `Logic Gate`
- tags `ECE2050`,`logic-gates` · must-cover：门的定义（执行逻辑函数 inversion/AND/OR/NAND/NOR…）；
  单输入（NOT、BUF）vs 两输入/多输入（AND、OR、XOR、NAND、NOR、XNOR）分类（p.3）；
  **三种描述方式**（真值表 / 时序图 timing diagram / 逻辑表达式）与"$n$ 输入有 $2^n$ 种组合"（p.4,6,8）；
  标准符号（distinctive shape 与 IEEE 矩形符号）与**负逻辑/气泡**约定（p.8-9 "How to verify/prove?"）；
  表的行按二进制顺序列出（p.13）；何时用 NAND/NOR（工程上最常用）。
- 图：`logic-gate-symbols.svg`（**重画**，schemdraw：7 种门 + BUF 的标准符号与表达式各一行）+ 裁剪 `ch3-two-input-gates.png`

### 3-02 | Inverter
- file `Notes/Inverter.md` · aliases `反相器` / `非门` / `反相器与缓冲器` / `Inverter` / `NOT Gate` / `Buffer`
- tags `ECE2050`,`logic-gates` · must-cover：NOT 的符号（三角形 + 负号指示圈 negation indicator）、
  表达式 $Y=\bar A$（bar 表示 complement）；真值表 0→1、1→0；**buffer**（非反相，为什么需要：驱动/整形）；
  时序图怎么看（输入/输出沿对齐，传播延迟概念，标注为延伸）；p.5 的 NOT/BUF 对照表；T/F 题：NOT 只能单输入。
- 图：`inverter-timing.svg`（重画，matplotlib：A 与 Y 的时序，含理想零延迟 vs 有延迟两条）+ 裁剪 `ch3-single-input-gates.png`

### 3-03 | AND Gate
- file `Notes/AND Gate.md` · aliases `与门` / `AND 门` / `AND Gate` / `AND Operation`
- tags `ECE2050`,`logic-gates` · must-cover：输出为 1 **当且仅当所有输入为 1**；表达式 $Y=AB$；
  两输入真值表（4 行）与"全 1 才出 1"；$n$ 输入 $2^n$ 行，AND3 例（p.13，$Y=ABC$）；
  时序图（任一输入为 0 → 输出 0 的"门控"直觉）；p.12 汇总图中 AND 的位置。
- 图：`and-gate-timing.svg`（重画）+ 裁剪 `ch3-two-input-gates.png`（与 3-01 共用，图注按 AND 写）

### 3-04 | OR Gate
- file `Notes/OR Gate.md` · aliases `或门` / `OR 门` / `OR Gate` / `OR Operation`
- tags `ECE2050`,`logic-gates` · must-cover：任一输入为 1 则输出 1（$Y=A+B$）；真值表；
  T/F 题陷阱："OR 的某个输入为 0 输出就为 0"是**错的**；时序图；OR3。
- 图：`or-gate-timing.svg`（重画）+ 裁剪 `ch3-two-input-gates.png`

### 3-05 | NAND Gate
- file `Notes/NAND Gate.md` · aliases `与非门` / `NAND 门` / `NAND Gate` / `NAND Operation`
- tags `ECE2050`,`logic-gates` · must-cover：NAND = AND + inverter（气泡即取反）；
  表达式 $Y=\overline{AB}$；真值表（只有全 1 时输出 0）；NAND3（p.13）；时序图 = AND 的反相；
  **注意 DeMorgan 的关系**（链 [[DeMorgan's Theorems]]，指向 Ch4）；工程意义（CMOS 里最便宜的门，纯文本提"通用门见 Ch5"）。
- 图：`nand-gate-timing.svg`（重画）+ 裁剪 `ch3-multiple-input-gates.png`

### 3-06 | NOR Gate
- file `Notes/NOR Gate.md` · aliases `或非门` / `NOR 门` / `NOR Gate` / `NOR Operation`
- tags `ECE2050`,`logic-gates` · must-cover：NOR = OR + inverter；$Y=\overline{A+B}$；真值表（只有全 0 时输出 1）；
  时序图 = OR 的反相；与 NAND 的对称性；T/F 题。
- 图：`nor-gate-timing.svg`（重画）+ 裁剪 `ch3-two-input-gates.png`

### 3-07 | Exclusive-OR Gate
- file `Notes/Exclusive-OR Gate.md` · aliases `异或门` / `XOR 门` / `异或` / `Exclusive-OR Gate` / `XOR Gate`
- tags `ECE2050`,`logic-gates` · must-cover：$Y=A\oplus B=A\bar B+\bar AB$；真值表（不同为 1）；
  **奇数个 1 → 1**（多输入 XOR3 奇校验，p.13 表格要逐行核对）；时序图；
  **应用：XOR 可以"把两个比特相加"**（p.11，sum 位；进位由 AND 给出 → 半加器，链 [[AND Gate]]）。
- 图：`xor-gate-timing.svg`（重画）＋ `xor-half-adder.svg`（重画，schemdraw：A、B → XOR 得 Sum、AND 得 Carry）＋ 裁剪 `ch3-xor-xnor.png`、`ch3-xor-adder.png`

### 3-08 | Exclusive-NOR Gate
- file `Notes/Exclusive-NOR Gate.md` · aliases `同或门` / `XNOR 门` / `同或` / `Exclusive-NOR Gate` / `XNOR Gate`
- tags `ECE2050`,`logic-gates` · must-cover：XNOR = XOR 的反相，$Y=\overline{A\oplus B}$；
  **相等检测器**（两输入相同 → 1）；真值表；时序图（与 XOR 互补）；多输入时的"偶数个 1"规律；
  T/F 题："XOR 在两个输入相反时输出 0"是**错的**（那是不同→1）。
- 图：`xnor-gate-timing.svg`（重画）+ 裁剪 `ch3-xor-xnor.png`

### 3-09 | Logic Levels
- file `Notes/Logic Levels.md` · aliases `逻辑电平` / `逻辑电平与电压范围` / `Logic Levels` / `Logic Level`
- tags `ECE2050`,`logic-levels` · must-cover：用**离散电压**表示 1/0（如 0 V 与 $V_{DD}$，p.15）；
  "4.99 V 是 1 还是 0？"→ 需要**电压范围**而非单点（p.16）；输入/输出用**不同**范围以容忍噪声；
  四个关键参数 $V_{IL}$、$V_{IH}$、$V_{OL}$、$V_{OH}$ 的定义与方向（p.18）；
  **$V_{DD}$ 缩放**（p.21-22）：从 5 V 一路降到 3.3/2.5/1.8/1.5/1.2/1.0 V，原因 = 防止烧毁微小晶体管 + 省功耗；
  不同供电电压的芯片互连要注意（电平不兼容）。
- 图：`logic-level-ranges.svg`（重画，matplotlib：一条竖直电压轴，标出 $V_{OL}/V_{IL}$ 与 $V_{IH}/V_{OH}$ 的
  过渡带，并用 p.23 的 TTL/CMOS 实测数值画两个实例区间）

### 3-10 | Noise Margin
- file `Notes/Noise Margin.md` · aliases `噪声容限` / `噪声裕度` / `Noise Margin` / `Noise Margins`
- tags `ECE2050`,`logic-levels` · must-cover：**噪声的定义**（任何使信号退化的东西：电阻、电源噪声、
  邻线耦合，p.17 的例子 5 V→4.5 V）；两个指标：

$$NM_H=V_{OH}-V_{IH},\qquad NM_L=V_{IL}-V_{OL}$$

  物理意义（输出保证的最差高电平与接收端要求的最低高电平之差 = 还能容忍多少噪声）；
  **数值校验**：用 p.23 表格算 TTL（$2.4-2.0=0.4$ V、$0.8-0.4=0.4$ V）、CMOS（$3.84-3.15=0.69$、$1.35-0.33=1.02$）、
  LVTTL（$0.4$、$0.4$）、LVCMOS（$2.7-1.8=0.9$、$0.9-0.36=0.54$）；为什么 $NM_H$ 与 $NM_L$ 都要看。
- 图：`noise-margin.svg`（重画，matplotlib：把 $V_{OH}/V_{IH}/V_{IL}/V_{OL}$ 画成同一电压轴上的四条线，
  阴影标出 $NM_H$ 与 $NM_L$ 两个区间，并标注 TTL 的具体数值）

### 3-11 | DC Transfer Characteristic
- file `Notes/DC Transfer Characteristic.md` · aliases `直流传输特性` / `电压传输特性` / `DC Transfer Characteristic` / `VTC`
- tags `ECE2050`,`logic-levels` · must-cover：VTC = $V_{out}$ 对 $V_{in}$ 的曲线（p.19-20）；
  **理想缓冲器**是阶跃、$NM_H=NM_L=V_{DD}/2$；**实际缓冲器**有过渡区，$NM_H+NM_L=V_{DD}$ 且每个都 $<V_{DD}/2$；
  实际反相器的 VTC（输出反相、有增益区与两个饱和区）；开关阈值 $V_M$ 与增益的关系（陡 → 噪声容限大）；
  与 [[Noise Margin]] 的关系：$NM$ 就是 VTC 上的水平"水平余量"；$V_{DD}$ 缩放对 VTC 的影响。
- 图：`dc-transfer-buffer.svg`（重画，matplotlib：双面板 (a) 理想缓冲器阶跃 + (b) 实际缓冲器，
  标出 $V_{IL}/V_{IH}/V_{OL}/V_{OH}$ 与 $NM$ 区间）+ `dc-transfer-inverter.svg`（可选：反相器 VTC 与 $V_M$）

---

## Ch4 · Boolean Algebra and Logic Simplification（讲义 63 页）

### 4-01 | Combinational Circuit
- file `Notes/Combinational Circuit.md` · aliases `组合电路` / `组合逻辑电路` / `Combinational Circuit` / `Combinational Logic`
- tags `ECE2050`,`boolean-algebra` · must-cover：逻辑电路的四个要素（inputs / outputs / functional spec / timing spec，p.4）；
  **节点分类**（输入节点 A,B,C、输出节点 Y,Z、内部节点 n1）与电路元件 E1…En（p.5）；
  **组合 vs 时序**（memoryless vs 有记忆，输出只由当前输入决定 vs 还取决于历史状态，p.6）；
  **组合电路的三条构成规则**（每个元件都是组合的、每个节点要么是输入要么只接一个输出、无环路，p.7）；
  违反规则的例子（短接两个输出会怎样）。
- 图：裁剪 `ch4-combinational-nodes.png`（讲义 p.5 原图）+ `combinational-rules.svg`（重画，schemdraw：合法 vs 非法构成的对照小电路）

### 4-02 | Boolean Equation
- file `Notes/Boolean Equation.md` · aliases `布尔方程` / `布尔表达式` / `Boolean Equation` / `Boolean Expression`
- tags `ECE2050`,`boolean-algebra` · must-cover：布尔方程 = 用输入表达输出的**功能规范**（p.9）；
  p.9 的加法器例：$S=A\oplus B\oplus C_{in}$、$C_{out}=AB+AC_{in}+BC_{in}$（逐项解释：两个/三个 1 时进位）；
  **从文字到方程** 5 个例子（p.10-14）：$P=R\bar S$、$W=M+N$、$E=M+CT\bar X$、$E=HS+H$、$E=HS+H\bar S$；
  重点讲清"and→乘、or→加、not→取反"的映射与括号优先级；最后一例可化简为 $H$（链 [[Laws and Rules of Boolean Algebra]]）。
- 图：`boolean-expression-from-words.svg`（重画，matplotlib：把 5 个文字例子与方程并排成表格式图）
  或纯 Markdown 表格 + 裁剪 `ch4-combinational-nodes.png`（若要图）

### 4-03 | Boolean Axioms
- file `Notes/Boolean Axioms.md` · aliases `布尔公理` / `布尔代数公理` / `Boolean Axioms` / `Axioms of Boolean Algebra`
- tags `ECE2050`,`boolean-algebra` · must-cover：变量只有 0/1 两个值 → 比普通代数简单（p.16）；
  **对偶性 (duality)**：AND↔OR、0↔1 互换得到对偶式（p.16-17）；
  A1（$B=0$ iff $B\ne1$）、A2（$0'=1$、$1'=0$）、A3（$0\cdot0=0$ / $1+1=1$）、
  A4（$1\cdot1=1$ / $0+0=0$）、A5（$0\cdot1=1\cdot0=0$ / $1+0=0+1=1$）；
  每条给出"为什么"与"对偶式怎么写"；**自检题**：写出任意一条的对偶。
- 图：无（Markdown 表格 + Mermaid 对偶操作示意即可）

### 4-04 | Laws and Rules of Boolean Algebra
- file `Notes/Laws and Rules of Boolean Algebra.md` · aliases `布尔代数定律与规则` / `布尔代数规则` / `Laws of Boolean Algebra` / `Rules of Boolean Algebra`
- tags `ECE2050`,`boolean-algebra` · must-cover：**三条定律**（交换 $A+B=B+A$、$AB=BA$；
  结合 $A+(B+C)=(A+B)+C$；分配 $A(B+C)=AB+AC$，p.19）；
  **12 条常用规则**（Floyd 编号，逐条给式子 + 对偶式 + 直觉/一句证明要点）：
  $A+0=A$、$A\cdot1=A$、$A+1=1$、$A\cdot0=0$、$A+A=A$、$A\cdot A=A$、$A+\bar A=1$、$A\bar A=0$、
  $\bar{\bar A}=A$、$A+AB=A$、$A+\bar AB=A+B$、$(A+B)(A+C)=A+BC$；
  强调第 10–12 条是**化简的主力**；布尔加法 ≠ 算术加法（$1+1=1$）。
- 图：`boolean-rules-table.svg`（重画，matplotlib：12 条规则的对偶对照卡片）或纯 Markdown 表格（二选一，
  推荐 Markdown 表格 + 一张"对偶"示意）

### 4-05 | Proof by Perfect Induction
- file `Notes/Proof by Perfect Induction.md` · aliases `完全归纳法` / `穷举证明` / `Perfect Induction` / `Proof by Exhaustion`
- tags `ECE2050`,`boolean-algebra` · must-cover：两种证明方法（p.20）：① perfect induction（穷举所有输入组合）；
  ② 用其它公理/定理把一个式子化成另一个；
  **Rule 10 的两种证法**（$A+AB=A$：真值表穷举 + 代数 $A(1+B)=A\cdot1=A$，p.22-23）；
  **Rule 11**（$A+\bar AB=A+B$：代数 $A+\bar AB=(A+\bar A)(A+B)=1\cdot(A+B)$，用 Rule 12，p.24-25）；
  **Rule 12**（$(A+B)(A+C)=A+BC$：展开 $AA+AC+AB+BC$，p.26-27）；
  何时用哪种（变量少 → 穷举；变量多 → 代数）。
- 图：`perfect-induction-rule10.svg`（重画，matplotlib：Rule 10 的真值表穷举 + 代数推导两条并排）

### 4-06 | DeMorgan's Theorems
- file `Notes/DeMorgan's Theorems.md` · aliases `德摩根定理` / `德摩根定律` / `DeMorgan's Theorems` / `De Morgan's Law`
- tags `ECE2050`,`boolean-algebra` · must-cover：两条定理

$$\overline{XY}=\bar X+\bar Y,\qquad \overline{X+Y}=\bar X\bar Y$$

  读法（"断开长横线并把符号反过来"）；**门级含义**：NAND ↔ 反相输入的 OR、NOR ↔ 反相输入的 AND；
  用 perfect induction 各证一遍；多变量推广 $\overline{XYZ}=\bar X+\bar Y+\bar Z$；
  **应用**：把 NAND/NOR 电路转成 AND/OR 形式、求反函数（SOP ↔ POS 的桥梁，链 [[Sum-of-Products Form]]、[[Product-of-Sums Form]]）；
  坑：只对**最外层**取反时不能逐项变号；与 [[NAND Gate]]、[[NOR Gate]] 的对应关系。
- 图：`demorgan-gate-equivalence.svg`（重画，schemdraw：左边 NAND，右边 OR+气泡输入，中间等号）

### 4-07 | Boolean Expression Simplification
- file `Notes/Boolean Expression Simplification.md` · aliases `布尔代数化简` / `逻辑表达式化简` / `Boolean Expression Simplification` / `Logic Simplification`
- tags `ECE2050`,`boolean-algebra` · must-cover：用公理与定理逐步化简的**写法规范**（每一步右侧标注所用规则，p.32）；
  讲义四例（p.31-33）逐步走完并给数值校验：
  ① $Y=A\bar B+\bar AB$ → $B$（$(\bar A+A)B$，用 Rule 12/7）；
  ② $Y=A\bar BC+A\bar BC+A\bar BC$ → $AC+BC$（补项技巧）；
  ③ $AB+\bar AB+C+B(B+C)$ → $AC+B$（Rule 5/7/10）；
  ④ $BC+BD+CD$ → $BC+BD$（用 $CD(B+\bar B)$ 补项消去 $CD$）；
  化简的意义（门数/延迟/功耗 ↓）；何时该停（与卡诺图的关系，链 [[Karnaugh Map]]）。
- 图：`simplification-example4.svg`（重画，matplotlib：例④的分步推导 + 每一步用到的规则）

### 4-08 | Minterm and Maxterm
- file `Notes/Minterm and Maxterm.md` · aliases `最小项与最大项` / `最小项` / `最大项` / `Minterm and Maxterm` / `Minterm` / `Maxterm`
- tags `ECE2050`,`boolean-algebra` · must-cover：五个术语的定义（p.35）：complement（带横线的变量）、
  literal（变量或其反）、implicant（literal 的乘积）、**minterm**（含全部输入变量的乘积，$m_i$）、
  **maxterm**（含全部输入变量的和，$M_i$）；
  编号规则（minterm：变量取 1 记 1、取 0 记 0，如 $\bar A\bar B=m_0$；maxterm 恰好相反）；
  **互补关系**：$M_i=\bar m_i$；每个 minterm 只在一行取 1、每个 maxterm 只在一行取 0；
  2 变量与 3 变量的完整 m/M 表。
- 图：`minterm-maxterm-table.svg`（重画，matplotlib：2/3 变量的 minterm 与 maxterm 对照表）

### 4-09 | Sum-of-Products Form
- file `Notes/Sum-of-Products Form.md` · aliases `与或式` / `积之和形式` / `Sum-of-Products` / `SOP Form` / `SOP`
- tags `ECE2050`,`boolean-forms` · must-cover：SOP = 乘积（AND）之和（OR）（p.36）；
  **任何布尔函数都能写成 SOP**；由真值表取**输出为 1 的行**（每行一个 minterm）再 OR；
  例：$Y=\bar A B + A\bar B$（异或的真值表）；
  **标准 SOP (standard SOP)**：每一项都含全部变量（p.40：$\bar AB C + \bar ABC D$ 补 $D+\bar D$ 的展开法）；
  判断标准 SOP 的方法；SOP 与 [[Minterm and Maxterm]] 的编号写法 $Y=\sum m(1,2)$。
- 图：`sop-from-truth-table.svg`（重画，matplotlib：真值表某一行的 minterm 高亮 → OR 成 SOP）

### 4-10 | Product-of-Sums Form
- file `Notes/Product-of-Sums Form.md` · aliases `或与式` / `和之积形式` / `Product-of-Sums` / `POS Form` / `POS`
- tags `ECE2050`,`boolean-forms` · must-cover：POS = 和（OR）之积（AND）（p.37）；
  由真值表取**输出为 0 的行**（每行一个 maxterm，变量取 0 写原变量、取 1 写反变量）再 AND；
  标准 POS 与补变量的方法（$A+\bar B+ C=(A+\bar B+C+D\bar D)$ 展开，p.41 用 Rule 12）；
  POS 与 SOP 的**同一性**验证（p.39 的午餐例子两种写法都得到 $E=CM$）；
  编号写法 $Y=\prod M(\dots)$。
- 图：`pos-from-truth-table.svg`（重画，matplotlib：真值表 0 行 → maxterm → AND 成 POS）

### 4-11 | Truth Table and Boolean Expression
- file `Notes/Truth Table and Boolean Expression.md` · aliases `真值表与布尔表达式` / `真值表转表达式` / `Truth Table and Boolean Expression` / `Truth Table to Expression`
- tags `ECE2050`,`boolean-forms` · must-cover：真值表 ↔ 标准 SOP/POS 的双向流程（p.43-46）；
  由标准 SOP 填真值表（$A\bar BC+\bar A\bar BC+\bar AB\bar C$ 例，逐行标 "Don't Care" 即该 minterm 为 0 的行，p.43）；
  由标准 POS 填真值表（p.44，每行 maxterm 为 1 处标 Don't Care）；
  从真值表写最小 SOP/POS（p.45-46 的 $X$ 例）；
  **检查方法**：写完后代回任意一行验证；域 (domain) 概念。
- 图：`truth-table-conversion.svg`（重画，matplotlib：SOP↔POS↔真值表的三向流程 + 一个完整例子）

### 4-12 | Karnaugh Map
- file `Notes/Karnaugh Map.md` · aliases `卡诺图` / `K 图` / `Karnaugh Map` / `K-Map`
- tags `ECE2050`,`karnaugh-map` · must-cover：定义与用途（把布尔式化成**最小** SOP/POS 的系统方法，p.48）；
  单元格 = 一种输入组合，格数 = $2^n$；**相邻格按 Gray 码编号**（相邻只变一个变量 —— 链 [[Gray Code]]）；
  3 变量（2×4）与 4 变量（4×4）的行列编号写法（`00 01 11 10`）；
  **圈组五规则**（每个 1 至少被圈一次；圈只能是水平/垂直不能对角；每圈跨度是 2 的幂；圈尽可能大；
  可以跨边界回绕，p.49）；由圈写出积项（圈内不变的变量保留、变化的变量消去）；
  3 变量例（p.50：$Y=AB+BC$）与 4 变量例（p.52：$Y=AC+ABD+ABC+BD$）。
- 图：`kmap-rules.svg`（重画，matplotlib：2×4 与 4×4 的编号布局 + 一个合法/非法圈组对照）
  + 裁剪 `ch4-kmap-3var-basic.png`、`ch4-kmap-4var.png`

### 4-13 | Karnaugh Map with Don't Cares
- file `Notes/Karnaugh Map with Don't Cares.md` · aliases `含无关项的卡诺图` / `无关项` / `Karnaugh Map with Don't Cares` / `Don't Care Conditions`
- tags `ECE2050`,`karnaugh-map` · must-cover：**don't care（X）的来源**（这些输入组合在现实中不会出现或输出无所谓）；
  规则：**只在有助于化简时才把 X 当 1 圈**（p.58）；
  例（p.59 的 4 变量表：$Y=A+BD+C$ 的化简过程逐圈说明）；
  **例题 4-32：BCD → 七段译码器**（p.60-61）：$1010$–$1111$ 六个非法 BCD 码即 X；
  段 a 的真值表与卡诺图 → $a=\bar A+C+B\bar D+\bar BD$；与 Ch2 的 [[Binary Coded Decimal]] 呼应。
- 图：`kmap-dont-care.svg`（重画，matplotlib：含 X 的 4 变量图 + 圈组高亮）+ 裁剪 `ch4-kmap-dont-care.png`、`ch4-seven-segment-kmap.png`

### 4-14 | POS Minimization with Karnaugh Map
- file `Notes/POS Minimization with Karnaugh Map.md` · aliases `卡诺图 POS 最小化` / `卡诺图求最小或与式` / `POS Minimization with Karnaugh Map` / `K-Map POS Minimization`
- tags `ECE2050`,`karnaugh-map` · must-cover：SOP 最小化圈 **1**、POS 最小化圈 **0**（p.54）；
  圈 0 后写 maxterm 的规则（圈内为 0 的变量写原变量、为 1 的写反变量，再 AND）；
  例 4-34（3 变量，$\bar AC+\bar AB=A(\bar B+\bar C)$ 等）、例 4-35（4 变量，给出的五个 maxterm）；
  **用同一张卡诺图在 POS 与 SOP 之间转换**（p.56：先填 0、再填 1、读两种最小式）；
  完整例题：给标准 POS → 最小 POS、标准 SOP、最小 SOP 三个结果（p.56 的六个 maxterm）。
- 图：`kmap-pos-minimization.svg`（重画，matplotlib：同一张 4 变量图上分别圈 0 与圈 1 的对照）
  + 裁剪 `ch4-kmap-pos-example.png`、`ch4-kmap-pos-to-sop.png`

---

## 图清单汇总

**重画 SVG（脚本 `Tools/figures/<name>.py`）**
| # | 图 | 工具 | 归属 |
|---|---|---|---|
| 1 | `logic-gate-symbols.svg` | schemdraw | 3-01 |
| 2 | `inverter-timing.svg` | matplotlib | 3-02 |
| 3 | `and-gate-timing.svg` | matplotlib | 3-03 |
| 4 | `or-gate-timing.svg` | matplotlib | 3-04 |
| 5 | `nand-gate-timing.svg` | matplotlib | 3-05 |
| 6 | `nor-gate-timing.svg` | matplotlib | 3-06 |
| 7 | `xor-gate-timing.svg` | matplotlib | 3-07 |
| 8 | `xor-half-adder.svg` | schemdraw | 3-07 |
| 9 | `xnor-gate-timing.svg` | matplotlib | 3-08 |
| 10 | `logic-level-ranges.svg` | matplotlib | 3-09 |
| 11 | `noise-margin.svg` | matplotlib | 3-10 |
| 12 | `dc-transfer-buffer.svg` | matplotlib | 3-11 |
| 13 | `combinational-rules.svg` | schemdraw | 4-01 |
| 14 | `demorgan-gate-equivalence.svg` | schemdraw | 4-06 |
| 15 | `simplification-example4.svg` | matplotlib | 4-07 |
| 16 | `minterm-maxterm-table.svg` | matplotlib | 4-08 |
| 17 | `sop-from-truth-table.svg` | matplotlib | 4-09 |
| 18 | `pos-from-truth-table.svg` | matplotlib | 4-10 |
| 19 | `truth-table-conversion.svg` | matplotlib | 4-11 |
| 20 | `kmap-rules.svg` | matplotlib | 4-12 |
| 21 | `kmap-dont-care.svg` | matplotlib | 4-13 |
| 22 | `kmap-pos-minimization.svg` | matplotlib | 4-14 |

**讲义裁剪 PNG（`Tools/pdfcrop.py` 已生成，直接嵌入）**
`ch3-inverter-symbol` `ch3-single-input-gates` `ch3-xor-xnor` `ch3-xor-adder` `ch3-two-input-gates`
`ch3-multiple-input-gates` `ch4-combinational-nodes` `ch4-kmap-3var-basic` `ch4-kmap-3var-example`
`ch4-kmap-4var` `ch4-kmap-pos-example` `ch4-kmap-pos-to-sop` `ch4-kmap-dont-care` `ch4-seven-segment-kmap`
