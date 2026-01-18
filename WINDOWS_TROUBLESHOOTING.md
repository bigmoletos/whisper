# Dépannage Windows

## Problème: "Failed to find real location of C:\Python314\python.exe"

### Diagnostic rapide

Exécutez ce script pour diagnostiquer votre installation Python:
```cmd
scripts\test_python.bat
```

### Solutions

#### 1. Python non installé ou mal installé

**Réinstaller Python:**
1. Téléchargez Python 3.11 ou 3.12 depuis [python.org](https://www.python.org/downloads/)
2. **IMPORTANT:** Cochez "Add Python to PATH" pendant l'installation
3. Redémarrez votre terminal après installation

**Ou via Microsoft Store:**
```powershell
# Cherchez "Python 3.11" dans Microsoft Store
# Installation automatique dans PATH
```

#### 2. Python installé mais pas dans PATH

**Ajouter Python au PATH manuellement:**

1. Ouvrez les Paramètres Système
2. Recherchez "Variables d'environnement"
3. Dans "Variables utilisateur", éditez "Path"
4. Ajoutez ces chemins (adaptez selon votre installation):
   ```
   C:\Users\VOTRE_NOM\AppData\Local\Programs\Python\Python311
   C:\Users\VOTRE_NOM\AppData\Local\Programs\Python\Python311\Scripts
   ```

**Ou via PowerShell (administrateur):**
```powershell
$pythonPath = (py -c "import sys; print(sys.executable)")
$pythonDir = Split-Path $pythonPath
$scriptsDir = Join-Path $pythonDir "Scripts"

[Environment]::SetEnvironmentVariable("PATH", "$env:PATH;$pythonDir;$scriptsDir", "User")
```

#### 3. Multiple versions de Python

Si vous avez plusieurs versions:

**Utiliser le Python Launcher:**
```cmd
py --list                  # Voir les versions disponibles
py -3.11 --version        # Utiliser Python 3.11
py -3.12 --version        # Utiliser Python 3.12
```

**Le script start_fast.bat détecte automatiquement:**
- Essaie `python` d'abord
- Si échec, essaie `py` (Python Launcher)
- Affiche le chemin utilisé

#### 4. Environnement virtuel

**Si vous utilisez un venv:**
```cmd
# Activer le venv d'abord
venv\Scripts\activate

# Puis lancer le script
scripts\start_fast.bat
```

### Test après correction

```cmd
# Test rapide
python --version
where python

# Test complet
scripts\test_python.bat

# Lancer l'application
scripts\start_fast.bat
```

## Autres problèmes courants

### "faster-whisper" ne s'installe pas

**Cause:** Rust n'est pas installé

**Solution:**
```cmd
scripts\install_rust.bat
```

Ou manuellement depuis [rustup.rs](https://rustup.rs/)

### Permission refusée

**Exécuter en tant qu'administrateur:**
- Clic droit sur PowerShell/CMD
- "Exécuter en tant qu'administrateur"

### Encodage/caractères bizarres

**Changer l'encodage du terminal:**
```cmd
chcp 65001
```

## Scripts de diagnostic

| Script | Description |
|--------|-------------|
| `scripts\test_python.bat` | Diagnostique Python complet |
| `scripts\check_rust.bat` | Vérifie installation Rust |
| `check_dependencies.py` | Vérifie dépendances Python |

## Support

Si le problème persiste:
1. Exécutez `scripts\test_python.bat`
2. Copiez la sortie complète
3. Vérifiez les messages d'erreur
