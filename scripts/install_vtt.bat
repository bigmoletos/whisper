@echo off
title Installation VTT - Voice-to-Text Tools
color 0A

echo ========================================
echo INSTALLATION VTT - VOICE-TO-TEXT TOOLS
echo ========================================
echo.

cd /d "%~dp0\.."

:menu
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║              INSTALLATION VTT - MENU PRINCIPAL                   ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  [1] Installation complète (Recommandé)                          ║
echo  ║      • Environnement virtuel isolé                               ║
echo  ║      • NumPy 2.3.0 compatible Numba                              ║
echo  ║      • PyTorch avec CUDA 12.1                                    ║
echo  ║      • Faster-Whisper + OpenAI Whisper                           ║
echo  ║      • Tous les modules audio et interface                       ║
echo  ║                                                                  ║
echo  ║  [2] Correction isolation environnement                          ║
echo  ║      • Résout problème NumPy 2.4 / Numba                         ║
echo  ║      • Crée environnement virtuel isolé                          ║
echo  ║                                                                  ║
echo  ║  [3] Vérification système                                        ║
echo  ║      • Diagnostic complet                                        ║
echo  ║      • Test compatibilité NumPy/Numba                            ║
echo  ║                                                                  ║
echo  ║  [Q] Quitter                                                     ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
set /p choice="  Votre choix [1-3/Q] : "

if "%choice%"=="1" goto install_complete
if "%choice%"=="2" goto fix_isolation
if "%choice%"=="3" goto verify_system
if /i "%choice%"=="Q" goto quit

echo.
echo  [!] Choix invalide
timeout /t 2 >nul
goto menu

:install_complete
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                  INSTALLATION COMPLÈTE VTT                       ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

echo [1/7] Vérification Python 3.12...
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis mais non trouvé
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    goto menu
)
py -3.12 --version
echo.

echo [2/7] Suppression ancien environnement...
if exist "venv_vtt_isolated" (
    echo Suppression de venv_vtt_isolated...
    rmdir /s /q "venv_vtt_isolated"
)
echo.

echo [3/7] Création environnement virtuel isolé...
py -3.12 -m venv venv_vtt_isolated --clear
if errorlevel 1 (
    echo [ERREUR] Échec création environnement virtuel
    pause
    goto menu
)
echo.

echo [4/7] Activation environnement...
call "venv_vtt_isolated\Scripts\activate.bat"
echo.

echo [5/7] Mise à jour pip...
python -m pip install --upgrade pip --quiet
echo.

echo [6/7] Installation dépendances (cela peut prendre plusieurs minutes)...
echo.
echo Installation NumPy 2.3.0 (compatible Numba)...
python -m pip install --no-deps numpy==2.3.0 --quiet
if errorlevel 1 (
    echo [ERREUR] Échec installation NumPy
    pause
    goto menu
)

echo Installation Numba...
python -m pip install numba --quiet
if errorlevel 1 (
    echo [ERREUR] Échec installation Numba
    pause
    goto menu
)

echo Installation PyTorch avec CUDA 12.1...
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --quiet
if errorlevel 1 (
    echo [AVERTISSEMENT] Échec installation PyTorch CUDA, tentative CPU...
    python -m pip install torch torchvision torchaudio --quiet
)

echo Installation Faster-Whisper...
python -m pip install faster-whisper --quiet

echo Installation OpenAI Whisper...
python -m pip install openai-whisper --quiet

echo Installation modules audio...
python -m pip install sounddevice pyaudio --quiet

echo Installation modules interface...
python -m pip install pyautogui pyperclip keyboard plyer --quiet

echo.
echo [7/7] Vérification installation...
python -c "import numpy; print(f'✓ NumPy: {numpy.__version__}')"
python -c "import numba; print(f'✓ Numba: {numba.__version__}')"
python -c "import torch; print(f'✓ PyTorch: {torch.__version__}')"
python -c "import torch; print(f'✓ CUDA disponible: {torch.cuda.is_available()}')"
python -c "import faster_whisper; print('✓ Faster-Whisper: OK')"
python -c "import whisper; print('✓ OpenAI Whisper: OK')"
python -c "import sounddevice; print('✓ SoundDevice: OK')"
python -c "import pyautogui; print('✓ PyAutoGUI: OK')"

echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                  INSTALLATION TERMINÉE                           ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
echo  [SUCCESS] Installation complète réussie !
echo.
echo  Pour utiliser VTT :
echo  1. Lancez start.bat
echo  2. Choisissez option [E] pour environnement isolé
echo  3. Ou utilisez option [1] si environnement global compatible
echo.
pause
goto menu

:fix_isolation
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║            CORRECTION ISOLATION ENVIRONNEMENT                    ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
echo  [PROBLÈME] NumPy 2.4 global incompatible avec Numba
echo  [SOLUTION] Création environnement virtuel isolé avec NumPy 2.3.0
echo.
set /p confirm="  Continuer ? [O/N] : "
if /i not "%confirm%"=="O" goto menu

echo.
echo [INFO] Lancement correction isolation...
call :install_complete
goto menu

:verify_system
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                  VÉRIFICATION SYSTÈME                            ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Vérification Python 3.12...
py -3.12 --version 2>nul
if errorlevel 1 (
    echo [ERREUR] Python 3.12 non trouvé
) else (
    echo [OK] Python 3.12 disponible
)
echo.

echo [2/4] Vérification environnement global...
py -3.12 -c "import numpy; print(f'NumPy global: {numpy.__version__}')" 2>nul
py -3.12 -c "import numba; print(f'Numba global: {numba.__version__}')" 2>nul
py -3.12 -c "import numpy; import numba; assert numpy.__version__ <= '2.3'; print('Compatibilité: OK')" 2>nul
if errorlevel 1 (
    echo [PROBLÈME] Environnement global incompatible NumPy/Numba
) else (
    echo [OK] Environnement global compatible
)
echo.

echo [3/4] Vérification environnement isolé...
if exist "venv_vtt_isolated\Scripts\activate.bat" (
    echo [OK] Environnement isolé existe
    call "venv_vtt_isolated\Scripts\activate.bat"
    python -c "import numpy; print(f'NumPy isolé: {numpy.__version__}')" 2>nul
    python -c "import numba; print(f'Numba isolé: {numba.__version__}')" 2>nul
    python -c "import torch; print(f'PyTorch CUDA: {torch.cuda.is_available()}')" 2>nul
) else (
    echo [INFO] Environnement isolé non créé
    echo [ACTION] Utilisez option [1] pour créer l'environnement
)
echo.

echo [4/4] Recommandations...
py -3.12 -c "import numpy; import numba; assert numpy.__version__ <= '2.3'" >nul 2>&1
if errorlevel 1 (
    echo [RECOMMANDATION] Utilisez option [E] dans start.bat
    echo                  ou créez environnement isolé avec option [1]
) else (
    echo [OK] Vous pouvez utiliser start.bat normalement
)
echo.

pause
goto menu

:quit
echo.
echo  Au revoir !
timeout /t 2 >nul
exit /b 0