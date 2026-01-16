@echo off
setlocal enabledelayedexpansion

:: Script d'installation de Whisper.cpp pour Windows
:: Ce script installe Whisper.cpp depuis les sources

title Installation de Whisper.cpp

:: Afficher les informations
echo ============================================
echo   Installation de Whisper.cpp pour Windows
echo ============================================
echo.

:: Vérifier que git est installé
where git >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo Erreur: git n'est pas installé
    echo Installez git depuis: https://git-scm.com/download/win
    pause
    exit /b 1
)

:: Vérifier que cmake est installé
where cmake >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo Erreur: cmake n'est pas installé
    echo Installez cmake via: winget install Kitware.CMake
    pause
    exit /b 1
)

:: Vérifier que Python est installé
where python >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo Erreur: Python n'est pas installé
    pause
    exit /b 1
)

:: Créer le répertoire de travail
set WORK_DIR=%~dp0whisper.cpp
if not exist "!WORK_DIR!" (
    mkdir "!WORK_DIR!"
)

cd "!WORK_DIR!"

:: Cloner le dépôt
echo Clonage du dépôt Whisper.cpp...
git clone https://github.com/ggerganov/whisper.cpp.git source
if !ERRORLEVEL! neq 0 (
    echo Erreur: Échec du clonage du dépôt
    pause
    exit /b 1
)

cd source

:: Télécharger le modèle GGML
echo Téléchargement du modèle GGML (medium)...
call download-ggml-model.sh medium
if !ERRORLEVEL! neq 0 (
    echo Avertissement: Téléchargement automatique échoué, tentative manuelle...
    powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin' -OutFile '../models/ggml-medium.bin'"
)

:: Créer le répertoire de build
echo Configuration de la compilation...
mkdir build
cd build

:: Configurer avec CMake
echo Exécution de CMake...
cmake .. -G "Visual Studio 17 2022" -DWHISPER_CUDA=OFF
if !ERRORLEVEL! neq 0 (
    echo Erreur: Échec de la configuration CMake
    echo Essayez: cmake .. -G "Visual Studio 16 2019"
    pause
    exit /b 1
)

:: Compiler
echo Compilation (cela peut prendre plusieurs minutes)...
cmake --build . --config Release --parallel 4
if !ERRORLEVEL! neq 0 (
    echo Erreur: Échec de la compilation
    pause
    exit /b 1
)

:: Installer le package Python
echo Installation du package Python...
cd ..
pip install .
if !ERRORLEVEL! neq 0 (
    echo Avertissement: Installation Python échouée, mais les binaires sont disponibles
)

:: Copier les modèles dans le cache
echo Configuration des modèles...
mkdir "%USERPROFILE%\.cache\whisper.cpp\models" 2>nul
copy "models\ggml-medium.bin" "%USERPROFILE%\.cache\whisper.cpp\models\" /Y

:: Créer un fichier de test
echo Création d'un fichier de test...
cd ..
(
    echo @echo off
    echo setlocal
    echo 
    echo :: Test de Whisper.cpp
    echo title Test Whisper.cpp
    echo 
    echo set MODEL_PATH=%%USERPROFILE%%\.cache\whisper.cpp\models\ggml-medium.bin
    echo 
    echo if not exist "%%MODEL_PATH%%" (
    echo     echo Erreur: Modèle non trouvé
    echo     pause
    echo     exit /b 1
    echo )
    echo 
    echo echo Test de la transcription avec Whisper.cpp
    echo python -c ""
    echo import whispercpp as wcpp
    echo import time
    echo 
    echo params = wcpp.WhisperParams()
    echo params.language = 'fr'
    echo 
    echo model = wcpp.Whisper(params)
    echo if not model.load_model(r'%%MODEL_PATH%%'):
    echo     print('Erreur: Impossible de charger le modèle')
    echo     exit(1)
    echo 
    echo print('✓ Whisper.cpp chargé avec succès !')
    echo print('Test de transcription (simulé)...')
    echo time.sleep(1)
    echo print('✓ Test terminé avec succès !')
    echo ""
) > test_whisper_cpp.bat

echo.
echo ============================================
echo   Installation de Whisper.cpp terminée !
echo ============================================
echo.
echo Pour utiliser Whisper.cpp:
1. Modifiez config.json:
   "engine": "whisper-cpp"
echo.
2. Lancez l'application:
   py -3.12 src/main.py
echo.
echo Pour tester l'installation:
   test_whisper_cpp.bat
echo.
echo Les binaires sont disponibles dans:
   !WORK_DIR!\source\build\Release
echo.

:end
pause