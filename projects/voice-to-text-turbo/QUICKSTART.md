# Démarrage Rapide - Voice-to-Text Turbo

## 1. Vérifier le GPU (optionnel mais recommandé)

```bash
# Vérifier si CUDA est installé
nvcc --version

# Vérifier le GPU NVIDIA
nvidia-smi
```

## 2. Installation (10 minutes)

```bash
# Ouvrir un terminal dans le dossier racine
cd whisper

# Lancer l'installation Faster-Whisper
scripts\install_faster_whisper.bat
```

## 3. Premier lancement

```bash
# Double-cliquez sur start.bat ou exécutez :
projects\voice-to-text-turbo\start.bat
```

## 4. Utiliser la transcription

| Action | Raccourci |
|--------|-----------|
| Démarrer/Arrêter l'enregistrement | `Ctrl+Shift+R` |
| Quitter l'application | `Ctrl+Shift+Q` |

## 5. Performance

Avec un GPU NVIDIA :
- Transcription quasi-instantanée
- Modèle `large-v3` utilisable en temps réel
- Latence < 1 seconde

## Problèmes courants

**CUDA non détecté ?**
1. Installez [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
2. Redémarrez votre terminal
3. Le mode CPU sera utilisé en fallback

**Erreur de mémoire GPU ?**
- Réduisez le modèle : `"model": "small"`
- Ou passez en CPU : `"device": "cpu"`

**Installation de Faster-Whisper échoue ?**
```bash
pip install faster-whisper --upgrade
```
