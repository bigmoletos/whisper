"""
Transcription par micro-batch pour réunions longues
Utilise Faster-Whisper pour transcrire des segments de 10 secondes
Avec sélection adaptative du modèle selon la mémoire disponible
"""

import threading
import logging
import time
import queue
from typing import Optional, Callable
from pathlib import Path
import sys
import numpy as np

# Ajouter le chemin parent pour importer les modules existants
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

logger = logging.getLogger(__name__)

# Import du sélecteur adaptatif
from .adaptive_model_selector import AdaptiveModelSelector

# Import du transcriber existant
try:
    from faster_whisper_transcriber import FasterWhisperTranscriber
    TRANSCRIBER_AVAILABLE = True
except ImportError:
    try:
        from src.faster_whisper_transcriber import FasterWhisperTranscriber
        TRANSCRIBER_AVAILABLE = True
    except ImportError:
        TRANSCRIBER_AVAILABLE = False
        logger.warning("FasterWhisperTranscriber non disponible")


class BatchTranscriber:
    """
    Transcrit l'audio par micro-batches de manière asynchrone
    Optimisé pour maintenir une latence faible et une mémoire constante
    """

    def __init__(
        self,
        model_name: str = "medium",
        language: str = "fr",
        device: str = "cpu",
        compute_type: str = "int8",
        sample_rate: int = 16000,
        on_transcription: Optional[Callable[[str, float, float], None]] = None,
        silence_threshold: float = 0.01,
        adaptive_model: bool = True,
        fallback_model: str = "small"
    ):
        """
        Initialise le transcriber par batch

        Args:
            model_name: Nom du modèle Whisper préféré
            language: Langue de transcription
            device: Device (cpu/cuda)
            compute_type: Type de calcul (int8/float16/float32)
            sample_rate: Fréquence d'échantillonnage
            on_transcription: Callback(text, start_time, end_time) pour chaque transcription
            silence_threshold: Seuil pour détecter le silence
            adaptive_model: Active la sélection adaptative du modèle selon la mémoire
            fallback_model: Modèle de repli si mémoire insuffisante
        """
        self.preferred_model_name = model_name
        self.fallback_model = fallback_model
        self.adaptive_model = adaptive_model
        self.language = language
        self.device = device
        self.compute_type = compute_type
        self.sample_rate = sample_rate
        self.on_transcription = on_transcription
        self.silence_threshold = silence_threshold

        # Sélecteur adaptatif
        self._model_selector: Optional[AdaptiveModelSelector] = None
        if adaptive_model:
            self._model_selector = AdaptiveModelSelector(
                preferred_model=model_name,
                fallback_model=fallback_model
            )

        # Nom du modèle effectif (déterminé au chargement)
        self.model_name = model_name

        # Transcriber Whisper (chargé à la demande)
        self._transcriber: Optional[FasterWhisperTranscriber] = None
        self._model_loaded = False

        # Queue pour traitement asynchrone
        self._queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._lock = threading.Lock()

        # Statistiques
        self._segments_processed = 0
        self._total_audio_duration = 0.0
        self._total_transcription_time = 0.0
        self._empty_segments = 0
        self._memory_errors = 0
        self._model_switches = 0

        # Session start time pour les timestamps
        self._session_start_time: Optional[float] = None

        logger.info(
            f"BatchTranscriber initialisé: préféré={model_name}, fallback={fallback_model}, "
            f"adaptatif={adaptive_model}, device={device}, compute={compute_type}"
        )

    def _load_model(self, model_name: Optional[str] = None) -> bool:
        """
        Charge le modèle Whisper si nécessaire
        Utilise la sélection adaptative si activée

        Args:
            model_name: Force un modèle spécifique (ignore la sélection adaptative)

        Returns:
            True si le modèle est chargé
        """
        if self._model_loaded:
            return True

        if not TRANSCRIBER_AVAILABLE:
            logger.error("FasterWhisperTranscriber non disponible")
            return False

        # Sélection adaptative du modèle si activée
        if model_name:
            selected_model = model_name
            selection_reason = "Modèle forcé"
        elif self._model_selector and self.adaptive_model:
            selected_model, selection_reason = self._model_selector.select_model()
            logger.info(f"Sélection adaptative: {selection_reason}")
        else:
            selected_model = self.model_name
            selection_reason = "Modèle par défaut"

        # Tentative de chargement avec fallback automatique
        return self._try_load_model(selected_model, selection_reason)

    def _try_load_model(self, model_name: str, reason: str = "") -> bool:
        """
        Tente de charger un modèle avec gestion des erreurs mémoire

        Args:
            model_name: Nom du modèle à charger
            reason: Raison de la sélection pour le log

        Returns:
            True si le modèle est chargé avec succès
        """
        try:
            logger.info(f"Chargement du modèle Whisper '{model_name}'... ({reason})")
            self._transcriber = FasterWhisperTranscriber(
                model_name=model_name,
                language=self.language,
                device=self.device,
                compute_type=self.compute_type
            )
            self._transcriber.load_model()
            self.model_name = model_name
            self._model_loaded = True
            logger.info(f"✓ Modèle Whisper '{model_name}' chargé avec succès")
            return True

        except (RuntimeError, MemoryError) as e:
            error_msg = str(e).lower()
            if "memory" in error_msg or "malloc" in error_msg or "alloc" in error_msg:
                logger.warning(f"Erreur mémoire lors du chargement de '{model_name}': {e}")
                self._memory_errors += 1

                # Tenter un fallback vers un modèle plus petit
                if self._model_selector:
                    fallback = self._model_selector.handle_memory_error()
                    if fallback and fallback != model_name:
                        self._model_switches += 1
                        logger.info(f"Tentative de fallback vers '{fallback}'...")
                        return self._try_load_model(fallback, "Fallback après erreur mémoire")

                logger.error("Impossible de charger un modèle - mémoire insuffisante")
                return False
            else:
                logger.error(f"Erreur chargement modèle: {e}", exc_info=True)
                return False

        except Exception as e:
            logger.error(f"Erreur chargement modèle: {e}", exc_info=True)
            return False

    def _reload_with_smaller_model(self) -> bool:
        """
        Recharge le transcriber avec un modèle plus petit après une erreur mémoire

        Returns:
            True si le rechargement a réussi
        """
        if not self._model_selector:
            return False

        # Libérer le modèle actuel
        self._transcriber = None
        self._model_loaded = False

        # Obtenir un modèle plus petit
        new_model = self._model_selector.handle_memory_error()
        if not new_model:
            return False

        self._model_switches += 1
        logger.info(f"Rechargement avec le modèle '{new_model}'...")

        return self._try_load_model(new_model, "Rechargement après erreur mémoire")

    def start(self) -> bool:
        """
        Démarre le worker de transcription

        Returns:
            True si démarré avec succès
        """
        with self._lock:
            if self._is_running:
                return True

            # Charger le modèle
            if not self._load_model():
                return False

            # Démarrer le worker thread
            self._is_running = True
            self._session_start_time = time.time()
            self._worker_thread = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name="BatchTranscriber-Worker"
            )
            self._worker_thread.start()

            logger.info("BatchTranscriber démarré")
            return True

    def stop(self) -> None:
        """Arrête le worker de transcription"""
        with self._lock:
            if not self._is_running:
                return

            self._is_running = False

            # Envoyer un signal de fin
            self._queue.put(None)

            # Attendre la fin du worker
            if self._worker_thread and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=5.0)

            logger.info(
                f"BatchTranscriber arrêté - {self._segments_processed} segments, "
                f"{self._total_audio_duration:.1f}s audio, "
                f"{self._total_transcription_time:.1f}s traitement"
            )

    def add_audio(self, audio_data: np.ndarray, timestamp: float) -> None:
        """
        Ajoute un segment audio à la queue de transcription

        Args:
            audio_data: Données audio numpy array
            timestamp: Timestamp du début du segment
        """
        if not self._is_running:
            logger.warning("BatchTranscriber non démarré, segment ignoré")
            return

        # Calculer la durée
        duration = len(audio_data) / self.sample_rate

        # Ajouter à la queue
        self._queue.put({
            "audio": audio_data,
            "timestamp": timestamp,
            "duration": duration
        })

    def _worker_loop(self) -> None:
        """Boucle principale du worker de transcription"""
        logger.debug("Worker de transcription démarré")

        while self._is_running:
            try:
                # Attendre un segment (avec timeout pour vérifier is_running)
                try:
                    item = self._queue.get(timeout=1.0)
                except queue.Empty:
                    continue

                # Signal de fin
                if item is None:
                    break

                # Traiter le segment
                self._process_segment(item)

            except Exception as e:
                logger.error(f"Erreur dans le worker: {e}", exc_info=True)

        logger.debug("Worker de transcription arrêté")

    def _process_segment(self, item: dict) -> None:
        """
        Traite un segment audio

        Args:
            item: Dictionnaire avec audio, timestamp, duration
        """
        audio = item["audio"]
        timestamp = item["timestamp"]
        duration = item["duration"]

        # Vérifier si c'est du silence
        energy = np.abs(audio).mean()
        if energy < self.silence_threshold:
            self._empty_segments += 1
            logger.debug(f"Segment silence ignoré (énergie: {energy:.6f})")
            # Appeler le callback avec une chaîne vide pour maintenir le timing
            if self.on_transcription:
                try:
                    self.on_transcription("", timestamp, timestamp + duration)
                except Exception as e:
                    logger.error(f"Erreur callback (silence): {e}")
            return

        # Transcrire
        start_time = time.time()
        try:
            text = self._transcriber.transcribe(audio, sample_rate=self.sample_rate)
            transcription_time = time.time() - start_time

            # Mise à jour des stats
            self._segments_processed += 1
            self._total_audio_duration += duration
            self._total_transcription_time += transcription_time

            # Log du résultat
            if text.strip():
                logger.info(
                    f"Segment #{self._segments_processed}: "
                    f"'{text[:50]}...' ({transcription_time:.2f}s pour {duration:.1f}s audio)"
                )
            else:
                self._empty_segments += 1
                logger.debug(f"Segment #{self._segments_processed}: vide")

            # Appeler le callback
            if self.on_transcription:
                try:
                    self.on_transcription(text, timestamp, timestamp + duration)
                except Exception as e:
                    logger.error(f"Erreur callback transcription: {e}")

        except (RuntimeError, MemoryError) as e:
            error_msg = str(e).lower()
            if "memory" in error_msg or "malloc" in error_msg or "alloc" in error_msg:
                logger.warning(f"Erreur mémoire pendant transcription: {e}")
                self._memory_errors += 1

                # Tenter de recharger avec un modèle plus petit
                if self._reload_with_smaller_model():
                    logger.info("Modèle rechargé, réessai du segment...")
                    # Remettre le segment dans la queue pour réessayer
                    self._queue.put(item)
                else:
                    logger.error("Impossible de continuer - mémoire insuffisante")
            else:
                logger.error(f"Erreur transcription segment: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Erreur transcription segment: {e}", exc_info=True)

    def get_stats(self) -> dict:
        """
        Retourne les statistiques de transcription

        Returns:
            Dictionnaire avec les statistiques
        """
        rtf = (
            self._total_transcription_time / self._total_audio_duration
            if self._total_audio_duration > 0 else 0
        )

        stats = {
            "segments_processed": self._segments_processed,
            "empty_segments": self._empty_segments,
            "total_audio_duration_seconds": self._total_audio_duration,
            "total_transcription_time_seconds": self._total_transcription_time,
            "real_time_factor": rtf,
            "queue_size": self._queue.qsize(),
            "model_loaded": self._model_loaded,
            "is_running": self._is_running,
            "current_model": self.model_name,
            "preferred_model": self.preferred_model_name,
            "adaptive_model_enabled": self.adaptive_model,
            "memory_errors": self._memory_errors,
            "model_switches": self._model_switches
        }

        # Ajouter les infos du sélecteur adaptatif si disponible
        if self._model_selector:
            stats["model_selector"] = self._model_selector.get_status()

        return stats

    def get_model_info(self) -> dict:
        """Retourne les informations sur le modèle"""
        if self._transcriber:
            return self._transcriber.get_model_info()
        return {
            "loaded": False,
            "model_name": self.model_name,
            "language": self.language
        }

    @property
    def is_running(self) -> bool:
        """Retourne True si le transcriber est actif"""
        return self._is_running

    @property
    def queue_size(self) -> int:
        """Retourne la taille de la queue"""
        return self._queue.qsize()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
