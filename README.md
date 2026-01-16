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
- **⚡ Ultra-rapide avec Whisper.cpp** : Latence < 0.5 seconde avec Whisper.cpp (implémentation C++)
- **🔔 Notifications visuelles** : Pop-ups et notifications pour indiquer l'état du service (enregistrement, traitement, prêt, erreurs)
- **📋 Feedback utilisateur** : L'utilisateur sait exactement ce qui se passe à chaque étape
- **🎯 Interface plus intuitive** : Plus besoin de deviner si l'application fonctionne

## Prérequis

### Logiciels requis

1. **Python 3.11 ou 3.12 (recommandé)** ou **Python 3.10 (minimum)**
   - **Version recommandée** : Python 3.11.4 ou 3.12.0
   - **Version minimale** : Python 3.10.0
   - **À éviter** : Python 3.14+ (problèmes de compatibilité avec faster-whisper)
   - Téléchargement : https://www.python.org/downloads/
   - Assurez-vous de cocher "Add Python to PATH" lors de l'installation
   
   **Méthodes d'installation** :
   ```bash
   # Via winget (recommandé pour Windows)
   winget install Python.Python.3.11
   
   # Via Microsoft Store
   Recherchez "Python 3.11" dans le Microsoft Store
   
   # Via chocolatey
   choco install python --version=3.11.4
   ```

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

## Notifications et Feedback Utilisateur

L'application inclut maintenant un système complet de notifications visuelles pour améliorer l'expérience utilisateur :

### Types de notifications

1. **🎤 Enregistrement en cours** : Apparaît lorsque vous commencez à enregistrer (Ctrl+Alt+7)
   - Indique que le microphone est actif
   - Rappelle le raccourci pour arrêter

2. **⏳ Traitement en cours** : Apparaît pendant la transcription
   - Indique que Whisper est en train de transcrire votre audio
   - Montre que l'application travaille

3. **✅ Texte prêt** : Apparaît lorsque la transcription est terminée
   - Affiche le texte transcrit
   - Indique que le texte est prêt à être injecté

4. **❌ Erreurs** : Apparaît en cas de problème
   - Affiche des messages d'erreur clairs
   - Aide au diagnostic des problèmes

5. **ℹ️ Informations** : Notifications générales
   - État du service (démarrage, arrêt)
   - Conseils d'utilisation

### Exemple de workflow avec notifications

1. **Démarrage** → Notification "Service démarré"
2. **Ctrl+Alt+7** → Notification "Enregistrement en cours 🎤"
3. **Relâcher Ctrl+Alt+7** → Notification "Traitement en cours ⏳"
4. **Transcription terminée** → Notification "Texte prêt ✅"
5. **Texte injecté** → Le texte apparaît dans votre application

### Désactivation des notifications

Si les notifications sont trop intrusives, vous pouvez :
- Modifier le code dans `src/notifications.py`
- Commenter les appels aux notifications dans `src/main.py`
- Utiliser le mode silencieux (à implémenter)

## Installation

### Étape 1 : Cloner ou télécharger le projet

```bash
cd C:\programmation\whisper_local_STT
```

### Étape 2 : Exécuter le script d'installation

#### Nouvelle méthode recommandée (avec notifications)

Double-cliquez sur `run_whisper.bat` ou exécutez dans un terminal :

```bash
run_whisper.bat
```

Ce script amélioré :
- Vérifie que Python est installé
- Utilise **pipx** (si disponible) ou **pip** pour les installations
- Installe automatiquement les dépendances manquantes
- Configure correctement l'environnement
- Lance l'application avec le système de notifications
- Affiche des messages clairs à chaque étape

#### Méthode originale (sans notifications)

Double-cliquez sur `scripts\install.bat` ou exécutez dans un terminal :

```bash
scripts\install.bat
```

Le script original va :
- Vérifier que Python est installé
- Mettre à jour pip
- Vérifier la présence de ffmpeg
- Installer toutes les dépendances Python nécessaires

### Étape 3 : Vérifier l'installation

Assurez-vous que tous les modules sont installés :

```bash
python -c "import whisper; import sounddevice; import pyautogui; import keyboard; print('OK')"
```

## Dernières Modifications et Mises à Jour

### Version 2.1 - Système de Notifications (📅 15/01/2026)

**Nouveautés :**
- ✨ **Système de notifications complet** : Pop-ups visuels pour toutes les étapes
- 🔔 **Notifications d'état** : Enregistrement, traitement, prêt, erreurs
- 🎯 **Meilleure expérience utilisateur** : Feedback clair à chaque étape
- 📋 **Notifications balloon** : Moins intrusives que les MessageBox
- 🔧 **Script de lancement amélioré** : `run_whisper.bat` avec gestion automatique

**Fichiers modifiés :**
- `src/main.py` - Ajout des appels aux notifications
- `src/notifications.py` - Nouveau module de gestion des notifications
- `run_whisper.bat` - Nouveau script de lancement avec pipx
- `README.md` - Documentation mise à jour

**Fichiers ajoutés :**
- `src/notifications.py` - Module complet de notifications
- `run_whisper.bat` - Script de lancement amélioré
- `test_notifications.py` - Script de test des notifications

**Améliorations techniques :**
- Utilisation de `pipx` pour les installations (meilleure pratique)
- Gestion des erreurs améliorée avec notifications
- Threads séparés pour les notifications (non-bloquantes)
- Support des notifications Windows 10 (win10toast)
- Fallback sur MessageBox si win10toast non disponible

### Version 2.0 - Faster-Whisper (📅 10/01/2026)

**Nouveautés :**
- ⚡ **Faster-Whisper** : Transcription 2-4x plus rapide
- 🎯 **Configuration flexible** : Choix entre Whisper standard et Faster-Whisper
- 📊 **Meilleures performances** : Latence réduite pour le temps réel

