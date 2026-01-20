# Changelog - Voice-to-Text Turbo

## [1.0.0] - 2026-01-20

### Ajouté
- Transcription vocale avec Faster-Whisper
- Accélération GPU CUDA
- Support des modèles small, medium, large-v2, large-v3
- Mode fallback CPU automatique
- Configuration compute_type (float16, int8)
- Scripts de lancement optimisés

### Performance
- Transcription 4x plus rapide qu'avec Whisper standard
- Latence réduite < 1 seconde avec GPU
- Utilisation mémoire GPU optimisée
