# Meeting Transcriber

**Assistant de transcription de réunion avec résumés automatiques**

## Description

Meeting Transcriber capture et transcrit automatiquement vos réunions en temps réel. Il génère des résumés intermédiaires et un rapport final complet avec les points clés, décisions et actions à suivre.

### Caractéristiques

- Capture audio système (réunions Teams, Zoom, etc.)
- Transcription en temps réel avec Faster-Whisper
- Détection basique des changements de locuteur
- Résumés automatiques avec Ollama (LLM local)
- Rapport final structuré (HTML, Markdown, JSON)
- Points clés et actions extraits automatiquement
- Fonctionne entièrement en local

## Prérequis

- Windows 10/11
- Python 3.10+
- 8 Go de RAM minimum
- [Ollama](https://ollama.ai) pour les résumés (optionnel)

## Installation rapide

```bash
# Installer les dépendances
scripts\install_meeting_assistant.bat

# Installer Ollama (optionnel, pour les résumés)
# Téléchargez depuis https://ollama.ai
ollama pull llama3.2
```

## Utilisation

1. Lancez `start.bat`
2. Tapez `start` pour démarrer l'enregistrement
3. La réunion est transcrite en temps réel
4. Tapez `stop` pour arrêter et générer le rapport
5. Le rapport est sauvegardé dans `./reports/`

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `start` | Démarrer la capture |
| `stop` | Arrêter et générer le rapport |
| `pause` | Mettre en pause |
| `resume` | Reprendre |
| `status` | Afficher l'état |
| `quit` | Quitter |

## Configuration

Modifiez `config.json` :

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `model` | Modèle Whisper | `medium` |
| `llm_backend` | Backend LLM | `ollama` |
| `ollama.model` | Modèle Ollama | `llama3.2` |

## Sortie

Le rapport final contient :

- **Résumé exécutif** - Vue d'ensemble en 2-3 phrases
- **Points clés** - Les éléments importants
- **Décisions** - Ce qui a été décidé
- **Actions** - Tâches avec responsables
- **Transcription** - Texte complet avec timestamps

## Support

Documentation complète dans `/docs`.
