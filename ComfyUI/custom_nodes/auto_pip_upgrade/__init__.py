# -*- coding: utf-8 -*-
"""auto_pip_upgrade — автоматическое обновление pip для портативной сборки.

Проблема: pip при каждом запуске пишет
    [!] [notice] A new release of pip is available: 26.1.1 -> 26.2.2

Решение: при старте ComfyUI (в фоне, чтобы не замедлять загрузку) узел
проверяет актуальную версию pip на PyPI и, если вышел новый релиз,
обновляет pip один раз. Пока ComfyUI работает — проверка не повторяется
("при первом обнаружении").

Отключение: установить переменную окружения PIP_AUTO_UPGRADE=0
(например, в launcher_config.json -> extra_args не поможет, ставьте
через свойства системы или bat-файл). По умолчанию включено.

Узел ничего не добавляет в граф (NODE_CLASS_MAPPINGS пуст).
"""

import json
import logging
import os
import subprocess
import sys
import threading
import time
import urllib.request

_CHECK_DELAY_SEC = 90   # подождать загрузку ComfyUI, чтобы не мешать старту
_HTTP_TIMEOUT_SEC = 20
_UPGRADE_TIMEOUT_SEC = 900

_NAME = "auto_pip_upgrade"


def _log_info(msg, *args):
    logging.info("[%s] " + msg, _NAME, *args)


def _log_warning(msg, *args):
    logging.warning("[%s] " + msg, _NAME, *args)


def _current_pip_version():
    r = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        capture_output=True, text=True, timeout=60,
    )
    # Пример вывода: "pip 26.1.1 from E:\\...\\site-packages\\pip (python 3.13)"
    return r.stdout.strip().split()[1]


def _latest_pip_version():
    url = "https://pypi.org/pypi/pip/json"
    req = urllib.request.Request(url, headers={"User-Agent": "comfy_v1-auto-pip-upgrade"})
    with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT_SEC) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["info"]["version"]


def _version_tuple(v):
    # Для версий pip вида "26.2.2" достаточно числового сравнения;
    # нечисловые части (если появятся) сравниваем как строки.
    parts = []
    for p in v.split("."):
        num, _, _rest = p.partition("_")
        try:
            parts.append((0, int(num)))
        except ValueError:
            parts.append((1, num))
    return parts


def run_check_once():
    """Одна проверка: если есть новый pip — обновить. Возвращает True при обновлении."""
    try:
        current = _current_pip_version()
    except Exception as e:  # noqa: BLE001
        _log_warning("не удалось определить текущую версию pip: %s", e)
        return False

    try:
        latest = _latest_pip_version()
    except Exception as e:  # noqa: BLE001
        _log_info("нет доступа к PyPI (%s), проверка пропущена", e)
        return False

    if _version_tuple(latest) <= _version_tuple(current):
        _log_info("pip %s актуален (PyPI: %s)", current, latest)
        return False

    _log_info("обнаружен новый релиз pip: %s -> %s, обновляю...", current, latest)
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip",
             "--disable-pip-version-check", "--quiet"],
            capture_output=True, text=True, timeout=_UPGRADE_TIMEOUT_SEC,
        )
        if r.returncode == 0:
            _log_info("pip обновлён: %s -> %s", current, latest)
            return True
        _log_warning("pip вернул код %s: %s", r.returncode, (r.stderr or r.stdout or "").strip()[-500:])
        return False
    except Exception as e:  # noqa: BLE001
        _log_warning("ошибка обновления pip: %s", e)
        return False


def _patch_frontend_locales():
    """Самовосстановление: удаляет zh/zh-TW из карты языков фронтенда.

    При обновлении comfyui-frontend-package через Manager патч (см.
    E:\\comfy_v1\\patch_frontend_zh.py) затирается — здесь он повторяется
    автоматически при старте. Идемпотентно: чистые файлы не трогает.
    """
    import glob
    import re

    base = os.path.join(sys.prefix, "Lib", "site-packages",
                        "comfyui_frontend_package", "static", "assets")
    re_zh = re.compile(r",zh:\{text:`[^`]*`,loaders:loadersFor\(`zh`\)\}")
    re_zhtw = re.compile(r',"zh-TW":\{text:`[^`]*`,loaders:loadersFor\(`zh-TW`\)\}')
    patched = 0
    try:
        for path in glob.glob(os.path.join(base, "i18n-*.js")):
            with open(path, encoding="utf-8") as f:
                s = f.read()
            orig = s
            s = re_zh.sub("", s)
            s = re_zhtw.sub("", s)
            if s != orig and "中文" not in s:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(s)
                patched += 1
        if patched:
            _log_info("патч языков фронтенда применён заново (файлов: %s) — "
                      "китайский в списке языков вырезан", patched)
    except Exception as e:  # noqa: BLE001
        _log_warning("не удалось применить патч языков фронтенда: %s", e)


def _worker():
    time.sleep(_CHECK_DELAY_SEC)
    run_check_once()
    _patch_frontend_locales()


def _start():
    import os
    if os.environ.get("PIP_AUTO_UPGRADE", "1").strip().lower() in ("0", "false", "off", "no"):
        _log_info("отключено через PIP_AUTO_UPGRADE=0")
        return
    t = threading.Thread(target=_worker, name=_NAME, daemon=True)
    t.start()


_start()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "run_check_once"]
