#!/usr/bin/env python3
"""Canonical build harness - reference implementation.

Copy this file to tools/build.py when a project needs reproducible builds.
Per the rule of origin (04-repo-standard-files.md), improvements are made
in the conventions repo first, then propagated to projects.

Stage pipeline (stages auto-skip when their inputs are absent):

  1. clean      rm build/, dist/, src/<pkg>/static/dist
  2. frontend   frontend/package.json present -> npm ci, npm test, npm run build
  3. deps       PyInstaller importable -> use current env, else build/venv
  4. exe        packaging/*.spec found -> pyinstaller --noconfirm <spec>
  5. stamp      dist/<App>.exe = latest (stable name),
                dist/<App>-<version>-<YYYYmmdd-HHMM>.exe = versioned copy
  6. self-test  <exe> --self-test, nonzero exit fails the build
  7. inventory  dist/INVENTORY.json: name, size, sha256, git rev, timestamp
  8. docker     only with --docker: docker build, tag :<version> and :latest

Usage:
  python tools/build.py              # exe build, whatever the repo supports
  python tools/build.py --docker     # additionally build the docker image
  python tools/build.py --no-self-test

Linux exe: run this same script inside a Linux build container (python
slim + build-essential + WebKitGTK dev headers) with the repo mounted.
Python is not cross-compilable - the binary is always produced on (or in)
the target OS.

stdlib only. No configuration file: the repo layout is the contract
(see 03-project-structure.md, 09-packaging-desktop.md).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def pyproject() -> dict:
    with open(ROOT / "pyproject.toml", "rb") as f:
        return tomllib.load(f)


def package_name() -> str:
    """Distribution name -> importable package name."""
    return pyproject()["project"]["name"].replace("-", "_")


def version() -> str:
    """Single source of truth: __version__ in the package itself."""
    sys.path.insert(0, str(ROOT / "src"))
    return str(importlib.import_module(package_name()).__version__)


def run(cmd: list[str], **kw) -> None:
    if kw.get("cwd") is None:
        kw["cwd"] = ROOT
    print(f">>> {' '.join(str(c) for c in cmd)}", flush=True)
    r = subprocess.call([str(c) for c in cmd], **kw)
    if r:
        raise SystemExit(f"stage failed ({r}): {' '.join(str(c) for c in cmd)}")


def npm() -> str:
    return "npm.cmd" if sys.platform == "win32" else "npm"


def stage_clean() -> None:
    for p in (ROOT / "build", ROOT / "dist",
              ROOT / "src" / package_name() / "static" / "dist"):
        shutil.rmtree(p, ignore_errors=True)


def stage_frontend() -> bool:
    """Build frontend if a frontend/package.json exists. Returns True if built."""
    frontend = ROOT / "frontend"
    if not (frontend / "package.json").exists():
        return False
    run([npm(), "ci"], cwd=frontend)
    pkg_scripts = json.loads((frontend / "package.json").read_text(
        encoding="utf-8")).get("scripts", {})
    if "test" in pkg_scripts:
        run([npm(), "test"], cwd=frontend)
    run([npm(), "run", "build"], cwd=frontend)
    return True


def stage_deps() -> str:
    """Return the python executable carrying PyInstaller."""
    if importlib.util.find_spec("PyInstaller"):
        return sys.executable
    venv = ROOT / "build" / "venv"
    py = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not py.exists():
        run([sys.executable, "-m", "venv", venv])
        run([py, "-m", "pip", "install", "-q", "--upgrade", "pip"])
        run([py, "-m", "pip", "install", "-q", "-e", ".[desktop],pyinstaller"])
    return str(py)


def stage_exe(py: str) -> list[Path]:
    specs = sorted((ROOT / "packaging").glob("*.spec"))
    before = set((ROOT / "dist").glob("*")) if (ROOT / "dist").exists() else set()
    for spec in specs:
        run([py, "-m", "PyInstaller", "--noconfirm", spec])
    if not (ROOT / "dist").exists():
        return []
    return [p for p in (ROOT / "dist").iterdir()
            if p not in before and p.suffix in (".exe", "") and p.is_file()]


def stage_stamp(artifacts: list[Path]) -> list[Path]:
    """latest + versioned copy; returns all shipped artifacts."""
    ver, ts = version(), datetime.now().strftime("%Y%m%d-%H%M")
    out = []
    for exe in artifacts:
        stem, suffix = exe.stem, exe.suffix
        versioned = exe.with_name(f"{stem}-{ver}-{ts}{suffix}")
        shutil.copy2(exe, versioned)
        out += [exe, versioned]
    return out


def stage_self_test(artifacts: list[Path]) -> None:
    latest = [a for a in artifacts if "-" + version() not in a.stem]
    for exe in latest:
        run([exe, "--self-test"])


def stage_inventory(artifacts: list[Path]) -> None:
    rev = subprocess.run(["git", "rev-parse", "--verify", "HEAD"],
                         capture_output=True, text=True, cwd=ROOT).stdout.strip()
    inv = [{"name": a.name, "size": a.stat().st_size,
            "sha256": hashlib.sha256(a.read_bytes()).hexdigest(),
            "git": rev, "built": datetime.now().isoformat(timespec="seconds")}
           for a in artifacts]
    (ROOT / "dist" / "INVENTORY.json").write_text(
        json.dumps(inv, indent=2) + "\n", encoding="utf-8")


def stage_docker(ver: str) -> None:
    name = pyproject()["project"]["name"].lower()
    run(["docker", "build", "--no-cache", "-t", f"{name}:{ver}",
         "-t", f"{name}:latest", "."])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docker", action="store_true",
                    help="also build the docker image (CI releases)")
    ap.add_argument("--no-self-test", action="store_true")
    args = ap.parse_args()

    stage_clean()
    stage_frontend()
    py = stage_deps() if list((ROOT / "packaging").glob("*.spec")) else None
    artifacts: list[Path] = []
    if py:
        artifacts = stage_exe(py)
        artifacts = stage_stamp(artifacts)
        if not args.no_self_test:
            stage_self_test(artifacts)
        stage_inventory(artifacts)
    if args.docker:
        stage_docker(version())
    for a in artifacts:
        print(f"built {a.relative_to(ROOT)} ({a.stat().st_size // 2**20} MB)")
    print("build ok")


if __name__ == "__main__":
    main()
