@echo off
setlocal enabledelayedexpansion

:: Script de vérification de l'installation Rust
:: Auteur: Bigmoletos
:: Date: 2026-01-18

echo ============================================
echo   Verification de Rust
echo ============================================
echo.

:: Vérifier rustc
echo 1. Verification de rustc...
rustc --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    rustc --version
    echo [OK] rustc est installe et disponible
) else (
    echo [ERREUR] rustc n'est pas installe ou pas dans le PATH
    echo.
    echo Installation de Rust:
    echo   1. Visitez https://rustup.rs/
    echo   2. Ou executez: scripts\install_rust.bat
    echo.
    pause
    exit /b 1
)

echo.

:: Vérifier cargo
echo 2. Verification de cargo...
cargo --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    cargo --version
    echo [OK] cargo est installe et disponible
) else (
    echo [ERREUR] cargo n'est pas installe
    pause
    exit /b 1
)

echo.

:: Test de compilation
echo 3. Test de compilation...
set TEMP_DIR=%TEMP%\rust_test_%RANDOM%
mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

cargo new test_rust --bin --quiet >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo [OK] Projet de test cree
    cd test_rust
    echo    Compilation en cours...

    cargo build --release --quiet >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        echo [OK] Compilation reussie

        target\release\test_rust.exe | findstr "Hello, world!" >nul 2>&1
        if !ERRORLEVEL! equ 0 (
            echo [OK] Execution reussie
        ) else (
            echo [AVERTISSEMENT] Compilation OK mais execution a echoue
        )
    ) else (
        echo [ERREUR] Echec de la compilation
        cd /d "%~dp0.."
        rmdir /s /q "%TEMP_DIR%" 2>nul
        pause
        exit /b 1
    )
) else (
    echo [ERREUR] Echec de la creation du projet
    cd /d "%~dp0.."
    rmdir /s /q "%TEMP_DIR%" 2>nul
    pause
    exit /b 1
)

:: Nettoyage
cd /d "%~dp0.."
rmdir /s /q "%TEMP_DIR%" 2>nul

echo.
echo ============================================
echo [OK] Rust est installe et fonctionne correctement
echo ============================================
echo.
echo Vous pouvez maintenant installer faster-whisper:
echo   pip install faster-whisper
echo.

pause
exit /b 0
