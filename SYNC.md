# 跨设备同步说明

工作模型已托管在私有 Git 仓库：**https://github.com/Leib603/wb-work-model**

## 这套同步怎么运作

```
本地 work-model/  ──push──>  私有仓库 GitHub  ──pull──>  其他设备
     (真相源)                   (唯一中心)               (手机/别的电脑)
```

- 只有 `source/` 和 `adapters/` 等文本文件进仓库；`work-model-package.zip` 是临时分发物，不入仓库。
- 任何设备拿到的是同一份真相源，改完 pull → 改 source → build.py → push。

## 新设备首次拉取（电脑）

前提：该设备已装 git，且已配置 GitHub 凭证（见下方"凭证配置"）。

```bash
git clone https://github.com/Leib603/wb-work-model.git
cd wb-work-model
python build.py
```

## 日常同步（任意设备，三句话）

```bash
git pull                 # 先拉取别人的改动
# ...改 source/ 里的文件，跑 python build.py...
git add -A && git commit -m "更新工作模型" && git push
```

## 手机端

手机不跑 git 命令，直接用 GitHub App：
- 安装 GitHub App 登录 Leib603，打开 `wb-work-model` 仓库即可**在线查看和编辑** Markdown。
- 改完在网页提交，电脑上 `git pull` 就能拿到。
- 要粘贴到手机上的 AI 时，直接打开 `adapters/04-手机速用版.md` 复制内容。

## 凭证配置（本地 git 推送需要，一次性）

当前这台电脑的 git 没有配置凭证，所以首次推送由 WorkBuddy 通过连接器完成；你后续要在本机用命令行 push，需二选一：

**方案 A — 装 GitHub CLI（最简单）**
```bash
# 安装 gh 后：
gh auth login        # 按提示选 GitHub.com → HTTPS → 浏览器登录
git config --global user.name "Leib603"
git config --global user.email "你的GitHub邮箱"
```

**方案 B — 用个人访问令牌（PAT）**
1. GitHub → Settings → Developer settings → Personal access tokens → 生成勾选 `repo` 的令牌
2. 配置：
```bash
git config --global user.name "Leib603"
git config --global user.email "你的GitHub邮箱"
git config --global credential.helper manager   # Windows 用凭据管理器，首次 push 时粘贴令牌
```

## 安全提醒

- 仓库是**私有**的，只有 Leib603 可见。
- 但真相源里含你的个人身份和偏好。若将来要公开仓库，先把 `source/identity/` 和 `source/memory/` 移出或脱敏。
