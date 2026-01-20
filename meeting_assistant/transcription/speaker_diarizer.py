"""
Diarisation des locuteurs pour identifier qui parle
Utilise pyannote-audio pour la détection automatique des voix
"""

import logging
import threading
import json
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

# Import conditionnel de pyannote
PYANNOTE_AVAILABLE = False
try:
    from pyannote.audio import Pipeline
    from pyannote.audio.pipelines.utils.hook import ProgressHook
    PYANNOTE_AVAILABLE = True
except ImportError:
    logger.warning("pyannote-audio non disponible - diarisation désactivée")


@dataclass
class Speaker:
    """Représente un locuteur identifié"""
    id: str  # ID unique (SPEAKER_00, SPEAKER_01, etc.)
    label: str  # Nom affiché (peut être personnalisé)
    color: str = ""  # Couleur pour l'affichage
    total_speaking_time: float = 0.0  # Temps de parole total en secondes
    segment_count: int = 0  # Nombre de segments
    voice_embedding: Optional[np.ndarray] = None  # Empreinte vocale (optionnel)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "label": self.label,
            "color": self.color,
            "total_speaking_time": self.total_speaking_time,
            "segment_count": self.segment_count
        }


@dataclass
class DiarizedSegment:
    """Segment avec information de locuteur"""
    speaker_id: str
    speaker_label: str
    start_time: float
    end_time: float
    text: str = ""
    confidence: float = 0.0

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def to_dict(self) -> Dict:
        return {
            "speaker_id": self.speaker_id,
            "speaker_label": self.speaker_label,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "text": self.text,
            "confidence": self.confidence,
            "duration": self.duration
        }


# Couleurs par défaut pour les locuteurs
DEFAULT_COLORS = [
    "#4A90D9",  # Bleu
    "#50C878",  # Vert émeraude
    "#FF6B6B",  # Rouge corail
    "#FFD93D",  # Jaune
    "#9B59B6",  # Violet
    "#1ABC9C",  # Turquoise
    "#E67E22",  # Orange
    "#95A5A6",  # Gris
]


