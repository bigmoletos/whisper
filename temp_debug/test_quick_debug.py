#!/usr/bin/env python3
"""
Test rapide pour diagnostiquer le problème d'injection de texte
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_text_injection_only():
    """Test uniquement l'injection de texte"""
    print("📝 Test injection de texte simple...")
    
    try:
        from src.text_injector import TextInjector
        
        injector = TextInjector(use_clipboard=True)
        test_text = "Test VTT - injection de texte"
        
        print(f"📍 Test avec: '{test_text}'")
        print("💡 Ouvrez un éditeur de texte (Notepad, Word, etc.) et cliquez dedans")
        input("Appuyez sur Entrée quand vous êtes prêt...")
        
        success = injector.inject_text(test_text)
        
        if success:
            print("✅ Injection réussie - vérifiez l'éditeur de texte")
        else:
            print("❌ Injection échouée")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_log_file():
    """Vérifier le fichier de log"""
    print("\n📋 Vérification du fichier de log...")
    
    log_file = Path("voice_transcriber_turbo.log")
    
    if log_file.exists():
        print(f"✅ Fichier de log trouvé: {log_file}")
        
        # Lire les dernières lignes
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines:
                print(f"📍 Dernières lignes du log ({len(lines)} lignes total):")
                for line in lines[-10:]:  # 10 dernières lignes
                    print(f"   {line.strip()}")
            else:
                print("⚠️  Fichier de log vide")
                
        except Exception as e:
            print(f"❌ Erreur lecture log: {e}")
    else:
        print("⚠️  Fichier de log non trouvé")
        print("   Cela peut indiquer que l'application ne démarre pas correctement")


def main():
    """Test principal"""
    print("🔍 DIAGNOSTIC RAPIDE - Problème d'injection de texte")
    print("=" * 60)
    
    # Test d'injection simple
    injection_ok = test_text_injection_only()
    
    # Vérifier les logs
    check_log_file()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC:")
    
    if injection_ok:
        print("✅ L'injection de texte fonctionne")
        print("💡 Le problème est probablement dans la transcription ou la capture audio")
        print("🔧 Lancez debug_text_injection.py pour un diagnostic complet")
    else:
        print("❌ L'injection de texte ne fonctionne pas")
        print("🔧 Vérifiez les permissions et les modules installés")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Si injection OK: Lancez debug_text_injection.py")
    print("2. Si injection KO: Vérifiez les dépendances (pyautogui, pyperclip)")
    print("3. Consultez le fichier de log pour plus de détails")


if __name__ == "__main__":
    main()
    input("\nAppuyez sur Entrée pour quitter...")