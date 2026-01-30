#!/usr/bin/env python3
"""
Version minimale de Voice-to-Text Turbo
Sans dépendances complexes pour diagnostic
"""

import sys
import json
import time
from pathlib import Path

def main():
    print("=== VOICE-TO-TEXT TURBO MINIMAL ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    
    # Test configuration
    config_path = Path("projects/voice-to-text-turbo/config.json")
    if not config_path.exists():
        print(f"[ERREUR] Configuration non trouvée: {config_path}")
        return 1
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[OK] Configuration chargée: {config['whisper']['engine']}")
    except Exception as e:
        print(f"[ERREUR] Lecture configuration: {e}")
        return 1
    
    # Test imports critiques un par un
    modules_to_test = [
        ("numpy", "import numpy as np"),
        ("torch", "import torch"),
        ("sounddevice", "import sounddevice"),
        ("faster_whisper", "import faster_whisper"),
        ("pyautogui", "import pyautogui"),
        ("keyboard", "import keyboard")
    ]
    
    for name, import_cmd in modules_to_test:
        try:
            exec(import_cmd)
            print(f"[OK] {name}")
        except ImportError as e:
            print(f"[MANQUANT] {name}: {e}")
            return 1
    
    # Test CUDA
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"[INFO] CUDA disponible: {cuda_available}")
        if cuda_available:
            print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")
    except:
        print("[WARNING] Impossible de tester CUDA")
    
    print("[SUCCESS] Tous les tests passés - Voice-to-Text Turbo devrait fonctionner")
    print("[INFO] Appuyez sur Ctrl+C pour arrêter")
    
    # Boucle simple pour maintenir le programme ouvert
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt demandé par l'utilisateur")
        return 0

if __name__ == "__main__":
    sys.exit(main())