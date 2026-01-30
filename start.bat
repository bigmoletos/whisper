@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: Vérification rapide et silencieuse du système (désactivée - script déplacé)
:: py -3.12 scripts\quick_check.py >nul 2>&1
:: if errorlevel 1 (
::     echo.
::     echo  [INFO] Première utilisation ou problème détecté
::     echo  [INFO] Utilisez [U] pour vérification système complète
::     echo.
::     timeout /t 3 >nul
:: )

:: Vérification spéciale NumPy/Numba (problème d'isolation environnement)
py -3.12 -c "import numpy; import numba; assert numpy.__version__ <= '2.3'" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ATTENTION] Problème de compatibilité NumPy/Numba détecté
    echo  [INFO] NumPy 2.4 global incompatible avec Numba
    echo  [SOLUTION] Utilisez [E] pour environnement isolé ou [I] pour correction
    echo.
    timeout /t 3 >nul
)

:menu
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                                                                  ║
echo  ║             VTT - VOICE-TO-TEXT TOOLS                            ║
echo  ║             Suite de transcription vocale                        ║
echo  ║                                                                  ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  TRANSCRIPTION VOCALE (dictée)                                   ║
echo  ║  ─────────────────────────────                                   ║
echo  ║                                                                  ║
echo  ║  [1] Voice-to-Text TURBO (Lancement Direct)                     ║
echo  ║      Lancement direct - Version recommandée                      ║
echo  ║      • Accélération GPU avec Faster-Whisper                      ║
echo  ║      • Modèle large-v3 haute qualité                             ║
echo  ║      • Raccourci : Ctrl+Alt+7 (toggle enregistrement)           ║
echo  ║                                                                  ║
echo  ║  [2] Voice-to-Text TURBO (Mode Fallback)                        ║
echo  ║      Version de secours avec Whisper standard                    ║
echo  ║      • Fonctionne sur CPU si problèmes GPU                       ║
echo  ║      • Plus lent mais plus compatible                             ║
echo  ║                                                                  ║
echo  ║  [E] Voice-to-Text TURBO (Environnement Isolé)                  ║
echo  ║      Solution pour problèmes NumPy/Numba                         ║
echo  ║      • Environnement virtuel complètement isolé                  ║
echo  ║      • NumPy 2.3 compatible avec Numba                           ║
echo  ║      • Résout les conflits avec autres projets Python            ║
echo  ║                                                                  ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  ASSISTANT DE RÉUNION                                            ║
echo  ║  ────────────────────                                            ║
echo  ║                                                                  ║
echo  ║  [3] Meeting Transcriber                                         ║
echo  ║      Transcription de réunion avec résumés automatiques          ║
echo  ║      • Capture l'audio système (Teams, Zoom, etc.)               ║
echo  ║      • Génère des résumés avec Ollama (IA locale)                ║
echo  ║      • Rapport final : points clés, décisions, actions           ║
echo  ║                                                                  ║
echo  ║  [4] Meeting Transcriber PRO                                     ║
echo  ║      Assistant avancé avec identification des locuteurs          ║
echo  ║      • Toutes les fonctionnalités de [3]                         ║
echo  ║      • + Diarisation : sait QUI parle (Jean, Marie, etc.)        ║
echo  ║      • + Statistiques de temps de parole par personne            ║
echo  ║      • Requiert : Token Hugging Face (gratuit)                   ║
echo  ║                                                                  ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  PERSONNALISATION                                                ║
echo  ║  ────────────────                                                ║
echo  ║                                                                  ║
echo  ║  [V] Adaptation vocale                                           ║
echo  ║      Améliorer la reconnaissance de votre voix                   ║
echo  ║      • Entraînement sur termes techniques                        ║
echo  ║      • Test de qualité vocale                                    ║
echo  ║      • Optimisation personnalisée                                ║
echo  ║                                                                  ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  [U] Vérification système complète                               ║
echo  ║  [I] Installation des dépendances                                ║
echo  ║  [C] Correction isolation environnement (NumPy/Numba)           ║
echo  ║  [D] Documentation                                               ║
echo  ║  [Q] Quitter                                                     ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
set /p choice="  Votre choix [1-4/E/V/U/I/C/D/Q] : "

