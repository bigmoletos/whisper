"""
Module de capture audio en temps réel avec détection de silence
"""

import sounddevice as sd
import numpy as np
import logging
from typing import Optional, Callable
import time

logger = logging.getLogger(__name__)


class AudioCapture:
    """Capture audio du microphone avec détection de silence"""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_duration: float = 3.0,
        silence_threshold: float = 0.01,
        silence_duration: float = 1.5
    ):
        """
        Initialise le capteur audio

        Args:
            sample_rate: Fréquence d'échantillonnage (Hz)
            channels: Nombre de canaux (1 = mono)
            chunk_duration: Durée de chaque segment audio (secondes)
            silence_threshold: Seuil de détection de silence (amplitude)
            silence_duration: Durée de silence pour arrêter l'enregistrement (secondes)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_duration = chunk_duration
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

        self.is_recording = False
        self.audio_buffer = []
        self.stream: Optional[sd.InputStream] = None

        # Vérifier les périphériques audio disponibles
        try:
            devices = sd.query_devices()
            default_input = sd.query_devices(kind='input')
            logger.info(f"Périphérique audio par défaut: {default_input['name']}")
        except Exception as e:
            logger.warning(f"Erreur lors de la détection des périphériques audio: {e}")

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback appelé pour chaque chunk audio"""
        if status:
            logger.warning(f"Status audio: {status}")

        if self.is_recording:
            # Convertir en numpy array et normaliser
            audio_chunk = indata[:, 0] if self.channels == 1 else indata
            self.audio_buffer.append(audio_chunk.copy())

    def start_recording(self) -> None:
        """Démarre l'enregistrement audio"""
        if self.is_recording:
            logger.warning("L'enregistrement est déjà en cours")
            return

        self.is_recording = True
        self.audio_buffer = []

        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.float32,
                callback=self._audio_callback,
                blocksize=int(self.sample_rate * 0.1)  # 100ms par bloc
            )
            self.stream.start()
            logger.info("Enregistrement audio démarré")
        except Exception as e:
            logger.error(f"Erreur lors du démarrage de l'enregistrement: {e}")
            self.is_recording = False
            raise

    def stop_recording(self) -> np.ndarray:
        """
        Arrête l'enregistrement et retourne l'audio capturé

        Returns:
            Array numpy contenant l'audio capturé
        """
        if not self.is_recording:
            logger.warning("Aucun enregistrement en cours")
            return np.array([])

        self.is_recording = False

        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None

            if self.audio_buffer:
                # Concaténer tous les chunks
                audio_data = np.concatenate(self.audio_buffer, axis=0)
                logger.info(f"Audio capturé: {len(audio_data) / self.sample_rate:.2f} secondes")
                return audio_data
            else:
                logger.warning("Aucune donnée audio capturée")
                return np.array([])
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt de l'enregistrement: {e}")
            return np.array([])

    def record_until_silence(self, max_duration: float = 30.0) -> np.ndarray:
        """
        Enregistre jusqu'à détection de silence ou durée maximale

        Args:
            max_duration: Durée maximale d'enregistrement (secondes)

        Returns:
            Array numpy contenant l'audio capturé
        """
        self.start_recording()

        silence_start_time = None
        start_time = time.time()
        chunk_samples = int(self.sample_rate * 0.1)  # 100ms

        try:
            while True:
                # Vérifier la durée maximale
                if time.time() - start_time > max_duration:
                    logger.info("Durée maximale d'enregistrement atteinte")
                    break

                # Attendre un chunk
                time.sleep(0.1)

                if not self.audio_buffer:
                    continue

                # Analyser le dernier chunk pour détecter le silence
                last_chunk = self.audio_buffer[-1]
                rms = np.sqrt(np.mean(last_chunk**2))

                if rms < self.silence_threshold:
                    # Silence détecté
                    if silence_start_time is None:
                        silence_start_time = time.time()
                    elif time.time() - silence_start_time >= self.silence_duration:
                        logger.info("Silence détecté, arrêt de l'enregistrement")
                        break
                else:
                    # Son détecté, réinitialiser le compteur de silence
                    silence_start_time = None

        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement jusqu'au silence: {e}", exc_info=True)

        # Arrêter l'enregistrement et retourner l'audio
        return self.stop_recording()

    def get_audio_level(self) -> float:
        """
        Retourne le niveau audio actuel (RMS)

        Returns:
            Niveau RMS de l'audio actuel
        """
        if not self.audio_buffer:
            return 0.0

        try:
            last_chunk = self.audio_buffer[-1]
            return float(np.sqrt(np.mean(last_chunk**2)))
        except Exception:
            return 0.0

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
