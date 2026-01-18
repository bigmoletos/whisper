# Guide de Portabilité - Whisper Local STT

## ✅ Ce projet est portable

Ce projet a été conçu pour être facilement transférable d'un ordinateur à l'autre sans modification de code.

## Principes de portabilité appliqués

### 1. **Aucun chemin absolu en dur**

❌ **À ÉVITER:**
```python
config_path = "C:/Users/John/Documents/whisper/config.json"
script_path = "/home/john/whisper_local_STT/scripts/start.sh"
```

✅ **UTILISÉ DANS CE PROJET:**
```python
# Python - Chemins relatifs basés sur __file__
script_dir = Path(__file__).parent.parent
config_path = script_dir / "config.json"

# Batch - Chemins relatifs basés sur le script
cd /d "%~dp0.."

# Bash - Chemins relatifs basés sur le script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
```

### 2. **Variables d'environnement pour les chemins utilisateur**

✅ **Utilisé pour:**
- Cache des modèles: `$HOME/.cache/whisper/` (Linux) ou `%USERPROFILE%\.cache\whisper\` (Windows)
- Installation Rust: `$HOME/.cargo/` (Linux) ou `%USERPROFILE%\.cargo\` (Windows)
- Environnement virtuel Python: `$VIRTUAL_ENV`

### 3. **Détection automatique de l'environnement**

Les scripts détectent automatiquement:
- ✅ Système d'exploitation (Windows/Linux)
- ✅ Environnement virtuel Python (venv)
- ✅ Disponibilité de pipx
- ✅ Installation de Rust

## Structure portable du projet

```
whisper_local_STT/
├── config.json              # Configuration (portable)
├── src/
│   ├── main.py             # Utilise Path(__file__)
│   ├── whisper_transcriber.py
│   └── ...
├── scripts/
│   ├── start_fast.bat      # Utilise %~dp0
│   ├── start_fast.sh       # Utilise $BASH_SOURCE
│   ├── config_checker.py   # Chemins relatifs
│   └── ...
└── venv/                   # Environnement virtuel (local)
```

## Comment transférer le projet

### Option 1: Git (recommandé)
```bash
# Sur la machine source
git clone https://github.com/votre-repo/whisper_local_STT.git

# Sur la nouvelle machine
git clone https://github.com/votre-repo/whisper_local_STT.git
cd whisper_local_STT
```

### Option 2: Copie directe
```bash
# Copier tout le dossier
# Windows
xcopy /E /I C:\source\whisper_local_STT D:\destination\whisper_local_STT

# Linux/Mac
cp -r /source/whisper_local_STT /destination/
```

### Option 3: Archive
```bash
# Créer une archive
# Windows (PowerShell)
Compress-Archive -Path whisper_local_STT -DestinationPath whisper_local_STT.zip

# Linux/Mac
tar -czf whisper_local_STT.tar.gz whisper_local_STT/

# Extraire sur la nouvelle machine
# Windows
Expand-Archive whisper_local_STT.zip

# Linux/Mac
tar -xzf whisper_local_STT.tar.gz
```

## Après transfert

### 1. Recréer l'environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Vérifier la configuration

```bash
# Le fichier config.json est portable, pas besoin de le modifier
cat config.json  # Linux
type config.json # Windows
```

### 3. Lancer l'application

```bash
# Windows
scripts\start_fast.bat

# Linux/WSL
./scripts/start_fast.sh
```

## Vérification de la portabilité

### Script de test de portabilité

Exécutez ce script pour vérifier qu'aucun chemin en dur n'est présent:

```bash
# Linux/WSL
grep -r "C:\\\\" --include="*.py" --include="*.bat" . 2>/dev/null
grep -r "/home/" --include="*.py" --include="*.sh" . 2>/dev/null | grep -v "expanduser"
grep -r "/mnt/c/" --include="*.py" --include="*.sh" . 2>/dev/null

