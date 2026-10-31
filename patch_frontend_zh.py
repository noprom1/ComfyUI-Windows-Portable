# -*- coding: utf-8 -*-
"""Универсальный патч: удаляет zh и zh-TW из карты языков фронтенда ComfyUI.
Находит актуальный чанк i18n-*.js независимо от хеша в имени (переживает
обновления comfyui-frontend-package). Идемпотентен.
"""
import re
import sys
import glob

ASSETS = r"E:\comfy_v1\python_standalone\Lib\site-packages\comfyui_frontend_package\static\assets"

# Регэкспы для записей карты языков (формат минифицированного бандла)
RE_ZH = re.compile(r",zh:\{text:`[^`]*`,loaders:loadersFor\(`zh`\)\}")
RE_ZHTW = re.compile(r',"zh-TW":\{text:`[^`]*`,loaders:loadersFor\(`zh-TW`\)\}')

candidates = sorted(glob.glob(ASSETS + r"\i18n-*.js"))
if not candidates:
    print("FAIL: no i18n-*.js chunk found")
    sys.exit(1)

patched_any = False
for path in candidates:
    s = open(path, encoding="utf-8").read()
    orig = s
    for rx in (RE_ZH, RE_ZHTW):
        s, n = rx.subn("", s)
        if n > 1:
            print("FAIL: %d matches in %s (expected <=1)" % (n, path))
            sys.exit(1)
    if s != orig:
        if "中文" in s:
            print("FAIL: Chinese glyphs still present after patch in %s" % path)
            sys.exit(1)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("PATCHED: %s (%d -> %d bytes)" % (path, len(orig), len(s)))
        patched_any = True
    else:
        if "中文" not in s and "zh:{text:" not in s:
            print("CLEAN: %s (already patched)" % path)
        else:
            print("CLEAN: %s (no zh map entries)" % path)

if not patched_any:
    print("NOTE: nothing to patch (already clean)")
print("OK")
