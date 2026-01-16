#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de notifications pour l'application Whisper STT
Gère les pop-ups et notifications visuelles
"""

import threading
import time
import ctypes
import sys
import os
from typing import Optional

class NotificationManager:
    """Gestionnaire des notifications pop-up"""
    
    def __init__(self):
        """Initialise le gestionnaire de notifications"""
        self.notification_thread: Optional[threading.Thread] = None
        self.stop_notification = False
        
    def show_notification(self, title: str, message: str, duration: int = 3, 
                         icon: str = "info", threaded: bool = True):
        """
        Affiche une notification pop-up
        
        Args:
            title: Titre de la notification
            message: Message de la notification
            duration: Durée d'affichage en secondes
            icon: Type d'icône (info, warning, error, success)
            threaded: Si True, affiche dans un thread séparé
        """
        if threaded:
            # Créer un thread pour la notification afin de ne pas bloquer l'application
            self.notification_thread = threading.Thread(
                target=self._show_notification_sync,
                args=(title, message, duration, icon)
            )
            self.notification_thread.daemon = True
            self.notification_thread.start()
        else:
            self._show_notification_sync(title, message, duration, icon)
    
    def _show_notification_sync(self, title: str, message: str, duration: int, icon: str):
        """Affiche une notification de manière synchrone"""
        try:
            # Mapper les types d'icônes
            icon_mapping = {
                "info": 0x40,      # MB_ICONINFORMATION
                "warning": 0x30,   # MB_ICONWARNING
                "error": 0x10,     # MB_ICONERROR
                "success": 0x40    # MB_ICONINFORMATION (utilisé pour succès)
            }
            
            icon_type = icon_mapping.get(icon.lower(), 0x40)  # Par défaut: info
            
            # Utiliser ctypes pour afficher une MessageBox Windows
            ctypes.windll.user32.MessageBoxW(
                None,
                message,
                title,
                icon_type | 0x40000  # MB_SETFOREGROUND pour mettre au premier plan
            )
            
        except Exception as e:
            print(f"Erreur lors de l'affichage de la notification: {e}")
    
    def show_temporary_notification(self, title: str, message: str, duration: int = 3):
        """
        Affiche une notification temporaire qui se ferme automatiquement
        
        Args:
            title: Titre de la notification
            message: Message de la notification
            duration: Durée d'affichage en secondes
        """
        # Pour Windows, nous pouvons utiliser un thread avec un timeout
        def show_timed_notification():
            try:
                # Créer une fenêtre de notification
                import tkinter as tk
                from tkinter import messagebox
                
                root = tk.Tk()
                root.withdraw()  # Masquer la fenêtre principale
                
                # Afficher la notification
                messagebox.showinfo(title, message)
                
            except ImportError:
                # Si tkinter n'est pas disponible, utiliser MessageBox standard
                ctypes.windll.user32.MessageBoxW(
                    None,
                    message,
                    title,
                    0x40  # MB_ICONINFORMATION
                )
            except Exception as e:
                print(f"Erreur lors de la notification temporaire: {e}")
        
        # Lancer dans un thread séparé
        notification_thread = threading.Thread(target=show_timed_notification)
        notification_thread.daemon = True
        notification_thread.start()
    
    def show_status_notification(self, status: str, details: str = ""):
        """
        Affiche une notification d'état standardisée
        
        Args:
            status: État actuel (starting, running, recording, processing, error)
            details: Détails supplémentaires
        """
        status_messages = {
            "starting": {
                "title": "Whisper STT - Démarrage",
                "message": f"L'application Whisper STT est en cours de démarrage...\n{details}",
                "icon": "info"
            },
            "running": {
                "title": "Whisper STT - En cours",
                "message": f"L'application Whisper STT est en cours d'exécution.\nAppuyez sur Ctrl+Alt+7 pour démarrer l'enregistrement.\n{details}",
                "icon": "success"
            },
            "recording": {
                "title": "Whisper STT - Enregistrement",
                "message": f"🎤 Enregistrement audio en cours...\nAppuyez à nouveau sur Ctrl+Alt+7 pour arrêter.\n{details}",
                "icon": "info"
            },
            "processing": {
                "title": "Whisper STT - Traitement",
                "message": f"⏳ Traitement de l'audio enregistré...\n{details}",
                "icon": "info"
            },
            "ready": {
                "title": "Whisper STT - Prêt",
                "message": f"✅ Texte prêt à être injecté !\n{details}",
                "icon": "success"
            },
            "error": {
                "title": "Whisper STT - Erreur",
                "message": f"❌ Une erreur est survenue:\n{details}",
                "icon": "error"
            }
        }
        
        config = status_messages.get(status, status_messages["running"])
        self.show_notification(config["title"], config["message"], icon=config["icon"])
    
    def show_balloon_notification(self, title: str, message: str):
        """
        Affiche une notification de type balloon (bulle Windows)
        
        Args:
            title: Titre de la notification
            message: Message de la notification
        """
        try:
            # Utiliser win10toast pour les notifications de type balloon
            from win10toast import ToastNotifier
            
            toaster = ToastNotifier()
            toaster.show_toast(
                title,
                message,
                duration=5,
                threaded=True
            )
            
        except ImportError:
            # Si win10toast n'est pas disponible, utiliser une MessageBox
            self.show_notification(title, message, icon="info")
        except Exception as e:
            print(f"Erreur lors de la notification balloon: {e}")
            self.show_notification(title, message, icon="info")

# Instance globale du gestionnaire de notifications
notification_manager = NotificationManager()

if __name__ == "__main__":
    # Test des notifications
    print("Test des notifications...")
    
    notif = NotificationManager()
    
    print("Affichage d'une notification de test...")
    notif.show_status_notification("running", "Test de notification")
    
    print("Test terminé.")