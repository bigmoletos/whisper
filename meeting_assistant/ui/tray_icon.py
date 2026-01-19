"""
Interface System Tray pour Meeting Assistant
Icône dans la barre des tâches avec menu contextuel
"""

import logging
import threading
import time
from pathlib import Path
from typing import Optional, Callable
import io

logger = logging.getLogger(__name__)

# Imports conditionnels
try:
    import pystray
    from pystray import MenuItem as item
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False
    logger.warning("pystray non disponible - interface tray désactivée")

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL non disponible - icônes personnalisées désactivées")


class TrayIcon:
    """
    Icône System Tray pour contrôler Meeting Assistant
    """

    # États de l'icône
    STATE_READY = "ready"      # Vert - prêt à enregistrer
    STATE_RECORDING = "recording"  # Rouge - enregistrement en cours
    STATE_PAUSED = "paused"    # Orange - en pause
    STATE_PROCESSING = "processing"  # Bleu - traitement en cours

    def __init__(
        self,
        on_start: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        on_pause: Optional[Callable] = None,
        on_resume: Optional[Callable] = None,
        on_quit: Optional[Callable] = None,
        on_status: Optional[Callable] = None
    ):
        """
        Initialise l'icône System Tray

        Args:
            on_start: Callback pour démarrer l'enregistrement
            on_stop: Callback pour arrêter l'enregistrement
            on_pause: Callback pour mettre en pause
            on_resume: Callback pour reprendre
            on_quit: Callback pour quitter
            on_status: Callback pour obtenir le status
        """
        if not PYSTRAY_AVAILABLE:
            raise ImportError("pystray n'est pas installé. Installez avec: pip install pystray pillow")

        self.on_start = on_start
        self.on_stop = on_stop
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.on_quit = on_quit
        self.on_status = on_status

        self._icon: Optional[pystray.Icon] = None
        self._state = self.STATE_READY
        self._is_running = False
        self._thread: Optional[threading.Thread] = None

        # Cache des icônes
        self._icons = {}
        self._create_icons()

        logger.info("TrayIcon initialisé")

    def _create_icons(self) -> None:
        """Crée les icônes pour chaque état"""
        if not PIL_AVAILABLE:
            return

        colors = {
            self.STATE_READY: "#22c55e",      # Vert
            self.STATE_RECORDING: "#ef4444",   # Rouge
            self.STATE_PAUSED: "#f59e0b",      # Orange
            self.STATE_PROCESSING: "#3b82f6"   # Bleu
        }

        for state, color in colors.items():
            self._icons[state] = self._create_icon(color)

    def _create_icon(self, color: str, size: int = 64) -> Image.Image:
        """
        Crée une icône circulaire simple

        Args:
            color: Couleur hex de l'icône
            size: Taille en pixels

        Returns:
            Image PIL
        """
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Cercle principal
        margin = 4
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=color,
            outline="#ffffff",
            width=2
        )

        # Symbole central selon l'état
        center = size // 2
        symbol_size = size // 4

        return image

    def _get_icon(self) -> Image.Image:
        """Retourne l'icône pour l'état actuel"""
        if self._state in self._icons:
            return self._icons[self._state]

        # Fallback: icône basique
        if PIL_AVAILABLE:
            return self._create_icon("#808080")

        # Sans PIL: créer une image minimale
        return Image.new('RGB', (64, 64), color='gray')

    def _create_menu(self):
        """Crée le menu contextuel"""
        is_recording = self._state == self.STATE_RECORDING
        is_paused = self._state == self.STATE_PAUSED

        menu_items = []

        # Status
        if self._state == self.STATE_READY:
            menu_items.append(item("Prêt", None, enabled=False))
        elif self._state == self.STATE_RECORDING:
            menu_items.append(item("Enregistrement...", None, enabled=False))
        elif self._state == self.STATE_PAUSED:
            menu_items.append(item("En pause", None, enabled=False))

        menu_items.append(pystray.Menu.SEPARATOR)

        # Actions
        if not is_recording and not is_paused:
            menu_items.append(item("Démarrer", self._on_start_click))
        else:
            menu_items.append(item("Démarrer", self._on_start_click, enabled=False))

        if is_recording:
            menu_items.append(item("Pause", self._on_pause_click))
        elif is_paused:
            menu_items.append(item("Reprendre", self._on_resume_click))
        else:
            menu_items.append(item("Pause", self._on_pause_click, enabled=False))

        if is_recording or is_paused:
            menu_items.append(item("Arrêter", self._on_stop_click))
        else:
            menu_items.append(item("Arrêter", self._on_stop_click, enabled=False))

        menu_items.append(pystray.Menu.SEPARATOR)

        # Status détaillé
        menu_items.append(item("Status", self._on_status_click))

        menu_items.append(pystray.Menu.SEPARATOR)

        # Quitter
        menu_items.append(item("Quitter", self._on_quit_click))

        return pystray.Menu(*menu_items)

    def _on_start_click(self, icon, item):
        """Callback click Démarrer"""
        if self.on_start:
            threading.Thread(target=self.on_start, daemon=True).start()

    def _on_stop_click(self, icon, item):
        """Callback click Arrêter"""
        if self.on_stop:
            threading.Thread(target=self.on_stop, daemon=True).start()

    def _on_pause_click(self, icon, item):
        """Callback click Pause"""
        if self.on_pause:
            self.on_pause()

    def _on_resume_click(self, icon, item):
        """Callback click Reprendre"""
        if self.on_resume:
            self.on_resume()

    def _on_status_click(self, icon, item):
        """Callback click Status"""
        if self.on_status:
            status = self.on_status()
            if status:
                # Afficher une notification
                self._notify(f"Durée: {status.get('elapsed_time_formatted', 'N/A')}")

    def _on_quit_click(self, icon, item):
        """Callback click Quitter"""
        self.stop()
        if self.on_quit:
            self.on_quit()

    def _notify(self, message: str, title: str = "Meeting Assistant") -> None:
        """Affiche une notification"""
        if self._icon and hasattr(self._icon, 'notify'):
            try:
                self._icon.notify(message, title)
            except Exception as e:
                logger.debug(f"Notification échouée: {e}")

    def set_state(self, state: str) -> None:
        """
        Change l'état de l'icône

        Args:
            state: Nouvel état (ready, recording, paused, processing)
        """
        self._state = state

        if self._icon:
            # Mettre à jour l'icône
            self._icon.icon = self._get_icon()
            # Mettre à jour le menu
            self._icon.menu = self._create_menu()
            # Mettre à jour le tooltip
            tooltips = {
                self.STATE_READY: "Meeting Assistant - Prêt",
                self.STATE_RECORDING: "Meeting Assistant - Enregistrement",
                self.STATE_PAUSED: "Meeting Assistant - Pause",
                self.STATE_PROCESSING: "Meeting Assistant - Traitement"
            }
            self._icon.title = tooltips.get(state, "Meeting Assistant")

        logger.debug(f"État tray changé: {state}")

    def start(self) -> None:
        """Démarre l'icône System Tray"""
        if self._is_running:
            return

        self._is_running = True

        # Créer l'icône
        self._icon = pystray.Icon(
            "meeting_assistant",
            self._get_icon(),
            "Meeting Assistant",
            menu=self._create_menu()
        )

        # Démarrer dans un thread
        self._thread = threading.Thread(
            target=self._icon.run,
            daemon=True,
            name="TrayIcon"
        )
        self._thread.start()

        logger.info("TrayIcon démarré")

    def stop(self) -> None:
        """Arrête l'icône System Tray"""
        if not self._is_running:
            return

        self._is_running = False

        if self._icon:
            try:
                self._icon.stop()
            except Exception as e:
                logger.debug(f"Erreur arrêt tray: {e}")
            self._icon = None

        logger.info("TrayIcon arrêté")

    @property
    def is_running(self) -> bool:
        """Retourne True si l'icône est active"""
        return self._is_running


