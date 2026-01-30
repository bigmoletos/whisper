# Guide de Dépannage - Injection de Texte

## Problème : La popup s'affiche mais le texte n'est pas restitué

### Symptômes
- ✅ La popup d'enregistrement apparaît
- ✅ La popup passe en mode "TRANSCRIPTION"
- ✅ La popup disparaît après traitement
- ❌ Aucun texte n'est injecté dans l'application

### Diagnostic étape par étape

#### 1. Test rapide d'injection
```bash
cd whisper
py -3.12 test_quick_debug.py
```

#### 2. Test complet du workflow
```bash
cd whisper
py -3.12 debug_text_injection.py
```

#### 3. Vérification des logs
Consultez le fichier `voice_transcriber_turbo.log` pour identifier l'étape qui échoue.

### Causes possibles et solutions

#### A. Problème de capture audio
**Symptômes dans les logs :**
```
Aucun audio capturé
```

**Solutions :**
1. Vérifiez que le microphone fonctionne
2. Testez avec un autre logiciel d'enregistrement
3. Vérifiez les permissions microphone Windows
4. Redémarrez l'application

#### B. Problème de transcription
**Symptômes dans les logs :**
```
Texte transcrit: '' (longueur: 0)
Aucun texte transcrit ou texte vide
```

**Solutions :**
1. Vérifiez que le modèle Whisper se charge correctement
2. Testez avec un enregistrement plus long (5+ secondes)
3. Parlez plus fort et distinctement
4. Vérifiez la configuration du modèle dans `config.json`

#### C. Problème d'injection de texte
**Symptômes dans les logs :**
```
Échec de l'injection du texte
```

**Solutions :**
1. Vérifiez que `pyautogui` et `pyperclip` sont installés :
   ```bash
   py -3.12 -c "import pyautogui, pyperclip; print('OK')"
   ```

2. Testez l'injection manuelle :
   ```bash
   py -3.12 -c "from shared.src.text_injector import TextInjector; TextInjector().inject_text('test')"
   ```

3. Vérifiez les permissions d'accessibilité Windows

#### D. Problème de configuration
**Vérifiez `projects/voice-to-text-turbo/config.json` :**

```json
{
    "whisper": {
        "engine": "faster-whisper",
        "model": "medium",
        "language": "fr",
        "device": "cuda"
    },
    "ui": {
        "show_recording_popup": true
    }
}
```

### Tests de validation

#### Test 1 : Modules de base
```bash
py -3.12 -c "import numpy, sounddevice, pyautogui, pyperclip, faster_whisper; print('Tous les modules OK')"
```

#### Test 2 : Capture audio
```bash
py -3.12 -c "
from shared.src.audio_capture import AudioCapture
import time
ac = AudioCapture()
ac.start_recording()
time.sleep(2)
data = ac.stop_recording()
print(f'Audio: {len(data)} échantillons')
"
```

#### Test 3 : Transcription
```bash
py -3.12 -c "
from shared.src.faster_whisper_transcriber import FasterWhisperTranscriber
import numpy as np
t = FasterWhisperTranscriber('tiny', 'fr', 'cpu', 'int8')
t.load_model()
# Test avec audio factice
audio = np.random.random(16000).astype(np.float32)
result = t.transcribe(audio, 16000)
print(f'Transcription test: {result}')
"
```

#### Test 4 : Injection
```bash
py -3.12 -c "
from shared.src.text_injector import TextInjector
ti = TextInjector()
success = ti.inject_text('Test injection VTT')
print(f'Injection: {success}')
"
```

### Solutions avancées

#### Réinstallation des dépendances
```bash
py -3.12 -m pip uninstall pyautogui pyperclip sounddevice numpy
py -3.12 -m pip install pyautogui pyperclip sounddevice numpy
```

#### Réinitialisation de la configuration
1. Sauvegardez `projects/voice-to-text-turbo/config.json`
2. Supprimez le fichier
3. Relancez l'application pour régénérer la config par défaut

#### Mode debug avancé
Modifiez `config.json` pour activer le debug :
```json
{
    "logging": {
        "level": "DEBUG",
        "file": "voice_transcriber_turbo.log"
    }
}
```

### Vérifications système

#### Permissions Windows
1. **Microphone** : Paramètres > Confidentialité > Microphone
2. **Accessibilité** : Autoriser les applications à contrôler l'ordinateur

#### Antivirus/Sécurité
Certains antivirus bloquent l'injection de texte. Ajoutez VTT aux exceptions.

#### Applications conflictuelles
Fermez les autres logiciels de reconnaissance vocale ou d'automatisation.

### Logs utiles à consulter

#### Logs normaux (succès)
```
Enregistrement démarré
Audio récupéré: 48000 échantillons
Transcription en cours...
Texte transcrit: 'bonjour test' (longueur: 12)
Injection du texte: 'bonjour test' (longueur: 12)
Texte injecté avec succès
```

#### Logs d'erreur typiques
```
# Pas d'audio
Audio récupéré: 0 échantillons
Aucun audio capturé

# Transcription vide
Texte transcrit: '' (longueur: 0)
Aucun texte transcrit ou texte vide

# Injection échouée
Échec de l'injection du texte
```

### Contact et support

Si le problème persiste après ces vérifications :

1. Exécutez `debug_text_injection.py` et notez les résultats
2. Consultez le fichier de log complet
3. Vérifiez la configuration système (Windows, antivirus, permissions)

Le diagnostic complet permettra d'identifier précisément l'étape qui échoue dans la chaîne de traitement.