if /i "%choice%"=="1" goto voice_turbo_direct
if /i "%choice%"=="2" goto voice_turbo_fallback
if /i "%choice%"=="E" goto voice_turbo_isolated
if /i "%choice%"=="e" goto voice_turbo_isolated
if /i "%choice%"=="3" goto meeting
if /i "%choice%"=="4" goto meeting_pro
if /i "%choice%"=="V" goto voice_adaptation
if /i "%choice%"=="v" goto voice_adaptation
if /i "%choice%"=="U" goto system_check
if /i "%choice%"=="u" goto system_check
if /i "%choice%"=="I" goto install_menu
if /i "%choice%"=="i" goto install_menu
if /i "%choice%"=="C" goto fix_isolation
if /i "%choice%"=="c" goto fix_isolation
if /i "%choice%"=="D" goto documentation
if /i "%choice%"=="d" goto documentation
if /i "%choice%"=="Q" goto quit
if /i "%choice%"=="q" goto quit

echo.
echo  [!] Choix invalide. Appuyez sur une touche...
pause >nul
goto menu

:voice_turbo_direct
cls
echo.
echo  Voice-to-Text TURBO (Lancement Direct)...
echo  ─────────────────────────────────────────
echo.
echo  Lancement direct de Voice-to-Text Turbo avec Faster-Whisper
echo  Configuration optimisée : CUDA + large-v3 + vocabulaire technique
echo.

:: Vérifier d'abord la compatibilité NumPy/Numba
py -3.12 -c "import numpy; import numba; assert numpy.__version__ <= '2.3'" >nul 2>&1
if errorlevel 1 (
    echo  [ATTENTION] Problème de compatibilité NumPy/Numba détecté
    echo  [INFO] Basculement automatique vers l'environnement isolé...
    echo.
    goto voice_turbo_isolated
)

echo  [INFO] Lancement direct intégré...
echo.
cd /d "%~dp0"
py -3.12 shared\src\main.py --config projects\voice-to-text-turbo\config.json
if errorlevel 1 (
    echo.
    echo  [ERREUR] Le programme s'est terminé avec une erreur
    echo  [INFO] Essayez l'option [E] pour l'environnement isolé
    pause
)
goto end

:voice_turbo_isolated
cls
echo.
echo  Voice-to-Text TURBO (Environnement Isolé)...
echo  ─────────────────────────────────────────────
echo.
echo  Cette version utilise un environnement virtuel complètement isolé
echo  pour résoudre les problèmes de compatibilité NumPy/Numba.
echo.

:: Vérifier si l'environnement isolé existe
if not exist "%~dp0venv_vtt_isolated\Scripts\activate.bat" (
    echo  [INFO] Environnement isolé non trouvé - Installation requise...
    echo.
    echo  [ERREUR] Veuillez d'abord exécuter l'option [I] pour installer VTT
    echo  [INFO] Puis choisissez l'option de correction d'isolation
    pause
    goto menu
)

echo  [INFO] Activation de l'environnement virtuel isolé...
call "%~dp0venv_vtt_isolated\Scripts\activate.bat"

echo  [INFO] Vérification des versions...
python -c "import numpy; print(f'NumPy: {numpy.__version__}')" 2>nul
if errorlevel 1 (
    echo  [ERREUR] NumPy non disponible dans l'environnement isolé
    echo  [SOLUTION] Exécutez [C] pour corriger l'isolation
    pause
    goto menu
)

python -c "import numba; print(f'Numba: {numba.__version__}')" 2>nul
if errorlevel 1 (
    echo  [ERREUR] Numba non disponible dans l'environnement isolé
    echo  [SOLUTION] Exécutez [C] pour corriger l'isolation
    pause
    goto menu
)

