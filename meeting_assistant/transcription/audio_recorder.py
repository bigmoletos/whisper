"""
Enregistreur audio pour sauvegarde complète de la session
Permet le post-processing avec pyannote pour une diarisation précise
"""

import logging
import threading
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional, List, Tuple
import time

logger = logging.getLogger(__name__)


class AudioRecorder:
    """
    Enregistre l'audio complet de la session pour post-processing
    """

    def __init__(
        self,
        session_dir: Path,
        session_id: str,
        sample_rate: int = 16000,
        channels: int = 1
    ):
        """
        Initialise l'enregistreur

        Args:
            session_dir: Répertoire de session
            session_id: ID de session
            sample_rate: Fréquence d'échantillonnage
            channels: Nombre de canaux
        """
        self.session_dir = Path(session_dir)
        self.session_id = session_id
        self.sample_rate = sample_rate
        self.channels = channels

        # Fichier de sortie
        self.audio_dir = self.session_dir / session_id / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.audio_file = self.audio_dir / "full_session.wav"

        # Buffer en mémoire
        self._audio_chunks: List[np.ndarray] = []
        self._lock = threading.Lock()
        self._total_samples = 0
        self._is_recording = False

        logger.info(f"AudioRecorder initialisé: {self.audio_file}")

    def start(self) -> None:
        """Démarre l'enregistrement"""
        self._is_recording = True
        self._audio_chunks = []
        self._total_samples = 0
        logger.info("Enregistrement audio démarré")

    def stop(self) -> Optional[Path]:
        """
        Arrête l'enregistrement et sauvegarde le fichier

        Returns:
            Chemin du fichier audio ou None si erreur
        """
        self._is_recording = False

        with self._lock:
            if not self._audio_chunks:
                logger.warning("Aucun audio enregistré")
                return None

            try:
                # Concaténer tous les chunks
                full_audio = np.concatenate(self._audio_chunks)

                # Sauvegarder en WAV
                sf.write(
                    self.audio_file,
                    full_audio,
                    self.sample_rate,
                    subtype='PCM_16'
                )

                duration = len(full_audio) / self.sample_rate
                logger.info(
                    f"Audio sauvegardé: {self.audio_file} "
                    f"({duration:.1f}s, {len(full_audio)} samples)"
                )

                # Libérer la mémoire
                self._audio_chunks = []

                return self.audio_file

            except Exception as e:
                logger.error(f"Erreur sauvegarde audio: {e}")
                return None

    def add_chunk(self, audio_data: np.ndarray) -> None:
        """
        Ajoute un chunk audio à l'enregistrement

        Args:
            audio_data: Données audio numpy array
        """
        if not self._is_recording:
            return

        with self._lock:
            self._audio_chunks.append(audio_data.copy())
            self._total_samples += len(audio_data)

    def get_duration(self) -> float:
        """Retourne la durée enregistrée en secondes"""
        return self._total_samples / self.sample_rate

    @property
    def is_recording(self) -> bool:
        return self._is_recording


