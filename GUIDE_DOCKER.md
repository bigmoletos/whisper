# Guide Docker - Whisper STT Global

## ⚠️ Limitations sur Windows

**Important** : Docker sur Windows a des limitations importantes pour ce type d'application :

1. **Accès au microphone** : Complexe, nécessite des configurations spéciales
2. **Injection de texte** : Ne peut pas injecter du texte dans les applications Windows depuis un conteneur
3. **Raccourcis clavier globaux** : Ne fonctionnent pas depuis un conteneur Docker

**Recommandation** : Utilisez Docker uniquement sur **Linux** ou **WSL2** avec une configuration spéciale.

## Utilisation sur Linux / WSL2

### Prérequis

- Docker et Docker Compose installés
- WSL2 configuré (si sur Windows)
- Accès aux périphériques audio configuré

### Construction de l'image

```bash
# Construire l'image Docker
docker-compose build

# Ou directement
docker build -t whisper-stt:latest .
```

### Démarrage du service

```bash
# Démarrer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Configuration

L'image Docker inclut :
- ✅ Python 3.11
- ✅ Rust (pour Faster-Whisper)
- ✅ Faster-Whisper préinstallé
- ✅ Toutes les dépendances nécessaires

## Utilisation sur Windows avec WSL2

### Configuration WSL2

1. **Installer WSL2** :
   ```powershell
   wsl --install
   ```

2. **Installer Docker Desktop** avec support WSL2

3. **Configurer l'accès audio** dans WSL2 (complexe)

### Limitations

Même avec WSL2, l'injection de texte dans les applications Windows ne fonctionnera pas depuis le conteneur.

## Alternative : Service Windows Natif

Pour Windows, il est **fortement recommandé** d'utiliser le service Windows natif :

```bash
scripts\install_windows_service.bat
```

Avantages :
- ✅ Accès direct au microphone Windows
- ✅ Injection de texte fonctionnelle
- ✅ Raccourcis clavier globaux
- ✅ Démarrage automatique au boot

## Commandes Docker Utiles

### Construire l'image

```bash
docker-compose build
```

### Démarrer le service

```bash
docker-compose up -d
```

### Voir les logs

```bash
docker-compose logs -f whisper-stt
```

### Arrêter le service

```bash
docker-compose down
```

### Redémarrer

```bash
docker-compose restart
```

### Accéder au shell du conteneur

```bash
docker-compose exec whisper-stt /bin/bash
```

### Vérifier le statut

```bash
docker-compose ps
```

## Configuration Docker

### Modifier les ressources

Éditez `docker-compose.yml` pour ajuster les limites :

```yaml
deploy:
  resources:
    limits:
      memory: 12G  # Ajustez selon votre RAM
      cpus: '4.0'  # Ajustez selon votre CPU
```

### Variables d'environnement

Vous pouvez surcharger la configuration via des variables d'environnement dans `docker-compose.yml`.

## Dépannage

### Erreur : "Cannot connect to the Docker daemon"

- Vérifiez que Docker Desktop est démarré
- Vérifiez que le service Docker est en cours d'exécution

### Erreur : "Permission denied" pour /dev/snd

Sur Linux, ajoutez votre utilisateur au groupe audio :
```bash
sudo usermod -a -G audio $USER
```

### Le conteneur ne démarre pas

Vérifiez les logs :
```bash
docker-compose logs whisper-stt
```

### Problème de mémoire

Réduisez les limites dans `docker-compose.yml` ou augmentez la RAM allouée à Docker.

## Recommandation Finale

**Pour Windows** : Utilisez le service Windows natif (`install_windows_service.bat`)

**Pour Linux** : Utilisez Docker avec cette configuration

**Pour développement/test** : Docker est utile pour tester l'isolation et la portabilité

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
