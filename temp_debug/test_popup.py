#!/usr/bin/env python3
"""
Test de la pop-up d'enregistrement VTT
Script de démonstration pour tester la pop-up
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

try:
    from src.recording_popup import show_recording, show_processing, hide_popup
    print("✅ Module pop-up importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Vérifiez que tkinter est installé: pip install tk")
    sys.exit(1)

def test_popup_sequence():
    """Test complet de la séquence pop-up"""
    print("\n🎬 Test de la pop-up d'enregistrement VTT")
    print("=" * 50)
    
    try:
        # Phase 1: Enregistrement
        print("📍 Phase 1: Affichage pop-up d'enregistrement...")
        show_recording()
        print("   ➤ Pop-up d'enregistrement affichée (5 secondes)")
        time.sleep(5)
        
        # Phase 2: Traitement
        print("📍 Phase 2: Changement en mode traitement...")
        show_processing()
        print("   ➤ Pop-up en mode traitement (3 secondes)")
        time.sleep(3)
        
        # Phase 3: Fermeture
        print("📍 Phase 3: Fermeture de la pop-up...")
        hide_popup()
        print("   ➤ Pop-up fermée")
        
        print("\n✅ Test terminé avec succès !")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")
        # S'assurer que la pop-up est fermée en cas d'erreur
        try:
            hide_popup()
        except:
            pass

def test_popup_manual():
    """Test manuel interactif"""
    print("\n🎮 Test manuel de la pop-up")
    print("=" * 50)
    
    try:
        input("Appuyez sur Entrée pour afficher la pop-up d'enregistrement...")
        show_recording()
        
        input("Appuyez sur Entrée pour passer en mode traitement...")
        show_processing()
        
        input("Appuyez sur Entrée pour fermer la pop-up...")
        hide_popup()
        
        print("✅ Test manuel terminé !")
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrompu par l'utilisateur")
        hide_popup()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        hide_popup()

if __name__ == "__main__":
    print("🔧 Test de la pop-up d'enregistrement VTT")
    print("Choisissez le type de test:")
    print("1. Test automatique (séquence complète)")
    print("2. Test manuel (interactif)")
    print("3. Quitter")
    
    try:
        choice = input("\nVotre choix (1-3): ").strip()
        
        if choice == "1":
            test_popup_sequence()
        elif choice == "2":
            test_popup_manual()
        elif choice == "3":
            print("Au revoir !")
        else:
            print("❌ Choix invalide")
            
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")