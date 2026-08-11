# Solo Companion — Windows install
# Run with: irm <url-to-this-file> | iex
$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/scoots31/solo-companion.git"
$InstallDir = Join-Path $env:USERPROFILE "Developer\Solo Companion"
$StartupDir = [Environment]::GetFolderPath("Startup")
$Port = 8710

Write-Host "Installing Solo Companion..."

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is required. Install it from https://git-scm.com, then run this again."
    exit 1
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is required. Install it from https://python.org, then run this again."
    exit 1
}

New-Item -ItemType Directory -Force -Path (Join-Path $env:USERPROFILE "Developer") | Out-Null

if (Test-Path $InstallDir) {
    Write-Host "Found an existing install - updating it..."
    git -C $InstallDir pull
} else {
    Write-Host "Downloading..."
    git clone $RepoUrl $InstallDir
}

$VenvPython = Join-Path $InstallDir ".venv\Scripts\python.exe"
$VenvPip = Join-Path $InstallDir ".venv\Scripts\pip.exe"

if (-not (Test-Path $VenvPython)) {
    python -m venv (Join-Path $InstallDir ".venv")
}
& $VenvPip install --quiet --upgrade pip flask

# Small launcher that runs the app hidden and keeps a log — used for both
# this session's start and every future login, so companion.log always
# reflects the most recent run.
$RunnerPath = Join-Path $InstallDir "run.bat"
@"
@echo off
cd /d "%~dp0"
".venv\Scripts\pythonw.exe" "app.py" >> companion.log 2>&1
"@ | Set-Content -Path $RunnerPath -Encoding ASCII

# Startup shortcut — runs at login with no console window
$WScriptShell = New-Object -ComObject WScript.Shell
$StartupShortcut = $WScriptShell.CreateShortcut((Join-Path $StartupDir "Solo Companion.lnk"))
$StartupShortcut.TargetPath = $RunnerPath
$StartupShortcut.WorkingDirectory = $InstallDir
$StartupShortcut.WindowStyle = 7  # minimized — no visible window
$StartupShortcut.Save()

# Desktop shortcut to the app itself
$DesktopShortcut = $WScriptShell.CreateShortcut((Join-Path $env:USERPROFILE "Desktop\Solo Companion.url"))
$DesktopShortcut.TargetPath = "http://localhost:$Port"
$DesktopShortcut.Save()

# Start it now for this session
Start-Process -FilePath $RunnerPath -WorkingDirectory $InstallDir -WindowStyle Hidden

Write-Host "Starting..."
$started = $false
for ($i = 0; $i -lt 15; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port" -UseBasicParsing -TimeoutSec 1
        if ($response.StatusCode -eq 200) { $started = $true; break }
    } catch {}
    Start-Sleep -Seconds 1
}

if ($started) {
    Start-Process "http://localhost:$Port"
    Write-Host ""
    Write-Host "Solo Companion is running at http://localhost:$Port"
    Write-Host "It'll start automatically from now on - a shortcut is on your Desktop."
    Write-Host "First launch will ask you to point it at the same folder you installed the Framework into."
} else {
    Write-Host "Didn't start within 15 seconds - check $InstallDir\companion.log for what went wrong."
    exit 1
}
