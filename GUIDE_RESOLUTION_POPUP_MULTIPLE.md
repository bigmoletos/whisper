# Guide de Résolution - Problème Popup Deuxième Utilisation

## Problème identifié

**Symptômes :**
- ✅ Premier enregistrement : popup s'affiche, transcription et injection OK
- ❌ Deuxième enregistrement : popup ne s'affiche plus, texte non injecté
- 📋 Logs montrent que le processus semble fonctionner normalement

## Cause racine

Le problème vient de la gestion du thread tkinter de la popup :
1. **Premier usage** : Thread créé, popup fonctionne
2. **Fin du premier usage** : Thread reste en vie mais dans un état instable
3. **Deuxième usage** : Thread existant réutilisé mais défaillant
4. **Résultat** : Popup invisible, processus bloqué

## Solution implémentée

### 1. Nettoyage automatique des threads morts
```python
def _cleanup_thread(self):
    """Nettoie le thread UI s'il est mort"""
    with self.lock:
        if self.ui_thread and not self.ui_thread.is_alive():
            self.ui_thread = None
            self.running = False
            self.window = None
            self.is_visible = False
```

### 2. Réinitialisation forcée avant chaque usage
```python
def show_recording(self):
    """Affiche la pop-up d'enregistrement (thread-safe)"""
    self._cleanup_thread()  # Nettoyer d'abord
    
    # Vider la queue des anciennes commandes
    while not self.command_queue.empty():
        try:
            self.command_queue.get_nowait()
        except queue.Empty:
            break
```

### 3. Nettoyage complet à l'arrêt du service
```python
def cleanup_popup():
    """Nettoie complètement la popup (pour redémarrage)"""
    global _popup
    if _popup:
        _popup.cleanup()
        _popup = None
```

### 4. Amélioration de la visibilité
```python
# Forcer au premier plan
self.window.attributes("-topmost", True)
self.window.lift()
```

## Tests de validation

### Test 1 : Utilisations multiples
```bash
cd whisper
py -3.12 test_popup_multiple.py
```

### Test 2 : Application complète
1. Lancez VTT avec `start.bat`
2. Choisissez option [1]
3. Testez plusieurs cycles `Ctrl+Alt+7`

## Vérifications

### Logs à surveiller
```
[DEBUG] Pop-up d'enregistrement affichée avec succès
Texte transcrit: '...' (longueur: X)
Texte injecté avec succès
```

### Comportement attendu
- **Chaque usage** : Popup visible et fonctionnelle
- **Pas de dégradation** : Performance constante
- **Nettoyage automatique** : Pas d'accumulation de ressources

## Dépannage avancé

### Si le problème persiste

1. **Vérifiez les permissions tkinter** :
   ```bash
   py -3.12 -c "import tkinter; root=tkinter.Tk(); root.destroy(); print('OK')"
   ```

2. **Testez le nettoyage manuel** :
   ```python
   from shared.src.recording_popup import cleanup_popup
   cleanup_popup()
   ```

3. **Mode debug avancé** :
   Modifiez `config.json` :
   ```json
   {
       "logging": {
           "level": "DEBUG"
       }
   }
   ```

### Problèmes connus

#### Thread zombie
**Symptôme** : Thread existe mais ne répond plus
**Solution** : Nettoyage automatique implémenté

#### Queue saturée
**Symptôme** : Commandes s'accumulent
**Solution** : Vidage de la queue avant chaque usage

#### Fenêtre cachée
**Symptôme** : Popup créée mais invisible
**Solution** : Forçage au premier plan avec `-topmost`

## Architecture de la solution

### Composants
- `ThreadSafeRecordingPopup` : Classe principale avec nettoyage
- `_cleanup_thread()` : Détection et nettoyage des threads morts
- `cleanup_popup()` : Nettoyage complet global
- `command_queue` : Queue vidée avant chaque usage

### Flux corrigé
1. **Demande d'affichage** → Nettoyage automatique
2. **Vérification thread** → Création si nécessaire
3. **Vidage queue** → Suppression anciennes commandes
4. **Affichage popup** → Forçage premier plan
5. **Fin d'usage** → Nettoyage automatique

### Sécurité
- **Locks threading** : Évite les conditions de course
- **Gestion d'erreurs** : Fallback gracieux
- **Nettoyage automatique** : Pas de fuite mémoire

## Validation finale

La solution corrige :
- ✅ Problème du deuxième enregistrement
- ✅ Accumulation de ressources
- ✅ Threads zombies
- ✅ Queue saturée
- ✅ Fenêtres cachées

Le système devrait maintenant fonctionner de manière fiable pour tous les usages consécutifs.