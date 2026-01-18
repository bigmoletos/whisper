#!/bin/bash

# Script de lancement simple pour Whisper STT avec Faster-Whisper
# Auteur: Bigmoletos
# Date: 2026-01-18

set -e  # Arrêter en cas d'erreur

echo "============================================"
echo "  Whisper STT - Faster-Whisper"
echo "============================================"
echo ""

# Changer vers le répertoire racine du projet
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "Répertoire du projet: $PROJECT_ROOT"
echo ""

# Vérifier Python
echo "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[ERREUR] Python n'est pas installé ou n'est pas dans le PATH"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD --version
echo "[OK] Python détecté"
echo ""

# Vérifier et configurer faster-whisper dans config.json
echo "Vérification et configuration..."
$PYTHON_CMD scripts/config_checker.py
if [ $? -ne 0 ]; then
    echo "[ERREUR] Impossible de configurer config.json"
    exit 1
fi
echo ""

# Vérifier que faster-whisper est installé
echo "Vérification de faster-whisper..."
if $PYTHON_CMD -c "import faster_whisper; print('[OK] faster-whisper est installé')" 2>/dev/null; then
    echo ""
else
    echo "[ERREUR] faster-whisper n'est pas installé"
    echo ""

    # Essayer avec pipx d'abord (recommandé)
    if command -v pipx &> /dev/null; then
        echo "Installation de faster-whisper avec pipx..."
        pipx install faster-whisper
        if [ $? -eq 0 ]; then
            echo "[OK] faster-whisper installé avec succès via pipx"
        else
            echo "[ERREUR] L'installation via pipx a échoué"
            echo ""
            echo "Solutions:"
            echo "1. Installez Rust depuis https://rustup.rs/"
            echo "2. Essayez: pip install faster-whisper --no-build-isolation"
            echo "3. Modifiez config.json pour utiliser \"engine\": \"whisper\""
            echo ""
            exit 1
        fi
    else
        # Sinon essayer pip
        echo "pipx non disponible, essai avec pip..."

        # Détecter si on est dans un virtualenv
        if [ -n "$VIRTUAL_ENV" ]; then
            echo "Environnement virtuel détecté: $VIRTUAL_ENV"
            $PYTHON_CMD -m pip install faster-whisper
        else
            echo "Installation en mode utilisateur..."
            $PYTHON_CMD -m pip install faster-whisper --user
        fi

        if [ $? -ne 0 ]; then
            echo ""
            echo "[ERREUR] L'installation de faster-whisper a échoué"
            echo ""
            echo "Solutions:"
            echo "1. Installez pipx: sudo apt install pipx"
            echo "2. Installez Rust depuis https://rustup.rs/"
            if [ -n "$VIRTUAL_ENV" ]; then
                echo "3. Essayez: pip install faster-whisper"
            else
                echo "3. Essayez: pip install faster-whisper --user"
            fi
            echo "4. Modifiez config.json pour utiliser \"engine\": \"whisper\""
            echo ""
            exit 1
        fi
        echo "[OK] faster-whisper installé avec succès"
    fi
fi

echo ""
echo "============================================"
echo "  Démarrage de l'application"
echo "============================================"
echo ""
echo "Raccourci: Ctrl+Alt+7"
echo "Arrêt: Ctrl+C"
echo ""

# Lancer l'application
$PYTHON_CMD -m src.main

EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "[OK] Application terminée normalement"
else
    echo "[ERREUR] Application terminée avec une erreur (code: $EXIT_CODE)"
fi

exit $EXIT_CODE
