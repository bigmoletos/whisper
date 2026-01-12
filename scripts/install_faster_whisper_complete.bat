@echo off
REM Script d'installation complète de Faster-Whisper avec Rust
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Installation Complete Faster-Whisper
echo ========================================
echo.
echo Ce script va installer Rust puis Faster-Whisper
echo pour obtenir une transcription en temps reel.
echo.

REM Vérifier les privilèges administrateur (recommandé mais pas obligatoire)
net session >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Certaines operations peuvent necessiter des privileges administrateur
    echo.
)

cd /d "%~dp0.."

REM Vérifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

echo [1/4] Verification de Python...
python --version
echo.

REM Vérifier si Rust est déjà installé
echo [2/4] Verification de Rust...
rustc --version >nul 2>&1
if errorlevel 1 (
    echo Rust n'est pas installe.
    echo.
    echo Installation de Rust...
    echo.

    REM Vérifier si winget est disponible
    where winget >nul 2>&1
    if errorlevel 1 (
        echo winget n'est pas disponible sur ce systeme.
        echo.
        echo winget n'est pas disponible.
        echo.
        echo Options:
        echo   1. Utiliser le script d'installation manuelle (recommandé)
        echo   2. Installer manuellement depuis https://rustup.rs/
        echo.
        set /p choice="Utiliser le script d'installation manuelle? (O/N): "

        if /i "%choice%"=="O" (
            echo.
            echo Lancement du script d'installation manuelle...
            call "%~dp0install_rust_manual.bat"
            if errorlevel 1 (
                echo.
                echo Installation manuelle echouee.
                pause
                exit /b 1
            )
            echo.
            echo IMPORTANT: Fermez et rouvrez ce terminal apres l'installation de Rust
            echo Puis relancez ce script.
            pause
            exit /b 0
        ) else (
            echo.
            echo Installation manuelle requise:
            echo   1. Visitez https://rustup.rs/
            echo   2. Telechargez rustup-init.exe
            echo   3. Executez rustup-init.exe
            echo   4. Fermez et rouvrez ce terminal
            echo   5. Relancez ce script apres l'installation
            echo.
            pause
            exit /b 1
        )
    )

    REM Essayer d'installer via winget
    echo Installation de Rust via winget...
    winget install Rustlang.Rustup --accept-package-agreements --accept-source-agreements

    if errorlevel 1 (
        echo.
        echo ERREUR: Echec de l'installation de Rust via winget
        echo.
        echo Installation manuelle requise:
        echo   1. Visitez https://rustup.rs/
        echo   2. Telechargez rustup-init.exe
        echo   3. Executez rustup-init.exe
        echo   4. Fermez et rouvrez ce terminal
        echo   5. Relancez ce script apres l'installation
        echo.
        pause
        exit /b 1
    )

    echo.
    echo IMPORTANT: Fermez et rouvrez ce terminal apres l'installation de Rust
    echo Le PATH doit etre reinitialise.
    echo.
    echo Apres avoir ferme et rouvert le terminal, relancez ce script.
    pause
    exit /b 0

) else (
    echo Rust est deja installe:
    rustc --version
    cargo --version
    echo.
)

REM Vérifier que Rust est dans le PATH (après installation)
rustc --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ATTENTION: Rust est installe mais n'est pas dans le PATH
    echo Fermez et rouvrez ce terminal, puis relancez ce script.
    echo.
    pause
    exit /b 1
)

echo [3/4] Installation de Faster-Whisper...
python -m pip install --upgrade pip
python -m pip install faster-whisper

if errorlevel 1 (
    echo.
    echo ERREUR: Echec de l'installation de Faster-Whisper
    echo.
    echo Causes possibles:
    echo   - Rust n'est pas correctement installe
    echo   - Le terminal n'a pas ete redemarre apres l'installation de Rust
    echo   - Probleme de compilation des dependances
    echo.
    echo Solutions:
    echo   1. Fermez et rouvrez le terminal
    echo   2. Verifiez que Rust est installe: rustc --version
    echo   3. Reessayez: pip install faster-whisper
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] Verification de l'installation...
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
echo Faster-Whisper est maintenant installe et pret a l'emploi.
echo.
echo Pour l'utiliser, modifiez config.json:
echo   "engine": "faster-whisper"
echo   "model": "large-v3"
echo   "compute_type": "int8"
echo.
echo Le systeme sera 2-4x plus rapide qu'avec Whisper standard!
echo.
pause
