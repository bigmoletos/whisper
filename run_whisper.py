#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script pour lancer l'application Whisper avec un timeout
"""

import os
import sys
import subprocess
import threading
import time

def run_whisper_with_timeout(timeout_seconds=15):
    """
    Lance l'application Whisper avec un timeout
    """
    print(f"Lancement de l'application Whisper (timeout: {timeout_seconds} secondes)...")
    
    def run_application():
        """Fonction pour lancer l'application"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.main"
            ], capture_output=True, text=True)
            
            print(f"Code de retour: {result.returncode}")
            if result.stdout:
                print(f"Sortie standard:\n{result.stdout}")
            if result.stderr:
                print(f"Erreur standard:\n{result.stderr}")
                
        except Exception as e:
            print(f"Exception lors de l'exécution: {e}")
    
    # Lancer l'application dans un thread séparé
    app_thread = threading.Thread(target=run_application)
    app_thread.daemon = True
    app_thread.start()
    
    # Attendre le timeout ou la fin de l'application
    app_thread.join(timeout=timeout_seconds)
    
    if app_thread.is_alive():
        print(f"L'application est toujours en cours après {timeout_seconds} secondes...")
        print("Vous pouvez continuer à l'utiliser ou l'arrêter manuellement.")
        return True
    else:
        print("L'application s'est terminée.")
        return False

def main():
    """
    Fonction principale
    """
    print("Lancement de l'application Whisper STT")
    print("=" * 40)
    
    # Lancer avec un timeout de 20 secondes
    success = run_whisper_with_timeout(20)
    
    if success:
        print("\nL'application semble fonctionner correctement !")
        print("Vous pouvez maintenant utiliser Whisper pour la transcription vocale.")
    else:
        print("\nL'application ne semble pas démarrer correctement.")
        print("Vérifiez les erreurs ci-dessus pour plus de détails.")

if __name__ == "__main__":
    main()