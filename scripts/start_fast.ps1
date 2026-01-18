# Script de lancement RAPIDE Whisper STT pour PowerShell
# Force Python 3.12
# Auteur: Bigmoletos
# Date: 2026-01-18

$Host.UI.RawUI.WindowTitle = "Whisper STT - Faster-Whisper (Fast)"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Whisper STT - Faster-Whisper (Fast)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $PSScriptRoot

# === DETECTION PYTHON 3.12 UNIQUEMENT ===
Write-Host "Detection de Python 3.12" -ForegroundColor Yellow

$pythonCmd = $null

# Test py -3.12
Write-Host "Test: py -3.12 --version" -ForegroundColor Gray
try {
    $result = & py -3.12 --version 2>&1 | Out-String
    $exitCode = $LASTEXITCODE

    Write-Host "Sortie: $result" -ForegroundColor Gray
    Write-Host "Code sortie: $exitCode" -ForegroundColor Gray

    if ($exitCode -eq 0 -or $result -match "Python 3\.12") {
        Write-Host "[OK] Python 3.12 trouve" -ForegroundColor Green
        $pythonCmd = @("py", "-3.12")
    } else {
        Write-Host "Echec: Code=$exitCode" -ForegroundColor Gray
    }
} catch {
    Write-Host "Exception: $($_.Exception.Message)" -ForegroundColor Gray
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "[ERREUR] Python 3.12 requis mais non trouve" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifiez manuellement:" -ForegroundColor Yellow
    Write-Host "  py -3.12 --version"
    Write-Host "  py --list"
    Write-Host ""
    Write-Host "Si Python 3.12 est installe, le probleme vient de PowerShell." -ForegroundColor Yellow
    Write-Host "Utilisez plutot le script batch:" -ForegroundColor Yellow
    Write-Host "  .\scripts\start_fast.bat" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

Write-Host ""
Write-Host "Commande Python: py -3.12" -ForegroundColor Cyan
Write-Host ""

# === VERIFICATION CONFIG ===
Write-Host "Verification de la configuration" -ForegroundColor Yellow

try {
    & py -3.12 scripts\config_checker.py
    if ($LASTEXITCODE -ne 0) {
        throw "Config error"
    }
} catch {
    Write-Host "[ERREUR] Probleme avec la configuration" -ForegroundColor Red
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

Write-Host ""

# === VERIFICATION FASTER-WHISPER ===
Write-Host "Verification de faster-whisper" -ForegroundColor Yellow

try {
    $null = & py -3.12 -c "import faster_whisper" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] faster-whisper est installe" -ForegroundColor Green
    } else {
        throw "Not installed"
    }
} catch {
    Write-Host "[INFO] faster-whisper n'est pas installe" -ForegroundColor Yellow
    Write-Host ""

    if ($env:VIRTUAL_ENV) {
        Write-Host "Installation de faster-whisper" -ForegroundColor Yellow
        & py -3.12 -m pip install faster-whisper
    } else {
        Write-Host "Installation de faster-whisper en mode utilisateur" -ForegroundColor Yellow
        & py -3.12 -m pip install faster-whisper --user
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERREUR] Installation de faster-whisper a echoue" -ForegroundColor Red
        Write-Host ""
        Write-Host "SOLUTIONS:" -ForegroundColor Yellow
        Write-Host "1. Installez Rust: https://rustup.rs/"
        Write-Host "2. OU changez config.json pour utiliser engine: whisper"
        Write-Host ""
        Read-Host "Appuyez sur Entree pour quitter"
        exit 1
    }
}

# === VERIFICATION DEPENDANCES ===
Write-Host ""
Write-Host "Verification des dependances" -ForegroundColor Yellow

try {
    $null = & py -3.12 -c "import sounddevice" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installation des dependances supplementaires" -ForegroundColor Yellow
        if ($env:VIRTUAL_ENV) {
            & py -3.12 -m pip install sounddevice numpy pywin32 pynput win10toast
        } else {
            & py -3.12 -m pip install sounddevice numpy pywin32 pynput win10toast --user
        }
    }
} catch { }

# === LANCEMENT APPLICATION ===
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Demarrage de l'application" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Raccourci: Ctrl+Alt+7" -ForegroundColor Yellow
Write-Host "Arret: Ctrl+C" -ForegroundColor Yellow
Write-Host ""

& py -3.12 -m src.main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Application terminee" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERREUR] Erreur code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host ""
Read-Host "Appuyez sur Entree pour quitter"
