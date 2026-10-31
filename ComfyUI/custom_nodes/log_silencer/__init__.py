# -*- coding: utf-8 -*-
"""log_silencer — глушит шумные deprecation-предупреждения в логе ComfyUI.

ComfyUI (server.py, middleware deprecation_warning) пишет в лог
[DEPRECATION WARNING] при каждом первом импорте браузером легаси-шимов
(/scripts/ui*, /extensions/core/*). Эти импорты делают десятки сторонних
кастом-нод, и предупреждение не является ошибкой — шимы продолжают
работать (совместимость сохраняется до выкидывания легаси-API).

Этот узел добавляет фильтр на корневой логгер, который убирает из лога
только эти строки. Никакие файлы ComfyUI не модифицируются (обновления
git не затрагиваются), удалив папку — вернёте стандартное поведение.

Чтобы вернуть предупреждения: удалите эту папку и перезапустите ComfyUI.
"""

import logging

_MARKER = "[DEPRECATION WARNING] Detected import of deprecated legacy API"


class _DeprecationLogFilter(logging.Filter):
    def filter(self, record):
        try:
            return _MARKER not in record.getMessage()
        except Exception:
            return True


_f = _DeprecationLogFilter()
logging.getLogger().addFilter(_f)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
