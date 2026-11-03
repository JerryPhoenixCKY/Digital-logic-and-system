# NOTE SPEC — ECE2050 第二章「Number Systems」专题笔记写作规范（子代理必须逐条遵守）

本库是 Obsidian 学习库（vault 根目录 = `ECE2050/`）。你要写的每一篇笔记都必须与已冻结的规划
`.scratch/PLAN-Ch2.md` 完全一致（文件名、aliases、tags、图名、双链目标）。

**绝对禁止**：修改 `Notes/ECE2050 Knowledge Tree.md`（知识树）、`Notes/Glossary.md`（术语表）、
`Tools/figstyle.py`、`Tools/check_vault.py`、`Tools/figcheck.py`、
`.scratch/PLAN-Ch2.md`、`.scratch/NOTE_SPEC.md`、以及任何**不属于你任务清单**的笔记或图文件。
你只创建/覆盖分配给你的 `Notes/*.md`、`Figures/*.svg`、`Tools/figures/*.py`。
（**固定布局**：知识树与术语表都在 `Notes/` 下，不要搬走；枢纽双链统一写文件名形式
`[[ECE2050 Knowledge Tree]]` / `[[Glossary]]`。）

---

## 0. 素材与可信来源（先读再写）

| 来源 | 用途 |
|---|---|
| `.scratch/extract/ECE2050-Chap2.txt` | 讲义正文纯文本（73 页）。用 `========== PAGE n ==========` 分隔，**n 就是讲义页序**（与页脚号一致），引用写作"讲义 p.42"。 |
| `.scratch/verify_ch2.txt` | **所有例题数字的权威来源**（已用 Python 复核）。笔记里的每个数字都必须与它一致。 |
| `.scratch/PLAN-Ch2.md` | 文件名 / aliases / tags / 图名 / must-cover 清单 / 双链白名单。 |

- 讲义抽取文本里的公式与图常被拆散、错序（例如下标掉行、`%&` 乱码）：**不要照抄乱码**，
  以 `PLAN-Ch2.md` 的 must-cover 与 `verify_ch2.txt` 为准。
- 若讲义原文与自洽性冲突（例如 p.54 的 `Q1.15 (1, -1]`、p.55 饱和加法的写法），**以自洽为准并在正文注明**，
  不要沉默地改数。
- 不要从讲义 PDF 截图、不要导出位图；所有图必须由 `Tools/figures/` 里的脚本重画。

---

## 1. 语言与风格

- 中英混排、**英文比重高**：要点词写成"中文 (English)"，例如"位权 (positional weight)"、
  "补码 (two's complement)"、"溢出 (overflow)"。标题与关键句可以直接用英文。
- 面向对象：正在学 ECE2050 的学生。写"为什么"，不只写"是什么"。
- 数学一律 LaTeX：行内 `$2^{N-1}$`，独立公式用 `$$ ... $$`。二进制/十六进制常量用 `\text{}` 或
  等宽文本写在公式外的行内代码里，例如 `1101 0110`、`0x28A`。
  **每个重要公式后面必须给**：① 一句话意义；② 数值校验（代入具体数字，写出算式与结果）。
- callout 只用这四种，且各有分工：
  - `> [!NOTE]` 定位：这篇在课程中的位置、前置知识
  - `> [!IMPORTANT]` 本质：核心机制、适用范围、为什么成立
  - `> [!TIP]` 直觉：类比、图像化理解、快速判断技巧
  - `> [!WARNING]` 坑：易错点、失效条件
- 层次/流程/决策**必须**用 Mermaid（```` ```mermaid ````），不要手画框图。
- 禁止 ASCII 字符画（`+---+`、`┌─┐` 之类），**表格用 Markdown 表格**。
- 不要写课程行政信息（考勤、评分、助教邮箱、exam 安排）——那些进知识树 `Notes/ECE2050 Knowledge Tree.md`。

## 2. frontmatter（严格按此格式，不要多字段、不要少字段）

```yaml
---
tags:
  - ECE2050
  - <分区标签：见 PLAN-Ch2.md 该篇 tags 字段>
date: 2026-09-16
aliases:
  - <中文名>
  - <英文全名>
  - <英文缩写或第三别名>
---
```

- `aliases` 必须包含**中文名 + 英文全名 + 英文缩写**；没有公认缩写时用 PLAN 里给的第三别名。
- 文件名本身就是英文全名，`aliases` 里仍要重复列一次英文全名。

## 3. 正文骨架（顺序固定，标题用英文，可加中文副标题）

```markdown
> [!NOTE] 定位 (Where this fits)
> 一句话说明本篇在第二章中的位置，并给前置笔记双链，例如：
> 前置：[[Number Systems]]、[[Binary Number System]]。

## 核心定义 (Core Definition)

...定义 + 记号 + 单位/位宽...

## 适用前提 (Assumptions and Validity)

> [!IMPORTANT] ...
...成立条件、失效边界...

## 推导过程 (Derivation)

...从定义/前一篇结论推出本篇的核心公式或算法，步骤可跟随，不跳步...

## 求解步骤与方法 (Method and Steps)

1. ...
2. ...

（必要时给 Mermaid 流程图）

## 例题 (Worked Example)

**Example 1 — ...**
题目、已知、求。
解：分步写。
**数值校验 (Numerical check)**：把结果代回 / 用第二种方法重算 / 检查位宽与范围。

## 常见误区 (Pitfalls)

> [!WARNING] ...
1. ...
2. ...
（3–6 条，每条写清"错在哪 + 正确做法"）

