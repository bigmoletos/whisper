#!/usr/bin/env python3
"""
Test de la nouvelle pop-up thread-safe
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_popup_threadsafe():
    """Test de la pop-up thread-safe"""
    print("🧪 Test pop-up thread-safe...")
    
    try:
        from src.recording_popup import show_recording, show_processing, hide_popup
        
        print("📍 1. Affichage pop-up enregistrement (3 sec)")
        print("   ➤ Cherchez une fenêtre '🎤 VTT Enregistrement' en haut à droite")
        show_recording()
        time.sleep(3)
        
        print("📍 2. Mode traitement (2 sec)")
        print("   ➤ La fenêtre devrait changer en '⚡ TRANSCRIPTION'")
        show_processing()
        time.sleep(2)
        
        print("📍 3. Fermeture")
        hide_popup()
        time.sleep(1)
        
        print("✅ Test réussi ! Pop-up thread-safe fonctionne.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_popup_threadsafe()
    
    if success:
        print("\n🎉 La nouvelle pop-up thread-safe fonctionne !")
        print("💡 Relancez maintenant l'application VTT")
    else:
        print("\n❌ Problème avec la pop-up thread-safe")
    
    input("\nAppuyez sur Entrée pour quitter...")