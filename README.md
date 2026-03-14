# flashcard-maker 🃏

> 文本转 Anki 记忆卡片技能 — 把笔记、教材、论文、网页自动生成闪卡，支持导出 .apkg 直接导入 Anki。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Allen091080/flashcard-maker/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](.)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://skills.sh)

---

## ✨ 功能特性

- 📝 **多种输入** — 文本、文件、PDF、URL
- 🃏 **三种卡片类型** — 问答（Basic）、填空（Cloze）、双语（Bilingual）
- 📦 **Anki 直导** — 导出 `.apkg` 格式，双击即可导入 Anki
- 📄 **多种格式** — 同时支持 CSV、Markdown、JSON 导出
- 🌏 **中英双语** — 支持中英文双语单词/术语卡片
- 🔢 **智能分割** — 自动从长文本中提取知识点

## 📋 需求

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python 3.10+ | 运行环境 | 内置 |
| genanki | 导出 .apkg | `pip3 install genanki`（可选）|
| pdfplumber | 读取 PDF | `pip3 install pdfplumber`（可选）|

导出 CSV/Markdown 无需任何额外依赖。

## 🚀 安装

```bash
npx skills add https://github.com/Allen091080/flashcard-maker -g -y
```

## 📖 使用示例

### 从文本生成卡片

```bash
python3 scripts/make_cards.py --text "
牛顿第一定律：物体在不受外力时，保持静止或匀速直线运动状态。
牛顿第二定律：F = ma，力等于质量乘以加速度。
牛顿第三定律：作用力与反作用力大小相等、方向相反。
" --format csv --output /tmp/cards
```

输出预览：

```
📖 共提取 3 个句子，开始生成卡片...
🃏 生成了 3 张卡片

📋 卡片预览（前5张）：
  [1] Q: 牛顿第一定律是什么？
      A: 物体在不受外力时，保持静止或匀速直线运动状态
  [2] Q: 牛顿第二定律的公式？
      A: F = ma，力等于质量乘以加速度
  [3] Q: 牛顿第三定律描述的是？
      A: 作用力与反作用力大小相等、方向相反

✅ CSV 已保存：/tmp/cards/cards_20260314_103000.csv
   导入方式：打开 Anki → 文件 → 导入 → 选择此文件
```

### 生成填空卡片

```bash
python3 scripts/make_cards.py --file notes.txt --type cloze --limit 20 --format csv
```

生成卡片示例：

```
光合作用将 {{c1::二氧化碳}} 和 {{c2::水}} 转化为葡萄糖和氧气
```

### 生成双语单词卡片

```bash
# 输入格式：中文\t英文 或 中文/英文
python3 scripts/make_cards.py --text "
人工智能/Artificial Intelligence
机器学习/Machine Learning
深度学习/Deep Learning
" --type bilingual --format csv
```

### 从 PDF 生成卡片

```bash
pip3 install pdfplumber
python3 scripts/make_cards.py --pdf ~/textbook.pdf --pages 1-30 --limit 50 --format apkg --deck "教材笔记"
# ✅ Anki 卡片包已保存：/tmp/cards/cards_20260314.apkg
```

### 从网页生成卡片

```bash
python3 scripts/make_cards.py --url "https://zh.wikipedia.org/wiki/量子力学" --limit 30 --format markdown
```

### 导出为 Anki .apkg

```bash
pip3 install genanki
python3 scripts/make_cards.py --file notes.txt --format apkg --deck "物理笔记" --output ~/anki/
# ✅ Anki 卡片包：~/anki/cards_20260314.apkg（双击导入 Anki）
```

## 💬 与 AI Agent 对话

```
帮我把这段笔记做成 Anki 卡片：
"线粒体是细胞的能量工厂，通过有氧呼吸产生ATP..."
→ 生成 Basic 卡片，导出 CSV

帮我做30个商务英语单词卡片
→ 生成双语 Bilingual 卡片

把这个 PDF 第1-20页做成填空卡片
→ 提取 PDF 内容，生成 Cloze 卡片，导出 .apkg
```

## 📁 项目结构

```
flashcard-maker/
├── SKILL.md              # Agent 技能定义
├── scripts/
│   └── make_cards.py     # 核心脚本
├── README.md
├── LICENSE               # MIT
└── .github/
    └── workflows/
        └── test.yml
```

## 📄 License

MIT © 2026 [Allen091080](https://github.com/Allen091080)
