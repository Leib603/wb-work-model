# 恢复到 WorkBuddy

> 生成日期：2026-11-19
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
