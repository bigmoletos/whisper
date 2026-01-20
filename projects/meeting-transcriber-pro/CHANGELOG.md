# Changelog - Meeting Transcriber Pro

## [1.0.0] - 2026-01-20

### Ajouté
- Diarisation des locuteurs avec Pyannote
- Enregistrement audio complet pour post-processing
- Post-processing pyannote en fin de session
- Correction automatique des attributions de locuteurs
- Statistiques de temps de parole par locuteur
- Renommage des locuteurs
- Prédéfinition des noms de participants
- Support GPU CUDA pour modèles large-v3
- Heuristiques avancées de détection de locuteur :
  - Analyse des pauses
  - Marqueurs de dialogue
  - Analyse de l'énergie audio
  - Détection de changement de langue

### Technique
- Intégration pyannote-audio 3.1
- AudioRecorder pour capture complète
- PyannotePostProcessor pour diarisation différée
- Mise à jour des fichiers de transcription après correction

### Configuration
- Support fichier .env pour TOKEN_HF
- Configuration use_pyannote activée par défaut
- Options de diarisation étendues
