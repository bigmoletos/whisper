#!/usr/bin/env python3
"""
Test de la popup avec utilisations multiples
Reproduit le problème du deuxième test
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_popup_multiple_uses():
    """Test de la popup avec plusieurs utilisations consécutives"""
    print("🔄 Test popup - utilisations multiples...")
    
    try:
        from src.recording_popup import show_recording, show_processing, hide_popup, cleanup_popup
        
        # Test 1
        print("\n📍 TEST 1 - Premier cycle")
        print("   ➤ Affichage enregistrement...")
        show_recording()
        time.sleep(2)
        
        print("   ➤ Mode traitement...")
        show_processing()
        time.sleep(1)
        
        print("   ➤ Fermeture...")
        hide_popup()
        time.sleep(1)
        
        print("✅ Test 1 terminé")
        
        # Test 2 - Simulation du problème
        print("\n📍 TEST 2 - Deuxième cycle (reproduction du problème)")
        print("   ➤ Affichage enregistrement...")
        show_recording()
        time.sleep(2)
        
        print("   ➤ Mode traitement...")
        show_processing()
        time.sleep(1)
        
        print("   ➤ Fermeture...")
        hide_popup()
        time.sleep(1)
        
        print("✅ Test 2 terminé")
        
        # Test 3 - Avec nettoyage explicite
        print("\n📍 TEST 3 - Avec nettoyage explicite")
        print("   ➤ Nettoyage complet...")
        cleanup_popup()
        time.sleep(0.5)
        
        print("   ➤ Affichage enregistrement...")
        show_recording()
        time.sleep(2)
        
        print("   ➤ Mode traitement...")
        show_processing()
        time.sleep(1)
        
        print("   ➤ Fermeture...")
        hide_popup()
        time.sleep(1)
        
        print("✅ Test 3 terminé")
        
        # Nettoyage final
        cleanup_popup()
        
        print("\n🎉 Tous les tests terminés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_popup_stress():
    """Test de stress - cycles rapides"""
    print("\n⚡ Test de stress - cycles rapides...")
    
    try:
        from src.recording_popup import show_recording, show_processing, hide_popup, cleanup_popup
        
        for i in range(5):
            print(f"   Cycle {i+1}/5...")
            show_recording()
            time.sleep(0.5)
            show_processing()
            time.sleep(0.5)
            hide_popup()
            time.sleep(0.2)
        
        cleanup_popup()
        print("✅ Test de stress réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur stress test: {e}")
        return False


def main():
    """Test principal"""
    print("🚀 TEST POPUP - Utilisations Multiples")
    print("=" * 60)
    print("Ce test reproduit le problème du deuxième enregistrement")
    print("et vérifie que la correction fonctionne.")
    print("=" * 60)
    
    # Test principal
    multiple_ok = test_popup_multiple_uses()
    
    # Test de stress
    stress_ok = test_popup_stress()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"   Utilisations multiples: {'✅' if multiple_ok else '❌'}")
    print(f"   Test de stress: {'✅' if stress_ok else '❌'}")
    
    if multiple_ok and stress_ok:
        print("\n🎉 SUCCÈS ! La popup fonctionne correctement")
        print("💡 Le problème du deuxième enregistrement devrait être résolu")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS")
        print("🔧 La popup nécessite encore des corrections")
    
    return multiple_ok and stress_ok


if __name__ == "__main__":
    success = main()
    input(f"\nAppuyez sur Entrée pour quitter... ({'✅' if success else '❌'})")