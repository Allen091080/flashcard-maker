#!/usr/bin/env python3
"""
flashcard-maker — 文本转 Anki 卡片脚本
用法: python3 make_cards.py --text "..." --output /tmp/cards
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime


def split_into_sentences(text: str) -> list:
    """将文本分割成句子"""
    text = text.strip()
    sentences = re.split(r'[。！？\n]+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def make_basic_cards(sentences: list, limit: int = None) -> list:
    """生成 Basic 问答卡片"""
    cards = []
    # 匹配"X是/为Y"、"X的Y是Z"等结构
    patterns = [
        (r"(.{2,20})(?:是|为|指的是|叫做)(.{5,100})", "{concept}是什么？", "{definition}"),
        (r"(.{2,20})(?:的|之)(.{2,10})(?:是|为)(.{5,80})", "{subject}的{attr}是什么？", "{value}"),
        (r"(.{5,30})(?:公式|计算方式|表达式)[为是：:]\s*(.{3,50})", "{concept}的公式是什么？", "{formula}"),
    ]

    for sentence in sentences:
        matched = False
        for pattern, q_tmpl, a_tmpl in patterns:
            m = re.search(pattern, sentence)
            if m:
                groups = m.groups()
                if len(groups) >= 2:
                    q = q_tmpl.format(
                        concept=groups[0], subject=groups[0],
                        attr=groups[1] if len(groups) > 2 else "",
                        definition=groups[-1]
                    )
                    a = a_tmpl.format(
                        definition=groups[-1], formula=groups[-1],
                        value=groups[-1]
                    )
                    cards.append({"type": "basic", "front": q.strip(), "back": a.strip(), "source": sentence})
                    matched = True
                    break

        if not matched and len(sentence) > 20:
            # 通用：把句子做成"这句话说的是什么？"
            # 只取前半部分作为提示
            mid = len(sentence) // 2
            cards.append({
                "type": "basic",
                "front": sentence[:mid] + "…（续）",
                "back": sentence,
                "source": sentence
            })

        if limit and len(cards) >= limit:
            break

    return cards


def make_cloze_cards(sentences: list, limit: int = None) -> list:
    """生成 Cloze 填空卡片"""
    cards = []
    # 找关键词（名词性短语、专有名词等）
    key_pattern = re.compile(r'[（(]?[\u4e00-\u9fff]{2,8}[）)]?(?:定理|定律|原理|公式|效应|现象|方法|算法|模型|理论)?')

    for sentence in sentences:
        keys = key_pattern.findall(sentence)
        # 选最重要的1-2个词填空
        keys = [k for k in keys if len(k) >= 2 and k in sentence][:2]
        if not keys:
            continue

        cloze_text = sentence
        for i, key in enumerate(keys, 1):
            cloze_text = cloze_text.replace(key, f"{{{{c{i}::{key}}}}}", 1)

        cards.append({"type": "cloze", "text": cloze_text, "source": sentence})
        if limit and len(cards) >= limit:
            break

    return cards


def make_bilingual_cards(sentences: list, lang: str = "zh-en", limit: int = None) -> list:
    """生成双语卡片（需要用户提供对照文本）"""
    cards = []
    # 简单处理：假设输入已经是"中文\t英文"或"中文/英文"格式
    for sentence in sentences:
        if "\t" in sentence:
            parts = sentence.split("\t", 1)
            cards.append({"type": "bilingual", "front": parts[0].strip(), "back": parts[1].strip(), "source": sentence})
        elif "/" in sentence and len(sentence.split("/")) == 2:
            parts = sentence.split("/", 1)
            cards.append({"type": "bilingual", "front": parts[0].strip(), "back": parts[1].strip(), "source": sentence})
        else:
            # 单语句子，做成中文正面，提示用户补充英文
            cards.append({"type": "bilingual", "front": sentence, "back": "（请补充翻译）", "source": sentence})
        if limit and len(cards) >= limit:
            break
    return cards


def export_csv(cards: list, output_path: str):
    """导出为 Anki 可导入的 CSV"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["#separator:comma"])
        writer.writerow(["#html:false"])
        writer.writerow(["#notetype:Basic"])
        writer.writerow(["Front", "Back", "Tags"])
        for c in cards:
            if c["type"] == "basic":
                writer.writerow([c["front"], c["back"], "auto-generated"])
            elif c["type"] == "cloze":
                writer.writerow([c["text"], "", "cloze auto-generated"])
            elif c["type"] == "bilingual":
                writer.writerow([c["front"], c["back"], "bilingual auto-generated"])
    print(f"✅ CSV 已保存：{output_path}")
    print(f"   导入方式：打开 Anki → 文件 → 导入 → 选择此文件")


