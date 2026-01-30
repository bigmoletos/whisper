#!/usr/bin/env python3
"""
Test simple du module main.py
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
script_dir = Path(__file__).parent
shared_dir = script_dir / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

print(f"[DEBUG] Script directory: {script_dir}")
print(f"[DEBUG] Shared directory: {shared_dir}")
print(f"[DEBUG] Python path: {sys.path[:3]}...")

try:
    print("[DEBUG] Tentative d'import des modules de base...")
    import json
    import logging
    print("[OK] Modules de base importés")
    
    print("[DEBUG] Tentative d'import des modules audio...")
    import numpy as np
    import sounddevice as sd
    print("[OK] Modules audio importés")
    
    print("[DEBUG] Tentative d'import PyTorch...")
    import torch
    print(f"[OK] PyTorch {torch.__version__} importé")
    print(f"[INFO] CUDA disponible: {torch.cuda.is_available()}")
    
    print("[DEBUG] Tentative d'import Faster-Whisper...")
    import faster_whisper
    print("[OK] Faster-Whisper importé")
    
    print("[DEBUG] Tentative d'import des modules système...")
    import pyautogui
    import keyboard
    import pyperclip
    print("[OK] Modules système importés")
    
    print("[DEBUG] Tentative d'import du module main...")
    from src.main import WhisperSTTService
    print("[OK] Module main importé")
    
    print("[DEBUG] Tentative de création du service...")
    config_path = script_dir / "projects" / "voice-to-text-turbo" / "config.json"
    print(f"[DEBUG] Configuration: {config_path}")
    
    if not config_path.exists():
        print(f"[ERREUR] Configuration non trouvée: {config_path}")
        sys.exit(1)
    
    service = WhisperSTTService(str(config_path))
    print("[SUCCESS] Service créé avec succès!")
    
    print("[INFO] Test terminé - tout fonctionne correctement")
    
except ImportError as e:
    print(f"[ERREUR IMPORT] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
except Exception as e:
    print(f"[ERREUR GENERALE] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)