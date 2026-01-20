# Guide d'utilisation - Whisper Local STT

## Scripts disponibles

### 1. `scripts/start_fast.bat` ⚡ (RECOMMANDÉ)
**Script simplifié et rapide pour lancer l'application avec Faster-Whisper**

- ✅ Simple et rapide
- ✅ Vérifie automatiquement Python et faster-whisper
- ✅ Configure automatiquement config.json si nécessaire
- ✅ Installe faster-whisper automatiquement si manquant
- ✅ Plus facile à maintenir

**Usage:**
```bash
# Windows
scripts\start_fast.bat

# Linux/WSL
./scripts/start_fast.sh
```

### 2. `scripts/start_fast_whisper.bat`
**Script complet avec toutes les vérifications**

- Vérifie la version de Python (3.10+)
- Vérifie toutes les dépendances
- Sauvegarde et restaure config.json
- Plus verbeux avec plus de messages d'aide

**Usage:**
```bash
scripts\start_fast_whisper.bat
```

### 3. `scripts/start_service.bat`
**Script basique (Whisper standard - LENT)**

- ⚠️ Utilise Whisper standard (plus lent que faster-whisper)
- Pas de vérifications avancées
- Plus simple mais moins performant

**Usage:**
```bash
scripts\start_service.bat
```

## Quelle version utiliser?

| Script | Vitesse | Simplicité | Recommandation |
|--------|---------|------------|----------------|
| `start_fast.bat` | ⚡⚡⚡ Très rapide | ✅ Simple | **RECOMMANDÉ** |
| `start_fast_whisper.bat` | ⚡⚡⚡ Très rapide | ⚠️ Verbeux | Pour debug |
| `start_service.bat` | 🐌 Lent | ✅ Simple | Déprécié |

## Configuration

Le fichier `config.json` à la racine du projet contrôle le moteur utilisé:

```json
{
  "whisper": {
    "engine": "faster-whisper",  // Options: "whisper", "faster-whisper", "whisper-cpp"
    "model": "medium",            // Options: "tiny", "base", "small", "medium", "large-v3"
    "language": "fr",
    "device": "cpu",              // Options: "cpu", "cuda" (pour GPU)
    "compute_type": "int8"        // Options: "int8", "float16", "float32"
  },
  "hotkey": {
    "modifiers": ["ctrl", "alt"],
    "key": "7"
  }
}
```

## Dépendances requises

Les packages Python suivants sont nécessaires:
- `faster-whisper` (nécessite Rust pour la compilation)
- `sounddevice`
- `numpy`
- `win10toast`
- `pywin32`
- `pynput`

### Installation avec pipx (RECOMMANDÉ)

`pipx` installe les packages dans des environnements virtuels isolés, ce qui évite les conflits.

**1. Installer pipx:**
```bash
# Windows
python -m pip install pipx
python -m pipx ensurepath

# Linux/WSL
sudo apt install pipx
pipx ensurepath
```

**2. Installer faster-whisper avec pipx:**
```bash
pipx install faster-whisper
```

Les scripts `start_fast.bat` et `start_fast.sh` détectent automatiquement `pipx` et l'utilisent en priorité.

### Installation avec pip (alternative)

Si pipx n'est pas disponible:
```bash
pip install faster-whisper sounddevice numpy win10toast pywin32 pynput --user
```

**Note:** `faster-whisper` nécessite Rust. Si l'installation échoue:
1. Installez Rust: https://rustup.rs/
2. Redémarrez votre terminal après l'installation de Rust
3. Essayez: `pip install faster-whisper --no-build-isolation --user`
4. Ou utilisez `"engine": "whisper"` dans config.json (plus lent mais sans Rust)

## Utilisation

1. Lancez un des scripts `.bat`
2. Attendez que le service démarre
3. Appuyez sur **Ctrl+Alt+7** pour commencer l'enregistrement
4. Parlez dans le microphone
5. Appuyez à nouveau sur **Ctrl+Alt+7** pour arrêter et transcrire
6. Le texte transcrit sera automatiquement collé là où se trouve votre curseur

## Dépannage

### Python non trouvé
- Installez Python 3.10+ depuis https://www.python.org/downloads/
- Ou via Microsoft Store (cherchez "Python 3.11")
- Vérifiez que Python est dans le PATH

### faster-whisper ne s'installe pas
- Installez Rust: https://rustup.rs/
- Redémarrez votre terminal
- Essayez: `pip install faster-whisper --no-build-isolation`
- Alternative: Utilisez `"engine": "whisper"` dans config.json

### L'application est trop lente
- Vérifiez que `config.json` utilise `"engine": "faster-whisper"`
- Utilisez un modèle plus petit: `"model": "small"` ou `"model": "base"`
- Si vous avez un GPU NVIDIA: changez `"device": "cuda"`

### Le raccourci clavier ne fonctionne pas
- Vérifiez que le service est bien lancé
- Essayez de changer le raccourci dans `config.json`
- Vérifiez qu'aucune autre application n'utilise ce raccourci

## Logs

Les logs sont enregistrés dans `whisper_stt.log` à la racine du projet.
Utilisez-les pour diagnostiquer les problèmes.

## Support

Pour plus d'informations, consultez:
- Documentation du projet dans `doc/`
- Fichier `CHANGELOG.md` pour les modifications récentes
- Issues sur GitHub (si applicable)
