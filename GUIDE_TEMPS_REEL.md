# Guide - Transcription en Temps Réel

## État Actuel du Système

Le système actuel utilise **Whisper en mode batch** :
- ✅ Haute précision
- ⚠️ Latence : 1-5 secondes selon le modèle
- ⚠️ Transcription après la fin de l'enregistrement

## Options pour le Temps Réel

### Option 1 : Faster-Whisper (Recommandé)

**Faster-Whisper** est une implémentation optimisée de Whisper qui permet la transcription en streaming.

#### Avantages
- ✅ **2-4x plus rapide** que Whisper standard
- ✅ **Streaming possible** : transcription pendant la parole
- ✅ **Même précision** que Whisper
- ✅ **Support GPU** amélioré
- ✅ **Quantification** : modèles plus légers

#### Installation

```bash
pip install faster-whisper
```

#### Implémentation

Créer `src/faster_whisper_transcriber.py` :

```python
"""
Module de transcription en temps réel avec Faster-Whisper
"""

from faster_whisper import WhisperModel
import numpy as np
import logging
from typing import Optional, Iterator

logger = logging.getLogger(__name__)


class FasterWhisperTranscriber:
    """Transcription en temps réel avec Faster-Whisper"""

    def __init__(
        self,
        model_name: str = "large-v3",
        language: str = "fr",
        device: str = "cpu",
        compute_type: str = "int8"  # int8, int8_float16, float16, float32
    ):
        """
        Initialise Faster-Whisper

        Args:
            model_name: Nom du modèle (large-v3, medium, small, etc.)
            language: Code langue
            device: cpu ou cuda
            compute_type: Type de calcul (int8 = plus rapide, float32 = plus précis)
        """
        self.model_name = model_name
        self.language = language
        self.device = device
        self.compute_type = compute_type
        self.model: Optional[WhisperModel] = None

        logger.info(f"Initialisation Faster-Whisper: {model_name} ({device}, {compute_type})")

    def load_model(self) -> None:
        """Charge le modèle Faster-Whisper"""
        if self.model is not None:
            return

        try:
            logger.info(f"Chargement du modèle Faster-Whisper '{self.model_name}'...")

            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type
            )

            logger.info(f"Modèle '{self.model_name}' chargé avec succès")

        except Exception as e:
            logger.error(f"Erreur lors du chargement: {e}", exc_info=True)
            raise

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """Transcrit l'audio (mode batch)"""
        if self.model is None:
            self.load_model()

        if len(audio) == 0:
            return ""

        try:
            # Normaliser l'audio
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            if np.abs(audio).max() > 1.0:
                audio = audio / np.abs(audio).max()

            # Transcription avec Faster-Whisper
            segments, info = self.model.transcribe(
                audio,
                language=self.language,
                beam_size=5,
                vad_filter=True,  # Filtre de détection de voix
                vad_parameters=dict(min_silence_duration_ms=500)
            )

            # Assembler le texte
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)

            text = " ".join(text_parts).strip()
            logger.info(f"Transcription réussie: '{text[:50]}...'")
            return text

        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {e}", exc_info=True)
            return ""

    def transcribe_streaming(
        self,
        audio_stream: Iterator[np.ndarray],
        sample_rate: int = 16000
    ) -> Iterator[str]:
        """
        Transcription en streaming (temps réel)

        Args:
            audio_stream: Itérateur de chunks audio
            sample_rate: Fréquence d'échantillonnage

        Yields:
            Texte transcrit au fur et à mesure
        """
        if self.model is None:
            self.load_model()

        # Buffer pour accumuler l'audio
        audio_buffer = []

        for audio_chunk in audio_stream:
            audio_buffer.append(audio_chunk)

            # Traiter par fenêtres de 3 secondes
            if len(audio_buffer) >= int(sample_rate * 3):
                # Concaténer les chunks
                audio_segment = np.concatenate(audio_buffer, axis=0)

                # Transcrire
                segments, _ = self.model.transcribe(
                    audio_segment,
                    language=self.language,
                    beam_size=1,  # Plus rapide pour le streaming
                    vad_filter=True
                )

                # Yielder le texte
                for segment in segments:
                    yield segment.text

                # Garder les 0.5 dernières secondes pour continuité
                keep_samples = int(sample_rate * 0.5)
                audio_buffer = audio_buffer[-keep_samples:]
```

### Option 2 : Whisper.cpp (C++ optimisé)

**Whisper.cpp** est une implémentation C++ très rapide de Whisper.

