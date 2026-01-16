#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script pour forcer l'installation de faster-whisper
"""

import sys
import subprocess
import platform

def force_install_faster_whisper():
    """Essaie différentes méthodes pour installer faster-whisper"""
    
    print("Tentative de forcer l'installation de faster-whisper...")
    print("=" * 50)
    
    # Méthode 1: Installation standard avec no-build-isolation
    print("\nMéthode 1: Installation avec --no-build-isolation")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "faster-whisper", "--no-build-isolation"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("[SUCCESS] Installation réussie avec méthode 1")
            return True
        else:
            print(f"[ERREUR] Échec méthode 1: {result.stderr[:200]}")
    except Exception as e:
        print(f"❌ Erreur méthode 1: {e}")
    
    # Méthode 2: Installation de la version 1.2.0
    print("\nMéthode 2: Installation de la version 1.2.0")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "faster-whisper==1.2.0", "--no-build-isolation"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("[SUCCESS] Installation réussie avec méthode 2")
            return True
        else:
            print(f"[ERREUR] Échec méthode 2: {result.stderr[:200]}")
    except Exception as e:
        print(f"❌ Erreur méthode 2: {e}")
    
    # Méthode 3: Installation des dépendances séparément
    print("\nMéthode 3: Installation des dépendances séparément")
    try:
        # Installer ctranslate2 d'abord
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "ctranslate2", "--no-build-isolation"
        ], capture_output=True, text=True, timeout=300)
        
        # Installer huggingface-hub
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "huggingface-hub"
        ], capture_output=True, text=True, timeout=300)
        
        # Installer tokenizers
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "tokenizers"
        ], capture_output=True, text=True, timeout=300)
        
        # Installer faster-whisper sans dépendances
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "faster-whisper", "--no-deps"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("[SUCCESS] Installation réussie avec méthode 3")
            return True
        else:
            print(f"[ERREUR] Échec méthode 3: {result.stderr[:200]}")
    except Exception as e:
        print(f"❌ Erreur méthode 3: {e}")
    
    # Méthode 4: Installation via conda (si disponible)
    print("\nMéthode 4: Installation via conda")
    try:
        result = subprocess.run([
            "conda", "install", "-c", "conda-forge", 
            "faster-whisper", "-y"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("[SUCCESS] Installation réussie avec méthode 4 (conda)")
            return True
        else:
            print(f"[ERREUR] Échec méthode 4: {result.stderr[:200]}")
    except Exception as e:
        print(f"❌ Erreur méthode 4: {e}")
    
    return False

def suggest_alternatives():
    """Propose des alternatives si l'installation échoue"""
    
    print("\n" + "=" * 50)
    print("ALTERNATIVES SI L'INSTALLATION ÉCHOUE")
    print("=" * 50)
    
    print("\n1. Utiliser Whisper standard (moins performant mais stable):")
    print("   Modifiez config.json:")
    print('   "engine": "whisper"')
    
    print("\n2. Installer Rust et réessayer:")
    print("   winget install Rustlang.Rustup")
    print("   pip uninstall faster-whisper")
    print("   pip install faster-whisper")
    
    print("\n3. Utiliser Python 3.11 au lieu de 3.12:")
    print("   py -3.11 -m pip install faster-whisper")
    
    print("\n4. Installer depuis les sources:")
    print("   git clone https://github.com/guillaumekln/faster-whisper.git")
    print("   cd faster-whisper")
    print("   pip install .")

def main():
    """Fonction principale"""
    
    print("Script de forçage d'installation de faster-whisper")
    print("Version de Python:", sys.version)
    print("Système:", platform.system())
    
    success = force_install_faster_whisper()
    
    if success:
        print("\n[SUCCESS] Installation de faster-whisper réussie !")
        print("Vous pouvez maintenant lancer l'application avec:")
        print("py -3.12 run_whisper.bat")
    else:
        print("\n[AVERTISSEMENT] Impossible d'installer faster-whisper")
        suggest_alternatives()

if __name__ == "__main__":
    main()