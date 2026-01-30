"""
Service principal Whisper STT Global pour Windows
Point d'entrée de l'application
"""

import json
import logging
import sys
import os
import time
from pathlib import Path
from typing import Optional

# Ajouter le répertoire parent au PYTHONPATH pour les imports
if __name__ == "__main__" or __package__ is None:
    script_dir = Path(__file__).parent.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

from src.audio_capture import AudioCapture
from src.whisper_transcriber import WhisperTranscriber
from src.text_injector import TextInjector
from src.keyboard_hotkey import HotkeyManager
from src.text_corrector import load_corrector_from_config

# Import des notifications
try:
    from src.notifications import NotificationManager
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("Module de notifications non disponible")

# Import conditionnel de Faster-Whisper
try:
    from src.faster_whisper_transcriber import FasterWhisperTranscriber
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False

# Import conditionnel de Whisper.cpp
try:
    from src.whisper_cpp_transcriber import WhisperCppTranscriber
    WHISPER_CPP_AVAILABLE = True
except ImportError:
    WHISPER_CPP_AVAILABLE = False

# Import de la pop-up d'enregistrement
try:
    from src.recording_popup import show_recording, show_processing, hide_popup, cleanup_popup
    RECORDING_POPUP_AVAILABLE = True
    print("[DEBUG] Module recording_popup importé avec succès")
except ImportError as e:
    RECORDING_POPUP_AVAILABLE = False
    print(f"[DEBUG] Module recording_popup non disponible: {e}")

# Configuration du logging
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Configure le système de logging

    Args:
        log_level: Niveau de logging (DEBUG, INFO, WARNING, ERROR)
        log_file: Fichier de log (optionnel)
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Format des logs
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))

    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )


