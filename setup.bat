@echo off
rem ============================================================
rem  Первый запуск сборки: разворачивает python_standalone
rem  и устанавливает все зависимости из requirements-файлов.
rem  Запускать ОДИН РАЗ. Далее пользуйтесь RUN_Launcher.bat
rem ============================================================
setlocal
cd /d "%~dp0"

if exist "python_standalone\python.exe" (
    echo python_standalone уже развёрнут. Зависимости можно доустановить:
    echo   python_standalone\python.exe scripts\install_requirements.py
    pause
    exit /b 0
)

echo === Шаг 1/3: скачивание Python 3.13 (python-build-standalone) ===
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\fetch_python.ps1"
if errorlevel 1 (
    echo ОШИБКА: не удалось скачать/распаковать Python.
    echo Запасной вариант: скопируйте папку python_standalone из рабочей сборки.
    pause
    exit /b 1
)

echo === Шаг 2/3: установка PyTorch + CUDA и пакетов ===
python_standalone\python.exe -m pip install --upgrade pip --disable-pip-version-check
python_standalone\python.exe scripts\install_requirements.py

echo === Шаг 3/3: готово ===
echo Теперь запустите RUN_Launcher.bat
echo Примечание: для обновления нод через ComfyUI-Manager нужен git:
echo   установите Git for Windows или положите portable-git в папку MinGit\cmd
pause