# Si aucune sortie, le projet est portable ✅
```

### Points à vérifier manuellement

- [ ] config.json n'a pas de chemins absolus
- [ ] Les scripts utilisent %~dp0 (bat) ou $BASH_SOURCE (sh)
- [ ] Les fichiers Python utilisent Path(__file__)
- [ ] Les chemins utilisateur utilisent os.path.expanduser("~") ou %USERPROFILE%

## Fichiers à NE PAS transférer

Ces fichiers/dossiers sont générés localement et ne doivent PAS être copiés:

```
❌ venv/                    # Environnement virtuel (à recréer)
❌ __pycache__/             # Cache Python
❌ *.pyc                    # Bytecode Python
❌ whisper_stt.log          # Fichiers de log
❌ .vscode/                 # Configuration IDE (optionnel)
❌ .idea/                   # Configuration IDE (optionnel)
```

Utilisez un `.gitignore` approprié:
```gitignore
venv/
__pycache__/
*.pyc
*.pyo
*.log
.vscode/
.idea/
*.egg-info/
dist/
build/
```

## Cas particuliers

### Modèles Whisper
Les modèles sont téléchargés dans:
- Windows: `%USERPROFILE%\.cache\whisper\`
- Linux: `~/.cache/whisper/`

Ces modèles peuvent être volumineux (plusieurs Go). Lors du transfert:
- **Option 1:** Les retélécharger sur la nouvelle machine (recommandé)
- **Option 2:** Copier le dossier .cache/whisper/ si vous voulez éviter le téléchargement

### Rust
Rust est installé dans:
- Windows: `%USERPROFILE%\.cargo\` et `%USERPROFILE%\.rustup\`
- Linux: `~/.cargo/` et `~/.rustup/`

**Recommandation:** Réinstaller Rust sur chaque machine avec:
```bash
# Windows
scripts\install_rust.bat

# Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Bonnes pratiques de portabilité

### ✅ À FAIRE

1. **Utiliser des chemins relatifs**
   ```python
   # Python
   BASE_DIR = Path(__file__).parent
   CONFIG_PATH = BASE_DIR / "config.json"
   ```

2. **Utiliser des variables d'environnement**
   ```python
   cache_dir = os.path.expanduser("~/.cache/whisper")
   ```

3. **Détecter l'OS**
   ```python
   import platform
   if platform.system() == "Windows":
       # Code Windows
   else:
       # Code Linux/Mac
   ```

### ❌ À ÉVITER

1. **Chemins absolus codés en dur**
   ```python
   config = "C:/Users/John/config.json"  # ❌
   ```

2. **Assumer un nom d'utilisateur**
   ```python
   path = "/home/john/project"  # ❌
   ```

3. **Chemins avec séparateurs codés en dur**
   ```python
   path = "folder\\subfolder\\file.txt"  # ❌ Windows uniquement
   # Utiliser:
   path = os.path.join("folder", "subfolder", "file.txt")  # ✅
   # Ou:
   path = Path("folder") / "subfolder" / "file.txt"  # ✅
   ```

## Validation de la portabilité

### Test sur une nouvelle machine

1. Transférer le projet (sans venv)
2. Créer un nouvel environnement virtuel
3. Installer les dépendances
4. Exécuter les scripts de test:
   ```bash
   python scripts/config_checker.py
   python check_dependencies.py
   ```
5. Lancer l'application:
   ```bash
   scripts\start_fast.bat  # Windows
   ./scripts/start_fast.sh # Linux
   ```

Si tout fonctionne sans modifier le code → ✅ Le projet est portable

## Support

Pour toute question sur la portabilité:
1. Consultez ce guide
2. Vérifiez que vous n'avez pas de chemins en dur
3. Assurez-vous d'avoir recréé l'environnement virtuel
4. Vérifiez que les dépendances sont installées

## Résumé

✅ **Ce projet est portable car:**
- Tous les chemins sont relatifs ou basés sur des variables d'environnement
- Les scripts détectent automatiquement l'environnement
- Aucun chemin utilisateur n'est codé en dur
- La documentation utilise des exemples génériques

Vous pouvez copier ce projet sur n'importe quel ordinateur et il fonctionnera sans modification !
