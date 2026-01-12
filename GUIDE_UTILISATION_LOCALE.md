# Guide d'Utilisation Locale - Whisper STT

## Fonctionnement Local Actuel

### Whisper fonctionne déjà 100% en local

Le système actuel utilise **Whisper d'OpenAI** qui fonctionne **entièrement hors ligne** après l'installation initiale :

1. **Téléchargement initial** : Le modèle Whisper est téléchargé une seule fois (au premier lancement)
2. **Stockage local** : Le modèle est stocké dans `~/.cache/whisper/` (Windows: `C:\Users\<user>\.cache\whisper\`)
3. **Traitement local** : Toute la transcription se fait sur votre machine, aucune connexion Internet requise

### Modèles Whisper disponibles

| Modèle | Taille | RAM | Usage | Téléchargement |
|--------|--------|-----|-------|----------------|
| **tiny** | ~39 MB | ~1 GB | Test rapide | Automatique |
| **base** | ~74 MB | ~1 GB | Usage léger | Automatique |
| **small** | ~244 MB | ~2 GB | Bon compromis | Automatique |
| **medium** | ~769 MB | ~5 GB | **Recommandé** | Automatique |
| **large** | ~1550 MB | ~10 GB | Maximum précision | Automatique |

**Configuration actuelle** : Le modèle est défini dans `config.json` :
```json
{
  "whisper": {
    "model": "medium",
    "language": "fr",
    "device": "cpu"
  }
}
```

## Différence avec Ollama/LM Studio

### Whisper vs LLM

- **Whisper** : Transcription vocale (Speech-to-Text) → Convertit la voix en texte
- **Ollama/LM Studio** : Modèles de langage (LLM) → Génèrent/améliorent du texte

Ce sont des outils **complémentaires** mais **différents** :
- Whisper = "Écouter et transcrire"
- Ollama/LM Studio = "Comprendre et générer du texte"

## Intégration Optionnelle avec Ollama/LM Studio

Si vous souhaitez **améliorer les transcriptions** avec un LLM local, voici comment procéder :

### Cas d'usage

1. **Correction orthographique** : Corriger les erreurs de transcription
2. **Ponctuation améliorée** : Améliorer la ponctuation et la mise en forme
3. **Reformulation** : Reformuler le texte pour plus de clarté
4. **Résumé** : Créer un résumé du texte transcrit

### Architecture proposée

```
Microphone → Whisper → Texte brut → Ollama/LM Studio → Texte amélioré → Injection
```

## Implémentation avec Ollama

### 1. Installation d'Ollama

```bash
# Télécharger depuis https://ollama.ai
# Ou via winget
winget install Ollama.Ollama
```

### 2. Télécharger un modèle LLM

Pour la correction/amélioration de texte en français, recommandations :

**Option 1 : Modèle léger (rapide)**
```bash
ollama pull mistral:7b
```

**Option 2 : Modèle performant (meilleure qualité)**
```bash
ollama pull llama3.2:3b
# ou
ollama pull mistral:7b-instruct
```

**Option 3 : Modèle spécialisé français**
```bash
ollama pull mistral:7b-instruct-q4_K_M
```

### 3. Créer un module d'intégration

Créer `src/llm_enhancer.py` :

```python
"""
Module d'amélioration de texte avec Ollama
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OllamaEnhancer:
    """Améliore les transcriptions avec Ollama"""

    def __init__(self, model: str = "mistral:7b", base_url: str = "http://localhost:11434"):
        """
        Initialise l'améliorateur de texte

        Args:
            model: Nom du modèle Ollama à utiliser
            base_url: URL de l'API Ollama
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"

        logger.info(f"Ollama enhancer initialisé avec le modèle: {model}")

    def enhance_text(self, text: str, task: str = "correct") -> str:
        """
        Améliore le texte transcrit

        Args:
            text: Texte à améliorer
            task: Type d'amélioration (correct, punctuate, reformulate)

        Returns:
            Texte amélioré
        """
        if not text or not text.strip():
            return text

        prompts = {
            "correct": f"Corrige les erreurs orthographiques et grammaticales dans ce texte, garde le sens original :\n\n{text}\n\nTexte corrigé :",
            "punctuate": f"Améliore la ponctuation et la mise en forme de ce texte, garde le sens original :\n\n{text}\n\nTexte amélioré :",
            "reformulate": f"Reformule ce texte pour plus de clarté, garde le sens original :\n\n{text}\n\nTexte reformulé :"
        }

        prompt = prompts.get(task, prompts["correct"])

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                enhanced_text = result.get("response", text).strip()
                logger.info(f"Texte amélioré avec succès (tâche: {task})")
                return enhanced_text
            else:
                logger.warning(f"Erreur Ollama: {response.status_code}")
                return text

        except requests.exceptions.ConnectionError:
            logger.warning("Ollama non disponible, retour du texte original")
            return text
        except Exception as e:
            logger.error(f"Erreur lors de l'amélioration: {e}", exc_info=True)
            return text

    def is_available(self) -> bool:
        """Vérifie si Ollama est disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
```

### 4. Modifier le service principal

Ajouter dans `src/main.py` :

```python
from llm_enhancer import OllamaEnhancer

# Dans __init__ :
self.llm_enhancer: Optional[OllamaEnhancer] = None

# Dans _initialize_components :
# Optionnel : activer l'amélioration LLM
if self.config.get("llm", {}).get("enabled", False):
    llm_config = self.config.get("llm", {})
    self.llm_enhancer = OllamaEnhancer(
        model=llm_config.get("model", "mistral:7b"),
        base_url=llm_config.get("base_url", "http://localhost:11434")
    )
    if self.llm_enhancer.is_available():
        self.logger.info("Amélioration LLM activée")
    else:
        self.logger.warning("Ollama non disponible, amélioration LLM désactivée")
        self.llm_enhancer = None

# Dans _process_recording, après la transcription :
text = self.transcriber.transcribe(audio_data, sample_rate=self.audio_capture.sample_rate)

if text:
    # Améliorer avec LLM si activé
    if self.llm_enhancer:
        llm_task = self.config.get("llm", {}).get("task", "correct")
        text = self.llm_enhancer.enhance_text(text, task=llm_task)

    # Injecter le texte
    if self.text_injector:
        # ...
```

### 5. Configuration dans config.json

```json
{
  "whisper": {
    "model": "medium",
    "language": "fr",
    "device": "cpu"
  },
  "llm": {
    "enabled": false,
    "model": "mistral:7b",
    "base_url": "http://localhost:11434",
    "task": "correct"
  },
  "hotkey": {
    "modifiers": ["ctrl", "alt"],
    "key": "7"
  }
}
```

**Options pour `task`** :
- `"correct"` : Correction orthographique et grammaticale
- `"punctuate"` : Amélioration de la ponctuation
- `"reformulate"` : Reformulation pour plus de clarté

## Implémentation avec LM Studio

LM Studio fonctionne de manière similaire à Ollama mais avec une interface graphique.

### 1. Installation

- Télécharger depuis https://lmstudio.ai
- Installer et lancer l'application

### 2. Télécharger un modèle

Dans LM Studio :
1. Aller dans "Search" ou "Browse"
2. Rechercher un modèle (ex: "mistral", "llama")
3. Télécharger un modèle quantifié (Q4_K_M recommandé)

### 3. Démarrer le serveur local

Dans LM Studio :
1. Aller dans "Local Server"
2. Sélectionner le modèle téléchargé
3. Cliquer sur "Start Server"
4. Noter l'URL (généralement `http://localhost:1234`)

### 4. Adapter le code

Modifier `src/llm_enhancer.py` pour supporter LM Studio :

```python
class LMStudioEnhancer:
    """Améliore les transcriptions avec LM Studio"""

    def __init__(self, base_url: str = "http://localhost:1234"):
        self.base_url = base_url
        self.api_url = f"{base_url}/v1/completions"

    def enhance_text(self, text: str, task: str = "correct") -> str:
        prompt = f"Corrige les erreurs dans ce texte :\n\n{text}\n\nTexte corrigé :"

        response = requests.post(
            self.api_url,
            json={
                "model": "local-model",  # Nom du modèle dans LM Studio
                "prompt": prompt,
                "max_tokens": 500,
                "temperature": 0.3
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["text"].strip()
        return text
```

## Recommandations

### Pour une utilisation simple (recommandé)

**Utilisez uniquement Whisper** :
- ✅ Fonctionne 100% hors ligne
- ✅ Rapide (1-3 secondes)
- ✅ Pas de dépendances supplémentaires
- ✅ Précision excellente avec le modèle medium

### Pour une amélioration avancée

**Ajoutez Ollama/LM Studio** si vous avez besoin de :
- Correction orthographique avancée
- Reformulation du texte
- Résumé automatique
- Traduction

**Inconvénients** :
- ⚠️ Nécessite plus de RAM (8-16 GB)
- ⚠️ Plus lent (5-15 secondes supplémentaires)
- ⚠️ Consomme plus de ressources CPU/GPU

## Résumé

| Fonctionnalité | Whisper seul | Whisper + Ollama |
|----------------|--------------|------------------|
| Transcription | ✅ | ✅ |
| Correction | Basique | Avancée |
| Vitesse | Rapide | Plus lent |
| RAM requise | 5 GB | 8-16 GB |
| Complexité | Simple | Moyenne |

**Conclusion** : Pour la plupart des usages, **Whisper seul est suffisant**. Ajoutez Ollama/LM Studio uniquement si vous avez besoin d'améliorations avancées du texte.

---

**Auteur** : Bigmoletos
**Date** : 2025-01-11
