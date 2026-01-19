"""
Stockage incrémental des transcriptions sur disque
Optimisé pour économiser la mémoire et permettre la récupération après crash
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class TranscriptSegment:
    """Représente un segment de transcription"""

    def __init__(
        self,
        text: str,
        start_time: float,
        end_time: float,
        segment_index: int
    ):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.segment_index = segment_index
        self.created_at = time.time()

    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            "text": self.text,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "segment_index": self.segment_index,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TranscriptSegment":
        """Crée depuis un dictionnaire"""
        segment = cls(
            text=data["text"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            segment_index=data["segment_index"]
        )
        segment.created_at = data.get("created_at", time.time())
        return segment

    def format_timestamp(self) -> str:
        """Formate le timestamp en HH:MM:SS"""
        total_seconds = int(self.start_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class TranscriptStorage:
    """
    Stockage incrémental des transcriptions
    Écrit sur disque au fur et à mesure pour économiser la mémoire
    """

    def __init__(
        self,
        session_dir: Path,
        session_id: str
    ):
        """
        Initialise le stockage

        Args:
            session_dir: Répertoire de base pour les sessions
            session_id: Identifiant unique de la session
        """
        self.session_dir = Path(session_dir)
        self.session_id = session_id

        # Créer le répertoire de session
        self.transcript_dir = self.session_dir / session_id / "transcript"
        self.transcript_dir.mkdir(parents=True, exist_ok=True)

        # Fichiers
        self.raw_file = self.transcript_dir / "raw.txt"
        self.segments_file = self.transcript_dir / "segments.jsonl"
        self.metadata_file = self.transcript_dir / "metadata.json"

        # État
        self._segment_count = 0
        self._total_duration = 0.0
        self._total_words = 0
        self._lock = threading.Lock()
        self._start_time = time.time()

        # Initialiser les fichiers
        self._init_files()

        logger.info(f"TranscriptStorage initialisé: {self.transcript_dir}")

    def _init_files(self) -> None:
        """Initialise les fichiers de stockage"""
        # Créer le fichier raw s'il n'existe pas
        if not self.raw_file.exists():
            self.raw_file.touch()

        # Créer le fichier segments s'il n'existe pas
        if not self.segments_file.exists():
            self.segments_file.touch()

        # Charger ou créer les métadonnées
        if self.metadata_file.exists():
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                self._segment_count = metadata.get("segment_count", 0)
                self._total_duration = metadata.get("total_duration", 0.0)
                self._total_words = metadata.get("total_words", 0)
                self._start_time = metadata.get("start_time", time.time())
        else:
            self._save_metadata()

    def _save_metadata(self) -> None:
        """Sauvegarde les métadonnées"""
        metadata = {
            "session_id": self.session_id,
            "segment_count": self._segment_count,
            "total_duration": self._total_duration,
            "total_words": self._total_words,
            "start_time": self._start_time,
            "last_update": time.time()
        }
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

    def add_segment(self, text: str, start_time: float, end_time: float) -> TranscriptSegment:
        """
        Ajoute un segment de transcription

        Args:
            text: Texte transcrit
            start_time: Timestamp de début (relatif au début de la session)
            end_time: Timestamp de fin

        Returns:
            Le segment créé
        """
        with self._lock:
            # Créer le segment
            segment = TranscriptSegment(
                text=text,
                start_time=start_time,
                end_time=end_time,
                segment_index=self._segment_count
            )

            # Écrire dans le fichier raw (texte brut avec timestamp)
            if text.strip():
                timestamp_str = segment.format_timestamp()
                with open(self.raw_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp_str}] {text}\n")

            # Écrire dans le fichier segments (JSONL)
            with open(self.segments_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(segment.to_dict(), ensure_ascii=False) + "\n")

            # Mise à jour des stats
            self._segment_count += 1
            self._total_duration = max(self._total_duration, end_time)
            self._total_words += len(text.split())

            # Sauvegarder les métadonnées périodiquement (tous les 10 segments)
            if self._segment_count % 10 == 0:
                self._save_metadata()

            return segment

    def get_text_since(self, minutes_ago: float) -> str:
        """
        Récupère le texte des N dernières minutes

        Args:
            minutes_ago: Nombre de minutes en arrière

        Returns:
            Texte concaténé
        """
        cutoff_time = self._total_duration - (minutes_ago * 60)
        if cutoff_time < 0:
            cutoff_time = 0

        texts = []
        with self._lock:
            with open(self.segments_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        segment_data = json.loads(line)
                        if segment_data["start_time"] >= cutoff_time:
                            if segment_data["text"].strip():
                                texts.append(segment_data["text"])

        return " ".join(texts)

    def get_all_text(self) -> str:
        """
        Récupère tout le texte transcrit

        Returns:
            Texte complet
        """
        with self._lock:
            if self.raw_file.exists():
                return self.raw_file.read_text(encoding="utf-8")
        return ""

    def get_segments(
        self,
        start_index: int = 0,
        end_index: Optional[int] = None
    ) -> List[TranscriptSegment]:
        """
        Récupère les segments dans une plage

        Args:
            start_index: Index de début
            end_index: Index de fin (None = jusqu'à la fin)

        Returns:
            Liste des segments
        """
        segments = []
        with self._lock:
            with open(self.segments_file, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i < start_index:
                        continue
                    if end_index is not None and i >= end_index:
                        break
                    if line.strip():
                        segment_data = json.loads(line)
                        segments.append(TranscriptSegment.from_dict(segment_data))
        return segments

    def get_formatted_transcript(self) -> List[dict]:
        """
        Récupère la transcription formatée pour le rapport

        Returns:
            Liste de dictionnaires avec timestamp et text
        """
        result = []
        with self._lock:
            with open(self.segments_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        segment_data = json.loads(line)
                        if segment_data["text"].strip():
                            segment = TranscriptSegment.from_dict(segment_data)
                            result.append({
                                "timestamp": segment.format_timestamp(),
                                "text": segment.text
                            })
        return result

    def get_stats(self) -> dict:
        """
        Retourne les statistiques de stockage

        Returns:
            Dictionnaire avec les statistiques
        """
        with self._lock:
            return {
                "session_id": self.session_id,
                "segment_count": self._segment_count,
                "total_duration_seconds": self._total_duration,
                "total_duration_formatted": self._format_duration(self._total_duration),
                "total_words": self._total_words,
                "words_per_minute": (
                    self._total_words / (self._total_duration / 60)
                    if self._total_duration > 0 else 0
                ),
                "raw_file_size_bytes": (
                    self.raw_file.stat().st_size if self.raw_file.exists() else 0
                ),
                "transcript_dir": str(self.transcript_dir)
            }

    def _format_duration(self, seconds: float) -> str:
        """Formate une durée en HH:MM:SS"""
        total = int(seconds)
        hours = total // 3600
        minutes = (total % 3600) // 60
        secs = total % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def finalize(self) -> None:
        """Finalise le stockage (sauvegarde les métadonnées finales)"""
        with self._lock:
            self._save_metadata()
            logger.info(
                f"Transcription finalisée: {self._segment_count} segments, "
                f"{self._format_duration(self._total_duration)}, "
                f"{self._total_words} mots"
            )

    @property
    def segment_count(self) -> int:
        """Nombre de segments"""
        return self._segment_count

    @property
    def total_duration(self) -> float:
        """Durée totale en secondes"""
        return self._total_duration

    @property
    def total_words(self) -> int:
        """Nombre total de mots"""
        return self._total_words
