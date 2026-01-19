"""
Buffer circulaire pour accumulation audio avant transcription
Optimisé pour une utilisation mémoire constante
"""

import threading
import logging
import time
from typing import Optional, Callable
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)


class AudioBuffer:
    """
    Buffer circulaire qui accumule l'audio et déclenche un callback
    quand la durée cible est atteinte (ex: 10 secondes)
    """

    def __init__(
        self,
        target_duration_seconds: float = 10.0,
        sample_rate: int = 16000,
        on_buffer_ready: Optional[Callable[[np.ndarray, float], None]] = None,
        silence_threshold: float = 0.01
    ):
        """
        Initialise le buffer audio

        Args:
            target_duration_seconds: Durée cible avant de déclencher le callback
            sample_rate: Fréquence d'échantillonnage
            on_buffer_ready: Callback(audio_data, timestamp) appelé quand le buffer est prêt
            silence_threshold: Seuil en dessous duquel l'audio est considéré comme silence
        """
        self.target_duration = target_duration_seconds
        self.sample_rate = sample_rate
        self.on_buffer_ready = on_buffer_ready
        self.silence_threshold = silence_threshold

        # Calcul de la taille cible en samples
        self.target_samples = int(target_duration_seconds * sample_rate)

        # Buffer principal - utilise une deque pour performance O(1)
        self._buffer = deque()
        self._current_samples = 0
        self._lock = threading.Lock()

        # Timestamp du premier échantillon du buffer courant
        self._buffer_start_time: Optional[float] = None

        # Compteur de buffers traités
        self._buffer_count = 0

        # Statistiques
        self._total_samples_processed = 0
        self._total_silence_samples = 0

        logger.info(
            f"AudioBuffer initialisé: {target_duration_seconds}s @ {sample_rate}Hz "
            f"(cible: {self.target_samples} samples)"
        )

    def add_chunk(self, audio_chunk: np.ndarray) -> None:
        """
        Ajoute un chunk audio au buffer

        Args:
            audio_chunk: Données audio numpy array
        """
        if len(audio_chunk) == 0:
            return

        with self._lock:
            # Enregistrer le timestamp du début si c'est le premier chunk
            if self._buffer_start_time is None:
                self._buffer_start_time = time.time()

            # Ajouter au buffer
            self._buffer.append(audio_chunk.copy())
            self._current_samples += len(audio_chunk)
            self._total_samples_processed += len(audio_chunk)

            # Vérifier si le buffer est prêt
            if self._current_samples >= self.target_samples:
                self._flush_buffer()

    def _flush_buffer(self) -> None:
        """
        Vide le buffer et déclenche le callback (appelé avec le lock déjà acquis)
        """
        if not self._buffer:
            return

        # Assembler tous les chunks
        audio_data = np.concatenate(list(self._buffer))

        # Tronquer à la taille exacte si nécessaire
        if len(audio_data) > self.target_samples:
            # Garder l'excédent pour le prochain buffer
            excess = audio_data[self.target_samples:]
            audio_data = audio_data[:self.target_samples]
            self._buffer.clear()
            self._buffer.append(excess)
            self._current_samples = len(excess)
        else:
            self._buffer.clear()
            self._current_samples = 0

        # Vérifier si c'est du silence
        audio_energy = np.abs(audio_data).mean()
        is_silence = audio_energy < self.silence_threshold

        if is_silence:
            self._total_silence_samples += len(audio_data)
            logger.debug(f"Buffer #{self._buffer_count}: silence détecté (énergie: {audio_energy:.6f})")
        else:
            logger.debug(f"Buffer #{self._buffer_count}: audio valide (énergie: {audio_energy:.6f})")

        # Appeler le callback même pour le silence (pour maintenir le timing)
        timestamp = self._buffer_start_time or time.time()
        self._buffer_start_time = time.time()  # Reset pour le prochain buffer
        self._buffer_count += 1

        # Déclencher le callback dans un thread séparé pour ne pas bloquer
        if self.on_buffer_ready:
            callback_thread = threading.Thread(
                target=self._safe_callback,
                args=(audio_data, timestamp, is_silence),
                daemon=True
            )
            callback_thread.start()

    def _safe_callback(self, audio_data: np.ndarray, timestamp: float, is_silence: bool) -> None:
        """
        Appelle le callback de manière sécurisée

        Args:
            audio_data: Données audio
            timestamp: Timestamp du début du buffer
            is_silence: True si c'est du silence
        """
        try:
            if self.on_buffer_ready:
                # Le callback reçoit (audio_data, timestamp)
                # is_silence est passé comme attribut de l'objet numpy si besoin
                self.on_buffer_ready(audio_data, timestamp)
        except Exception as e:
            logger.error(f"Erreur dans le callback on_buffer_ready: {e}", exc_info=True)

    def flush(self) -> Optional[np.ndarray]:
        """
        Force le vidage du buffer même s'il n'est pas plein

        Returns:
            Données audio restantes ou None
        """
        with self._lock:
            if not self._buffer:
                return None

            audio_data = np.concatenate(list(self._buffer))
            timestamp = self._buffer_start_time or time.time()

            self._buffer.clear()
            self._current_samples = 0
            self._buffer_start_time = None
            self._buffer_count += 1

            # Déclencher le callback
            if self.on_buffer_ready and len(audio_data) > 0:
                self._safe_callback(audio_data, timestamp, False)

            return audio_data

    def clear(self) -> None:
        """Vide le buffer sans déclencher de callback"""
        with self._lock:
            self._buffer.clear()
            self._current_samples = 0
            self._buffer_start_time = None

    def get_stats(self) -> dict:
        """
        Retourne les statistiques du buffer

        Returns:
            Dictionnaire avec les statistiques
        """
        with self._lock:
            total_duration = self._total_samples_processed / self.sample_rate
            silence_duration = self._total_silence_samples / self.sample_rate

            return {
                "buffer_count": self._buffer_count,
                "current_samples": self._current_samples,
                "current_duration_seconds": self._current_samples / self.sample_rate,
                "target_duration_seconds": self.target_duration,
                "total_processed_seconds": total_duration,
                "total_silence_seconds": silence_duration,
                "speech_ratio": 1 - (silence_duration / total_duration) if total_duration > 0 else 0,
                "memory_usage_bytes": self._current_samples * 4  # float32 = 4 bytes
            }

    @property
    def current_duration(self) -> float:
        """Retourne la durée actuelle du buffer en secondes"""
        return self._current_samples / self.sample_rate

    @property
    def is_ready(self) -> bool:
        """Retourne True si le buffer a atteint la durée cible"""
        return self._current_samples >= self.target_samples

    @property
    def buffer_count(self) -> int:
        """Retourne le nombre de buffers traités"""
        return self._buffer_count

    def __len__(self) -> int:
        """Retourne le nombre de samples dans le buffer"""
        return self._current_samples


