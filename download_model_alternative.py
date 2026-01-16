#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script alternatif pour télécharger les modèles Whisper
"""

import os
import sys
import time
import subprocess

def download_whisper_model_standard():
    """
    Télécharge les modèles Whisper en utilisant le package whisper standard
    """
    print("Tentative de telechargement des modeles Whisper via le package standard...")
    
    try:
        # Essayer d'importer whisper et de télécharger le modèle
        import whisper
        
        print("Chargement du modele large-v3 via whisper standard...")
        start_time = time.time()
        
        # Cela devrait déclencher le téléchargement
        model = whisper.load_model("large-v3")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"[SUCCESS] Modele large-v3 telecharge via whisper standard !")
        print(f"   Temps ecoule: {duration:.2f} secondes")
        print(f"   Type de modele: {type(model)}")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur avec whisper standard: {e}")
        return False

def download_via_cli():
    """
    Essaye de télécharger via la ligne de commande
    """
    print("Tentative de telechargement via la ligne de commande...")
    
    try:
        # Essayer d'utiliser la commande whisper pour télécharger
        result = subprocess.run([
            sys.executable, "-m", "whisper", "--download", "large-v3"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("[SUCCESS] Telechargement via CLI reussi !")
            print(f"Sortie: {result.stdout}")
            return True
        else:
            print(f"[ERREUR] Telechargement via CLI echoue")
            print(f"Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERREUR] Erreur avec la commande CLI: {e}")
        return False

def main():
    """
    Fonction principale
    """
    print("Script alternatif de telechargement des modeles Whisper")
    print("=" * 50)
    
    # Essayer d'abord avec whisper standard
    success = download_whisper_model_standard()
    
    if not success:
        # Essayer via la ligne de commande
        success = download_via_cli()
    
    if success:
        print("\n[SUCCESS] Les modeles ont ete telecharges avec succes !")
        print("Vous pouvez maintenant utiliser Whisper pour la transcription vocale.")
    else:
        print("\n[AVERTISSEMENT] Impossible de telecharger les modeles automatiquement.")
        print("Les modeles seront telecharges lors de la premiere utilisation de l'application.")
        print("Assurez-vous d'avoir une connexion internet stable.")

if __name__ == "__main__":
    main()