# Installation Ollama sans droits admin (Windows 11)

## Qu'est-ce qu'Ollama ?

Ollama permet d'executer des modeles IA en local (Codestral, Llama, Mistral, etc.) sans envoyer de donnees dans le cloud. Gratuit et hors ligne.

---

## Methode 1 : Installation portable (RECOMMANDEE)

### 1.1 Telecharger le binaire

```powershell
# Creer le dossier d'installation
$ollamaDir = "$env:USERPROFILE\dev\ollama"
New-Item -ItemType Directory -Path $ollamaDir -Force

# Telecharger la derniere version
$url = "https://github.com/ollama/ollama/releases/latest/download/ollama-windows-amd64.zip"
$zipPath = "$ollamaDir\ollama.zip"

Invoke-WebRequest -Uri $url -OutFile $zipPath
```

### 1.2 Extraire l'archive

```powershell
# Extraire
Expand-Archive -Path $zipPath -DestinationPath $ollamaDir -Force

# Nettoyer
Remove-Item $zipPath
```

### 1.3 Configurer les variables d'environnement

```powershell
# Dossier pour les modeles (peut etre volumineux : 5-50 Go)
$modelsDir = "$env:USERPROFILE\dev\ollama\models"
New-Item -ItemType Directory -Path $modelsDir -Force

# Variables d'environnement utilisateur (persistantes)
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $modelsDir, "User")
[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "127.0.0.1:11434", "User")

# Ajouter au PATH utilisateur
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$ollamaDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$ollamaDir", "User")
}
```

### 1.4 Redemarrer PowerShell et tester

```powershell
# Fermer et rouvrir PowerShell, puis :
ollama --version
```


## Débug ollama ne se lance pas
### Définir le bon chemin
  $ollamaDir = "C:\Users\franck.desmedt\dev\ollama"

  #### Récupérer le PATH actuel et nettoyer les entrées incorrectes
  $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
  $cleanPath = ($currentPath -split ";" | Where-Object { $_ -and $_ -ne '$ollamaDir' }) -join ";"

  #### Ajouter le bon chemin si absent
  if ($cleanPath -notlike "*$ollamaDir*") {
      [Environment]::SetEnvironmentVariable("PATH", "$cleanPath;$ollamaDir", "User")
  }

  #### Appliquer immédiatement dans la session actuelle
  $env:PATH += ";$ollamaDir"

  #### Tester
  ollama --version


---

## Methode 2 : Script d'installation automatique

Copier et executer ce script complet :

```powershell
# === INSTALLATION OLLAMA PORTABLE ===

Write-Host "Installation Ollama portable..." -ForegroundColor Cyan

# Dossiers
$ollamaDir = "$env:USERPROFILE\dev\ollama"
$modelsDir = "$ollamaDir\models"

# Creer les dossiers
New-Item -ItemType Directory -Path $ollamaDir -Force | Out-Null
New-Item -ItemType Directory -Path $modelsDir -Force | Out-Null

# Telecharger
Write-Host "Telechargement en cours..." -ForegroundColor Yellow
$url = "https://github.com/ollama/ollama/releases/latest/download/ollama-windows-amd64.zip"
$zipPath = "$ollamaDir\ollama.zip"
Invoke-WebRequest -Uri $url -OutFile $zipPath -UseBasicParsing

# Extraire
Write-Host "Extraction..." -ForegroundColor Yellow
Expand-Archive -Path $zipPath -DestinationPath $ollamaDir -Force
Remove-Item $zipPath

# Variables d'environnement
Write-Host "Configuration..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $modelsDir, "User")
[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "127.0.0.1:11434", "User")

$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$ollamaDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$ollamaDir", "User")
}

Write-Host "`n[OK] Installation terminee !" -ForegroundColor Green
Write-Host "Redemarrez PowerShell puis tapez : ollama --version" -ForegroundColor Cyan
```

---

## Demarrer le serveur Ollama

### Demarrage manuel

```powershell
# Demarrer le serveur (garder le terminal ouvert)
ollama serve
```

### Demarrage en arriere-plan

```powershell
# Demarrer en arriere-plan
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden

