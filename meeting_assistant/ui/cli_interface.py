"""
Interface en ligne de commande pour Meeting Assistant
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CLIInterface:
    """
    Interface CLI pour contrôler Meeting Assistant
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialise l'interface CLI

        Args:
            config_path: Chemin vers le fichier de configuration
        """
        self.config_path = config_path or Path(__file__).parent.parent / "config.json"
        self.config = self._load_config()

        # Session active
        self._active_session = None

    def _load_config(self) -> dict:
        """Charge la configuration"""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_config(self) -> None:
        """Sauvegarde la configuration"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def start_meeting(self, name: str, interactive: bool = True) -> bool:
        """
        Démarre une nouvelle session de réunion

        Args:
            name: Nom de la réunion
            interactive: Mode interactif (attend les commandes)

        Returns:
            True si démarrée avec succès
        """
        from ..session.meeting_session import MeetingSession

        print(f"\n{'='*60}")
        print(f"  Meeting Assistant - Démarrage")
        print(f"{'='*60}")
        print(f"\n  Réunion: {name}")
        print(f"  Configuration: {self.config_path}")
        print()

        # Vérifier les backends LLM
        print("  Vérification des backends LLM...")
        from ..analysis.llm_analyzer import LLMAnalyzer
        llm = LLMAnalyzer(self.config)
        backends = llm.get_available_backends()
        for backend, available in backends.items():
            status = "[OK]" if available else "[X]"
            print(f"    {status} {backend}")

        if not any(backends.values()):
            print("\n  [ERREUR] Aucun backend LLM disponible!")
            print("  Vérifiez qu'Ollama est lancé ou configurez une API OpenAI/Anthropic.")
            return False

        print(f"\n  Backend actif: {llm.get_primary_backend()}")
        print()

        # Callback de status
        def on_status(status: str, data: dict):
            timestamp = time.strftime("%H:%M:%S")
            if status == "started":
                print(f"  [{timestamp}] Session démarrée (ID: {data.get('session_id', 'N/A')})")
            elif status == "summary_generated":
                print(f"  [{timestamp}] Résumé généré: {data.get('time_range', '')} ({data.get('key_points_count', 0)} points clés)")
            elif status == "stopping":
                print(f"  [{timestamp}] Arrêt en cours...")
            elif status == "generating_report":
                print(f"  [{timestamp}] Génération du rapport final...")
            elif status == "stopped":
                print(f"  [{timestamp}] Session terminée")

        # Créer la session
        try:
            self._active_session = MeetingSession(
                config=self.config,
                meeting_name=name,
                on_status_change=on_status
            )

            print("  Chargement du modèle Whisper...")
            print("  (Cela peut prendre quelques secondes au premier lancement)")
            print()

            if not self._active_session.start():
                print("\n  [ERREUR] Échec du démarrage de la session")
                return False

            print()
            print(f"  {'='*56}")
            print(f"  ENREGISTREMENT EN COURS")
            print(f"  {'='*56}")
            print()
            print("  Commandes disponibles:")
            print("    p - Pause/Reprise")
            print("    s - Status")
            print("    q - Arrêter et générer le rapport")
            print()

            if interactive:
                self._interactive_loop()

            return True

        except Exception as e:
            logger.error(f"Erreur démarrage session: {e}", exc_info=True)
            print(f"\n  [ERREUR] {e}")
            return False

    def _interactive_loop(self) -> None:
        """Boucle interactive pour contrôler la session"""
        try:
            while self._active_session and self._active_session.is_running:
                try:
                    cmd = input("  > ").strip().lower()

                    if cmd == 'q':
                        self._stop_meeting()
                        break
                    elif cmd == 'p':
                        if self._active_session.is_paused:
                            self._active_session.resume()
                            print("  [REPRISE] Enregistrement repris")
                        else:
                            self._active_session.pause()
                            print("  [PAUSE] Enregistrement en pause")
                    elif cmd == 's':
                        self._print_status()
                    elif cmd == '':
                        continue
                    else:
                        print(f"  Commande inconnue: {cmd}")

                except EOFError:
                    # Ctrl+D
                    self._stop_meeting()
                    break

        except KeyboardInterrupt:
            print("\n\n  Interruption détectée, arrêt en cours...")
            self._stop_meeting()

    def _stop_meeting(self) -> None:
        """Arrête la réunion en cours"""
        if not self._active_session:
            return

        print("\n  Arrêt de la session...")
        report = self._active_session.stop()

        if report:
            print()
            print(f"  {'='*56}")
            print(f"  RAPPORT GÉNÉRÉ")
            print(f"  {'='*56}")
            print()
            print(f"  Durée totale: {report.duration}")
            print(f"  Temps de génération: {report.generation_time:.2f}s")
            print(f"  Backend utilisé: {report.llm_backend}")
            print()
            print("  Résumé exécutif:")
            print(f"  {report.executive_summary[:200]}...")
            print()
            print(f"  Points clés: {len(report.key_points)}")
            print(f"  Actions: {len(report.action_items)}")
            print(f"  Décisions: {len(report.decisions)}")
            print()

            # Générer les fichiers
            from ..output.report_generator import ReportGenerator
            generator = ReportGenerator(
                output_dir=Path(self.config.get("output", {}).get("directory", "./meeting_reports"))
            )

            formats = self.config.get("output", {}).get("formats", ["markdown", "html"])
            include_transcript = self.config.get("output", {}).get("include_full_transcript", True)

            # Ajouter les segments de transcription si disponible
            report_dict = report.to_dict()
            if self._active_session._transcript_storage:
                report_dict["transcript_segments"] = \
                    self._active_session._transcript_storage.get_formatted_transcript()

            generated = generator.generate_all(
                report_dict,
                self._active_session.session_id,
                formats=formats,
                include_transcript=include_transcript
            )

            print("  Fichiers générés:")
            for fmt, path in generated.items():
                print(f"    - {path}")
            print()

        self._active_session = None

    def _print_status(self) -> None:
        """Affiche le status de la session"""
        if not self._active_session:
            print("  Aucune session active")
            return

        status = self._active_session.get_status()
        print()
        print(f"  Session: {status.get('session_id', 'N/A')}")
        print(f"  État: {'PAUSE' if status.get('is_paused') else 'ENREGISTREMENT'}")
        print(f"  Durée: {status.get('elapsed_time_formatted', '00:00:00')}")

        if 'transcript' in status:
            t = status['transcript']
            print(f"  Segments: {t.get('segment_count', 0)}")
            print(f"  Mots: {t.get('total_words', 0)}")

        if 'summarizer' in status:
            s = status['summarizer']
            print(f"  Résumés générés: {s.get('summary_count', 0)}")

        print()

    def list_sessions(self) -> None:
        """Liste les sessions existantes"""
        from ..session.checkpoint_manager import CheckpointManager

        sessions_dir = Path(self.config.get("session", {}).get("sessions_directory", "./meeting_sessions"))

        if not sessions_dir.exists():
            print("  Aucune session trouvée")
            return

        print(f"\n  {'='*60}")
        print(f"  Sessions enregistrées")
        print(f"  {'='*60}\n")

        for session_path in sorted(sessions_dir.iterdir(), reverse=True):
            if session_path.is_dir():
                state_file = session_path / "session_state.json"
                if state_file.exists():
                    with open(state_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        print(f"  ID: {data.get('session_id', 'N/A')}")
                        print(f"  Nom: {data.get('meeting_name', 'N/A')}")
                        print(f"  Date: {data.get('created_at', 'N/A')}")
                        print(f"  État: {data.get('state', 'N/A')}")
                        if 'stats' in data:
                            stats = data['stats']
                            duration = stats.get('total_audio_duration', 0)
                            print(f"  Durée: {int(duration//3600):02d}:{int((duration%3600)//60):02d}:{int(duration%60):02d}")
                        print()

    def show_status(self) -> None:
        """Affiche le status de la session active"""
        if self._active_session:
            self._print_status()
        else:
            print("  Aucune session active")

    def resume_session(self, session_id: str) -> bool:
        """
        Reprend une session interrompue

        Args:
            session_id: ID de la session à reprendre

        Returns:
            True si reprise avec succès
        """
        # TODO: Implémenter la reprise de session
        print(f"  Reprise de session non encore implémentée")
        print(f"  Session demandée: {session_id}")
        return False


def create_parser() -> argparse.ArgumentParser:
    """Crée le parser d'arguments"""
    parser = argparse.ArgumentParser(
        prog="meeting_assistant",
        description="Assistant de réunion avec transcription et résumé automatique"
    )

    parser.add_argument(
        "--config", "-c",
        type=Path,
        help="Chemin vers le fichier de configuration"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mode verbose (debug)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande start
    start_parser = subparsers.add_parser("start", help="Démarre une nouvelle session")
    start_parser.add_argument(
        "--name", "-n",
        default="Réunion",
        help="Nom de la réunion"
    )

    # Commande list
    subparsers.add_parser("list", help="Liste les sessions")

    # Commande status
    subparsers.add_parser("status", help="Affiche le status de la session active")

    # Commande resume
    resume_parser = subparsers.add_parser("resume", help="Reprend une session interrompue")
    resume_parser.add_argument(
        "--session", "-s",
        required=True,
        help="ID de la session à reprendre"
    )

    return parser


def main():
    """Point d'entrée CLI"""
    parser = create_parser()
    args = parser.parse_args()

    # Configuration du logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Interface CLI
    cli = CLIInterface(config_path=args.config)

    # Exécuter la commande
    if args.command == "start":
        cli.start_meeting(args.name)
    elif args.command == "list":
        cli.list_sessions()
    elif args.command == "status":
        cli.show_status()
    elif args.command == "resume":
        cli.resume_session(args.session)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
