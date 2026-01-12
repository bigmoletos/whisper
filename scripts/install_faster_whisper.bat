@echo off
REM Script d'installation de Faster-Whisper avec gestion de Rust
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Installation de Faster-Whisper
echo ========================================
echo.

REM Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe
    pause
    exit /b 1
)

echo [1/3] Verification de Rust...
rustc --version >nul 2>&1
if errorlevel 1 (
    echo Rust n'est pas installe.
    echo.
    echo Options:
    echo   1. Installer Rust automatiquement (recommandé)
    echo   2. Installer Rust manuellement depuis https://rustup.rs/
    echo   3. Utiliser Whisper standard (pas de Rust necessaire)
    echo.
    set /p choice="Votre choix (1/2/3): "

    if "%choice%"=="1" (
        echo.
        echo Installation de Rust via winget...
        winget install Rustlang.Rustup
        if errorlevel 1 (
            echo ERREUR: Echec de l'installation de Rust
            echo Veuillez installer Rust manuellement depuis https://rustup.rs/
            pause
            exit /b 1
        )
        echo.
        echo IMPORTANT: Fermez et rouvrez ce terminal apres l'installation de Rust
        echo Puis relancez ce script.
        pause
        exit /b 0
    ) else if "%choice%"=="2" (
        echo.
        echo Veuillez installer Rust depuis https://rustup.rs/
        echo Puis relancez ce script.
        pause
        exit /b 0
    ) else (
        echo.
        echo Utilisation de Whisper standard (pas de Faster-Whisper)
        echo Modifiez config.json pour utiliser "engine": "whisper"
        pause
        exit /b 0
    )
) else (
    rustc --version
    echo Rust detecte avec succes!
    echo.
)

echo [2/3] Installation de Faster-Whisper...
cd /d "%~dp0.."
python -m pip install faster-whisper

if errorlevel 1 (
    echo.
    echo ERREUR: Echec de l'installation de Faster-Whisper
    echo.
    echo Solutions alternatives:
    echo   1. Verifier que Rust est correctement installe
    echo   2. Essayer: pip install faster-whisper --prefer-binary
    echo   3. Utiliser Whisper standard dans config.json
    pause
    exit /b 1
)

echo.
echo [3/3] Verification de l'installation...
python -c "from faster_whisper import WhisperModel; print('Faster-Whisper installe avec succes!')"

if errorlevel 1 (
    echo ERREUR: Faster-Whisper n'est pas correctement installe
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Vous pouvez maintenant utiliser Faster-Whisper dans config.json:
echo   "engine": "faster-whisper"
echo.
pause
