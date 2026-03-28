from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 10)
WINDOWS_FALLBACK_TAG = "-3.11"
WINDOWS_PREFERRED_PY = Path("C:/ProgramData/anaconda3/python.exe")


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def capture(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def venv_python(venv_dir: Path) -> Path:
    if platform.system().lower().startswith("win"):
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def parse_ver(text: str) -> tuple[int, int]:
    parts = text.strip().split(".")
    return int(parts[0]), int(parts[1])


def parse_python_version_output(text: str) -> tuple[int, int]:
    normalized = text.strip().lower().replace("python", "").strip()
    return parse_ver(normalized)


def py_version(py_exec: Path) -> tuple[int, int]:
    out = capture([str(py_exec), "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"])
    return parse_ver(out)


def require_supported_runtime() -> list[str]:
    current = sys.version_info[:2]
    if current >= MIN_PYTHON:
        return [sys.executable, "-m", "venv"]

    if platform.system().lower().startswith("win"):
        if WINDOWS_PREFERRED_PY.exists():
            try:
                out = capture([str(WINDOWS_PREFERRED_PY), "--version"])
                if parse_python_version_output(out) >= MIN_PYTHON:
                    return [str(WINDOWS_PREFERRED_PY), "-m", "venv"]
            except Exception:
                pass
        try:
            out = capture(["py", WINDOWS_FALLBACK_TAG, "--version"])
            if out.lower().startswith("python") and parse_python_version_output(out) >= MIN_PYTHON:
                return ["py", WINDOWS_FALLBACK_TAG, "-m", "venv"]
        except Exception:
            pass

    min_txt = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
    raise SystemExit(
        f"Python {min_txt}+ is required. Current interpreter is {current[0]}.{current[1]}. "
        f"Install Python {min_txt}+ or run with an appropriate interpreter."
    )


def ensure_venv(venv_dir: Path, recreate: bool = False) -> Path:
    creator = require_supported_runtime()

    if recreate and venv_dir.exists():
        shutil.rmtree(venv_dir)

    if venv_dir.exists():
        py = venv_python(venv_dir)
        if not py.exists() or py_version(py) < MIN_PYTHON:
            shutil.rmtree(venv_dir)

    if not venv_dir.exists():
        print(f"Creating virtual environment at {venv_dir}")
        run([*creator, str(venv_dir)])

    py = venv_python(venv_dir)
    if not py.exists():
        raise RuntimeError(f"Virtual environment Python not found: {py}")

    if py_version(py) < MIN_PYTHON:
        raise RuntimeError("Created virtual environment does not satisfy Python >= 3.10")

    return py


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap deterministic HieraFlex dev environment")
    parser.add_argument("--venv", default=".venv", help="Virtual environment directory")
    parser.add_argument("--with-frontend", action="store_true", help="Install frontend npm dependencies")
    parser.add_argument("--with-optional", action="store_true", help="Install optional RL/Hugging Face extras")
    parser.add_argument("--skip-editable", action="store_true", help="Skip editable install")
    parser.add_argument("--recreate", action="store_true", help="Force recreation of the virtual environment")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    os.chdir(project_root)

    venv_dir = (project_root / args.venv).resolve()
    py = ensure_venv(venv_dir, recreate=args.recreate)

    lock_file = project_root / "requirements-lock.txt"
    if not lock_file.exists():
        raise FileNotFoundError(f"Missing lock file: {lock_file}")

    run([str(py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    run([str(py), "-m", "pip", "install", "-r", str(lock_file)])

    if args.with_optional:
        optional = project_root / "requirements-lock-optional.txt"
        if not optional.exists():
            raise FileNotFoundError(f"Missing optional lock file: {optional}")
        run([str(py), "-m", "pip", "install", "-r", str(optional)])

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
    print("Run tests with: .\\.venv\\Scripts\\python.exe -m pytest -q")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
