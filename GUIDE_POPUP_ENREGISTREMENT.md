# Guide Pop-up d'Enregistrement VTT

## Vue d'ensemble

La pop-up d'enregistrement est une fenêtre discrète qui s'affiche pendant l'enregistrement vocal pour indiquer l'état du système.

## Fonctionnalités

### États de la pop-up
1. **🔴 ENREGISTREMENT** - Pendant la capture audio
2. **⚡ TRANSCRIPTION** - Pendant le traitement
3. **Cachée** - Quand inactive

### Positionnement
- **Position** : Coin supérieur droit de l'écran
- **Taille** : 220x90 pixels
- **Toujours au premier plan** : Oui

## Configuration

### Activation/Désactivation
Dans `projects/voice-to-text-turbo/config.json` :

```json
{
    "ui": {
        "show_recording_popup": true,
        "popup_position": "top-right",
        "popup_timeout_ms": 3000
    }
}
```

### Options disponibles
- `show_recording_popup` : `true`/`false` - Active/désactive la pop-up
- `popup_position` : Position (actuellement seul "top-right" supporté)
- `popup_timeout_ms` : Durée d'affichage (non utilisé actuellement)

## Comportement

### Priorité d'affichage
1. **Pop-up activée** → Affiche la pop-up moderne, pas de notifications Windows
2. **Pop-up désactivée** → Utilise les notifications Windows classiques

### Thread-safety
- La pop-up utilise un système de queue pour être thread-safe
- Compatible avec les callbacks de raccourcis clavier
- Pas de blocage de l'interface principale

## Tests

### Test isolé
```bash
cd whisper
py -3.12 test_popup_threadsafe.py
```

### Test dans l'application
1. Lancez VTT avec `start.bat`
2. Choisissez option [1] Voice-to-Text TURBO
3. Utilisez `Ctrl+Alt+7` pour tester

## Dépannage

### Pop-up ne s'affiche pas
1. **Vérifiez la configuration** :
   ```json
   "show_recording_popup": true
   ```

2. **Testez tkinter** :
   ```bash
   py -3.12 -c "import tkinter; print('OK')"
   ```

3. **Vérifiez les logs** :
   - Cherchez `[DEBUG] Pop-up d'enregistrement affichée`
   - Ou `[DEBUG] Erreur affichage pop-up`

### Anciennes notifications persistent
- Si `show_recording_popup: true`, les notifications Windows ne devraient plus apparaître
- Redémarrez l'application après modification de la config

### Erreurs tkinter
- Assurez-vous que Python 3.12 inclut tkinter
- Sur certains systèmes, installez `python3-tk`

## Architecture technique

### Composants
- `ThreadSafeRecordingPopup` : Classe principale thread-safe
- `command_queue` : Queue pour les commandes UI
- `ui_worker` : Thread dédié à l'interface

### Flux d'exécution
1. Hotkey callback → `show_recording()`
2. Commande ajoutée à la queue
3. UI thread traite la commande
4. Fenêtre tkinter mise à jour

### Sécurité
- Thread daemon pour éviter les blocages
- Gestion d'erreurs complète
- Nettoyage automatique des ressources

## Intégration

### Dans main.py
```python
# Import conditionnel
try:
    from src.recording_popup import show_recording, show_processing, hide_popup
    RECORDING_POPUP_AVAILABLE = True
except ImportError:
    RECORDING_POPUP_AVAILABLE = False

# Utilisation
if RECORDING_POPUP_AVAILABLE and config["ui"]["show_recording_popup"]:
    show_recording()  # Au lieu de notification
```

### Fallback automatique
Si la pop-up échoue, le système bascule automatiquement sur les notifications Windows.

## Personnalisation future

### Extensions possibles
- Positions configurables (top-left, bottom-right, etc.)
- Thèmes de couleurs
- Animations d'apparition/disparition
- Indicateur de niveau audio
- Temps d'enregistrement affiché

### Configuration avancée
```json
{
    "ui": {
        "show_recording_popup": true,
        "popup_theme": "dark",
        "popup_position": "top-right",
        "popup_opacity": 0.9,
        "show_audio_level": true,
        "show_timer": true
    }
}
```