# Whisper STT Global pour Windows

Service de transcription vocale en temps réel utilisant Whisper (OpenAI) pour convertir la voix en texte dans n'importe quelle application Windows.

## Description

Ce service permet de transcrire votre voix en texte et d'injecter automatiquement le texte transcrit dans le champ actif de n'importe quelle application (formulaires, chats, éditeurs de texte, etc.). Tout fonctionne localement sur votre machine, sans connexion Internet requise après l'installation initiale.

## Fonctionnalités

- **Transcription vocale en temps réel** : Utilise Whisper ou Faster-Whisper pour une transcription précise et rapide
- **Service global** : Fonctionne dans toutes les applications Windows
- **Raccourci clavier personnalisable** : Active/désactive la transcription avec un raccourci (par défaut: Ctrl+Alt+7)
- **Détection automatique de silence** : Arrête l'enregistrement automatiquement après une période de silence
- **Injection automatique** : Le texte transcrit est automatiquement inséré dans le champ actif
- **100% local** : Aucune donnée n'est envoyée en ligne, tout est traité localement
- **Temps réel avec Faster-Whisper** : Latence < 1 seconde avec Faster-Whisper (nécessite Rust)

## Prérequis

### Logiciels requis

1. **Python 3.10 ou supérieur**
   - Téléchargement : https://www.python.org/downloads/
   - Assurez-vous de cocher "Add Python to PATH" lors de l'installation

2. **ffmpeg**
   - Téléchargement : https://ffmpeg.org/download.html
   - Ou via winget : `winget install ffmpeg`
   - Assurez-vous que ffmpeg est dans votre PATH

3. **Rust** (optionnel, uniquement pour Faster-Whisper)
   - Téléchargement : https://rustup.rs/
   - Ou via winget : `winget install Rustlang.Rustup`
   - Nécessaire uniquement si vous voulez utiliser Faster-Whisper
   - Whisper standard fonctionne sans Rust

### Matériel recommandé

- **RAM** : Minimum 8GB (16GB recommandé pour le modèle large)
- **Processeur** : Processeur moderne (Intel i5/i7 ou AMD équivalent)
- **GPU** (optionnel) : GPU NVIDIA avec CUDA pour accélérer la transcription (le CPU fonctionne aussi)
- **Microphone** : Microphone fonctionnel configuré dans Windows

## Installation

### Étape 1 : Cloner ou télécharger le projet

```bash
cd C:\programmation\whisper_local_STT
```

### Étape 2 : Exécuter le script d'installation

Double-cliquez sur `scripts\install.bat` ou exécutez dans un terminal :

```bash
scripts\install.bat
```

Le script va :
- Vérifier que Python est installé
- Mettre à jour pip
- Vérifier la présence de ffmpeg
- Installer toutes les dépendances Python nécessaires

### Étape 3 : Vérifier l'installation

Assurez-vous que tous les modules sont installés :

```bash
python -c "import whisper; import sounddevice; import pyautogui; import keyboard; print('OK')"
```

## Configuration

Le fichier `config.json` contient toutes les options de configuration :

```json
{
  "whisper": {
    "model": "medium",        // Options: tiny, base, small, medium, large
    "language": "fr",         // Code langue ISO (fr, en, es, etc.)
    "device": "cpu"           // cpu ou cuda (si GPU disponible)
  },
  "audio": {
    "sample_rate": 16000,     // Fréquence d'échantillonnage
    "channels": 1,            // Nombre de canaux (1 = mono)
    "chunk_duration": 3.0,    // Durée des segments audio (secondes)
    "silence_threshold": 0.01, // Seuil de détection de silence
    "silence_duration": 1.5    // Durée de silence pour arrêter (secondes)
  },
  "hotkey": {
    "modifiers": ["ctrl", "shift"], // Modificateurs du raccourci
    "key": "v"                      // Touche principale
  },
  "logging": {
    "level": "INFO",          // DEBUG, INFO, WARNING, ERROR
    "file": "whisper_stt.log" // Fichier de log (optionnel)
  }
}
```

### Modèles Whisper

- **tiny** : Très rapide, moins précis (~1GB RAM)
- **base** : Rapide, précision moyenne (~1GB RAM)
- **small** : Bon compromis vitesse/précision (~2GB RAM)
- **medium** : Très précis, plus lent (~5GB RAM) - **Recommandé**
- **large** : Le plus précis, le plus lent (~10GB RAM)

### Utilisation d'un GPU

Si vous avez un GPU NVIDIA avec CUDA installé, modifiez `config.json` :

```json
{
  "whisper": {
    "device": "cuda"
  }
}
```

Assurez-vous d'avoir installé PyTorch avec support CUDA :
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Utilisation

### Démarrage du service

Double-cliquez sur `scripts\start_service.bat` ou exécutez :

