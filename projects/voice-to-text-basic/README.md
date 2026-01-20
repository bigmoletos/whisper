# Voice-to-Text Basic

**Transcription vocale simple avec Whisper standard**

## Description

Voice-to-Text Basic est un outil de transcription vocale qui convertit la parole en texte en temps réel. Il utilise le modèle Whisper d'OpenAI et fonctionne entièrement sur CPU, ce qui le rend accessible sur n'importe quel ordinateur.

### Caractéristiques

- Transcription en temps réel
- Fonctionne sur CPU (pas de GPU requis)
- Raccourcis clavier personnalisables
- Collage automatique du texte transcrit
- Support multilingue (français par défaut)
- Notifications système

## Prérequis

- Windows 10/11
- Python 3.10 ou supérieur
- 4 Go de RAM minimum
- Microphone

## Installation rapide

```bash
# Depuis le répertoire racine du projet
scripts\install.bat
```

## Utilisation

1. Double-cliquez sur `start.bat`
2. Appuyez sur `Ctrl+Shift+R` pour démarrer/arrêter l'enregistrement
3. Le texte transcrit est automatiquement collé à la position du curseur
4. Appuyez sur `Ctrl+Shift+Q` pour quitter

## Configuration

Modifiez `config.json` pour personnaliser :

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `model` | Modèle Whisper (tiny, base, small, medium) | `base` |
| `language` | Langue de transcription | `fr` |
| `toggle_recording` | Raccourci enregistrement | `ctrl+shift+r` |
| `quit` | Raccourci pour quitter | `ctrl+shift+q` |

## Modèles disponibles

| Modèle | RAM requise | Qualité | Vitesse |
|--------|-------------|---------|---------|
| tiny | 1 Go | Basique | Très rapide |
| base | 1.5 Go | Bonne | Rapide |
| small | 2.5 Go | Très bonne | Modérée |
| medium | 5 Go | Excellente | Lente |

## Support

Pour toute question ou problème, consultez la documentation principale dans `/docs`.
