@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

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
echo  ║  [1] Voice-to-Text BASIC                                         ║
echo  ║      Transcription simple avec Whisper standard                  ║
echo  ║      • Fonctionne sur CPU (pas de GPU requis)                    ║
echo  ║      • Idéal pour : dictée vocale, notes rapides                 ║
echo  ║      • Raccourci : Ctrl+Alt+7 (toggle enregistrement)           ║
echo  ║                                                                  ║
echo  ║  [2] Voice-to-Text TURBO                                         ║
echo  ║      Transcription rapide avec Faster-Whisper                    ║
echo  ║      • Accélération GPU (4x plus rapide)                         ║
echo  ║      • Idéal pour : transcription fluide en temps réel           ║
echo  ║      • Requiert : GPU NVIDIA recommandé (fonctionne aussi CPU)   ║
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
echo  ║  [I] Installation des dépendances                                ║
echo  ║  [D] Documentation                                               ║
echo  ║  [Q] Quitter                                                     ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
set /p choice="  Votre choix [1-4/I/D/Q] : "

if /i "%choice%"=="1" goto voice_basic
if /i "%choice%"=="2" goto voice_turbo
if /i "%choice%"=="3" goto meeting
if /i "%choice%"=="4" goto meeting_pro
if /i "%choice%"=="I" goto install_menu
if /i "%choice%"=="D" goto documentation
if /i "%choice%"=="Q" goto quit
if /i "%choice%"=="q" goto quit

echo.
echo  [!] Choix invalide. Appuyez sur une touche...
pause >nul
goto menu

:voice_basic
cls
echo.
echo  Lancement de Voice-to-Text BASIC...
echo  ───────────────────────────────────
echo.
call "%~dp0projects\voice-to-text-basic\start.bat"
goto end

:voice_turbo
cls
echo.
echo  Lancement de Voice-to-Text TURBO...
echo  ───────────────────────────────────
echo.
call "%~dp0projects\voice-to-text-turbo\start.bat"
goto end

:meeting
cls
echo.
echo  Lancement de Meeting Transcriber...
echo  ───────────────────────────────────
echo.
call "%~dp0projects\meeting-transcriber\start.bat"
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
call "%~dp0projects\meeting-transcriber-pro\start.bat"
goto end

:install_menu
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                      INSTALLATION                                ║
echo  ╠══════════════════════════════════════════════════════════════════╣
echo  ║                                                                  ║
echo  ║  [1] Installation de base (Voice-to-Text)                        ║
echo  ║  [2] Installation Faster-Whisper (GPU)                           ║
echo  ║  [3] Installation Meeting Assistant                              ║
echo  ║  [4] Installation complète (tout)                                ║
echo  ║                                                                  ║
echo  ║  [R] Retour au menu principal                                    ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.
set /p ichoice="  Votre choix [1-4/R] : "

if "%ichoice%"=="1" (
    call "%~dp0scripts\install.bat"
    pause
    goto install_menu
)
if "%ichoice%"=="2" (
    call "%~dp0scripts\install_faster_whisper.bat"
    pause
    goto install_menu
)
if "%ichoice%"=="3" (
    call "%~dp0scripts\install_meeting_assistant.bat"
    pause
    goto install_menu
)
if "%ichoice%"=="4" (
    echo.
    echo  Installation complète en cours...
    call "%~dp0scripts\install.bat"
    call "%~dp0scripts\install_faster_whisper.bat"
    call "%~dp0scripts\install_meeting_assistant.bat"
    echo.
    echo  [OK] Installation complète terminée.
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
echo  [R] Retour au menu principal
echo.
set /p dchoice="  Votre choix [1-2/R] : "

if "%dchoice%"=="1" (
    start notepad "%~dp0README.md"
    goto documentation
)
if "%dchoice%"=="2" (
    start notepad "%~dp0QUICKSTART.md"
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
