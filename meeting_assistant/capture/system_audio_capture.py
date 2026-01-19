"""
Capture audio système via WASAPI Loopback (Windows)
Permet de capturer l'audio de sortie du système (Teams, Zoom, etc.) de manière invisible
"""

import threading
import logging
import time
from typing import Optional, Callable
import numpy as np

logger = logging.getLogger(__name__)

# Import PyAudioWPatch avec gestion d'erreur
try:
    import pyaudiowpatch as pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    try:
        import pyaudio
        PYAUDIO_AVAILABLE = True
        logger.warning("PyAudioWPatch non disponible, utilisation de PyAudio standard (loopback limité)")
    except ImportError:
        PYAUDIO_AVAILABLE = False
        pyaudio = None
        logger.error("PyAudio non disponible - la capture audio ne fonctionnera pas")


class SystemAudioCapture:
    """
    Capture l'audio système via WASAPI Loopback
    Permet d'enregistrer la sortie audio sans microphone
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_duration: float = 0.1,
        on_audio_chunk: Optional[Callable[[np.ndarray], None]] = None
    ):
        """
        Initialise la capture audio système

        Args:
            sample_rate: Fréquence d'échantillonnage cible (16000 pour Whisper)
            channels: Nombre de canaux (1 = mono)
            chunk_duration: Durée de chaque chunk audio en secondes
            on_audio_chunk: Callback appelé pour chaque chunk audio capturé
        """
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "PyAudioWPatch n'est pas installé. "
                "Installez avec: pip install PyAudioWPatch"
            )

        self.target_sample_rate = sample_rate
        self.channels = channels
        self.chunk_duration = chunk_duration
        self.on_audio_chunk = on_audio_chunk

        self._pyaudio: Optional[pyaudio.PyAudio] = None
        self._stream = None
        self._capture_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._is_paused = False
        self._lock = threading.Lock()

        # Informations du device loopback
        self._loopback_device = None
        self._device_sample_rate = None
        self._device_channels = None

        logger.info(f"SystemAudioCapture initialisé (target: {sample_rate}Hz, {channels}ch)")

    def _find_loopback_device(self) -> dict:
        """
        Trouve le device WASAPI loopback pour capturer l'audio système

        Returns:
            Dictionnaire avec les informations du device
        """
        if self._pyaudio is None:
            self._pyaudio = pyaudio.PyAudio()

        # Chercher le device loopback WASAPI
        loopback_device = None

        try:
            # PyAudioWPatch: utiliser get_loopback_device()
            if hasattr(self._pyaudio, 'get_loopback_device_info_generator'):
                # Méthode PyAudioWPatch
                for loopback in self._pyaudio.get_loopback_device_info_generator():
                    logger.debug(f"Loopback device trouvé: {loopback['name']}")
                    # Prendre le premier device loopback disponible
                    if loopback_device is None:
                        loopback_device = loopback
                    # Préférer le device par défaut
                    if "default" in loopback['name'].lower():
                        loopback_device = loopback
                        break
            else:
                # Fallback: chercher manuellement dans les devices
                host_api_count = self._pyaudio.get_host_api_count()
                for host_idx in range(host_api_count):
                    host_info = self._pyaudio.get_host_api_info_by_index(host_idx)
                    if "WASAPI" in host_info.get('name', ''):
                        # Trouver le device de sortie par défaut WASAPI
                        default_output = host_info.get('defaultOutputDevice', -1)
                        if default_output >= 0:
                            device_info = self._pyaudio.get_device_info_by_index(default_output)
                            loopback_device = device_info
                            break

        except Exception as e:
            logger.error(f"Erreur lors de la recherche du device loopback: {e}")

        if loopback_device is None:
            # Dernier recours: utiliser le device de sortie par défaut
            try:
                default_output = self._pyaudio.get_default_output_device_info()
                loopback_device = default_output
                logger.warning("Utilisation du device de sortie par défaut (pas de loopback dédié)")
            except Exception as e:
                raise RuntimeError(f"Impossible de trouver un device audio: {e}")

        logger.info(f"Device loopback sélectionné: {loopback_device.get('name', 'Unknown')}")
        logger.info(f"  - Sample rate: {loopback_device.get('defaultSampleRate', 'N/A')}Hz")
        logger.info(f"  - Channels: {loopback_device.get('maxInputChannels', 'N/A')}")

        return loopback_device

    def _resample_audio(self, audio: np.ndarray, orig_rate: int, target_rate: int) -> np.ndarray:
        """
        Rééchantillonne l'audio si nécessaire

        Args:
            audio: Données audio
            orig_rate: Fréquence d'origine
            target_rate: Fréquence cible

        Returns:
            Audio rééchantillonné
        """
        if orig_rate == target_rate:
            return audio

        # Calcul du ratio de rééchantillonnage
        ratio = target_rate / orig_rate
        new_length = int(len(audio) * ratio)

        # Rééchantillonnage simple par interpolation linéaire
        indices = np.linspace(0, len(audio) - 1, new_length)
        resampled = np.interp(indices, np.arange(len(audio)), audio)

        return resampled.astype(np.float32)

    def _convert_to_mono(self, audio: np.ndarray, channels: int) -> np.ndarray:
        """
        Convertit l'audio multi-canal en mono

        Args:
            audio: Données audio (entrelacées)
            channels: Nombre de canaux

        Returns:
            Audio mono
        """
        if channels == 1:
            return audio

        # Reshape pour séparer les canaux
        try:
            audio_reshaped = audio.reshape(-1, channels)
            # Moyenne des canaux
            mono = audio_reshaped.mean(axis=1)
            return mono.astype(np.float32)
        except Exception as e:
            logger.warning(f"Erreur conversion mono: {e}, retour audio brut")
            return audio

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """
        Callback appelé par PyAudio pour chaque chunk audio
        """
        if status:
            logger.warning(f"Audio status: {status}")

        if self._is_paused:
            return (None, pyaudio.paContinue)

        try:
            # Convertir les bytes en numpy array
            audio_data = np.frombuffer(in_data, dtype=np.float32)

            # Convertir en mono si nécessaire
            if self._device_channels and self._device_channels > 1:
                audio_data = self._convert_to_mono(audio_data, self._device_channels)

            # Rééchantillonner si nécessaire
            if self._device_sample_rate and self._device_sample_rate != self.target_sample_rate:
                audio_data = self._resample_audio(
                    audio_data,
                    int(self._device_sample_rate),
                    self.target_sample_rate
                )

            # Appeler le callback utilisateur
            if self.on_audio_chunk and len(audio_data) > 0:
                self.on_audio_chunk(audio_data)

        except Exception as e:
            logger.error(f"Erreur dans le callback audio: {e}")

        return (None, pyaudio.paContinue)

    def start(self) -> bool:
        """
        Démarre la capture audio système

        Returns:
            True si démarré avec succès
        """
        with self._lock:
            if self._is_running:
                logger.warning("La capture est déjà en cours")
                return True

            try:
                # Initialiser PyAudio
                if self._pyaudio is None:
                    self._pyaudio = pyaudio.PyAudio()

                # Trouver le device loopback
                self._loopback_device = self._find_loopback_device()
                self._device_sample_rate = int(self._loopback_device.get('defaultSampleRate', 44100))
                self._device_channels = max(
                    self._loopback_device.get('maxInputChannels', 2),
                    self._loopback_device.get('maxOutputChannels', 2)
                )
                if self._device_channels == 0:
                    self._device_channels = 2

                # Calculer la taille du buffer
                frames_per_buffer = int(self._device_sample_rate * self.chunk_duration)

                logger.info(f"Ouverture du stream: {self._device_sample_rate}Hz, {self._device_channels}ch, buffer={frames_per_buffer}")

                # Ouvrir le stream
                stream_kwargs = {
                    'format': pyaudio.paFloat32,
                    'channels': self._device_channels,
                    'rate': self._device_sample_rate,
                    'input': True,
                    'frames_per_buffer': frames_per_buffer,
                    'stream_callback': self._audio_callback,
                }

                # Ajouter le device loopback si disponible
                if 'index' in self._loopback_device:
                    stream_kwargs['input_device_index'] = self._loopback_device['index']

                self._stream = self._pyaudio.open(**stream_kwargs)
                self._stream.start_stream()
                self._is_running = True
                self._is_paused = False

                logger.info("Capture audio système démarrée")
                return True

            except Exception as e:
                logger.error(f"Erreur au démarrage de la capture: {e}", exc_info=True)
                self._cleanup()
                return False

    def stop(self) -> None:
        """Arrête la capture audio"""
        with self._lock:
            if not self._is_running:
                return

            self._is_running = False
            self._cleanup()
            logger.info("Capture audio système arrêtée")

    def pause(self) -> None:
        """Met en pause la capture (continue de tourner mais ignore l'audio)"""
        self._is_paused = True
        logger.info("Capture audio mise en pause")

    def resume(self) -> None:
        """Reprend la capture après une pause"""
        self._is_paused = False
        logger.info("Capture audio reprise")

    def _cleanup(self) -> None:
        """Nettoie les ressources"""
        if self._stream:
            try:
                self._stream.stop_stream()
                self._stream.close()
            except Exception as e:
                logger.debug(f"Erreur fermeture stream: {e}")
            self._stream = None

        if self._pyaudio:
            try:
                self._pyaudio.terminate()
            except Exception as e:
                logger.debug(f"Erreur terminaison PyAudio: {e}")
            self._pyaudio = None

    @property
    def is_running(self) -> bool:
        """Retourne True si la capture est en cours"""
        return self._is_running

    @property
    def is_paused(self) -> bool:
        """Retourne True si la capture est en pause"""
        return self._is_paused

    def get_device_info(self) -> dict:
        """Retourne les informations sur le device de capture"""
        if self._loopback_device:
            return {
                "name": self._loopback_device.get('name', 'Unknown'),
                "sample_rate": self._device_sample_rate,
                "channels": self._device_channels,
                "target_sample_rate": self.target_sample_rate,
                "target_channels": self.channels
            }
        return {"status": "not_initialized"}

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False

    def __del__(self):
        self.stop()
