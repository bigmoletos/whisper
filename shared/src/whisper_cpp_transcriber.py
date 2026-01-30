#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de transcription utilisant Whisper.cpp pour des performances optimales
"""

import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

# Configuration du logging
logger = logging.getLogger(__name__)

try:
    import whispercpp as wcpp
    WHISPER_CPP_AVAILABLE = True
except ImportError:
    WHISPER_CPP_AVAILABLE = False
    # Module optionnel - pas d'avertissement si non disponible

class WhisperCppTranscriber:
    """Transcription utilisant Whisper.cpp pour des performances optimales"""
    
    def __init__(
        self,
        model_name: str = "medium",
        language: str = "fr",
        device: str = "cpu",
        compute_type: str = "int8",
        download_root: Optional[str] = None
    ):
        """
        Initialise le transcripteur Whisper.cpp
        
        Args:
            model_name: Nom du modèle (tiny, base, small, medium, large)
            language: Code langue ISO (fr, en, es, etc.)
            device: Périphérique (cpu ou cuda)
            compute_type: Type de calcul (int8, float16, etc.)
            download_root: Répertoire pour télécharger les modèles
        """
        self.model_name = model_name
        self.language = language
        self.device = device
        self.compute_type = compute_type
        self.download_root = download_root
        self.model: Optional[wcpp.Whisper] = None
        
        logger.info(f"Initialisation Whisper.cpp: {model_name} (langue: {language}, device: {device}, compute: {compute_type})")
    
    def load_model(self) -> None:
        """Charge le modèle Whisper.cpp"""
        if not WHISPER_CPP_AVAILABLE:
            raise RuntimeError("whispercpp n'est pas installé. Veuillez installer whisper-cpp-python")
        
        if self.model is not None:
            logger.info("Modèle déjà chargé")
            return
        
        try:
            logger.info(f"Chargement du modèle Whisper.cpp '{self.model_name}'...")
            start_time = time.time()
            
            # Configurer les paramètres
            params = wcpp.WhisperParams()
            params.language = self.language
            
            if self.compute_type == "int8":
                params.quantize = True
            
            # Charger le modèle
            self.model = wcpp.Whisper(params)
            
            # Charger le modèle spécifique
            model_path = self._get_model_path()
            if not self.model.load_model(model_path):
                raise RuntimeError(f"Échec du chargement du modèle: {model_path}")
            
            end_time = time.time()
            logger.info(f"Modèle '{self.model_name}' chargé en {end_time - start_time:.2f} secondes")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle Whisper.cpp: {e}")
            raise
    
    def _get_model_path(self) -> str:
        """Retourne le chemin vers le fichier de modèle"""
        # Chemin par défaut pour les modèles ggml
        model_mapping = {
            "tiny": "ggml-tiny.bin",
            "base": "ggml-base.bin",
            "small": "ggml-small.bin",
            "medium": "ggml-medium.bin",
            "large": "ggml-large-v3.bin"
        }
        
        model_file = model_mapping.get(self.model_name, f"ggml-{self.model_name}.bin")
        
        # Vérifier si le modèle existe dans le cache
        cache_dir = os.path.join(
            os.path.expanduser("~"), ".cache", "whisper.cpp", "models"
        )
        
        if self.download_root:
            model_path = os.path.join(self.download_root, model_file)
        else:
            model_path = os.path.join(cache_dir, model_file)
        
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        return model_path
    
    def transcribe(self, audio_data: bytes, sample_rate: int) -> str:
        """
        Transcrit l'audio en texte
        
        Args:
            audio_data: Données audio brutes
            sample_rate: Fréquence d'échantillonnage
        
        Returns:
            Texte transcrit
        """
        if self.model is None:
            self.load_model()
        
        if not self.model:
            raise RuntimeError("Modèle non chargé")
        
        try:
            logger.info("Transcription avec Whisper.cpp...")
            start_time = time.time()
            
            # Convertir les données audio au format attendu
            # Whisper.cpp attend des float32 dans [-1.0, 1.0]
            import numpy as np
            import soundfile as sf
            from io import BytesIO
            
            # Charger l'audio
            audio_array, sr = sf.read(BytesIO(audio_data))
            
            # Convertir en mono si nécessaire
            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)
            
            # Normaliser
            audio_array = audio_array.astype(np.float32) / 32768.0
            
            # Transcrire
            self.model.full_params.n_threads = 4  # Utiliser 4 threads
            self.model.full_params.translate = False
            self.model.full_params.language = self.language
            
            if not self.model.full(audio_array, sample_rate):
                raise RuntimeError("Échec de la transcription")
            
            # Récupérer le nombre de segments
            n_segments = self.model.full_n_segments()
            
            # Construire le texte
            text_parts = []
            for i in range(n_segments):
                segment_text = self.model.full_get_segment_text(i)
                text_parts.append(segment_text)
            
            full_text = " ".join(text_parts)
            
            end_time = time.time()
            logger.info(f"Transcription terminée en {end_time - start_time:.2f} secondes")
            
            return full_text.strip()
            
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}")
            raise
    
    def __del__(self):
        """Nettoyage"""
        if hasattr(self, 'model') and self.model:
            del self.model

# Test si le module est disponible
if __name__ == "__main__":
    print("Test du module Whisper.cpp")
    
    if WHISPER_CPP_AVAILABLE:
        print("✓ whispercpp est disponible")
        
        try:
            transcriber = WhisperCppTranscriber(model_name="medium", language="fr")
            print("✓ Module WhisperCppTranscriber créé avec succès")
        except Exception as e:
            print(f"✗ Erreur lors de la création: {e}")
    else:
        print("✗ whispercpp n'est pas disponible")
        print("Installez avec: pip install whisper-cpp-python")