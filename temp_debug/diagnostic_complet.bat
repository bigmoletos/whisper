@echo off
echo ========================================
echo   DIAGNOSTIC COMPLET VTT
echo ========================================
echo.
echo Verification de l'environnement Voice-to-Text Tools
echo.

cd /d "%~dp0\.."

echo [INFO] Activation de l'environnement virtuel...
if exist "venv_whisper\Scripts\activate.bat" (
    call venv_whisper\Scripts\activate.bat
    echo [OK] Environnement virtuel active
) else (
    echo [ERREUR] Environnement virtuel non trouve
    echo Executez d'abord install.bat
    pause
    exit /b 1
)

echo.
echo [INFO] 1. Test de compatibilite CUDA...
echo ----------------------------------------
python scripts\utils\check_cuda_compatibility.py

echo.
echo [INFO] 2. Test de l'installation CUDA...
echo ----------------------------------------
python scripts\utils\test_cuda_installation.py

echo.
echo [INFO] 3. Test de PyAudio...
echo ----------------------------------------
python scripts\utils\test_pyaudio.py

echo.
echo [INFO] 4. Verification des configurations...
echo ----------------------------------------
echo Verification des fichiers de configuration:

for %%f in (
    "projects\voice-to-text-basic\config.json"
    "projects\voice-to-text-turbo\config.json"
    "shared\src\config.json"
) do (
    if exist "%%f" (
        echo [OK] %%f
    ) else (
        echo [MANQUANT] %%f
    )
)

echo.
echo [INFO] 5. Test des dependances principales...
echo ----------------------------------------
python scripts\utils\test_dependencies.py

echo.
echo [INFO] 6. Verification des modeles Whisper...
echo ----------------------------------------
python -c "
import os
from pathlib import Path
cache_dir = Path.home() / '.cache' / 'whisper'
if cache_dir.exists():
    models = list(cache_dir.glob('*.pt'))
    if models:
        print(f'Modeles Whisper trouves: {len(models)}')
        for model in models:
            print(f'  - {model.name}')
    else:
        print('Aucun modele Whisper en cache')
else:
    print('Dossier cache Whisper non trouve')
"

echo.
echo ========================================
echo   DIAGNOSTIC TERMINE
echo ========================================
echo.
echo Consultez les rapports generes dans:
echo - cuda_compatibility_report.json
echo - cuda_test_report.json
echo.
pause