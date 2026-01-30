#!/usr/bin/env python3
"""
Test rapide de la nouvelle pop-up d'enregistrement
Force le rechargement du module pour éviter les conflits de cache
"""

import sys
import time
import importlib
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

def test_nouvelle_popup():
    """Test de la nouvelle pop-up avec rechargement forcé"""
    print("🔄 Test de la nouvelle pop-up d'enregistrement VTT")
    print("=" * 60)
    
    try:
        # Forcer le rechargement du module
        if 'src.recording_popup' in sys.modules:
            importlib.reload(sys.modules['src.recording_popup'])
            print("🔄 Module rechargé depuis le cache")
        
        from src.recording_popup import show_recording, show_processing, hide_popup
        print("✅ Nouveau module pop-up importé")
        
        # Test séquence complète
        print("\n📍 Phase 1: Pop-up d'enregistrement (5 secondes)")
        print("   ➤ Recherchez une petite fenêtre noire en haut à droite")
        print("   ➤ Avec un point rouge clignotant et un compteur")
        show_recording()
        time.sleep(5)
        
        print("\n📍 Phase 2: Mode traitement (3 secondes)")
        print("   ➤ Le point rouge devient un éclair vert")
        print("   ➤ Texte change en 'Transcription...'")
        show_processing()
        time.sleep(3)
        
        print("\n📍 Phase 3: Fermeture")
        hide_popup()
        print("   ➤ Pop-up fermée")
        
        print("\n✅ Test réussi ! La nouvelle pop-up fonctionne.")
        print("💡 Si vous voyez encore l'ancienne notification,")
        print("   redémarrez complètement l'application VTT.")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que le fichier recording_popup.py existe")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        # S'assurer que la pop-up est fermée
        try:
            hide_popup()
        except:
            pass

if __name__ == "__main__":
    test_nouvelle_popup()
    input("\nAppuyez sur Entrée pour quitter...")