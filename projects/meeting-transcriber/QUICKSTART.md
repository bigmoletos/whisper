# Démarrage Rapide - Meeting Transcriber

## 1. Installation (15 minutes)

```bash
# Installer le Meeting Assistant
scripts\install_meeting_assistant.bat
```

## 2. Installer Ollama (optionnel mais recommandé)

Pour les résumés automatiques :

1. Téléchargez [Ollama](https://ollama.ai)
2. Installez et lancez Ollama
3. Téléchargez un modèle :
   ```bash
   ollama pull llama3.2
   ```

## 3. Premier lancement

```bash
projects\meeting-transcriber\start.bat
```

## 4. Transcrire une réunion

```
> start          # Démarrer la capture
[INFO] Capture démarrée...

# Lancez votre réunion (Teams, Zoom, etc.)
# La transcription s'affiche en temps réel

> stop           # Arrêter et générer le rapport
[INFO] Rapport généré: reports/rapport_20260120_143052.html
```

## 5. Consulter le rapport

Le rapport est généré en 3 formats :
- `rapport_XXXXXXXX.html` - Version web
- `rapport_XXXXXXXX.md` - Version Markdown
- `rapport_XXXXXXXX.json` - Version données

## Problèmes courants

**L'audio n'est pas capturé ?**
- Vérifiez que le son système fonctionne (écoutez la réunion)
- Windows peut nécessiter l'activation du "Stereo Mix"

**Pas de résumés ?**
- Ollama n'est pas lancé : `ollama serve`
- Modèle non installé : `ollama pull llama3.2`

**Erreur de mémoire ?**
- Réduisez le modèle dans `config.json` : `"model": "small"`
