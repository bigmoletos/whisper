# Mode Opératoire - Fonctionnement de Whisper STT

## Vue d'ensemble

Ce document explique le fonctionnement technique de Whisper (OpenAI) et son intégration dans le service de transcription vocale globale pour Windows.

## Qu'est-ce que Whisper ?

Whisper est un modèle de reconnaissance vocale (Speech-to-Text) développé par OpenAI. Il utilise l'apprentissage profond (deep learning) pour convertir la parole en texte avec une grande précision, même dans des conditions difficiles (bruit de fond, accents, etc.).

### Caractéristiques principales

- **Multilingue** : Supporte plus de 100 langues
- **Robuste** : Fonctionne bien même avec du bruit de fond
- **Précis** : Très bonne précision sur la transcription
- **Local** : Peut fonctionner entièrement hors ligne après installation

## Architecture du système

### Flux de données

```
Microphone → Capture Audio → Traitement → Whisper → Transcription → Injection Texte
```

### Composants du système

1. **Capture Audio** (`audio_capture.py`)
   - Capture le signal audio du microphone en temps réel
   - Détecte les périodes de silence
   - Normalise le signal audio

2. **Transcription Whisper** (`whisper_transcriber.py`)
   - Charge le modèle Whisper (une seule fois au démarrage)
   - Traite les segments audio capturés
   - Retourne le texte transcrit

3. **Injection de Texte** (`text_injector.py`)
   - Injecte le texte transcrit dans le champ actif
   - Utilise le presse-papiers ou la simulation de frappe

4. **Service Principal** (`main.py`)
   - Coordonne tous les composants
   - Gère les raccourcis clavier
   - Gère le cycle de vie du service

## Fonctionnement détaillé

### 1. Initialisation du service

Lors du démarrage du service :

```python
# 1. Chargement de la configuration
config = load_config("config.json")

# 2. Initialisation du logger
setup_logging()

# 3. Création des composants
audio_capture = AudioCapture(...)
transcriber = WhisperTranscriber(model="medium", language="fr")
text_injector = TextInjector()

# 4. Chargement du modèle Whisper (peut prendre 10-30 secondes)
transcriber.load_model()  # Télécharge le modèle si nécessaire
```

**Important** : Le chargement du modèle Whisper est l'étape la plus longue. Le modèle est téléchargé automatiquement la première fois (plusieurs GB selon le modèle choisi).

### 2. Enregistrement audio

Quand l'utilisateur appuie sur le raccourci clavier (Ctrl+Shift+V) :

```python
# Démarrage de la capture
audio_capture.start_recording()

# Le callback audio_callback() est appelé en continu
# Les données audio sont stockées dans audio_buffer
```

**Format audio** :
- Fréquence d'échantillonnage : 16000 Hz (standard pour Whisper)
- Canaux : 1 (mono)
- Format : Float32, normalisé entre -1.0 et 1.0

### 3. Détection de fin d'enregistrement

L'enregistrement s'arrête quand :
- L'utilisateur réappuie sur le raccourci (toggle)
- Une période de silence est détectée (configurable)

```python
# Détection de silence
rms = sqrt(mean(audio_chunk²))  # Calcul du niveau RMS
if rms < silence_threshold:
    # Silence détecté
    if silence_duration >= 1.5 secondes:
        stop_recording()
```

### 4. Transcription avec Whisper

Une fois l'audio capturé :

```python
# 1. Normalisation de l'audio
audio = audio / max(abs(audio))  # Normalisation [-1, 1]

# 2. Appel à Whisper
result = whisper_model.transcribe(
    audio,
    language="fr",
    task="transcribe"
)

# 3. Extraction du texte
text = result["text"].strip()
```

**Processus interne de Whisper** :

1. **Préprocessing** :
   - Découpage en fenêtres temporelles
   - Transformation en spectrogramme (représentation fréquentielle)

2. **Encodage** :
   - Le modèle encode l'audio en représentations numériques
   - Utilise un réseau de neurones Transformer

3. **Décodage** :
   - Génération de tokens de texte
   - Détection automatique de la langue (si non spécifiée)
   - Ponctuation et mise en forme

4. **Post-traitement** :
   - Nettoyage du texte
   - Suppression des répétitions
   - Correction des erreurs courantes

### 5. Injection du texte

Le texte transcrit est injecté dans le champ actif :

```python
# Méthode 1 : Via presse-papiers (recommandé)
pyperclip.copy(text)
pyautogui.hotkey('ctrl', 'v')

# Méthode 2 : Simulation de frappe
pyautogui.write(text)
```

## Modèles Whisper disponibles

| Modèle | Taille | RAM requise | Vitesse | Précision |
|--------|--------|-------------|---------|-----------|
| tiny   | ~39 MB | ~1 GB       | Très rapide | Moyenne |
| base   | ~74 MB | ~1 GB       | Rapide | Bonne |
| small  | ~244 MB | ~2 GB      | Moyenne | Très bonne |
| medium | ~769 MB | ~5 GB      | Lente | Excellente |
| large  | ~1550 MB | ~10 GB    | Très lente | Maximale |

**Recommandation** : Utilisez `medium` pour un bon compromis vitesse/précision.

