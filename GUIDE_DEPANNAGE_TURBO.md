# Guide de dépannage Voice-to-Text Turbo

## Problème : Voice-to-Text Turbo se ferme immédiatement

### Solution recommandée (Python 3.12 mode --user)

1. **Lancez le menu principal** : `start.bat`
2. **Choisissez l'option [2U]** : Voice-to-Text TURBO (Mode User - Recommandé)
3. **Si des dépendances manquent**, lancez d'abord : `fix_turbo_user.bat`

### Diagnostic des problèmes

Si l'option 2U ne fonctionne pas, utilisez les outils de diagnostic :

#### 1. Test rapide
```bash
diagnostic_simple.bat
```
Ce script vérifie :
- Python 3.12 disponible
- Imports critiques (PyTorch, Faster-Whisper, SoundDevice)
- Fichiers requis (main.py, config.json)

#### 2. Réparation automatique
```bash
fix_turbo_user.bat
```
Ce script installe automatiquement :
- PyTorch avec CUDA (mode --user)
- Faster-Whisper
- Dépendances audio (SoundDevice)
- Dépendances système Windows

### Vérifications manuelles

#### Python 3.12
```bash
py -3.12 --version
```
Doit afficher : `Python 3.12.x`

#### CUDA disponible
```bash
py -3.12 -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

#### Faster-Whisper
```bash
py -3.12 -c "import faster_whisper; print('Faster-Whisper OK')"
```

### Options alternatives

Si l'option 2U ne fonctionne toujours pas :

1. **Option [2S]** : Setup automatique Python 3.12 avec environnement virtuel
2. **Option [2M]** : Version moderne avec pipx
3. **Option [1]** : Voice-to-Text Basic (CPU uniquement, plus lent mais plus stable)

### Configuration CUDA

Pour de meilleures performances, assurez-vous que :
- CUDA Toolkit est installé (ou utilisez `scripts/install_cuda_pip.bat`)
- PyTorch détecte CUDA : `torch.cuda.is_available()` retourne `True`
- La configuration utilise `"device": "cuda"` dans `config.json`

### Logs et débogage

Les logs sont sauvegardés dans :
- `voice_transcriber_turbo.log` (application)
- `whisper_stt.log` (service principal)

Pour plus de détails, activez le mode DEBUG dans `config.json` :
```json
{
    "logging": {
        "level": "DEBUG",
        "file": "voice_transcriber_turbo.log"
    }
}
```

### Support

Si les problèmes persistent :
1. Vérifiez les logs d'erreur
2. Testez d'abord l'option [1] (Voice-to-Text Basic)
3. Utilisez `diagnostic_simple.bat` pour identifier le problème exact