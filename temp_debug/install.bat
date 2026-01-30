@echo off
REM Script d'installation pour Whisper STT Global
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Installation de Whisper STT Global
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.10 ou superieur depuis https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Verification de Python...
python --version
echo.

REM Vérifier que pip est disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: pip n'est pas disponible
    pause
    exit /b 1
)

echo [2/4] Mise a jour de pip...
python -m pip install --upgrade pip
echo.

REM Vérifier que ffmpeg est installé
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: ffmpeg n'est pas detecte dans le PATH
    echo Whisper necessite ffmpeg pour fonctionner
    echo Veuillez installer ffmpeg depuis https://ffmpeg.org/download.html
    echo Ou utilisez: winget install ffmpeg
    echo.
    set /p continue="Continuer quand meme? (O/N): "
    if /i not "%continue%"=="O" (
        exit /b 1
    )
) else (
    echo [3/5] ffmpeg detecte...
    ffmpeg -version | findstr "version"
    echo.
)

REM Vérifier Rust (optionnel, pour Faster-Whisper)
rustc --version >nul 2>&1
if errorlevel 1 (
    echo [4/5] Rust n'est pas installe (optionnel)
    echo Rust est necessaire uniquement pour Faster-Whisper
    echo Whisper standard fonctionne sans Rust
    echo.
    echo Pour installer Rust:
    echo   winget install Rustlang.Rustup
    echo   Ou depuis https://rustup.rs/
    echo.
) else (
    echo [4/5] Rust detecte...
    rustc --version
    echo   (Faster-Whisper peut etre installe)
    echo.
)

REM Installer les dépendances Python
echo [5/5] Installation des dependances Python...
cd /d "%~dp0.."
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERREUR: Echec de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Vous pouvez maintenant lancer le service avec:
echo   scripts\start_service.bat
echo.
pause
