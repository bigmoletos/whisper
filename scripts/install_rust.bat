@echo off
REM Script d'installation de Rust pour Faster-Whisper
REM Auteur: Bigmoletos
REM Date: 2025-01-11

echo ========================================
echo Installation de Rust
echo ========================================
echo.
echo Rust est necessaire pour installer Faster-Whisper
echo (Whisper standard fonctionne sans Rust)
echo.

REM Vérifier si Rust est déjà installé
rustc --version >nul 2>&1
if not errorlevel 1 (
    echo Rust est deja installe:
    rustc --version
    echo.
    echo Pas besoin de reinstaller.
    pause
    exit /b 0
)

echo [1/2] Installation de Rust via winget...
winget install Rustlang.Rustup

if errorlevel 1 (
    echo.
    echo ERREUR: Echec de l'installation via winget
    echo.
    echo Installation manuelle:
    echo   1. Visitez https://rustup.rs/
    echo   2. Telechargez et executez rustup-init.exe
    echo   3. Suivez les instructions
    echo.
    pause
    exit /b 1
)

echo.
echo [2/2] Verification de l'installation...
echo.
echo IMPORTANT: Fermez et rouvrez ce terminal apres l'installation
echo Rust doit etre reinitialise dans le PATH
echo.
echo Apres avoir ferme et rouvert le terminal, verifiez avec:
echo   rustc --version
echo.
echo Ensuite, vous pourrez installer Faster-Whisper:
echo   pip install faster-whisper
echo.
pause
