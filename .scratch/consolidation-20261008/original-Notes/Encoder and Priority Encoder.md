---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
updated: 2026-10-08
aliases:
  - 编码器与优先编码器
  - Encoder and Priority Encoder
  - Priority encoding
  - Priority Circuit
  - 优先电路
---

# Encoder and Priority Encoder · 编码器与优先编码器

> [!SUMMARY] Quick recall · 英文速览
> An ordinary encoder assumes one active input. A priority encoder selects the highest-priority active input even when several are asserted. A valid output distinguishes no request from request zero.

## Core Definition · 核心定义

编码器 (encoder) 将独热 (one-hot) 输入线路转为紧凑的二进制码 (binary code)。4-to-2 编码器输入 $D_0\ldots D_3$，输出 $Y_1Y_0$。普通编码器需约定同时最多一个输入为 1；优先编码器 (priority encoder) 取消这个限制，但必须给出优先级顺序 (priority order)。所有输入、输出与有效指示均为无量纲的 0/1；本篇默认高有效、稳态组合逻辑。

## Derivation · 推导

普通 one-hot 情况：$Y_1=D_2+D_3$，$Y_0=D_1+D_3$。若 D1=D2=1，会输出 11，错误地像 D3；因此 one-hot 假设不可省略。

取 D3 最高优先、高有效。先生成获胜线路：

$$W_3=D_3,\ W_2=\bar D_3D_2,\ W_1=\bar D_3\bar D_2D_1,\ W_0=\bar D_3\bar D_2\bar D_1D_0.$$
$$Y_1=D_3+D_2,\qquad Y_0=D_3+\bar D_2D_1,\qquad V=D_3+D_2+D_1+D_0.$$

Notice that the output code is different from the winner mask. The W signals are one-hot; the Y signals encode the index. V specifies whether the code represents an actual request.

| Inputs $D_3D_2D_1D_0$ | Code | V |
|---|---|---|
| 1XXX | 11 | 1 |
| 01XX | 10 | 1 |
| 001X | 01 | 1 |
| 0001 | 00 | 1 |
| 0000 | 00 by convention | 0 |

X here means that a lower-priority input cannot change the result. It does not mean the physical input must be electrically unknown.

## Priority Circuit Versus Priority Encoder · 优先电路与编码输出，Ch5 p.20–22

课件输入名是 $A_3A_2A_1A_0$，输出名是 $Y_3Y_2Y_1Y_0$。它要求 “Output asserted corresponding to most significant TRUE input”，因此这四位输出是**独热获胜掩码 (one-hot winner mask)**。为避免与本篇二位编码输出 $Y_1Y_0$ 混淆，以下用 $D_i$ 对应课件 $A_i$，用 $W_i$ 对应课件 $Y_i$。

| $D_3D_2D_1D_0$ | Winner mask $W_3W_2W_1W_0$ | Binary code $Y_1Y_0$ | $V$ |
|---|---|---|---|
| 0000 | 0000 | 00 | 0 |
| 0001 | 0001 | 00 | 1 |
| 0010 | 0010 | 01 | 1 |
| 0011 | 0010 | 01 | 1 |
| 0100 | 0100 | 10 | 1 |
| 0101 | 0100 | 10 | 1 |
| 0110 | 0100 | 10 | 1 |
| 0111 | 0100 | 10 | 1 |
| 1000 | 1000 | 11 | 1 |
| 1001 | 1000 | 11 | 1 |
| 1010 | 1000 | 11 | 1 |
| 1011 | 1000 | 11 | 1 |
| 1100 | 1000 | 11 | 1 |
| 1101 | 1000 | 11 | 1 |
| 1110 | 1000 | 11 | 1 |
| 1111 | 1000 | 11 | 1 |

Two invariants make the winner equations easy to verify: at most one $W_i$ is 1, and $W_3+W_2+W_1+W_0=V$. Each lower winner includes complements of every higher input, so a higher request suppresses all lower requests.

从获胜线路编码可得到前面的紧凑式：

$$
\begin{aligned}
Y_1&=W_3+W_2=D_3+D_2,\\
Y_0&=W_3+W_1=D_3+\bar D_2D_1.
\end{aligned}
$$

例如 1011 应获胜于 D3：课件输出为 1000，编码输出为 11；两者表达同一个选择结果，但格式不同。

### Input X Versus Output Don't-Care · 输入压缩与输出无关项

课件 p.22 把 16 行压缩为 $0000\to0000$、$0001\to0001$、$001X\to0010$、$01XX\to0100$、$1XXX\to1000$。输入端 X 是“任意取值仍给相同输出”，一行分别代表 1、1、2、4、8 种输入，共 16 种。

Those X symbols compact an already complete truth table. The outputs remain specified for all sixteen patterns. They do not justify turning multiple-request cases into output don't-cares for K-map minimization.

另一个设计若明确声明 all-zero 时位置码不被使用，且使用者受有效指示 (valid indicator) V 控制，则该行的 **code 输出**可另行指定为无关项；这属于新规范，不能由 p.22 的输入 X 自动推断。通用规则见 [[Karnaugh Map with Don't Cares]]。

## Worked Examples · 例题

**Example 1.** D=0110，D2 与 D1 同时请求。W2=1，其余 0；code=10，V=1。输出不会是普通编码器的 11。

**Example 2.** D=0001 与 D=0000 都可给 code=00，但 V 分别为 1、0。没有 V 时无法区分“请求 0”和“没有请求”。

**Active-low interface.** 若外部 $\bar D_i=0$ 表示请求，先形成正逻辑 request $D_i=\overline{\bar D_i}$。如果输出也是低有效 binary code，则再取补。输入低有效与输出低有效是两个独立约定。

**Eight-to-three extension.** 最高获胜输入 $W_i=D_i\prod_{j=i+1}^{7}\bar D_j$；每个 code bit OR 所有索引该位为 1 的 W。适用于中断仲裁或按键选择。

## Pitfalls and Review · 易错点与复习

- A decoder selects a line from a code; an encoder creates a code from a line.
- 优先级不保证公平；一直存在高优先请求时，低优先可能 starvation。
- 验证重叠请求和 all-zero 情况，不能只测试 one-hot。

**Exam answer:** “The highest asserted input suppresses all lower-priority inputs. The valid signal prevents the no-input case from being confused with input zero.”

## Position codes in a scanned keyboard · 扫描键盘中的位置码

An eight-row matrix uses a three-bit row encoder and an eight-column matrix uses a three-bit column encoder. Combining the fields produces a six-bit position code, with an independent valid condition. Active-low one-cold inputs require the corresponding input polarity conversion or device model.

[[Keyboard Scanning and Encoding]] 把该组合块连接到扫描状态、debounce与load事件；编码器本身不能决定一次按下应产生几次字符。

## Connections · 相关笔记

[[Combinational Logic Design]], [[Decoder]], [[Karnaugh Map with Don't Cares]], [[Universal Gates and Bubble Pushing]], [[Shift Registers]], [[Magnitude Comparator]].

## Sources · 来源

- Tinghuan CHEN, *ECE 2050 Digital Logic and Systems, Chapter 5: Combinational Logic Design*, PDF p.20–22：优先电路、四路独热方程、完整与压缩真值表；[本地课件](../ECE2050-Chap5.pdf#page=20)。二位编码与 V 是在四路获胜模型上展开的推导，课件该例题的输出仍为四路独热。

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