# Verifier que le serveur tourne
Invoke-RestMethod http://localhost:11434/api/tags
```

### Demarrage automatique (optionnel)

Ajouter au DevKit PowerShell ou $PROFILE :

```powershell
# Demarrer Ollama au lancement de PowerShell si pas deja actif
function Start-OllamaIfNeeded {
    try {
        $null = Invoke-RestMethod http://localhost:11434/api/tags -TimeoutSec 1
    } catch {
        Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 2
    }
}
Start-OllamaIfNeeded
```

---

## Installer des modeles

### Modeles recommandes

```powershell
# Codestral (code, 22 Go) - RECOMMANDE pour le DevKit
ollama pull codestral:latest

# Llama 3.2 (general, 4 Go) - Leger et polyvalent
ollama pull llama3.2:latest

# Mistral (general, 4 Go)
ollama pull mistral:latest

# Qwen 2.5 Coder (code, 4 Go) - Alternative legere
ollama pull qwen2.5-coder:latest
```

### Lister les modeles installes

```powershell
ollama list
```

### Supprimer un modele

```powershell
ollama rm nom-du-modele
```

---

## Usage quotidien

### Mode interactif

```powershell
# Chat avec un modele
ollama run codestral

# Quitter : /bye ou Ctrl+D
```

### Mode one-shot

```powershell
# Question directe
ollama run codestral "Explique les design patterns en Java"
```

### Avec le DevKit PowerShell

```powershell
# Le DevKit utilise automatiquement Ollama en mode local
codestral -Mode local "Optimise ce code"
Invoke-Codex -Prompt "Classe Java" -Language java -Mode local
```

---

## Configuration avancee

### Variables d'environnement

| Variable | Description | Valeur par defaut |
|----------|-------------|-------------------|
| `OLLAMA_MODELS` | Dossier des modeles | `~\.ollama\models` |
| `OLLAMA_HOST` | Adresse du serveur | `127.0.0.1:11434` |
| `OLLAMA_NUM_PARALLEL` | Requetes paralleles | `1` |
| `OLLAMA_MAX_LOADED_MODELS` | Modeles en memoire | `1` |

### Optimisation memoire

```powershell
# Limiter la memoire GPU (si GPU faible)
[Environment]::SetEnvironmentVariable("OLLAMA_MAX_VRAM", "4096", "User")

# Forcer CPU uniquement (si pas de GPU)
[Environment]::SetEnvironmentVariable("OLLAMA_NO_GPU", "1", "User")
```

---

## Troubleshooting

### Erreur "ollama n'est pas reconnu"

```powershell
# Verifier le PATH
$env:PATH -split ";" | Where-Object { $_ -like "*ollama*" }

# Ajouter manuellement si absent
$env:PATH += ";$env:USERPROFILE\dev\ollama"
```

### Erreur "connection refused"

```powershell
# Le serveur n'est pas demarre
ollama serve

# Ou en arriere-plan
Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden
```

### Erreur "model not found"

```powershell
# Telecharger le modele d'abord
ollama pull codestral:latest
```

### Espace disque insuffisant

```powershell
# Verifier l'espace utilise
Get-ChildItem "$env:USERPROFILE\dev\ollama\models" -Recurse |
    Measure-Object -Property Length -Sum |
    Select-Object @{N='Size (GB)';E={[math]::Round($_.Sum/1GB,2)}}

# Supprimer les modeles inutilises
ollama rm ancien-modele
```

---

## Structure des fichiers

```
C:\Users\{username}\dev\ollama\
├── ollama.exe              (binaire principal)
├── models\                 (modeles telecharges)
│   ├── codestral\
│   ├── llama3.2\
│   └── ...
```

---

## Liens utiles

- Site officiel : https://ollama.ai/
- GitHub : https://github.com/ollama/ollama
- Liste des modeles : https://ollama.ai/library
- Documentation : https://github.com/ollama/ollama/blob/main/docs/
