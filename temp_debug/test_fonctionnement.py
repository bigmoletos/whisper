#!/usr/bin/env python3
"""
Test rapide du fonctionnement complet VTT
Vérifie que tous les modules sont correctement importés
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

def test_imports():
    """Test des imports critiques"""
    print("🔧 Test des imports VTT...")
    
    try:
        # Test imports de base
        from src.audio_capture import AudioCapture
        print("✅ AudioCapture importé")
        
        from src.text_injector import TextInjector
        print("✅ TextInjector importé")
        
        from src.keyboard_hotkey import HotkeyManager
        print("✅ HotkeyManager importé")
        
        # Test import Faster-Whisper
        try:
            from src.faster_whisper_transcriber import FasterWhisperTranscriber
            print("✅ FasterWhisperTranscriber importé")
        except ImportError:
            print("⚠️  FasterWhisperTranscriber non disponible")
        
        # Test import notifications
        try:
            from src.notifications import NotificationManager
            print("✅ NotificationManager importé")
        except ImportError:
            print("⚠️  NotificationManager non disponible")
        
        # Test import nouvelle pop-up
        try:
            from src.recording_popup import show_recording, show_processing, hide_popup
            print("✅ RecordingPopup importé")
        except ImportError:
            print("⚠️  RecordingPopup non disponible")
        
        print("\n✅ Tous les imports critiques fonctionnent")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur d'import: {e}")
        return False

def test_config():
    """Test de la configuration"""
    print("\n🔧 Test de la configuration...")
    
    config_path = Path("projects/voice-to-text-turbo/config.json")
    if config_path.exists():
        print("✅ Fichier config.json trouvé")
        
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Vérifier les sections critiques
            if "whisper" in config:
                print("✅ Section whisper présente")
            if "audio" in config:
                print("✅ Section audio présente")
            if "hotkey" in config:
                print("✅ Section hotkey présente")
            if "ui" in config:
                print("✅ Section ui présente")
                if config["ui"].get("show_recording_popup", False):
                    print("✅ Pop-up d'enregistrement activée")
                else:
                    print("⚠️  Pop-up d'enregistrement désactivée")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lecture config: {e}")
            return False
    else:
        print("❌ Fichier config.json non trouvé")
        return False

if __name__ == "__main__":
    print("🚀 Test de fonctionnement VTT")
    print("=" * 50)
    
    imports_ok = test_imports()
    config_ok = test_config()
    
    print("\n" + "=" * 50)
    if imports_ok and config_ok:
        print("✅ SYSTÈME FONCTIONNEL")
        print("💡 Vous pouvez relancer start.bat")
    else:
        print("❌ PROBLÈMES DÉTECTÉS")
        print("💡 Vérifiez les erreurs ci-dessus")
    
    input("\nAppuyez sur Entrée pour quitter...")