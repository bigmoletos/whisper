# Script de lancement Whisper STT pour PowerShell
# Auteur: Bigmoletos
# Date: 2026-01-18

$Host.UI.RawUI.WindowTitle = "Whisper STT - Faster-Whisper"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Whisper STT - Faster-Whisper" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Aller à la racine du projet
Set-Location $PSScriptRoot

# === DETECTION PYTHON ===
Write-Host "Detection de Python" -ForegroundColor Yellow

$pythonCmd = $null
$pythonVersion = $null

# Tester py -3.12
try {
    $output = & py -3.12 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Python 3.12 trouve" -ForegroundColor Green
        Write-Host $output
        $pythonCmd = "py", "-3.12"
        $pythonVersion = "3.12"
    }
} catch { }

# Tester py -3.11
if (-not $pythonCmd) {
    try {
        $output = & py -3.11 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python 3.11 trouve" -ForegroundColor Green
            Write-Host $output
            $pythonCmd = "py", "-3.11"
            $pythonVersion = "3.11"
        }
    } catch { }
}

# Tester py -3.10
if (-not $pythonCmd) {
    try {
        $output = & py -3.10 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python 3.10 trouve" -ForegroundColor Green
            Write-Host $output
            $pythonCmd = "py", "-3.10"
            $pythonVersion = "3.10"
        }
    } catch { }
}

# Tester python
if (-not $pythonCmd) {
    try {
        $output = & python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python trouve" -ForegroundColor Green
            Write-Host $output
            $pythonCmd = "python"
        }
    } catch { }
}

# Tester py
if (-not $pythonCmd) {
    try {
        $output = & py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python trouve via py" -ForegroundColor Green
            Write-Host $output
            $pythonCmd = "py"
        }
    } catch { }
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "[ERREUR] Python non trouve" -ForegroundColor Red
    Write-Host "Installez Python 3.12 depuis: https://www.python.org/downloads/"
    Write-Host ""
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

Write-Host ""
Write-Host "Commande Python: $($pythonCmd -join ' ')" -ForegroundColor Cyan
Write-Host ""

# === VERIFICATION CONFIG ===
Write-Host "Verification de la configuration" -ForegroundColor Yellow

try {
    & $pythonCmd[0] $pythonCmd[1..($pythonCmd.Length-1)] scripts\config_checker.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERREUR] Probleme avec la configuration" -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour quitter"
        exit 1
    }
} catch {
    Write-Host "[ERREUR] Impossible d'executer config_checker.py" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

Write-Host ""

# === VERIFICATION FASTER-WHISPER ===
Write-Host "Verification de faster-whisper" -ForegroundColor Yellow

$checkCmd = $pythonCmd + @("-c", "import faster_whisper")
try {
    $null = & $checkCmd[0] $checkCmd[1..($checkCmd.Length-1)] 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] faster-whisper est installe" -ForegroundColor Green
    } else {
        throw "Not installed"
    }
} catch {
    Write-Host "[INFO] faster-whisper n'est pas installe" -ForegroundColor Yellow
    Write-Host ""

    # Vérifier si on est dans un venv
    if ($env:VIRTUAL_ENV) {
        Write-Host "[INFO] Environnement virtuel detecte: $env:VIRTUAL_ENV" -ForegroundColor Cyan
        Write-Host "Installation de faster-whisper" -ForegroundColor Yellow
        $installCmd = $pythonCmd + @("-m", "pip", "install", "faster-whisper")
    } else {
        Write-Host "Installation de faster-whisper en mode utilisateur" -ForegroundColor Yellow
        $installCmd = $pythonCmd + @("-m", "pip", "install", "faster-whisper", "--user")
    }

    try {
        & $installCmd[0] $installCmd[1..($installCmd.Length-1)]
        if ($LASTEXITCODE -ne 0) {
            throw "Installation failed"
        }
        Write-Host ""
        Write-Host "[OK] faster-whisper installe avec succes" -ForegroundColor Green
    } catch {
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

# === LANCEMENT APPLICATION ===
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Demarrage de l'application" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Raccourci: Ctrl+Alt+7" -ForegroundColor Yellow
Write-Host "Arret: Ctrl+C" -ForegroundColor Yellow
Write-Host ""

$launchCmd = $pythonCmd + @("-m", "src.main")
try {
    & $launchCmd[0] $launchCmd[1..($launchCmd.Length-1)]

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Application terminee normalement" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[ERREUR] Application terminee avec erreur (code: $LASTEXITCODE)" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "[ERREUR] $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Appuyez sur Entree pour quitter"
