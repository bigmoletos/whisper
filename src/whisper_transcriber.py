"""
Module de transcription audio utilisant Whisper
"""

import whisper
import numpy as np
import logging
from typing import Optional
import torch

logger = logging.getLogger(__name__)


class WhisperTranscriber:
    """Wrapper autour de Whisper pour la transcription audio"""

    def __init__(self, model_name: str = "medium", language: str = "fr", device: str = "cpu"):
        """
        Initialise le transcribeur Whisper

        Args:
            model_name: Nom du modèle Whisper (tiny, base, small, medium, large)
            language: Code langue ISO (fr, en, etc.)
            device: Device à utiliser (cpu, cuda)
        """
        self.model_name = model_name
        self.language = language
        self.device = device
        self.model: Optional[whisper.Whisper] = None

        # Vérifier la disponibilité de CUDA
        if device == "cuda" and torch.cuda.is_available():
            self.device = "cuda"
            logger.info(f"CUDA disponible, utilisation du GPU")
        else:
            self.device = "cpu"
            if device == "cuda":
                logger.warning("CUDA demandé mais non disponible, utilisation du CPU")

        logger.info(f"Initialisation du modèle Whisper: {model_name} (langue: {language}, device: {device})")

    def load_model(self) -> None:
        """Charge le modèle Whisper (téléchargement automatique si nécessaire)"""
        if self.model is not None:
            logger.info("Modèle déjà chargé")
            return

        try:
            logger.info(f"Chargement du modèle Whisper '{self.model_name}'...")
            logger.info("(Premier chargement: téléchargement automatique du modèle)")

            self.model = whisper.load_model(self.model_name, device=self.device)

            logger.info(f"Modèle '{self.model_name}' chargé avec succès")

            # Afficher les informations du modèle
            if hasattr(self.model, 'dims'):
                logger.debug(f"Dimensions du modèle: {self.model.dims}")

        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle Whisper: {e}")
            raise

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """
        Transcrit l'audio en texte

        Args:
            audio: Array numpy contenant les données audio
            sample_rate: Fréquence d'échantillonnage de l'audio

        Returns:
            Texte transcrit
        """
        if self.model is None:
            logger.error("Modèle non chargé, chargement en cours...")
            self.load_model()

        if len(audio) == 0:
            logger.warning("Audio vide, retour d'une chaîne vide")
            return ""

        try:
            # Normaliser l'audio si nécessaire
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)

            # S'assurer que l'audio est dans la plage [-1, 1]
            if np.abs(audio).max() > 1.0:
                audio = audio / np.abs(audio).max()

            logger.info(f"Transcription de {len(audio) / sample_rate:.2f} secondes d'audio...")

            # Transcrire avec Whisper
            result = self.model.transcribe(
                audio,
                language=self.language,
                task="transcribe",
                fp16=False if self.device == "cpu" else True
            )

            text = result["text"].strip()

            if text:
                logger.info(f"Transcription réussie: '{text[:50]}...' (longueur: {len(text)})")
            else:
                logger.warning("Transcription vide (aucun texte détecté)")

            return text

        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}", exc_info=True)
            return ""

    def transcribe_file(self, audio_path: str) -> str:
        """
        Transcrit un fichier audio

        Args:
            audio_path: Chemin vers le fichier audio

        Returns:
            Texte transcrit
        """
        if self.model is None:
            self.load_model()

        try:
            logger.info(f"Transcription du fichier: {audio_path}")
            result = self.model.transcribe(
                audio_path,
                language=self.language,
                task="transcribe"
            )

            text = result["text"].strip()
            logger.info(f"Transcription réussie: '{text[:50]}...'")
            return text

        except Exception as e:
            logger.error(f"Erreur lors de la transcription du fichier: {e}", exc_info=True)
            return ""

    def get_model_info(self) -> dict:
        """
        Retourne les informations sur le modèle chargé

        Returns:
            Dictionnaire avec les informations du modèle
        """
        if self.model is None:
            return {"loaded": False}

        return {
            "loaded": True,
            "model_name": self.model_name,
            "language": self.language,
            "device": self.device,
            "is_multilingual": hasattr(self.model, 'is_multilingual') and self.model.is_multilingual
        }

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        # Le modèle Whisper se libère automatiquement
        self.model = None