def run_with_tray(config: dict) -> None:
    """
    Lance Meeting Assistant avec l'interface System Tray

    Args:
        config: Configuration de l'application
    """
    if not PYSTRAY_AVAILABLE:
        print("Erreur: pystray n'est pas installé")
        print("Installez avec: pip install pystray pillow")
        return

    from ..session.meeting_session import MeetingSession

    session: Optional[MeetingSession] = None

    def on_start():
        nonlocal session
        if session and session.is_running:
            return

        session = MeetingSession(
            config=config,
            meeting_name="Réunion",
            on_status_change=lambda s, d: update_tray_state(s)
        )

        if session.start():
            tray.set_state(TrayIcon.STATE_RECORDING)
        else:
            session = None

    def on_stop():
        nonlocal session
        if session:
            tray.set_state(TrayIcon.STATE_PROCESSING)
            session.stop()
            session = None
            tray.set_state(TrayIcon.STATE_READY)

    def on_pause():
        if session:
            session.pause()
            tray.set_state(TrayIcon.STATE_PAUSED)

    def on_resume():
        if session:
            session.resume()
            tray.set_state(TrayIcon.STATE_RECORDING)

    def on_status():
        if session:
            return session.get_status()
        return None

    def on_quit():
        if session and session.is_running:
            session.stop()

    def update_tray_state(status: str):
        if status == "started":
            tray.set_state(TrayIcon.STATE_RECORDING)
        elif status == "paused":
            tray.set_state(TrayIcon.STATE_PAUSED)
        elif status == "stopped":
            tray.set_state(TrayIcon.STATE_READY)
        elif status == "generating_report":
            tray.set_state(TrayIcon.STATE_PROCESSING)

    # Créer l'icône tray
    tray = TrayIcon(
        on_start=on_start,
        on_stop=on_stop,
        on_pause=on_pause,
        on_resume=on_resume,
        on_quit=on_quit,
        on_status=on_status
    )

    print("Meeting Assistant démarré dans le System Tray")
    print("Cliquez droit sur l'icône pour accéder aux options")

    # Démarrer (bloquant dans le thread principal)
    tray._icon = pystray.Icon(
        "meeting_assistant",
        tray._get_icon(),
        "Meeting Assistant - Prêt",
        menu=tray._create_menu()
    )
    tray._is_running = True
    tray._icon.run()
