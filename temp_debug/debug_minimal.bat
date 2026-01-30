@echo off
chcp 65001 >nul

echo ================================================
echo    DEBUG MINIMAL - VOICE-TO-TEXT TURBO
echo ================================================
echo.

:: Test Python 3.12
echo [1] Test Python 3.12...
py -3.12 --version
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé
    pause
    exit /b 1
)

:: Test import minimal
echo.
echo [2] Test import minimal...
py -3.12 -c "print('Python fonctionne')"
if errorlevel 1 (
    echo [ERREUR] Python ne fonctionne pas
    pause
    exit /b 1
)

:: Test du fichier main.py avec verbose
echo.
echo [3] Test main.py avec erreurs détaillées...
echo [DEBUG] Répertoire actuel: %CD%
echo [DEBUG] Fichier main.py: shared\src\main.py
echo [DEBUG] Configuration: projects\voice-to-text-turbo\config.json
echo.

if not exist "shared\src\main.py" (
    echo [ERREUR] main.py non trouvé
    pause
    exit /b 1
)

if not exist "projects\voice-to-text-turbo\config.json" (
    echo [ERREUR] config.json non trouvé
    pause
    exit /b 1
)

echo [INFO] Lancement avec capture d'erreur complète...
echo.

py -3.12 -c "
import sys
import traceback
sys.path.insert(0, 'shared')
try:
    print('[DEBUG] Tentative d\'import du module main...')
    import src.main as main_module
    print('[DEBUG] Import réussi')
    
    print('[DEBUG] Tentative de création du service...')
    service = main_module.WhisperSTTService('projects/voice-to-text-turbo/config.json')
    print('[DEBUG] Service créé avec succès')
    
    print('[SUCCESS] Initialisation réussie - le service fonctionne')
    
except ImportError as e:
    print('[ERREUR IMPORT]', str(e))
    print('[TRACEBACK]')
    traceback.print_exc()
except Exception as e:
    print('[ERREUR GENERALE]', str(e))
    print('[TRACEBACK]')
    traceback.print_exc()
"

echo.
echo [INFO] Test terminé. Appuyez sur une touche...
pause >nul