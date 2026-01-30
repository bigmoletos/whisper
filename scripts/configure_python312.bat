@echo off
chcp 65001 >nul

echo ================================================
echo    Configuration Python 3.12 par défaut
echo ================================================
echo.

:: Vérifier que Python 3.12 est disponible
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé sur ce système
    echo.
    echo Versions disponibles :
    py -0 2>nul
    echo.
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    exit /b 1
)

echo [INFO] Python 3.12 détecté : 
py -3.12 --version

:: Créer le fichier py.ini pour définir Python 3.12 par défaut
set "PY_INI=%USERPROFILE%\py.ini"

echo.
echo [INFO] Configuration de Python 3.12 comme version par défaut...
echo [defaults] > "%PY_INI%"
echo python=3.12 >> "%PY_INI%"

if exist "%PY_INI%" (
    echo [OK] Fichier py.ini créé : %PY_INI%
    echo.
    echo Contenu :
    type "%PY_INI%"
    echo.
    echo [OK] Python 3.12 est maintenant la version par défaut
    echo [INFO] Utilisez 'py' au lieu de 'python' pour garantir l'utilisation de 3.12
) else (
    echo [ERREUR] Impossible de créer le fichier py.ini
)

echo.
echo Test de la configuration :
py --version

echo.
pause