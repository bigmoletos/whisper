@echo off
chcp 65001 >nul

echo ================================================
echo    REDÉMARRAGE COMPLET VTT
echo ================================================
echo.

echo [1/3] Arrêt de tous les processus Python VTT...
taskkill /f /im python.exe 2>nul
taskkill /f /im py.exe 2>nul
timeout /t 2 >nul

echo [2/3] Nettoyage du cache Python...
if exist "__pycache__" rmdir /s /q "__pycache__" 2>nul
if exist "shared\__pycache__" rmdir /s /q "shared\__pycache__" 2>nul
if exist "shared\src\__pycache__" rmdir /s /q "shared\src\__pycache__" 2>nul

echo [3/3] Test de la nouvelle pop-up...
py -3.12 test_nouvelle_popup.py

echo.
echo ================================================
echo    REDÉMARRAGE TERMINÉ
echo ================================================
echo.
echo [INFO] Vous pouvez maintenant relancer start.bat
echo [INFO] La nouvelle pop-up devrait s'afficher
echo.
pause