# -*- coding: utf-8 -*-
"""Установка зависимостей сборки ComfyUI (requirements-torch.txt + requirements.lock.txt).

Запускается setup.bat после разворачивания python_standalone.
Логика: сначала torch-стек из индекса pytorch (cu130), затем основной lock.
Если какие-то строки lock не встают — они ставятся по одной, ошибки
собираются в requirements-failed.txt (обычно это пакеты, чьи wheel'ы
недоступны на момент установки; нужные ноды можно починить через
ComfyUI-Manager -> Try Fix).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TORCH_REQ = ROOT / "requirements-torch.txt"
LOCK = ROOT / "requirements.lock.txt"
FAILED = ROOT / "requirements-failed.txt"
PYTORCH_INDEX = "https://download.pytorch.org/whl/cu130"


def run_pip(args, timeout=3600):
    cmd = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check"] + args
    return subprocess.run(cmd).returncode


def main():
    print("=" * 60)
    print("[1/2] PyTorch + CUDA (requirements-torch.txt)")
    print("=" * 60)
    if run_pip(["-r", str(TORCH_REQ), "--index-url", PYTORCH_INDEX]) != 0:
        print("ПРЕДУПРЕЖДЕНИЕ: torch-стек установился с ошибками, продолжаю...")

    print("=" * 60)
    print("[2/2] Основной набор пакетов (requirements.lock.txt)")
    print("=" * 60)
    code = run_pip(["-r", str(LOCK)])
    if code == 0:
        print("Все пакеты установлены успешно.")
        return 0

    print("Часть пакетов не встала, пробую по одной строке...")
    lines = [l.strip() for l in LOCK.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.strip().startswith("#")]
    failed = []
    for i, line in enumerate(lines, 1):
        rc = run_pip([line])
        if rc != 0:
            print(f"  FAILED [{i}/{len(lines)}]: {line}")
            failed.append(line)
    FAILED.write_text("\n".join(failed) + ("\n" if failed else ""), encoding="utf-8")
    print(f"Готово. Не установилось: {len(failed)} (список: {FAILED.name}).")
    print("ComfyUI может работать и без них; недостающее для конкретных нод")
    print("доставляется через ComfyUI-Manager -> Try Fix.")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
