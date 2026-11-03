# Tools — 配图与校验工具链 (Figure and QA toolchain)

本目录是笔记库的**可复用工具链**。所有 `Figures/*.svg` 都由这里的脚本生成，
不要手工编辑 SVG（手改的图无法复现，也无法与正文保持同步）。

## 库结构 (Vault layout) — 本库的固定约定

| 位置 | 内容 |
|---|---|
| `Notes/` | **正式笔记都在这里**：31 篇主线笔记 + 知识树 `ECE2050 Knowledge Tree.md` + 术语表 `Glossary.md` |
| `Figures/` | 57 张自绘 SVG 与 23 张讲义 PNG（其中九张 Ch6 保留全页）；图片由脚本生成 |
| `Tools/figures/` | 每张图一个渲染脚本，与 `Figures/<name>.svg` 同名 |
| `.scratch/` | 素材提取与数字校验（`extract/`、`png/`、`verify_ch2.py`、`verify_ch2.txt`、`NOTE_SPEC.md`、`PLAN-Ch2.md`） |

- **Bilingual writing / 双语写作**：章节标题与索引摘要以英文优先，后接中文提示；专题笔记开头给出简短 English quick recall。中文保留用于推导、易混淆条件和例题解释。整体可读文字的英文比例以约40%为目标，代码、数学和元数据不计入估算。增加英文时，先核对术语和技术含义，不逐句机械翻译，也不删除原有中文解释。
- **合并笔记 / Consolidated notes**：每章 1–5 篇，正文按概念与因果顺序推进；详细推导、例题与原图使用对应小节中的可展开块。旧标题与别名保留用于检索，正式双链指向新文件和相应小节。总行数含折叠内容，原有微型笔记的长度提示仅供参考。
- 枢纽双链统一写**文件名形式**：`[[ECE2050 Knowledge Tree]]`、`[[Glossary]]`
  （`[[Knowledge Tree]]` 也命中，因为知识树在 `aliases` 里保留了这个别名；但本库**统一用文件名形式**）。
  每篇笔记结尾固定 `索引：[[ECE2050 Knowledge Tree]] · [[Glossary]]`。
- `check_vault.py` 按 `index` / `glossary` **标签**定位这两个枢纽文件 —— 以后再改名或换目录也不会失效，
  但**默认位置就是 `Notes/`**，新笔记一律写进 `Notes/`；它还会提醒索引行是否用了非规范写法。

## 文件

| 文件 | 作用 |
|---|---|
| `figstyle.py` | **唯一视觉来源**：配色、线宽、字号、schemdraw/matplotlib 全局样式，以及 `save_svg` / `save_fig`（同时输出 SVG 与 PNG 备份）。与 ECE2001 库同源，保证两库视觉语言一致。 |
| `figures/<name>.py` | 每张图一个脚本，与 `Figures/<name>.svg` **同名**。 |
| `check_vault.py` | 正式笔记体检：frontmatter、双链可达性、图片存在性、SVG 合法性（含 CJK 方框检测）、知识树 ✅ 标注、字符画残留。必须保持 `PROBLEMS (0)`。它会按 `index`/`glossary` 标签**自动定位**知识树与术语表，并按**文件名或 aliases** 解析双链。草稿和工具文档中的示例占位符不属于正式笔记。 |
| `figcheck.py` | 单张图的**布局体检**：渲染后遍历所有文本包围盒，报"文字互相压字"和"文字跑出画布"。用法 `figcheck.py <name>`，或 `figcheck.py --all` 扫全部 matplotlib 图。**新图必须 0 problem**。 |
| `pdfcrop.py` | **讲义裁剪图**：登记表驱动，把讲义 PDF 的插图渲成 `Figures/<name>.png`（300 dpi）。`mode="graphics"` 自动取图形并集（会剔除整页背景、标题横幅、页脚 logo 带；若并集过小则自动退回 `"content"` 整幅内容区），另有 `"page"` / `"below"`。用法 `pdfcrop.py [name ...]`。用于"原图即答案"的符号块与例题图；**需要推导/精确标注的图仍要重画 SVG**。 |
| `ascii_preview.py` | 把 PNG 备份转成 ASCII，供没有图像查看器的环境肉眼核对图形轮廓。 |

素材提取脚本与中间产物在 `.scratch/`：`.scratch/extract_pdf.py`（PDF→文本）、
`.scratch/extract/`（讲义纯文本）、`.scratch/verify_ch2.py` + `.scratch/verify_ch2.txt`
（第二章全部例题数字的机器复核报告）、`.scratch/png/`（图的 PNG 备份）。

