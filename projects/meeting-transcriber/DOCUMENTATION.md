# Documentation Complète - Meeting Transcriber

## Table des matières

1. [Architecture](#architecture)
2. [Installation détaillée](#installation-détaillée)
3. [Configuration](#configuration)
4. [Backends LLM](#backends-llm)
5. [Formats de sortie](#formats-de-sortie)
6. [Dépannage](#dépannage)

---

## Architecture

```
meeting-transcriber/
├── start.bat           # Lanceur
├── config.json         # Configuration
├── sessions/           # Données de session
└── reports/            # Rapports générés

Code source (../../shared/lib/meeting_assistant/):
├── capture/            # Capture audio système
│   ├── system_audio_capture.py
│   └── audio_buffer.py
├── transcription/      # Transcription
│   ├── batch_transcriber.py
│   ├── adaptive_model_selector.py
│   └── transcript_storage.py
├── analysis/           # Analyse LLM
│   ├── llm_analyzer.py
│   ├── intermediate_summarizer.py
│   └── final_synthesizer.py
├── output/             # Génération de rapports
│   └── report_generator.py
├── session/            # Gestion de session
│   ├── meeting_session.py
│   └── checkpoint_manager.py
└── ui/                 # Interface utilisateur
    └── cli_interface.py
```

---

## Installation détaillée

### Dépendances système

1. **Python 3.10+**
2. **FFmpeg** pour le traitement audio
3. **PortAudio** (inclus avec PyAudio)

### Installation manuelle

```bash
# Créer l'environnement
python -m venv venv_whisper
venv_whisper\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
pip install -r requirements_meeting.txt

# Télécharger le modèle
python download_model.py --model medium
```

### Installation Ollama

```bash
# Windows - Téléchargez l'installateur depuis ollama.ai

# Démarrer le service
ollama serve

# Télécharger le modèle
ollama pull llama3.2
```

---

## Configuration

### config.json complet

```json
{
    "audio": {
        "sample_rate": 16000,
        "channels": 1,
        "micro_batch_seconds": 10,
        "silence_threshold": 0.01
    },
    "transcription": {
        "model": "medium",
        "fallback_model": "small",
        "adaptive_model": true,
        "language": "fr",
        "device": "cpu",
        "compute_type": "int8",
        "diarization": {
            "enabled": true,
            "speaker_change_pause": 2.0,
            "max_speakers": 10
        }
    },
    "analysis": {
        "llm_backend": "ollama",
        "ollama": {
            "base_url": "http://localhost:11434",
            "model": "llama3.2"
        },
        "intermediate_summary_interval_minutes": 10
    },
    "session": {
        "sessions_directory": "./sessions",
        "checkpoint_interval_seconds": 60
    },
    "output": {
        "directory": "./reports",
        "formats": ["html", "markdown", "json"],
        "include_transcript": true
    }
}
```

### Sélection adaptative du modèle

Le système choisit automatiquement le modèle selon la RAM disponible :

| RAM disponible | Modèle sélectionné |
|----------------|-------------------|
| < 2.5 Go | tiny |
| 2.5 - 4 Go | base |
| 4 - 8 Go | small |
| 8 - 16 Go | medium |
| > 16 Go | large-v3 |

---

## Backends LLM

### Ollama (recommandé)

Fonctionne entièrement en local :

```json
{
    "llm_backend": "ollama",
    "ollama": {
        "base_url": "http://localhost:11434",
        "model": "llama3.2"
    }
}
```

Modèles recommandés :
- `llama3.2` - Équilibre performance/qualité
- `mistral` - Bon pour le français
- `qwen2.5:7b` - Multilingue

### OpenAI (optionnel)

Nécessite une clé API :

```json
{
    "llm_backend": "openai",
    "openai": {
        "model": "gpt-4o-mini"
    }
}
```

Variable d'environnement : `OPENAI_API_KEY`

---

## Formats de sortie

### HTML

Rapport interactif avec :
- Navigation par sections
- Transcription avec timestamps cliquables
- Statistiques visuelles

### Markdown

Format texte structuré, idéal pour :
- Documentation
- Partage sur GitHub/GitLab
- Import dans Notion, Obsidian

### JSON

Données brutes pour :
- Intégration avec d'autres outils
- Analyse programmatique
- Archivage structuré

---

## Dépannage

### L'audio système n'est pas capturé

**Windows :**
1. Ouvrez les paramètres son
2. Allez dans "Périphériques d'enregistrement"
3. Activez "Stereo Mix" ou "What U Hear"

**Alternative :** Utilisez un câble audio virtuel (VB-Audio Cable)

### Erreur de mémoire pendant la transcription

Le système bascule automatiquement vers un modèle plus petit. Si ça persiste :

1. Réduisez `model` dans config.json
2. Fermez les applications gourmandes
3. Activez `adaptive_model: true`

### Les résumés ne sont pas générés

1. Vérifiez qu'Ollama est lancé : `ollama serve`
2. Testez le modèle : `ollama run llama3.2 "test"`
3. Vérifiez l'URL : `http://localhost:11434`

### La transcription est de mauvaise qualité

- Augmentez le modèle si la RAM le permet
- Vérifiez la qualité audio de la source
- Réduisez le bruit de fond
