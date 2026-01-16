# Guide d'Optimisation des Performances

Ce guide vous aidera à optimiser les performances de votre système Whisper STT pour obtenir une latence minimale et une transcription rapide.

## Configuration Actuelle

Avec votre système (32 Go RAM, 6 Go VRAM), vous pouvez utiliser les configurations suivantes :

### 1. **Configuration Optimale (Recommandée)**

```json
{
  "whisper": {
    "engine": "faster-whisper",
    "model": "medium",
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

**Performances estimées** :
- Latence : 0.5-2 secondes
- Mémoire : ~3-5 Go
- Précision : Très bonne

### 2. **Configuration Ultra-Rapide (si vous avez un GPU)**

```json
{
  "whisper": {
    "engine": "faster-whisper",
    "model": "medium",
    "language": "fr",
    "device": "cuda",
    "compute_type": "float16"
  }
}
```

**Performances estimées** :
- Latence : 0.2-1 seconde
- Mémoire : ~3-5 Go (GPU)
- Précision : Excellente

### 3. **Configuration Légère (pour les systèmes moins puissants)**

```json
{
  "whisper": {
    "engine": "faster-whisper",
    "model": "small",
    "language": "fr",
    "device": "cpu",
    "compute_type": "int8"
  }
}
```

**Performances estimées** :
- Latence : 0.3-1 seconde
- Mémoire : ~1-2 Go
- Précision : Bonne

## Optimisations Supplémentaires

### 1. **Réduire la durée des segments audio**

```json
"chunk_duration": 1.5  // Au lieu de 3.0
```

Cela permet un traitement plus rapide mais peut réduire légèrement la précision.

### 2. **Optimiser la détection de silence**

```json
"silence_duration": 0.8  // Au lieu de 1.5
```

Cela permet d'arrêter l'enregistrement plus rapidement après la fin de la parole.

### 3. **Utiliser plus de threads**

Si vous avez un CPU multi-cœur, vous pouvez augmenter le nombre de threads utilisés par Faster-Whisper.

### 4. **Désactiver les notifications si nécessaire**

```json
"notifications": {
  "enabled": false
}
```

Cela peut réduire légèrement la latence en évitant les overheads des notifications.

## Comparaison des Performances

| Configuration | Latence | Mémoire | Précision | Utilisation CPU |
|--------------|---------|---------|-----------|----------------|
| Faster-Whisper medium + int8 | 0.5-2s | 3-5GB | ⭐⭐⭐⭐ | 30-50% |
| Faster-Whisper small + int8 | 0.3-1s | 1-2GB | ⭐⭐⭐ | 20-40% |
| Whisper medium | 2-4s | 3-5GB | ⭐⭐⭐⭐ | 50-70% |
| Whisper small | 1-3s | 1-2GB | ⭐⭐⭐ | 30-50% |

## Recommandations pour Votre Système

Avec 32 Go de RAM et 6 Go de VRAM, vous pouvez :

1. **Utiliser le modèle medium** sans problème de mémoire
2. **Activer int8** pour des performances optimales
3. **Réduire chunk_duration** à 1.5-2.0 secondes pour une latence minimale
4. **Utiliser Faster-Whisper** pour des performances 2-4x meilleures que Whisper standard

## Configuration Finale Recommandée

```json
{
  "whisper": {
    "engine": "faster-whisper",
    "model": "medium",
    "language": "fr",
    "device": "cpu",
    "compute_type": "int8"
  },
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "chunk_duration": 1.8,
    "silence_threshold": 0.01,
    "silence_duration": 0.8
  },
  "notifications": {
    "enabled": true,
    "type": "balloon"
  }
}
```

Cette configuration offre un excellent compromis entre latence, précision et utilisation des ressources.

## Comment Appliquer ces Optimisations

1. **Modifiez votre `config.json`** avec la configuration recommandée
2. **Redémarrez l'application**
3. **Testez les performances** avec différents paramètres
4. **Ajustez** selon vos besoins spécifiques

Avec ces optimisations, vous devriez obtenir une latence minimale tout en maintenant une excellente précision de transcription !