# Guide de Dépannage Rapide - VTT

## 🚨 Problèmes courants et solutions

### 1. **Erreur "import not recognized" dans les scripts batch**

**Symptôme :**
```
'import' n'est pas reconnu en tant que commande interne
```

**Cause :** Code Python multiligne dans fichier .bat

**Solution :**
```bash
# Utilisez les scripts Python séparés
cd whisper
python scripts\utils\test_cuda_installation.py
python scripts\utils\test_pyaudio.py
```

### 2. **Erreur "Microsoft Visual C++ 14.0 required"**

**Symptôme :**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solutions :**
1. **Installation via wheels précompilés :**
```bash
pip install --only-binary=all pyaudio
```

2. **Installation alternative :**
```bash
pip install pipwin
pipwin install pyaudio
```

3. **Via conda (recommandé) :**
```bash
conda install pyaudio
```

### 3. **PyAudio "No module named 'pyaudio'"**

**Solutions par ordre de préférence :**

1. **Script automatique :**
```bash
cd whisper
scripts\install_pyaudio_windows.bat
```

2. **Installation manuelle :**
```bash
pip install pyaudio
```

3. **Si échec, wheels précompilés :**
- Téléchargez depuis : https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Installez : `pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl`

### 4. **CUDA non détecté malgré l'installation**

**Diagnostic :**
```bash
cd whisper
python scripts\utils\check_cuda_compatibility.py
```

**Solutions :**
1. **Vérifier les pilotes NVIDIA :**
```bash
nvidia-smi
```

2. **Réinstaller PyTorch CUDA :**
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

3. **Test manuel :**
```python
import torch
print(torch.cuda.is_available())
```

### 5. **Configuration ignorée (utilise modèle "base")**

**Symptôme :**
```
Modèle 'base' chargé avec succès
```

**Cause :** Mauvais chemin de configuration

**Solution :**
1. **Vérifier le fichier utilisé :**
```bash
# Doit utiliser projects/voice-to-text-turbo/config.json
# Pas shared/src/config.json
```

2. **Lancer depuis le bon dossier :**
```bash
cd whisper/projects/voice-to-text-turbo
start.bat
```

### 6. **Reconnaissance vocale imprécise**

**Solutions immédiates :**

1. **Utiliser le bon modèle :**
```json
{
    "whisper": {
        "model": "large-v3",  // Au lieu de "base"
        "device": "cuda"      // Si disponible
    }
}
```

2. **Lancer l'adaptation vocale :**
```bash
cd whisper
scripts\voice_adaptation.bat
```

3. **Améliorer l'environnement :**
- Microphone proche (15-20 cm)
- Environnement silencieux
- Parler 20% plus lentement

## 🔧 Scripts de diagnostic

### Diagnostic complet
```bash
cd whisper
scripts\diagnostic_complet.bat
```

### Tests individuels
```bash
# Test CUDA
python scripts\utils\test_cuda_installation.py

# Test PyAudio
python scripts\utils\test_pyaudio.py

# Test compatibilité
python scripts\utils\check_cuda_compatibility.py
```

## 📊 Codes de sortie des scripts

| Code | Signification | Action |
|------|---------------|--------|
| 0 | Succès | Continuer |
| 1 | Avertissement | Vérifier les logs |
| 2 | Échec partiel | Réinstaller composants |
| 3 | Échec critique | Contacter support |

## 🎯 Solutions par symptôme

### "Impossible d'initialiser le périphérique PRN"
- **Cause :** Problème d'affichage Windows
- **Solution :** Ignorer, n'affecte pas le fonctionnement

### "La syntaxe de la commande n'est pas correcte"
- **Cause :** Code Python multiligne dans .bat
- **Solution :** Utiliser les scripts Python séparés

### "whispercpp non disponible"
- **Cause :** Module optionnel manquant
- **Solution :** Utiliser faster-whisper ou whisper standard

### "Fichier de configuration non trouvé"
- **Cause :** Chemin incorrect
- **Solution :** Vérifier le dossier de lancement

## 🚀 Installation propre (si tout échoue)

1. **Supprimer l'environnement :**
```bash
rmdir /s /q venv_whisper
```

2. **Réinstaller :**
```bash
scripts\install.bat
```

3. **Installer CUDA :**
```bash
scripts\install_cuda_pip.bat
```

4. **Tester :**
```bash
scripts\diagnostic_complet.bat
```

## 📞 Support avancé

### Logs à consulter
- `whisper_stt.log` - Logs de transcription
- `cuda_compatibility_report.json` - Rapport CUDA
- `cuda_test_report.json` - Test d'installation

### Informations à fournir
1. Version Windows
2. GPU (nvidia-smi)
3. Version Python
4. Logs d'erreur complets
5. Résultat du diagnostic complet

---

**💡 Conseil :** Commencez toujours par `scripts\diagnostic_complet.bat` pour identifier rapidement les problèmes.