echo  [INFO] Lancement de Voice-to-Text TURBO (environnement isolé)...
echo.
cd /d "%~dp0"
python shared\src\main.py --config projects\voice-to-text-turbo\config.json
if errorlevel 1 (
    echo.
    echo  [ERREUR] Le programme s'est terminé avec une erreur
    echo  [INFO] Vérifiez voice_transcriber_turbo.log pour plus de détails
    pause
)
goto end

:fix_isolation
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║              CORRECTION ISOLATION ENVIRONNEMENT                 ║
echo  ║           Résolution problème NumPy 2.4 / Numba                 ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
echo  [PROBLÈME DÉTECTÉ]
echo  NumPy 2.4 installé globalement est incompatible avec Numba
echo  qui nécessite NumPy 2.3 ou inférieur.
echo.
echo  [SOLUTION]
echo  Création d'un environnement virtuel complètement isolé avec
echo  les versions compatibles de tous les packages.
echo.
set /p confirm="  Continuer ? [O/N] : "
if /i not "%confirm%"=="O" goto menu

echo.
echo  [INFO] Lancement du script d'installation unifié...
if exist "%~dp0scripts\install_vtt.bat" (
    call "%~dp0scripts\install_vtt.bat"
) else (
    echo  [ERREUR] Script install_vtt.bat non trouvé
    echo  [INFO] Veuillez vérifier l'installation de VTT
)
echo.
pause
goto menu
cls
echo.
echo  Voice-to-Text TURBO (Mode Fallback)...
echo  ──────────────────────────────────────
echo.
echo  Cette version utilise Whisper standard au lieu de Faster-Whisper
echo  pour éviter les problèmes de compatibilité.
echo.
if exist "%~dp0projects\voice-to-text-turbo\start_fallback.bat" (
    call "%~dp0projects\voice-to-text-turbo\start_fallback.bat"
    if errorlevel 1 (
        echo.
        echo  [ERREUR] Le programme s'est terminé avec une erreur
        echo  [INFO] Vérifiez voice_transcriber_fallback.log
        pause
    )
) else (
    echo  [ERREUR] Script start_fallback.bat non trouvé
    pause
)
goto end

:voice_turbo_fallback
cls
echo.
echo  Voice-to-Text TURBO (Mode Fallback)...
echo  ──────────────────────────────────────
echo.
echo  Cette version utilise Whisper standard au lieu de Faster-Whisper
echo  pour éviter les problèmes de compatibilité.
echo.
if exist "%~dp0projects\voice-to-text-turbo\start_fallback.bat" (
    call "%~dp0projects\voice-to-text-turbo\start_fallback.bat"
    if errorlevel 1 (
        echo.
        echo  [ERREUR] Le programme s'est terminé avec une erreur
        echo  [INFO] Vérifiez voice_transcriber_fallback.log
        pause
    )
) else (
    echo  [ERREUR] Script start_fallback.bat non trouvé
    pause
)
goto end

:system_check
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                    VTT - VÉRIFICATION SYSTÈME                    ║
echo  ║                 Diagnostic complet des dépendances               ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Vérifier Python 3.12
echo [1/6] Vérification Python 3.12...
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python 3.12 requis mais non trouvé
    echo [INFO] Installez Python 3.12 depuis python.org
    pause
    goto menu
)
echo [OK] Python 3.12 détecté

:: Vérifier les modules Python de base
echo [2/6] Vérification modules Python de base...
py -3.12 -c "import json, logging, pathlib, numpy, sounddevice, pyautogui, keyboard, pyperclip" >nul 2>&1
if errorlevel 1 (
    echo [MANQUANT] Modules de base manquants
    echo [INFO] Utilisez l'option [I] pour installer les dépendances
    pause
    goto menu
) else (
    echo [OK] Modules de base présents
)

