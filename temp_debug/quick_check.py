#!/usr/bin/env python3
"""
Vérification rapide du système VTT au démarrage
Vérifie seulement les éléments critiques sans installation automatique
"""

import sys
import os

def quick_system_check():
    """Vérification rapide et silencieuse du système"""
    try:
        # Vérifier Python 3.12 (déjà fait par l'appel du script)
        
        # Vérifier les modules critiques
        import json, logging, pathlib
        import numpy, sounddevice, pyautogui, keyboard, pyperclip
        
        # Vérifier PyTorch et CUDA
        import torch
        if not torch.cuda.is_available():
            return False, "CUDA non disponible"
        
        # Vérifier Faster-Whisper
        import faster_whisper
        
        # Test rapide Faster-Whisper (sans charger de modèle)
        # Juste vérifier que l'import fonctionne
        
        # Vérifier les fichiers de configuration
        config_path = os.path.join('projects', 'voice-to-text-turbo', 'config.json')
        main_path = os.path.join('shared', 'src', 'main.py')
        
        if not os.path.exists(config_path):
            return False, "Configuration manquante"
        
        if not os.path.exists(main_path):
            return False, "Fichier principal manquant"
        
        return True, "Système OK"
        
    except ImportError as e:
        return False, f"Module manquant: {e}"
    except Exception as e:
        return False, f"Erreur: {e}"

if __name__ == "__main__":
    success, message = quick_system_check()
    if success:
        print("[OK] Système prêt")
        sys.exit(0)
    else:
        print(f"[INFO] {message} - Utilisez [U] pour diagnostic complet")
        sys.exit(1)