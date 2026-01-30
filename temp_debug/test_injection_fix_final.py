#!/usr/bin/env python3
"""
Test final pour vérifier la correction du problème d'injection de texte
Ce script teste spécifiquement le problème où l'injection fonctionne la première fois
mais échoue aux tentatives suivantes.
"""

import sys
import time
from pathlib import Path

# Ajouter le chemin vers les modules partagés
script_dir = Path(__file__).parent.parent
shared_dir = script_dir / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

from src.text_injector import TextInjector

def test_multiple_injections():
    """Test d'injections multiples pour reproduire et vérifier la correction du bug"""
    
    print("🧪 TEST INJECTION MULTIPLE - Vérification de la correction")
    print("=" * 60)
    print("Ce test reproduit le problème où l'injection fonctionne")
    print("la première fois mais échoue aux tentatives suivantes.")
    print("=" * 60)
    
    # Créer l'injecteur
    injector = TextInjector(use_clipboard=True)
    
    # Textes de test
    test_texts = [
        "Premier test d'injection - ceci devrait fonctionner",
        "Deuxième test - c'est ici que le problème apparaissait",
        "Troisième test - vérification de la stabilité",
        "Quatrième test - test de robustesse continue"
    ]
    
    print(f"📝 Préparation de {len(test_texts)} tests d'injection...")
    print("⚠️  IMPORTANT: Placez votre curseur dans un champ de texte (ex: Notepad)")
    print("⏰ Vous avez 5 secondes pour positionner votre curseur...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🚀 Début des tests d'injection...")
    
    results = []
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📍 TEST {i}/{len(test_texts)}")
        print(f"   Texte: '{text[:30]}...'")
        
        # SOLUTION APPLIQUÉE: Réinitialiser l'état avant chaque injection
        print("   🔄 Réinitialisation de l'état de l'injecteur...")
        injector.reset_state()
        
        # Attendre un peu entre les injections
        if i > 1:
            print("   ⏳ Délai de sécurité...")
            time.sleep(2)
        
        print("   💉 Injection en cours...")
        start_time = time.time()
        
        # Utiliser la méthode robuste
        success = injector.inject_text_robust(text)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if success:
            print(f"   ✅ SUCCÈS (durée: {duration:.2f}s)")
            results.append(True)
        else:
            print(f"   ❌ ÉCHEC (durée: {duration:.2f}s)")
            results.append(False)
        
        # Attendre un peu pour voir le résultat
        time.sleep(1)
    
    # Résultats finaux
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX")
    print("=" * 60)
    
    success_count = sum(results)
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    for i, (text, success) in enumerate(zip(test_texts, results), 1):
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"Test {i}: {status} - '{text[:40]}...'")
    
    print(f"\n📈 Taux de réussite: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎉 PARFAIT! Tous les tests ont réussi!")
        print("✅ Le problème d'injection multiple semble résolu!")
    elif success_rate >= 75:
        print("👍 BIEN! La plupart des tests ont réussi.")
        print("⚠️  Il peut y avoir encore quelques problèmes mineurs.")
    else:
        print("⚠️  PROBLÈME! Plusieurs tests ont échoué.")
        print("🔧 Des améliorations supplémentaires sont nécessaires.")
    
    return success_rate

def test_rapid_injections():
    """Test d'injections rapides pour vérifier la robustesse"""
    
    print("\n🏃 TEST INJECTIONS RAPIDES")
    print("=" * 40)
    
    injector = TextInjector(use_clipboard=True)
    
    rapid_texts = [
        "Rapide 1",
        "Rapide 2", 
        "Rapide 3"
    ]
    
    print("⚠️  Test d'injections rapides (délai réduit)")
    print("⏰ 3 secondes pour positionner votre curseur...")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    results = []
    
    for i, text in enumerate(rapid_texts, 1):
        print(f"\n⚡ Test rapide {i}: '{text}'")
        
        # Réinitialisation
        injector.reset_state()
        
        # Délai très court
        if i > 1:
            time.sleep(0.5)
        
        success = injector.inject_text_robust(text)
        results.append(success)
        
        status = "✅" if success else "❌"
        print(f"   {status} Résultat: {'SUCCÈS' if success else 'ÉCHEC'}")
    
    rapid_success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 Taux de réussite rapide: {sum(results)}/{len(results)} ({rapid_success_rate:.1f}%)")
    
    return rapid_success_rate

if __name__ == "__main__":
    try:
        print("🎯 TEST COMPLET DE CORRECTION D'INJECTION")
        print("=" * 60)
        
        # Test principal
        main_success_rate = test_multiple_injections()
        
        # Test rapide
        rapid_success_rate = test_rapid_injections()
        
        # Résumé final
        print("\n" + "=" * 60)
        print("🏁 RÉSUMÉ FINAL")
        print("=" * 60)
        print(f"📊 Injections normales: {main_success_rate:.1f}% de réussite")
        print(f"⚡ Injections rapides: {rapid_success_rate:.1f}% de réussite")
        
        overall_success = (main_success_rate + rapid_success_rate) / 2
        print(f"🎯 Score global: {overall_success:.1f}%")
        
        if overall_success >= 90:
            print("\n🎉 EXCELLENT! La correction fonctionne parfaitement!")
        elif overall_success >= 75:
            print("\n👍 BIEN! La correction améliore significativement la situation.")
        else:
            print("\n⚠️  Des améliorations supplémentaires sont nécessaires.")
        
        print("\n💡 Si vous voyez encore des problèmes:")
        print("   1. Vérifiez que vous êtes dans un champ de texte éditable")
        print("   2. Essayez avec différentes applications (Notepad, Word, etc.)")
        print("   3. Vérifiez les logs pour plus de détails")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n📝 Test terminé. Appuyez sur Entrée pour quitter...")
    input()