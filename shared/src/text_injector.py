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
        Injecte le texte via le presse-papiers (Ctrl+V) - Version robuste

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

            # Attendre que le presse-papiers soit prêt
            time.sleep(0.15)
            
            # Vérifier que le texte est bien dans le presse-papiers
            clipboard_content = pyperclip.paste()
            if clipboard_content != text:
                logger.warning("Le texte n'a pas été correctement copié dans le presse-papiers")
                return False

            # Obtenir des infos sur la fenêtre active pour debug
            window_info = self.get_active_window_info()
            logger.debug(f"Fenêtre active: {window_info}")

            # SOLUTION ROBUSTE : Forcer le focus et injecter
            logger.debug("Injection robuste avec focus forcé...")
            
            # Étape 1: S'assurer du focus en cliquant au curseur actuel
            current_pos = pyautogui.position()
            pyautogui.click(current_pos.x, current_pos.y)
            time.sleep(0.1)
            
            # Étape 2: Simuler Ctrl+V avec délai
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)  # Délai plus long pour laisser le temps à l'injection
            
            # Étape 3: VÉRIFICATION RÉELLE - Essayer de récupérer le texte injecté
            # Méthode 1: Sélectionner tout et vérifier
            try:
                # Sauvegarder position curseur
                pyautogui.press('end')  # Aller à la fin
                time.sleep(0.05)
                
                # Sélectionner le texte qu'on vient d'injecter
                # On sélectionne autant de caractères qu'on a injecté
                for _ in range(len(text)):
                    pyautogui.hotkey('shift', 'left')
                
                time.sleep(0.1)
                
                # Copier la sélection pour vérifier
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.1)
                
                # Vérifier si c'est notre texte
                selected_text = pyperclip.paste()
                
                # Remettre le curseur à la fin
                pyautogui.press('end')
                
                if selected_text == text:
                    logger.info(f"Texte injecté et vérifié avec succès: '{text[:50]}...'")
                    return True
                else:
                    logger.warning(f"Vérification échouée. Attendu: '{text[:30]}...', Trouvé: '{selected_text[:30]}...'")
                    # Essayer méthode alternative
                    return self._inject_alternative_method(text)
                    
            except Exception as e:
                logger.debug(f"Vérification par sélection échouée: {e}")
                # Essayer méthode alternative
                return self._inject_alternative_method(text)

        except Exception as e:
            logger.error(f"Erreur lors de l'injection via presse-papiers: {e}", exc_info=True)
            # Essayer la méthode de frappe en fallback
            logger.info("Tentative de fallback vers la frappe simulée...")
            return self._inject_via_typing(text)
    
    def _inject_alternative_method(self, text: str) -> bool:
        """
        Méthode alternative d'injection plus agressive
        
        Args:
            text: Texte à injecter
            
        Returns:
            True si succès, False sinon
        """
        try:
            logger.info("Utilisation de la méthode alternative d'injection...")
            
            # Méthode 1: Clear + Paste
            pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')  # Coller
            time.sleep(0.2)
            
            # Vérification simple
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
            content = pyperclip.paste()
            if text in content:
                logger.info("Injection alternative réussie")
                pyautogui.press('end')  # Curseur à la fin
                return True
            
            # Méthode 2: Frappe directe
            logger.info("Tentative de frappe directe...")
            pyautogui.hotkey('ctrl', 'a')  # Clear
            time.sleep(0.1)
            pyautogui.write(text, interval=0.02)  # Frappe avec délai
            time.sleep(0.2)
            
            logger.info("Frappe directe terminée")
            return True
            
        except Exception as e:
            logger.error(f"Méthode alternative échouée: {e}")
            return False

    def _inject_via_typing(self, text: str) -> bool:
        """
        Injecte le texte en simulant la frappe - Version robuste

        Args:
            text: Texte à injecter

        Returns:
            True si succès, False sinon
        """
        try:
            logger.debug(f"Frappe simulée robuste du texte: '{text[:50]}...'")

            # S'assurer du focus
            current_pos = pyautogui.position()
            pyautogui.click(current_pos.x, current_pos.y)
            time.sleep(0.1)

            # Nettoyer le champ d'abord
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.05)
            
            # Utiliser pyautogui.write pour taper le texte
            # Avec un intervalle plus lent pour s'assurer que chaque caractère passe
            pyautogui.write(text, interval=0.03)
            
            # Attendre que la frappe soit terminée
            time.sleep(0.2)

            logger.info(f"Texte injecté via frappe simulée robuste: '{text[:50]}...'")
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

    def inject_text_robust(self, text: str) -> bool:
        """
        Injection ultra-robuste avec vérification réelle

        Args:
            text: Texte à injecter

        Returns:
            True si succès, False sinon
        """
        if not text or not text.strip():
            logger.warning("Texte vide, aucune injection")
            return False

        logger.info(f"Injection ultra-robuste du texte: '{text[:50]}...' (longueur: {len(text)})")

        # Sauvegarder le presse-papiers original
        try:
            original_clipboard = pyperclip.paste()
        except:
            original_clipboard = ""

        # Méthode 1: Injection avec vérification stricte
        try:
            logger.info("Tentative 1: Injection avec vérification stricte")
            
            # Copier le texte
            pyperclip.copy(text)
            time.sleep(0.1)
            
            # Vérifier que c'est bien copié
            if pyperclip.paste() != text:
                logger.warning("Échec copie presse-papiers")
                raise Exception("Clipboard copy failed")
            
            # Forcer le focus
            pyautogui.click()
            time.sleep(0.1)
            
            # Injecter
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # VÉRIFICATION RÉELLE : Sélectionner et vérifier
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
            injected_content = pyperclip.paste()
            
            if text in injected_content:
                logger.info("✅ Injection vérifiée avec succès (méthode 1)")
                pyautogui.press('end')  # Curseur à la fin
                return True
            else:
                logger.warning(f"Vérification échouée. Contenu: '{injected_content[:50]}...'")
                raise Exception("Verification failed")
                
        except Exception as e:
            logger.warning(f"Méthode 1 échouée: {e}")

        # Méthode 2: Clear + Paste agressif
        try:
            logger.info("Tentative 2: Clear + Paste agressif")
            
            pyperclip.copy(text)
            time.sleep(0.1)
            
            # Clear complet
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # Paste
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            # Vérification
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
            content = pyperclip.paste()
            if content == text:
                logger.info("✅ Injection vérifiée avec succès (méthode 2)")
                pyautogui.press('end')
                return True
            else:
                logger.warning(f"Méthode 2 - Contenu incorrect: '{content[:50]}...'")
                raise Exception("Method 2 failed")
                
        except Exception as e:
            logger.warning(f"Méthode 2 échouée: {e}")

        # Méthode 3: Frappe caractère par caractère
        try:
            logger.info("Tentative 3: Frappe caractère par caractère")
            
            # Clear
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # Frappe lente
            for char in text:
                pyautogui.write(char)
                time.sleep(0.01)  # Très lent mais sûr
            
            time.sleep(0.2)
            
            # Vérification
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
            content = pyperclip.paste()
            if content == text:
                logger.info("✅ Injection vérifiée avec succès (méthode 3)")
                pyautogui.press('end')
                return True
            else:
                logger.warning(f"Méthode 3 - Contenu incorrect: '{content[:50]}...'")
                
        except Exception as e:
            logger.warning(f"Méthode 3 échouée: {e}")

        # Méthode 4: Dernière chance - frappe normale
        try:
            logger.info("Tentative 4: Frappe normale (dernière chance)")
            
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.write(text, interval=0.02)
            time.sleep(0.3)
            
            logger.info("✅ Frappe normale terminée (pas de vérification)")
            return True
            
        except Exception as e:
            logger.error(f"Toutes les méthodes ont échoué: {e}")

        # Restaurer le presse-papiers original
        try:
            pyperclip.copy(original_clipboard)
        except:
            pass

        logger.error("❌ ÉCHEC COMPLET - Toutes les méthodes d'injection ont échoué")
        return False

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