:: Vérifier PyTorch et CUDA
echo [3/6] Vérification PyTorch et CUDA...
py -3.12 -c "import torch; print('CUDA:', torch.cuda.is_available())" >nul 2>&1
if errorlevel 1 (
    echo [MANQUANT] PyTorch manquant
    echo [INFO] Utilisez l'option [I] pour installer les dépendances
    pause
    goto menu
) else (
    :: Vérifier si CUDA fonctionne correctement
    py -3.12 -c "import torch; assert torch.cuda.is_available()" >nul 2>&1
    if errorlevel 1 (
        echo [PROBLÈME] CUDA détecté mais non fonctionnel
        echo [INFO] Utilisez l'option [I] pour corriger l'installation
        pause
        goto menu
    ) else (
        echo [OK] PyTorch avec CUDA fonctionnel
    )
)

:: Vérifier Faster-Whisper avec CUDA
echo [4/6] Vérification Faster-Whisper...
py -3.12 -c "import faster_whisper; faster_whisper.WhisperModel('tiny', device='cuda', compute_type='float16')" >nul 2>&1
if errorlevel 1 (
    echo [PROBLÈME] Faster-Whisper CUDA non fonctionnel
    echo [INFO] Utilisez l'option [I] pour corriger l'installation
    pause
    goto menu
) else (
    echo [OK] Faster-Whisper avec CUDA fonctionnel
)

:: Vérifier les fichiers de configuration
echo [5/6] Vérification configuration...
if not exist "%~dp0projects\voice-to-text-turbo\config.json" (
    echo [ERREUR] Configuration Voice-to-Text Turbo manquante
    pause
    goto menu
)
if not exist "%~dp0shared\src\main.py" (
    echo [ERREUR] Fichier principal main.py manquant
    pause
    goto menu
)
echo [OK] Configuration présente

:: Test rapide du système complet
echo [6/6] Test système complet...
timeout /t 1 >nul
py -3.12 -c "import sys, os; sys.path.insert(0, 'shared'); from src.faster_whisper_transcriber import FasterWhisperTranscriber; transcriber = FasterWhisperTranscriber('tiny', 'fr', 'cuda', 'float16'); transcriber.load_model(); print('Système VTT prêt !')" >nul 2>&1
if errorlevel 1 (
    echo [PROBLÈME] Test système échoué - Vérification des logs...
    echo [INFO] Consultez voice_transcriber_turbo.log pour plus de détails
    pause
    goto menu
) else (
    echo [OK] Système VTT entièrement fonctionnel
)

echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                    VÉRIFICATIONS TERMINÉES                       ║
echo  ║                   Système prêt à l'utilisation                   ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
echo  [SUCCESS] Toutes les vérifications sont terminées !
echo  [INFO] Vous pouvez maintenant utiliser Voice-to-Text Turbo
echo.
pause
goto menu

:voice_adaptation
cls
echo.
echo  Adaptation vocale - Amélioration de la reconnaissance
echo  ───────────────────────────────────────────────────────
echo.
echo  [INFO] Cette fonctionnalité est en cours de développement.
echo  [INFO] Les scripts d'adaptation vocale ont été déplacés vers temp_debug/
echo.
echo  Pour améliorer la reconnaissance vocale :
echo  1. Utilisez le vocabulaire enrichi dans config.json
echo  2. Parlez clairement et distinctement
echo  3. Utilisez un microphone de qualité
echo.
pause
goto menu

:meeting
cls
echo.
echo  Lancement de Meeting Transcriber...
echo  ───────────────────────────────────
echo.
if exist "%~dp0projects\meeting-transcriber\start.bat" (
    call "%~dp0projects\meeting-transcriber\start.bat"
    if errorlevel 1 (
        echo.
        echo  [ERREUR] Le programme s'est terminé avec une erreur
        pause
    )
) else (
    echo  [ERREUR] Fichier start.bat non trouvé dans meeting-transcriber
    pause
)
goto end

