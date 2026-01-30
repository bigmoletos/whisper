#!/usr/bin/env python3
"""
Test de la nouvelle pop-up simplifiée
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

def test_popup_simple():
    """Test de la pop-up simplifiée"""
    print("🧪 Test pop-up simplifiée...")
    
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
        
        print("✅ Test réussi ! Pop-up simplifiée fonctionne.")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_popup_simple()
    
    if success:
        print("\n🎉 La nouvelle pop-up fonctionne !")
        print("💡 Relancez maintenant l'application VTT")
    else:
        print("\n❌ Problème avec la pop-up")
    
    input("\nAppuyez sur Entrée pour quitter...")