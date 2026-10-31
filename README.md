# ComfyUI Portable EN — сборка с английским интерфейсом и подключаемыми переводами

Портативная сборка ComfyUI для Windows на базе [YanWenKun/ComfyUI-Windows-Portable](https://github.com/YanWenKun/ComfyUI-Windows-Portable) (GPL-3.0), доработанная:

- **Только английский интерфейс** — китайский язык и китайские зеркала вырезаны;
- **свои переводы кладутся в папку `tl\`** (например `tl\ru` — русский) и подхватываются автоматически;
- кнопка **Stop лаунчера гарантированно останавливает сервер** (Job Object);
- **pip самообновляется** при выходе новых релизов (`auto_pip_upgrade`);
- **шумные DEPRECATION-варнинги** легаси-API убраны из лога (`log_silencer`);
- вырезан китайский из списка языков фронтенда (самовосстанавливающийся патч).

## Версии стека

| Компонент | Версия |
|---|---|
| ComfyUI | v0.43.2 (2026-10-30) |
| Python | 3.13.12 (python-build-standalone) |
| PyTorch | 2.10.0 + cu130 |
| xformers | 0.0.35 |
| comfyui-frontend-package | 1.57.4 (патчен: вырезан китайский) |
| comfyui-workflow-templates | 0.11.100 |
| OS | Windows 10/11 x64, NVIDIA GPU (CUDA 13.0) |

## Установка

### Вариант А — автоматически (первый запуск)

```bat
setup.bat
```
Скачает Python 3.13 (python-build-standalone) в `python_standalone\`, установит
PyTorch cu130 (`requirements-torch.txt`) и весь зафиксированный набор пакетов
(`requirements.lock.txt`, 300+ пакетов, включая wheel'ы с GitHub для пакетов без
PyPI-дистрибутива под Windows: flash-attn, insightface-зависимости, SAM-2 и т.п.).
Затем — `RUN_Launcher.bat`.

### Вариант Б — из рабочей сборки (надёжный)

Скопируйте папку `python_standalone\` из существующей рабочей сборки в корень репо
и запустите `RUN_Launcher.bat`.

### Примечания

- `MinGit\` в репо не включён: положите туда portable-git (`cmd\git.exe`) или установите
  [Git for Windows](https://git-scm.com/download/win) — нужен Manager'у для обновления git-нод.
- Модели не входят в репо: скелет папок `ComfyUI\models\` уже создан, файлы кладутся внутрь.
- Кэши HuggingFace/Torch во время работы пишутся в `HuggingFaceHub\` и `TorchHome\`.

## Переводы интерфейса (папка `tl\`)

Базовый язык — английский. Доступные коды языков (встроенный список фронтенда):

`en`, `ru`, `ja`, `ko`, `fr`, `es`, `ar`, `tr`, `pt-BR`, `fa`, `he`, `it`

Чтобы добавить/перекрыть перевод:

```text
tl\<код>\main.json       — тексты интерфейса
tl\<код>\nodeDefs.json   — названия и описания нод
tl\<код>\commands.json   — команды
tl\<код>\settings.json   — настройки
```

Перезапустите ComfyUI, выберите язык в Settings → Language. Пример рабочего
перевода: `tl\ru\nodeDefs.json` (переименовывает KSampler — видно сразу).
Подробности: `tl\README.txt`.

## Custom Nodes (64 шт.)

| Нода | Версия | Описание |
|---|---|---|
| [auto_pip_upgrade](https://github.com/search?q=auto_pip_upgrade&type=repositories) | в составе сборки (без git) | [служебная] автообновление pip + самовосстановление выреза китайского языка фронтенда |
| [cg-use-everywhere](https://github.com/search?q=cg-use-everywhere&type=repositories) | `1e1d25f` (2026-10-26) | Use Everywhere: широковещательные связи без проводов |
| [comfy_mtb](https://github.com/search?q=comfy_mtb&type=repositories) | `b35b5d8` (2026-07-04) | Утилиты mtb: INSIGHTFACE, анимация, дев-инструменты |
| [ComfyLiterals](https://github.com/search?q=ComfyLiterals&type=repositories) | `bdddb08` (2023-11-19) | Литералы и переменные в графе |
| [ComfyUI-Advanced-ControlNet](https://github.com/search?q=ComfyUI-Advanced-ControlNet&type=repositories) | `27a67fe` (2026-07-28) | Расширенное управление ControlNet (мультиконтролы, веса) |
| [ComfyUI-AnimateDiff-Evolved](https://github.com/search?q=ComfyUI-AnimateDiff-Evolved&type=repositories) | `9257651` (2026-07-28) | AnimateDiff: анимация диффузией |
| [ComfyUI-bleh](https://github.com/search?q=ComfyUI-bleh&type=repositories) | `1c2bc62` (2026-09-16) | Утилиты bleh: латенты, k-сэмплеры |
| [ComfyUI-Crystools](https://github.com/search?q=ComfyUI-Crystools&type=repositories) | `2f18256` (2025-10-26) | Монитор GPU/CPU/RAM, сравнение изображений, утилиты |
| [ComfyUI-Custom-Scripts](https://github.com/search?q=ComfyUI-Custom-Scripts&type=repositories) | `609f3af` (2026-02-12) | pysssss: автодополнение промптов, улучшения виджетов |
| [ComfyUI-DepthAnythingV2](https://github.com/search?q=ComfyUI-DepthAnythingV2&type=repositories) | `5531878` (2026-03-06) | Карты глубины Depth Anything V2 |
| [ComfyUI-DepthCrafter-Nodes](https://github.com/search?q=ComfyUI-DepthCrafter-Nodes&type=repositories) | `f469414` (2025-05-04) | Видео-глубина DepthCrafter |
| [ComfyUI-Detail-Daemon](https://github.com/search?q=ComfyUI-Detail-Daemon&type=repositories) | `3394e44` (2026-08-18) | Управление уровнем детализации при сэмплировании |
| [ComfyUI-DyPE](https://github.com/search?q=ComfyUI-DyPE&type=repositories) | в составе сборки (без git) | DyPE: экстраполяция разрешения диффузионных моделей |
| [ComfyUI-Easy-Use](https://github.com/search?q=ComfyUI-Easy-Use&type=repositories) | `b0b47ca` (2026-10-21) | Крупный пакет упрощения пайплайнов (лойлоды, сэмплеры, пайплайны) |
| [ComfyUI-Florence2](https://github.com/search?q=ComfyUI-Florence2&type=repositories) | `9ece3de` (2026-05-06) | Florence-2: детекция объектов, капшенинг, OCR |
| [ComfyUI-Frame-Interpolation](https://github.com/search?q=ComfyUI-Frame-Interpolation&type=repositories) | `26545cc` (2026-03-29) | Интерполяция кадров: RIFE, FILM |
| [ComfyUI-GGUF](https://github.com/search?q=ComfyUI-GGUF&type=repositories) | `edd981b` (2026-09-21) | Загрузка диффузоров в формате GGUF |
| [ComfyUI-IC-Light-Native](https://github.com/search?q=ComfyUI-IC-Light-Native&type=repositories) | `40883a8` (2025-02-26) | IC-Light: переработка освещения изображений |
| [ComfyUI-Image-Analysis-Tools](https://github.com/search?q=ComfyUI-Image-Analysis-Tools&type=repositories) | `5a26d6e` (2026-08-13) | Инструменты анализа изображений |
| [ComfyUI-Image-Saver](https://github.com/search?q=ComfyUI-Image-Saver&type=repositories) | `dbf9457` (2026-09-26) | Продвинутое сохранение изображений с метаданными |
| [ComfyUI-Image-Selector](https://github.com/search?q=ComfyUI-Image-Selector&type=repositories) | `058846b` (2025-03-16) | Интерактивный выбор изображений в графе |
| [ComfyUI-Impact-Pack](https://github.com/search?q=ComfyUI-Impact-Pack&type=repositories) | `cc015e3` (2026-10-30) | Детекция/сегментация: FaceDetailer, SEGS, апскейл лиц |
| [ComfyUI-Impact-Subpack](https://github.com/search?q=ComfyUI-Impact-Subpack&type=repositories) | `50c7b71` (2025-07-22) | Ultralytics-детекторы (bbox/segm) для Impact Pack |
| [ComfyUI-Inspire-Pack](https://github.com/search?q=ComfyUI-Inspire-Pack&type=repositories) | `d23db9a` (2025-11-18) | Расширения Impact: промпт-бэкенды, сэмплеры, блоки |
| [ComfyUI-KJNodes](https://github.com/search?q=ComfyUI-KJNodes&type=repositories) | `ab72eda` (2026-10-29) | Утилиты Kijai: маски, превью, конвейерные помощники |
| [ComfyUI-Krea2-attention-tweak](https://github.com/search?q=ComfyUI-Krea2-attention-tweak&type=repositories) | `df4c380` (2026-07-13) | Твик внимания для моделей Krea |
| [ComfyUI-layerdiffuse](https://github.com/search?q=ComfyUI-layerdiffuse&type=repositories) | `b4f6a9e` (2025-02-26) | Прозрачные PNG через LayerDiffuse |
| [ComfyUI-Lora-Manager](https://github.com/search?q=ComfyUI-Lora-Manager&type=repositories) | `1f0579a9` (2026-10-31) | Менеджер LoRA: библиотека, превью, рецепты, civitai |
| [ComfyUI-Manager](https://github.com/search?q=ComfyUI-Manager&type=repositories) | `8afdee04` (2026-10-28) | Менеджер нод: установка, обновление, удаление, снапшоты окружения |
| [comfyui-mxtoolkit](https://github.com/search?q=comfyui-mxtoolkit&type=repositories) | в составе сборки (без git) | Утилиты Mixlab: маски, текст, интеграции |
| [ComfyUI-nunchaku](https://github.com/search?q=ComfyUI-nunchaku&type=repositories) | `b600f87` (2026-09-06) | Nunchaku: INT4-инференс квантованных моделей (MIT-Han-Lab) |
| [comfyui-portrait-master](https://github.com/search?q=comfyui-portrait-master&type=repositories) | `dbf65b8` (2026-02-09) | Генератор промптов портретов |
| [ComfyUI-ppm](https://github.com/search?q=ComfyUI-ppm&type=repositories) | `e042ee9` (2026-10-31) | Вариации сэмплеров и промпт-утилиты (pamparamm) |
| [comfyui-propost](https://github.com/search?q=comfyui-propost&type=repositories) | `df6a6d1` (2024-12-25) | Постобработка: зерно, виньетка, bloom, хроматика |
| [ComfyUI-QwenVL](https://github.com/search?q=ComfyUI-QwenVL&type=repositories) | `1b67b44` (2026-09-14) | Qwen2.5-VL: описание картинок, VQA, локальный VLM |
| [ComfyUI-RadialAttn](https://github.com/search?q=ComfyUI-RadialAttn&type=repositories) | `effd401` (2025-12-19) | RadialAttention: ускорение видео-диффузии |
| [Comfyui-Resolution-Master](https://github.com/search?q=Comfyui-Resolution-Master&type=repositories) | в составе сборки (без git) | Управление разрешением/аспектом генерации |
| [ComfyUI-SeedVR2_VideoUpscaler](https://github.com/search?q=ComfyUI-SeedVR2_VideoUpscaler&type=repositories) | `4490bd1` (2025-12-24) | Видео-апскейл SeedVR2 (One-Step) |
| [comfyui-segment-anything-2](https://github.com/search?q=comfyui-segment-anything-2&type=repositories) | в составе сборки (без git) | SAM2: сегментация объектов по точкам/боксам |
| [ComfyUI-to-Python-Extension](https://github.com/search?q=ComfyUI-to-Python-Extension&type=repositories) | `6cdcc23` (2026-04-11) | Экспорт воркфлоу в Python-код |
| [ComfyUI-VideoHelperSuite](https://github.com/search?q=ComfyUI-VideoHelperSuite&type=repositories) | `4d907be` (2026-09-01) | Видео: загрузка, склейка, preview, латенты |
| [ComfyUI-WanAnimatePreprocess](https://github.com/search?q=ComfyUI-WanAnimatePreprocess&type=repositories) | `0e0b6a2` (2026-05-27) | Препроцессинг персонажей для Wan Animate |
| [ComfyUI-WanVideoWrapper](https://github.com/search?q=ComfyUI-WanVideoWrapper&type=repositories) | в составе сборки (без git) | Kijai: обёртка Wan 2.1/2.2 текст→видео/картинка→видео |
| [ComfyUI-WD14-Tagger](https://github.com/search?q=ComfyUI-WD14-Tagger&type=repositories) | `9e0a6e7` (2025-07-11) | Автотеггинг изображений (Danbooru WD14) |
| [ComfyUI_Comfyroll_CustomNodes](https://github.com/search?q=ComfyUI_Comfyroll_CustomNodes&type=repositories) | `d78b780` (2024-01-24) | XY-сетки, списки, интерфейсные и графические утилиты |
| [comfyui_controlnet_aux](https://github.com/search?q=comfyui_controlnet_aux&type=repositories) | `a587a4c` (2026-10-11) | Препроцессоры ControlNet: DWPose, depth, lineart и др. |
| [ComfyUI_essentials](https://github.com/search?q=ComfyUI_essentials&type=repositories) | `9d9f4be` (2025-04-14) | Базовые операции с изображениями, масками и латентами |
| [ComfyUI_FizzNodes](https://github.com/search?q=ComfyUI_FizzNodes&type=repositories) | `7d6ea60` (2024-10-29) | Волновые/анимационные ноды Fizz |
| [ComfyUI_IPAdapter_plus](https://github.com/search?q=ComfyUI_IPAdapter_plus&type=repositories) | `a0f451a` (2025-04-14) | IPAdapter: перенос стиля/лица из референса |
| [ComfyUI_LayerStyle](https://github.com/search?q=ComfyUI_LayerStyle&type=repositories) | `51977b2` (2026-10-10) | Слои, вырезки (RMBG), текст, PS-подобные операции |
| [ComfyUI_Mira](https://github.com/search?q=ComfyUI_Mira&type=repositories) | `dfb1c84` (2026-10-22) | Утилиты и теггер (ONNX), обработка изображений |
| [ComfyUI_smZNodes](https://github.com/search?q=ComfyUI_smZNodes&type=repositories) | `fa16c4d` (2026-10-11) | — |
| [ComfyUI_UltimateSDUpscale](https://github.com/search?q=ComfyUI_UltimateSDUpscale&type=repositories) | `a5547db` (2026-06-22) | Тайловый апскейл Ultimate SD Upscale |
| [efficiency-nodes-comfyui](https://github.com/search?q=efficiency-nodes-comfyui&type=repositories) | `4579b7d` (2026-03-31) | Скриптовые ноды: XY-plot, HiRes-Fix, стеки LoRA |
| [log_silencer](https://github.com/search?q=log_silencer&type=repositories) | в составе сборки (без git) | [служебная] глушит DEPRECATION-варнинги легаси-API в логе |
| [mikey_nodes](https://github.com/search?q=mikey_nodes&type=repositories) | `a5aa9cf` (2025-10-03) | Промптинг, сохранение с метаданными, служебные ноды |
| [minimax-h3-image-studio](https://github.com/search?q=minimax-h3-image-studio&type=repositories) | в составе сборки (без git) | Ноды MiniMax H3: генерация изображений и видео через API |
| [RES4LYF](https://github.com/search?q=RES4LYF&type=repositories) | `56e4475` (2026-10-01) | Расширенные сэмплеры: несмещённые/классические/DPM-варианты |
| [rgthree-comfy](https://github.com/search?q=rgthree-comfy&type=repositories) | `bc48c6a` (2026-10-30) | Удобства графа: мьют/байпас группами, быстрые связки, статус-нодa |
| [sd-dynamic-thresholding](https://github.com/search?q=sd-dynamic-thresholding&type=repositories) | `73e4e04` (2025-03-14) | Динамический порог CFG для высоких CFG |
| [sdxl_prompt_styler](https://github.com/search?q=sdxl_prompt_styler&type=repositories) | `5106817` (2024-03-24) | Стилизация позитив/негатив промптов по матрицам стилей |
| [tl_bridge](https://github.com/search?q=tl_bridge&type=repositories) | в составе сборки (без git) | [служебная] подключает папку tl\ как источник переводов интерфейса |
| [was-node-suite-comfyui](https://github.com/search?q=was-node-suite-comfyui&type=repositories) | `44de705` (2026-06-04) | Огромный набор текстовых и имиджевых утилит WAS |
| [z-tipo-extension](https://github.com/search?q=z-tipo-extension&type=repositories) | `549a433` (2026-10-22) | TIPO: умный теггинг и расширение промптов (Danbooru) |

Ноды устанавливались/обновлялись через ComfyUI-Manager; версии зафиксированы на
момент сборки. Модели самих нод (onnx/ckpt внутри `custom_nodes\`) в репо не входят —
скачиваются автоматически при первом использовании ноды.

## Структура

```text
ComfyUI\            — код ComfyUI + custom_nodes + скелет models
ExtraScripts\       — запуск из командной строки (run_nvidia_gpu.bat и др.)
tl\                 — пользовательские переводы интерфейса
scripts\            — bootstrap-скрипты установки
launcher.py         — GUI-лаунчер (Gooey): прокси, зеркала, параметры, внимание
setup.bat           — первичная установка окружения
RUN_Launcher.bat    — обычный запуск
patch_frontend_zh.py— ручное применение выреза китайского к фронтенду
requirements-*.txt  — зафиксированные зависимости
```

## Лицензии

- ComfyUI — GPL-3.0 (`ComfyUI\LICENSE`); данная сборка распространяется на тех же условиях.
- Базовая портативная упаковка: [YanWenKun/ComfyUI-Windows-Portable](https://github.com/YanWenKun/ComfyUI-Windows-Portable) (GPL-3.0).
- Каждая custom node — под лицензией своего автора (ссылки в таблице выше).
