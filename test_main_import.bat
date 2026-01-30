@echo off
chcp 65001 >nul

echo ================================================
echo    TEST IMPORT MAIN.PY
echo ================================================
echo.

echo [INFO] Test d'import du module main.py avec détails...
echo.

py -3.12 -c "
import sys
import os
from pathlib import Path

print('[DEBUG] Répertoire actuel:', os.getcwd())
print('[DEBUG] Python path:', sys.path[:3])

# Ajouter shared au path
shared_dir = Path('shared')
if shared_dir.exists():
    sys.path.insert(0, str(shared_dir))
    print('[DEBUG] Ajouté shared au path')
else:
    print('[ERREUR] Répertoire shared non trouvé')
    exit(1)

try:
    print('[DEBUG] Import du module main...')
    from src.main import WhisperSTTService
    print('[OK] Import réussi')
    
    print('[DEBUG] Test de création du service...')
    config_path = 'projects/voice-to-text-turbo/config.json'
    if not Path(config_path).exists():
        print(f'[ERREUR] Configuration non trouvée: {config_path}')
        exit(1)
    
    service = WhisperSTTService(config_path)
    print('[SUCCESS] Service créé avec succès!')
    
except Exception as e:
    print(f'[ERREUR] {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

echo.
echo [INFO] Test terminé
pause