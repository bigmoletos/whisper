"""
Module d'injection de texte dans le champ actif
"""

import pyautogui
import pyperclip
import logging
import time
import sys

# Configuration pyautogui pour Windows
pyautogui.FAILSAFE = False  # Désactiver la sécurité (peut être réactivée si nécessaire)
pyautogui.PAUSE = 0.01  # Pause minimale entre les actions

logger = logging.getLogger(__name__)


class TextInjector:
    """Injecte du texte dans le champ actif de l'application"""

    def __init__(self, use_clipboard: bool = True):
        """
        Initialise l'injecteur de texte

        Args:
            use_clipboard: Si True, utilise le presse-papiers + Ctrl+V, sinon simule la frappe
        """
        self.use_clipboard = use_clipboard
        logger.info(f"Injecteur de texte initialisé (méthode: {'presse-papiers' if use_clipboard else 'frappe simulée'})")

    def inject_text(self, text: str) -> bool:
        """
        Injecte le texte dans le champ actif

        Args:
            text: Texte à injecter

        Returns:
            True si succès, False sinon
        """
        if not text or not text.strip():
            logger.warning("Texte vide, aucune injection")
            return False

        try:
            if self.use_clipboard:
                return self._inject_via_clipboard(text)
            else:
                return self._inject_via_typing(text)

        except Exception as e:
            logger.error(f"Erreur lors de l'injection du texte: {e}", exc_info=True)
            return False

    def _inject_via_clipboard(self, text: str) -> bool:
        """
        Injecte le texte via le presse-papiers (Ctrl+V)

        Args:
            text: Texte à injecter

        Returns:
            True si succès, False sinon
        """
        try:
            # Sauvegarder le contenu actuel du presse-papiers
            try:
                old_clipboard = pyperclip.paste()
            except Exception:
                old_clipboard = ""

            # Copier le nouveau texte dans le presse-papiers
            pyperclip.copy(text)
            logger.debug(f"Texte copié dans le presse-papiers: '{text[:50]}...'")

            # Attendre un court instant pour s'assurer que le presse-papiers est prêt
            time.sleep(0.05)

            # Simuler Ctrl+V
            pyautogui.hotkey('ctrl', 'v')
            logger.info(f"Texte injecté via presse-papiers: '{text[:50]}...'")

            # Optionnel: restaurer l'ancien contenu du presse-papiers après un délai
            # (commenté pour éviter les problèmes de timing)
            # time.sleep(0.1)
            # pyperclip.copy(old_clipboard)

            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'injection via presse-papiers: {e}", exc_info=True)
            return False

    def _inject_via_typing(self, text: str) -> bool:
        """
        Injecte le texte en simulant la frappe

        Args:
            text: Texte à injecter

        Returns:
            True si succès, False sinon
        """
        try:
            logger.debug(f"Frappe simulée du texte: '{text[:50]}...'")

            # Utiliser pyautogui.write pour taper le texte
            # Cette méthode gère automatiquement les caractères spéciaux
            pyautogui.write(text, interval=0.01)

            logger.info(f"Texte injecté via frappe simulée: '{text[:50]}...'")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de la frappe simulée: {e}", exc_info=True)
            return False

    def inject_with_enter(self, text: str, press_enter: bool = False) -> bool:
        """
        Injecte le texte et optionnellement appuie sur Entrée

        Args:
            text: Texte à injecter
            press_enter: Si True, appuie sur Entrée après l'injection

        Returns:
            True si succès, False sinon
        """
        success = self.inject_text(text)

        if success and press_enter:
            try:
                time.sleep(0.1)  # Attendre que le texte soit injecté
                pyautogui.press('enter')
                logger.debug("Touche Entrée pressée")
            except Exception as e:
                logger.warning(f"Erreur lors de l'appui sur Entrée: {e}")

        return success

    def get_active_window_info(self) -> dict:
        """
        Retourne des informations sur la fenêtre active

        Returns:
            Dictionnaire avec les informations de la fenêtre
        """
        try:
            # Sur Windows, on peut utiliser pywin32 pour plus d'infos
            if sys.platform == 'win32':
                try:
                    import win32gui
                    import win32process

                    hwnd = win32gui.GetForegroundWindow()
                    window_title = win32gui.GetWindowText(hwnd)
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)

                    return {
                        "title": window_title,
                        "pid": pid,
                        "hwnd": hwnd
                    }
                except ImportError:
                    logger.warning("pywin32 non disponible, informations limitées")

            # Fallback: utiliser pyautogui
            return {
                "title": "Unknown",
                "position": pyautogui.position()
            }

        except Exception as e:
            logger.warning(f"Erreur lors de la récupération des infos de fenêtre: {e}")
            return {}

    def clear_and_inject(self, text: str) -> bool:
        """
        Efface le contenu actuel du champ et injecte le nouveau texte

        Args:
            text: Texte à injecter

        Returns:
            True si succès, False sinon
        """
        try:
            # Sélectionner tout (Ctrl+A)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.05)

            # Injecter le nouveau texte
            return self.inject_text(text)

        except Exception as e:
            logger.error(f"Erreur lors du remplacement du texte: {e}", exc_info=True)
            return False
