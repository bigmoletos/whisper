"""
Module de transcription audio utilisant Faster-Whisper
Version optimisée et plus rapide de Whisper
"""

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_IMPORTED = True
except ImportError:
    FASTER_WHISPER_IMPORTED = False
    WhisperModel = None  # Pour éviter les erreurs de référence

import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FasterWhisperTranscriber:
    """Wrapper autour de Faster-Whisper pour la transcription audio optimisée"""

    def __init__(
        self,
        model_name: str = "large-v3",
        language: str = "fr",
        device: str = "cpu",
        compute_type: str = "int8"
    ):
        """
        Initialise le transcribeur Faster-Whisper

        Args:
            model_name: Nom du modèle (large-v3, medium, small, base, tiny)
            language: Code langue ISO (fr, en, etc.)
            device: Device à utiliser (cpu, cuda)
            compute_type: Type de calcul (int8, int8_float16, float16, float32)
                         - int8 : Plus rapide, précision légèrement réduite
                         - float16 : Bon compromis
                         - float32 : Plus précis, plus lent
        """
        if not FASTER_WHISPER_IMPORTED:
            raise ImportError(
                "faster-whisper n'est pas installé. "
                "Installez avec: pip install faster-whisper "
                "(nécessite Rust: https://rustup.rs/)"
            )

        self.model_name = model_name
        self.language = language
        self.device = device
        self.compute_type = compute_type
        self.model: Optional[WhisperModel] = None

        logger.info(f"Initialisation Faster-Whisper: {model_name} (langue: {language}, device: {device}, compute: {compute_type})")

    def load_model(self) -> None:
        """Charge le modèle Faster-Whisper (téléchargement automatique si nécessaire)"""
        if self.model is not None:
            logger.info("Modèle déjà chargé")
            return

        try:
            logger.info(f"Chargement du modèle Faster-Whisper '{self.model_name}'...")
            logger.info("(Premier chargement: téléchargement automatique du modèle)")

            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type
            )

            logger.info(f"Modèle '{self.model_name}' chargé avec succès")

        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle Faster-Whisper: {e}", exc_info=True)
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

            # Transcrire avec Faster-Whisper
            # Faster-Whisper accepte directement les arrays numpy
            segments, info = self.model.transcribe(
                audio,
                language=self.language,
                beam_size=5,
                vad_filter=True,  # Filtre de détection de voix (améliore la précision)
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    threshold=0.5
                )
            )

            # Assembler le texte depuis les segments
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)

            text = " ".join(text_parts).strip()

            if text:
                logger.info(f"Transcription réussie: '{text[:50]}...' (longueur: {len(text)})")
                logger.debug(f"Langue détectée: {info.language}, probabilité: {info.language_probability:.2f}")
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
            segments, info = self.model.transcribe(
                audio_path,
                language=self.language,
                beam_size=5,
                vad_filter=True
            )

            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)

            text = " ".join(text_parts).strip()
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
            "compute_type": self.compute_type,
            "engine": "faster-whisper"
        }

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        self.model = None
