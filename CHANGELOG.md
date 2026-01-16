# Journal des Modifications - Whisper STT

Ce fichier documente toutes les modifications significatives apportées au projet Whisper STT.

## [2.1.0] - 2026-01-15

### Ajouté

- **Système de notifications complet** : Nouveau module `src/notifications.py` avec :
  - Notifications pop-up (MessageBox Windows)
  - Notifications balloon (bulles Windows avec win10toast)
  - Notifications standardisées pour tous les états
  - Gestion des threads pour les notifications non-bloquantes

- **Notifications d'état** :
  - Notification de démarrage du service
  - Notification d'enregistrement en cours (🎤)
  - Notification de traitement en cours (⏳)
  - Notification de texte prêt (✅)
  - Notification d'erreurs (❌)
  - Notification d'arrêt du service

- **Script de lancement amélioré** : `run_whisper.bat` avec :
  - Détection automatique de pipx
  - Installation préférentielle avec pipx
  - Fallback sur pip si pipx non disponible
  - Vérification complète des dépendances
  - Vérification de la version de Python
  - Messages utilisateur clairs
  - Configuration automatique de l'environnement

- **Vérification de la version de Python** : Nouveau module `check_python_version.py` avec :
  - Détection de la version de Python
  - Vérification de compatibilité
  - Suggestions d'installation
  - Détection des versions multiples
  - Conseils pour les versions optimales

- **Documentation mise à jour** :
  - Section "Notifications et Feedback Utilisateur" dans README.md
  - Section "Dernières Modifications" dans README.md
  - Configuration des notifications dans la documentation
  - Instructions d'utilisation des notifications
  - Section "Problèmes de version de Python" dans le dépannage
  - Mise à jour des prérequis avec les versions recommandées

- **Fichiers de test** :
  - `test_notifications.py` - Script de test complet des notifications
  - Tests pour tous les types de notifications
  - `check_python_version.py` - Script de vérification de version

### Modifié

- **src/main.py** :
  - Ajout des imports pour le module de notifications
  - Initialisation du gestionnaire de notifications
  - Ajout des appels aux notifications dans les méthodes clés :
    - `run()` - Notification d'erreur en cas d'exception
    - `start()` - Notification de service démarré
    - `_start_recording()` - Notification d'enregistrement
    - `_process_recording()` - Notifications de traitement et prêt
    - `stop()` - Notification d'arrêt
  - Gestion des erreurs améliorée avec notifications

- **README.md** :
  - Ajout de la section sur les notifications
  - Mise à jour des instructions d'installation
  - Documentation des nouvelles fonctionnalités
  - Journal des modifications intégré

- **Configuration** :
  - Ajout de la section `notifications` dans la documentation
  - Options de configuration pour les notifications

### Améliorations Techniques

- **Gestion des dépendances** :
  - Utilisation préférentielle de pipx pour les installations
  - Meilleure isolation des environnements
  - Évite les conflits de dépendances

- **Expérience utilisateur** :
  - Feedback visuel à chaque étape
  - Plus besoin de deviner l'état de l'application
  - Messages d'erreur clairs et utiles

- **Robustesse** :
  - Fallback sur MessageBox si win10toast non disponible
  - Gestion des erreurs avec notifications
  - Threads séparés pour éviter le blocage

## [2.0.0] - 2026-01-10

### Ajouté

- **Support Faster-Whisper** : Intégration de l'implémentation optimisée
- **Configuration flexible** : Choix entre Whisper standard et Faster-Whisper
- **Détection automatique** : Fallback sur Whisper si Faster-Whisper non disponible
- **Documentation Faster-Whisper** : Guides d'installation et d'utilisation

### Modifié

- **src/main.py** : Ajout de la détection et du chargement de Faster-Whisper
- **config.json** : Ajout de l'option `engine` pour choisir le moteur
- **README.md** : Documentation mise à jour pour Faster-Whisper

## [1.0.0] - 2025-12-01

### Ajouté

- **Version initiale** : Service Whisper STT de base
- **Transcription vocale** : Utilisation de Whisper standard
- **Injection de texte** : Fonctionnalité d'injection dans les applications
- **Raccourcis clavier** : Activation par raccourci clavier
- **Détection de silence** : Arrêt automatique de l'enregistrement

### Fonctionnalités Initiales

- Capture audio avec sounddevice
- Transcription avec Whisper
- Injection de texte avec pyautogui
- Gestion des raccourcis avec pynput
- Configuration via config.json

## Format du Journal des Modifications

Ce journal suit les conventions suivantes :

- **Ajouté** : Pour les nouvelles fonctionnalités
- **Modifié** : Pour les modifications de fonctionnalités existantes
- **Supprimé** : Pour les fonctionnalités supprimées
- **Corrigé** : Pour les corrections de bugs
- **Sécurité** : Pour les corrections de vulnérabilités
- **Améliorations Techniques** : Pour les améliorations non visibles par l'utilisateur

Chaque version suit le format : `[MAJEUR.MINEUR.PATCH]` - `AAAA-MM-JJ`

- **MAJEUR** : Modifications incompatibles avec les versions précédentes
- **MINEUR** : Ajout de fonctionnalités compatibles
- **PATCH** : Corrections de bugs compatibles

## Comment Contribuer

Les contributions sont les bienvenues ! Pour proposer des modifications :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. Pushez sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.