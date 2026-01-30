#!/usr/bin/env python3
"""
Debug de la pop-up d'enregistrement
Diagnostique pourquoi la nouvelle pop-up ne s'affiche pas
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

def debug_popup_import():
    """Debug de l'import de la pop-up"""
    print("🔍 Debug import pop-up...")
    
    try:
        # Test import direct
        from src.recording_popup import show_recording, show_processing, hide_popup
        print("✅ Import recording_popup réussi")
        
        # Test de la variable RECORDING_POPUP_AVAILABLE
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "shared"))
        
        # Simuler l'import comme dans main.py
        try:
            from src.recording_popup import show_recording, show_processing, hide_popup
            RECORDING_POPUP_AVAILABLE = True
            print("✅ RECORDING_POPUP_AVAILABLE = True")
        except ImportError:
            RECORDING_POPUP_AVAILABLE = False
            print("❌ RECORDING_POPUP_AVAILABLE = False")
        
        return RECORDING_POPUP_AVAILABLE
        
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def debug_config():
    """Debug de la configuration UI"""
    print("\n🔍 Debug configuration UI...")
    
    try:
        import json
        config_path = Path("projects/voice-to-text-turbo/config.json")
        
        if not config_path.exists():
            print("❌ Fichier config.json non trouvé")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        ui_config = config.get("ui", {})
        show_popup = ui_config.get("show_recording_popup", True)
        
        print(f"✅ Configuration UI trouvée")
        print(f"   show_recording_popup: {show_popup}")
        
        if not show_popup:
            print("⚠️  Pop-up désactivée dans la configuration !")
        
        return show_popup
        
    except Exception as e:
        print(f"❌ Erreur config: {e}")
        return False

def debug_tkinter():
    """Debug de tkinter"""
    print("\n🔍 Debug tkinter...")
    
    try:
        import tkinter as tk
        print("✅ tkinter disponible")
        
        # Test création fenêtre
        root = tk.Tk()
        root.withdraw()  # Cacher immédiatement
        root.destroy()
        print("✅ Création fenêtre tkinter OK")
        
        return True
        
    except ImportError:
        print("❌ tkinter non disponible")
        return False
    except Exception as e:
        print(f"❌ Erreur tkinter: {e}")
        return False

def test_popup_direct():
    """Test direct de la pop-up"""
    print("\n🔍 Test direct de la pop-up...")
    
    try:
        from src.recording_popup import show_recording, hide_popup
        
        print("📍 Affichage pop-up test (3 secondes)...")
        show_recording()
        
        import time
        time.sleep(3)
        
        hide_popup()
        print("✅ Test pop-up réussi")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test pop-up: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Debug Pop-up VTT")
    print("=" * 50)
    
    # Tests de diagnostic
    import_ok = debug_popup_import()
    config_ok = debug_config()
    tkinter_ok = debug_tkinter()
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS:")
    print(f"   Import pop-up: {'✅' if import_ok else '❌'}")
    print(f"   Configuration: {'✅' if config_ok else '❌'}")
    print(f"   Tkinter: {'✅' if tkinter_ok else '❌'}")
    
    if import_ok and config_ok and tkinter_ok:
        print("\n🧪 Test direct de la pop-up...")
        test_popup_direct()
    else:
        print("\n❌ Problèmes détectés - Pop-up ne peut pas fonctionner")
    
    input("\nAppuyez sur Entrée pour quitter...")