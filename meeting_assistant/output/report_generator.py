"""
Générateur de rapports en différents formats
Supporte Markdown, HTML et PDF (optionnel)
"""

import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Import Jinja2
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    logger.warning("Jinja2 non disponible - génération de rapports limitée")

# Import markdown
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class ReportGenerator:
    """
    Génère des rapports de réunion en différents formats
    """

    def __init__(
        self,
        templates_dir: Optional[Path] = None,
        output_dir: Path = Path("./meeting_reports")
    ):
        """
        Initialise le générateur de rapports

        Args:
            templates_dir: Répertoire des templates Jinja2
            output_dir: Répertoire de sortie des rapports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Templates
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"

        self.templates_dir = templates_dir

        # Environnement Jinja2
        self._jinja_env = None
        if JINJA2_AVAILABLE and templates_dir.exists():
            self._jinja_env = Environment(
                loader=FileSystemLoader(str(templates_dir)),
                autoescape=select_autoescape(['html', 'xml'])
            )

        logger.info(f"ReportGenerator initialisé: {output_dir}")

    def generate_markdown(
        self,
        report_data: Dict[str, Any],
        session_id: str,
        include_transcript: bool = True
    ) -> Path:
        """
        Génère un rapport Markdown

        Args:
            report_data: Données du rapport (depuis MeetingReport.to_dict())
            session_id: ID de la session
            include_transcript: Inclure la transcription complète

        Returns:
            Chemin du fichier généré
        """
        output_file = self.output_dir / f"rapport_{session_id}.md"

        if self._jinja_env:
            # Utiliser le template
            try:
                template = self._jinja_env.get_template("report_markdown.j2")
                content = template.render(
                    **report_data,
                    include_full_transcript=include_transcript,
                    version="1.0.0"
                )
            except Exception as e:
                logger.warning(f"Erreur template Jinja2: {e}, fallback vers génération manuelle")
                content = self._generate_markdown_manual(report_data, include_transcript)
        else:
            content = self._generate_markdown_manual(report_data, include_transcript)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Rapport Markdown généré: {output_file}")
        return output_file

    def _generate_markdown_manual(
        self,
        report_data: Dict[str, Any],
        include_transcript: bool
    ) -> str:
        """
        Génère le Markdown manuellement (sans Jinja2)

        Args:
            report_data: Données du rapport
            include_transcript: Inclure la transcription

        Returns:
            Contenu Markdown
        """
        lines = []

        # Titre
        lines.append(f"# {report_data.get('title', 'Rapport de Réunion')}")
        lines.append("")
        lines.append(f"**Date:** {report_data.get('date', 'N/A')}")
        lines.append(f"**Durée:** {report_data.get('duration', 'N/A')}")
        lines.append(f"**Participants:** {report_data.get('participants', 'Non spécifié')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Résumé exécutif
        lines.append("## Résumé Exécutif")
        lines.append("")
        lines.append(report_data.get('executive_summary', 'Aucun résumé disponible.'))
        lines.append("")
        lines.append("---")
        lines.append("")

        # Points clés
        lines.append("## Points Clés")
        lines.append("")
        for point in report_data.get('key_points', []):
            lines.append(f"- {point}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Highlights
        lines.append("## Highlights")
        lines.append("")
        for highlight in report_data.get('highlights', []):
            lines.append(f"### {highlight.get('topic', 'Sujet')}")
            lines.append(highlight.get('content', ''))
            lines.append("")
        lines.append("---")
        lines.append("")

        # Actions
        lines.append("## Actions à Suivre")
        lines.append("")
        for action in report_data.get('action_items', []):
            action_text = f"- [ ] **{action.get('action', 'N/A')}**"
            if action.get('assignee'):
                action_text += f" - *{action['assignee']}*"
            if action.get('deadline'):
                action_text += f" (Échéance: {action['deadline']})"
            lines.append(action_text)
        lines.append("")
        lines.append("---")
        lines.append("")

        # Décisions
        lines.append("## Décisions Prises")
        lines.append("")
        for decision in report_data.get('decisions', []):
            lines.append(f"- {decision}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Transcription
        if include_transcript and report_data.get('transcript_segments'):
            lines.append("## Transcription Complète")
            lines.append("")
            lines.append("<details>")
            lines.append("<summary>Cliquez pour afficher la transcription complète</summary>")
            lines.append("")
            for segment in report_data.get('transcript_segments', []):
                lines.append(f"**[{segment.get('timestamp', '')}]** {segment.get('text', '')}")
                lines.append("")
            lines.append("</details>")
            lines.append("")

        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*Rapport généré automatiquement par Meeting Assistant v1.0.0*")

        return "\n".join(lines)

    def generate_html(
        self,
        report_data: Dict[str, Any],
        session_id: str,
        include_transcript: bool = True
    ) -> Path:
        """
        Génère un rapport HTML

        Args:
            report_data: Données du rapport
            session_id: ID de la session
            include_transcript: Inclure la transcription complète

        Returns:
            Chemin du fichier généré
        """
        output_file = self.output_dir / f"rapport_{session_id}.html"

        if self._jinja_env:
            try:
                template = self._jinja_env.get_template("report_html.j2")
                content = template.render(
                    **report_data,
                    include_full_transcript=include_transcript,
                    version="1.0.0"
                )
            except Exception as e:
                logger.warning(f"Erreur template HTML: {e}, conversion depuis Markdown")
                content = self._markdown_to_html(report_data, include_transcript)
        else:
            content = self._markdown_to_html(report_data, include_transcript)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Rapport HTML généré: {output_file}")
        return output_file

    def _markdown_to_html(
        self,
        report_data: Dict[str, Any],
        include_transcript: bool
    ) -> str:
        """
        Convertit le Markdown en HTML basique

        Args:
            report_data: Données du rapport
            include_transcript: Inclure la transcription

        Returns:
            Contenu HTML
        """
        md_content = self._generate_markdown_manual(report_data, include_transcript)

        if MARKDOWN_AVAILABLE:
            html_body = markdown.markdown(md_content, extensions=['extra', 'toc'])
        else:
            # Conversion très basique
            html_body = md_content.replace("\n", "<br>\n")

        # Template HTML basique
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_data.get('title', 'Rapport de Réunion')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ color: #2563eb; }}
        h2 {{ color: #1e40af; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }}
        h3 {{ color: #3730a3; }}
        ul {{ padding-left: 1.5rem; }}
        li {{ margin: 0.5rem 0; }}
        hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0; }}
        details {{ background: #f8fafc; padding: 1rem; border-radius: 8px; }}
        summary {{ cursor: pointer; font-weight: bold; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

        return html

    def generate_json(
        self,
        report_data: Dict[str, Any],
        session_id: str
    ) -> Path:
        """
        Génère un rapport JSON

        Args:
            report_data: Données du rapport
            session_id: ID de la session

        Returns:
            Chemin du fichier généré
        """
        output_file = self.output_dir / f"rapport_{session_id}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Rapport JSON généré: {output_file}")
        return output_file

    def generate_all(
        self,
        report_data: Dict[str, Any],
        session_id: str,
        formats: List[str] = None,
        include_transcript: bool = True
    ) -> Dict[str, Path]:
        """
        Génère le rapport dans plusieurs formats

        Args:
            report_data: Données du rapport
            session_id: ID de la session
            formats: Liste des formats (markdown, html, json)
            include_transcript: Inclure la transcription

        Returns:
            Dictionnaire {format: chemin_fichier}
        """
        if formats is None:
            formats = ["markdown", "html"]

        generated = {}

        for fmt in formats:
            try:
                if fmt == "markdown":
                    generated["markdown"] = self.generate_markdown(
                        report_data, session_id, include_transcript
                    )
                elif fmt == "html":
                    generated["html"] = self.generate_html(
                        report_data, session_id, include_transcript
                    )
                elif fmt == "json":
                    generated["json"] = self.generate_json(report_data, session_id)
                else:
                    logger.warning(f"Format non supporté: {fmt}")
            except Exception as e:
                logger.error(f"Erreur génération format {fmt}: {e}")

        return generated

    def list_reports(self) -> List[Dict[str, Any]]:
        """
        Liste tous les rapports générés

        Returns:
            Liste des rapports avec métadonnées
        """
        reports = []

        for f in self.output_dir.glob("rapport_*.md"):
            session_id = f.stem.replace("rapport_", "")
            reports.append({
                "session_id": session_id,
                "markdown": f,
                "html": self.output_dir / f"rapport_{session_id}.html",
                "json": self.output_dir / f"rapport_{session_id}.json",
                "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            })

        return sorted(reports, key=lambda x: x["created_at"], reverse=True)
