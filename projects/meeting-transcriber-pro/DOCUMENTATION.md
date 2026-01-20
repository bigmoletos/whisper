# Documentation Complète - Meeting Transcriber Pro

## Table des matières

1. [Architecture Pro](#architecture-pro)
2. [Configuration Hugging Face](#configuration-hugging-face)
3. [Diarisation des locuteurs](#diarisation-des-locuteurs)
4. [Configuration avancée](#configuration-avancée)
5. [Backends LLM](#backends-llm)
6. [Dépannage](#dépannage)

---

## Architecture Pro

Meeting Transcriber Pro ajoute des modules spécialisés pour la diarisation :

```
Code source additionnel :
├── transcription/
│   ├── audio_recorder.py       # Enregistrement audio complet
│   ├── speaker_diarizer.py     # Gestion des locuteurs
│   └── batch_transcriber.py    # Heuristiques de changement
└── utils/
    └── env_loader.py           # Chargement des tokens
```

### Flux de traitement

```
Audio → Capture → Buffer → Transcription → Diarisation temps réel
                                ↓
                    Enregistrement audio complet
                                ↓
                    [Stop] Post-processing Pyannote
                                ↓
                    Correction des locuteurs
                                ↓
                    Génération du rapport
```

---

## Configuration Hugging Face

### Obtenir un token

1. **Créer un compte** : [huggingface.co/join](https://huggingface.co/join)

2. **Accepter les licences** (obligatoire) :

   Visitez ces pages et cliquez "Agree and access repository" :
   - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
   - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)

3. **Créer le token** :
   - Allez sur [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Cliquez "New token"
   - Nom : `meeting-transcriber`
   - Type : `Read`
   - Copiez le token

### Configurer le token

**Option 1 : Variable d'environnement**
```bash
# Windows CMD
set TOKEN_HF=hf_xxxxxxxxxxxxxxxxxx

# Windows PowerShell
$env:TOKEN_HF="hf_xxxxxxxxxxxxxxxxxx"

# Permanent (System Properties > Environment Variables)
```

**Option 2 : Fichier .env**

Créez `api-keys.env` :
```
TOKEN_HF=hf_xxxxxxxxxxxxxxxxxx
```

Configurez dans `config.json` :
```json
{
    "diarization": {
        "env_file": "C:/Users/votre_nom/.secrets/api-keys.env",
        "hf_token_env": "TOKEN_HF"
    }
}
```

---

## Diarisation des locuteurs

### Fonctionnement en deux phases

**Phase 1 : Temps réel (heuristiques)**

Pendant la réunion, le système détecte les changements de locuteur via :
- Pauses > 2 secondes
- Marqueurs de dialogue (?, !, tirets)
- Variations d'énergie audio
- Changements de patterns linguistiques

**Phase 2 : Post-processing (Pyannote)**

À la fin de la session :
1. L'audio complet est analysé par Pyannote
2. Les voix distinctes sont identifiées
3. Les attributions sont corrigées
4. La transcription est mise à jour

### Renommer les locuteurs

**Avant la session :**
```
> start
Noms des participants: Jean Dupont, Marie Martin, Pierre Durand
```

**Pendant la session :**
```
> rename SPEAKER_00 Jean Dupont
> rename SPEAKER_01 Marie Martin
```

### Statistiques

Le rapport inclut :
```json
{
    "speaker_stats": {
        "speaker_count": 3,
        "total_speaking_time": 1650.5,
        "speakers": [
            {
                "id": "SPEAKER_00",
                "label": "Jean Dupont",
                "total_speaking_time": 742.3,
                "speaking_percentage": 45.0
            },
            ...
        ]
    }
}
```

---

## Configuration avancée

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
        "model": "large-v3",
        "fallback_model": "medium",
        "adaptive_model": true,
        "language": "fr",
        "device": "cuda",
        "compute_type": "float16",
        "diarization": {
            "enabled": true,
            "speaker_change_pause": 2.0,
            "max_speakers": 10,
            "participant_names": [],
            "use_pyannote": true,
            "hf_token_env": "TOKEN_HF",
            "env_file": ""
        }
    },
    "analysis": {
        "llm_backend": "ollama",
        "ollama": {
            "base_url": "http://localhost:11434",
            "model": "llama3.2"
        }
    },
    "output": {
        "include_speaker_stats": true
    }
}
```

### Paramètres de diarisation

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| `enabled` | Activer la diarisation | `true` |
| `speaker_change_pause` | Pause suggérant un changement (s) | `2.0` |
| `max_speakers` | Nombre max de locuteurs | `10` |
| `use_pyannote` | Activer le post-processing | `true` |
| `hf_token_env` | Variable d'env du token | `TOKEN_HF` |

---

## Backends LLM

### Ollama (local, gratuit)

```json
{
    "llm_backend": "ollama",
    "ollama": {
        "model": "llama3.2"
    }
}
```

### OpenAI

```json
{
    "llm_backend": "openai",
    "openai": {
        "model": "gpt-4o-mini"
    }
}
```
Variable : `OPENAI_API_KEY`

### Anthropic

```json
{
    "llm_backend": "anthropic",
    "anthropic": {
        "model": "claude-3-haiku-20240307"
    }
}
```
Variable : `ANTHROPIC_API_KEY`

---

## Dépannage

### Token Hugging Face invalide

```
Erreur: Token Hugging Face requis pour pyannote
```

**Solutions :**
1. Vérifiez la variable `TOKEN_HF` : `echo %TOKEN_HF%`
2. Vérifiez que les licences sont acceptées sur Hugging Face
3. Régénérez le token

### Pyannote non installé

```
pyannote-audio non disponible pour le post-processing
```

**Solution :**
```bash
pip install pyannote.audio --user
```

### Erreur CUDA avec Pyannote

```
CUDA out of memory during diarization
```

**Solutions :**
1. Fermez les autres applications GPU
2. Réduisez `max_speakers`
3. Le CPU sera utilisé en fallback

### Locuteurs mal identifiés

Le post-processing corrige automatiquement. Si le problème persiste :
1. Augmentez `speaker_change_pause` si les changements sont trop fréquents
2. Réduisez si des locuteurs sont fusionnés
3. Prédéfinissez les noms des participants

---

## Comparaison avec Meeting Transcriber

| Fonctionnalité | Standard | Pro |
|----------------|----------|-----|
| Transcription | Oui | Oui |
| Résumés IA | Oui | Oui |
| Diarisation heuristique | Basique | Avancée |
| Diarisation Pyannote | Non | Oui |
| Statistiques locuteurs | Non | Oui |
| GPU recommandé | Non | Oui |
| Token HF requis | Non | Oui |
