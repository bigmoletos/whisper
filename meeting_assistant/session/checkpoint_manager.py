"""
Gestionnaire de checkpoints pour sauvegarde et récupération d'état
Permet de reprendre une session après un crash ou une interruption
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class SessionState(Enum):
    """États possibles d'une session"""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    CRASHED = "crashed"
    COMPLETED = "completed"


class CheckpointManager:
    """
    Gère les checkpoints de session pour la récupération après crash
    Sauvegarde périodiquement l'état de la session
    """

    def __init__(
        self,
        session_dir: Path,
        session_id: str,
        checkpoint_interval: float = 60.0
    ):
        """
        Initialise le gestionnaire de checkpoints

        Args:
            session_dir: Répertoire de base des sessions
            session_id: ID unique de la session
            checkpoint_interval: Intervalle entre les checkpoints en secondes
        """
        self.session_dir = Path(session_dir)
        self.session_id = session_id
        self.checkpoint_interval = checkpoint_interval

        # Répertoire de la session
        self.session_path = self.session_dir / session_id
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Fichiers
        self.state_file = self.session_path / "session_state.json"
        self.checkpoint_file = self.session_path / "checkpoint.json"

        # État interne
        self._state = SessionState.CREATED
        self._session_data: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._checkpoint_thread: Optional[threading.Thread] = None
        self._is_running = False

        # Timestamps
        self._start_time: Optional[float] = None
        self._last_checkpoint_time: Optional[float] = None

        logger.info(f"CheckpointManager initialisé: {self.session_path}")

    def initialize_session(
        self,
        meeting_name: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Initialise une nouvelle session

        Args:
            meeting_name: Nom de la réunion
            config: Configuration de la session

        Returns:
            Données de session initialisées
        """
        with self._lock:
            self._start_time = time.time()
            self._state = SessionState.CREATED

            self._session_data = {
                "session_id": self.session_id,
                "meeting_name": meeting_name,
                "created_at": datetime.now().isoformat(),
                "start_time": self._start_time,
                "state": self._state.value,
                "config": config,
                "stats": {
                    "total_audio_duration": 0.0,
                    "segments_transcribed": 0,
                    "summaries_generated": 0,
                    "last_activity_time": self._start_time
                }
            }

            self._save_state()
            logger.info(f"Session initialisée: {meeting_name}")

            return self._session_data.copy()

    def load_session(self) -> Optional[Dict[str, Any]]:
        """
        Charge une session existante depuis le disque

        Returns:
            Données de session ou None si non trouvée
        """
        if not self.state_file.exists():
            logger.warning(f"Fichier d'état non trouvé: {self.state_file}")
            return None

        with self._lock:
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self._session_data = json.load(f)

                self._state = SessionState(self._session_data.get("state", "created"))
                self._start_time = self._session_data.get("start_time")

                # Si la session était en cours, elle a crashé
                if self._state == SessionState.RUNNING:
                    self._state = SessionState.CRASHED
                    self._session_data["state"] = self._state.value
                    self._save_state()
                    logger.warning("Session précédente détectée comme crashée")

                logger.info(f"Session chargée: {self._session_data.get('meeting_name')}")
                return self._session_data.copy()

            except Exception as e:
                logger.error(f"Erreur chargement session: {e}")
                return None

    def update_state(self, new_state: SessionState) -> None:
        """
        Met à jour l'état de la session

        Args:
            new_state: Nouvel état
        """
        with self._lock:
            self._state = new_state
            self._session_data["state"] = new_state.value
            self._session_data["stats"]["last_activity_time"] = time.time()
            self._save_state()
            logger.debug(f"État mis à jour: {new_state.value}")

    def update_stats(self, **kwargs) -> None:
        """
        Met à jour les statistiques de session

        Args:
            **kwargs: Statistiques à mettre à jour
        """
        with self._lock:
            for key, value in kwargs.items():
                if key in self._session_data["stats"]:
                    self._session_data["stats"][key] = value
                else:
                    self._session_data["stats"][key] = value

            self._session_data["stats"]["last_activity_time"] = time.time()

    def save_checkpoint(self, checkpoint_data: Dict[str, Any]) -> None:
        """
        Sauvegarde un checkpoint complet

        Args:
            checkpoint_data: Données à sauvegarder
        """
        with self._lock:
            checkpoint = {
                "timestamp": time.time(),
                "session_id": self.session_id,
                "data": checkpoint_data
            }

            with open(self.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, indent=2, ensure_ascii=False)

            self._last_checkpoint_time = time.time()
            self._save_state()

            logger.debug("Checkpoint sauvegardé")

    def load_checkpoint(self) -> Optional[Dict[str, Any]]:
        """
        Charge le dernier checkpoint

        Returns:
            Données du checkpoint ou None
        """
        if not self.checkpoint_file.exists():
            return None

        try:
            with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                checkpoint = json.load(f)
                return checkpoint.get("data")
        except Exception as e:
            logger.error(f"Erreur chargement checkpoint: {e}")
            return None

    def _save_state(self) -> None:
        """Sauvegarde l'état courant sur disque"""
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self._session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde état: {e}")

    def start_auto_checkpoint(self) -> None:
        """Démarre la sauvegarde automatique des checkpoints"""
        if self._is_running:
            return

        self._is_running = True
        self._checkpoint_thread = threading.Thread(
            target=self._checkpoint_loop,
            daemon=True,
            name="CheckpointManager-AutoSave"
        )
        self._checkpoint_thread.start()
        logger.info(f"Auto-checkpoint démarré (intervalle: {self.checkpoint_interval}s)")

    def stop_auto_checkpoint(self) -> None:
        """Arrête la sauvegarde automatique"""
        self._is_running = False
        if self._checkpoint_thread and self._checkpoint_thread.is_alive():
            self._checkpoint_thread.join(timeout=2.0)
        logger.info("Auto-checkpoint arrêté")

    def _checkpoint_loop(self) -> None:
        """Boucle de sauvegarde automatique"""
        while self._is_running:
            time.sleep(self.checkpoint_interval)
            if self._is_running:
                with self._lock:
                    self._save_state()

    def finalize(self, success: bool = True) -> None:
        """
        Finalise la session

        Args:
            success: True si la session s'est terminée normalement
        """
        self.stop_auto_checkpoint()

        with self._lock:
            self._state = SessionState.COMPLETED if success else SessionState.STOPPED
            self._session_data["state"] = self._state.value
            self._session_data["end_time"] = time.time()

            if self._start_time:
                duration = time.time() - self._start_time
                self._session_data["total_duration"] = duration

            self._save_state()
            logger.info(f"Session finalisée: {self._state.value}")

    def get_session_info(self) -> Dict[str, Any]:
        """Retourne les informations de session"""
        with self._lock:
            info = self._session_data.copy()

            # Ajouter la durée écoulée
            if self._start_time:
                info["elapsed_time"] = time.time() - self._start_time

            return info

    def get_recoverable_sessions(self) -> list:
        """
        Liste les sessions récupérables

        Returns:
            Liste des sessions avec état CRASHED ou PAUSED
        """
        sessions = []

        if not self.session_dir.exists():
            return sessions

        for session_path in self.session_dir.iterdir():
            if session_path.is_dir():
                state_file = session_path / "session_state.json"
                if state_file.exists():
                    try:
                        with open(state_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            state = data.get("state", "")
                            if state in [SessionState.CRASHED.value, SessionState.PAUSED.value]:
                                sessions.append({
                                    "session_id": data.get("session_id"),
                                    "meeting_name": data.get("meeting_name"),
                                    "created_at": data.get("created_at"),
                                    "state": state,
                                    "stats": data.get("stats", {})
                                })
                    except Exception:
                        pass

        return sessions

    @property
    def state(self) -> SessionState:
        """État actuel de la session"""
        return self._state

    @property
    def elapsed_time(self) -> float:
        """Temps écoulé depuis le début de la session"""
        if self._start_time:
            return time.time() - self._start_time
        return 0.0
