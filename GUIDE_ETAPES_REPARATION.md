# Guide de réparation étape par étape

## Problème : Voice-to-Text Turbo ne fonctionne pas

### Étape 1 : Test Python de base
```bash
test_python_base.bat
```
**Si ça échoue** : Python 3.12 n'est pas correctement installé
- Téléchargez Python 3.12 depuis python.org
- Installez avec l'option "Add to PATH"

### Étape 2 : Test des modules
```bash
test_modules.bat
```
**Si des modules manquent** : Passez à l'étape 3

### Étape 3 : Installation des modules
```bash
install_modules_simple.bat
```
**Attendez la fin** : L'installation peut prendre 5-10 minutes

### Étape 4 : Re-test des modules
```bash
test_modules.bat
```
**Si tous les modules sont OK** : Passez à l'étape 5

### Étape 5 : Test Voice-to-Text Turbo
```bash
start.bat
# Choisir option [2F] (Mode Fallback)
```

### Étape 6 : Si ça marche pas encore
```bash
test_direct.bat
```
Ce script vous donnera l'erreur exacte.

## Solutions par problème

### "Python 3.12 non trouvé"
- Installez Python 3.12 depuis python.org
- Redémarrez votre terminal

### "Module XXX manquant"
- Lancez `install_modules_simple.bat`
- Si ça échoue, installez manuellement :
  ```bash
  py -3.12 -m pip install --user [nom_du_module]
  ```

### "CUDA non disponible"
- Normal si vous n'avez pas de GPU NVIDIA
- Utilisez l'option [2F] (Mode Fallback) qui fonctionne sur CPU

### "Permission denied"
- Utilisez toujours `--user` avec pip
- Ne lancez jamais en tant qu'administrateur

### "Application se ferme immédiatement"
- Lancez `test_direct.bat` pour voir l'erreur exacte
- Vérifiez que tous les modules sont installés avec `test_modules.bat`

## Ordre de test recommandé

1. `test_python_base.bat` ✓
2. `test_modules.bat` ✓
3. `install_modules_simple.bat` (si nécessaire)
4. `test_modules.bat` (re-test)
5. `start.bat` → option [2F]

Si tout échoue, utilisez l'option [1] (Voice-to-Text Basic) qui est plus simple et stable.