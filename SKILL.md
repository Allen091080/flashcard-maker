---
name: flashcard-maker
description: 把任意文本、笔记、PDF 或网页内容转成 Anki 记忆卡片，支持导出 .apkg/.csv 格式，支持中英文双语卡片。
version: "1.0.0"
metadata: {"openclaw": {"os": ["darwin", "linux", "win32"], "emoji": "🃏", "user-invocable": true, "homepage": "https://github.com/Allen091080/flashcard-maker", "tags": ["study", "anki", "learning", "memory", "education"]}}
---

# Flashcard Maker — 文本转 Anki 卡片

把笔记、文章、教材内容自动拆解成记忆卡片（Question/Answer 格式），导出为 Anki 可直接导入的 `.apkg` 或 `.csv` 格式。

## 适用场景

| 场景 | 用这个？ |
|------|---------|
| 把笔记转成 Anki 卡片 | ✅ 是 |
| 背单词/术语/概念 | ✅ 是 |
| 考试复习卡片制作 | ✅ 是 |
| 中英文双语卡片 | ✅ 是 |
| 代码知识卡片（编程）| ✅ 是 |
| PDF/网页内容提取 | ✅ 是 |
| 制作 PPT 幻灯片 | ❌ 否 |

## 卡片类型

### Basic（基础）
```
Q: 光合作用的原料是什么？
A: 二氧化碳（CO₂）和水（H₂O），以及光能
```

### Cloze（填空）
```
光合作用将 {{c1::二氧化碳}} 和 {{c2::水}} 转化为葡萄糖和氧气
```

### Bilingual（双语）
```
Front: Photosynthesis
Back: 光合作用 — 植物利用光能将CO₂和H₂O合成有机物的过程
```

### Code（代码）
```
Q: Python 中如何反转一个列表？
A: my_list[::-1]  或  list(reversed(my_list))
```

## 如何使用

### 1. 从文本直接生成卡片

```bash
# 从文字内容生成
python3 {baseDir}/scripts/make_cards.py --text "线粒体是细胞的能量工厂，通过有氧呼吸产生ATP..." --output /tmp/bio_cards

# 从文件读取内容
python3 {baseDir}/scripts/make_cards.py --file /path/to/notes.txt --output /tmp/cards
```

### 2. 从 PDF 提取内容生成卡片

```bash
python3 {baseDir}/scripts/make_cards.py --pdf /path/to/textbook.pdf --pages 1-20 --output /tmp/cards
```

### 3. 从网页 URL 生成卡片

```bash
python3 {baseDir}/scripts/make_cards.py --url "https://example.com/article" --output /tmp/cards
```

### 4. 指定卡片类型和数量

```bash
# 生成填空题卡片，限 20 张
python3 {baseDir}/scripts/make_cards.py --file notes.txt --type cloze --limit 20 --output /tmp/cards

# 生成双语卡片
python3 {baseDir}/scripts/make_cards.py --file vocab.txt --type bilingual --lang zh-en --output /tmp/cards
```

### 5. 导出格式

```bash
# 导出为 Anki .apkg（直接双击导入 Anki）
python3 {baseDir}/scripts/make_cards.py --file notes.txt --format apkg --deck "生物笔记" --output /tmp/cards

# 导出为 CSV（可导入任意闪卡应用）
python3 {baseDir}/scripts/make_cards.py --file notes.txt --format csv --output /tmp/cards

# 导出为 Markdown（人类可读格式）
python3 {baseDir}/scripts/make_cards.py --file notes.txt --format markdown --output /tmp/cards
```

## 与 AI Agent 对话示例

```
用户：帮我把这段笔记做成 Anki 卡片：
"牛顿第一定律：物体在不受外力作用时，保持静止或匀速直线运动状态。
牛顿第二定律：F = ma，力等于质量乘以加速度。
牛顿第三定律：作用力与反作用力大小相等、方向相反。"

Agent：已生成 3 张卡片：
卡片1 Q: 牛顿第一定律的内容是？
      A: 物体在不受外力时，保持静止或匀速直线运动状态
卡片2 Q: 牛顿第二定律的公式？
      A: F = ma（力 = 质量 × 加速度）
卡片3 Q: 牛顿第三定律描述的是？
      A: 作用力与反作用力大小相等、方向相反

导出为 /tmp/physics_cards.apkg，双击可导入 Anki。

用户：帮我做 20 个英语单词卡片，主题是"商务英语"
Agent：[生成双语卡片，正面英文，背面中文释义+例句]
```

## 重要规则

1. **每张卡片只包含一个知识点**，不要把多个概念塞进一张卡
2. **Answer 要简洁**，不超过 3 行，长解释放在 Note 字段
3. **Cloze 填空要有意义**，挖去的词必须是关键知识点
4. **生成数量**：默认每 100 字生成约 3-5 张卡片
5. **导出 .apkg 需要安装 genanki**：`pip3 install genanki`
6. **代码卡片要用等宽字体格式**（使用 `<code>` 标签）