## Optimisations et performances

### Utilisation du GPU (CUDA)

Si vous avez un GPU NVIDIA :

```json
{
  "whisper": {
    "device": "cuda"
  }
}
```

**Avantages** :
- Transcription 5-10x plus rapide
- Meilleure utilisation des ressources

**Prérequis** :
- GPU NVIDIA avec support CUDA
- PyTorch avec support CUDA installé

### Gestion de la mémoire

Le modèle Whisper est chargé une seule fois en mémoire. Pour libérer la mémoire :

```python
# Le modèle reste en mémoire pendant toute la durée du service
# Pour libérer : arrêter le service
```

### Latence

La latence dépend de :
- **Taille du modèle** : Plus grand = plus lent
- **Longueur de l'audio** : Plus long = plus de temps
- **Matériel** : CPU vs GPU
- **Charge système** : Autres applications en cours

**Temps typiques** (modèle medium, CPU) :
- 3 secondes d'audio → ~2-3 secondes de transcription
- 10 secondes d'audio → ~5-7 secondes de transcription

## Dépannage technique

### Problème : Modèle ne se charge pas

**Causes possibles** :
- Pas assez de RAM
- Connexion Internet nécessaire pour le premier téléchargement
- Espace disque insuffisant (~2-10 GB selon le modèle)

**Solutions** :
- Utiliser un modèle plus petit (tiny, base)
- Vérifier l'espace disque disponible
- Vérifier la connexion Internet (premier lancement)

### Problème : Transcription lente

**Causes possibles** :
- Modèle trop grand pour le matériel
- CPU surchargé
- Pas de GPU disponible

**Solutions** :
- Utiliser un modèle plus petit
- Fermer les autres applications
- Installer PyTorch avec CUDA si GPU disponible

### Problème : Transcription incorrecte

**Causes possibles** :
- Mauvaise qualité audio
- Langue incorrecte dans la config
- Bruit de fond important
- Parole trop rapide ou peu claire

**Solutions** :
- Améliorer la qualité du microphone
- Vérifier la langue dans `config.json`
- Réduire le bruit de fond
- Parler plus clairement et distinctement

## Architecture technique détaillée

### Pipeline de traitement

```
┌─────────────┐
│  Microphone │
└──────┬──────┘
       │ Signal analogique
       ▼
┌─────────────┐
│  Sounddevice │ ← Échantillonnage 16kHz
└──────┬──────┘
       │ Array numpy (float32)
       ▼
┌─────────────┐
│ Normalisation│ ← Normalisation [-1, 1]
└──────┬──────┘
       │ Audio normalisé
       ▼
┌─────────────┐
│   Whisper   │ ← Modèle Transformer
└──────┬──────┘
       │ Texte transcrit
       ▼
┌─────────────┐
│ Text Injector│ ← Injection dans champ actif
└─────────────┘
```

### Structure du modèle Whisper

Le modèle Whisper utilise une architecture Transformer :

1. **Encoder** : Traite l'audio en séquences de tokens
2. **Decoder** : Génère le texte à partir des tokens encodés
3. **Attention Mechanism** : Fait correspondre les parties audio aux mots

### Format des données

**Entrée (Audio)** :
- Format : NumPy array de float32
- Shape : `(n_samples,)` pour mono
- Plage : [-1.0, 1.0]
- Fréquence : 16000 Hz

**Sortie (Texte)** :
- Format : String UTF-8
- Langue : Dépend de la configuration
- Encodage : Unicode

## Sécurité et confidentialité

### Traitement local

- **100% local** : Aucune donnée n'est envoyée en ligne
- **Pas de stockage** : Les enregistrements audio ne sont pas sauvegardés
- **Mémoire temporaire** : Les données sont en RAM uniquement

### Logs

Les logs peuvent contenir :
- Les textes transcrits (pour le débogage)
- Les erreurs et warnings
- Les informations de performance

**Recommandation** : Vérifiez le fichier `whisper_stt.log` régulièrement et supprimez-le si nécessaire.

## Améliorations possibles

### Optimisations futures

1. **Streaming** : Transcription en temps réel pendant la parole
2. **Cache** : Mise en cache des transcriptions similaires
3. **Multi-threading** : Traitement parallèle de plusieurs segments
4. **Compression** : Réduction de la taille du modèle avec la quantification

### Extensions possibles

1. **Support de plusieurs langues** : Détection automatique
2. **Correction automatique** : Post-traitement avec un correcteur orthographique
3. **Commandes vocales** : Exécution de commandes via la voix
4. **Interface graphique** : GUI pour la configuration et le contrôle

## Références

- **Documentation Whisper** : https://github.com/openai/whisper
- **Paper original** : "Robust Speech Recognition via Large-Scale Weak Supervision"
- **Modèles disponibles** : https://github.com/openai/whisper#available-models-and-languages

## Conclusion

Whisper est un modèle puissant qui permet une transcription vocale de haute qualité entièrement locale. Le système implémenté dans ce projet coordonne la capture audio, la transcription et l'injection de texte pour offrir une expérience utilisateur fluide et intuitive.

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
**Version** : 1.0