#### Avantages
- ✅ **Très rapide** (optimisé C++)
- ✅ **Streaming natif**
- ✅ **Faible consommation mémoire**
- ⚠️ Plus complexe à intégrer (nécessite bindings Python)

#### Installation

```bash
# Option 1 : Via pip (bindings Python)
pip install whisper-cpp-python

# Option 2 : Compiler depuis les sources
# Plus complexe, voir https://github.com/ggerganov/whisper.cpp
```

### Option 3 : Vosk (Temps Réel Natif)

**Vosk** est un modèle STT spécialement conçu pour le temps réel.

#### Avantages
- ✅ **Temps réel natif** (< 100ms de latence)
- ✅ **Très léger** (modèles 50-200 MB)
- ✅ **Streaming continu**
- ⚠️ Précision légèrement inférieure à Whisper

#### Installation

```bash
pip install vosk
```

#### Exemple d'utilisation

```python
import vosk
import json

# Charger le modèle
model = vosk.Model("vosk-model-fr-0.22")  # Modèle français
rec = vosk.KaldiRecognizer(model, 16000)

# Streaming
while True:
    data = stream.read(4000)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print(result["text"])
    else:
        partial = json.loads(rec.PartialResult())
        print(partial["partial"])
```

### Option 4 : Optimisations du Système Actuel

Sans changer de modèle, vous pouvez optimiser :

#### A. Utiliser un GPU

```json
{
  "whisper": {
    "model": "large",
    "device": "cuda"  // ← Activer CUDA
  }
}
```

**Gain** : 5-10x plus rapide avec GPU NVIDIA

#### B. Utiliser un modèle quantifié

Faster-Whisper supporte la quantification :
- `int8` : 2x plus rapide, précision légèrement réduite
- `float16` : Bon compromis

#### C. Réduire la longueur des segments

```json
{
  "audio": {
    "chunk_duration": 2.0,  // ← Réduire de 3.0 à 2.0 secondes
    "silence_duration": 1.0  // ← Réduire le silence
  }
}
```

**Gain** : Transcription plus fréquente, latence perçue réduite

## Comparaison des Solutions

| Solution | Latence | Précision | Complexité | RAM |
|----------|---------|-----------|------------|-----|
| **Whisper standard** | 1-5s | ⭐⭐⭐⭐⭐ | Simple | 5-10 GB |
| **Faster-Whisper** | 0.5-2s | ⭐⭐⭐⭐⭐ | Moyenne | 5-10 GB |
| **Whisper.cpp** | 0.3-1s | ⭐⭐⭐⭐⭐ | Complexe | 5-10 GB |
| **Vosk** | <0.1s | ⭐⭐⭐⭐ | Simple | 1-2 GB |
| **GPU + Whisper** | 0.2-1s | ⭐⭐⭐⭐⭐ | Simple | 5-10 GB |

## Recommandation : Faster-Whisper

Pour votre cas d'usage, je recommande **Faster-Whisper** car :
- ✅ 2-4x plus rapide que Whisper standard
- ✅ Même précision
- ✅ Facile à intégrer
- ✅ Support streaming
- ✅ Compatible avec votre code existant

## Implémentation Recommandée

### Étape 1 : Installer Faster-Whisper

```bash
pip install faster-whisper
```

### Étape 2 : Modifier requirements.txt

Ajouter :
```
faster-whisper>=0.10.0
```

### Étape 3 : Mettre à jour la configuration

```json
{
  "whisper": {
    "model": "large-v3",
    "language": "fr",
    "device": "cpu",
    "engine": "faster-whisper",  // ← Nouveau
    "compute_type": "int8"        // ← Nouveau (int8, float16, float32)
  }
}
```

### Étape 4 : Adapter le code

Modifier `src/whisper_transcriber.py` pour supporter Faster-Whisper en option.

## Mode Streaming (Temps Réel Vrai)

Pour une transcription vraiment en temps réel (pendant que vous parlez), il faut :

1. **Capturer l'audio par petits chunks** (100-500ms)
2. **Transcrire chaque chunk** au fur et à mesure
3. **Afficher/injecter le texte progressivement**

**Limitation** : Whisper fonctionne mieux sur des segments de 2-3 secondes minimum, donc le "vrai temps réel" reste difficile.

**Alternative** : Utiliser Vosk pour le temps réel pur, ou Faster-Whisper avec des fenêtres glissantes.

## Résumé

| Besoin | Solution Recommandée |
|--------|---------------------|
| **Précision maximale** | Whisper large + GPU |
| **Vitesse optimale** | Faster-Whisper + GPU |
| **Temps réel pur** | Vosk |
| **Compromis** | Faster-Whisper medium + int8 |

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
