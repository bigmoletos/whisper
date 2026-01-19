"""
Génération de résumés intermédiaires toutes les N minutes
Permet de réduire la latence finale en pré-synthétisant par chunks
"""

import json
import logging
import threading
import time
from pathlib import Path
from typing import Optional, List, Callable
from datetime import datetime

from .llm_analyzer import LLMAnalyzer, LLMResponse, SYSTEM_PROMPTS

logger = logging.getLogger(__name__)


class IntermediateSummary:
    """Représente un résumé intermédiaire"""

    def __init__(
        self,
        chunk_index: int,
        start_time: float,
        end_time: float,
        summary: str,
        key_points: List[str],
        actions: List[dict]
    ):
        self.chunk_index = chunk_index
        self.start_time = start_time
        self.end_time = end_time
        self.summary = summary
        self.key_points = key_points
        self.actions = actions
        self.created_at = time.time()

    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            "chunk_index": self.chunk_index,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "summary": self.summary,
            "key_points": self.key_points,
            "actions": self.actions,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IntermediateSummary":
        """Crée depuis un dictionnaire"""
        summary = cls(
            chunk_index=data["chunk_index"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            summary=data["summary"],
            key_points=data.get("key_points", []),
            actions=data.get("actions", [])
        )
        summary.created_at = data.get("created_at", time.time())
        return summary

    def format_time_range(self) -> str:
        """Formate la plage temporelle"""
        def format_seconds(s):
            total = int(s)
            hours = total // 3600
            minutes = (total % 3600) // 60
            secs = total % 60
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"

        return f"{format_seconds(self.start_time)} - {format_seconds(self.end_time)}"


class IntermediateSummarizer:
    """
    Génère des résumés intermédiaires à intervalles réguliers
    Permet de pré-traiter la réunion pour une synthèse finale rapide
    """

    def __init__(
        self,
        llm_analyzer: LLMAnalyzer,
        session_dir: Path,
        session_id: str,
        interval_minutes: float = 10.0,
        on_summary_ready: Optional[Callable[[IntermediateSummary], None]] = None
    ):
        """
        Initialise le summarizer intermédiaire

        Args:
            llm_analyzer: Instance de LLMAnalyzer
            session_dir: Répertoire de session
            session_id: ID de session
            interval_minutes: Intervalle entre les résumés
            on_summary_ready: Callback appelé quand un résumé est prêt
        """
        self.llm = llm_analyzer
        self.session_dir = Path(session_dir)
        self.session_id = session_id
        self.interval_seconds = interval_minutes * 60
        self.on_summary_ready = on_summary_ready

        # Répertoire des résumés
        self.summaries_dir = self.session_dir / session_id / "summaries"
        self.summaries_dir.mkdir(parents=True, exist_ok=True)

        # État
        self._summaries: List[IntermediateSummary] = []
        self._current_chunk_index = 0
        self._last_summary_time = 0.0
        self._lock = threading.Lock()

        # Charger les résumés existants (pour recovery)
        self._load_existing_summaries()

        logger.info(
            f"IntermediateSummarizer initialisé: intervalle={interval_minutes}min, "
            f"{len(self._summaries)} résumés existants"
        )

    def _load_existing_summaries(self) -> None:
        """Charge les résumés existants depuis le disque"""
        summary_files = sorted(self.summaries_dir.glob("chunk_*.json"))
        for f in summary_files:
            try:
                with open(f, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    summary = IntermediateSummary.from_dict(data)
                    self._summaries.append(summary)
                    self._current_chunk_index = max(
                        self._current_chunk_index,
                        summary.chunk_index + 1
                    )
                    self._last_summary_time = max(
                        self._last_summary_time,
                        summary.end_time
                    )
            except Exception as e:
                logger.warning(f"Erreur chargement résumé {f}: {e}")

    def should_summarize(self, current_time: float) -> bool:
        """
        Vérifie s'il est temps de générer un résumé

        Args:
            current_time: Temps actuel de la réunion en secondes

        Returns:
            True s'il faut générer un résumé
        """
        time_since_last = current_time - self._last_summary_time
        return time_since_last >= self.interval_seconds

    def generate_summary(
        self,
        text: str,
        start_time: float,
        end_time: float
    ) -> Optional[IntermediateSummary]:
        """
        Génère un résumé intermédiaire pour un chunk de texte

        Args:
            text: Texte à résumer
            start_time: Temps de début du chunk
            end_time: Temps de fin du chunk

        Returns:
            IntermediateSummary ou None si échec
        """
        if not text.strip():
            logger.debug("Texte vide, pas de résumé généré")
            return None

        with self._lock:
            chunk_index = self._current_chunk_index

            logger.info(f"Génération résumé chunk #{chunk_index}...")

            # Construire le prompt
            prompt = f"""Voici un extrait de transcription d'une réunion (minutes {int(start_time/60)} à {int(end_time/60)}):

---
{text}
---

Génère un résumé structuré de cet extrait avec:
1. RÉSUMÉ: Un paragraphe résumant les points principaux
2. POINTS CLÉS: Liste des points importants (maximum 5)
3. ACTIONS: Actions identifiées avec responsable si mentionné

Format ta réponse exactement comme suit:
RÉSUMÉ:
[ton résumé ici]

POINTS CLÉS:
- [point 1]
- [point 2]
...

ACTIONS:
- [action 1] | Responsable: [nom ou N/A] | Deadline: [date ou N/A]
- [action 2] | Responsable: [nom ou N/A] | Deadline: [date ou N/A]
..."""

            # Appeler le LLM
            response = self.llm.analyze(
                prompt,
                system_prompt=SYSTEM_PROMPTS["intermediate_summary"]
            )

            if not response.success:
                logger.error(f"Erreur génération résumé: {response.error}")
                return None

            # Parser la réponse
            summary_text, key_points, actions = self._parse_response(response.text)

            # Créer le résumé
            summary = IntermediateSummary(
                chunk_index=chunk_index,
                start_time=start_time,
                end_time=end_time,
                summary=summary_text,
                key_points=key_points,
                actions=actions
            )

            # Sauvegarder
            self._save_summary(summary)
            self._summaries.append(summary)
            self._current_chunk_index += 1
            self._last_summary_time = end_time

            logger.info(
                f"Résumé chunk #{chunk_index} généré: "
                f"{len(key_points)} points clés, {len(actions)} actions"
            )

            # Callback
            if self.on_summary_ready:
                try:
                    self.on_summary_ready(summary)
                except Exception as e:
                    logger.error(f"Erreur callback résumé: {e}")

            return summary

    def _parse_response(self, response_text: str) -> tuple:
        """
        Parse la réponse du LLM

        Args:
            response_text: Texte brut de la réponse

        Returns:
            Tuple (summary, key_points, actions)
        """
        summary = ""
        key_points = []
        actions = []

        current_section = None
        lines = response_text.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Détecter les sections
            if line.upper().startswith("RÉSUMÉ") or line.upper().startswith("RESUME"):
                current_section = "summary"
                # Le résumé peut être sur la même ligne après ":"
                if ":" in line:
                    summary = line.split(":", 1)[1].strip()
                continue
            elif line.upper().startswith("POINTS CLÉS") or line.upper().startswith("POINTS CLES"):
                current_section = "points"
                continue
            elif line.upper().startswith("ACTIONS"):
                current_section = "actions"
                continue

            # Traiter selon la section
            if current_section == "summary":
                summary += " " + line if summary else line
            elif current_section == "points":
                if line.startswith("-") or line.startswith("•"):
                    point = line.lstrip("-•").strip()
                    if point:
                        key_points.append(point)
            elif current_section == "actions":
                if line.startswith("-") or line.startswith("•"):
                    action_data = self._parse_action(line)
                    if action_data:
                        actions.append(action_data)

        return summary.strip(), key_points, actions

    def _parse_action(self, line: str) -> Optional[dict]:
        """
        Parse une ligne d'action

        Args:
            line: Ligne au format "- [action] | Responsable: X | Deadline: Y"

        Returns:
            Dictionnaire avec action, assignee, deadline
        """
        line = line.lstrip("-•").strip()
        if not line:
            return None

        parts = line.split("|")
        action = parts[0].strip()
        assignee = None
        deadline = None

        for part in parts[1:]:
            part = part.strip()
            if part.lower().startswith("responsable"):
                assignee = part.split(":", 1)[1].strip() if ":" in part else None
                if assignee and assignee.upper() in ["N/A", "NA", "NON SPÉCIFIÉ", "-"]:
                    assignee = None
            elif part.lower().startswith("deadline") or part.lower().startswith("échéance"):
                deadline = part.split(":", 1)[1].strip() if ":" in part else None
                if deadline and deadline.upper() in ["N/A", "NA", "NON SPÉCIFIÉ", "-"]:
                    deadline = None

        return {
            "action": action,
            "assignee": assignee,
            "deadline": deadline
        }

    def _save_summary(self, summary: IntermediateSummary) -> None:
        """Sauvegarde un résumé sur disque"""
        filename = f"chunk_{summary.chunk_index:04d}.json"
        filepath = self.summaries_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, indent=2, ensure_ascii=False)

    def get_all_summaries(self) -> List[IntermediateSummary]:
        """Retourne tous les résumés générés"""
        with self._lock:
            return self._summaries.copy()

    def get_summary_count(self) -> int:
        """Retourne le nombre de résumés"""
        return len(self._summaries)

    def get_all_actions(self) -> List[dict]:
        """Retourne toutes les actions identifiées"""
        actions = []
        for summary in self._summaries:
            actions.extend(summary.actions)
        return actions

    def get_all_key_points(self) -> List[str]:
        """Retourne tous les points clés"""
        points = []
        for summary in self._summaries:
            points.extend(summary.key_points)
        return points

    def get_stats(self) -> dict:
        """Retourne les statistiques"""
        total_actions = sum(len(s.actions) for s in self._summaries)
        total_points = sum(len(s.key_points) for s in self._summaries)

        return {
            "summary_count": len(self._summaries),
            "total_actions": total_actions,
            "total_key_points": total_points,
            "last_summary_time": self._last_summary_time,
            "interval_minutes": self.interval_seconds / 60
        }
