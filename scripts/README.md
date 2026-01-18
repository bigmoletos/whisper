# Scripts de lancement - Whisper Local STT

## Scripts testés et fonctionnels

### ✅ `start_fast.sh` (Linux/WSL) - TESTÉ
Script Bash pour lancer Whisper avec Faster-Whisper.

**Test effectué:**
- ✅ Détection de Python
- ✅ Vérification de config.json via config_checker.py
- ✅ Détection de faster-whisper
- ✅ Gestion automatique pipx/pip

**Usage:**
```bash
./scripts/start_fast.sh
```

### ✅ `config_checker.py` - TESTÉ
Script Python pour vérifier et configurer config.json.

**Test effectué:**
- ✅ Lecture de config.json
- ✅ Vérification de l'engine
- ✅ Mise à jour automatique si nécessaire

### 🔄 `start_fast.bat` (Windows) - À TESTER
Script Batch pour Windows avec la même logique que le .sh.

**Usage:**
```cmd
scripts\start_fast.bat
```

**Fonctionnalités:**
- Détection automatique de Python
- Configuration automatique via config_checker.py
- Détection et utilisation de pipx (recommandé)
- Fallback sur pip --user si pipx non disponible
- Messages d'erreur détaillés avec solutions

## Ordre de priorité pour l'installation

Les scripts utilisent cet ordre:
1. **pipx** (recommandé) - Environnement virtuel isolé
2. **pip --user** (fallback) - Installation locale utilisateur
3. **Message d'erreur** avec solutions si échec

## Installation de pipx

### Windows
```cmd
python -m pip install pipx
python -m pipx ensurepath
```

### Linux/WSL
```bash
sudo apt install pipx
pipx ensurepath
```

**Redémarrez votre terminal après l'installation de pipx.**

## Installation de Rust (si nécessaire)

`faster-whisper` nécessite Rust pour compiler certaines dépendances.

### Windows
1. Téléchargez rustup-init.exe depuis https://rustup.rs/
2. Exécutez l'installateur
3. Acceptez les options par défaut
4. Redémarrez votre terminal

### Linux/WSL
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

## Autres scripts

### `start_fast_whisper.bat` (ancien)
Version plus verbeuse avec plus de vérifications. Conservé pour compatibilité.

### `start_service.bat` (déprécié)
Version basique utilisant Whisper standard (lent). Non recommandé.

## Dépannage

### "faster-whisper n'est pas installé"
1. Installez pipx (voir ci-dessus)
2. Relancez le script, il installera automatiquement faster-whisper
3. Si échec : installez Rust puis réessayez

### "Python n'est pas installé"
- Windows : Installez Python depuis https://www.python.org/ ou Microsoft Store
- Linux : `sudo apt install python3 python3-pip`

### Le script .sh n'est pas exécutable
```bash
chmod +x scripts/start_fast.sh
```

## Scripts de vérification Rust

### ✅ `check_rust.sh` (Linux/WSL) - TESTÉ
Vérifie que Rust est installé et fonctionne correctement.

**Test effectué:**
- ✅ Détection de rustc et cargo
- ✅ Test de compilation d'un projet
- ✅ Vérification de l'exécution

**Usage:**
```bash
./scripts/check_rust.sh
```

### 🔄 `check_rust.bat` (Windows)
Version Windows du script de vérification Rust.

**Usage:**
```cmd
scripts\check_rust.bat
```

### `install_rust.bat` (Windows)
Script d'installation de Rust via winget ou téléchargement manuel.

**Usage:**
```cmd
scripts\install_rust.bat
```

## Status des tests

| Script | Testé | Fonctionnel | Plateforme | Notes |
|--------|-------|-------------|------------|-------|
| `start_fast.sh` | ✅ | ✅ | Linux/WSL | Détection venv OK |
| `start_fast.bat` | 🔄 | 🔄 | Windows | Détection venv ajoutée |
| `config_checker.py` | ✅ | ✅ | Tous | - |
| `check_rust.sh` | ✅ | ✅ | Linux/WSL | Installation Rust testée |
| `check_rust.bat` | 🔄 | 🔄 | Windows | - |
| `install_rust.bat` | ⏳ | ⏳ | Windows | - |
| `start_fast_whisper.bat` | ❌ | ❌ | Windows | Bug d'échappement |
| `start_service.bat` | ⚠️ | ⚠️ | Windows | Lent (Whisper standard) |

**Légende:**
- ✅ Testé et fonctionne
- 🔄 Logique corrigée, à tester sur Windows
- ⏳ En attente de test
- ❌ Problème connu
- ⚠️ Déprécié

## Installation Rust testée sur Linux/WSL

Rust a été installé et testé avec succès:
- ✅ rustc 1.92.0 (ded5c06cf 2025-12-08)
- ✅ cargo 1.92.0 (344c4567c 2025-10-21)
- ✅ Compilation fonctionnelle
- ✅ Exécution validée
