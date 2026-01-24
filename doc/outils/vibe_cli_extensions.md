# Guide des Extensions CLI Vibe (Mistral)

**Auteur** : Bigmoletos  
**Version** : 1.0  
**Date** : 24-01-2026  
**Contexte** : Guide de référence pour utiliser Mistral Vibe CLI avec ses outils, agents et configurations.

---

## 📋 Table des matières

1. [Tableau récapitulatif des commandes](#-tableau-récapitulatif-des-commandes)
2. [Installation et mise à jour](#-installation-et-mise-à-jour)
3. [Syntaxe interactive](#-syntaxe-interactive)
4. [Outils intégrés](#-outils-intégrés)
5. [Configuration](#-configuration)
6. [Agents personnalisés](#-agents-personnalisés)
7. [Modes d'approbation](#-modes-dapprobation)
8. [Exemples pratiques](#-exemples-pratiques)

---

## 📊 Tableau récapitulatif des commandes

### Commandes CLI principales

| Commande | Description | Exemple |
|----------|-------------|---------|
| `vibe` | Lancer en mode interactif | `vibe` |
| `vibe "prompt"` | Démarrer avec un prompt | `vibe "Analyse ce projet"` |
| `vibe --auto-approve` | Mode auto-approbation | `vibe --auto-approve` |
| `vibe --agent <name>` | Utiliser un agent personnalisé | `vibe --agent security` |
| `vibe --model <model>` | Spécifier le modèle | `vibe --model devstral-large` |
| `vibe --help` | Afficher l'aide | `vibe --help` |
| `vibe --version` | Afficher la version | `vibe --version` |

### Préfixes interactifs

| Préfixe | Description | Exemple |
|---------|-------------|---------|
| `@` | Référencer un fichier | `@src/main.py` |
| `!` | Exécuter une commande shell | `!git status` |
| `/` | Commandes slash | `/help` |

### Commandes slash

| Commande | Description |
|----------|-------------|
| `/config` | Voir/modifier la configuration |
| `/theme` | Changer le thème visuel |

**Note** : Vibe CLI est très minimaliste. La documentation officielle mentionne principalement `/config` et `/theme` comme commandes slash. D'autres commandes comme `/help`, `/clear`, `/quit`, `/model`, `/tools`, `/history`, `/undo`, `/diff`, `/save`, `/load` ne sont pas documentées officiellement et peuvent ne pas exister.

**Interaction principale** : Utilisez les préfixes `@` (fichiers), `!` (shell) et le mode interactif standard.

### Outils disponibles

| Outil | Description | Commande interne |
|-------|-------------|------------------|
| `read_file` | Lire un fichier | Automatique |
| `write_file` | Écrire dans un fichier | Automatique |
| `search_replace` | Rechercher et remplacer | Automatique |
| `bash` | Exécuter des commandes shell | Automatique |
| `grep` | Rechercher dans les fichiers | Automatique |
| `ripgrep` | Recherche rapide | Automatique |
| `todo` | Gestion des tâches | Automatique |
| `glob` | Recherche de fichiers par pattern | Automatique |

---

## 🚀 Installation et mise à jour

### Installation

| Méthode | Commande |
|---------|----------|
| **Script officiel** | `curl -LsSf https://mistral.ai/vibe/install.sh \| bash` |
| **uv (recommandé)** | `uv tool install mistral-vibe` |
| **pip** | `pip install mistral-vibe` |
| **pipx** | `pipx install mistral-vibe` |

### Mise à jour

```bash
# Via uv
uv tool upgrade mistral-vibe

# Via pip
pip install --upgrade mistral-vibe

# Via pipx
pipx upgrade mistral-vibe
```

### Configuration initiale

```bash
# Configurer la clé API Mistral
export MISTRAL_API_KEY="your-api-key"

# Ou via fichier de configuration
vibe
# Puis suivre les instructions de configuration
```

---

## ⌨️ Syntaxe interactive

### Préfixes spéciaux

Vibe utilise des préfixes pour différentes actions :

#### `@` - Référence de fichier

```bash
# Référencer un fichier
@src/main.py explique ce fichier

# Référencer plusieurs fichiers
@src/main.py @src/utils.py compare ces fichiers

# Autocomplétion disponible après @
@src/[TAB]
```

#### `!` - Commandes shell

```bash
# Exécuter une commande
!git status

# Exécuter et analyser le résultat
!npm test puis analyse les erreurs

# Commandes complexes
!find . -name "*.py" -type f
```

#### `/` - Commandes slash

```bash
# Configuration
/config

# Changer de thème
/theme
```

**Note** : Vibe CLI se concentre principalement sur les préfixes `@` et `!` plutôt que sur de nombreuses commandes slash.

### Autocomplétion

| Préfixe | Autocomplétion |
|---------|----------------|
| `@` | Fichiers et dossiers |
| `/` | Commandes slash |
| `!` | Historique shell |

---

## 🔧 Outils intégrés

### Description
Vibe dispose d'une suite d'outils intégrés que l'IA utilise automatiquement selon les besoins.

### Tableau des outils

| Outil | Description | Paramètres |
|-------|-------------|------------|
| `read_file` | Lit le contenu d'un fichier | `path`, `offset`, `limit` |
| `write_file` | Écrit dans un fichier | `path`, `content` |
| `search_replace` | Recherche et remplace du texte | `path`, `old`, `new` |
| `bash` | Exécute des commandes shell | `command`, `timeout` |
| `grep` | Recherche dans les fichiers | `pattern`, `path`, `flags` |
| `ripgrep` | Recherche rapide (rg) | `pattern`, `path`, `options` |
| `glob` | Trouve des fichiers par pattern | `pattern`, `path` |
| `todo` | Gère une liste de tâches | `action`, `task` |

### Détails des outils

#### `read_file`

Lit le contenu d'un fichier avec support de pagination.

```
Paramètres :
- path: Chemin du fichier
- offset: Ligne de début (optionnel)
- limit: Nombre de lignes (optionnel)
```

#### `write_file`

Écrit ou crée un fichier.

```
Paramètres :
- path: Chemin du fichier
- content: Contenu à écrire
```

#### `search_replace`

Effectue des remplacements dans un fichier.

```
Paramètres :
- path: Chemin du fichier
- old: Texte à rechercher
- new: Texte de remplacement
- count: Nombre de remplacements (optionnel)
```

#### `bash`

Exécute des commandes dans un terminal stateful.

```
Paramètres :
- command: Commande à exécuter
- timeout: Timeout en secondes (optionnel)
- cwd: Répertoire de travail (optionnel)
```

#### `todo`

Gère une liste de tâches pour suivre la progression.

```
Actions :
- add: Ajouter une tâche
- complete: Marquer comme terminée
- list: Lister les tâches
- clear: Effacer les tâches terminées
```

---

## ⚙️ Configuration

### Fichiers de configuration

| Emplacement | Scope |
|-------------|-------|
| `~/.vibe/config.toml` | Global (utilisateur) |
| `./.vibe/config.toml` | Projet |

### Structure config.toml

```toml
# Configuration globale Vibe

[api]
# Clé API Mistral
api_key = "your-api-key"
# Ou utiliser une variable d'environnement
# api_key = "${MISTRAL_API_KEY}"

[model]
# Modèle par défaut
default = "devstral-medium"
# Modèles disponibles: devstral-small, devstral-medium, devstral-large

[tools]
# Outils activés par défaut
enabled = ["read_file", "write_file", "bash", "grep", "todo"]

# Mode d'approbation
# "ask" = demander confirmation
# "auto" = approuver automatiquement
# "deny" = refuser automatiquement
approval_mode = "ask"

# Outils auto-approuvés
auto_approve = ["read_file", "grep", "glob"]

# Outils toujours bloqués
blocked = []

[shell]
# Shell par défaut
shell = "/bin/bash"
# Timeout par défaut (secondes)
timeout = 30

[ui]
# Thème
theme = "dark"
# Activer les couleurs
colors = true
# Afficher les suggestions
suggestions = true

[history]
# Taille de l'historique
max_size = 1000
# Sauvegarder l'historique
save = true
# Emplacement
path = "~/.vibe/history"

[context]
# Scanner automatiquement le projet
auto_scan = true
# Fichiers à ignorer
ignore = [".git", "node_modules", "__pycache__", ".venv"]
# Profondeur maximale
max_depth = 10
```

### Variables d'environnement

| Variable | Description |
|----------|-------------|
| `MISTRAL_API_KEY` | Clé API Mistral |
| `VIBE_MODEL` | Modèle par défaut |
| `VIBE_CONFIG` | Chemin du fichier config |
| `VIBE_AUTO_APPROVE` | Mode auto-approbation (true/false) |

---

## 🤖 Agents personnalisés

### Description
Les agents personnalisés permettent de configurer des comportements spécialisés pour différents types de tâches.

### Emplacement

```
~/.vibe/agents/           # Global
./.vibe/agents/           # Projet
```

### Structure d'un agent

```
.vibe/agents/
├── security.toml
├── reviewer.toml
└── docs.toml
```

### Format d'un agent

```toml
# .vibe/agents/security.toml

[agent]
name = "security"
description = "Agent spécialisé en audit de sécurité"

[agent.prompt]
system = """
Tu es un expert en sécurité informatique.
Ton rôle est d'identifier les vulnérabilités et de proposer des corrections.

Focus sur :
- Injections SQL/XSS
- Gestion des secrets
- Authentification/Autorisation
- Validation des entrées
"""

[agent.tools]
# Outils disponibles pour cet agent
enabled = ["read_file", "grep", "ripgrep", "glob"]
# Pas d'écriture pour l'audit
blocked = ["write_file", "bash"]

[agent.context]
# Fichiers à analyser en priorité
focus = ["**/*.py", "**/*.js", "**/*.ts", "**/auth/**", "**/api/**"]
```

### Utilisation

```bash
# Lancer avec un agent
vibe --agent security

# En mode interactif
/agent security
```

### Exemple d'agent de documentation

```toml
# .vibe/agents/docs.toml

[agent]
name = "docs"
description = "Agent spécialisé en documentation"

[agent.prompt]
system = """
Tu es un expert en documentation technique.
Génère des documentations claires et complètes.

Style :
- Markdown formaté
- Exemples de code
- Sections bien structurées
"""

[agent.tools]
enabled = ["read_file", "write_file", "glob"]
auto_approve = ["read_file"]

[agent.templates]
readme = "templates/README.md.j2"
api_doc = "templates/API.md.j2"
```

---

## 🛡️ Modes d'approbation

### Description
Vibe propose différents modes de contrôle pour l'exécution des outils.

### Modes disponibles

| Mode | Description | Flag |
|------|-------------|------|
| **Ask** | Demande confirmation (défaut) | `--approval ask` |
| **Auto** | Approuve automatiquement | `--auto-approve` |
| **Deny** | Refuse automatiquement | `--approval deny` |

### Configuration par outil

```toml
# config.toml

[tools]
# Mode global
approval_mode = "ask"

# Outils toujours approuvés
auto_approve = ["read_file", "grep", "glob"]

# Outils toujours bloqués
blocked = ["rm", "sudo"]

# Outils nécessitant confirmation
require_confirm = ["write_file", "bash"]
```

### Mode YOLO (Auto-approve)

```bash
# Lancer en mode auto-approve
vibe --auto-approve

# ⚠️ Attention : toutes les actions sont exécutées sans confirmation
```

### Bonnes pratiques

| Contexte | Mode recommandé |
|----------|-----------------|
| Production | `ask` |
| Développement | `ask` ou outils spécifiques auto |
| Tests automatisés | `auto` avec outils limités |
| Sandbox/Docker | `auto` acceptable |

---

## 📝 Exemples pratiques

### Exemple 1 : Session de développement

```bash
# Démarrer Vibe
vibe

# Analyser le projet
> Analyse la structure de ce projet et résume-la

# Référencer un fichier
> @src/main.py explique cette fonction

# Modifier du code
> Ajoute la gestion des erreurs dans @src/utils.py

# Exécuter les tests
> !pytest tests/

# Configurer l'affichage
/config

# Changer le thème
/theme
```

**Note** : Vibe CLI n'a pas de commande `/diff` documentée. Les modifications sont affichées automatiquement.

### Exemple 2 : Configuration projet Python

```toml
# .vibe/config.toml

[api]
api_key = "${MISTRAL_API_KEY}"

[model]
default = "devstral-medium"

[tools]
enabled = ["read_file", "write_file", "bash", "grep", "todo"]
auto_approve = ["read_file", "grep"]

[context]
auto_scan = true
ignore = [".git", "__pycache__", ".venv", "*.pyc"]

[shell]
shell = "/bin/bash"
timeout = 60
```

### Exemple 3 : Agent de refactoring

```toml
# .vibe/agents/refactor.toml

[agent]
name = "refactor"
description = "Agent spécialisé en refactoring"

[agent.prompt]
system = """
Tu es un expert en refactoring et clean code.
Améliore le code en suivant :
- Principes SOLID
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- Patterns de conception appropriés
"""

[agent.tools]
enabled = ["read_file", "write_file", "search_replace", "grep"]
auto_approve = ["read_file"]
```

### Exemple 4 : Script d'automatisation

```bash
#!/bin/bash
# Script de revue de code automatique

# Lancer Vibe en mode non-interactif
vibe --auto-approve --agent reviewer << 'EOF'
Analyse tous les fichiers modifiés depuis le dernier commit.
Pour chaque fichier :
1. Vérifie la qualité du code
2. Identifie les problèmes potentiels
3. Suggère des améliorations

Génère un rapport au format Markdown dans review_report.md
EOF
```

### Exemple 5 : Gestion des tâches avec todo

```bash
# En mode interactif

# Ajouter des tâches
> Crée une liste de tâches pour implémenter l'authentification

# L'IA utilise l'outil todo automatiquement
# Exemple de sortie :
# ✓ todo add "Créer le modèle User"
# ✓ todo add "Implémenter le endpoint /login"
# ✓ todo add "Ajouter le middleware JWT"

# Voir les tâches
> /todo list

# Marquer comme terminé
> /todo complete 1
```

---

## 📚 Ressources supplémentaires

| Ressource | URL |
|-----------|-----|
| **Documentation officielle** | [docs.mistral.ai/mistral-vibe](https://docs.mistral.ai/mistral-vibe) |
| **Installation** | [docs.mistral.ai/mistral-vibe/introduction/install](https://docs.mistral.ai/mistral-vibe/introduction/install) |
| **Configuration** | [docs.mistral.ai/mistral-vibe/introduction/configuration](https://docs.mistral.ai/mistral-vibe/introduction/configuration) |
| **GitHub** | [github.com/mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe) |
| **Modèles Devstral** | [docs.mistral.ai/models/devstral](https://docs.mistral.ai/models/devstral) |

---

## 🔄 Notes de version

**v1.0 (24-01-2026)**
- Création du guide initial
- Documentation installation et configuration
- Documentation outils intégrés
- Documentation agents personnalisés
- Modes d'approbation
- Tableaux récapitulatifs
- Exemples pratiques

---

**Note** : Ce document est une référence pratique. Certaines commandes peuvent évoluer. Consultez la documentation officielle Mistral pour les informations à jour.

<<<END>>>
