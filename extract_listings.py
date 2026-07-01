# -*- coding: utf-8 -*-
"""从 xr-know-008 章节提取代码清单到 code/ai-agent-book/src，并生成 manifest。"""
import json, re, os, glob

CHAPTERS_DIR = r"d:/zcqiand-life/1-projects/xr-knowledge-suite/output/xr-know-008/chapters"
OUT_DIR = r"d:/zcqiand-life/1-projects/xr-knowledge-suite/code/ai-agent-book/src"
MANIFEST = r"d:/zcqiand-life/1-projects/xr-knowledge-suite/code/ai-agent-book/extracted_code_manifest.json"

# 语言 -> 后缀
EXT = {
    "python": ".py",
    "bash": ".sh",
    "dockerfile": ".dockerfile",
    "json": ".json",
    "markdown": ".md",
    "mermaid": ".mmd",
    "yaml": ".yaml",
    "yml": ".yaml",
}

# 匹配开栏: ```python {title="代码清单1-1: 使用 LangChain 创建一个简单的 Agent"}
# 语言可选（部分栏写作 ``` {title="..."}，无语言标注）
FENCE_RE = re.compile(r'^```([a-zA-Z0-9]*)\s*\{.*?title="(代码清单\d+-\d+(?:（[^）]*）)?[:：]\s*[^"]*)".*\}\s*$')
# Windows 非法文件名字符
ILLEGAL = re.compile(r'[\\/:*?"<>|]')


def safe_desc(desc: str) -> str:
    """把标题中冒号后的描述转成安全文件名片段，保留空格/中文。"""
    return ILLEGAL.sub("_", desc).strip()


def extract():
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = []
    seen_names = {}  # filename -> count（防碰撞）

    chapters = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "chapter-*.md")))
    for ch_path in chapters:
        ch_file = os.path.basename(ch_path)
        with open(ch_path, encoding="utf-8") as f:
            lines = f.read().split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]
            m = FENCE_RE.match(line)
            if not m:
                i += 1
                continue
            lang = m.group(1).lower()
            title = m.group(2).strip()
            # 统一冒号: 把中文：换成英文: 仅用于解析，标题原文保留
            # 标题形如 "代码清单1-1: 使用 LangChain..."
            # 拆出 编号 和 描述
            mm = re.match(r'(代码清单\d+-\d+(?:（[^）]*）)?)[:：]\s*(.*)', title)
            if not mm:
                i += 1
                continue
            num_part = mm.group(1)
            desc = mm.group(2).strip()

            # 收代码到下一个 ``` 栏。若下一栏本身是「代码清单开栏」，
            # 说明当前块缺闭合栏（章节瑕疵）——当前块到此结束，不吞该开栏。
            code_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                code_lines.append(lines[j])
                j += 1
            # j 指向下一栏（或文件尾）
            next_is_listing = j < len(lines) and FENCE_RE.match(lines[j]) is not None
            code = "\n".join(code_lines)
            if code and not code.endswith("\n"):
                code += "\n"

            # 跳过空代码块（章节瑕疵，如空栏）
            if not code.strip():
                i = j if next_is_listing else j + 1
                continue

            ext = EXT.get(lang, ".txt") if lang else ".txt"
            fname = f"{num_part}_ {safe_desc(desc)}{ext}"
            # 防同章/跨章同名碰撞
            if fname in seen_names:
                seen_names[fname] += 1
                stem, e = os.path.splitext(fname)
                fname = f"{stem}_{seen_names[fname]}{e}"
            else:
                seen_names[fname] = 1

            fpath = os.path.join(OUT_DIR, fname)
            with open(fpath, "w", encoding="utf-8", newline="\n") as out:
                out.write(code)

            manifest.append({
                "title": title,
                "lang": lang,
                "chapter_file": ch_file,
                "line": i + 1,
                "extracted_file": f"src\\{fname}",
                "source": None,
            })
            # 下一栏是代码清单开栏则不吞，否则跳过裸闭合栏
            i = j if next_is_listing else j + 1

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest


if __name__ == "__main__":
    m = extract()
    print(f"extracted: {len(m)} listings")
    # 统计
    import collections
    by_ch = collections.Counter(x["chapter_file"] for x in m)
    by_lang = collections.Counter(x["lang"] for x in m)
    print("by lang:", dict(by_lang))
    print("chapters covered:", len(by_ch))
    for k in sorted(by_ch):
        print(f"  {k}: {by_ch[k]}")
