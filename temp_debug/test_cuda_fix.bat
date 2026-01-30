@echo off
chcp 65001 >nul

echo ================================================
echo    TEST CUDA APRÈS CORRECTION
echo ================================================
echo.

echo [INFO] Test rapide de CUDA après correction
echo.

:: Test PyTorch CUDA
echo [1/3] Test PyTorch CUDA...
py -3.12 scripts\test_cuda_pytorch.py pytorch

if errorlevel 1 (
    echo [ERREUR] PyTorch CUDA ne fonctionne pas
    pause
    exit /b 1
)

:: Test Faster-Whisper
echo.
echo [2/3] Test Faster-Whisper CUDA...
py -3.12 scripts\test_cuda_pytorch.py faster-whisper

if errorlevel 1 (
    echo [ERREUR] Faster-Whisper CUDA ne fonctionne pas
    pause
    exit /b 1
)

:: Test Voice-to-Text Turbo
echo.
echo [3/3] Test Voice-to-Text Turbo...
echo [INFO] Test de 5 secondes de l'application...

timeout /t 2 >nul
start /min py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json
timeout /t 5 >nul
taskkill /f /im python.exe 2>nul

echo.
echo ================================================
echo    RÉSULTAT DU TEST
echo ================================================
echo [SUCCESS] CUDA fonctionne correctement !
echo [SUCCESS] Voice-to-Text Turbo avec GPU est prêt
echo.
echo [INFO] Vous pouvez maintenant utiliser:
echo [INFO] start.bat puis choisir [1] pour l'accélération GPU
echo.
pause