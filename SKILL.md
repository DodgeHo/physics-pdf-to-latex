---
name: physics-pdf-to-latex
description: 把高中物理试卷/高考真题 PDF 批量转为符合 MathLive 规范的 LaTeX 源码：探查 PDF 结构、按题裁切无法转写的装置图/电路图/示意图为本地 PNG、对照渲染图转写题干选项与公式、为每题自写物理解析与答案，并校验图片引用与格式合规。适用于用户发来试卷/真题/习题 PDF 要求"转 LaTeX / 转 tex / 转 MathLive / 出解析 / 截图配图"，或需要把整卷整理成可渲染源码的场景。
---

# 物理试卷 PDF → MathLive LaTeX

## 概述

将一份物理试卷 PDF 转换为可在 MathLive 中直接渲染的 `.tex` 源码：题目文字与公式转写为 LaTeX，不能公式化的图形按题裁切为本地图片，每题附自写解析与答案。

## 工作流

按五个阶段执行，详细操作见 [references/workflow.md](references/workflow.md)：

1. **探查**：运行 `scripts/probe_pdf.py`，导出逐页预览 PNG 与文字层，统计图片/绘图 bbox。转写以预览图为准，文字层仅用于定位。
2. **裁切**：编写 JSON 清单，运行 `scripts/crop_images.py`，3 倍分辨率裁切题目图形到 `images/`。
3. **转写**：对照预览图逐题转写题干、选项、公式、表格；检索公开真题交叉核对答案，争议题以物理规律为准并标注。
4. **解析**：用自己的语言写解析——选择题逐项给依据，计算题列方程、代入、结果与单位；答案行单独一行。
5. **校验**：运行 `scripts/verify_tex.py`，确认图片命中、题号齐全、无违禁命令与间距/转义残留。

## 格式规范

成稿必须遵守 MathLive 硬规范（禁用命令、array 表格、选项分行、核素写法、题间空行、绝对路径、裸下划线等），完整清单见 [references/mathlive-format.md](references/mathlive-format.md)。

## 脚本索引

| 脚本 | 用途 |
| --- | --- |
| `scripts/probe_pdf.py` | 探查页数/文字/图片/绘图 bbox，生成预览图与文字层 |
| `scripts/crop_images.py` | 按 JSON 清单高分辨率裁切题目图形 |
| `scripts/verify_tex.py` | 校验 tex：图片命中、题号、违禁命令、残留间距/转义 |

## 关键提醒

- PDF 文字层公式上下标常错位，**必须对照渲染预览图核对**，不要直接复制文字层。
- 解析要重写物理过程，不能照抄参考答案；选择题需逐项判断。
- `.tex` 与 `images/` 目录必须一起交付（图片为本地绝对路径引用）。
