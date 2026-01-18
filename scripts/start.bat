@echo off
setlocal enabledelayedexpansion

:: Script de lancement Whisper STT
:: Version ultra-robuste

title Whisper STT

echo ============================================
echo   Whisper STT - Faster-Whisper
echo ============================================
echo.

:: Aller à la racine du projet
cd /d "%~dp0"

:: === DETECTION PYTHON ===
echo Detection de Python...
echo.

:: Test py -3.12
echo [1/5] Test: py -3.12
call py -3.12 --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo    =^> OK
    goto :use_py312
)
echo    =^> Non disponible

:: Test py -3.11
echo [2/5] Test: py -3.11
call py -3.11 --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo    =^> OK
    goto :use_py311
)
echo    =^> Non disponible

:: Test py -3.10
echo [3/5] Test: py -3.10
call py -3.10 --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo    =^> OK
    goto :use_py310
)
echo    =^> Non disponible

:: Test python
echo [4/5] Test: python
call python --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo    =^> OK
    goto :use_python
)
echo    =^> Non disponible

:: Test py
echo [5/5] Test: py
call py --version 2>nul
if %ERRORLEVEL% equ 0 (
    echo    =^> OK
    goto :use_py
)
echo    =^> Non disponible

echo.
echo [ERREUR] Aucune version de Python trouvee
echo.
echo Installez Python 3.12 depuis: https://www.python.org/downloads/
pause
exit /b 1

:: === UTILISATION PYTHON 3.12 ===
:use_py312
echo.
echo [OK] Utilisation de Python 3.12
py -3.12 --version
echo.
echo Verification de la configuration...
py -3.12 scripts\config_checker.py || goto :error
echo.
echo Verification de faster-whisper...
py -3.12 -c "import faster_whisper" 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] Installation de faster-whisper...
    py -3.12 -m pip install faster-whisper --user
    if %ERRORLEVEL% neq 0 goto :install_error
)
echo.
echo Lancement de l'application...
echo Raccourci: Ctrl+Alt+7
echo.
py -3.12 -m src.main
goto :end

:: === UTILISATION PYTHON 3.11 ===
:use_py311
echo.
echo [OK] Utilisation de Python 3.11
py -3.11 --version
echo.
py -3.11 scripts\config_checker.py || goto :error
py -3.11 -c "import faster_whisper" 2>nul || py -3.11 -m pip install faster-whisper --user
py -3.11 -m src.main
goto :end

:: === UTILISATION PYTHON 3.10 ===
:use_py310
echo.
echo [OK] Utilisation de Python 3.10
py -3.10 --version
echo.
py -3.10 scripts\config_checker.py || goto :error
py -3.10 -c "import faster_whisper" 2>nul || py -3.10 -m pip install faster-whisper --user
py -3.10 -m src.main
goto :end

:: === UTILISATION PYTHON (defaut) ===
:use_python
echo.
echo [OK] Utilisation de python
python --version
echo.
python scripts\config_checker.py || goto :error
python -c "import faster_whisper" 2>nul || python -m pip install faster-whisper --user
python -m src.main
goto :end

:: === UTILISATION PY ===
:use_py
echo.
echo [OK] Utilisation de py
py --version
echo.
py scripts\config_checker.py || goto :error
py -c "import faster_whisper" 2>nul || py -m pip install faster-whisper --user
py -m src.main
goto :end

:install_error
echo.
echo [ERREUR] Installation de faster-whisper a echoue
echo.
echo SOLUTIONS:
echo 1. Installez Rust: https://rustup.rs/
echo 2. OU modifiez config.json: "engine": "whisper"
goto :error

:error
echo.
echo [ERREUR] Une erreur s'est produite
pause
exit /b 1

:end
echo.
pause
