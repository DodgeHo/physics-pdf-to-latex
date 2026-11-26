# physics-pdf-to-latex

> 仓库地址：https://github.com/DodgeHo/physics-pdf-to-latex

为 **tapphysics** 服务：把**高中物理试卷 / 高考真题 PDF**（含 docx 转出的 PDF）批量转成符合 **MathLive** 规范的 LaTeX 源码：题干、选项、公式转写为 LaTeX，无法公式化的装置图、电路图、光路图自动裁剪为本地图片，并为每道题独立推导解析与答案，逐卷校验、逐卷留问题记录。

---

## 一句话上手（给外行）

直接把下面这句话发给你的 AI 助手，它会主动到上面的 GitHub 仓库下载（或读取）代码，把技能装好：

> 请到 https://github.com/DodgeHo/physics-pdf-to-latex 下载（或读取）这个仓库，把里面的 `physics-pdf-to-latex` 技能文件夹安装到你的用户技能目录（`.user_skills`），装好后回复我；以后我发物理试卷 PDF，就用它转成 MathLive 能渲染的 LaTeX 并配解析。

装好之后，发试卷 PDF 再说一句：

> 用 physics-pdf-to-latex 把这份试卷转成 MathLive LaTeX，配图裁成本地图片，每题附解析，有问题列出来。

整批几十卷时可以说："这些卷子一次做完，有问题的地方记录在文件里。"

---

## 它会做什么

1. **探查 PDF**：逐页渲染预览图（1.6x），统计文字层、图片与矢量绘图坐标。
2. **自动裁图**：按页把所有图形区域（嵌入位图 + 绘图簇）裁成 3 倍 PNG，`pNN_k.png` 命名，不猜题号；再拼一张带文件名的 `_sheet.png` 总览供人工判归属。
3. **转写题目**：对照渲染图逐题转写题干、选项、公式、表格；文字层只用于定位，公式上下标以渲染图为准。
4. **写解析**：要点式——选择题逐项给依据，实验题给操作理由与误差来源，计算题给方程、代入与结论。
5. **校验 + 留痕**：`verify_tex.py` 检查图片命中、题号连续、违禁命令；每卷附 `_notes/<卷名>.md` 问题记录（缺题、缺答案、与答案键冲突、图像选项映射不确定等）。

## 答案口径（重要）

- 答案以**源答案键**为准，解析自己重写，不因"算得更顺"改答案。
- 源无答案时自行推导，并在问题记录标注"需人工复核"。
- **网络只提供题干**：缺题面可用公开真题补齐并注明来源，但答案与解析不照抄网络答案册，网络答案只用于比对，差异双向登记。
- 缺题、缺选项、缺数据一律如实登记，不编造；缺题按源题号跳号。

## 安装

### 方式一：让 AI 自动安装（推荐）

把下面这句话发给 AI，它会主动克隆 / 读取仓库并完成安装：

> 到 https://github.com/DodgeHo/physics-pdf-to-latex 下载仓库，把 `physics-pdf-to-latex` 文件夹放到我的用户技能目录（`.user_skills`）。

### 方式二：手动安装

1. 打开 https://github.com/DodgeHo/physics-pdf-to-latex ，点 `Code` → `Download ZIP`（或 `git clone https://github.com/DodgeHo/physics-pdf-to-latex.git`）。
2. 解压后，把整个 `physics-pdf-to-latex` 文件夹复制到你的 AI 工作区的用户技能目录：

   ```
   <工作区>/workspace/.user_skills/physics-pdf-to-latex
   ```

   如果找不到 `.user_skills` 目录，直接问你的 AI："我的用户技能目录 `.user_skills` 在哪？" 它会定位后放入。

3. 重启 / 新开一轮对话，技能即被识别。

## 目录结构

```
physics-pdf-to-latex/
├── SKILL.md                      # 技能元信息与触发规则（AI 读取）
├── README.md                     # 本说明文件（人类阅读）
├── references/
│   ├── workflow.md               # 单卷五阶段详细操作流程
│   ├── batch-spec.md             # 批量成卷规范（隔离、并行、验收）
│   └── mathlive-format.md        # MathLive 格式硬规范
└── scripts/
    ├── prep.py                   # 一键：预览 + 自动裁图 + 编号总览（--scan 加 3.6x 整页）
    ├── probe_pdf.py              # 探查 PDF：页数/文字/图片/绘图 bbox + 预览图
    ├── qfig.py                   # 按页裁出全部图形区域（pNN_k.png + _figs.json）
    ├── sheet.py                  # 裁图拼成带文件名的 _sheet.png 总览
    ├── compose.py                # 2–4 张选项小图合成带 A/B/C/D 标签的单图
    ├── crop_images.py            # 按 JSON 清单精确裁切（已知 rect 时用）
    └── verify_tex.py             # 校验 tex：图片命中、题号、违禁命令、格式残留
```

## 快速开始

```bash
# 1) 探查 + 自动裁图 + 总览（一卷一条命令）
python scripts/prep.py "试卷.pdf" "2025湖南" --root "D:\试卷批次"

# 2) 读 _sheet.png 判归属，读 preview/page_N.png 转写，写成 2025湖南.tex

# 3) 校验（须 OK）
python scripts/verify_tex.py "2025湖南.tex"
```

纯扫描件（文字层为空）加 `--scan`，会额外输出 3.6x 整页图。docx 源先用 Word COM 转 PDF：`$doc.SaveAs2($out, 17)`。

## 运行依赖

- Python 3.9+
- 第三方库：`pymupdf`、`Pillow`

  ```bash
  python -m pip install pymupdf Pillow
  ```

## 输出约定

```
tex输出/<卷名>/<卷名>.tex      # 成稿
tex输出/<卷名>/images/*.png    # 配图（绝对路径引用，需与 tex 一起保存）
tex输出/_notes/<卷名>.md       # 问题记录（五栏：源 / 题数·配图 / 校验 / 问题）
```

- 表格用 `array` 环境；选项分行书写；核素写成 `${}_{90}^{232}\mathrm{Th}$`。
- 题间源码留三个空行；填空直接写裸下划线；禁用 `\quad`、`\qquad`、`\vspace`、`\hline`、`itemize`、`enumerate`、`\ce`、`align`、`tabular`、`\textbf`、`\_`。

完整规范见 [`references/mathlive-format.md`](references/mathlive-format.md)，单卷流程见 [`references/workflow.md`](references/workflow.md)，批量见 [`references/batch-spec.md`](references/batch-spec.md)。

## 适用范围

面向**高中物理 / 高考真题**试卷。其它理科试卷（化学、生物）可参照调整公式与图表规范；化学方程式如需 `\ce` 风格，需另行扩展。