## Dépannage et Solutions

### Problèmes de version de Python

**Symptômes** : Erreurs de compilation, problèmes avec `faster-whisper`, messages "version incompatible"

**Solutions** :

#### 1. Vérifier votre version de Python
```bash
python --version
# Ou pour voir toutes les versions disponibles
py --list
```

#### 2. Utiliser une version spécifique de Python
Si vous avez plusieurs versions installées :
```bash
# Pour Python 3.11
py -3.11 run_whisper.bat

# Pour Python 3.12
py -3.12 run_whisper.bat
```

#### 3. Installer la bonne version de Python
```bash
# Via winget (recommandé)
winget install Python.Python.3.11

# Via le site officiel
# Téléchargez depuis https://www.python.org/downloads/
```

#### 4. Problèmes spécifiques à Python 3.14+
Si vous devez utiliser Python 3.14+ :
```bash
# Solution 1: Utiliser Whisper standard au lieu de Faster-Whisper
# Modifiez config.json:
{
  "whisper": {
    "engine": "whisper",  // Au lieu de "faster-whisper"
    "model": "medium",
    "language": "fr",
    "device": "cpu"
  }
}

# Solution 2: Installer avec des options spécifiques
pip install faster-whisper --no-build-isolation

# Solution 3: Installer une version spécifique
pip install faster-whisper==1.2.1
```

### Problèmes d'installation de faster-whisper

Si vous rencontrez des erreurs lors de l'installation de `faster-whisper`, voici plusieurs solutions :

#### 1. Problème de compilation avec Python 3.14

**Symptômes** : Erreurs de compilation Cython, problèmes avec `av`

**Solutions** :
```bash
# Solution 1: Utiliser Python 3.11 ou 3.12 (recommandé)
py -3.11 run_whisper.bat

# Solution 2: Installer avec --no-build-isolation
pip install faster-whisper --no-build-isolation

# Solution 3: Installer une version spécifique
pip install faster-whisper==1.2.1
```

#### 2. Utiliser Whisper standard à la place

Modifiez votre `config.json` :
```json
{
  "whisper": {
    "engine": "whisper",  // Au lieu de "faster-whisper"
    "model": "medium",
    "language": "fr",
    "device": "cpu"
  }
}
```

#### 3. Installer avec conda

Si vous avez conda/anaconda :
```bash
conda install -c conda-forge faster-whisper
```

#### 4. Installer manuellement les dépendances

```bash
# Installer les dépendances de base d'abord
pip install sounddevice numpy win10toast pywin32 pynput

# Puis essayer faster-whisper avec des options spécifiques
pip install --only-binary :all: faster-whisper
```

### Problèmes de microphone

**Symptômes** : "Aucun audio capturé", "Module de capture audio non initialisé"

**Solutions** :
1. Vérifiez que votre microphone est bien connecté
2. Allez dans Paramètres Windows > Système > Son
3. Vérifiez que le bon microphone est sélectionné
4. Testez avec l'application "Enregistreur vocal" de Windows
5. Redémarrez votre ordinateur

### Installation de Whisper.cpp

**Pour installer Whisper.cpp pour des performances optimales** :

#### Méthode 1: Installation via pip (recommandée)
```bash
pip install whisper-cpp-python
```

#### Méthode 2: Installation depuis les sources
```bash
# Cloner le dépôt
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp

# Télécharger le modèle GGML (par exemple medium)
./download-ggml-model.sh medium

# Construire le projet
mkdir build && cd build
cmake .. -DWHISPER_CUDA=ON  # Si vous avez un GPU NVIDIA
make -j

# Installer le package Python
pip install .
```

#### Méthode 3: Utiliser les modèles pré-compilés
```bash
# Télécharger un modèle GGML pré-compilé
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin

# Placer dans le répertoire des modèles
mkdir -p ~/.cache/whisper.cpp/models
mv ggml-medium.bin ~/.cache/whisper.cpp/models/
```

#### Configuration pour Whisper.cpp
```json
{
  "whisper": {
    "engine": "whisper-cpp",
    "model": "medium",
    "language": "fr",
    "device": "cpu"
  }
}
```

### Problèmes de raccourcis clavier

**Symptômes** : Le raccourci Ctrl+Alt+7 ne fonctionne pas

**Solutions** :
1. Vérifiez qu'aucun autre programme n'utilise ce raccourci
2. Modifiez le raccourci dans `config.json` :
```json
"hotkey": {
  "modifiers": ["ctrl", "alt"],
  "key": "space"
}
```
3. Redémarrez l'application

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
  },
  "notifications": {
    "enabled": true,           // Active/désactive les notifications
    "type": "balloon",        // "balloon" ou "popup" ou "both"
    "show_recording": true,    // Notification d'enregistrement
    "show_processing": true,   // Notification de traitement
    "show_ready": true,        // Notification de texte prêt
    "show_errors": true        // Notification d'erreurs
  }
}
```

> **Note** : La section `notifications` est optionnelle. Par défaut, toutes les notifications sont activées.

### Moteurs de Transcription

Le projet supporte plusieurs moteurs de transcription, par ordre de performance :

1. **whisper-cpp** : Implémentation C++ (le plus rapide, ~0.2-0.5s de latence)
   - Nécessite `whisper-cpp-python`
   - Modèles GGML optimisés
   - Support GPU via CUDA

2. **faster-whisper** : Implémentation Python optimisée (~0.5-2s de latence)
   - Nécessite Rust pour l'installation
   - Support multi-thread
   - Quantification int8

3. **whisper** : Implémentation Python standard (~2-5s de latence)
   - Le plus stable
   - Moins de dépendances
   - Bonne précision

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