class PyannotePostProcessor:
    """
    Post-processeur utilisant pyannote pour la diarisation
    """

    def __init__(
        self,
        hf_token: Optional[str] = None,
        hf_token_env: str = "TOKEN_HF",
        model_name: str = "pyannote/speaker-diarization-3.1"
    ):
        """
        Initialise le post-processeur

        Args:
            hf_token: Token Hugging Face
            hf_token_env: Variable d'environnement contenant le token
            model_name: Nom du modèle pyannote
        """
        import os
        self.hf_token = hf_token or os.environ.get(hf_token_env)
        self.model_name = model_name

        self._pipeline = None
        self._pipeline_loaded = False

        # Vérifier si pyannote est disponible
        try:
            from pyannote.audio import Pipeline
            self._pyannote_available = True
        except ImportError:
            self._pyannote_available = False
            logger.warning("pyannote-audio non disponible pour le post-processing")

    def _load_pipeline(self) -> bool:
        """Charge le pipeline pyannote"""
        if self._pipeline_loaded:
            return True

        if not self._pyannote_available:
            return False

        if not self.hf_token:
            logger.error("Token Hugging Face requis pour pyannote")
            return False

        try:
            from pyannote.audio import Pipeline

            logger.info(f"Chargement du pipeline pyannote '{self.model_name}'...")
            self._pipeline = Pipeline.from_pretrained(
                self.model_name,
                use_auth_token=self.hf_token
            )
            self._pipeline_loaded = True
            logger.info("Pipeline pyannote chargé avec succès")
            return True

        except Exception as e:
            logger.error(f"Erreur chargement pipeline pyannote: {e}")
            return False

    def process_audio_file(
        self,
        audio_file: Path,
        min_speakers: int = 1,
        max_speakers: int = 10
    ) -> List[Tuple[float, float, str]]:
        """
        Effectue la diarisation sur un fichier audio

        Args:
            audio_file: Chemin du fichier audio
            min_speakers: Nombre minimum de locuteurs
            max_speakers: Nombre maximum de locuteurs

        Returns:
            Liste de tuples (start, end, speaker_id)
        """
        if not self._load_pipeline():
            logger.error("Impossible de charger le pipeline pyannote")
            return []

        try:
            logger.info(f"Diarisation de {audio_file}...")
            start_time = time.time()

            # Exécuter la diarisation
            diarization = self._pipeline(
                str(audio_file),
                min_speakers=min_speakers,
                max_speakers=max_speakers
            )

            # Extraire les segments
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                segments.append((turn.start, turn.end, speaker))

            elapsed = time.time() - start_time
            logger.info(
                f"Diarisation terminée: {len(segments)} segments, "
                f"{len(set(s[2] for s in segments))} locuteurs détectés "
                f"({elapsed:.1f}s)"
            )

            return segments

        except Exception as e:
            logger.error(f"Erreur diarisation pyannote: {e}", exc_info=True)
            return []

    def reassign_speakers_to_transcript(
        self,
        transcript_segments: List[dict],
        diarization_segments: List[Tuple[float, float, str]]
    ) -> List[dict]:
        """
        Réattribue les locuteurs aux segments de transcription

        Args:
            transcript_segments: Segments de transcription avec start_time, end_time, text
            diarization_segments: Segments de diarisation (start, end, speaker)

        Returns:
            Segments de transcription avec speaker_id mis à jour
        """
        if not diarization_segments:
            return transcript_segments

        result = []

        for trans_seg in transcript_segments:
            trans_start = trans_seg.get("start_time", 0)
            trans_end = trans_seg.get("end_time", 0)
            trans_mid = (trans_start + trans_end) / 2

            # Trouver le locuteur pour ce segment
            best_speaker = None
            best_overlap = 0

            for diar_start, diar_end, speaker in diarization_segments:
                # Calculer le chevauchement
                overlap_start = max(trans_start, diar_start)
                overlap_end = min(trans_end, diar_end)
                overlap = max(0, overlap_end - overlap_start)

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_speaker = speaker

            # Si pas de chevauchement, utiliser le milieu du segment
            if best_speaker is None:
                for diar_start, diar_end, speaker in diarization_segments:
                    if diar_start <= trans_mid <= diar_end:
                        best_speaker = speaker
                        break

            # Mettre à jour le segment
            updated_seg = trans_seg.copy()
            if best_speaker:
                updated_seg["speaker_id"] = best_speaker
                # Convertir SPEAKER_XX en Locuteur N
                try:
                    speaker_num = int(best_speaker.split("_")[1]) + 1
                    updated_seg["speaker_label"] = f"Locuteur {speaker_num}"
                except:
                    updated_seg["speaker_label"] = best_speaker

            result.append(updated_seg)

        return result

    @property
    def is_available(self) -> bool:
        """Vérifie si pyannote est disponible"""
        return self._pyannote_available and self.hf_token is not None
