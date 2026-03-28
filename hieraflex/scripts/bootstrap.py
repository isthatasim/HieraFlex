from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import venv
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def venv_python(venv_dir: Path) -> Path:
    if platform.system().lower().startswith("win"):
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def ensure_venv(venv_dir: Path) -> Path:
    if not venv_dir.exists():
        print(f"Creating virtual environment at {venv_dir}")
        venv.create(str(venv_dir), with_pip=True)
    py = venv_python(venv_dir)
    if not py.exists():
        raise RuntimeError(f"Virtual environment Python not found: {py}")
    return py


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap deterministic HieraFlex dev environment")
    parser.add_argument("--venv", default=".venv", help="Virtual environment directory")
    parser.add_argument("--with-frontend", action="store_true", help="Install frontend npm dependencies")
    parser.add_argument("--skip-editable", action="store_true", help="Skip editable install")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    os.chdir(project_root)

    venv_dir = (project_root / args.venv).resolve()
    py = ensure_venv(venv_dir)

    lock_file = project_root / "requirements-lock.txt"
    if not lock_file.exists():
        raise FileNotFoundError(f"Missing lock file: {lock_file}")

    run([str(py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    run([str(py), "-m", "pip", "install", "-r", str(lock_file)])

    if not args.skip_editable:
        run([str(py), "-m", "pip", "install", "-e", ".", "--no-deps"])

    if args.with_frontend:
        frontend = project_root / "frontend"
        run(["npm", "install"], cwd=frontend)

    print("\nBootstrap complete.")
    if platform.system().lower().startswith("win"):
        print(f"Activate with: {venv_dir}\\Scripts\\Activate.ps1")
    else:
        print(f"Activate with: source {venv_dir}/bin/activate")
    print("Run tests with: pytest -q")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
