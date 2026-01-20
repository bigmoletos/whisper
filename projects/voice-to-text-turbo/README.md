# Voice-to-Text Turbo

**Transcription vocale rapide avec Faster-Whisper et accélération GPU**

## Description

Voice-to-Text Turbo est la version haute performance de l'outil de transcription vocale. Il utilise Faster-Whisper, une implémentation optimisée qui offre des transcriptions jusqu'à 4x plus rapides grâce à l'accélération GPU (CUDA).

### Caractéristiques

- **4x plus rapide** que Whisper standard
- Accélération GPU avec CUDA
- Support des modèles jusqu'à large-v3
- Transcription en temps réel fluide
- Faible latence
- Support multilingue

## Prérequis

- Windows 10/11
- Python 3.10 ou supérieur
- **GPU NVIDIA avec CUDA** (recommandé)
- 8 Go de RAM minimum
- Microphone

## Installation rapide

```bash
# Depuis le répertoire racine du projet
scripts\install_faster_whisper.bat
```

## Utilisation

1. Double-cliquez sur `start.bat`
2. Appuyez sur `Ctrl+Shift+R` pour démarrer/arrêter l'enregistrement
3. Le texte transcrit est automatiquement collé
4. Appuyez sur `Ctrl+Shift+Q` pour quitter

## Configuration

Modifiez `config.json` pour personnaliser :

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `model` | Modèle (small, medium, large-v3) | `medium` |
| `device` | Device (cuda/cpu) | `cuda` |
| `compute_type` | Précision (float16/int8) | `float16` |

## Modèles disponibles

| Modèle | VRAM requise | Qualité | Vitesse |
|--------|--------------|---------|---------|
| small | 2 Go | Bonne | Très rapide |
| medium | 5 Go | Très bonne | Rapide |
| large-v2 | 10 Go | Excellente | Modérée |
| large-v3 | 10 Go | Meilleure | Modérée |

## Mode CPU (sans GPU)

Si vous n'avez pas de GPU NVIDIA, modifiez `config.json` :

```json
{
    "faster_whisper": {
        "device": "cpu",
        "compute_type": "int8"
    }
}
```

## Support

Pour toute question, consultez la documentation dans `/docs`.
