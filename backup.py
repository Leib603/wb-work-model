#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WB 工作模型 · 备份器
====================
生成一个「自包含快照包」：解压出来就是一整套完整可用的工作模型，
附带 SHA256 校验清单。出问题时用 restore.py 把备份提出来即可用。

用法：
    python backup.py [备注]      例：python backup.py 建仓前

特性：
    - 时间戳命名，保留最近 KEEP 份，自动清理更旧的
    - 同时更新 LATEST.zip，永远指向最新快照
    - manifest.json 记录每份快照的时间、备注、文件数、SHA256
    - 快照包内含全部真相源、适配文件、脚本、文档
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
KEEP = 5

# 不进入快照的内容
EXCLUDE_DIRS = {".git", "backups", "__pycache__", ".workbuddy"}
EXCLUDE_FILES = {"work-model-package.zip"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(ROOT).parts
        if any(d in EXCLUDE_DIRS for d in rel_parts):
            continue
        if p.name in EXCLUDE_FILES:
            continue
        files.append(p)
    return files


def main() -> None:
    note = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "手动备份"
    SNAP_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    snap_name = f"snapshot-{stamp}.zip"
    snap_path = SNAP_DIR / snap_name

    files = collect_files()
    print(f"收集到 {len(files)} 个文件，生成快照 {snap_name} ...")

    # 写入快照 zip（内部路径相对 work-model 根，解压即得完整目录）
    with zipfile.ZipFile(snap_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.relative_to(ROOT).as_posix())

    digest = sha256_file(snap_path)
    entry = {
        "name": snap_name,
        "created_at": now.isoformat(timespec="seconds"),
        "note": note,
        "file_count": len(files),
        "size_bytes": snap_path.stat().st_size,
        "sha256": digest,
    }

    # 读取已有 manifest
    manifest = {"version": 1, "snapshots": []}
    if MANIFEST.exists():
        try:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    manifest.setdefault("snapshots", [])
    manifest["snapshots"].insert(0, entry)

    # 只保留最近 KEEP 份，删除更旧的实体文件
    removed = []
    while len(manifest["snapshots"]) > KEEP:
        old = manifest["snapshots"].pop()
        old_path = SNAP_DIR / old["name"]
        if old_path.exists():
            old_path.unlink()
            removed.append(old["name"])

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 更新 LATEST.zip
    latest = BACKUP_DIR / "LATEST.zip"
    shutil.copyfile(snap_path, latest)

    print(f"  快照已保存：{snap_path.relative_to(ROOT)}")
    print(f"  快捷副本：  {latest.relative_to(ROOT)}")
    print(f"  SHA256：    {digest[:16]}...")
    if removed:
        print(f"  已清理旧备份：{', '.join(removed)}")
    print(f"\n完成。共 {len(manifest['snapshots'])} 份快照在册。")


if __name__ == "__main__":
    main()
