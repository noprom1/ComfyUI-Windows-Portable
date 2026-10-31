# Скачивает и распаковывает python-build-standalone (CPython 3.13, Windows x64)
# в папку python_standalone рядом со скриптом. Используется setup.bat.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $root "python_standalone"

if (Test-Path (Join-Path $dest "python.exe")) {
    Write-Host "python_standalone уже существует, пропуск."
    exit 0
}

# Ищем последний релиз с ассетом CPython 3.13 install_only для Windows x64
$release = Invoke-RestMethod -Uri "https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest" -TimeoutSec 60
$asset = $release.assets | Where-Object { $_.name -match "^cpython-3\.13\..*x86_64-pc-windows-msvc-shared-install_only\.tar\.gz$" } | Select-Object -First 1
if (-not $asset) { throw "Не найден подходящий ассет python-build-standalone" }

$url = $asset.browser_download_url
$tmp = Join-Path $env:TEMP ("psa_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
$archive = Join-Path $tmp $asset.name

Write-Host "Скачиваю $url"
Invoke-WebRequest -Uri $url -OutFile $archive -TimeoutSec 1800

Write-Host "Распаковываю..."
New-Item -ItemType Directory -Path $dest -Force | Out-Null
tar -xzf $archive -C $dest
if ($LASTEXITCODE -ne 0) { throw "tar завершился с ошибкой" }

Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
if (-not (Test-Path (Join-Path $dest "python.exe"))) { throw "python.exe не найден после распаковки" }
Write-Host "Python развёрнут: $dest"
exit 0
