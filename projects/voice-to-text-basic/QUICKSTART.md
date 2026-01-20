# Démarrage Rapide - Voice-to-Text Basic

## 1. Installation (5 minutes)

```bash
# Ouvrir un terminal dans le dossier racine du projet
cd whisper

# Lancer l'installation
scripts\install.bat
```

## 2. Premier lancement

```bash
# Double-cliquez sur start.bat ou exécutez :
projects\voice-to-text-basic\start.bat
```

## 3. Utiliser la transcription

| Action | Raccourci |
|--------|-----------|
| Démarrer/Arrêter l'enregistrement | `Ctrl+Shift+R` |
| Quitter l'application | `Ctrl+Shift+Q` |

## 4. C'est parti !

1. Ouvrez n'importe quelle application (Word, Notepad, Email...)
2. Placez votre curseur où vous voulez écrire
3. Appuyez sur `Ctrl+Shift+R` et parlez
4. Appuyez à nouveau sur `Ctrl+Shift+R` pour arrêter
5. Le texte est automatiquement collé !

## Problèmes courants

**Le texte n'est pas collé ?**
- Vérifiez que votre curseur est dans une zone de texte

**Qualité médiocre ?**
- Essayez un modèle plus grand dans `config.json` : `"model": "small"`

**Erreur Python ?**
- Assurez-vous d'avoir Python 3.10+ : `python --version`
