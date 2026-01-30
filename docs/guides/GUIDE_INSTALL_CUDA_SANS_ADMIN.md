# Guide d'installation CUDA sans droits administrateur

## 🎯 Objectif
Installer CUDA Toolkit pour accélérer Whisper sans avoir besoin de droits administrateur sur Windows.

## 🚀 Méthode 1 : Installation via pip (Recommandée)

### Avantages
- ✅ Pas besoin de droits admin
- ✅ Installation rapide (5-10 minutes)
- ✅ Intégration automatique avec Python
- ✅ Gestion des dépendances automatique

### Étapes

1. **Lancer le script automatique**
```bash
cd whisper
scripts\install_cuda_pip.bat
```

2. **Vérification manuelle** (optionnel)
```python
import torch
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Version CUDA: {torch.version.cuda}")
```

3. **Configuration Whisper**
Modifiez `projects/voice-to-text-turbo/config.json` :
```json
{
    "whisper": {
        "device": "cuda",
        "compute_type": "float16"
    }
}
```

## 🔧 Méthode 2 : Installation portable avec Conda

### Prérequis
Téléchargez Miniconda depuis : https://docs.conda.io/en/latest/miniconda.html
- Choisissez la version Windows x86_64
- Installez dans `%USERPROFILE%\miniconda3` (pas besoin d'admin)

### Installation
```bash
cd whisper
scripts\install_cuda_portable.bat
```

### Utilisation
```bash
conda activate cuda_env
cd whisper/projects/voice-to-text-turbo
start.bat
```

## 🛠️ Méthode 3 : Installation manuelle

### Étape 1 : Télécharger CUDA Toolkit
1. Allez sur https://developer.nvidia.com/cuda-downloads
2. Sélectionnez : Windows > x86_64 > 11 > exe (network)
3. Téléchargez le fichier (plus petit, ~3MB)

### Étape 2 : Extraction portable
```cmd
# Créer un dossier temporaire
mkdir C:\temp\cuda

# Extraire sans installer
cuda_11.8.0_522.06_windows_network.exe -s -extract:C:\temp\cuda

# Copier vers votre dossier utilisateur
xcopy C:\temp\cuda %USERPROFILE%\cuda /E /I
```

### Étape 3 : Variables d'environnement
Ajoutez à votre PATH utilisateur :
```
%USERPROFILE%\cuda\bin
%USERPROFILE%\cuda\libnvvp
```

Variables d'environnement :
```
CUDA_PATH=%USERPROFILE%\cuda
CUDA_PATH_V11_8=%USERPROFILE%\cuda
```

## 🧪 Tests et validation

### Test 1 : CUDA Runtime
```python
import torch
print("CUDA disponible:", torch.cuda.is_available())
print("Nombre de GPU:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
```

### Test 2 : Faster-Whisper avec CUDA
```python
from faster_whisper import WhisperModel

# Test avec CUDA
try:
    model = WhisperModel("tiny", device="cuda")
    print("✅ Faster-Whisper CUDA: OK")
except Exception as e:
    print(f"❌ Erreur CUDA: {e}")
    
# Fallback CPU
model = WhisperModel("tiny", device="cpu")
print("✅ Faster-Whisper CPU: OK")
```

### Test 3 : Performance
```python
import time
from faster_whisper import WhisperModel

# Test CPU vs CUDA
audio_file = "test.wav"  # Votre fichier de test

# CPU
start = time.time()
model_cpu = WhisperModel("small", device="cpu")
segments_cpu, _ = model_cpu.transcribe(audio_file)
cpu_time = time.time() - start

# CUDA (si disponible)
if torch.cuda.is_available():
    start = time.time()
    model_cuda = WhisperModel("small", device="cuda")
    segments_cuda, _ = model_cuda.transcribe(audio_file)
    cuda_time = time.time() - start
    
    print(f"CPU: {cpu_time:.2f}s")
    print(f"CUDA: {cuda_time:.2f}s")
    print(f"Accélération: {cpu_time/cuda_time:.1f}x")
```

## 🚨 Dépannage

### Problème : "CUDA not available"
**Causes possibles :**
1. Pilotes NVIDIA obsolètes
2. GPU non compatible CUDA
3. Installation incomplète

**Solutions :**
```bash
# Vérifier le GPU
nvidia-smi

# Vérifier la compatibilité
python -c "import torch; print(torch.cuda.is_available()); print(torch.version.cuda)"

# Réinstaller PyTorch
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Problème : "Out of memory"
**Solution :** Réduire la taille du modèle ou utiliser compute_type
```json
{
    "whisper": {
        "model": "small",  // Au lieu de "large"
        "compute_type": "int8"  // Au lieu de "float16"
    }
}
```

### Problème : Installation pip échoue
**Solution :** Utiliser conda ou installation manuelle
```bash
# Alternative avec conda
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

## 📊 Comparaison des performances

| Méthode | Vitesse | Facilité | Compatibilité |
|---------|---------|----------|---------------|
| **pip** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **conda** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **manuel** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

## 🎯 Recommandations

### Pour débutants
1. Essayez d'abord `install_cuda_pip.bat`
2. Si échec, utilisez conda
3. En dernier recours, installation manuelle

### Pour utilisateurs avancés
1. Conda pour un contrôle total
2. Installation manuelle pour optimisation maximale

### Configuration optimale
```json
{
    "whisper": {
        "engine": "faster-whisper",
        "model": "medium",
        "device": "cuda",
        "compute_type": "float16",
        "vad_filter": true
    }
}
```

## 📈 Gains de performance attendus

| Modèle | CPU (i7) | GPU (RTX 3060) | Accélération |
|--------|----------|----------------|--------------|
| tiny | 0.5s | 0.1s | 5x |
| small | 2s | 0.3s | 6-7x |
| medium | 5s | 0.8s | 6-8x |
| large | 12s | 2s | 6x |

---

**💡 Conseil :** Commencez par la méthode pip, c'est la plus simple et fonctionne dans 90% des cas !