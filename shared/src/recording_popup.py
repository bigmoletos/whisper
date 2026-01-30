"""
Pop-up discrète d'enregistrement pour VTT
Version thread-safe avec nettoyage automatique
"""

import tkinter as tk
import threading
import time
import queue
from typing import Optional


class ThreadSafeRecordingPopup:
    """Pop-up thread-safe pour l'enregistrement avec nettoyage automatique"""
    
    def __init__(self):
        self.window: Optional[tk.Tk] = None
        self.is_visible = False
        self.command_queue = queue.Queue()
        self.ui_thread = None
        self.running = False
        self.lock = threading.Lock()
        
    def _cleanup_thread(self):
        """Nettoie le thread UI s'il est mort"""
        with self.lock:
            if self.ui_thread and not self.ui_thread.is_alive():
                self.ui_thread = None
                self.running = False
                self.window = None
                self.is_visible = False
        
    def _ui_worker(self):
        """Worker thread pour l'interface utilisateur"""
        try:
            # Créer la fenêtre dans ce thread
            self.window = tk.Tk()
            self.window.withdraw()  # Cacher initialement
            self.window.title("🎤 VTT Enregistrement")
            self.window.geometry("220x90")
            self.window.resizable(False, False)
            self.window.attributes("-topmost", True)
            self.window.configure(bg="#2d2d2d")
            
            # Positionnement
            screen_width = self.window.winfo_screenwidth()
            x = screen_width - 240
            y = 20
            self.window.geometry(f"220x90+{x}+{y}")
            
            # Traiter les commandes
            def process_commands():
                try:
                    while not self.command_queue.empty():
                        command = self.command_queue.get_nowait()
                        
                        if command == "show_recording":
                            self._show_recording_ui()
                        elif command == "show_processing":
                            self._show_processing_ui()
                        elif command == "hide":
                            self._hide_ui()
                        elif command == "quit":
                            self.running = False
                            return
                            
                except queue.Empty:
                    pass
                except Exception as e:
                    print(f"Erreur process_commands: {e}")
                
                if self.running:
                    self.window.after(50, process_commands)
            
            # Démarrer le traitement des commandes
            self.running = True
            process_commands()
            
            # Boucle principale tkinter
            self.window.mainloop()
            
        except Exception as e:
            print(f"Erreur UI thread: {e}")
        finally:
            with self.lock:
                self.running = False
                self.window = None
                self.is_visible = False
    
    def _show_recording_ui(self):
        """Affiche l'interface d'enregistrement"""
        if not self.window:
            return
            
        try:
            # Nettoyer le contenu existant
            for widget in self.window.winfo_children():
                widget.destroy()
            
            # Créer le nouveau contenu
            frame = tk.Frame(self.window, bg="#2d2d2d", padx=15, pady=15)
            frame.pack(fill="both", expand=True)
            
            status = tk.Label(frame, text="🔴 ENREGISTREMENT", 
                            font=("Arial", 11, "bold"), 
                            fg="#ff4444", bg="#2d2d2d")
            status.pack()
            
            info = tk.Label(frame, text="Ctrl+Alt+7 pour arrêter", 
                          font=("Arial", 9), 
                          fg="#cccccc", bg="#2d2d2d")
            info.pack(pady=(5, 0))
            
            # Afficher la fenêtre
            self.window.deiconify()
            self.window.lift()
            self.window.attributes("-topmost", True)  # Forcer au premier plan
            self.is_visible = True
            
        except Exception as e:
            print(f"Erreur show_recording_ui: {e}")
    
    def _show_processing_ui(self):
        """Affiche l'interface de traitement"""
        if not self.window or not self.is_visible:
            return
            
        try:
            # Nettoyer le contenu existant
            for widget in self.window.winfo_children():
                widget.destroy()
            
            # Créer le nouveau contenu
            frame = tk.Frame(self.window, bg="#2d2d2d", padx=15, pady=15)
            frame.pack(fill="both", expand=True)
            
            status = tk.Label(frame, text="⚡ TRANSCRIPTION", 
                            font=("Arial", 11, "bold"), 
                            fg="#44ff44", bg="#2d2d2d")
            status.pack()
            
            info = tk.Label(frame, text="Traitement en cours...", 
                          font=("Arial", 9), 
                          fg="#cccccc", bg="#2d2d2d")
            info.pack(pady=(5, 0))
            
            # S'assurer que la fenêtre reste visible
            self.window.lift()
            self.window.attributes("-topmost", True)
            
        except Exception as e:
            print(f"Erreur show_processing_ui: {e}")
    
    def _hide_ui(self):
        """Cache l'interface"""
        if not self.window:
            return
            
        try:
            self.window.withdraw()
            self.is_visible = False
        except Exception as e:
            print(f"Erreur hide_ui: {e}")
    
    def show_recording(self):
        """Affiche la pop-up d'enregistrement (thread-safe)"""
        self._cleanup_thread()  # Nettoyer d'abord
        
        if not self.running:
            # Démarrer le thread UI si nécessaire
            if not self.ui_thread or not self.ui_thread.is_alive():
                self.ui_thread = threading.Thread(target=self._ui_worker, daemon=True)
                self.ui_thread.start()
                time.sleep(0.3)  # Laisser plus de temps au thread de démarrer
        
        # NETTOYAGE COMPLET de la queue pour éviter les interférences
        command_count = 0
        while not self.command_queue.empty():
            try:
                old_command = self.command_queue.get_nowait()
                command_count += 1
            except queue.Empty:
                break
        
        if command_count > 0:
            print(f"[DEBUG] Nettoyé {command_count} anciennes commandes de la queue")
        
        # Attendre un peu pour s'assurer que le thread est prêt
        time.sleep(0.1)
        
        self.command_queue.put("show_recording")
        print("[DEBUG] Commande show_recording envoyée")
    
    def show_processing(self):
        """Change en mode traitement (thread-safe)"""
        if self.running:
            self.command_queue.put("show_processing")
    
    def hide(self):
        """Cache la pop-up (thread-safe)"""
        if self.running:
            self.command_queue.put("hide")
    
    def cleanup(self):
        """Nettoie complètement la popup"""
        with self.lock:
            if self.running:
                self.command_queue.put("quit")
            
            if self.ui_thread and self.ui_thread.is_alive():
                # Attendre un peu que le thread se termine
                self.ui_thread.join(timeout=1.0)
            
            self.ui_thread = None
            self.running = False
            self.window = None
            self.is_visible = False