class SilenceDetector:
    """
    Détecteur de silence pour optimiser la transcription
    Ne transcrit pas les périodes de silence prolongé
    """

    def __init__(
        self,
        threshold: float = 0.01,
        min_silence_duration: float = 2.0,
        sample_rate: int = 16000
    ):
        """
        Initialise le détecteur de silence

        Args:
            threshold: Seuil d'énergie pour le silence
            min_silence_duration: Durée minimale de silence pour le détecter
            sample_rate: Fréquence d'échantillonnage
        """
        self.threshold = threshold
        self.min_silence_samples = int(min_silence_duration * sample_rate)
        self.sample_rate = sample_rate

        self._consecutive_silence_samples = 0
        self._in_silence = False

    def process(self, audio: np.ndarray) -> bool:
        """
        Analyse un chunk audio pour détecter le silence

        Args:
            audio: Données audio

        Returns:
            True si on est dans une période de silence prolongé
        """
        energy = np.abs(audio).mean()

        if energy < self.threshold:
            self._consecutive_silence_samples += len(audio)
            if self._consecutive_silence_samples >= self.min_silence_samples:
                if not self._in_silence:
                    logger.debug("Entrée en période de silence")
                self._in_silence = True
        else:
            if self._in_silence:
                logger.debug(f"Fin du silence après {self._consecutive_silence_samples / self.sample_rate:.1f}s")
            self._consecutive_silence_samples = 0
            self._in_silence = False

        return self._in_silence

    def reset(self) -> None:
        """Réinitialise le détecteur"""
        self._consecutive_silence_samples = 0
        self._in_silence = False

    @property
    def is_silent(self) -> bool:
        """Retourne True si on est actuellement en silence"""
        return self._in_silence