class WhisperSTTService:
    """Service principal de transcription vocale"""

    def __init__(self, config_path: str = "config.json"):
        """
        Initialise le service

        Args:
            config_path: Chemin vers le fichier de configuration
        """
        self.config_path = config_path

        # Configuration du logging AVANT de charger la config (pour les logs)
        # Utiliser une config par défaut temporaire
        temp_config = self._default_config()
        log_config = temp_config.get("logging", {})
        setup_logging(
            log_level=log_config.get("level", "INFO"),
            log_file=log_config.get("file")
        )

        self.logger = logging.getLogger(__name__)

        # Maintenant charger la vraie configuration
        self.config = self._load_config()

        # Reconfigurer le logging avec la vraie config si différente
        log_config = self.config.get("logging", {})
        if log_config.get("level") != temp_config.get("logging", {}).get("level") or \
           log_config.get("file") != temp_config.get("logging", {}).get("file"):
            setup_logging(
                log_level=log_config.get("level", "INFO"),
                log_file=log_config.get("file")
            )

        self.logger.info("Initialisation du service Whisper STT")

        # Composants
        self.audio_capture: Optional[AudioCapture] = None
        self.transcriber: Optional[WhisperTranscriber] = None
        self.text_injector: Optional[TextInjector] = None
        self.hotkey_manager: Optional[HotkeyManager] = None
        self.notification_manager: Optional[NotificationManager] = None
        self.text_corrector = None  # Module de correction post-transcription

        # État
        self.is_recording = False
        self.is_processing = False
        self.running = False

        # Initialiser les composants
        self._initialize_components()

    def _load_config(self) -> dict:
        """
        Charge la configuration depuis le fichier JSON

        Returns:
            Dictionnaire de configuration
        """
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                self.logger.warning(f"Fichier de configuration non trouvé: {self.config_path}, utilisation des valeurs par défaut")
                return self._default_config()

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.logger.info(f"Configuration chargée depuis: {self.config_path}")
            return config

        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la configuration: {e}", exc_info=True)
            return self._default_config()

    def _default_config(self) -> dict:
        """Retourne la configuration par défaut avec détection automatique des capacités"""
        # Détection automatique de CUDA
        device = "cpu"
        compute_type = "int8"
        engine = "whisper"
        
        try:
            import torch
            if torch.cuda.is_available():
                device = "cuda"
                compute_type = "float16"
                if FASTER_WHISPER_AVAILABLE:
                    engine = "faster-whisper"
                print(f"[INFO] CUDA détecté - Configuration optimisée activée (device: {device}, engine: {engine})")
            else:
                print("[INFO] CUDA non disponible - Configuration CPU utilisée")
        except ImportError:
            print("[INFO] PyTorch non disponible - Configuration CPU de base")
        
        return {
            "whisper": {
                "engine": engine,
                "model": "medium",  # Compromis qualité/vitesse selon standards VTT
                "language": "fr",
                "device": device,
                "compute_type": compute_type,
                "vad_filter": True if device == "cuda" else False,
                "initial_prompt": "Transcription professionnelle en français avec vocabulaire technique informatique, noms propres corrects et ponctuation appropriée."
            },
            "audio": {
                "sample_rate": 16000,
                "channels": 1,
                "chunk_duration": 3.0,
                "silence_threshold": 0.01,
                "silence_duration": 1.5
            },
            "hotkey": {
                "modifiers": ["ctrl", "alt"],
                "key": "7"
            },
            "logging": {
                "level": "INFO",
                "file": "whisper_stt.log"
            }
        }

    def _initialize_components(self) -> None:
        """Initialise tous les composants du service"""
        try:
            # Configuration audio
            audio_config = self.config.get("audio", {})
            self.audio_capture = AudioCapture(
                sample_rate=audio_config.get("sample_rate", 16000),
                channels=audio_config.get("channels", 1),
                chunk_duration=audio_config.get("chunk_duration", 3.0),
                silence_threshold=audio_config.get("silence_threshold", 0.01),
                silence_duration=audio_config.get("silence_duration", 1.5)
            )
            self.logger.info("Module de capture audio initialisé")

            # Configuration Whisper
            whisper_config = self.config.get("whisper", {})
            engine = whisper_config.get("engine", "whisper")  # "whisper" ou "faster-whisper"

            if engine == "whisper-cpp":
                if not WHISPER_CPP_AVAILABLE:
                    self.logger.warning("Whisper.cpp non disponible, tentative avec Faster-Whisper")
                    engine = "faster-whisper"
                else:
                    try:
                        # Utiliser Whisper.cpp (le plus rapide)
                        model_name = whisper_config.get("model", "medium")

                        self.transcriber = WhisperCppTranscriber(
                            model_name=model_name,
                            language=whisper_config.get("language", "fr"),
                            device=whisper_config.get("device", "cpu"),
                            compute_type=whisper_config.get("compute_type", "int8")
                        )
                        self.logger.info("Module Whisper.cpp initialisé (moteur ultra-rapide)")
                    except Exception as e:
                        self.logger.error(f"Erreur lors de l'initialisation de Whisper.cpp: {e}")
                        self.logger.warning("Basculement vers Faster-Whisper")
                        engine = "faster-whisper"

            if engine == "faster-whisper":
                if not FASTER_WHISPER_AVAILABLE:
                    self.logger.warning("Faster-Whisper non disponible, utilisation de Whisper standard")
                    self.logger.warning("Pour installer Faster-Whisper: pip install faster-whisper")
                    self.logger.warning("Note: Faster-Whisper nécessite Rust (https://rustup.rs/)")
                    engine = "whisper"  # Fallback sur Whisper standard
                else:
                    try:
                        # Utiliser Faster-Whisper (plus rapide)
                        model_name = whisper_config.get("model", "large-v3")
                        # Mapper les noms de modèles si nécessaire
                        model_mapping = {
                            "large": "large-v3",
                            "medium": "medium",
                            "small": "small",
                            "base": "base",
                            "tiny": "tiny"
                        }
                        model_name = model_mapping.get(model_name, model_name)

                        self.transcriber = FasterWhisperTranscriber(
                            model_name=model_name,
                            language=whisper_config.get("language", "fr"),
                            device=whisper_config.get("device", "cpu"),
                            compute_type=whisper_config.get("compute_type", "int8"),
                            initial_prompt=whisper_config.get("initial_prompt", "")
                        )
                        self.logger.info("Module Faster-Whisper initialisé (moteur optimisé)")
                    except Exception as e:
                        self.logger.error(f"Erreur lors de l'initialisation de Faster-Whisper: {e}")
                        self.logger.warning("Basculement vers Whisper standard")
                        engine = "whisper"  # Fallback sur Whisper standard

            if engine == "whisper":
                # Utiliser Whisper standard
                self.transcriber = WhisperTranscriber(
                    model_name=whisper_config.get("model", "medium"),
                    language=whisper_config.get("language", "fr"),
                    device=whisper_config.get("device", "cpu"),
                    initial_prompt=whisper_config.get("initial_prompt", "")
                )
                self.logger.info("Module Whisper standard initialisé")

            # Injecteur de texte
            self.text_injector = TextInjector(use_clipboard=True)
            self.logger.info("Module d'injection de texte initialisé")

            # Gestionnaire de raccourcis
            self.hotkey_manager = HotkeyManager()
            self.logger.info("Gestionnaire de raccourcis initialisé")

            # Gestionnaire de notifications
            if NOTIFICATIONS_AVAILABLE:
                self.notification_manager = NotificationManager()
                self.logger.info("Gestionnaire de notifications initialisé")
            else:
                self.logger.warning("Module de notifications non disponible")

            # Module de correction de texte (post-traitement)
            self.text_corrector = load_corrector_from_config(self.config)
            if self.text_corrector:
                self.logger.info("Module de correction de texte initialisé")
            else:
                self.logger.info("Correction de texte désactivée")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation des composants: {e}", exc_info=True)
            raise

    def _on_hotkey_pressed(self) -> None:
        """Callback appelé lorsque le raccourci clavier est pressé (toggle)"""
        if self.is_processing:
            self.logger.debug("Traitement déjà en cours, ignore la demande")
            return

        if self.is_recording:
            # Arrêter l'enregistrement et traiter
            self.logger.info("Arrêt de l'enregistrement et traitement...")
            self._process_recording()
        else:
            # Démarrer l'enregistrement
            self.logger.info("Démarrage de l'enregistrement (appuyez à nouveau pour arrêter)")
            self._start_recording()

    def _start_recording(self) -> None:
        """Démarre l'enregistrement audio"""
        try:
            if self.audio_capture:
                self.audio_capture.start_recording()
                self.is_recording = True
                self.logger.info("Enregistrement démarré (relâchez le raccourci pour arrêter)")
                
                # Afficher la pop-up d'enregistrement (priorité sur les notifications)
                ui_config = self.config.get("ui", {})
                popup_enabled = ui_config.get("show_recording_popup", True)
                
                self.logger.info(f"[DEBUG] RECORDING_POPUP_AVAILABLE: {RECORDING_POPUP_AVAILABLE}")
                self.logger.info(f"[DEBUG] show_recording_popup config: {popup_enabled}")
                
                if RECORDING_POPUP_AVAILABLE and popup_enabled:
                    self.logger.info("[DEBUG] Affichage de la nouvelle pop-up")
                    try:
                        show_recording()
                        self.logger.info("[DEBUG] Pop-up d'enregistrement affichée avec succès")
                        # Ne pas afficher de notification si la pop-up fonctionne
                    except Exception as e:
                        self.logger.error(f"[DEBUG] Erreur affichage pop-up: {e}", exc_info=True)
                        # Fallback sur notification en cas d'erreur pop-up
                        if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                            self.notification_manager.show_status_notification("recording")
                else:
                    self.logger.info("[DEBUG] Pop-up désactivée, utilisation des notifications")
                    # Utiliser les notifications si pop-up désactivée
                    if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                        self.notification_manager.show_status_notification("recording")
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage de l'enregistrement: {e}", exc_info=True)
            # Cacher la pop-up en cas d'erreur
            ui_config = self.config.get("ui", {})
            if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                hide_popup()
            # Afficher notification d'erreur
            if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                self.notification_manager.show_status_notification("error", str(e))
            self.is_recording = False

    def _process_recording(self) -> None:
        """Traite l'enregistrement audio : transcription et injection"""
        if self.is_processing:
            return

        self.is_processing = True
        self.is_recording = False

        # Changer la pop-up en mode traitement (priorité sur notifications)
        ui_config = self.config.get("ui", {})
        if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
            show_processing()
            # Ne pas afficher de notification si la pop-up fonctionne
        else:
            # Utiliser les notifications si pop-up désactivée
            if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                self.notification_manager.show_status_notification("processing")

        try:
            # Arrêter l'enregistrement et récupérer l'audio
            if not self.audio_capture:
                self.logger.error("Module de capture audio non initialisé")
                if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                    self.notification_manager.show_status_notification("error", "Module de capture audio non initialisé")
                return

            audio_data = self.audio_capture.stop_recording()

            if len(audio_data) == 0:
                self.logger.warning("Aucun audio capturé")
                self.is_processing = False
                # Cacher la pop-up si pas d'audio
                ui_config = self.config.get("ui", {})
                if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                    hide_popup()
                else:
                    # Utiliser notification si pop-up désactivée
                    if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                        self.notification_manager.show_status_notification("error", "Aucun audio capturé")
                return

            # Transcrire avec Whisper
            if not self.transcriber:
                self.logger.error("Module Whisper non initialisé")
                # Cacher la pop-up en cas d'erreur
                ui_config = self.config.get("ui", {})
                if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                    hide_popup()
                else:
                    # Utiliser notification si pop-up désactivée
                    if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                        self.notification_manager.show_status_notification("error", "Module Whisper non initialisé")
                return

            # Charger le modèle si nécessaire
            self.transcriber.load_model()

            # Transcrire
            self.logger.info("Transcription en cours...")
            text = self.transcriber.transcribe(audio_data, sample_rate=self.audio_capture.sample_rate)
            self.logger.info(f"Texte transcrit: '{text}' (longueur: {len(text) if text else 0})")

            # Correction orthographique et grammaticale (post-traitement)
            if text and self.text_corrector:
                self.logger.info("Correction du texte en cours...")
                original_text = text
                text = self.text_corrector.correct_text(text)
                self.logger.info(f"Texte corrigé: '{original_text}' -> '{text}'")

            if text and text.strip():
                # Injecter le texte
                if self.text_injector:
                    self.logger.info(f"Injection du texte: '{text[:50]}...' (longueur: {len(text)})")
                    
                    # Utiliser la méthode robuste d'injection
                    success = self.text_injector.inject_text_robust(text)
                    
                    if success:
                        self.logger.info("Texte injecté avec succès")
                        # Afficher notification de succès (priorité à la pop-up)
                        ui_config = self.config.get("ui", {})
                        if not (RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True)):
                            # Utiliser notification seulement si pop-up désactivée
                            if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                                self.notification_manager.show_status_notification("ready", f"Texte: {text[:100]}...")
                    else:
                        self.logger.error("Échec de l'injection du texte")
                        # Cacher la pop-up en cas d'erreur
                        ui_config = self.config.get("ui", {})
                        if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                            hide_popup()
                        # Afficher notification d'erreur
                        if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                            self.notification_manager.show_status_notification("error", "Échec de l'injection du texte")
                else:
                    self.logger.error("Module d'injection de texte non initialisé")
                    # Cacher la pop-up en cas d'erreur
                    ui_config = self.config.get("ui", {})
                    if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                        hide_popup()
                    # Afficher notification d'erreur
                    if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                        self.notification_manager.show_status_notification("error", "Module d'injection de texte non initialisé")
            else:
                self.logger.warning(f"Aucun texte transcrit ou texte vide. Texte brut: '{text}'")
                # Cacher la pop-up si pas de texte
                ui_config = self.config.get("ui", {})
                if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                    hide_popup()
                else:
                    # Utiliser notification si pop-up désactivée
                    if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                        self.notification_manager.show_status_notification("error", "Aucun texte transcrit")

        except Exception as e:
            self.logger.error(f"Erreur lors du traitement de l'enregistrement: {e}", exc_info=True)

        finally:
            self.is_processing = False
            # Cacher la pop-up à la fin du traitement
            ui_config = self.config.get("ui", {})
            if RECORDING_POPUP_AVAILABLE and ui_config.get("show_recording_popup", True):
                hide_popup()

    def start(self) -> None:
        """Démarre le service"""
        if self.running:
            self.logger.warning("Service déjà en cours d'exécution")
            return

        try:
            # Charger le modèle Whisper (peut prendre du temps)
            self.logger.info("Chargement du modèle Whisper (cela peut prendre quelques instants)...")
            if self.transcriber:
                self.transcriber.load_model()

            # Enregistrer le raccourci clavier
            hotkey_config = self.config.get("hotkey", {})
            modifiers = hotkey_config.get("modifiers", ["ctrl", "shift"])
            key = hotkey_config.get("key", "v")

            if self.hotkey_manager:
                self.hotkey_manager.register_hotkey(
                    modifiers=modifiers,
                    key=key,
                    callback=self._on_hotkey_pressed,
                    name="Transcription vocale"
                )

            self.running = True
            self.logger.info("Service démarré avec succès")
            self.logger.info(f"Appuyez sur {'+'.join(modifiers)}+{key} pour démarrer/arrêter la transcription")
            self.logger.info("Appuyez sur Ctrl+C pour arrêter le service")

            # Afficher une notification que le service est démarré
            if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                self.notification_manager.show_status_notification("running", 
                    f"Raccourci: {'+'.join(modifiers)}+{key}")

        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage du service: {e}", exc_info=True)
            if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                self.notification_manager.show_status_notification("error", str(e))
            raise

    def stop(self) -> None:
        """Arrête le service"""
        if not self.running:
            return

        self.logger.info("Arrêt du service...")
        self.running = False

        # Arrêter l'enregistrement si en cours
        if self.is_recording and self.audio_capture:
            self.audio_capture.stop_recording()

        # Nettoyer la popup
        if RECORDING_POPUP_AVAILABLE:
            try:
                cleanup_popup()
                self.logger.info("Pop-up nettoyée")
            except Exception as e:
                self.logger.warning(f"Erreur nettoyage popup: {e}")

        # Désenregistrer les raccourcis
        if self.hotkey_manager:
            self.hotkey_manager.unregister_all()

        self.logger.info("Service arrêté")
        
        # Afficher une notification d'arrêt
        if NOTIFICATIONS_AVAILABLE and self.notification_manager:
            self.notification_manager.show_notification(
                "Whisper STT - Arrêt",
                "Le service Whisper STT a été arrêté.",
                icon="info"
            )

    def run(self) -> None:
        """Boucle principale du service"""
        self.start()

        try:
            # Boucle principale
            while self.running:
                time.sleep(0.1)

                # La capture audio se fait en continu via le callback
                # L'arrêt se fait via le raccourci clavier

        except KeyboardInterrupt:
            self.logger.info("Interruption clavier détectée")
        except Exception as e:
            self.logger.error(f"Erreur dans la boucle principale: {e}", exc_info=True)
            if NOTIFICATIONS_AVAILABLE and self.notification_manager:
                self.notification_manager.show_status_notification("error", str(e))
        finally:
            self.stop()


def main():
    """Point d'entrée principal"""
    import argparse
    
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Service de transcription vocale VTT')
    parser.add_argument('--config', '-c', 
                       help='Chemin vers le fichier de configuration JSON',
                       default=None)
    
    args = parser.parse_args()
    
    # Déterminer le chemin du fichier de configuration
    if args.config and Path(args.config).exists():
        config_path = Path(args.config)
        print(f"[INFO] Utilisation de la configuration: {config_path}")
    else:
        # Fallback vers la configuration par défaut
        script_dir = Path(__file__).parent
        config_path = script_dir / "config.json"
        if not config_path.exists():
            print(f"[WARNING] Configuration par défaut non trouvée: {config_path}")
            print("[INFO] Utilisation des valeurs par défaut")

    # Créer et démarrer le service
    service = WhisperSTTService(config_path=str(config_path))
    service.run()


if __name__ == "__main__":
    main()