# Instance globale
_popup = None


def show_recording() -> None:
    """Affiche la pop-up d'enregistrement"""
    global _popup
    try:
        if _popup is None:
            _popup = ThreadSafeRecordingPopup()
        _popup.show_recording()
    except Exception as e:
        print(f"Erreur show_recording: {e}")


def show_processing() -> None:
    """Change en mode traitement"""
    global _popup
    try:
        if _popup:
            _popup.show_processing()
    except Exception as e:
        print(f"Erreur show_processing: {e}")


def hide_popup() -> None:
    """Cache la pop-up"""
    global _popup
    try:
        if _popup:
            _popup.hide()
    except Exception as e:
        print(f"Erreur hide_popup: {e}")


def cleanup_popup() -> None:
    """Nettoie complètement la popup (pour redémarrage)"""
    global _popup
    try:
        if _popup:
            _popup.cleanup()
            _popup = None
    except Exception as e:
        print(f"Erreur cleanup_popup: {e}")


if __name__ == "__main__":
    # Test simple
    print("Test pop-up thread-safe avec nettoyage...")
    
    # Test 1
    show_recording()
    time.sleep(2)
    show_processing()
    time.sleep(1)
    hide_popup()
    time.sleep(1)
    
    # Test 2 (simulation du problème)
    print("Test 2...")
    show_recording()
    time.sleep(2)
    show_processing()
    time.sleep(1)
    hide_popup()
    
    # Nettoyage
    cleanup_popup()
    
    print("Test terminé.")