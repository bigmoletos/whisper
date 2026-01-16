#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de lancement de Whisper STT avec notifications
Gère correctement les chemins et les dépendances
"""

import sys
import os
import subprocess
import time

def launch_whisper():
    """Lance l'application Whisper STT avec gestion des chemins"""
    
    # Ajouter le répertoire src au PYTHONPATH
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, 'src')
    
    # Configurer l'environnement
    env = os.environ.copy()
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = src_dir + ';' + env['PYTHONPATH']
    else:
        env['PYTHONPATH'] = src_dir
    
    print(f"Lancement de Whisper STT depuis: {script_dir}")
    print(f"Répertoire src: {src_dir}")
    print(f"PYTHONPATH: {env['PYTHONPATH']}")
    
    try:
        # Lancer l'application principale
        result = subprocess.Popen([
            sys.executable, "-m", "src.main"
        ], env=env, cwd=script_dir)
        
        print(f"Application lancée avec PID: {result.pid}")
        print("L'application Whisper STT est maintenant en cours d'exécution.")
        print("Appuyez sur Ctrl+Alt+7 pour démarrer/arrêter l'enregistrement.")
        print("Appuyez sur Ctrl+C dans cette console pour arrêter le service.")
        
        # Attendre que l'utilisateur arrête le programme
        result.wait()
        
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        return False
    
    return True

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("Vérification des dépendances...")
    
    required_packages = [
        'sounddevice',
        'numpy',
        'faster-whisper',
        'win10toast',
        'pywin32',
        'pynput'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} est installé")
        except ImportError:
            print(f"❌ {package} est manquant")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n{len(missing_packages)} packages manquants: {', '.join(missing_packages)}")
        print("Installation des packages manquants...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installé avec succès")
            except subprocess.CalledProcessError:
                print(f"❌ Échec de l'installation de {package}")
        
        return False
    else:
        print("✅ Toutes les dépendances sont installées")
        return True

def main():
    """Fonction principale"""
    print("🚀 Lanceur Whisper STT avec Notifications")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("\n⚠️  Certaines dépendances sont manquantes. Veuillez les installer manuellement.")
        return
    
    print("\nDémarrage de l'application...")
    
    # Lancer l'application
    success = launch_whisper()
    
    if success:
        print("\n🎉 L'application s'est terminée normalement.")
    else:
        print("\n❌ L'application n'a pas pu démarrer correctement.")

if __name__ == "__main__":
    main()