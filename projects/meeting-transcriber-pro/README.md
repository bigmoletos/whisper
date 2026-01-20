# Meeting Transcriber Pro

**Assistant de réunion avancé avec diarisation des locuteurs (Pyannote)**

## Description

Meeting Transcriber Pro est la version complète de l'assistant de réunion. Il ajoute la **diarisation des locuteurs** grâce à Pyannote, permettant d'identifier automatiquement qui parle à quel moment.

### Caractéristiques

- **Diarisation des locuteurs** avec Pyannote
- Capture audio système haute qualité
- Transcription GPU avec modèles large-v3
- Identification automatique des voix
- Statistiques de temps de parole par locuteur
- Résumés IA avancés (Ollama, OpenAI, Anthropic)
- Post-processing pour correction des locuteurs
- Renommage des locuteurs (Jean, Marie, etc.)

## Prérequis

- Windows 10/11
- Python 3.10+
- **GPU NVIDIA** (recommandé)
- 16 Go de RAM
- **Token Hugging Face** (pour Pyannote)
- [Ollama](https://ollama.ai) (optionnel)

## Installation rapide

```bash
# Installer les dépendances
scripts\install_meeting_assistant.bat

# Installer Pyannote
pip install pyannote.audio

# Configurer le token Hugging Face
set TOKEN_HF=votre_token_huggingface
```

## Configuration du Token Hugging Face

1. Créez un compte sur [huggingface.co](https://huggingface.co)
2. Acceptez les conditions d'utilisation :
   - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
   - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)
3. Créez un token : [Settings > Access Tokens](https://huggingface.co/settings/tokens)
4. Configurez dans `config.json` ou comme variable d'environnement

## Utilisation

```bash
# Définir le token (une fois par session)
set TOKEN_HF=hf_votre_token

# Lancer
projects\meeting-transcriber-pro\start.bat
```

## Commandes

| Commande | Description |
|----------|-------------|
| `start` | Démarrer avec noms des participants (optionnel) |
| `stop` | Arrêter + post-processing pyannote |
| `rename <ID> <nom>` | Renommer un locuteur |
| `status` | Voir les statistiques |

## Fonctionnalités Pro

### Diarisation temps réel
- Détection des changements de locuteur par heuristiques
- Analyse des pauses, intonations, énergie audio

### Post-processing Pyannote
- Analyse complète de l'audio en fin de session
- Correction automatique des attributions
- Identification précise des voix

### Statistiques des locuteurs
```
Locuteur 1 (Jean): 45% du temps de parole (12 min 30s)
Locuteur 2 (Marie): 35% du temps de parole (9 min 45s)
Locuteur 3 (Pierre): 20% du temps de parole (5 min 30s)
```

## Support

Documentation complète dans `DOCUMENTATION.md`.
