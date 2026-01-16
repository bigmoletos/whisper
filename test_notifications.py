#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de test pour les notifications
"""

import time
from src.notifications import NotificationManager

def test_notifications():
    """Teste toutes les notifications"""
    print("Test des notifications Whisper STT")
    print("=" * 40)
    
    notif = NotificationManager()
    
    # Test 1: Notification de démarrage
    print("1. Test notification de démarrage...")
    notif.show_status_notification("starting", "Initialisation en cours")
    time.sleep(1)
    
    # Test 2: Notification en cours d'exécution
    print("2. Test notification en cours d'exécution...")
    notif.show_status_notification("running", "Raccourci: Ctrl+Alt+7")
    time.sleep(1)
    
    # Test 3: Notification d'enregistrement
    print("3. Test notification d'enregistrement...")
    notif.show_status_notification("recording")
    time.sleep(1)
    
    # Test 4: Notification de traitement
    print("4. Test notification de traitement...")
    notif.show_status_notification("processing")
    time.sleep(1)
    
    # Test 5: Notification prêt
    print("5. Test notification prêt...")
    notif.show_status_notification("ready", "Texte: Bonjour, ceci est un test")
    time.sleep(1)
    
    # Test 6: Notification d'erreur
    print("6. Test notification d'erreur...")
    notif.show_status_notification("error", "Erreur de connexion au microphone")
    time.sleep(1)
    
    # Test 7: Notification balloon (bulle Windows)
    print("7. Test notification balloon...")
    notif.show_balloon_notification("Whisper STT", "Test de notification de type balloon")
    time.sleep(2)
    
    print("\nTous les tests de notifications sont terminés !")
    print("Vous devriez avoir vu plusieurs types de notifications apparaître.")

if __name__ == "__main__":
    test_notifications()