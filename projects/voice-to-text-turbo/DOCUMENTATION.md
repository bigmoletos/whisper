# Documentation Complète - Voice-to-Text Turbo

## Table des matières

1. [Architecture](#architecture)
2. [Prérequis GPU](#prérequis-gpu)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Optimisation des performances](#optimisation-des-performances)
6. [Dépannage](#dépannage)

---

## Architecture

Voice-to-Text Turbo utilise [Faster-Whisper](https://github.com/guillaumekln/faster-whisper), une réimplémentation de Whisper basée sur CTranslate2 qui offre :

- Inférence jusqu'à 4x plus rapide
- Utilisation mémoire réduite
- Support de la quantification int8
- Accélération GPU native

---

## Prérequis GPU

### GPU NVIDIA recommandé

| Catégorie | GPU | VRAM | Modèle max |
|-----------|-----|------|------------|
| Entrée de gamme | GTX 1650 | 4 Go | small |
| Milieu de gamme | RTX 3060 | 8 Go | medium |
| Haut de gamme | RTX 3080+ | 10+ Go | large-v3 |

### Installation CUDA

1. Téléchargez [CUDA Toolkit 11.8+](https://developer.nvidia.com/cuda-downloads)
2. Installez cuDNN correspondant
3. Vérifiez l'installation :
   ```bash
   nvcc --version
   nvidia-smi
   ```

---

## Installation

### Installation automatique

```bash
scripts\install_faster_whisper.bat
```

### Installation manuelle

```bash
# Activer l'environnement
venv_whisper\Scripts\activate

# Installer Faster-Whisper avec CUDA
pip install faster-whisper

# Pour GPU NVIDIA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## Configuration

### config.json complet

```json
{
    "engine": "faster_whisper",
    "faster_whisper": {
        "model": "medium",
        "language": "fr",
        "device": "cuda",
        "compute_type": "float16",
        "beam_size": 5,
        "vad_filter": true,
        "vad_parameters": {
            "threshold": 0.5,
            "min_speech_duration_ms": 250,
            "max_speech_duration_s": 30,
            "min_silence_duration_ms": 2000
        }
    }
}
```

### Options de compute_type

| Type | Description | VRAM | Vitesse |
|------|-------------|------|---------|
| `float32` | Précision maximale | Élevée | Lente |
| `float16` | Équilibre (GPU) | Moyenne | Rapide |
| `int8_float16` | Quantifié mixte | Basse | Très rapide |
| `int8` | Quantifié (CPU) | Très basse | Moyenne |

---

## Optimisation des performances

### Maximiser la vitesse

```json
{
    "faster_whisper": {
        "model": "small",
        "compute_type": "int8_float16",
        "beam_size": 1,
        "vad_filter": true
    }
}
```

### Maximiser la qualité

```json
{
    "faster_whisper": {
        "model": "large-v3",
        "compute_type": "float16",
        "beam_size": 5,
        "best_of": 5
    }
}
```

### VAD (Voice Activity Detection)

Le VAD filtre les silences pour accélérer la transcription :

```json
{
    "vad_filter": true,
    "vad_parameters": {
        "threshold": 0.5,
        "min_speech_duration_ms": 250
    }
}
```

---

## Dépannage

### Erreur CUDA

```
CUDA out of memory
```

**Solution :**
1. Réduisez le modèle ou le compute_type
2. Fermez les autres applications GPU
3. Utilisez le mode CPU en fallback

### Faster-Whisper ne s'installe pas

```bash
# Réinstaller avec --force
pip install --force-reinstall faster-whisper

# Ou installer depuis source
pip install git+https://github.com/guillaumekln/faster-whisper.git
```

### Performance médiocre sur CPU

Le mode CPU est moins optimisé. Pour de meilleures performances CPU, utilisez :

```json
{
    "device": "cpu",
    "compute_type": "int8",
    "model": "small"
}
```

---

## Comparaison avec Voice-to-Text Basic

| Caractéristique | Basic | Turbo |
|-----------------|-------|-------|
| Vitesse | 1x | 4x |
| GPU requis | Non | Recommandé |
| Modèle max pratique | medium | large-v3 |
| Latence | ~3s | < 1s |
| Installation | Simple | Moyenne |
