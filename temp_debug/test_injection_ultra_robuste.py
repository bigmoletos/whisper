#!/usr/bin/env python3
"""
Test de l'injection ultra-robuste
Vérification que le texte apparaît VRAIMENT
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_injection_ultra_robuste():
    """Test de l'injection ultra-robuste avec vérification visuelle"""
    print("🚀 Test injection ULTRA-ROBUSTE")
    print("=" * 60)
    
    try:
        from src.text_injector import TextInjector
        
        injector = TextInjector(use_clipboard=True)
        
        # Textes de test de complexité croissante
        test_texts = [
            "Test simple",
            "Test avec accents : éàùç",
            "Test plus long avec ponctuation : Bonjour, comment allez-vous ?",
            "Test technique : Python, JavaScript, API REST, JSON, XML",
            "Test complet : Non, je ne veux pas de solution temporaire. Appliquer quelque chose de robuste."
        ]
        
        print("📝 INSTRUCTIONS IMPORTANTES :")
        print("1. Ouvrez Notepad (ou un éditeur de texte)")
        print("2. Cliquez dans le champ de texte")
        print("3. NE CHANGEZ PAS DE FENÊTRE pendant les tests")
        print("4. Observez si le texte apparaît VRAIMENT")
        print()
        
        input("Appuyez sur Entrée quand Notepad est ouvert et actif...")
        
        results = []
        
        for i, test_text in enumerate(test_texts, 1):
            print(f"\n🔧 TEST {i}/5: '{test_text[:30]}...'")
            print("   ➤ Injection en cours...")
            
            # Utiliser la méthode ultra-robuste
            success = injector.inject_text_robust(test_text)
            
            print(f"   ➤ Résultat technique: {'✅' if success else '❌'}")
            
            # Demander confirmation visuelle à l'utilisateur
            user_confirm = input("   ➤ Le texte est-il VRAIMENT apparu dans Notepad ? (o/n): ").lower().strip()
            visual_success = user_confirm in ['o', 'oui', 'y', 'yes']
            
            results.append({
                'text': test_text,
                'technical': success,
                'visual': visual_success,
                'match': success == visual_success
            })
            
            print(f"   ➤ Confirmation visuelle: {'✅' if visual_success else '❌'}")
            print(f"   ➤ Cohérence: {'✅' if success == visual_success else '❌ PROBLÈME!'}")
            
            if i < len(test_texts):
                print("   ➤ Nettoyage pour le test suivant...")
                time.sleep(1)
        
        # Résultats finaux
        print("\n" + "=" * 60)
        print("📊 RÉSULTATS DÉTAILLÉS:")
        
        technical_success = sum(1 for r in results if r['technical'])
        visual_success = sum(1 for r in results if r['visual'])
        coherent = sum(1 for r in results if r['match'])
        
        for i, result in enumerate(results, 1):
            status = "✅" if result['match'] and result['visual'] else "❌"
            print(f"   Test {i}: {status} - Technique: {result['technical']}, Visuel: {result['visual']}")
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   Succès technique: {technical_success}/{len(test_texts)}")
        print(f"   Succès visuel: {visual_success}/{len(test_texts)}")
        print(f"   Cohérence: {coherent}/{len(test_texts)}")
        
        # Diagnostic
        if visual_success == len(test_texts):
            print("\n🎉 PARFAIT ! L'injection fonctionne vraiment")
            return True
        elif visual_success > 0:
            print(f"\n⚠️  PARTIEL - {visual_success}/{len(test_texts)} injections réussies")
            print("💡 Certaines méthodes fonctionnent, à optimiser")
            return False
        else:
            print("\n❌ ÉCHEC COMPLET - Aucune injection visible")
            print("🔧 Problème fondamental à résoudre")
            return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_focus_detection():
    """Test de détection de focus"""
    print("\n🎯 Test de détection de focus...")
    
    try:
        from src.text_injector import TextInjector
        
        injector = TextInjector()
        window_info = injector.get_active_window_info()
        
        print(f"📍 Fenêtre active détectée: {window_info}")
        
        if 'title' in window_info and window_info['title']:
            print(f"✅ Titre: {window_info['title']}")
            return True
        else:
            print("❌ Impossible de détecter la fenêtre active")
            return False
        
    except Exception as e:
        print(f"❌ Erreur détection focus: {e}")
        return False


def main():
    """Test principal"""
    print("🚀 TEST INJECTION ULTRA-ROBUSTE")
    print("Ce test vérifie que l'injection fonctionne VRAIMENT")
    print("avec confirmation visuelle de l'utilisateur.")
    print("=" * 60)
    
    # Test de focus
    focus_ok = test_focus_detection()
    
    if not focus_ok:
        print("\n⚠️  Problème de détection de focus, mais on continue...")
    
    # Test principal
    injection_ok = test_injection_ultra_robuste()
    
    print("\n" + "=" * 60)
    print("🏁 CONCLUSION:")
    
    if injection_ok:
        print("✅ L'injection ultra-robuste FONCTIONNE")
        print("💡 Le système VTT devrait maintenant fonctionner correctement")
    else:
        print("❌ L'injection ultra-robuste NE FONCTIONNE PAS")
        print("🔧 Il faut investiguer plus profondément le problème")
    
    print("\n💡 CONSEILS:")
    print("- Si ça marche ici mais pas dans VTT, c'est un problème de timing")
    print("- Si ça ne marche nulle part, c'est un problème de permissions")
    print("- Testez avec différentes applications (Notepad, Word, etc.)")
    
    return injection_ok


if __name__ == "__main__":
    success = main()
    input(f"\nAppuyez sur Entrée pour quitter... ({'✅' if success else '❌'})")