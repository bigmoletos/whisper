@echo off
REM Script de lancement Whisper avec limitation mémoire MKL
REM Utile quand Neo4j/Memgraph/autres apps utilisent beaucoup de RAM

echo Lancement de Whisper STT avec limitation memoire MKL...
echo.

REM Limiter les threads MKL et OpenMP pour reduire l'usage memoire
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set NUMEXPR_NUM_THREADS=1

REM Augmenter la limite d'allocation MKL (en MB)
set MKL_MALLOC_HEAP_LIMIT=1024

REM Lancer l'application
cd /d "%~dp0"
..\..\venv_vtt_isolated\Scripts\python.exe main.py

pause
