# -*- coding: utf-8 -*-
"""tl_bridge — подключает пользовательские переводы интерфейса из папки tl\\.

Папка tl\\ лежит в корне портативной сборки (рядом с ComfyUI\\).
ComfyUI подхватывает переводы из custom_nodes/*/locales/<lang>/*.json,
поэтому этот узел создаёт junction-ссылку:
    ComfyUI\\custom_nodes\\tl_bridge\\locales  ->  <корень сборки>\\tl

Структура перевода (см. tl\\README.txt):
    tl\\<lang>\\main.json        — тексты интерфейса фронтенда
    tl\\<lang>\\nodeDefs.json    — названия и описания нод
    tl\\<lang>\\commands.json    — команды (меню, хоткеи)
    tl\\<lang>\\settings.json    — названия настроек

Ссылка пересоздаётся при каждом старте ComfyUI с актуальным абсолютным
путём, поэтому сборка остаётся переносимой (относительные пути).
После добавления/изменения файлов перевода перезапустите ComfyUI.

NODE_CLASS_MAPPINGS пуст — этот узел ничего не добавляет в граф,
он только обслуживает папку переводов.
"""

import logging
import os
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_COMFYUI_ROOT = os.path.dirname(os.path.dirname(_HERE))  # custom_nodes/tl_bridge -> custom_nodes -> ComfyUI
_PACK_ROOT = os.path.dirname(_COMFYUI_ROOT)              # корень портативной сборки (E:\comfy_v1)
_TL_DIR = os.path.join(_PACK_ROOT, "tl")
_LINK = os.path.join(_HERE, "locales")


def _ensure_link():
    """Создаёт/обновляет junction locales -> tl (идемпотентно, portable-safe)."""
    try:
        os.makedirs(_TL_DIR, exist_ok=True)
        target = os.path.realpath(_TL_DIR)
        current = os.path.realpath(_LINK) if os.path.lexists(_LINK) else None
        if current == target:
            return True
        if os.path.lexists(_LINK):
            if os.path.isdir(_LINK) and not os.path.islink(_LINK) and os.listdir(_LINK):
                logging.warning("[tl_bridge] %s существует как обычная непустая папка, не трогаю", _LINK)
                return False
            os.rmdir(_LINK)  # junction/symlink или пустая папка
        # mklink /J <link> <target> — junction не требует прав администратора
        r = subprocess.run(
            ["cmd", "/c", "mklink", "/J", _LINK, _TL_DIR],
            check=True, capture_output=True,
        )
        logging.info("[tl_bridge] создан junction %s -> %s", _LINK, _TL_DIR)
        return True
    except Exception as e:  # noqa: BLE001
        logging.warning("[tl_bridge] не удалось создать ссылку на tl: %s", e)
        return False


_ensure_link()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
