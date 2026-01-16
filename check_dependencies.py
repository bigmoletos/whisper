#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de vérification des dépendances
"""

import sys
import subprocess
import json

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
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f'[OK] {package} est installé')
        except ImportError:
            print(f'[ERREUR] {package} est manquant')
            missing.append(package)
    
    if missing:
        print(f'\n[AVERTISSEMENT] {len(missing)} package(s) manquant(s): {missing}')
        print('Installation automatique avec pipx (si disponible) ou pip...')
        
        # Vérifier si pipx est disponible
        try:
            subprocess.check_call(['pipx', '--version'],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            use_pipx = True
            print('Utilisation de pipx pour l\'installation')
        except:
            use_pipx = False
            print('pipx non disponible, utilisation de pip')
        
        for package in missing:
            try:
                if use_pipx:
                    # Utiliser pipx pour les installations globales
                    subprocess.check_call(['pipx', 'install', package],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    # Utiliser pip pour les installations locales
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f'✓ {package} installé')
            except:
                print(f'✗ Échec de l\'installation de {package}')
                print(f'   Essayez: pipx install {package} ou python -m pip install {package}')
                
                # Solutions spécifiques pour faster-whisper
                if package == 'faster-whisper':
                    print('')
                    print('   Solutions pour faster-whisper:')
                    print('   1. Essayez: pip install faster-whisper --no-build-isolation')
                    print('   2. Essayez: pip install faster-whisper==1.2.1')
                    print('   3. Utilisez Python 3.11 ou 3.12 au lieu de 3.14')
                    print('   4. Modifiez config.json pour utiliser "engine": "whisper"')
                    print('   5. Essayez: conda install -c conda-forge faster-whisper')
        
        return False
    else:
        print("✅ Toutes les dépendances sont installées")
        return True

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1)