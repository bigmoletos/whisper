"""
Synthèse finale rapide à partir des résumés intermédiaires
Conçu pour générer un rapport complet en moins de 30 secondes
"""

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from .llm_analyzer import LLMAnalyzer, SYSTEM_PROMPTS
from .intermediate_summarizer import IntermediateSummary

logger = logging.getLogger(__name__)


@dataclass
class MeetingReport:
    """Rapport final de réunion"""
    title: str
    date: str
    duration: str
    participants: str = "Non spécifié"

    executive_summary: str = ""
    key_points: List[str] = field(default_factory=list)
    highlights: List[Dict[str, str]] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)

    # Métadonnées
    generation_time: float = 0.0
    llm_backend: str = ""
    total_tokens: int = 0

    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            "title": self.title,
            "date": self.date,
            "duration": self.duration,
            "participants": self.participants,
            "executive_summary": self.executive_summary,
            "key_points": self.key_points,
            "highlights": self.highlights,
            "action_items": self.action_items,
            "decisions": self.decisions,
            "metadata": {
                "generation_time": self.generation_time,
                "llm_backend": self.llm_backend,
                "total_tokens": self.total_tokens
            }
        }


class FinalSynthesizer:
    """
    Synthétiseur final pour générer le rapport de réunion
    Utilise les résumés intermédiaires pour une génération rapide
    """

    def __init__(
        self,
        llm_analyzer: LLMAnalyzer,
        max_synthesis_time: float = 30.0
    ):
        """
        Initialise le synthétiseur

        Args:
            llm_analyzer: Instance de LLMAnalyzer
            max_synthesis_time: Temps max en secondes pour la synthèse
        """
        self.llm = llm_analyzer
        self.max_time = max_synthesis_time

        logger.info(f"FinalSynthesizer initialisé (max {max_synthesis_time}s)")

    def synthesize(
        self,
        summaries: List[IntermediateSummary],
        meeting_title: str,
        meeting_date: str,
        meeting_duration: str,
        participants: str = "Non spécifié"
    ) -> MeetingReport:
        """
        Génère le rapport final à partir des résumés intermédiaires

        Args:
            summaries: Liste des résumés intermédiaires
            meeting_title: Titre de la réunion
            meeting_date: Date de la réunion
            meeting_duration: Durée formatée
            participants: Liste des participants

        Returns:
            MeetingReport complet
        """
        start_time = time.time()

        logger.info(f"Début synthèse finale: {len(summaries)} résumés à traiter")

        # Créer le rapport de base
        report = MeetingReport(
            title=meeting_title,
            date=meeting_date,
            duration=meeting_duration,
            participants=participants
        )

        if not summaries:
            report.executive_summary = "Aucun contenu à synthétiser."
            report.generation_time = time.time() - start_time
            return report

        # Collecter les données des résumés intermédiaires
        all_summaries_text = []
        all_key_points = []
        all_actions = []

        for s in summaries:
            all_summaries_text.append(f"[{s.format_time_range()}]\n{s.summary}")
            all_key_points.extend(s.key_points)
            all_actions.extend(s.actions)

        # Construire le prompt de synthèse
        summaries_combined = "\n\n".join(all_summaries_text)

        prompt = f"""Voici les résumés intermédiaires d'une réunion intitulée "{meeting_title}":

{summaries_combined}

---

Points clés identifiés précédemment:
{self._format_list(all_key_points)}

Actions identifiées:
{self._format_actions(all_actions)}

---

Génère un rapport de synthèse final avec les sections suivantes:

1. RÉSUMÉ EXÉCUTIF: 2-3 phrases qui capturent l'essence de la réunion

2. POINTS CLÉS: Les 5-7 points les plus importants (consolidés et dédupliqués)

3. HIGHLIGHTS: 2-4 moments ou discussions importants avec contexte

4. DÉCISIONS: Liste des décisions prises pendant la réunion

5. ACTIONS: Liste consolidée des actions avec responsables et deadlines

Format ta réponse exactement comme suit:

RÉSUMÉ EXÉCUTIF:
[2-3 phrases]

POINTS CLÉS:
- [point 1]
- [point 2]
...

HIGHLIGHTS:
### [Sujet 1]
[Description du highlight]

### [Sujet 2]
[Description du highlight]

DÉCISIONS:
- [décision 1]
- [décision 2]
...

ACTIONS:
- [action] | Responsable: [nom] | Deadline: [date]
..."""

        # Appeler le LLM
        response = self.llm.analyze(
            prompt,
            system_prompt=SYSTEM_PROMPTS["final_synthesis"]
        )

        if response.success:
            # Parser la réponse
            self._parse_synthesis_response(response.text, report)
            report.llm_backend = response.backend
            report.total_tokens = response.tokens_used
        else:
            logger.error(f"Erreur synthèse: {response.error}")
            # Fallback: utiliser les données brutes
            report.executive_summary = "Erreur lors de la synthèse automatique."
            report.key_points = all_key_points[:7]
            report.action_items = all_actions

        report.generation_time = time.time() - start_time

        logger.info(
            f"Synthèse terminée en {report.generation_time:.2f}s: "
            f"{len(report.key_points)} points, {len(report.action_items)} actions"
        )

        return report

    def _format_list(self, items: List[str]) -> str:
        """Formate une liste en texte"""
        if not items:
            return "Aucun"
        return "\n".join(f"- {item}" for item in items)

    def _format_actions(self, actions: List[dict]) -> str:
        """Formate les actions en texte"""
        if not actions:
            return "Aucune action identifiée"

        lines = []
        for a in actions:
            line = f"- {a.get('action', 'N/A')}"
            if a.get('assignee'):
                line += f" | {a['assignee']}"
            if a.get('deadline'):
                line += f" | {a['deadline']}"
            lines.append(line)
        return "\n".join(lines)

    def _parse_synthesis_response(self, text: str, report: MeetingReport) -> None:
        """
        Parse la réponse de synthèse du LLM

        Args:
            text: Texte brut de la réponse
            report: Rapport à remplir
        """
        current_section = None
        current_highlight = None
        lines = text.strip().split("\n")

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Détecter les sections
            line_upper = line_stripped.upper()
            if line_upper.startswith("RÉSUMÉ EXÉCUTIF") or line_upper.startswith("RESUME EXECUTIF"):
                current_section = "executive"
                if ":" in line_stripped:
                    content = line_stripped.split(":", 1)[1].strip()
                    if content:
                        report.executive_summary = content
                continue
            elif line_upper.startswith("POINTS CLÉS") or line_upper.startswith("POINTS CLES"):
                current_section = "points"
                continue
            elif line_upper.startswith("HIGHLIGHTS"):
                current_section = "highlights"
                continue
            elif line_upper.startswith("DÉCISIONS") or line_upper.startswith("DECISIONS"):
                current_section = "decisions"
                continue
            elif line_upper.startswith("ACTIONS"):
                current_section = "actions"
                continue

            # Traiter selon la section
            if current_section == "executive":
                if report.executive_summary:
                    report.executive_summary += " " + line_stripped
                else:
                    report.executive_summary = line_stripped

            elif current_section == "points":
                if line_stripped.startswith("-") or line_stripped.startswith("•"):
                    point = line_stripped.lstrip("-•").strip()
                    if point:
                        report.key_points.append(point)

            elif current_section == "highlights":
                if line_stripped.startswith("###"):
                    # Nouveau highlight
                    if current_highlight and current_highlight.get("content"):
                        report.highlights.append(current_highlight)
                    topic = line_stripped.lstrip("#").strip()
                    current_highlight = {"topic": topic, "content": ""}
                elif current_highlight is not None:
                    if current_highlight["content"]:
                        current_highlight["content"] += " " + line_stripped
                    else:
                        current_highlight["content"] = line_stripped

            elif current_section == "decisions":
                if line_stripped.startswith("-") or line_stripped.startswith("•"):
                    decision = line_stripped.lstrip("-•").strip()
                    if decision:
                        report.decisions.append(decision)

            elif current_section == "actions":
                if line_stripped.startswith("-") or line_stripped.startswith("•"):
                    action = self._parse_action_line(line_stripped)
                    if action:
                        report.action_items.append(action)

        # Ajouter le dernier highlight si présent
        if current_highlight and current_highlight.get("content"):
            report.highlights.append(current_highlight)

    def _parse_action_line(self, line: str) -> Optional[dict]:
        """Parse une ligne d'action"""
        line = line.lstrip("-•").strip()
        if not line:
            return None

        parts = line.split("|")
        action = parts[0].strip()
        assignee = None
        deadline = None

        for part in parts[1:]:
            part = part.strip()
            part_lower = part.lower()
            if part_lower.startswith("responsable") or part_lower.startswith("assigné"):
                value = part.split(":", 1)[1].strip() if ":" in part else part
                if value and value.upper() not in ["N/A", "NA", "-", "NON SPÉCIFIÉ"]:
                    assignee = value
            elif part_lower.startswith("deadline") or part_lower.startswith("échéance"):
                value = part.split(":", 1)[1].strip() if ":" in part else part
                if value and value.upper() not in ["N/A", "NA", "-", "NON SPÉCIFIÉ"]:
                    deadline = value

        return {
            "action": action,
            "assignee": assignee,
            "deadline": deadline
        }

    def quick_synthesis_from_text(
        self,
        full_transcript: str,
        meeting_title: str,
        meeting_date: str,
        meeting_duration: str
    ) -> MeetingReport:
        """
        Synthèse rapide directe depuis le texte brut (fallback si pas de résumés intermédiaires)
        ATTENTION: Plus lent pour les longues réunions

        Args:
            full_transcript: Transcription complète
            meeting_title: Titre de la réunion
            meeting_date: Date
            meeting_duration: Durée

        Returns:
            MeetingReport
        """
        start_time = time.time()

        logger.warning("Synthèse directe depuis transcription brute (peut être lent)")

        report = MeetingReport(
            title=meeting_title,
            date=meeting_date,
            duration=meeting_duration
        )

        # Tronquer si trop long (garder environ 15000 caractères)
        max_chars = 15000
        if len(full_transcript) > max_chars:
            # Garder début et fin
            half = max_chars // 2
            full_transcript = (
                full_transcript[:half] +
                "\n\n[... transcription tronquée ...]\n\n" +
                full_transcript[-half:]
            )
            logger.warning(f"Transcription tronquée à {max_chars} caractères")

        prompt = f"""Analyse cette transcription de réunion et génère un rapport complet:

{full_transcript}

Génère:
1. RÉSUMÉ EXÉCUTIF (2-3 phrases)
2. POINTS CLÉS (5-7 points maximum)
3. HIGHLIGHTS (2-3 moments importants)
4. DÉCISIONS prises
5. ACTIONS avec responsables si mentionnés"""

        response = self.llm.analyze(
            prompt,
            system_prompt=SYSTEM_PROMPTS["final_synthesis"]
        )

        if response.success:
            self._parse_synthesis_response(response.text, report)
            report.llm_backend = response.backend
            report.total_tokens = response.tokens_used
        else:
            report.executive_summary = f"Erreur: {response.error}"

        report.generation_time = time.time() - start_time
        return report
