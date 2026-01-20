# Documentation Complète - Voice-to-Text Basic

## Table des matières

1. [Architecture](#architecture)
2. [Installation détaillée](#installation-détaillée)
3. [Configuration](#configuration)
4. [Utilisation avancée](#utilisation-avancée)
5. [Dépannage](#dépannage)
6. [API et personnalisation](#api-et-personnalisation)

---

## Architecture

```
voice-to-text-basic/
├── start.bat           # Script de lancement
├── config.json         # Configuration
├── README.md           # Documentation rapide
├── QUICKSTART.md       # Guide de démarrage
├── CHANGELOG.md        # Historique des versions
└── DOCUMENTATION.md    # Ce fichier
```

Le code source est partagé dans `../../shared/src/` :

- `main.py` - Point d'entrée principal
- `audio_capture.py` - Capture audio du microphone
- `whisper_transcriber.py` - Transcription avec Whisper
- `keyboard_hotkey.py` - Gestion des raccourcis clavier
- `text_injector.py` - Injection du texte transcrit
- `notifications.py` - Notifications système

---

## Installation détaillée

### Prérequis système

1. **Python 3.10+**
   ```bash
   python --version
   # Doit afficher Python 3.10.x ou supérieur
   ```

2. **FFmpeg** (recommandé)
   ```bash
   # Avec Chocolatey
   choco install ffmpeg

   # Ou télécharger depuis https://ffmpeg.org
   ```

### Installation manuelle

```bash
# Créer l'environnement virtuel
python -m venv venv_whisper

# Activer l'environnement
venv_whisper\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Télécharger le modèle Whisper
python download_model.py --model base
```

---

## Configuration

### Fichier config.json

```json
{
    "engine": "whisper",
    "whisper": {
        "model": "base",        // tiny, base, small, medium
        "language": "fr",       // Code langue ISO
        "device": "cpu"         // cpu uniquement pour ce mode
    },
    "audio": {
        "sample_rate": 16000,   // Fréquence d'échantillonnage
        "channels": 1,          // Mono
        "chunk_size": 1024      // Taille des chunks audio
    },
    "hotkeys": {
        "toggle_recording": "ctrl+shift+r",
        "quit": "ctrl+shift+q"
    },
    "output": {
        "auto_paste": true,     // Coller automatiquement
        "notifications": true    // Afficher les notifications
    }
}
```

### Modèles Whisper

| Modèle | Paramètres | RAM | VRAM | Qualité |
|--------|------------|-----|------|---------|
| tiny | 39M | ~1 Go | ~1 Go | Basique |
| base | 74M | ~1.5 Go | ~1 Go | Bonne |
| small | 244M | ~2.5 Go | ~2 Go | Très bonne |
| medium | 769M | ~5 Go | ~5 Go | Excellente |

---

## Utilisation avancée

### Ligne de commande

```bash
# Lancer avec une config personnalisée
python main.py --config mon_config.json

# Spécifier un modèle
python main.py --model small

# Mode debug
python main.py --debug
```

### Variables d'environnement

```bash
# Définir le niveau de log
set WHISPER_LOG_LEVEL=DEBUG

# Désactiver les notifications
set WHISPER_NOTIFICATIONS=false
```

---

## Dépannage

### Le microphone n'est pas détecté

1. Vérifiez les permissions Windows :
   - Paramètres > Confidentialité > Microphone
   - Autorisez l'accès au microphone

2. Testez le microphone :
   ```bash
   python -c "import sounddevice; print(sounddevice.query_devices())"
   ```

### Erreur de mémoire

- Utilisez un modèle plus petit : `"model": "tiny"`
- Fermez les applications gourmandes en RAM

### Transcription incorrecte

- Parlez clairement et à un rythme normal
- Réduisez le bruit ambiant
- Essayez un modèle plus grand

### Raccourcis clavier ne fonctionnent pas

- Vérifiez qu'aucune autre application n'utilise les mêmes raccourcis
- Exécutez en tant qu'administrateur si nécessaire

---

## API et personnalisation

### Utiliser le transcriber dans votre code

```python
from whisper_transcriber import WhisperTranscriber

# Initialiser
transcriber = WhisperTranscriber(
    model_name="base",
    language="fr"
)

# Charger le modèle
transcriber.load_model()

# Transcrire un fichier audio
result = transcriber.transcribe("audio.wav")
print(result["text"])
```

### Événements et callbacks

```python
def on_transcription(text, start_time, end_time):
    print(f"[{start_time:.2f}s] {text}")

# Utiliser avec le callback
transcriber.on_transcription = on_transcription
```

---

## Support

- Documentation principale : `../../docs/`
- Issues : Créez un fichier dans `../../docs/issues/`
- Logs : Consultez `voice_transcriber.log`
