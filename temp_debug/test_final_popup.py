#!/usr/bin/env python3
"""
Test final de la pop-up d'enregistrement
Vérifie que tout fonctionne correctement
"""

import sys
import time
import json
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_configuration():
    """Test de la configuration"""
    print("🔧 Test configuration...")
    
    config_path = Path("projects/voice-to-text-turbo/config.json")
    if not config_path.exists():
        print("❌ Fichier config.json non trouvé")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        ui_config = config.get("ui", {})
        popup_enabled = ui_config.get("show_recording_popup", False)
        
        print(f"✅ Configuration chargée")
        print(f"   show_recording_popup: {popup_enabled}")
        
        if not popup_enabled:
            print("⚠️  Pop-up désactivée dans la configuration")
            print("   Pour l'activer, modifiez 'show_recording_popup': true")
        
        return popup_enabled
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False


def test_import():
    """Test d'import du module"""
    print("\n📦 Test import module...")
    
    try:
        from src.recording_popup import show_recording, show_processing, hide_popup
        print("✅ Module recording_popup importé")
        return True
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        return False


def test_tkinter():
    """Test de tkinter"""
    print("\n🖼️  Test tkinter...")
    
    try:
        import tkinter as tk
        
        # Test création fenêtre
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        
        print("✅ Tkinter fonctionnel")
        return True
        
    except Exception as e:
        print(f"❌ Erreur tkinter: {e}")
        return False


def test_popup_functionality():
    """Test de fonctionnalité de la pop-up"""
    print("\n🎯 Test fonctionnalité pop-up...")
    
    try:
        from src.recording_popup import show_recording, show_processing, hide_popup
        
        print("📍 Affichage enregistrement (2 sec)...")
        show_recording()
        time.sleep(2)
        
        print("📍 Mode traitement (2 sec)...")
        show_processing()
        time.sleep(2)
        
        print("📍 Fermeture...")
        hide_popup()
        time.sleep(0.5)
        
        print("✅ Test fonctionnel réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_integration():
    """Test d'intégration avec main.py"""
    print("\n🔗 Test intégration main.py...")
    
    try:
        # Simuler l'import comme dans main.py
        try:
            from src.recording_popup import show_recording, show_processing, hide_popup
            RECORDING_POPUP_AVAILABLE = True
            print("✅ Import dans main.py simulé avec succès")
        except ImportError:
            RECORDING_POPUP_AVAILABLE = False
            print("❌ Import dans main.py échouerait")
            return False
        
        # Test de la logique de configuration
        config_path = Path("projects/voice-to-text-turbo/config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            ui_config = config.get("ui", {})
            popup_enabled = ui_config.get("show_recording_popup", True)
            
            if RECORDING_POPUP_AVAILABLE and popup_enabled:
                print("✅ Pop-up sera utilisée dans l'application")
                return True
            else:
                print("⚠️  Notifications Windows seront utilisées")
                return False
        else:
            print("❌ Configuration non trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur intégration: {e}")
        return False


def main():
    """Test principal"""
    print("🚀 TEST FINAL - Pop-up d'Enregistrement VTT")
    print("=" * 60)
    
    # Tests
    config_ok = test_configuration()
    import_ok = test_import()
    tkinter_ok = test_tkinter()
    
    if not (config_ok and import_ok and tkinter_ok):
        print("\n❌ Tests préliminaires échoués")
        print("   Corrigez les erreurs avant de continuer")
        return False
    
    # Tests avancés
    popup_ok = test_popup_functionality()
    integration_ok = test_main_integration()
    
    # Résultats
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX:")
    print(f"   Configuration: {'✅' if config_ok else '❌'}")
    print(f"   Import module: {'✅' if import_ok else '❌'}")
    print(f"   Tkinter: {'✅' if tkinter_ok else '❌'}")
    print(f"   Fonctionnalité: {'✅' if popup_ok else '❌'}")
    print(f"   Intégration: {'✅' if integration_ok else '❌'}")
    
    all_ok = all([config_ok, import_ok, tkinter_ok, popup_ok, integration_ok])
    
    if all_ok:
        print("\n🎉 SUCCÈS ! La pop-up est prête à l'emploi")
        print("💡 Lancez VTT avec start.bat et testez Ctrl+Alt+7")
        print("📖 Consultez GUIDE_POPUP_ENREGISTREMENT.md pour plus d'infos")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 Corrigez les erreurs ci-dessus")
        print("📖 Consultez GUIDE_POPUP_ENREGISTREMENT.md pour le dépannage")
    
    return all_ok


if __name__ == "__main__":
    success = main()
    input(f"\nAppuyez sur Entrée pour quitter... ({'✅' if success else '❌'})")