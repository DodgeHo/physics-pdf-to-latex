# physics-pdf-to-latex

把**高中物理试卷 / 高考真题 PDF** 批量转成符合 **MathLive** 规范的 LaTeX 源码：题干、选项、公式转写为 LaTeX，无法公式化的装置图、电路图、光路图按题裁切为本地图片，并为每道题写好自解析与答案。

---

## 一句话上手（给外行）

下载本仓库后，**把下面这句话连同仓库地址（或解压后的文件夹）一起发给你的 AI 助手**，它会自动读完说明、把技能装好：

> 请阅读这个仓库的 `README.md`，把 `physics-pdf-to-latex` 文件夹安装到你的用户技能目录（`.user_skills`），装好后回复我；以后我发物理试卷 PDF，就用它转成 MathLive 能渲染的 LaTeX 并配解析。

装好之后，以后直接发试卷 PDF，再说一句：

> 用 physics-pdf-to-latex 把这份试卷转成 MathLive LaTeX，题目图形裁成本地图片，每题附自写解析。

---

## 它会做什么

1. **探查 PDF**：逐页渲染预览图，统计文字、图片、矢量绘图及其坐标位置。
2. **裁切图形**：把电路图、装置图、示意图等按题裁成 3 倍分辨率 PNG，存入 `images/`。
3. **转写题目**：对照预览图逐题转写题干、选项、公式、表格；公式上下标以渲染图为准，不盲信 PDF 文字层。
4. **撰写解析**：用自己的语言重写物理过程——选择题逐项判断对错，计算题列方程、代入数值、给出结果与单位。
5. **自动校验**：检查图片引用是否命中、题号是否齐全、有无 MathLive 不支持的命令或残留格式。

## 手动安装

1. 下载本仓库 ZIP 并解压。
2. 把整个 `physics-pdf-to-latex` 文件夹复制到你的 AI 工作区的用户技能目录：

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
│   ├── workflow.md               # 五阶段详细操作流程
│   └── mathlive-format.md        # MathLive 格式硬规范（禁用命令、写法约定）
└── scripts/
    ├── probe_pdf.py              # 探查 PDF：页数/文字/图片/绘图 bbox + 预览图
    ├── crop_images.py            # 按 JSON 清单高分辨率裁切题目图形
    └── verify_tex.py            # 校验 tex：图片命中、题号、违禁命令、格式残留
```

## 运行依赖

- Python 3.9+
- 第三方库：`pymupdf`、`Pillow`

  ```bash
  python -m pip install pymupdf Pillow
  ```

## 输出约定

- 成稿：`<卷名>.tex` + 同目录 `images/` 图形文件夹，两者需一起保存（图片为本地绝对路径引用）。
- 表格用 `array` 环境；选项分行书写；核素写成 `${}_{90}^{232}\mathrm{Th}$` 形式。
- 题与题之间在源码中留三个空行；填空横线直接写裸下划线；不使用 `\quad`、`\qquad`、`\vspace`、`\hline`、`itemize`、`\ce`、`align`、`tabular`。

完整规范见 [`references/mathlive-format.md`](references/mathlive-format.md)，详细流程见 [`references/workflow.md`](references/workflow.md)。

## 适用范围

目前面向**高中物理 / 高考真题**试卷。其它理科试卷（化学、生物）可参照调整公式与图表规范；化学方程式如需 `\ce` 风格，需另行扩展。