```bash
scripts\start_service.bat
```

Ou directement avec Python :

```bash
python -m src.main
```

### Utilisation de la transcription

1. **Démarrez le service** (voir ci-dessus)
2. **Ouvrez l'application** où vous voulez insérer du texte (navigateur, Word, Notepad, etc.)
3. **Cliquez dans le champ de texte** où vous voulez insérer le texte
4. **Appuyez sur le raccourci** (par défaut: `Ctrl+Shift+V`) pour démarrer l'enregistrement
5. **Parlez** dans votre microphone
6. **Relâchez le raccourci** pour arrêter l'enregistrement et déclencher la transcription
7. Le texte transcrit sera automatiquement inséré dans le champ actif

### Arrêt du service

Appuyez sur `Ctrl+C` dans le terminal où le service tourne.

## Dépannage

### Le service ne démarre pas

- Vérifiez que Python est installé : `python --version`
- Vérifiez que les dépendances sont installées : `pip list | findstr whisper`
- Vérifiez les logs dans `whisper_stt.log`

### Aucun son n'est capturé

- Vérifiez que votre microphone est configuré dans Windows
- Vérifiez les paramètres de confidentialité Windows (Autorisations microphone)
- Testez votre microphone avec l'enregistreur Windows

### La transcription est vide ou incorrecte

- Vérifiez que vous parlez assez fort et clairement
- Ajustez le `silence_threshold` dans `config.json` si nécessaire
- Essayez un modèle plus grand (medium au lieu de small)
- Vérifiez que la langue configurée correspond à votre langue

### Le texte n'est pas injecté

- Vérifiez que le champ de texte est actif (cliquez dedans)
- Certaines applications peuvent bloquer l'injection automatique (applications sécurisées)
- Essayez de copier manuellement le texte depuis les logs

### Erreur "CUDA not available"

- C'est normal si vous n'avez pas de GPU NVIDIA
- Le service fonctionne parfaitement avec le CPU
- Changez `device` à `"cpu"` dans `config.json`

### Le modèle Whisper ne se télécharge pas

- Vérifiez votre connexion Internet (nécessaire uniquement au premier lancement)
- Le modèle est téléchargé dans `~/.cache/whisper/`
- Vous pouvez télécharger manuellement depuis : https://github.com/openai/whisper

## Structure du projet

```
whisper_local_STT/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Service principal
│   ├── audio_capture.py        # Capture audio
│   ├── whisper_transcriber.py  # Transcription Whisper
│   ├── text_injector.py        # Injection de texte
│   └── keyboard_hotkey.py      # Gestion des raccourcis
├── scripts/
│   ├── install.bat             # Script d'installation
│   └── start_service.bat       # Script de démarrage
├── config.json                 # Configuration
├── requirements.txt             # Dépendances Python
└── README.md                   # Cette documentation
```

## Démarrage automatique au boot Windows

### Option 1 : Service Windows (Recommandé)

Pour installer le service Windows qui démarre automatiquement :

1. **Exécutez le script d'installation** (en tant qu'administrateur) :
   ```bash
   scripts\install_windows_service.bat
   ```

2. Le service sera installé et démarré automatiquement au boot.

Voir `GUIDE_DEMARRAGE_AUTOMATIQUE.md` pour plus de détails.

### Option 2 : Dossier Startup (Simple)

1. Créez un raccourci vers `scripts\start_service.bat`
2. Appuyez sur `Win+R`, tapez `shell:startup` et appuyez sur Entrée
3. Copiez le raccourci dans ce dossier

## Sécurité et confidentialité

- **100% local** : Toutes les données audio sont traitées localement
- **Aucune connexion Internet** : Aucune donnée n'est envoyée en ligne (sauf téléchargement initial du modèle)
- **Pas de stockage permanent** : Les enregistrements audio ne sont pas sauvegardés
- **Logs** : Les logs peuvent contenir les textes transcrits, vérifiez le fichier `whisper_stt.log`

## Limitations

- La transcription prend 1-3 secondes selon le modèle et le matériel
- Le modèle large nécessite beaucoup de RAM (~10GB)
- Certaines applications sécurisées peuvent bloquer l'injection automatique de texte
- Fonctionne uniquement sur Windows (pour l'instant)

## Support et contributions

Pour signaler un problème ou proposer une amélioration, veuillez créer une issue dans le dépôt du projet.

## Licence

Ce projet utilise Whisper d'OpenAI qui est sous licence MIT. Voir les licences des dépendances pour plus d'informations.

## Auteur

Bigmoletos - 2025

---

**Note** : Ce service nécessite des privilèges administrateur pour certaines fonctionnalités (raccourcis clavier globaux). Si vous rencontrez des problèmes, essayez de lancer le service en tant qu'administrateur.
