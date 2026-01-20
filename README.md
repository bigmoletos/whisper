# VTT - Voice-to-Text Tools

**Suite d'outils de transcription vocale et d'assistance aux réunions**

## Présentation

VTT (Voice-to-Text Tools) est une collection de 4 outils de transcription vocale, du plus simple au plus avancé :

| Outil | Description | GPU requis | Token HF |
|-------|-------------|------------|----------|
| [Voice-to-Text Basic](#voice-to-text-basic) | Transcription simple CPU | Non | Non |
| [Voice-to-Text Turbo](#voice-to-text-turbo) | Transcription rapide GPU | Recommandé | Non |
| [Meeting Transcriber](#meeting-transcriber) | Assistant de réunion | Non | Non |
| [Meeting Transcriber Pro](#meeting-transcriber-pro) | Réunion + diarisation | Recommandé | Oui |

---

## Voice-to-Text Basic

**Transcription vocale simple avec Whisper standard**

- Fonctionne sur CPU uniquement
- Modèles : tiny, base, small, medium
- Idéal pour : dictée vocale, notes rapides
- Installation facile

```bash
projects\voice-to-text-basic\start.bat
```

[Documentation complète →](projects/voice-to-text-basic/README.md)

---

## Voice-to-Text Turbo

**Transcription vocale rapide avec Faster-Whisper et GPU**

- Accélération GPU CUDA (4x plus rapide)
- Modèles : small, medium, large-v3
- Idéal pour : transcription en temps réel fluide
- Requiert : GPU NVIDIA (recommandé)

```bash
projects\voice-to-text-turbo\start.bat
```

[Documentation complète →](projects/voice-to-text-turbo/README.md)

---

## Meeting Transcriber

**Assistant de transcription de réunion avec résumés automatiques**

- Capture audio système (Teams, Zoom, etc.)
- Transcription en temps réel
- Résumés automatiques avec Ollama (LLM local)
- Rapport final : points clés, décisions, actions
- Détection basique des locuteurs

```bash
projects\meeting-transcriber\start.bat
```

[Documentation complète →](projects/meeting-transcriber/README.md)

---

## Meeting Transcriber Pro

**Assistant de réunion avancé avec diarisation des locuteurs**

- Toutes les fonctionnalités de Meeting Transcriber
- **Diarisation des locuteurs** avec Pyannote
- Identification automatique des voix
- Statistiques de temps de parole
- Post-processing pour correction précise
- Requiert : Token Hugging Face

```bash
set TOKEN_HF=votre_token
projects\meeting-transcriber-pro\start.bat
```

[Documentation complète →](projects/meeting-transcriber-pro/README.md)

---

## Installation rapide

### Prérequis

- Windows 10/11
- Python 3.10 ou supérieur
- 8 Go de RAM (16 Go recommandé pour Pro)

### Installation de base

```bash
# Cloner ou télécharger le projet
cd whisper

# Installer les dépendances de base
scripts\install.bat

# Pour les outils de réunion
scripts\install_meeting_assistant.bat
```

### Optionnel

```bash
# Pour Voice-to-Text Turbo (GPU)
scripts\install_faster_whisper.bat

# Pour les résumés automatiques
# Téléchargez Ollama depuis https://ollama.ai
ollama pull llama3.2

# Pour Meeting Transcriber Pro (diarisation)
pip install pyannote.audio --user
# + Créez un token sur https://huggingface.co/settings/tokens
```

---

## Structure du projet

```
whisper/
├── projects/                    # Les 4 sous-projets
│   ├── voice-to-text-basic/     # Transcription simple
│   ├── voice-to-text-turbo/     # Transcription rapide
│   ├── meeting-transcriber/     # Assistant réunion
│   └── meeting-transcriber-pro/ # Assistant réunion + pyannote
├── shared/                      # Code source partagé
│   ├── src/                     # Transcription vocale
│   └── lib/                     # Meeting assistant
├── scripts/                     # Scripts d'installation
├── docs/                        # Documentation
├── requirements.txt             # Dépendances de base
└── requirements_meeting.txt     # Dépendances meeting
```

---

## Choisir le bon outil

### Je veux simplement dicter du texte
→ **Voice-to-Text Basic** - Simple, fonctionne partout

### Je veux une transcription rapide et fluide
→ **Voice-to-Text Turbo** - Si vous avez un GPU NVIDIA

### Je veux transcrire mes réunions
→ **Meeting Transcriber** - Transcription + résumés automatiques

### Je veux savoir qui dit quoi dans mes réunions
→ **Meeting Transcriber Pro** - Identification des locuteurs

---

## Raccourcis clavier (Voice-to-Text)

| Action | Raccourci |
|--------|-----------|
| Démarrer/Arrêter l'enregistrement | `Ctrl+Shift+R` |
| Quitter | `Ctrl+Shift+Q` |

---

## Commandes (Meeting Transcriber)

| Commande | Description |
|----------|-------------|
| `start` | Démarrer la capture |
| `stop` | Arrêter et générer le rapport |
| `pause` / `resume` | Mettre en pause / reprendre |
| `status` | Afficher l'état |
| `quit` | Quitter |

---

## Technologies utilisées

- **OpenAI Whisper** - Modèle de reconnaissance vocale
- **Faster-Whisper** - Version optimisée avec CTranslate2
- **Pyannote** - Diarisation des locuteurs
- **Ollama** - LLM local pour les résumés
- **PyAudio** - Capture audio

---

## Support

- Documentation détaillée dans chaque sous-projet
- Guides d'installation : `docs/guides/`
- Dépannage : voir DOCUMENTATION.md de chaque projet

---

## Licence

Ce projet est fourni à des fins éducatives et personnelles.
