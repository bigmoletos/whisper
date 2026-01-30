@echo off
chcp 65001 >nul

echo ================================================
echo    TEST EXISTENCE DES FICHIERS
echo ================================================
echo.

echo [INFO] Vérification des fichiers requis...
echo.

:: Vérifier main.py
if exist "shared\src\main.py" (
    echo [OK] shared\src\main.py
) else (
    echo [ERREUR] shared\src\main.py MANQUANT
    goto :error
)

:: Vérifier config.json
if exist "projects\voice-to-text-turbo\config.json" (
    echo [OK] projects\voice-to-text-turbo\config.json
) else (
    echo [ERREUR] projects\voice-to-text-turbo\config.json MANQUANT
    goto :error
)

:: Vérifier les modules Python dans shared/src
echo.
echo [INFO] Vérification des modules Python...

if exist "shared\src\audio_capture.py" (
    echo [OK] audio_capture.py
) else (
    echo [ERREUR] audio_capture.py MANQUANT
)

if exist "shared\src\whisper_transcriber.py" (
    echo [OK] whisper_transcriber.py
) else (
    echo [ERREUR] whisper_transcriber.py MANQUANT
)

if exist "shared\src\faster_whisper_transcriber.py" (
    echo [OK] faster_whisper_transcriber.py
) else (
    echo [WARNING] faster_whisper_transcriber.py MANQUANT (optionnel)
)

if exist "shared\src\text_injector.py" (
    echo [OK] text_injector.py
) else (
    echo [ERREUR] text_injector.py MANQUANT
)

if exist "shared\src\keyboard_hotkey.py" (
    echo [OK] keyboard_hotkey.py
) else (
    echo [ERREUR] keyboard_hotkey.py MANQUANT
)

echo.
echo [SUCCESS] Vérification des fichiers terminée
goto :end

:error
echo.
echo [ERREUR] Des fichiers critiques sont manquants
echo [INFO] Le projet semble incomplet

:end
pause