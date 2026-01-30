@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ================================================
echo    VOICE-TO-TEXT TURBO - Version Moderne (pipx)
echo    (Faster-Whisper - GPU/CUDA)
echo ================================================
echo.

:: Répertoire du projet
set "PROJECT_DIR=%~dp0"
set "ROOT_DIR=%PROJECT_DIR%..\.."
set "SHARED_DIR=%ROOT_DIR%\shared"

:: Vérifier pipx
where pipx >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pipx non trouvé. Exécutez scripts\modern_install.bat
    pause
    exit /b 1
)

:: Vérifier l'installation VTT
pipx run --spec openai-whisper python -c "import whisper, faster_whisper, torch" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Installation VTT incomplète. Exécutez scripts\modern_install.bat
    pause
    exit /b 1
)

:: Vérifier CUDA via pipx
echo [INFO] Vérification de CUDA...
pipx run --spec openai-whisper python -c "
import torch
if torch.cuda.is_available():
    print('[INFO] CUDA détecté - Mode GPU activé')
    print(f'[INFO] GPU: {torch.cuda.get_device_name(0)}')
    exit(0)
else:
    print('[AVERTISSEMENT] CUDA non détecté. Mode CPU utilisé.')
    exit(1)
" 2>nul
if errorlevel 1 (
    echo [AVERTISSEMENT] CUDA non détecté. L'application fonctionnera en mode CPU.
    echo [INFO] Pour de meilleures performances, vérifiez votre installation CUDA.
) else (
    echo [INFO] CUDA détecté - Mode GPU activé
)

:: Configuration du projet
echo [INFO] Configuration du projet Voice-to-Text Turbo...
copy "%PROJECT_DIR%config.json" "%SHARED_DIR%\src\config.json" >nul
if exist "%SHARED_DIR%\src\config.json" (
    echo [INFO] Configuration Turbo activée (CUDA + large-v3)
) else (
    echo [WARNING] Échec de copie de configuration
)

:: Lancer l'application avec pipx
echo.
echo [INFO] Démarrage de Voice-to-Text Turbo (version moderne)...
echo [INFO] Raccourci: Ctrl+Alt+7 (toggle enregistrement)
echo.

cd /d "%SHARED_DIR%\src"

REM Définir les variables d'environnement pour pipx
set "PYTHONPATH=%SHARED_DIR%"

REM Lancer avec pipx
pipx run --spec openai-whisper python main.py --config "%PROJECT_DIR%config.json"

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est terminée avec une erreur
    pause
)

endlocal