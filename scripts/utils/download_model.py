#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script pour télécharger les modèles Whisper nécessaires
"""

import os
import sys
import time
from faster_whisper import WhisperModel

def download_whisper_model(model_name="large-v3", device="cpu", compute_type="int8"):
    """
    Télécharge un modèle Whisper en utilisant Faster-Whisper
    """
    print(f"Debut du telechargement du modele {model_name}...")
    print(f"Configuration: device={device}, compute_type={compute_type}")
    print("Ceci peut prendre plusieurs minutes selon votre connexion internet...")
    
    start_time = time.time()
    
    try:
        # Essayer de charger le modèle - cela devrait déclencher le téléchargement
        print(f"Chargement du modele {model_name}...")
        model = WhisperModel(model_name, device=device, compute_type=compute_type)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"[SUCCESS] Modele {model_name} telecharge et charge avec succes !")
        print(f"   Temps ecoule: {duration:.2f} secondes")
        print(f"   Type de modele: {type(model)}")
        
        return model
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors du telechargement du modele {model_name}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """
    Fonction principale
    """
    print("Script de telechargement des modeles Whisper")
    print("=" * 50)
    
    # Télécharger le modèle principal
    model = download_whisper_model("large-v3")
    
    if model:
        print("\n[SUCCESS] Tous les modeles ont ete telecharges avec succes !")
        print("Vous pouvez maintenant utiliser Whisper pour la transcription vocale.")
    else:
        print("\n[AVERTISSEMENT] Certains modeles n'ont pas pu etre telecharges.")
        print("Ils seront telecharges automatiquement lors de la premiere utilisation.")

if __name__ == "__main__":
    main()