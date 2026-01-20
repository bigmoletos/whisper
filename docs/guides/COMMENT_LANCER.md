# 🚀 Comment lancer Whisper STT

## ⚡ Version FAST (Python 3.12 requis)

**Recommandée si vous avez Python 3.12 installé**

### PowerShell
```powershell
.\scripts\start_fast.ps1
```

### Batch
```cmd
.\scripts\start_fast.bat
```

**Caractéristiques:**
- ✅ Force Python 3.12 (meilleure compatibilité)
- ✅ Installation automatique de faster-whisper
- ✅ Installation automatique des dépendances
- ❌ Refuse de démarrer si Python 3.12 absent

---

## 🔄 Version NORMALE (Python 3.10+ accepté)

**Si vous n'avez pas Python 3.12**

### PowerShell
```powershell
.\scripts\start.ps1
```

### Batch
```cmd
.\scripts\start.bat
```

**Caractéristiques:**
- ✅ Accepte Python 3.10, 3.11, 3.12
- ✅ Priorité à Python 3.12 si disponible
- ✅ Installation automatique de faster-whisper
- ✅ Installation automatique des dépendances
- ⚠️ Peut avoir des problèmes avec Python 3.14+

---

## 🆚 Comparaison

| Critère | Version FAST | Version NORMALE |
|---------|-------------|-----------------|
| **Python requis** | 3.12 uniquement | 3.10, 3.11, 3.12 |
| **Compatibilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Installation auto** | ✅ | ✅ |
| **Recommandé pour** | Production | Développement/Test |

---

## 📋 Que font les scripts

1. **Détectent Python** (3.12 pour fast, 3.10+ pour normal)
2. **Vérifient config.json** via `scripts\config_checker.py`
3. **Installent faster-whisper** si manquant
4. **Installent les dépendances** (sounddevice, numpy, pywin32, pynput, win10toast)
5. **Lancent l'application** `src\main.py`

---

## 🔧 Prérequis

### Pour faster-whisper (recommandé mais optionnel)
Installez Rust: https://rustup.rs/

**OU**

Modifiez `config.json`:
```json
{
  "whisper": {
    "engine": "whisper"
  }
}
```

### Pour Python 3.12
Téléchargez depuis: https://www.python.org/downloads/release/python-3127/

---

## ✅ Vérifier votre installation Python

```powershell
# Lister toutes les versions
py --list

# Tester Python 3.12
py -3.12 --version

# Tester Python 3.11
py -3.11 --version
```

---

## 🐛 Dépannage

### Erreur: "Python 3.12 requis mais non trouvé"
→ Utilisez la version NORMALE: `.\start.ps1` ou `.\scripts\start.bat`
→ OU installez Python 3.12

### Erreur: "ModuleNotFoundError: No module named 'sounddevice'"
→ Les dépendances seront installées automatiquement
→ OU installez manuellement: `py -3.12 -m pip install sounddevice numpy pywin32 pynput win10toast --user`

### Erreur: "Installation de faster-whisper a échoué"
1. Installez Rust: https://rustup.rs/
2. Redémarrez votre terminal
3. Relancez le script
4. OU changez config.json pour utiliser `"engine": "whisper"`

### Erreur PowerShell: "l'exécution de scripts est désactivée"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📁 Structure des scripts

```
whisper_local_STT/
├── scripts/
│   ├── start_fast.ps1      ← PowerShell FAST (Python 3.12)
│   ├── start_fast.bat      ← Batch FAST (Python 3.12)
│   ├── start.ps1           ← PowerShell NORMAL (Python 3.10+)
│   └── start.bat           ← Batch NORMAL (Python 3.10+)
├── src/
│   └── main.py            ← Application principale
└── config.json            ← Configuration
```

---

## 🎯 Raccourcis une fois lancé

- **Ctrl+Alt+7** : Démarrer/arrêter l'enregistrement vocal
- **Ctrl+C** : Quitter l'application

---

## 💡 Recommandation

**Pour un usage normal:**
```powershell
.\scripts\start_fast.ps1
```

**Si vous rencontrez des problèmes:**
```powershell
.\scripts\start.ps1
```

**Si PowerShell pose problème:**
```cmd
.\scripts\start_fast.bat
```
