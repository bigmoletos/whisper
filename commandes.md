# Commandes Utiles - Setup & Environnement

## Setup Environnement Python

### Créer et activer venv avec pip à jour
```powershell
C:\Python311\python.exe -m pip install --upgrade --user pip
python -m venv venv --without-pip
.\venv\Scripts\Activate
pip install --user -r requirements.txt
```

### Une ligne - Setup complet
```powershell
C:\Python311\python.exe -m pip install --upgrade --user pip ; python -m venv venv --without-pip ; .\venv\Scripts\Activate.ps1 ; pip install --user -r requirements.txt
```

### Installation avec pipx (recommandé)
```powershell
# Installer pipx d'abord
python -m pip install --user pipx
python -m pipx ensurepath

# Installer les packages avec pipx
pipx install sounddevice numpy faster-whisper win10toast pywin32 pynput
```

---

## Jupyter & Notebooks

### Lancer Jupyter Notebook
```powershell
.\venv\Scripts\Activate
jupyter notebook
```

### Lancer JupyterLab
```powershell
jupyter lab
```

### Lister les kernels disponibles
```powershell
jupyter kernelspec list
```

---

## Commandes Whisper STT

### Lancer l'application avec notifications
```batch
# Méthode recommandée - utilise run_whisper.bat
run_whisper.bat

# Ou depuis la ligne de commande
python run_whisper.bat
```

### Lancer l'application standard
```batch
# Méthode originale
python -m src.main

# Ou avec configuration du chemin
set PYTHONPATH=src;%PYTHONPATH%
python -m src.main
```

### Tester les notifications
```python
# Tester le système de notifications
python test_notifications.py

# Tester une notification spécifique
python -c "from src.notifications import NotificationManager; notif = NotificationManager(); notif.show_status_notification('running', 'Test')"
```

### Vérifier les dépendances
```python
# Vérifier que toutes les dépendances sont installées
python -c "
import sounddevice, numpy, faster_whisper, win10toast, pywin32, pynput
print('✓ Toutes les dépendances sont installées')
"
```

### Lancer avec différents modèles
```python
# Modifier temporairement le modèle (dans le code)
python -c "
import json
config = json.load(open('config.json'))
config['whisper']['model'] = 'medium'  # ou 'small', 'large', etc.
json.dump(config, open('config.json', 'w'), indent=2)
print('Modèle changé pour:', config['whisper']['model'])
"
```

## Commandes Python Utiles (IA)

### Tester les imports principaux
```python
import numpy as np
import pandas as pd
from sklearn import datasets
import torch
import ollama
print("Tous les imports OK!")
```

### Vérifier la version CUDA/GPU (PyTorch)
```python
import torch
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
```

### Charger un modèle Ollama et faire une requête
```python
import ollama
response = ollama.generate(model='llama2', prompt='Bonjour!')
print(response['response'])
```

### Pandas - Lire et filtrer CSV
```python
import pandas as pd
df = pd.read_csv('url_open_in_edge.csv')
print(df.head())
filtered = df[df['url'].str.contains('example.com', na=False)]
filtered.to_csv('filtered.csv', index=False)
```

---

## Filtrer URLs avec le script Python

### Filtrer par substring
```powershell
python filter_urls.py --input url_open_in_edge.csv --contains "example.com" --output filtered.csv
```

### Filtrer par domaine (requiert tldextract)
```powershell
pip install tldextract
python filter_urls.py --input url_open_in_edge.csv --domain example.com --exclude-duplicates
```

### Filtrer par regex
```powershell
python filter_urls.py --input url_open_in_edge.csv --regex "^https?://(www\.)?" --output filtered.csv
```

---

## Playwright - Web Automation

### Installer Playwright et navigateurs
```powershell
pip install playwright
playwright install
```

### Script simple Playwright
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

---

## Commandes Shell/Batch

### PowerShell - Lister fichiers récursif
```powershell
Get-ChildItem -Recurse -Filter "*.csv" | Select-Object FullName
```

### PowerShell - Nettoyer répertoire
```powershell
Remove-Item -Recurse -Force venv
Remove-Item -Path "*.pyc" -Recurse
```

### CMD/Batch - Créer dossier et venv
```batch
@echo off
mkdir my_project
cd my_project
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

### Bash (Linux/Mac) - Équivalent
```bash
#!/bin/bash
mkdir my_project
cd my_project
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration .bashrc / .bash_profile (Linux/Mac)

```bash
# Alias pour activer venv rapidement
alias venv_activate='source venv/bin/activate'

# Alias pour Jupyter
alias jup='jupyter notebook'
alias juplab='jupyter lab'

# Alias pour Python
alias py='python3'
alias pip3='pip3 --user'

# Alias pour nettoyage Python
alias pyclean='find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null; find . -name "*.pyc" -delete'
```

---

## Git & Versioning

### Initialiser repo git avec .gitignore
```bash
git init
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
git add .
git commit -m "Initial commit"
```

---

## Pip - Utilitaires

### Freezer les dépendances installées
```powershell
pip freeze > requirements_locked.txt
```

### Installer depuis requirements.txt le --user permet l'installation en mode local
```powershell
pip install --user -r requirements.txt
```

### Mettre à jour pip le --user permet l'installation en mode local
```powershell
python -m pip install --user --upgrade pip
```

### Lister les paquets obsolètes
```powershell
pip list --outdated
```

---

## Ollama - Local LLM

### Installer Ollama (Desktop App)
Télécharger depuis: https://ollama.ai

### Lancer Ollama localement
```powershell
ollama serve
```

### Utiliser depuis Python
```python
import ollama
response = ollama.generate(model='llama2', prompt='Explain AI')
print(response['response'])
```

---

## Commandes MacOS/Linux

### Installer Python & pip (Homebrew)
```bash
brew install python3
pip3 install --upgrade pip
```

### Activer venv sur Mac/Linux
```bash
source venv/bin/activate
```

---

## Ressources & Documentation

- **Jupyter**: https://jupyter.org/
- **Pandas**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/
- **PyTorch**: https://pytorch.org/
- **Ollama**: https://ollama.ai
- **Playwright**: https://playwright.dev/python/