## 环境

```
D:\anaconda\python.exe        # Anaconda，含 schemdraw 0.23 / matplotlib / numpy / pdfplumber / pillow
```

（`python` 在 PATH 上但没有 schemdraw，务必用上面的完整路径。）

## 新增一张图的固定流程

1. 写 `Tools/figures/<name>.py`，头部固定：

```python
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figstyle import (INK, HILITE, ACCENT, MUTED, FILL, GOOD, BAD,
                      schematic, save_svg, elm, apply_mpl_style, save_fig)
```

2. 原理图/电路图用 `schematic()` 起步，曲线/区间/位域图用 `apply_mpl_style()` 起步。
3. 渲染：`D:\anaconda\python.exe Tools\figures\<name>.py` → 输出 `Figures/<name>.svg` + `.scratch/png/<name>.png`。
4. 核对轮廓：`D:\anaconda\python.exe Tools\ascii_preview.py <name>`（或直接看 `.scratch/png/<name>.png`）。
5. 在笔记中用 `![[<name>.svg]]` 嵌入，并写一行斜体图注。
6. 收尾跑一次 `D:\anaconda\python.exe Tools\check_vault.py`。

## 视觉规范（实测结论，勿重新试错）

- 配色只用 `figstyle` 常量：本体 `INK`、强调/关键 `HILITE`、次级强调 `ACCENT`、
  辅助虚线 `MUTED`、填充 `FILL`、对/错标注 `GOOD`/`BAD`；线宽统一 2.0。
- 离散元件一律用 schemdraw 标准几何（电阻 `elm.Resistor` 的锯齿、D 触发器 `elm.FlipFlop`、
  XOR 用 `schemdraw.logic`），不要手工拼折线；节点用实心圆点；元件必须标注。
- 接地符号连到底部母线；**无参考地的电路刻意不接地**。
- 图内文字只写英文/数学符号：SVG 内嵌 DejaVu 字形，写中文会变方框。
- **schemdraw 0.23 的坑**：`elm.SourceV()` / `elm.SourceI()` 的 `elmparams` 写死 `theta=90`，
  `.at(p).to(q)` 只设定长度、**不设定方向**；源必须显式写 `.up()/.down()/.left()/.right()`，
  长度用 `.length(L)`。
- **位域/位串类图约定**（本库大量使用）：bit 格用 `FILL` 填充 + `INK` 边框；
  被强调的位（符号位、进位、校验位、非法码）用 `HILITE` 或 `BAD`；正确结果用 `GOOD`；
  二进制串一律 **4 位一组**书写，便于肉眼核对。
- 需要精确推导或统一标注的图用脚本重画 SVG；讲义原图本身是学习对象时，可用登记过的 `pdfcrop.py` 生成 PNG，并在笔记中注明来源。
- 一图一义；多情形用 `(a)` `(b)` 子图并排。

## 2026-09-30 全库扩展验证

规划与概念覆盖记录在 `.scratch/PLAN-Expansion-20260930.md`、`.scratch/source-coverage-20260930.md`；
新增例题验算为 `.scratch/verify_expansion.py` 和 `.scratch/application-checks.py`。
`.scratch/audit_expansion.py` 核对知识树、术语表、canonical links、语义入链和英文比例估算。
仅按需要运行构建脚本；正式笔记完成后的手工编辑不要被草稿重建覆盖。

## 2026-10-09 合并笔记内容补全

已对照 88 篇专题原稿，将 662 个原稿二级小节的内容整合到 31 篇主线笔记。
正文补齐完整定义、适用条件、关键表格、解题方法与误区，详细推导和例题保留在对应小节。
备份、逐节覆盖记录与正式仓库验证结果见 `.scratch/full-content-20261008/README.md`。
合并后的详细内容有意保留，原有微型笔记长度提示不能作为删减正文的依据。

## Chapter 6 figure sources · 第六章配图来源

`pdfcrop.py` 的 `ch6-*` 登记项生成九张 Chapter 6 原图，源页为 10、11、23、27、34、37、40、44、53。
这些登记项使用 `page` 模式，完整保留靠近页边的电源标记、反相横线和公式。
`Tools/figures/ch6-static-hazard-timing.py` 生成与 p.52–53 变量一致的自绘时序图；1/2/1 ns 是正文声明的示例延迟，不是器件参数。
原图来源页码写在各笔记图注中；图表、公式与例题应同时保持一致。
