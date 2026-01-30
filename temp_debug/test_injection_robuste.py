#!/usr/bin/env python3
"""
Test de l'injection de texte robuste
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_injection_methods():
    """Test des différentes méthodes d'injection"""
    print("📝 Test des méthodes d'injection de texte...")
    
    try:
        from src.text_injector import TextInjector
        
        injector = TextInjector(use_clipboard=True)
        test_text = "Test d'injection VTT - méthode robuste"
        
        print(f"📍 Texte de test: '{test_text}'")
        print("💡 Ouvrez un éditeur de texte (Notepad, Word, etc.) et cliquez dedans")
        input("Appuyez sur Entrée quand vous êtes prêt pour le test...")
        
        # Test 1: Méthode standard
        print("\n🔧 Test 1: Méthode standard")
        success1 = injector.inject_text(test_text + " - Standard")
        print(f"   Résultat: {'✅' if success1 else '❌'}")
        
        time.sleep(2)
        
        # Test 2: Méthode robuste
        print("\n🔧 Test 2: Méthode robuste")
        success2 = injector.inject_text_robust(test_text + " - Robuste")
        print(f"   Résultat: {'✅' if success2 else '❌'}")
        
        time.sleep(2)
        
        # Test 3: Clear and inject
        print("\n🔧 Test 3: Clear and inject")
        success3 = injector.clear_and_inject(test_text + " - Clear&Inject")
        print(f"   Résultat: {'✅' if success3 else '❌'}")
        
        return success1 or success2 or success3
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_window_focus():
    """Test de focus de fenêtre"""
    print("\n🎯 Test de focus de fenêtre...")
    
    try:
        from src.text_injector import TextInjector
        
        injector = TextInjector()
        window_info = injector.get_active_window_info()
        
        print(f"📍 Fenêtre active: {window_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_clipboard_verification():
    """Test de vérification du presse-papiers"""
    print("\n📋 Test de vérification du presse-papiers...")
    
    try:
        import pyperclip
        
        test_text = "Test presse-papiers VTT"
        
        # Copier
        pyperclip.copy(test_text)
        time.sleep(0.1)
        
        # Vérifier
        clipboard_content = pyperclip.paste()
        
        if clipboard_content == test_text:
            print("✅ Presse-papiers fonctionne correctement")
            return True
        else:
            print(f"❌ Problème presse-papiers. Attendu: '{test_text}', Trouvé: '{clipboard_content}'")
            return False
        
    except Exception as e:
        print(f"❌ Erreur presse-papiers: {e}")
        return False


def main():
    """Test principal"""
    print("🚀 TEST INJECTION ROBUSTE")
    print("=" * 60)
    print("Ce test vérifie les différentes méthodes d'injection de texte")
    print("et identifie pourquoi le texte n'apparaît pas.")
    print("=" * 60)
    
    # Tests préliminaires
    clipboard_ok = test_clipboard_verification()
    focus_ok = test_window_focus()
    
    if not clipboard_ok:
        print("\n❌ Problème avec le presse-papiers - arrêt des tests")
        return False
    
    # Test principal d'injection
    injection_ok = test_injection_methods()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"   Presse-papiers: {'✅' if clipboard_ok else '❌'}")
    print(f"   Focus fenêtre: {'✅' if focus_ok else '❌'}")
    print(f"   Injection texte: {'✅' if injection_ok else '❌'}")
    
    if injection_ok:
        print("\n🎉 SUCCÈS ! L'injection de texte fonctionne")
        print("💡 Si le problème persiste dans VTT, c'est un problème de timing ou de focus")
    else:
        print("\n❌ PROBLÈME D'INJECTION IDENTIFIÉ")
        print("🔧 Vérifiez les permissions et les modules pyautogui/pyperclip")
    
    print("\n💡 CONSEILS:")
    print("- Assurez-vous que l'éditeur de texte a le focus")
    print("- Testez avec différentes applications (Notepad, Word, etc.)")
    print("- Vérifiez les permissions d'accessibilité Windows")
    
    return injection_ok


if __name__ == "__main__":
    success = main()
    input(f"\nAppuyez sur Entrée pour quitter... ({'✅' if success else '❌'})")