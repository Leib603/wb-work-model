#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WB 工作模型打包器
=================
从 source/（真相源）读取内容，自动生成各平台适配文件，并打包成 zip。

用法：
    python build.py

之后只需维护 source/ 下的文件，改完重新跑一次即可全平台同步。
无需任何第三方依赖，只用 Python 标准库。
"""

from pathlib import Path
from datetime import datetime
import zipfile

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"
OUT = ROOT / "adapters"
ZIP_NAME = ROOT / "work-model-package.zip"

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def read(rel: str) -> str:
    """读取真相源中的文件；不存在时返回空字符串并提示。
    自动剥离开头的 YAML frontmatter，避免把元数据带进适配文件。"""
    p = SRC / rel
    if not p.exists():
        print(f"  [跳过] 缺少 {rel}")
        return ""
    text = p.read_text(encoding="utf-8").strip()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:].strip()
    return text


def collect_dir(rel: str) -> list[tuple[str, str]]:
    """收集目录下所有 .md 文件（含子目录），返回 (相对路径, 内容)。"""
    base = SRC / rel
    items = []
    if not base.exists():
        return items
    for p in sorted(base.rglob("*.md")):
        content = p.read_text(encoding="utf-8").strip()
        if content.startswith("---"):
            end = content.find("\n---", 3)
            if end != -1:
                content = content[end + 4:].strip()
        items.append((str(p.relative_to(SRC)).replace("\\", "/"), content))
    return items


def write_out(name: str, content: str) -> None:
    p = OUT / name
    p.write_text(content, encoding="utf-8")
    print(f"  [生成] {name}")


# ---------------------------------------------------------------------------
# 读取真相源
# ---------------------------------------------------------------------------

print("读取真相源 ...")
soul = read("identity/SOUL.md")
identity = read("identity/IDENTITY.md")
user = read("identity/USER.md")
memory = read("memory/MEMORY.md")

decisions = collect_dir("memory/decisions")
skills = collect_dir("skills")
knowledge = collect_dir("knowledge")

def bundle(items: list[tuple[str, str]]) -> str:
    if not items:
        return "_（暂无内容）_"
    parts = []
    for rel, content in items:
        parts.append(f"### {rel}\n\n{content}")
    return "\n\n---\n\n".join(parts)

decisions_bundle = bundle(decisions)
skills_bundle = bundle(skills)
knowledge_bundle = bundle(knowledge)

today = datetime.now().strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# 适配 1：对话类 AI（ChatGPT / Claude / Gemini）——可直接粘贴的主提示词
# ---------------------------------------------------------------------------

chat_prompt = f"""# WB 工作模型 · 对话类 AI 主提示词

> 生成日期：{today}
> 用法：把本文件的全部内容复制，粘贴到新对话的第一条消息，开头加一句：
> "以下是我的工作模型，请完整读取并在本次对话中始终遵守。"

---

## 一、你的身份

{identity}

## 二、你的行为准则

{soul}

## 三、关于我

{user}

## 四、长期记忆

{memory}

## 五、可复用工作流

{skills_bundle}

## 六、知识索引

{knowledge_bundle}

---

## 七、给我的一句话提醒

我是 Leib，你记得叫我称呼的人。你不是一次性问答工具，是我的长期协作伙伴。
如果你发现这份模型有过时或矛盾之处，直接告诉我，不要默默猜测。
"""

write_out("01-对话类AI-主提示词.md", chat_prompt)

# ---------------------------------------------------------------------------
# 适配 2：编码类工具（Codex / Cursor / Copilot / Windsurf）——AGENTS.md 标准
# ---------------------------------------------------------------------------

agents_md = f"""# AGENTS.md — 协作约定

> 本文件遵循 AGENTS.md 开放标准，供编码类 AI 工具在会话开始时自动读取。
> 由 WB 工作模型生成于 {today}。请勿直接编辑本文件，改 source/ 后重新生成。

## 协作身份

- 助手代号：**WB**（由用户 Leib 命名）。
- 风格：直接、有主见、不奉承；该动手时给出可执行的产出，而非泛泛建议。

## 关于用户

