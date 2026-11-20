# WB 工作模型 · 可移植包

这是一个"用户拥有的工作模型"：一份真相源，自动生成手机、电脑和各 AI 平台都能用的版本。
模型（发动机）可以换，这套工作模型（资产）跟着你走。

## 目录结构

```
work-model/
├── source/                  ← 你唯一需要维护的地方
│   ├── identity/           身份层：SOUL / IDENTITY / USER
│   ├── memory/             记忆层：长期记忆 + 决策记录
│   │   └── decisions/
│   ├── skills/             技能层：可复用工作流
│   ├── knowledge/          知识层：资料索引
│   └── staff/              员工层：5 个 AI 员工岗位卡 + TEAM.md 调度规范
├── adapters/                ← 自动生成，勿手动改
│   ├── 01-对话类AI-主提示词.md   ChatGPT / Claude / Gemini 粘贴用
│   ├── 02-AGENTS.md              编码类工具通用标准
│   ├── 03-CLAUDE.md              Claude Code 引用文件
│   ├── 04-手机速用版.md          手机精简版
│   └── 05-恢复到WorkBuddy.md     换设备时装回的说明
├── backups/                 ← 自包含快照，出问题时提出来用（详见 BACKUP.md）
│   ├── snapshots/           带时间戳的快照（保留最近 5 份）
│   ├── LATEST.zip           永远指向最新快照
│   └── manifest.json        快照清单 + SHA256 校验
├── build.py                 ← 打包脚本：真相源 → 各平台适配
├── backup.py                ← 备份脚本：生成自包含快照
├── restore.py               ← 恢复脚本：校验并提取快照
├── BACKUP.md                ← 备份与恢复说明
├── MIGRATION.md             ← 迁移/拷贝/导入操作手册（换设备照着做）
├── SYNC.md                  ← 跨设备 Git 同步说明
└── work-model-package.zip   ← 运行脚本后生成的可分发压缩包
```

## 日常使用（三步）

1. **改**：只改 `source/` 里的 Markdown。有新偏好写进 `memory/MEMORY.md`，有新决策写进 `memory/decisions/`，有新工作流写进 `skills/`。
2. **跑**：`python build.py`（无需安装任何依赖）。
3. **用**：把 `adapters/` 里对应的文件，粘贴或放到相应平台。

## 各平台怎么用

- **ChatGPT / Claude / Gemini 网页或 App**：打开 `01-对话类AI-主提示词.md`，全文复制，作为新对话第一条消息粘贴。
- **Cursor / Codex / Copilot / Windsurf**：把 `02-AGENTS.md` 放到项目根目录（改名为 `AGENTS.md`），工具会自动读取。
- **Claude Code**：把 `02-AGENTS.md` 改名为 `AGENTS.md`、`03-CLAUDE.md` 改名为 `CLAUDE.md`，都放项目根目录。
- **手机**：打开 `04-手机速用版.md`，复制到备忘录或云笔记，用时粘贴到 AI 对话开头。
- **换新设备上的 WorkBuddy**：按 `05-恢复到WorkBuddy.md` 操作。

## 跨设备同步

真相源已托管到私有 Git 仓库 `https://github.com/Leib603/wb-work-model`，详见 `SYNC.md`。

## 备份与恢复

重要节点先跑 `python backup.py`（生成自包含快照），出问题用 `python restore.py` 提出来即可用。详见 `BACKUP.md`。备份与 Git 同步互补：Git 管历史，备份管"随时能提出一份直接用的"。

## 迁移与导入

换设备、换平台、导入到手机或新电脑——照着 `MIGRATION.md` 操作手册做，含完整场景和验证清单。

## 维护原则

- 一句话标准：**如果这个细节会改变一个好搭档帮你的方式，它就该进 source/**；如果只是有趣，放归档。
- 记忆层只在"事情真的变了"时更新，不记流水账。
- 每月回顾一次：补上变真的，删掉不再适用的，在决策记录里留下带日期的说明。