class SpeakerDiarizer:
    """
    Gère la diarisation des locuteurs
    Détecte automatiquement les différentes voix et permet le renommage
    """

    def __init__(
        self,
        hf_token: Optional[str] = None,
        hf_token_env: str = "TOKEN_HF",
        model_name: str = "pyannote/speaker-diarization-3.1",
        min_speakers: int = 1,
        max_speakers: int = 10,
        session_dir: Optional[Path] = None,
        session_id: Optional[str] = None
    ):
        """
        Initialise le diarizer

        Args:
            hf_token: Token Hugging Face (requis pour pyannote)
            hf_token_env: Nom de la variable d'environnement contenant le token
            model_name: Nom du modèle pyannote
            min_speakers: Nombre minimum de locuteurs attendus
            max_speakers: Nombre maximum de locuteurs attendus
            session_dir: Répertoire de session pour sauvegarder les mappings
            session_id: ID de session
        """
        # Récupérer le token depuis l'environnement si non fourni
        import os
        self.hf_token = hf_token or os.environ.get(hf_token_env)
        self.model_name = model_name
        self.min_speakers = min_speakers
        self.max_speakers = max_speakers
        self.session_dir = session_dir
        self.session_id = session_id

        # Pipeline pyannote (chargé à la demande)
        self._pipeline: Optional[Pipeline] = None
        self._pipeline_loaded = False

        # Mapping des locuteurs
        self._speakers: Dict[str, Speaker] = {}
        self._speaker_labels: Dict[str, str] = {}  # ID -> Label personnalisé
        self._lock = threading.Lock()

        # Charger les labels sauvegardés si disponibles
        self._load_speaker_labels()

        logger.info(
            f"SpeakerDiarizer initialisé: {model_name}, "
            f"speakers={min_speakers}-{max_speakers}"
        )

    def _load_pipeline(self) -> bool:
        """
        Charge le pipeline pyannote

        Returns:
            True si chargé avec succès
        """
        if self._pipeline_loaded:
            return True

        if not PYANNOTE_AVAILABLE:
            logger.error("pyannote-audio n'est pas installé")
            return False

        if not self.hf_token:
            logger.error(
                "Token Hugging Face requis pour pyannote. "
                "Obtenez-en un sur https://huggingface.co/settings/tokens"
            )
            return False

        try:
            logger.info(f"Chargement du modèle de diarisation '{self.model_name}'...")
            self._pipeline = Pipeline.from_pretrained(
                self.model_name,
                use_auth_token=self.hf_token
            )
            self._pipeline_loaded = True
            logger.info("Pipeline de diarisation chargé avec succès")
            return True

        except Exception as e:
            logger.error(f"Erreur chargement pipeline diarisation: {e}")
            return False

    def diarize(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> List[Tuple[float, float, str]]:
        """
        Effectue la diarisation sur un segment audio

        Args:
            audio_data: Données audio numpy array
            sample_rate: Fréquence d'échantillonnage

        Returns:
            Liste de tuples (start, end, speaker_id)
        """
        if not self._pipeline_loaded:
            if not self._load_pipeline():
                return []

        try:
            # Créer un fichier audio temporaire ou utiliser le format attendu
            import tempfile
            import soundfile as sf

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                temp_path = f.name
                sf.write(temp_path, audio_data, sample_rate)

            # Exécuter la diarisation
            diarization = self._pipeline(
                temp_path,
                min_speakers=self.min_speakers,
                max_speakers=self.max_speakers
            )

            # Nettoyer
            Path(temp_path).unlink(missing_ok=True)

            # Extraire les segments
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                segments.append((turn.start, turn.end, speaker))

                # Enregistrer le locuteur
                self._register_speaker(speaker, turn.end - turn.start)

            return segments

        except Exception as e:
            logger.error(f"Erreur diarisation: {e}", exc_info=True)
            return []

    def diarize_with_transcription(
        self,
        segments: List[Dict],
        audio_duration: float
    ) -> List[DiarizedSegment]:
        """
        Associe les segments de transcription aux locuteurs
        Version simplifiée basée sur la détection de changement de voix

        Args:
            segments: Liste de segments avec 'start', 'end', 'text'
            audio_duration: Durée totale de l'audio

        Returns:
            Liste de DiarizedSegment
        """
        if not segments:
            return []

        # Si pyannote n'est pas disponible, utiliser une heuristique simple
        if not PYANNOTE_AVAILABLE or not self._pipeline_loaded:
            return self._simple_diarization(segments)

        # TODO: Implémenter la diarisation complète avec pyannote
        return self._simple_diarization(segments)

    def _simple_diarization(self, segments: List[Dict]) -> List[DiarizedSegment]:
        """
        Diarisation simplifiée basée sur les pauses
        Heuristique: une pause > 2s suggère un changement de locuteur

        Args:
            segments: Liste de segments

        Returns:
            Liste de DiarizedSegment
        """
        if not segments:
            return []

        result = []
        current_speaker_idx = 0
        last_end_time = 0.0
        pause_threshold = 2.0  # Pause suggérant un changement de locuteur

        for seg in segments:
            start = seg.get("start", seg.get("start_time", 0))
            end = seg.get("end", seg.get("end_time", 0))
            text = seg.get("text", "")

            # Détecter un changement potentiel de locuteur
            if start - last_end_time > pause_threshold:
                current_speaker_idx = (current_speaker_idx + 1) % self.max_speakers

            speaker_id = f"SPEAKER_{current_speaker_idx:02d}"
            speaker = self._get_or_create_speaker(speaker_id)

            result.append(DiarizedSegment(
                speaker_id=speaker_id,
                speaker_label=speaker.label,
                start_time=start,
                end_time=end,
                text=text
            ))

            # Mettre à jour les stats du locuteur
            speaker.total_speaking_time += (end - start)
            speaker.segment_count += 1

            last_end_time = end

        return result

    def _register_speaker(self, speaker_id: str, duration: float) -> None:
        """Enregistre ou met à jour un locuteur"""
        with self._lock:
            speaker = self._get_or_create_speaker(speaker_id)
            speaker.total_speaking_time += duration
            speaker.segment_count += 1

    def _get_or_create_speaker(self, speaker_id: str) -> Speaker:
        """Récupère ou crée un locuteur"""
        if speaker_id not in self._speakers:
            # Créer un nouveau locuteur
            idx = len(self._speakers)
            color = DEFAULT_COLORS[idx % len(DEFAULT_COLORS)]

            # Utiliser le label personnalisé si disponible
            label = self._speaker_labels.get(speaker_id, f"Locuteur {idx + 1}")

            self._speakers[speaker_id] = Speaker(
                id=speaker_id,
                label=label,
                color=color
            )

            logger.info(f"Nouveau locuteur détecté: {speaker_id} -> {label}")

        return self._speakers[speaker_id]

    def rename_speaker(self, speaker_id: str, new_label: str) -> bool:
        """
        Renomme un locuteur

        Args:
            speaker_id: ID du locuteur (SPEAKER_00, etc.)
            new_label: Nouveau nom à afficher

        Returns:
            True si renommé avec succès
        """
        with self._lock:
            if speaker_id in self._speakers:
                self._speakers[speaker_id].label = new_label
                self._speaker_labels[speaker_id] = new_label
                self._save_speaker_labels()
                logger.info(f"Locuteur renommé: {speaker_id} -> {new_label}")
                return True
            else:
                # Enregistrer pour usage futur
                self._speaker_labels[speaker_id] = new_label
                self._save_speaker_labels()
                return True
        return False

    def set_speaker_names(self, names: List[str]) -> None:
        """
        Définit les noms des locuteurs à l'avance

        Args:
            names: Liste des noms dans l'ordre (Locuteur 1, 2, etc.)
        """
        with self._lock:
            for i, name in enumerate(names):
                speaker_id = f"SPEAKER_{i:02d}"
                self._speaker_labels[speaker_id] = name

                if speaker_id in self._speakers:
                    self._speakers[speaker_id].label = name

            self._save_speaker_labels()
            logger.info(f"Noms des locuteurs définis: {names}")

    def get_speakers(self) -> List[Speaker]:
        """Retourne la liste des locuteurs détectés"""
        with self._lock:
            return list(self._speakers.values())

    def get_speaker_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques des locuteurs"""
        with self._lock:
            total_time = sum(s.total_speaking_time for s in self._speakers.values())

            return {
                "speaker_count": len(self._speakers),
                "total_speaking_time": total_time,
                "speakers": [
                    {
                        **s.to_dict(),
                        "speaking_percentage": (
                            (s.total_speaking_time / total_time * 100)
                            if total_time > 0 else 0
                        )
                    }
                    for s in self._speakers.values()
                ]
            }

    def _save_speaker_labels(self) -> None:
        """Sauvegarde les labels des locuteurs"""
        if not self.session_dir or not self.session_id:
            return

        try:
            labels_file = self.session_dir / self.session_id / "speaker_labels.json"
            labels_file.parent.mkdir(parents=True, exist_ok=True)

            with open(labels_file, "w", encoding="utf-8") as f:
                json.dump(self._speaker_labels, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Erreur sauvegarde labels locuteurs: {e}")

    def _load_speaker_labels(self) -> None:
        """Charge les labels des locuteurs depuis la session"""
        if not self.session_dir or not self.session_id:
            return

        try:
            labels_file = self.session_dir / self.session_id / "speaker_labels.json"

            if labels_file.exists():
                with open(labels_file, "r", encoding="utf-8") as f:
                    self._speaker_labels = json.load(f)
                logger.info(f"Labels locuteurs chargés: {len(self._speaker_labels)}")

        except Exception as e:
            logger.error(f"Erreur chargement labels locuteurs: {e}")

    def format_transcript_with_speakers(
        self,
        segments: List[DiarizedSegment],
        include_timestamps: bool = True
    ) -> str:
        """
        Formate la transcription avec les noms des locuteurs

        Args:
            segments: Liste de segments diarisés
            include_timestamps: Inclure les timestamps

        Returns:
            Transcription formatée
        """
        if not segments:
            return ""

        lines = []
        current_speaker = None

        for seg in segments:
            if seg.speaker_label != current_speaker:
                current_speaker = seg.speaker_label

                if include_timestamps:
                    timestamp = self._format_time(seg.start_time)
                    lines.append(f"\n[{timestamp}] **{current_speaker}**:")
                else:
                    lines.append(f"\n**{current_speaker}**:")

            if seg.text.strip():
                lines.append(seg.text.strip())

        return "\n".join(lines)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Formate un temps en MM:SS"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    @property
    def is_available(self) -> bool:
        """Vérifie si la diarisation est disponible"""
        return PYANNOTE_AVAILABLE

    @property
    def is_loaded(self) -> bool:
        """Vérifie si le pipeline est chargé"""
        return self._pipeline_loaded