{user}

## 行为准则

{soul}

## 项目约定

- 沟通与文档默认使用简体中文；代码标识符使用英文。
- 涉及资金的场景：涨用红色、跌用绿色（中国习惯）；默认货币符号 ¥。
- 修改文件前先读取，避免覆盖未知内容。

## 可复用工作流

{skills_bundle}

## 上下文与记忆

{memory}

## 决策记录（为什么这么定）

{decisions_bundle}
"""

write_out("02-AGENTS.md", agents_md)

# ---------------------------------------------------------------------------
# 适配 3：Claude Code ——CLAUDE.md 引用 AGENTS.md
# ---------------------------------------------------------------------------

claude_md = f"""# CLAUDE.md

> Claude Code 不会自动读取 AGENTS.md，因此用本文件显式引入。
> 生成于 {today}。

@import AGENTS.md

请将同目录下的 `02-AGENTS.md` 内容作为本项目协作约定的完整来源。
若工具支持 @import，上面的指令会自动加载；若不支持，请手动把 AGENTS.md 内容读入上下文。
"""

write_out("03-CLAUDE.md", claude_md)

# ---------------------------------------------------------------------------
# 适配 4：手机端——精简版，适合手机复制粘贴
# ---------------------------------------------------------------------------

mobile_md = f"""# WB · 手机速用版

> 生成日期：{today}
> 用法：复制到手机备忘录/云笔记，用的时候整段粘贴到 AI 对话开头。
> 保持精简，因为手机上输入和阅读都不方便。

---

你是 **WB**，我的长期协作 AI。我是 **Leib**。
风格：直接、有主见、不奉承。该动手时给可执行的产出。

我的偏好：
- 工作模型、记忆、工作流必须是我拥有的文件，不锁在某家平台里。
- 中文交流。

当前我们在做的事：建立「可移植工作模型」——一份真相源，自动生成手机/电脑/各 AI 平台都能用的适配。

{user}

如果你发现这份模型有过时或矛盾之处，直接告诉我。
"""

write_out("04-手机速用版.md", mobile_md)

# ---------------------------------------------------------------------------
# 适配 5：恢复说明——如何把模型装回 WorkBuddy
# ---------------------------------------------------------------------------

restore_md = f"""# 恢复到 WorkBuddy

> 生成日期：{today}
> 当你在新设备/新环境用 WorkBuddy，需要把工作模型装回去时，按下面做。

## 方法

把 `source/identity/` 下的三个文件，复制到 WorkBuddy 个人记忆目录：

```
SOUL.md      → ~/.workbuddy/<你的用户ID>-personal/SOUL.md
IDENTITY.md  → ~/.workbuddy/<用户ID>-personal/IDENTITY.md
USER.md      → ~/.workbuddy/<用户ID>-personal/USER.md
```

工作区记忆则复制 `source/memory/MEMORY.md` 到：
```
<工作区>/.workbuddy/memory/MEMORY.md
```

直接在对话里告诉我"把工作模型装回去"，并把 source 文件放好，我会帮你完成复制。

## 提示

- 当前这台机器的用户目录是：`~/.workbuddy/user-2b0fece5-78d3-4765-81d1-74911f9f47f7-personal/`
- 换新设备后用户 ID 可能变化，以实际目录为准。
"""

write_out("05-恢复到WorkBuddy.md", restore_md)

# ---------------------------------------------------------------------------
# 打包 zip（包含真相源、所有适配、脚本、文档；排除 .git 与 backups）
# ---------------------------------------------------------------------------

print("打包 zip ...")
EXCLUDE_DIRS = {".git", "backups", "restored", "__pycache__", ".workbuddy"}
EXCLUDE_FILES = {ZIP_NAME.name}
with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        parts = p.relative_to(ROOT).parts
        if any(d in EXCLUDE_DIRS for d in parts):
            continue
        if p.name in EXCLUDE_FILES:
            continue
        z.write(p, p.relative_to(ROOT))

print(f"\n完成：{ZIP_NAME.name}")
print(f"真相源文件 {len(list(SRC.rglob('*.md')))} 个，适配文件 5 个。")
