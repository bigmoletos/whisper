# Guide - Système Temps Réel avec Faster-Whisper

## Objectif

Obtenir une transcription vocale en temps réel (latence < 1 seconde) avec Faster-Whisper.

## Installation Complète

### Étape 1 : Installer Rust

**Méthode automatique** (recommandée) :
```bash
scripts\install_faster_whisper_complete.bat
```

Ce script installe automatiquement :
1. Rust (si nécessaire)
2. Faster-Whisper
3. Vérifie l'installation

**Méthode manuelle** :
```bash
# Installer Rust
winget install Rustlang.Rustup

# OU télécharger depuis https://rustup.rs/

# Fermer et rouvrir le terminal après installation
```

### Étape 2 : Vérifier Rust

Après avoir fermé et rouvert le terminal :
```bash
rustc --version
cargo --version
```

Si les commandes fonctionnent, Rust est correctement installé.

### Étape 3 : Installer Faster-Whisper

```bash
pip install faster-whisper
```

Ou utiliser le script complet :
```bash
scripts\install_faster_whisper_complete.bat
```

## Configuration pour Temps Réel

### Configuration Optimale

Modifiez `config.json` :

```json
{
  "whisper": {
    "engine": "faster-whisper",
    "model": "large-v3",
    "language": "fr",
    "device": "cpu",
    "compute_type": "int8"
  },
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "chunk_duration": 2.0,
    "silence_threshold": 0.01,
    "silence_duration": 1.0
  }
}
```

### Options de `compute_type` pour la vitesse

| Type | Vitesse | Précision | RAM | Recommandation |
|------|---------|-----------|-----|----------------|
| `int8` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Faible | ✅ **Temps réel** |
| `int8_float16` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Moyenne | ✅ Bon compromis |
| `float16` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Moyenne | Précision max |
| `float32` | ⭐⭐ | ⭐⭐⭐⭐⭐ | Élevée | Non recommandé |

**Pour le temps réel** : Utilisez `int8` (le plus rapide).

### Optimisation Audio

Pour réduire la latence perçue :

```json
{
  "audio": {
    "chunk_duration": 2.0,      // Réduire de 3.0 à 2.0 secondes
    "silence_duration": 1.0      // Réduire de 1.5 à 1.0 seconde
  }
}
```

## Performances Attendues

### Avec Faster-Whisper + int8

| Modèle | Latence (CPU) | Latence (GPU) | Précision |
|--------|---------------|---------------|-----------|
| **large-v3** | 0.5-2s | 0.2-0.5s | ⭐⭐⭐⭐⭐ |
| **medium** | 0.3-1s | 0.1-0.3s | ⭐⭐⭐⭐ |
| **small** | 0.2-0.5s | 0.1-0.2s | ⭐⭐⭐ |

### Comparaison avec Whisper Standard

| Moteur | Latence | Vitesse |
|--------|---------|---------|
| Whisper standard | 3-5s | 1x |
| Faster-Whisper (int8) | 0.5-2s | **2-4x plus rapide** |

## Utilisation du GPU (Optionnel)

Si vous avez un GPU NVIDIA, activez CUDA pour encore plus de vitesse :

```json
{
  "whisper": {
    "device": "cuda",
    "compute_type": "int8_float16"
  }
}
```

**Gain supplémentaire** : 5-10x plus rapide qu'avec CPU.

## Vérification du Temps Réel

### Test de latence

1. Démarrez le service :
   ```bash
   scripts\start_service.bat
   ```

2. Testez la transcription :
   - Appuyez sur `Ctrl+Alt+7`
   - Parlez une phrase courte (2-3 secondes)
   - Relâchez le raccourci
   - Mesurez le temps entre la fin de la parole et l'apparition du texte

**Objectif** : < 1 seconde de latence totale.

### Optimisations Supplémentaires

Si la latence est encore trop élevée :

1. **Réduire la taille du modèle** :
   ```json
   {
     "model": "medium"  // Au lieu de "large-v3"
   }
   ```

2. **Utiliser un GPU** si disponible

3. **Réduire les segments audio** :
   ```json
   {
     "chunk_duration": 1.5  // Encore plus court
   }
   ```

## Dépannage

### Erreur "Rust not found"

1. Fermez et rouvrez le terminal
2. Vérifiez : `rustc --version`
3. Si toujours absent, réinstallez Rust

### Erreur lors de l'installation de Faster-Whisper

1. Vérifiez que Rust est installé : `rustc --version`
2. Mettez à jour pip : `pip install --upgrade pip`
3. Réessayez : `pip install faster-whisper`

### Latence encore élevée

1. Vérifiez que Faster-Whisper est utilisé (logs au démarrage)
2. Utilisez `compute_type: "int8"`
3. Réduisez la taille du modèle si nécessaire
4. Activez le GPU si disponible

## Résumé

Pour obtenir un système en temps réel :

1. ✅ Installer Rust : `scripts\install_faster_whisper_complete.bat`
2. ✅ Configurer `engine: "faster-whisper"` dans `config.json`
3. ✅ Utiliser `compute_type: "int8"` pour la vitesse maximale
4. ✅ Réduire `chunk_duration` à 2.0 secondes
5. ✅ (Optionnel) Activer GPU si disponible

**Résultat attendu** : Latence < 1 seconde, transcription quasi instantanée !

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
