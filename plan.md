
Composants techniques
1. Installation des dépendances
Python 3.10+ avec pip
ffmpeg (pour le traitement audio)
openai-whisper (modèle medium ou large)
pyaudio ou sounddevice (capture audio)
pyautogui ou pywin32 (injection de texte)
keyboard ou pynput (gestion des raccourcis clavier)
2. Capture audio (audio_capture.py)
Utilise sounddevice ou pyaudio pour capturer l'audio en temps réel
Enregistre des segments audio (par exemple 3-5 secondes)
Gère le silence pour détecter la fin de la parole
Sauvegarde temporairement les segments audio
3. Transcription Whisper (whisper_transcriber.py)
Charge le modèle Whisper (medium ou large) au démarrage
Traite les segments audio capturés
Retourne le texte transcrit
Gère le cache du modèle pour éviter les rechargements
4. Injection de texte (text_injector.py)
Détecte la fenêtre active
Utilise pyautogui ou pywin32 pour simuler la frappe
Alternative : copie dans le presse-papiers et simule Ctrl+V
Gère les caractères spéciaux et l'encodage
5. Service principal (main.py)
Boucle principale qui écoute le raccourci clavier
Coordonne la capture audio, transcription et injection
Gère l'état (actif/inactif)
Logging pour le débogage
6. Configuration (config.json)
Modèle Whisper à utiliser (medium/large)
Raccourci clavier personnalisable
Paramètres audio (fréquence d'échantillonnage, durée des segments)
Langue de transcription
Workflow
Oui
Non
Non
Oui
Démarrage du service
Chargement modèle Whisper
Attente raccourci clavier
Raccourci pressé?
Début capture audio
Enregistrement segment audio
Fin de parole détectée?
Transcription Whisper
Injection texte dans champ actif
Étapes d'implémentation
Setup initial : Créer la structure de fichiers et requirements.txt
Module capture audio : Implémenter la capture en temps réel avec gestion du silence
Module Whisper : Intégrer Whisper avec chargement du modèle et transcription
Module injection : Implémenter l'injection de texte dans le champ actif
Service principal : Coordonner tous les modules avec gestion des raccourcis
Configuration : Système de configuration JSON avec valeurs par défaut
Scripts d'installation : Scripts batch pour faciliter l'installation sur Windows
Documentation : README avec instructions d'installation et d'usage
Considérations techniques
Performance : Le modèle large nécessite ~10GB RAM et un GPU recommandé
Latence : La transcription peut prendre 1-3 secondes selon le modèle
Audio : Configuration du microphone par défaut du système
Sécurité : Aucune donnée audio n'est envoyée en ligne (tout est local)
Compatibilité : Fonctionne avec toutes les applications Windows standard
Dépendances principales
openai-whisper : Modèle de transcription
sounddevice ou pyaudio : Capture audio
numpy : Traitement des données audio
pyautogui ou pywin32 : Injection de texte
keyboard ou pynput : Gestion des raccourcis clavier
ffmpeg-python : Traitement audio (si nécessaire)
Notes d'implémentation
Le modèle Whisper sera téléchargé automatiquement au premier lancement
Le service peut être lancé au démarrage de Windows
Les logs seront écrits dans un fichier pour le débogage
Configuration par défaut : modèle medium, raccourci Ctrl+Shift+V