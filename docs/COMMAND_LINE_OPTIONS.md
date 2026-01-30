# Options de ligne de commande VTT

## Vue d'ensemble

Tous les outils VTT supportent maintenant les arguments de ligne de commande pour une utilisation avancée et une meilleure flexibilité de configuration.

## Syntaxe générale

```bash
python shared\src\main.py [OPTIONS]
```

## Options disponibles

### --config, -c

Spécifie le chemin vers un fichier de configuration JSON personnalisé.

```bash
# Syntaxe longue
python shared\src\main.py --config mon_config.json

# Syntaxe courte
python shared\src\main.py -c mon_config.json
```

**Comportement :**
- Si le fichier spécifié existe, il sera utilisé
- Si le fichier n'existe pas, l'application utilisera la configuration par défaut
- Si aucune option n'est fournie, l'application cherche `config.json` dans le répertoire `shared/src/`

### --help, -h

Affiche l'aide et la liste des options disponibles.

```bash
python shared\src\main.py --help
```

## Exemples d'utilisation

### Utilisation basique

```bash
# Utiliser la configuration par défaut
python shared\src\main.py
```

### Configurations spécifiques par projet

```bash
# Voice-to-Text Basic
python shared\src\main.py -c projects\voice-to-text-basic\config.json

# Voice-to-Text Turbo
python shared\src\main.py -c projects\voice-to-text-turbo\config.json
```

### Configurations de test

```bash
# Configuration pour tests de performance
python shared\src\main.py -c test_configs\performance_test.json

# Configuration pour débogage
python shared\src\main.py -c test_configs\debug.json
```

### Configurations personnalisées

```bash
# Configuration avec modèle spécifique
python shared\src\main.py -c configs\whisper_large.json

# Configuration pour environnement de production
python shared\src\main.py -c configs\production.json
```

## Structure des fichiers de configuration

Les fichiers de configuration doivent suivre le format JSON standard :

```json
{
    "whisper": {
        "engine": "faster-whisper",
        "model": "medium",
        "language": "fr",
        "device": "cuda"
    },
    "audio": {
        "sample_rate": 16000,
        "channels": 1,
        "chunk_size": 1024
    },
    "hotkey": {
        "modifiers": ["ctrl", "alt"],
        "key": "7"
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    }
}
```

## Cas d'usage avancés

### Développement et tests

```bash
# Test avec différents modèles
python shared\src\main.py -c test_configs\tiny_model.json
python shared\src\main.py -c test_configs\large_model.json

# Test avec différents périphériques
python shared\src\main.py -c test_configs\cpu_only.json
python shared\src\main.py -c test_configs\gpu_optimized.json
```

### Automatisation

```bash
# Script batch avec configuration dynamique
set CONFIG_FILE=configs\session_%DATE%.json
python shared\src\main.py -c %CONFIG_FILE%

# Intégration dans des workflows CI/CD
python shared\src\main.py -c ci_configs\test_environment.json
```

### Environnements multiples

```bash
# Développement
python shared\src\main.py -c configs\dev.json

# Test
python shared\src\main.py -c configs\test.json

# Production
python shared\src\main.py -c configs\prod.json
```

## Gestion des erreurs

### Fichier de configuration introuvable

Si le fichier spécifié n'existe pas :

```
[WARNING] Configuration par défaut non trouvée: mon_config.json
[INFO] Utilisation des valeurs par défaut
```

L'application continuera avec les valeurs par défaut intégrées.

### Configuration invalide

Si le fichier JSON est malformé, l'application affichera une erreur détaillée et s'arrêtera.

### Permissions insuffisantes

Si l'application n'a pas les permissions pour lire le fichier de configuration, elle utilisera les valeurs par défaut.

## Bonnes pratiques

### Organisation des configurations

```
configs/
├── dev.json              # Développement
├── test.json             # Tests
├── prod.json             # Production
├── models/
│   ├── tiny.json         # Modèle léger
│   ├── medium.json       # Modèle standard
│   └── large.json        # Modèle haute qualité
└── hardware/
    ├── cpu_only.json     # CPU uniquement
    └── gpu_optimized.json # GPU optimisé
```

### Nommage des fichiers

- Utilisez des noms descriptifs : `whisper_large_gpu.json`
- Incluez l'environnement : `dev_config.json`, `prod_config.json`
- Spécifiez le matériel : `cpu_config.json`, `cuda_config.json`

### Versioning

- Versionnez vos configurations avec Git
- Documentez les changements dans les configurations
- Utilisez des configurations par défaut stables

## Intégration avec les scripts existants

Les scripts `start.bat` existants utilisent déjà cette fonctionnalité :

```batch
python main.py --config "%PROJECT_DIR%config.json"
```

Cette approche garantit que chaque projet utilise sa configuration spécifique tout en permettant une flexibilité maximale pour les utilisateurs avancés.

## Dépannage

### L'option --config ne fonctionne pas

Vérifiez que vous utilisez la version mise à jour de `shared/src/main.py` qui inclut le support d'argparse.

### Configuration ignorée

Assurez-vous que le chemin vers le fichier de configuration est correct et que le fichier existe.

### Erreurs de syntaxe JSON

Validez votre fichier JSON avec un outil en ligne ou un éditeur avec validation JSON intégrée.