# Guide des Raccourcis Clavier

## Configuration du raccourci

Le raccourci clavier est configuré dans le fichier `config.json` :

```json
{
  "hotkey": {
    "modifiers": ["right alt"],
    "key": "¤"
  }
}
```

## Modificateurs disponibles

Les modificateurs suivants sont supportés :

- `ctrl` ou `control` : Touche Ctrl
- `shift` : Touche Shift
- `alt` : Touche Alt gauche
- `right alt` ou `altgr` ou `alt gr` : Touche AltGr (Alt droite)
- `win` ou `windows` : Touche Windows
- `cmd` : Touche Cmd (Mac, non applicable sur Windows)

## Touches principales

### Touches alphanumériques
- Lettres : `"a"`, `"b"`, `"c"`, etc.
- Chiffres : `"1"`, `"2"`, `"3"`, etc.

### Touches spéciales
- `"space"` : Barre d'espace
- `"enter"` : Touche Entrée
- `"tab"` : Touche Tabulation
- `"esc"` : Touche Échap
- `"backspace"` : Touche Retour arrière
- `"delete"` : Touche Supprimer

### Touches de fonction
- `"f1"`, `"f2"`, `"f3"`, etc. jusqu'à `"f12"`

### Flèches directionnelles
- `"up"` : Flèche haut
- `"down"` : Flèche bas
- `"left"` : Flèche gauche
- `"right"` : Flèche droite

### Caractères spéciaux

**Attention** : Les caractères spéciaux comme `¤`, `€`, `£`, etc. peuvent ne pas fonctionner directement selon votre clavier et la bibliothèque.

**Solutions alternatives** :

1. **Utiliser le code de la touche physique** :
   - Sur un clavier AZERTY, `¤` est généralement sur la touche `4` avec AltGr
   - Vous pouvez essayer : `"modifiers": ["right alt"], "key": "4"`

2. **Utiliser un script de détection** :
   Créez un fichier `test_key.py` pour détecter le code de la touche :
   ```python
   import keyboard

   def on_key(event):
       print(f"Touche pressée: {event.name}")
       print(f"Code: {event.scan_code}")
       print(f"Caractère: {event.char}")

   keyboard.on_press(on_key)
   keyboard.wait()
   ```

3. **Utiliser une combinaison plus simple** :
   - `AltGr + F1` : `"modifiers": ["right alt"], "key": "f1"`
   - `AltGr + Space` : `"modifiers": ["right alt"], "key": "space"`

## Exemples de configurations

### Exemple 1 : AltGr + ¤
```json
{
  "hotkey": {
    "modifiers": ["right alt"],
    "key": "¤"
  }
}
```

**Note** : Si cela ne fonctionne pas, essayez :
```json
{
  "hotkey": {
    "modifiers": ["right alt"],
    "key": "4"
  }
}
```
(Car sur AZERTY, AltGr+4 produit généralement ¤)

### Exemple 2 : Ctrl + Alt + V
```json
{
  "hotkey": {
    "modifiers": ["ctrl", "alt"],
    "key": "v"
  }
}
```

### Exemple 3 : Windows + F1
```json
{
  "hotkey": {
    "modifiers": ["win"],
    "key": "f1"
  }
}
```

### Exemple 4 : Shift + Ctrl + Espace
```json
{
  "hotkey": {
    "modifiers": ["shift", "ctrl"],
    "key": "space"
  }
}
```

## Dépannage

### Le raccourci ne fonctionne pas

1. **Vérifier la syntaxe** :
   - Les modificateurs doivent être en minuscules
   - Utiliser `"right alt"` pour AltGr (pas `"altgr"` ou `"alt gr"`)

2. **Tester avec un raccourci simple** :
   ```json
   {
     "hotkey": {
       "modifiers": ["ctrl", "shift"],
       "key": "v"
     }
   }
   ```

3. **Vérifier les conflits** :
   - Le raccourci peut être déjà utilisé par une autre application
   - Certains raccourcis système ne peuvent pas être interceptés

4. **Vérifier les logs** :
   - Consultez `whisper_stt.log` pour voir les erreurs
   - Le service doit afficher : "Raccourci enregistré: ..."

### Caractères spéciaux non reconnus

Si un caractère spécial comme `¤` ne fonctionne pas :

1. **Utiliser le code de scan** :
   - Détectez le code avec le script `test_key.py` ci-dessus
   - Utilisez le nom de la touche physique au lieu du caractère

2. **Alternative** :
   - Utilisez une combinaison différente qui fonctionne sur votre clavier
   - Par exemple : `AltGr + F1` ou `Ctrl + Alt + Espace`

## Script de test

Créez `test_hotkey.py` pour tester votre raccourci :

```python
import keyboard
import time

def test_hotkey():
    print("Appuyez sur votre raccourci (AltGr+¤)...")
    print("Appuyez sur ESC pour quitter")

    def on_hotkey():
        print("✓ Raccourci détecté avec succès!")

    # Enregistrer le raccourci
    keyboard.add_hotkey('right alt+¤', on_hotkey)
    # Ou essayer avec le code de la touche
    # keyboard.add_hotkey('right alt+4', on_hotkey)

    keyboard.wait('esc')
    print("Test terminé")

if __name__ == "__main__":
    test_hotkey()
```

Exécutez avec :
```bash
python test_hotkey.py
```

## Notes importantes

- **Permissions** : Sur Windows, certains raccourcis globaux nécessitent des privilèges administrateur
- **Conflits** : Vérifiez que le raccourci n'est pas utilisé par une autre application
- **Clavier** : Le comportement peut varier selon la disposition du clavier (AZERTY, QWERTY, etc.)
- **Caractères Unicode** : Les caractères spéciaux peuvent nécessiter l'utilisation du nom de la touche physique plutôt que le caractère

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
