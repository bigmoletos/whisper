"""
Orchestrateur principal de session de réunion
Coordonne la capture audio, transcription, analyse et génération de rapport
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import uuid

from ..capture.system_audio_capture import SystemAudioCapture
from ..capture.audio_buffer import AudioBuffer
from ..transcription.batch_transcriber import BatchTranscriber
from ..transcription.transcript_storage import TranscriptStorage
from ..analysis.llm_analyzer import LLMAnalyzer
from ..analysis.intermediate_summarizer import IntermediateSummarizer
from ..analysis.final_synthesizer import FinalSynthesizer, MeetingReport
from .checkpoint_manager import CheckpointManager, SessionState

logger = logging.getLogger(__name__)


class MeetingSession:
    """
    Session de réunion complète
    Orchestre tous les composants pour une capture et analyse invisible
    """

    def __init__(
        self,
        config: Dict[str, Any],
        meeting_name: str = "Réunion",
        session_id: Optional[str] = None,
        on_status_change: Optional[Callable[[str, Dict], None]] = None
    ):
        """
        Initialise une session de réunion

        Args:
            config: Configuration complète (depuis config.json)
            meeting_name: Nom de la réunion
            session_id: ID de session (None = nouveau)
            on_status_change: Callback pour les changements d'état
        """
        self.config = config
        self.meeting_name = meeting_name
        self.session_id = session_id or self._generate_session_id()
        self.on_status_change = on_status_change

        # Configuration
        audio_config = config.get("audio", {})
        transcription_config = config.get("transcription", {})
        analysis_config = config.get("analysis", {})
        session_config = config.get("session", {})
        output_config = config.get("output", {})

        # Répertoires
        self.sessions_dir = Path(session_config.get("sessions_directory", "./meeting_sessions"))
        self.output_dir = Path(output_config.get("directory", "./meeting_reports"))
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Composants (initialisés à la demande)
        self._audio_capture: Optional[SystemAudioCapture] = None
        self._audio_buffer: Optional[AudioBuffer] = None
        self._transcriber: Optional[BatchTranscriber] = None
        self._transcript_storage: Optional[TranscriptStorage] = None
        self._llm_analyzer: Optional[LLMAnalyzer] = None
        self._summarizer: Optional[IntermediateSummarizer] = None
        self._synthesizer: Optional[FinalSynthesizer] = None
        self._checkpoint_manager: Optional[CheckpointManager] = None

        # État
        self._is_running = False
        self._is_paused = False
        self._start_time: Optional[float] = None
        self._lock = threading.Lock()

        # Thread de résumé intermédiaire
        self._summary_thread: Optional[threading.Thread] = None
        self._summary_stop_event = threading.Event()

        # Cache de config
        self._audio_config = audio_config
        self._transcription_config = transcription_config
        self._analysis_config = analysis_config
        self._session_config = session_config
        self._output_config = output_config

        logger.info(f"MeetingSession créée: {self.meeting_name} (ID: {self.session_id})")

    def _generate_session_id(self) -> str:
        """Génère un ID de session unique"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique = uuid.uuid4().hex[:6]
        return f"{timestamp}_{unique}"

    def _init_components(self) -> bool:
        """
        Initialise tous les composants

        Returns:
            True si tous les composants sont initialisés
        """
        try:
            # Checkpoint Manager
            self._checkpoint_manager = CheckpointManager(
                session_dir=self.sessions_dir,
                session_id=self.session_id,
                checkpoint_interval=self._session_config.get("checkpoint_interval_seconds", 60)
            )
            self._checkpoint_manager.initialize_session(self.meeting_name, self.config)

            # Transcript Storage
            self._transcript_storage = TranscriptStorage(
                session_dir=self.sessions_dir,
                session_id=self.session_id
            )

            # Batch Transcriber
            self._transcriber = BatchTranscriber(
                model_name=self._transcription_config.get("model", "medium"),
                language=self._transcription_config.get("language", "fr"),
                device=self._transcription_config.get("device", "cpu"),
                compute_type=self._transcription_config.get("compute_type", "int8"),
                sample_rate=self._audio_config.get("sample_rate", 16000),
                on_transcription=self._on_transcription,
                silence_threshold=self._audio_config.get("silence_threshold", 0.01)
            )

            # Audio Buffer
            self._audio_buffer = AudioBuffer(
                target_duration_seconds=self._audio_config.get("micro_batch_seconds", 10),
                sample_rate=self._audio_config.get("sample_rate", 16000),
                on_buffer_ready=self._on_buffer_ready,
                silence_threshold=self._audio_config.get("silence_threshold", 0.01)
            )

            # Audio Capture
            self._audio_capture = SystemAudioCapture(
                sample_rate=self._audio_config.get("sample_rate", 16000),
                channels=self._audio_config.get("channels", 1),
                on_audio_chunk=self._audio_buffer.add_chunk
            )

            # LLM Analyzer
            self._llm_analyzer = LLMAnalyzer(self.config)

            # Intermediate Summarizer
            self._summarizer = IntermediateSummarizer(
                llm_analyzer=self._llm_analyzer,
                session_dir=self.sessions_dir,
                session_id=self.session_id,
                interval_minutes=self._analysis_config.get("intermediate_summary_interval_minutes", 10),
                on_summary_ready=self._on_summary_ready
            )

            # Final Synthesizer
            self._synthesizer = FinalSynthesizer(
                llm_analyzer=self._llm_analyzer
            )

            logger.info("Tous les composants initialisés")
            return True

        except Exception as e:
            logger.error(f"Erreur initialisation composants: {e}", exc_info=True)
            return False

    def start(self) -> bool:
        """
        Démarre la session de réunion

        Returns:
            True si démarrée avec succès
        """
        with self._lock:
            if self._is_running:
                logger.warning("Session déjà en cours")
                return True

            # Initialiser les composants
            if not self._init_components():
                return False

            # Démarrer les composants
            try:
                # Transcriber (charge le modèle)
                if not self._transcriber.start():
                    logger.error("Échec démarrage transcriber")
                    return False

                # Capture audio
                if not self._audio_capture.start():
                    logger.error("Échec démarrage capture audio")
                    self._transcriber.stop()
                    return False

                # Checkpoint auto-save
                self._checkpoint_manager.start_auto_checkpoint()
                self._checkpoint_manager.update_state(SessionState.RUNNING)

                # Thread de résumé périodique
                self._summary_stop_event.clear()
                self._summary_thread = threading.Thread(
                    target=self._summary_loop,
                    daemon=True,
                    name="MeetingSession-SummaryLoop"
                )
                self._summary_thread.start()

                self._is_running = True
                self._start_time = time.time()

                self._notify_status("started", {"session_id": self.session_id})
                logger.info(f"Session démarrée: {self.meeting_name}")

                return True

            except Exception as e:
                logger.error(f"Erreur démarrage session: {e}", exc_info=True)
                self._cleanup()
                return False

    def stop(self) -> Optional[MeetingReport]:
        """
        Arrête la session et génère le rapport final

        Returns:
            MeetingReport ou None si erreur
        """
        with self._lock:
            if not self._is_running:
                logger.warning("Session non en cours")
                return None

            logger.info("Arrêt de la session en cours...")
            self._notify_status("stopping", {})

            # Arrêter la capture
            if self._audio_capture:
                self._audio_capture.stop()

            # Vider le buffer restant
            if self._audio_buffer:
                self._audio_buffer.flush()

            # Arrêter le thread de résumé
            self._summary_stop_event.set()
            if self._summary_thread and self._summary_thread.is_alive():
                self._summary_thread.join(timeout=5.0)

            # Attendre que la queue de transcription se vide
            if self._transcriber:
                logger.info("Attente fin des transcriptions...")
                timeout = 30.0
                start = time.time()
                while self._transcriber.queue_size > 0 and (time.time() - start) < timeout:
                    time.sleep(0.5)
                self._transcriber.stop()

            # Finaliser le stockage
            if self._transcript_storage:
                self._transcript_storage.finalize()

            self._is_running = False

            # Générer le rapport final
            report = self._generate_final_report()

            # Finaliser le checkpoint
            if self._checkpoint_manager:
                self._checkpoint_manager.finalize(success=True)

            self._notify_status("stopped", {"report_generated": report is not None})
            logger.info("Session arrêtée")

            return report

    def pause(self) -> None:
        """Met la session en pause"""
        with self._lock:
            if not self._is_running or self._is_paused:
                return

            if self._audio_capture:
                self._audio_capture.pause()

            self._is_paused = True

            if self._checkpoint_manager:
                self._checkpoint_manager.update_state(SessionState.PAUSED)

            self._notify_status("paused", {})
            logger.info("Session mise en pause")

    def resume(self) -> None:
        """Reprend la session après une pause"""
        with self._lock:
            if not self._is_running or not self._is_paused:
                return

            if self._audio_capture:
                self._audio_capture.resume()

            self._is_paused = False

            if self._checkpoint_manager:
                self._checkpoint_manager.update_state(SessionState.RUNNING)

            self._notify_status("resumed", {})
            logger.info("Session reprise")

    def _on_buffer_ready(self, audio_data, timestamp: float) -> None:
        """
        Callback quand un buffer audio est prêt

        Args:
            audio_data: Données audio
            timestamp: Timestamp du buffer
        """
        if self._transcriber and self._is_running and not self._is_paused:
            # Calculer le timestamp relatif au début de la session
            relative_time = timestamp - self._start_time if self._start_time else 0
            self._transcriber.add_audio(audio_data, relative_time)

    def _on_transcription(self, text: str, start_time: float, end_time: float) -> None:
        """
        Callback pour chaque transcription

        Args:
            text: Texte transcrit
            start_time: Temps de début
            end_time: Temps de fin
        """
        if self._transcript_storage:
            self._transcript_storage.add_segment(text, start_time, end_time)

        # Mettre à jour les stats
        if self._checkpoint_manager:
            self._checkpoint_manager.update_stats(
                total_audio_duration=end_time,
                segments_transcribed=self._transcript_storage.segment_count if self._transcript_storage else 0
            )

    def _on_summary_ready(self, summary) -> None:
        """
        Callback quand un résumé intermédiaire est prêt

        Args:
            summary: IntermediateSummary
        """
        self._notify_status("summary_generated", {
            "chunk_index": summary.chunk_index,
            "time_range": summary.format_time_range(),
            "key_points_count": len(summary.key_points)
        })

        if self._checkpoint_manager:
            self._checkpoint_manager.update_stats(
                summaries_generated=self._summarizer.get_summary_count() if self._summarizer else 0
            )

    def _summary_loop(self) -> None:
        """Boucle de génération des résumés intermédiaires"""
        check_interval = 30.0  # Vérifier toutes les 30 secondes

        while not self._summary_stop_event.is_set():
            self._summary_stop_event.wait(check_interval)

            if self._summary_stop_event.is_set():
                break

            if not self._is_running or self._is_paused:
                continue

            # Vérifier si un résumé est nécessaire
            if self._transcript_storage and self._summarizer:
                current_time = self._transcript_storage.total_duration
                if self._summarizer.should_summarize(current_time):
                    # Récupérer le texte des dernières N minutes
                    interval = self._analysis_config.get("intermediate_summary_interval_minutes", 10)
                    text = self._transcript_storage.get_text_since(interval)

                    if text.strip():
                        start_time = max(0, current_time - interval * 60)
                        self._summarizer.generate_summary(text, start_time, current_time)

    def _generate_final_report(self) -> Optional[MeetingReport]:
        """
        Génère le rapport final

        Returns:
            MeetingReport ou None
        """
        if not self._synthesizer:
            return None

        logger.info("Génération du rapport final...")
        self._notify_status("generating_report", {})

        try:
            # Récupérer tous les résumés intermédiaires
            summaries = self._summarizer.get_all_summaries() if self._summarizer else []

            # Calculer la durée
            duration = self._transcript_storage.total_duration if self._transcript_storage else 0
            duration_str = self._format_duration(duration)

            # Date
            date_str = datetime.now().strftime("%d/%m/%Y %H:%M")

            # Générer le rapport
            if summaries:
                report = self._synthesizer.synthesize(
                    summaries=summaries,
                    meeting_title=self.meeting_name,
                    meeting_date=date_str,
                    meeting_duration=duration_str
                )
            else:
                # Fallback: synthèse directe depuis le texte
                full_text = self._transcript_storage.get_all_text() if self._transcript_storage else ""
                report = self._synthesizer.quick_synthesis_from_text(
                    full_transcript=full_text,
                    meeting_title=self.meeting_name,
                    meeting_date=date_str,
                    meeting_duration=duration_str
                )

            # Sauvegarder le rapport
            self._save_report(report)

            logger.info(f"Rapport généré en {report.generation_time:.2f}s")
            return report

        except Exception as e:
            logger.error(f"Erreur génération rapport: {e}", exc_info=True)
            return None

    def _save_report(self, report: MeetingReport) -> None:
        """Sauvegarde le rapport en JSON"""
        report_file = self.sessions_dir / self.session_id / "final_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

    def _format_duration(self, seconds: float) -> str:
        """Formate une durée en HH:MM:SS"""
        total = int(seconds)
        hours = total // 3600
        minutes = (total % 3600) // 60
        secs = total % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def _notify_status(self, status: str, data: Dict) -> None:
        """Notifie un changement de statut"""
        if self.on_status_change:
            try:
                self.on_status_change(status, data)
            except Exception as e:
                logger.error(f"Erreur callback status: {e}")

    def _cleanup(self) -> None:
        """Nettoie les ressources"""
        if self._audio_capture:
            self._audio_capture.stop()
        if self._transcriber:
            self._transcriber.stop()
        if self._checkpoint_manager:
            self._checkpoint_manager.stop_auto_checkpoint()

    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut actuel de la session

        Returns:
            Dictionnaire avec le statut complet
        """
        status = {
            "session_id": self.session_id,
            "meeting_name": self.meeting_name,
            "is_running": self._is_running,
            "is_paused": self._is_paused,
            "elapsed_time": time.time() - self._start_time if self._start_time else 0,
            "elapsed_time_formatted": self._format_duration(
                time.time() - self._start_time if self._start_time else 0
            )
        }

        if self._transcript_storage:
            status["transcript"] = self._transcript_storage.get_stats()

        if self._transcriber:
            status["transcriber"] = self._transcriber.get_stats()

        if self._summarizer:
            status["summarizer"] = self._summarizer.get_stats()

        if self._audio_buffer:
            status["buffer"] = self._audio_buffer.get_stats()

        if self._llm_analyzer:
            status["llm_backends"] = self._llm_analyzer.get_available_backends()

        return status

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
