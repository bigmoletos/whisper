# Démarrage Rapide - VTT

## Quel outil choisir ?

| Besoin | Outil | Commande |
|--------|-------|----------|
| Dicter du texte (simple) | Voice-to-Text Basic | `projects\voice-to-text-basic\start.bat` |
| Dicter du texte (rapide) | Voice-to-Text Turbo | `projects\voice-to-text-turbo\start.bat` |
| Transcrire une réunion | Meeting Transcriber | `projects\meeting-transcriber\start.bat` |
| Réunion + qui parle | Meeting Transcriber Pro | `projects\meeting-transcriber-pro\start.bat` |

---

## Installation express (5 minutes)

```bash
# 1. Ouvrir un terminal dans le dossier whisper
cd whisper

# 2. Installer les dépendances
scripts\install.bat

# 3. C'est prêt !
```

---

## Voice-to-Text (dictée vocale)

### Démarrage
```bash
projects\voice-to-text-basic\start.bat
```

### Utilisation
1. Ouvrez n'importe quelle application (Word, Email, etc.)
2. Placez votre curseur
3. `Ctrl+Shift+R` → Parlez → `Ctrl+Shift+R`
4. Le texte est collé automatiquement !

---

## Meeting Transcriber (réunions)

### Installation
```bash
scripts\install_meeting_assistant.bat
```

### Démarrage
```bash
projects\meeting-transcriber\start.bat
```

### Utilisation
```
> start          # Lancer la capture
# ... votre réunion ...
> stop           # Arrêter et générer le rapport
```

Le rapport est créé dans `projects\meeting-transcriber\reports\`

---

## Meeting Transcriber Pro (avec diarisation)

### Prérequis
1. Token Hugging Face : [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Accepter les licences : [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)

### Installation
```bash
pip install pyannote.audio --user
```

### Démarrage
```bash
set TOKEN_HF=hf_votre_token
projects\meeting-transcriber-pro\start.bat
```

---

## Problèmes courants

### Python non trouvé
Installez Python 3.10+ depuis [python.org](https://python.org)

### Erreur de mémoire
Utilisez un modèle plus petit dans le `config.json` du projet

### Audio non capturé (réunions)
Activez "Stereo Mix" dans les paramètres son Windows

---

## Prochaines étapes

- Consultez le README de chaque sous-projet pour la configuration avancée
- Installez Ollama pour les résumés automatiques : [ollama.ai](https://ollama.ai)
- Pour Voice-to-Text Turbo, installez CUDA pour l'accélération GPU
