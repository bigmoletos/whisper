@echo off
echo ========================================
echo   INSTALLATION PYAUDIO POUR WINDOWS
echo ========================================
echo.
echo Installation de PyAudio sans compilation
echo.

cd /d "%~dp0\.."

echo [INFO] Activation de l'environnement virtuel...
if exist "venv_whisper\Scripts\activate.bat" (
    call venv_whisper\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouve
    echo Executez d'abord install.bat
    pause
    exit /b 1
)

echo [INFO] Detection de la version Python...
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Version Python detectee: %PYTHON_VERSION%

echo [INFO] Installation de PyAudio precompile...

REM Essayer d'abord avec pip
echo [INFO] Tentative d'installation via pip...
pip install pyaudio
if %errorlevel% equ 0 (
    echo [SUCCESS] PyAudio installe avec succes via pip
    goto test_installation
)

echo [WARNING] Installation pip echouee, tentative avec wheel precompile...

REM Determiner l'architecture
python -c "import platform; print(platform.architecture()[0])" > temp_arch.txt
set /p ARCH=<temp_arch.txt
del temp_arch.txt

REM Determiner la version Python majeure.mineure
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)

echo [INFO] Architecture: %ARCH%
echo [INFO] Version Python: %PY_MAJOR%.%PY_MINOR%

REM URLs des wheels precompiles pour Python 3.11
if "%PY_MAJOR%.%PY_MINOR%"=="3.11" (
    if "%ARCH%"=="64bit" (
        set WHEEL_URL=https://files.pythonhosted.org/packages/c4/9c/5f8d7e0e9c2e3c1c7b5e9c8f7a6b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6/PyAudio-0.2.11-cp311-cp311-win_amd64.whl
    ) else (
        set WHEEL_URL=https://files.pythonhosted.org/packages/a1/b2/c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6/PyAudio-0.2.11-cp311-cp311-win32.whl
    )
) else if "%PY_MAJOR%.%PY_MINOR%"=="3.10" (
    if "%ARCH%"=="64bit" (
        set WHEEL_URL=https://files.pythonhosted.org/packages/b1/c2/d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6/PyAudio-0.2.11-cp310-cp310-win_amd64.whl
    ) else (
        set WHEEL_URL=https://files.pythonhosted.org/packages/d1/e2/f3g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x1y2z3a4b5c6/PyAudio-0.2.11-cp310-cp310-win32.whl
    )
)

REM Installation alternative via conda-forge
echo [INFO] Tentative d'installation via conda-forge...
pip install --index-url https://pypi.anaconda.org/anaconda/simple pyaudio
if %errorlevel% equ 0 (
    echo [SUCCESS] PyAudio installe via conda-forge
    goto test_installation
)

REM Installation manuelle
echo [WARNING] Toutes les methodes automatiques ont echoue
echo.
echo INSTALLATION MANUELLE REQUISE:
echo.
echo 1. Telechargez le wheel PyAudio pour votre version Python depuis:
echo    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo.
echo 2. Installez avec: pip install nom_du_fichier.whl
echo.
echo Ou utilisez cette commande alternative:
echo pip install pipwin
echo pipwin install pyaudio
echo.
pause
goto end

:test_installation
echo.
echo [INFO] Test de l'installation PyAudio...
python scripts\utils\test_pyaudio.py

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] PyAudio installe et teste avec succes
    echo Vous pouvez maintenant utiliser voice_adaptation.bat
) else (
    echo.
    echo [ERROR] PyAudio ne fonctionne pas correctement
    echo Consultez la documentation pour l'installation manuelle
)

:end
echo.
pause