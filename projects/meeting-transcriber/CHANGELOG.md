# Changelog - Meeting Transcriber

## [1.0.0] - 2026-01-20

### Ajouté
- Capture audio système (loopback) pour réunions
- Transcription temps réel avec Faster-Whisper
- Détection basique des changements de locuteur (pauses)
- Résumés intermédiaires automatiques
- Synthèse finale avec points clés et actions
- Support Ollama pour analyse LLM locale
- Export HTML, Markdown et JSON
- Interface CLI interactive
- Système de checkpoints pour récupération après crash
- Sélection adaptative du modèle selon la mémoire

### Architecture
- Module de capture audio système
- Buffer audio avec détection de silence
- Transcription par micro-batches (10s)
- Stockage incrémental des segments
- Analyse LLM asynchrone
