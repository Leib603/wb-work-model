# 工作模型 · 迁移 / 拷贝 / 导入 操作手册

> 这份手册解决一个问题：**换设备、换平台、出问题后，怎么把工作模型搬过去并正常用起来。**
> 面向的是"照着做就行"的场景，每一步都有具体命令或动作。

---

## 〇、先分清三种"载体"（最重要）

很多人出错是因为搞混了要搬哪个文件。先记住这张表：

| 载体 | 文件名 / 位置 | 它是什么 | 什么时候用 |
|------|--------------|---------|-----------|
| **① Git 仓库** | `github.com/Leib603/wb-work-model` | 云端主副本，带完整历史 | **日常迁移首选**。换电脑、多设备同步 |
| **② 分发包** | `work-model-package.zip`（根目录） | 一套干净的完整工作模型（不含备份和 .git） | 发给别人、传到另一台设备、无 Git 时用 |
| **③ 备份快照** | `backups/LATEST.zip`、`backups/snapshots/snapshot-*.zip` | 某时刻的自包含快照，带 SHA256 校验 | 模型改坏了要回退、灾难恢复 |

**一句话选择**：
- 有网络、要同步 → 用 ① Git
- 没网络、要搬运整套 → 用 ② 分发包
- 改坏了、要回到过去某个状态 → 用 ③ 备份快照

---

## 一、迁移到另一台新电脑

### 方式 A：用 Git（推荐）

适合有网络的情况，拉下来就是最新的，还能持续同步。

**前提**：新电脑装了 git，且配好了 GitHub 凭证（见第五节）。

```bash
# 1. 克隆仓库
git clone https://github.com/Leib603/wb-work-model.git

# 2. 进入目录
cd wb-work-model

# 3. 生成各平台适配文件
python build.py
```

完成后，你会得到完整的工作模型。`adapters/` 下是 5 个平台适配文件，`source/` 是真相源。

**验证**：打开 `adapters/01-对话类AI-主提示词.md`，确认里面有 `WB` 和 `Leib` 字样。

### 方式 B：用分发包（无 Git / 无网络）

适合不方便用 Git 的情况，比如临时电脑、公司受限环境。

1. 从旧电脑拿到 `work-model-package.zip`（拷贝方式见第四节）
2. 在新电脑上解压，得到 `work-model/` 文件夹
3. 进入文件夹，跑一次：
   ```bash
   cd work-model
   python build.py
   ```
4. 完成。该文件夹就是完整工作模型，可正常维护。

> 说明：zip 里已经带了生成好的 `adapters/`，所以即使暂时没 Python，也能直接打开里面的主提示词文件使用。跑 `build.py` 只是为了在改动后刷新适配。

---

## 二、从备份恢复（模型改坏了 / 回到过去）

备份快照是"救命绳"——它是自包含的，解压出来就是一整套能用的工作模型。

### 场景 1：当前电脑改坏了，要回退

在 `work-model/` 目录下：

```bash
# 看看有哪些备份
python restore.py list

# 安全提取最新备份到 restored/ 目录（不动当前工作区）
python restore.py latest

# 确认 restored/ 里的内容没问题后，用它覆盖当前工作区
python restore.py latest --apply
```

**保险机制**（放心操作）：
- 恢复前会自动把"当前坏掉的状态"存成一份新快照——万一回退错了，还能再退回来
- 恢复前校验 SHA256，快照损坏会被拒绝
- 默认先提取到独立目录，给你检查的机会，`--apply` 才真正覆盖

### 场景 2：只拿到一个备份 zip，想直接用

比如从云盘/微信里拿到 `LATEST.zip` 或某个 `snapshot-*.zip`：

1. 解压这个 zip，得到一整套文件（含 `source/`、`adapters/`、`build.py` 等）
2. 因为它是自包含的，解压后**直接就是可用的人工模型**
3. 有 Python 就跑一次 `python build.py` 刷新适配
4. 想把它作为新工作区，把解压出的文件夹当作 `work-model/` 用即可

> 关键认知：备份 zip 和分发包 zip 都是"解压即用"的完整工作模型，区别在于备份带了时间戳和校验、专为回退设计。

---

## 三、导入到手机

手机不能跑 git 命令、通常也没 Python，所以走"查看 + 粘贴"路线。

### 方式 A：用 GitHub App（能联网、想随时看最新版）

1. 手机安装 GitHub App，登录 `Leib603`
2. 打开私有仓库 `wb-work-model`
3. 直接在线查看任何文件；需要改就在网页上编辑并 commit
4. 要用的时候，打开 `adapters/04-手机速用版.md`，复制内容粘贴到手机 AI 对话开头

> 在手机上改了文件后，电脑端执行 `git pull` 就能拿到改动。

### 方式 B：把文件传到手机（没装 GitHub App）

