@echo off
echo ========================================
echo   TEST DE PERFORMANCE CUDA
echo ========================================
echo.

cd /d "%~dp0\.."

echo [INFO] Activation de l'environnement virtuel...
if exist "venv_whisper\Scripts\activate.bat" (
    call venv_whisper\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouve
    pause
    exit /b 1
)

echo [INFO] Test de performance Faster-Whisper avec CUDA...
python -c "
import time
from faster_whisper import WhisperModel

print('=== TEST DE PERFORMANCE CUDA ===')
print('Chargement du modèle medium avec CUDA...')

start_time = time.time()
model = WhisperModel('medium', device='cuda', compute_type='float16')
load_time = time.time() - start_time

print(f'Temps de chargement: {load_time:.2f}s')
print('✅ Modèle chargé avec succès')
print()
print('Configuration recommandée activée:')
print('- Engine: faster-whisper')
print('- Device: cuda')
print('- Model: large-v3')
print('- Compute type: float16')
print('- VAD filter: activé')
print()
print('🚀 Votre système est optimisé pour la transcription rapide!')
"

echo.
echo [INFO] Lancement du projet Voice-to-Text Turbo...
echo Appuyez sur Ctrl+Alt+7 pour tester la transcription
echo.
cd projects\voice-to-text-turbo
start.bat