:meeting_pro
cls
echo.
echo  Lancement de Meeting Transcriber PRO...
echo  ───────────────────────────────────────
echo.
echo  [INFO] Ce mode nécessite un token Hugging Face.
echo.
if not defined TOKEN_HF (
    echo  Le token TOKEN_HF n'est pas défini.
    echo.
    set /p hf_token="  Entrez votre token Hugging Face (ou appuyez sur Entrée pour continuer) : "
    if not "!hf_token!"=="" (
        set "TOKEN_HF=!hf_token!"
        echo.
        echo  [OK] Token défini pour cette session.
    )
)
echo.
if exist "%~dp0projects\meeting-transcriber-pro\start.bat" (
    call "%~dp0projects\meeting-transcriber-pro\start.bat"
    if errorlevel 1 (
        echo.
        echo  [ERREUR] Le programme s'est terminé avec une erreur
        pause
    )
) else (
    echo  [ERREUR] Fichier start.bat non trouvé dans meeting-transcriber-pro
    pause
)
goto end

:install_menu
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                      INSTALLATION                                ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  [1] Installation complète VTT (Recommandé)                      ║
echo  ║      • Environnement virtuel isolé                               ║
echo  ║      • Toutes les dépendances                                    ║
echo  ║                                                                  ║
echo  ║  [2] Correction isolation environnement                          ║
echo  ║      • Résout problème NumPy/Numba                               ║
echo  ║                                                                  ║
echo  ║  [3] Vérification système                                        ║
echo  ║      • Diagnostic complet                                        ║
echo  ║                                                                  ║
echo  ║  [R] Retour au menu principal                                    ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
set /p ichoice="  Votre choix [1-3/R] : "

if "%ichoice%"=="1" (
    if exist "%~dp0scripts\install_vtt.bat" (
        call "%~dp0scripts\install_vtt.bat"
    ) else (
        echo [ERREUR] Script install_vtt.bat non trouvé
    )
    pause
    goto install_menu
)
if "%ichoice%"=="2" goto fix_isolation
if "%ichoice%"=="3" (
    if exist "%~dp0scripts\install_vtt.bat" (
        call "%~dp0scripts\install_vtt.bat"
    ) else (
        echo [ERREUR] Script install_vtt.bat non trouvé
    )
    pause
    goto install_menu
)
if /i "%ichoice%"=="R" goto menu
goto install_menu

:documentation
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                      DOCUMENTATION                               ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  Fichiers disponibles :                                          ║
echo  ║                                                                  ║
echo  ║  • README.md         - Vue d'ensemble du projet                  ║
echo  ║  • QUICKSTART.md     - Démarrage rapide                          ║
echo  ║  • MIGRATION_PIPX.md - Guide migration pipx                      ║
echo  ║                                                                  ║
echo  ║  Documentation par projet :                                      ║
echo  ║  • projects\voice-to-text-basic\README.md                        ║
echo  ║  • projects\voice-to-text-turbo\README.md                        ║
echo  ║  • projects\meeting-transcriber\README.md                        ║
echo  ║  • projects\meeting-transcriber-pro\README.md                    ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
echo  [1] Ouvrir README.md
echo  [2] Ouvrir QUICKSTART.md
echo  [3] Ouvrir MIGRATION_PIPX.md
echo  [R] Retour au menu principal
echo.
set /p dchoice="  Votre choix [1-3/R] : "

if "%dchoice%"=="1" (
    if exist "%~dp0README.md" (
        start notepad "%~dp0README.md"
    ) else (
        echo [ERREUR] README.md non trouvé
        pause
    )
    goto documentation
)
if "%dchoice%"=="2" (
    if exist "%~dp0QUICKSTART.md" (
        start notepad "%~dp0QUICKSTART.md"
    ) else (
        echo [ERREUR] QUICKSTART.md non trouvé
        pause
    )
    goto documentation
)
if "%dchoice%"=="3" (
    if exist "%~dp0MIGRATION_PIPX.md" (
        start notepad "%~dp0MIGRATION_PIPX.md"
    ) else (
        echo [ERREUR] MIGRATION_PIPX.md non trouvé
        pause
    )
    goto documentation
)
if /i "%dchoice%"=="R" goto menu
goto documentation

:quit
cls
echo.
echo  Au revoir !
echo.
timeout /t 2 >nul
exit /b 0

:end
echo.
echo  [INFO] Application terminée.
echo.
pause
goto menu

endlocal