1. 在电脑上把 `work-model-package.zip` 传到手机（微信文件传输助手、云盘、邮件、数据线都行）
2. 手机解压，打开 `adapters/04-手机速用版.md`
3. 复制全文，粘贴到手机上的 AI（ChatGPT / Claude / Gemini App）对话开头

> 手机端不需要跑任何脚本——`04-手机速用版.md` 是专门精简过的，复制粘贴即可恢复身份和上下文。

---

## 四、文件怎么在设备间拷贝

根据需要选一种：

| 途径 | 适合 | 操作 |
|------|------|------|
| **Git push / pull** | 电脑之间、有网络 | 最省事，见第一节方式 A |
| **微信 / QQ 文件传输** | 临时、快速 | 把 zip 发给自己，另一端下载 |
| **云盘**（腾讯微云/OneDrive/坚果云） | 长期多设备 | 把 zip 放进同步目录，各设备取用 |
| **U 盘 / 移动硬盘** | 无网络、大文件 | 拷贝 zip，插到另一台解压 |
| **邮件** | 发给自己留底 | 把 zip 作为附件发到自己的邮箱 |
| **数据线** | 电脑↔手机直连 | 直接传 zip 到手机 |

**建议**：日常靠 Git（第一节），另外把 `work-model-package.zip` 发一份到自己微信/邮箱作备份——万一 Git 出问题，还有第二份。

---

## 五、新设备配 GitHub 凭证（clone / push 的前提）

新电脑第一次用 `git clone` 私有仓库会要凭证。二选一：

**方案 A — GitHub CLI（最简单）**
```bash
# 安装 gh 后
gh auth login        # 选 GitHub.com → HTTPS → 浏览器登录
git config --global user.name "Leib603"
git config --global user.email "你的GitHub邮箱"
```

**方案 B — 个人访问令牌（PAT）**
1. GitHub → Settings → Developer settings → Personal access tokens → 生成勾选 `repo` 的令牌
2. 配置：
```bash
git config --global user.name "Leib603"
git config --global user.email "你的GitHub邮箱"
git config --global credential.helper manager
# 首次 push/clone 时粘贴令牌
```

> 当前这台机器已配好凭证，能直接 clone/push，无需再做这步。

---

## 六、导入完成后，必做验证清单

搬到新设备后，逐条确认，确保模型真的可用：

- [ ] `source/` 下有 identity / memory / skills / knowledge 四类文件
- [ ] `adapters/` 下有 5 个适配文件
- [ ] 跑 `python build.py` 不报错
- [ ] 打开 `adapters/01-对话类AI-主提示词.md`，能看到 `WB` 和 `Leib`
- [ ] 把主提示词粘贴到一个全新 AI 对话，问它"你是谁、我是谁"，能正确回答
- [ ] （Git 设备）`git status` 显示干净，`git log` 能看到历史提交

**终极测试**（来自社区实践）：把主提示词粘贴到全新 AI，问三个问题——
1. "我这个任务最可能误解什么？"
2. "用我的语气起草，但标出你在猜的地方。"
3. "如果我按这个发出去，会违反我自己的哪条规则？"

如果回答能具体引用你的工作背景，说明模型迁移成功；如果只是客套话，说明真相源还不够具体，需要补充。

---

## 七、常见问题排查

**Q：clone 时提示 403 / Repository not found？**
A：私有仓库需要凭证且账号要有权限。按第五节配置凭证。确认登录的是 `Leib603`。

**Q：push 时提示冲突（rejected / non-fast-forward）？**
A：别的设备先推过改动。执行 `git pull` 合并后再 `git push`。

**Q：解压 zip 后找不到 adapters/？**
A：确认解压的是完整的 `work-model-package.zip` 或快照包，不是单个文件。解压后应看到一个文件夹，里面有 `source/`、`adapters/`。

**Q：手机上打不开 zip？**
A：用系统自带的文件 App 或解压工具（如 iZip、ZArchiver）。或者直接跳过解压——在 GitHub App 里在线打开 `04-手机速用版.md` 复制即可。

**Q：恢复后发现有内容不对？**
A：正因为有"恢复前自动备份"机制，`restore.py list` 里会有恢复前存的那份快照。再执行一次 `restore.py <那份快照> --apply` 即可退回。

---

## 八、日常维护节奏

- 每次重要改动后：`python build.py` 刷新适配，然后 `git add -A && git commit && git push`
- 重要节点（大改前、每月回顾）：`python backup.py 备注` 留一份自包含快照
- 每月：回顾 `source/`，补上变真的、删掉不再适用的，在 `source/memory/decisions/` 留下带日期的说明

---

_本手册位于 `work-model/MIGRATION.md`，会随 `build.py` 一起进入分发包，随 Git 一起同步。_
