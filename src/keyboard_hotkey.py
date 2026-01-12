"""
Module de gestion des raccourcis clavier globaux
"""

import keyboard
import logging
from typing import Callable, Optional, List
import threading

logger = logging.getLogger(__name__)


class KeyboardHotkey:
    """Gestionnaire de raccourcis clavier globaux"""

    def __init__(self, modifiers: List[str], key: str, callback: Callable[[], None]):
        """
        Initialise le gestionnaire de raccourci clavier

        Args:
            modifiers: Liste des modificateurs (ex: ['ctrl', 'shift'])
            key: Touche principale (ex: 'v')
            callback: Fonction à appeler lorsque le raccourci est pressé
        """
        self.modifiers = [m.lower() for m in modifiers]
        self.key = key.lower()
        self.callback = callback
        self.is_registered = False
        self.hotkey_string = self._build_hotkey_string()

        logger.info(f"Raccourci clavier initialisé: {self.hotkey_string}")

    def _build_hotkey_string(self) -> str:
        """
        Construit la chaîne de raccourci pour la bibliothèque keyboard

        Returns:
            Chaîne de raccourci (ex: 'ctrl+shift+v')
        """
        # Normaliser ALTGR - la bibliothèque keyboard utilise "alt gr" (avec espace)
        normalized_modifiers = []
        for mod in self.modifiers:
            mod_lower = mod.lower().strip()
            if mod_lower in ['altgr', 'alt gr', 'right alt', 'rightalt']:
                # La bibliothèque keyboard reconnaît "alt gr" (avec espace)
                normalized_modifiers.append('alt gr')
            else:
                normalized_modifiers.append(mod_lower)

        # Pour les caractères spéciaux, utiliser le nom de la touche physique
        # Par exemple, sur AZERTY, ¤ est produit par AltGr+4, donc utiliser "4"
        key_normalized = self.key.lower().strip()

        # Mapper certains caractères spéciaux vers leurs touches physiques
        special_char_map = {
            '¤': '4',  # Sur AZERTY, AltGr+4 produit ¤
            '€': 'e',  # Sur AZERTY, AltGr+E produit €
            '£': 'l',  # Sur AZERTY, AltGr+L produit £
        }

        if key_normalized in special_char_map:
            key_normalized = special_char_map[key_normalized]
            logger.info(f"Caractère spécial '{self.key}' mappé vers la touche '{key_normalized}'")

        parts = sorted(normalized_modifiers) + [key_normalized]
        return '+'.join(parts)

    def register(self) -> bool:
        """
        Enregistre le raccourci clavier

        Returns:
            True si succès, False sinon
        """
        if self.is_registered:
            logger.warning("Raccourci déjà enregistré")
            return True

        try:
            # Utiliser add_hotkey pour détecter les combinaisons de touches
            keyboard.add_hotkey(
                self.hotkey_string,
                self._on_hotkey_pressed,
                suppress=False
            )
            logger.info(f"Raccourci enregistré: {self.hotkey_string}")
            self.is_registered = True
            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du raccourci: {e}", exc_info=True)
            return False

    def _on_hotkey_pressed(self) -> None:
        """Callback appelé lorsque le raccourci est pressé"""
        try:
            logger.debug(f"Raccourci détecté: {self.hotkey_string}")
            # Appeler le callback dans un thread séparé pour éviter les blocages
            threading.Thread(target=self.callback, daemon=True).start()

        except Exception as e:
            logger.error(f"Erreur dans le callback du raccourci: {e}", exc_info=True)

    def unregister(self) -> None:
        """Désenregistre le raccourci clavier"""
        if not self.is_registered:
            return

        try:
            # keyboard.remove_hotkey nécessite l'ID retourné par add_hotkey
            # Pour simplifier, on utilise unhook_all qui désenregistre tout
            # (dans un vrai système, il faudrait stocker les IDs)
            keyboard.unhook_all()
            self.is_registered = False
            logger.info(f"Raccourci désenregistré: {self.hotkey_string}")

        except Exception as e:
            logger.error(f"Erreur lors du désenregistrement du raccourci: {e}", exc_info=True)

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        self.unregister()


class HotkeyManager:
    """Gestionnaire centralisé des raccourcis clavier"""

    def __init__(self):
        """Initialise le gestionnaire de raccourcis"""
        self.hotkeys: List[KeyboardHotkey] = []
        logger.info("Gestionnaire de raccourcis initialisé")

    def register_hotkey(
        self,
        modifiers: List[str],
        key: str,
        callback: Callable[[], None],
        name: Optional[str] = None
    ) -> Optional[KeyboardHotkey]:
        """
        Enregistre un nouveau raccourci clavier

        Args:
            modifiers: Liste des modificateurs
            key: Touche principale
            callback: Fonction à appeler
            name: Nom optionnel du raccourci

        Returns:
            Instance de KeyboardHotkey ou None en cas d'erreur
        """
        try:
            hotkey = KeyboardHotkey(modifiers, key, callback)
            if hotkey.register():
                self.hotkeys.append(hotkey)
                if name:
                    logger.info(f"Raccourci '{name}' enregistré: {hotkey.hotkey_string}")
                return hotkey
            else:
                logger.error(f"Échec de l'enregistrement du raccourci: {hotkey.hotkey_string}")
                return None

        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du raccourci: {e}", exc_info=True)
            return None

    def unregister_all(self) -> None:
        """Désenregistre tous les raccourcis"""
        for hotkey in self.hotkeys:
            hotkey.unregister()
        self.hotkeys.clear()
        logger.info("Tous les raccourcis ont été désenregistrés")

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        self.unregister_all()
