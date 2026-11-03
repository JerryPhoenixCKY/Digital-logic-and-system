---
tags:
  - ECE2050
  - combinational-blocks
date: 2026-09-30
aliases:
  - 编码器与优先编码器
  - Encoder and Priority Encoder
  - Priority encoding
---

# Encoder and Priority Encoder · 编码器与优先编码器

> [!SUMMARY] Quick recall · 英文速览
> An ordinary encoder assumes one active input. A priority encoder selects the highest-priority active input even when several are asserted. A valid output distinguishes no request from request zero.

## Core Definition · 核心定义

编码器 (encoder) 将 one-hot 的输入线路转为紧凑 binary code。4-to-2 编码器输入 $D_0\ldots D_3$，输出 $Y_1Y_0$。普通编码器需约定同时最多一个输入为 1；优先编码器取消这个限制，但必须给出 priority order。

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

[[Decoder]], [[Karnaugh Map with Don't Cares]], [[Universal Gates and Bubble Pushing]], [[Shift Registers]], [[Magnitude Comparator]].

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