## 相关笔记 (Connections)

- 上游 (upstream)：[[...]] —— 为什么它是本篇的前提
- 下游 (downstream)：[[...]] —— 本篇是它的基础
- 平行 (parallel)：[[...]] —— 容易混淆/常一起考

---
索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]
```

- 正文长度（含 frontmatter、不含代码块中的图脚本）控制在 **120–260 行**；宁精不滥。
- 每篇至少 2 个例题，其中至少 1 个来自讲义页序（PLAN 已指定）；例题必须有可复核的数字结论。

## 4. 配图规则（铁律，来自实测）

**混合策略（作者 2026-09 确认）**：图分两类——
① **重画 SVG**：凡是需要推导、精确标注或轴刻度的（时序图、逻辑电平区间、噪声容限、VTC、卡诺图圈组、
门级等价、位域与曲线）→ 必须写脚本重画；
② **讲义裁剪 PNG**：符号块、器件总表、例题图等"原图即答案"的内容 → 直接嵌入 `Figures/` 下**已生成**的
裁剪图（`![[ch3-two-input-gates.png]]`），图注必须写明"讲义 p.N 原图"。
裁剪图由 `Tools/pdfcrop.py` 的登记表统一生成（**不要**手写 PNG、**不要**改那个脚本、**不要**重新裁剪）；
③ **真值表、定理表、家族参数表一律用 Markdown 表格**，既不裁剪也不画图。

- 原理图/电路图 → **schemdraw**；曲线/区间/位域/表格化示意图 → **matplotlib**。
- **必须复用** `Tools/figstyle.py`（库内唯一视觉来源），脚本头部固定写：

```python
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
```

- 脚本路径 `Tools/figures/<同名>.py`，图片 `Figures/<同名>.svg`，
  调用 `save_svg(d, '<同名>')` / `save_fig(fig, '<同名>')`（自动同时写 PNG 备份到 `.scratch/png/`）。
- **必须实际运行脚本**确认成功（`D:\anaconda\python.exe Tools\figures\<同名>.py`），
  不允许"写完脚本但没跑过"。
- 跑完用 `D:\anaconda\python.exe Tools\ascii_preview.py <同名>` 核对轮廓（字符越密=墨越多），
  确认没有空图、没有元素跑到画布外、没有元素互相压字；如有 `read_image` 工具，直接看
  `.scratch/png/<同名>.png` 更可靠。
- 图内文字**只能用英文/数学符号**（SVG 内嵌 DejaVu 字体没有中文字形，写中文会变方框）。
- 配色只用 figstyle 里的常量：本体 `INK`、强调/关键 `HILITE`、次级强调 `ACCENT`、
  辅助虚线 `MUTED`、填充 `FILL`、对/错标注 `GOOD`/`BAD`。线宽不要自己写数字（用默认）。
- **一图一义**；多情形用 `(a)` `(b)` 子图并排，用 `ax.set_title('(a) ...')` 标注。
- 笔记中嵌图：单独一行 `![[<同名>.svg]]`，下一行写斜体图注：
  `*图 1 — ...（说明这张图想表达什么，与正文的哪个结论对应）*`。图号按该篇出现顺序从 1 开始。
- 图出现的位置要贴近相关正文（定义之后 / 推导之后 / 例题之前）。

## 5. 双链规则

- **只能**链接 `.scratch/PLAN-Ch2.md`「双链白名单」中的名字（18 篇笔记 + `Knowledge Tree` + `Glossary`）。
- 显示名可用中文：`[[Two's Complement Representation|补码]]`。
- 不要在正文里链接尚未存在的其它概念（宁可写纯文本，如 "shift register（Ch8 内容）"）。
- 每篇结尾必须有 `索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]`（保证双向可达）。

## 6. 例题与数值校验（硬要求）

- 用 `.scratch/verify_ch2.txt` 里已算好的数字；如果计划外的数字，自己用
  `D:\anaconda\python.exe -c "..."` 复核后再写进笔记。
- 校验必须**真的算一遍**并写进正文，例如"回代：$1000_2+1101_2=1\,0101_2$，丢弃进位得 $0101_2=5$ ✓"。
- 二进制常量写成 `1011 0110` 这种 4 位一组的形式，便于肉眼核对。

## 7. 交付前自检清单（逐条打勾后再结束）

1. 文件名与 PLAN 完全一致；frontmatter 三字段齐全、aliases ≥3 条、tags 两个（`ECE2050` + 分区标签）。
2. 骨架九段齐全，标题用英文；无 ASCII 图；无 PDF 截图；正文 120–260 行。
3. 所有 `[[...]]` 目标都在白名单内；结尾有索引行。
4. 图脚本已实际运行成功（贴出打印的 `wrote ...` 行作为证据）；SVG 存在于 `Figures/`；
   笔记用 `![[...svg]]` 嵌入 + 斜体图注；图内无中文字符。
5. 例题数字已复核，正文写出校验过程。
6. 图和正文语义一致（不要出现"如图所示"但图画的是别的东西）。
7. 只改动了分配给你的文件（最后 `git status` 式自查：列出你写了哪些文件）。

## 8. 收尾

写完自己那批后，运行一次全库体检并把输出贴给自己看：

```
D:\anaconda\python.exe Tools\check_vault.py
```

你**不需要**让 `PROBLEMS` 归零（可能有别的批次还没写完），但**不能**出现由你负责的文件引起的
problem（未解析双链、缺图、缺 frontmatter、知识树漏项除外——知识树由主代理统一维护）。