def export_markdown(cards: list, output_path: str):
    """导出为 Markdown 格式（人类可读）"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# 记忆卡片 — {datetime.now().strftime('%Y-%m-%d')}\n\n"]
    for i, c in enumerate(cards, 1):
        if c["type"] == "basic":
            lines.append(f"## 卡片 {i}（问答）\n")
            lines.append(f"**Q:** {c['front']}\n\n")
            lines.append(f"**A:** {c['back']}\n\n")
            lines.append("---\n\n")
        elif c["type"] == "cloze":
            lines.append(f"## 卡片 {i}（填空）\n")
            lines.append(f"{c['text']}\n\n")
            lines.append("---\n\n")
        elif c["type"] == "bilingual":
            lines.append(f"## 卡片 {i}（双语）\n")
            lines.append(f"**正面:** {c['front']}\n\n")
            lines.append(f"**背面:** {c['back']}\n\n")
            lines.append("---\n\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"✅ Markdown 已保存：{output_path}")


def export_apkg(cards: list, deck_name: str, output_path: str):
    """导出为 Anki .apkg 格式（需要 genanki）"""
    try:
        import genanki
    except ImportError:
        print("⚠️  导出 .apkg 需要安装：pip3 install genanki")
        print("   改为导出 CSV 格式...")
        export_csv(cards, output_path.replace(".apkg", ".csv"))
        return

    model_basic = genanki.Model(
        1607392319,
        "Basic (auto)",
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{"name": "Card 1", "qfmt": "{{Front}}", "afmt": "{{FrontSide}}<hr>{{Back}}"}],
    )
    deck = genanki.Deck(2059400110, deck_name)
    for c in cards:
        if c["type"] in ("basic", "bilingual"):
            note = genanki.Note(model=model_basic, fields=[c.get("front", c.get("text", "")), c.get("back", "")])
            deck.add_note(note)

    genanki.Package(deck).write_to_file(output_path)
    print(f"✅ Anki 卡片包已保存：{output_path}")
    print(f"   导入方式：双击 .apkg 文件，或拖拽到 Anki 窗口")


def read_input(args) -> str:
    """读取输入文本"""
    if args.text:
        return args.text
    elif args.file:
        return Path(args.file).read_text(encoding="utf-8")
    elif args.pdf:
        try:
            import pdfplumber
            with pdfplumber.open(args.pdf) as pdf:
                pages = pdf.pages
                if args.pages:
                    start, end = map(int, args.pages.split("-"))
                    pages = pages[start-1:end]
                return "\n".join(p.extract_text() or "" for p in pages)
        except ImportError:
            print("❌ 读取 PDF 需要：pip3 install pdfplumber", file=sys.stderr)
            sys.exit(1)
    elif args.url:
        try:
            import urllib.request
            with urllib.request.urlopen(args.url) as r:
                html = r.read().decode("utf-8", errors="ignore")
            # 简单去标签
            text = re.sub(r"<[^>]+>", " ", html)
            return re.sub(r"\s+", " ", text)
        except Exception as e:
            print(f"❌ 无法访问 URL：{e}", file=sys.stderr)
            sys.exit(1)
    else:
        return sys.stdin.read()


def main():
    parser = argparse.ArgumentParser(description="文本转 Anki 卡片")
    inp = parser.add_mutually_exclusive_group()
    inp.add_argument("--text", help="直接输入文本内容")
    inp.add_argument("--file", help="从文件读取")
    inp.add_argument("--pdf", help="从 PDF 文件读取")
    inp.add_argument("--url", help="从网页 URL 读取")

    parser.add_argument("--pages", help="PDF 页码范围，如 1-20")
    parser.add_argument("--type", choices=["basic", "cloze", "bilingual"], default="basic")
    parser.add_argument("--limit", type=int, default=None, help="最多生成多少张卡片")
    parser.add_argument("--format", choices=["csv", "markdown", "apkg", "json"], default="csv")
    parser.add_argument("--deck", default="My Deck", help="Anki 牌组名称")
    parser.add_argument("--lang", default="zh-en", help="双语卡片语言对")
    parser.add_argument("--output", default="/tmp", help="输出目录")

    args = parser.parse_args()

    text = read_input(args)
    sentences = split_into_sentences(text)

    if not sentences:
        print("❌ 未能从输入中提取有效句子", file=sys.stderr)
        sys.exit(1)

    print(f"📖 共提取 {len(sentences)} 个句子，开始生成卡片...")

    if args.type == "basic":
        cards = make_basic_cards(sentences, args.limit)
    elif args.type == "cloze":
        cards = make_cloze_cards(sentences, args.limit)
    elif args.type == "bilingual":
        cards = make_bilingual_cards(sentences, args.lang, args.limit)

    print(f"🃏 生成了 {len(cards)} 张卡片")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.format == "csv":
        export_csv(cards, str(out_dir / f"cards_{ts}.csv"))
    elif args.format == "markdown":
        export_markdown(cards, str(out_dir / f"cards_{ts}.md"))
    elif args.format == "apkg":
        export_apkg(cards, args.deck, str(out_dir / f"cards_{ts}.apkg"))
    elif args.format == "json":
        out_file = out_dir / f"cards_{ts}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 已保存：{out_file}")

    # 预览前5张
    print("\n📋 卡片预览（前5张）：")
    for i, c in enumerate(cards[:5], 1):
        if c["type"] == "basic":
            print(f"  [{i}] Q: {c['front'][:40]}")
            print(f"      A: {c['back'][:40]}")
        elif c["type"] == "cloze":
            print(f"  [{i}] {c['text'][:60]}")
        elif c["type"] == "bilingual":
            print(f"  [{i}] {c['front'][:30]} → {c['back'][:30]}")
        print()


if __name__ == "__main__":
    main()
