#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de vérification de la version de Python
"""

import sys
import subprocess

def check_python_version():
    """Vérifie que la version de Python est compatible"""
    
    major = sys.version_info.major
    minor = sys.version_info.minor
    
    print(f"Version de Python détectée: {major}.{minor}.{sys.version_info.micro}")
    
    # Vérifier la version minimale
    if major < 3:
        print("[ERREUR] Python 2.x n'est pas supporté")
        print("Veuillez installer Python 3.10 ou supérieur")
        return False
    
    if major == 3:
        if minor < 10:
            print("[ERREUR] Python 3.9 et versions antérieures ne sont pas supportées")
            print("Veuillez installer Python 3.10 ou supérieur")
            return False
        elif minor == 10:
            print("[AVERTISSEMENT] Python 3.10 est supporté mais certaines fonctionnalités peuvent être limitées")
            print("Recommandé: Python 3.11 ou 3.12 pour une meilleure compatibilité")
            return True
        elif minor == 11 or minor == 12:
            print("[OK] Version de Python optimale pour Whisper STT")
            return True
        elif minor == 13:
            print("[AVERTISSEMENT] Python 3.13 est très récent et peut avoir des problèmes de compatibilité")
            print("Recommandé: Utiliser Python 3.11 ou 3.12")
            return True
        elif minor >= 14:
            print("[AVERTISSEMENT] Python 3.14+ peut avoir des problèmes avec faster-whisper")
            print("Recommandé: Utiliser Python 3.11 ou 3.12")
            print("Solutions:")
            print("  1. Installez Python 3.11 ou 3.12")
            print("  2. Utilisez Whisper standard au lieu de Faster-Whisper")
            print("  3. Essayez: pip install faster-whisper --no-build-isolation")
            return True
    
    return True

def suggest_python_installation():
    """Propose des méthodes d'installation de Python"""
    
    print("\n[INFORMATION] Méthodes d'installation de Python:")
    print("\n1. Installation via Microsoft Store (recommandé pour Windows):")
    print("   - Ouvrez Microsoft Store")
    print("   - Cherchez 'Python 3.11' ou 'Python 3.12'")
    print("   - Installez la version souhaitée")
    
    print("\n2. Installation via le site officiel:")
    print("   - Téléchargez depuis https://www.python.org/downloads/")
    print("   - Choisissez Python 3.11.4 ou 3.12.0")
    print("   - Cochez 'Add Python to PATH' pendant l'installation")
    
    print("\n3. Installation via winget (Windows Package Manager):")
    print("   winget install Python.Python.3.11")
    print("   ou")
    print("   winget install Python.Python.3.12")
    
    print("\n4. Installation via chocolatey:")
    print("   choco install python --version=3.11.4")
    print("   ou")
    print("   choco install python --version=3.12.0")

def check_multiple_python_versions():
    """Vérifie si plusieurs versions de Python sont disponibles"""
    
    print("\n[INFORMATION] Vérification des autres versions de Python disponibles...")
    
    # Tester les versions courantes
    versions_to_test = [
        ("3.12", "py -3.12 --version"),
        ("3.11", "py -3.11 --version"),
        ("3.10", "py -3.10 --version")
    ]
    
    available_versions = []
    
    for version, command in versions_to_test:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0 and "Python" in result.stdout:
                print(f"[OK] Python {version} est disponible: {result.stdout.strip()}")
                available_versions.append(version)
            else:
                print(f"[INFO] Python {version} n'est pas disponible")
        except:
            print(f"[INFO] Python {version} n'est pas disponible")
    
    if available_versions:
        print(f"\n[CONSEIL] Vous pouvez lancer l'application avec une version spécifique:")
        for version in available_versions:
            print(f"   py -{version} run_whisper.bat")
    
    return available_versions

if __name__ == "__main__":
    print("Vérification de la version de Python pour Whisper STT")
    print("=" * 50)
    
    # Vérifier la version actuelle
    version_ok = check_python_version()
    
    # Vérifier les autres versions disponibles
    available_versions = check_multiple_python_versions()
    
    if not version_ok:
        suggest_python_installation()
        sys.exit(1)
    else:
        if available_versions:
            print(f"\n[CONSEIL] Pour une meilleure compatibilité, utilisez:")
            for version in ["3.12", "3.11"]:
                if version in available_versions:
                    print(f"   py -{version} run_whisper.bat")
                    break
        
        print("\n[OK] Version de Python compatible détectée")
        sys.exit(0)