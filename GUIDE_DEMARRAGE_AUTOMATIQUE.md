# Guide - Démarrage Automatique du Service

## Options Disponibles

Il existe plusieurs façons de faire démarrer le service automatiquement au démarrage de Windows.

## Option 1 : Service Windows (Recommandé)

### Avantages
- ✅ Démarrage automatique au boot
- ✅ Redémarrage automatique en cas d'erreur
- ✅ Gestion via les Services Windows
- ✅ Fonctionne même sans être connecté

### Installation

1. **Exécuter le script d'installation** (en tant qu'administrateur) :
   ```bash
   scripts\install_windows_service.bat
   ```

2. **Vérifier l'installation** :
   - Ouvrir `services.msc`
   - Chercher "Whisper STT Global Service"
   - Vérifier qu'il est en "Démarrage automatique"

### Commandes de gestion

```bash
# Démarrer le service
nssm.exe start WhisperSTT

# Arrêter le service
nssm.exe stop WhisperSTT

# Redémarrer le service
nssm.exe restart WhisperSTT

# Voir le statut
nssm.exe status WhisperSTT

# Désinstaller le service
nssm.exe remove WhisperSTT confirm
```

### Logs

Les logs sont disponibles dans :
- `logs\service.log` : Logs standard
- `logs\service_error.log` : Logs d'erreur

## Option 2 : Démarrage Windows (Simple)

### Méthode 1 : Dossier Startup

1. **Créer un raccourci** vers `scripts\start_service.bat`
2. **Copier le raccourci** dans le dossier de démarrage :
   - Appuyer sur `Win+R`
   - Taper `shell:startup`
   - Coller le raccourci

### Méthode 2 : Tâche planifiée

1. Ouvrir le **Planificateur de tâches** (`taskschd.msc`)
2. Créer une **nouvelle tâche**
3. Configurer :
   - **Déclencheur** : Au démarrage
   - **Action** : Démarrer un programme
   - **Programme** : `python`
   - **Arguments** : `-m src.main`
   - **Répertoire** : `C:\programmation\whisper_local_STT`

## Option 3 : Docker (Avancé)

### Limitations sur Windows

⚠️ **Important** : Docker sur Windows a des limitations pour ce type d'application :
- Accès au microphone complexe
- Injection de texte dans les applications Windows difficile
- Nécessite Docker Desktop avec WSL2

### Utilisation (Linux recommandé)

Si vous utilisez Linux ou WSL2 :

```bash
# Construire l'image
docker-compose build

# Démarrer le service
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Démarrage automatique Docker

Pour démarrer automatiquement au boot :

```bash
# Activer le démarrage automatique
docker-compose up -d
```

Docker Compose redémarre automatiquement les conteneurs au boot si `restart: unless-stopped` est configuré.

## Option 4 : Script PowerShell au démarrage

Créer `scripts\start_service.ps1` :

```powershell
# Script PowerShell pour démarrer le service
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectPath = Split-Path -Parent $scriptPath

Set-Location $projectPath

# Démarrer le service en arrière-plan
Start-Process python -ArgumentList "-m", "src.main" -WindowStyle Hidden
```

Puis ajouter au démarrage Windows (voir Option 2).

## Comparaison des Options

| Option | Facilité | Fiabilité | Gestion | Recommandation |
|--------|----------|-----------|---------|----------------|
| **Service Windows** | Moyenne | ⭐⭐⭐⭐⭐ | Excellente | ✅ **Recommandé** |
| **Dossier Startup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Basique | ✅ Simple |
| **Tâche planifiée** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Bonne | ✅ Flexible |
| **Docker** | ⭐⭐ | ⭐⭐⭐ | Bonne | ⚠️ Complexe sur Windows |

## Recommandation

Pour Windows, utilisez l'**Option 1 (Service Windows)** car :
- ✅ Démarrage garanti au boot
- ✅ Redémarrage automatique en cas d'erreur
- ✅ Gestion professionnelle via Services Windows
- ✅ Fonctionne même sans session utilisateur

## Dépannage

### Le service ne démarre pas

1. Vérifier les logs : `logs\service.log`
2. Vérifier que Python est dans le PATH système
3. Vérifier les permissions (exécuter en administrateur)

### Le service démarre mais ne fonctionne pas

1. Vérifier que le microphone est accessible
2. Vérifier les permissions Windows pour le microphone
3. Tester manuellement : `python -m src.main`

### Désinstaller le service

```bash
nssm.exe stop WhisperSTT
nssm.exe remove WhisperSTT confirm
```

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
