#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WB 工作模型 · 恢复器
====================
从快照包把工作模型提取出来使用。三重保险：
    1. 恢复前先把「当前状态」自动备份成一份快照，可反悔
    2. 恢复前校验目标快照的 SHA256，损坏则拒绝
    3. 解压到独立目录，确认无误后再由你决定是否替换

用法：
    python restore.py list              列出所有可用快照
    python restore.py latest            把最新快照提取到 restored/ 目录
    python restore.py <快照文件名>       提取指定快照
    python restore.py latest --apply    提取并直接用它覆盖当前工作区
"""

from pathlib import Path
from datetime import datetime
import zipfile
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parent
BACKUP_DIR = ROOT / "backups"
SNAP_DIR = BACKUP_DIR / "snapshots"
MANIFEST = BACKUP_DIR / "manifest.json"
LATEST = BACKUP_DIR / "LATEST.zip"
RESTORE_DIR = ROOT / "restored"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {"snapshots": []}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {"snapshots": []}


def list_snapshots() -> None:
    m = load_manifest()
    snaps = m.get("snapshots", [])
    print(f"可用快照（共 {len(snaps)} 份）：\n")
    if not snaps:
        print("  暂无快照。先运行 python backup.py 创建一份。")
        return
    for i, s in enumerate(snaps, 1):
        size_kb = s.get("size_bytes", 0) / 1024
        print(f"  {i}. {s['name']}")
        print(f"     时间：{s.get('created_at', '?')}  备注：{s.get('note', '-')}")
        print(f"     文件：{s.get('file_count', '?')} 个  大小：{size_kb:.1f} KB")
        print(f"     SHA256：{s.get('sha256', '?')[:16]}...\n")


def resolve_snapshot(arg: str) -> Path | None:
    if arg.lower() in ("latest", "last", "最新"):
        return LATEST if LATEST.exists() else None
    p = SNAP_DIR / arg
    return p if p.exists() else None


def verify(path: Path, m: dict) -> bool:
    """校验快照 SHA256 与清单一致。"""
    expected = None
    for s in m.get("snapshots", []):
        if s["name"] == path.name or (path == LATEST and s["name"] == m["snapshots"][0]["name"]):
            expected = s.get("sha256")
            break
    actual = sha256_file(path)
    if expected and actual != expected:
        print(f"  [校验失败] SHA256 不符！\n   期望：{expected}\n   实际：{actual}")
        return False
    print(f"  [校验通过] SHA256 {actual[:16]}...")
    return True


def emergency_backup() -> None:
    """恢复前先把当前状态存一份，防止误操作。"""
    try:
        import backup
        sys.argv = [sys.argv[0], "恢复前自动备份"]
        backup.main()
        print()
    except Exception as e:
        print(f"  [警告] 自动备份当前状态失败：{e}")
        print("  为安全起见，已中止恢复。请手动运行 python backup.py 后再试。")
        sys.exit(1)


def extract(snap: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    with zipfile.ZipFile(snap, "r") as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"快照内文件损坏：{bad}")
        z.extractall(target)
    print(f"  已提取到：{target.relative_to(ROOT)}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("list", "-l", "ls"):
        list_snapshots()
        return

    apply = "--apply" in args
    args = [a for a in args if a != "--apply"]
    if not args:
        list_snapshots()
        return

    m = load_manifest()
    snap = resolve_snapshot(args[0])
    if snap is None:
        print(f"找不到快照：{args[0]}")
        print("用 python restore.py list 查看可用快照。")
        sys.exit(1)

    print(f"准备恢复：{snap.name}\n")

    # 保险 1：自动备份当前状态
    print("[1/3] 备份当前状态（可反悔）...")
    emergency_backup()

    # 保险 2：校验目标快照
    print("[2/3] 校验目标快照完整性...")
    if not verify(snap, m):
        print("校验未通过，已中止恢复。")
        sys.exit(1)

    # 保险 3：提取到独立目录
    print("[3/3] 提取快照...")
    extract(snap, RESTORE_DIR)

    if apply:
        print("\n[--apply] 用快照内容覆盖当前工作区...")
        for item in RESTORE_DIR.iterdir():
            if item.name in ("backups", "restored"):
                continue
            dest = ROOT / item.name
            if dest.is_dir():
                shutil.rmtree(dest)
            elif dest.exists():
                dest.unlink()
            shutil.copytree(item, dest) if item.is_dir() else shutil.copyfile(item, dest)
        print("已覆盖。工作模型已回滚到快照状态。")
    else:
        print(f"\n完成。快照已提取到 {RESTORE_DIR.relative_to(ROOT)}，")
        print("当前工作区未被改动。确认无误后可：")
        print("  - 直接用 restored/ 里的整套文件（含 build.py）")
        print("  - 或运行 python restore.py latest --apply 覆盖当前工作区")


if __name__ == "__main__":
    main()
