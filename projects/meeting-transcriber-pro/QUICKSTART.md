# Démarrage Rapide - Meeting Transcriber Pro

## 1. Installation (20 minutes)

```bash
# Installer le Meeting Assistant
scripts\install_meeting_assistant.bat

# Installer Pyannote (diarisation)
pip install pyannote.audio --user
```

## 2. Configurer Hugging Face (requis pour Pyannote)

1. Créez un compte : [huggingface.co/join](https://huggingface.co/join)

2. Acceptez les licences (cliquez sur chaque lien et acceptez) :
   - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
   - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)

3. Créez un token : [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Type : "Read"
   - Copiez le token (commence par `hf_`)

4. Configurez le token :
   ```bash
   # Option 1 : Variable d'environnement
   set TOKEN_HF=hf_votre_token_ici

   # Option 2 : Dans config.json
   # "env_file": "C:/chemin/vers/api-keys.env"
   ```

## 3. Premier lancement

```bash
set TOKEN_HF=hf_votre_token
projects\meeting-transcriber-pro\start.bat
```

## 4. Transcrire une réunion

```
> start
Entrez les noms des participants (optionnel, séparés par virgule):
> Jean, Marie, Pierre

[INFO] Capture démarrée avec 3 participants prédéfinis

# ... la réunion se déroule ...

> stop
[INFO] Post-processing pyannote en cours...
[INFO] 3 locuteurs détectés
[INFO] Rapport généré: reports/rapport_20260120.html
```

## 5. Le rapport inclut

- Transcription avec noms des locuteurs
- Statistiques de temps de parole
- Résumé exécutif
- Actions par participant

## Problèmes courants

**Token Hugging Face invalide ?**
- Vérifiez que vous avez accepté les licences des modèles
- Recréez un token avec les permissions "Read"

**Pyannote non installé ?**
```bash
pip install pyannote.audio --user
```

**GPU non détecté ?**
- Installez CUDA Toolkit
- Le CPU sera utilisé (plus lent)
