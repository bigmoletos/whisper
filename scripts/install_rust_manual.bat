@echo off
REM Script d'installation manuelle de Rust
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Installation Manuelle de Rust
echo ========================================
echo.

REM Vérifier si Rust est déjà installé
rustc --version >nul 2>&1
if not errorlevel 1 (
    echo Rust est deja installe:
    rustc --version
    echo.
    pause
    exit /b 0
)

echo Rust n'est pas installe.
echo.
echo Ce script va vous guider pour installer Rust manuellement.
echo.

REM Télécharger rustup-init.exe
echo [1/3] Telechargement de rustup-init.exe...
echo.

set RUSTUP_URL=https://win.rustup.rs/x86_64
set RUSTUP_FILE=%TEMP%\rustup-init.exe

echo Telechargement depuis %RUSTUP_URL%...
powershell -Command "Invoke-WebRequest -Uri '%RUSTUP_URL%' -OutFile '%RUSTUP_FILE%'"

if errorlevel 1 (
    echo.
    echo ERREUR: Echec du telechargement
    echo.
    echo Telechargement manuel:
    echo   1. Visitez https://rustup.rs/
    echo   2. Cliquez sur "Download rustup-init.exe"
    echo   3. Executez le fichier telecharge
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Execution de rustup-init.exe...
echo.
echo IMPORTANT: Dans l'installateur Rust:
echo   - Appuyez sur Entree pour accepter les options par defaut
echo   - Attendez la fin de l'installation
echo.

REM Exécuter rustup-init
start /wait "" "%RUSTUP_FILE%"

if errorlevel 1 (
    echo.
    echo ERREUR: L'installation de Rust a echoue
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Verification de l'installation...
echo.

REM Attendre un peu pour que le PATH soit mis à jour
timeout /t 2 /nobreak >nul

REM Vérifier dans un nouveau processus pour avoir le nouveau PATH
powershell -Command "& { $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); rustc --version }"

if errorlevel 1 (
    echo.
    echo ATTENTION: Rust semble installe mais n'est pas dans le PATH
    echo.
    echo SOLUTION: Fermez et rouvrez ce terminal, puis verifiez avec:
    echo   rustc --version
    echo.
    echo Si cela fonctionne, vous pouvez installer Faster-Whisper:
    echo   pip install faster-whisper
    echo.
) else (
    echo.
    echo Rust est installe avec succes!
    echo.
    echo Vous pouvez maintenant installer Faster-Whisper:
    echo   pip install faster-whisper
    echo.
)

pause
