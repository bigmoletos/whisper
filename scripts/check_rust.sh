#!/bin/bash
# Script de vérification de l'installation Rust
# Auteur: Bigmoletos
# Date: 2026-01-18

echo "============================================"
echo "  Vérification de Rust"
echo "============================================"
echo ""

# Charger l'environnement Rust si disponible
if [ -f "$HOME/.cargo/env" ]; then
    source "$HOME/.cargo/env"
fi

# Vérifier rustc
echo "1. Vérification de rustc..."
if command -v rustc &> /dev/null; then
    rustc --version
    echo "✅ rustc est installé et disponible"
else
    echo "❌ rustc n'est pas installé ou pas dans le PATH"
    echo ""
    echo "Installation de Rust:"
    echo "  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

echo ""

# Vérifier cargo
echo "2. Vérification de cargo..."
if command -v cargo &> /dev/null; then
    cargo --version
    echo "✅ cargo est installé et disponible"
else
    echo "❌ cargo n'est pas installé"
    exit 1
fi

echo ""

# Test de compilation
echo "3. Test de compilation..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

cargo new test_rust --bin --quiet 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Projet de test créé"

    cd test_rust
    echo "   Compilation en cours..."

    if cargo build --release --quiet 2>&1; then
        echo "✅ Compilation réussie"

        if ./target/release/test_rust | grep -q "Hello, world!"; then
            echo "✅ Exécution réussie"
        else
            echo "⚠️  Compilation OK mais exécution a échoué"
        fi
    else
        echo "❌ Échec de la compilation"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
else
    echo "❌ Échec de la création du projet"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Nettoyage
rm -rf "$TEMP_DIR"

echo ""
echo "============================================"
echo "✅ Rust est installé et fonctionne correctement"
echo "============================================"
echo ""
echo "Vous pouvez maintenant installer faster-whisper:"
echo "  pip install faster-whisper"
echo ""

exit 0
