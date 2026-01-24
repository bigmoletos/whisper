# Guide des Extensions CLI Kiro (AWS)

**Auteur** : Bigmoletos  
**Version** : 1.0  
**Date** : 24-01-2026  
**Contexte** : Guide de référence pour enrichir Kiro avec MCP, Specs, Steering, Hooks, Agents et configurations.

---

## 📋 Table des matières

1. [Tableau récapitulatif des commandes](#-tableau-récapitulatif-des-commandes)
2. [Installation et mise à jour](#-installation-et-mise-à-jour)
3. [Commandes slash](#-commandes-slash)
4. [Specs - Spécifications](#-specs---spécifications)
5. [Steering - Directives](#-steering---directives)
6. [Hooks - Automatisations](#-hooks---automatisations)
7. [MCP - Model Context Protocol](#-mcp---model-context-protocol)
8. [Agents personnalisés](#-agents-personnalisés)
9. [Configuration globale](#-configuration-globale)
10. [Exemples pratiques](#-exemples-pratiques)

---

## 📊 Tableau récapitulatif des commandes

### Commandes CLI principales

| Commande | Description | Exemple |
|----------|-------------|---------|
| `kiro-cli` | Lancer Kiro en mode interactif | `kiro-cli` |
| `kiro-cli update` | Mettre à jour Kiro CLI | `kiro-cli update` |
| `kiro-cli update -y` | Mise à jour sans confirmation | `kiro-cli update -y` |
| `kiro-cli --version` | Afficher la version | `kiro-cli --version` |
| `kiro-cli --help` | Afficher l'aide | `kiro-cli --help` |

### Commandes slash système (mode interactif)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/model` | Changer de modèle IA ou définir la préférence | `/model` |
| `/agent` | Gérer les agents et basculer entre configurations | `/agent` |
| `/chat` | Gérer les sessions de chat (sauvegarder, charger, basculer) | `/chat` |
| `/mcp` | Voir quels serveurs MCP sont actuellement chargés | `/mcp` |
| `/billing` | Afficher les informations de facturation et crédits | `/billing` |

**Note** : Les autres commandes de base comme `/help`, `/quit`, `/clear`, `/context` existent probablement mais ne sont pas explicitement documentées.

### Commandes slash personnalisées (Steering manuel)

Les fichiers steering avec `inclusion: manual` deviennent des commandes slash. Exemples :

| Commande | Description | Fichier source |
|----------|-------------|----------------|
| `/code-review` | Appliquer les règles de revue de code | `.kiro/steering/code-review.md` |
| `/accessibility` | Appliquer les règles d'accessibilité | `.kiro/steering/accessibility.md` |
| `/performance` | Appliquer les règles de performance | `.kiro/steering/performance.md` |

**Note** : Ces commandes ne sont PAS intégrées - vous devez créer les fichiers steering correspondants.

### Commandes slash personnalisées (Hooks manuels)

Les hooks avec `trigger: manual` deviennent des commandes slash. Exemples :

| Commande | Description | Fichier source |
|----------|-------------|----------------|
| `/sync-source-to-docs` | Synchroniser source vers docs | Hook dans `.kiro/hooks/hooks.yaml` |
| `/run-tests` | Exécuter les tests | Hook dans `.kiro/hooks/hooks.yaml` |
| `/generate-changelog` | Générer le changelog | Hook dans `.kiro/hooks/hooks.yaml` |

**Note** : Ces commandes ne sont PAS intégrées - vous devez créer les hooks correspondants.

---

## 🚀 Installation et mise à jour

### Installation

| Plateforme | Commande d'installation |
|------------|-------------------------|
| **macOS** | `curl -fsSL https://cli.kiro.dev/install \| bash` |
| **Ubuntu/Debian** | `sudo dpkg -i kiro-cli.deb` |
| **Linux AppImage** | `chmod +x kiro-cli.appimage && ./kiro-cli.appimage` |
| **Linux (zip)** | Télécharger puis `./kirocli/install.sh` |

### Mise à jour

```bash
# Mise à jour standard
kiro-cli update

# Mise à jour sans confirmation (non-interactif)
kiro-cli update -y
kiro-cli update --non-interactive
```

### Vérification

```bash
# Vérifier la version
kiro-cli --version

# Afficher l'aide
kiro-cli --help
```

---

## ⌨️ Commandes slash

### Description
Les commandes slash sont accessibles en tapant `/` dans le chat. Elles permettent d'accéder rapidement aux fonctionnalités système, aux hooks manuels et aux fichiers steering sans quitter la conversation.

### Types de commandes

| Type | Description | Configuration |
|------|-------------|---------------|
| **Commandes système** | Gestion de modèle, agent, chat, MCP, billing | Intégrées dans Kiro CLI |
| **Steering manuels** | Appliquent des règles spécifiques | `inclusion: manual` dans le frontmatter du fichier `.kiro/steering/*.md` |
| **Hooks manuels** | Déclenchent des actions personnalisées | `trigger: manual` dans le hook `.kiro/hooks/hooks.yaml` |

### Commandes système détaillées (Documentées officiellement)

#### `/model`
Bascule vers un modèle IA différent ou définit votre préférence de modèle par défaut.

#### `/agent`
Gère les agents et bascule entre différentes configurations d'agents.

#### `/chat`
Gère les sessions de chat : sauvegarder, charger et basculer entre sessions.

#### `/mcp`
Affiche quels serveurs MCP sont actuellement chargés.

#### `/billing`
Affiche les informations de facturation et de crédits.

**Note** : D'autres commandes comme `/help`, `/quit`, `/clear`, `/context` peuvent exister mais ne sont pas explicitement documentées dans la documentation officielle de Kiro.

---

## 📋 Specs - Spécifications

### Description
Les Specs sont des artefacts structurés qui formalisent le processus de développement pour les fonctionnalités complexes. Elles permettent de décomposer les exigences en user stories avec critères d'acceptation.

### Workflow en 3 phases

| Phase | Description | Contenu |
|-------|-------------|---------|
| **1. Requirements** | Définition des exigences | User stories avec notation EARS |
| **2. Design** | Architecture technique | Diagrammes de séquence, composants |
| **3. Implementation** | Suivi des tâches | Tâches discrètes et traçables |

### Structure des Specs

```
.kiro/specs/
├── feature-auth/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── feature-dashboard/
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

### Exemple de requirements.md

```markdown
# Feature: Authentification utilisateur

## User Stories

### US-001: Connexion par email
**En tant que** utilisateur
**Je veux** me connecter avec mon email
**Afin de** accéder à mon compte

#### Critères d'acceptation
- [ ] Le formulaire valide le format email
- [ ] Le mot de passe est masqué
- [ ] Message d'erreur clair en cas d'échec
```

### Fonctionnalités clés

| Fonctionnalité | Description |
|----------------|-------------|
| **Import JIRA/Confluence** | Importer des requirements existants via MCP |
| **Suivi automatique** | Les tâches passent à "In Progress" puis "Done" automatiquement |
| **Raffinement itératif** | Mise à jour des requirements, design et tâches au fil du projet |
| **Collaboration équipe** | Specs versionnées et partageables via Git |

---

## 🎯 Steering - Directives

### Description
Le Steering donne à Kiro une connaissance persistante de votre workspace via des fichiers markdown. Cela assure une génération de code cohérente et réduit les répétitions.

### Emplacement des fichiers

| Scope | Emplacement |
|-------|-------------|
| **Workspace** | `.kiro/steering/` |
| **Global** | `~/.kiro/steering/` |
| **Équipe** | Distribué via MDM ou dépôts Git |

### Fichiers fondamentaux

| Fichier | Description | Contenu |
|---------|-------------|---------|
| `product.md` | Vue d'ensemble produit | Objectifs, public cible, fonctionnalités clés |
| `tech.md` | Stack technologique | Frameworks, bibliothèques, contraintes |
| `structure.md` | Structure projet | Organisation des fichiers, conventions de nommage |

### Exemple de product.md

```markdown
---
inclusion: always
---

# Product Overview

## Description
Application de transcription vocale locale utilisant Whisper.

## Objectifs
- Transcription temps réel sans connexion internet
- Support multilingue
- Intégration système (raccourcis clavier)

## Public cible
- Développeurs
- Professionnels nécessitant de la dictée vocale
```

### Exemple de tech.md

```markdown
---
inclusion: always
---

# Technology Stack

## Backend
- Python 3.12+
- faster-whisper pour la transcription
- pynput pour les raccourcis clavier

## Contraintes
- Doit fonctionner offline
- Compatible Windows/Linux/macOS
- Utilisation GPU optionnelle (CUDA)
```

### Options d'inclusion

| Option | Description |
|--------|-------------|
| `inclusion: always` | Toujours inclus dans le contexte |
| `inclusion: auto` | Inclus automatiquement si pertinent |
| `inclusion: manual` | Inclus via commande slash uniquement |

### Créer un steering manuel (commande slash)

```markdown
---
inclusion: manual
---

# Code Review Guidelines

## Règles
- Vérifier la couverture de tests
- Respecter les principes SOLID
- Documenter les fonctions publiques
```

Ce fichier sera accessible via `/code-review`.

---

## ⚡ Hooks - Automatisations

### Description
Les hooks automatisent les workflows de développement en exécutant des actions lors d'événements IDE (sauvegarde, création, suppression de fichiers, prompts utilisateur).

### Types de déclencheurs

| Trigger | Description | Événement |
|---------|-------------|-----------|
| `file-saved` | Fichier sauvegardé | Après sauvegarde |
| `file-created` | Fichier créé | Après création |
| `file-deleted` | Fichier supprimé | Après suppression |
| `user-prompt` | Prompt utilisateur | Sur demande |
| `manual` | Manuel | Via commande slash |

### Structure d'un hook

```yaml
name: sync-docs
description: Synchronise le code source avec la documentation
trigger: file-saved
patterns:
  - "src/**/*.ts"
  - "src/**/*.py"
instructions: |
  Quand un fichier source est modifié, mettre à jour
  la documentation correspondante dans /docs
```

### Gestion des hooks

| Action | Méthode |
|--------|---------|
| **Activer/Désactiver** | Cliquer sur l'icône œil dans le panneau Agent Hooks |
| **Éditer** | Sélectionner le hook et modifier triggers/patterns/instructions |
| **Supprimer** | Sélectionner le hook et cliquer "Delete Hook" |
| **Exécuter manuellement** | Cliquer sur le bouton play à côté du nom |

### Exemples de hooks

#### Hook de synchronisation documentation

```yaml
name: sync-source-to-docs
trigger: manual
instructions: |
  Analyser les fichiers sources modifiés et mettre à jour
  la documentation API correspondante.
```

#### Hook de tests automatiques

```yaml
name: run-tests-on-save
trigger: file-saved
patterns:
  - "src/**/*.py"
  - "tests/**/*.py"
instructions: |
  Exécuter pytest sur les fichiers de tests correspondants
  au fichier modifié.
```

#### Hook de génération changelog

```yaml
name: generate-changelog
trigger: manual
instructions: |
  Analyser les commits récents et générer une entrée
  de changelog formatée selon Keep a Changelog.
```

---

## 🔌 MCP - Model Context Protocol

### Description
Le MCP permet d'étendre les capacités de Kiro en connectant des serveurs externes (AWS, bases de données, outils, etc.).

### Fichiers de configuration

| Priorité | Emplacement |
|----------|-------------|
| 1 (haute) | Configuration de l'agent |
| 2 | `.kiro/settings/mcp.json` (workspace) |
| 3 (basse) | `~/.kiro/settings/mcp.json` (global) |

### Structure de configuration

```json
{
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server"],
      "env": {
        "AWS_PROFILE": "default"
      },
      "timeout": 120000,
      "autoApprove": ["read", "list"],
      "disabledTools": ["delete"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "remote-api": {
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### Options de configuration

| Option | Type | Description |
|--------|------|-------------|
| `command` | string | Commande pour serveurs locaux (requis si local) |
| `url` | string | URL pour serveurs distants (requis si remote) |
| `args` | array | Arguments de la commande |
| `env` | object | Variables d'environnement |
| `timeout` | number | Timeout en ms (défaut: 120000) |
| `autoApprove` | array | Outils approuvés automatiquement |
| `disabledTools` | array | Outils désactivés |
| `headers` | object | Headers HTTP (serveurs distants) |

### Serveurs MCP populaires

| Serveur | Description | Commande |
|---------|-------------|----------|
| `@aws/mcp-server` | Services AWS (S3, Lambda, EC2, IAM) | `npx -y @aws/mcp-server` |
| `@modelcontextprotocol/server-filesystem` | Accès fichiers | `npx -y @modelcontextprotocol/server-filesystem` |
| `@modelcontextprotocol/server-github` | Intégration GitHub | `npx -y @modelcontextprotocol/server-github` |
| `@modelcontextprotocol/server-postgres` | Base PostgreSQL | `npx -y @modelcontextprotocol/server-postgres` |

---

## 🤖 Agents personnalisés

### Description
Les agents personnalisés permettent de configurer des outils et permissions spécialisés pour différents workflows.

### Structure de configuration d'agent

```json
{
  "name": "aws-specialist",
  "description": "Agent spécialisé pour l'infrastructure AWS",
  "prompt": "Tu es un expert AWS. Utilise les best practices AWS.",
  "mcpServers": ["aws"],
  "tools": ["read", "write", "aws", "shell"],
  "allowedTools": ["read", "aws"],
  "toolsSettings": {
    "aws": {
      "allowedServices": ["s3", "lambda", "cloudformation", "ec2", "iam", "logs"]
    }
  },
  "resources": [
    "file://./docs/aws-guidelines.md"
  ],
  "hooks": {
    "onSpawn": "aws sts get-caller-identity"
  }
}
```

### Champs de configuration

| Champ | Description |
|-------|-------------|
| `name` | Identifiant de l'agent |
| `description` | Description de ce que fait l'agent |
| `prompt` | Contexte/system prompt (texte ou `file://` URI) |
| `mcpServers` | Serveurs MCP accessibles |
| `tools` | Outils disponibles pour l'agent |
| `allowedTools` | Outils exécutables sans confirmation |
| `toolsSettings` | Configuration spécifique par outil |
| `resources` | Fichiers/documentation disponibles |
| `hooks` | Commandes déclenchées à des moments spécifiques |

### Exemple: Agent AWS Specialist

```json
{
  "name": "aws-specialist",
  "description": "Infrastructure AWS management",
  "prompt": "file://./agents/aws-prompt.md",
  "mcpServers": ["aws"],
  "allowedTools": ["read", "aws"],
  "toolsSettings": {
    "aws": {
      "allowedServices": ["s3", "lambda", "cloudformation", "ec2", "iam", "logs"]
    }
  },
  "hooks": {
    "onSpawn": "aws sts get-caller-identity"
  }
}
```

### Exemple: Agent Code Review

```json
{
  "name": "code-reviewer",
  "description": "Revue de code approfondie",
  "prompt": "Tu es un reviewer expert. Vérifie la qualité, sécurité et performance.",
  "tools": ["read", "grep", "glob"],
  "allowedTools": ["read"],
  "resources": [
    "file://./.kiro/steering/code-review.md"
  ]
}
```

### Sélectionner un agent

```bash
# En mode interactif
/agent aws-specialist

# Ou via le menu de sélection
/agent
```

---

## ⚙️ Configuration globale

### Arborescence de configuration

```
~/.kiro/
├── settings/
│   └── mcp.json          # Configuration MCP globale
└── steering/
    ├── product.md        # Steering global
    ├── tech.md
    └── structure.md

.kiro/                     # Dans le workspace
├── settings/
│   └── mcp.json          # Configuration MCP projet
├── steering/
│   ├── product.md
│   ├── tech.md
│   ├── structure.md
│   └── code-review.md    # Steering manuel
├── specs/
│   └── feature-xxx/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
├── hooks/
│   └── hooks.yaml
└── agents/
    └── aws-specialist.json
```

### Priorité de configuration

1. **Agent Config** (plus haute priorité)
2. **Workspace** (`.kiro/`)
3. **Global** (`~/.kiro/`)

---

## 📝 Exemples pratiques

### Exemple 1 : Configuration d'un projet Python

```bash
# 1. Créer la structure Kiro
mkdir -p .kiro/steering .kiro/specs .kiro/hooks

# 2. Créer le steering product.md
cat > .kiro/steering/product.md << 'EOF'
---
inclusion: always
---

# Product Overview

Application de transcription vocale locale.

## Objectifs
- Transcription temps réel offline
- Support multilingue
- Intégration raccourcis clavier
EOF

# 3. Créer le steering tech.md
cat > .kiro/steering/tech.md << 'EOF'
---
inclusion: always
---

# Technology Stack

- Python 3.12+
- faster-whisper
- pynput
- pytest pour les tests
EOF
```

### Exemple 2 : Configuration MCP pour AWS

```json
// .kiro/settings/mcp.json
{
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server"],
      "env": {
        "AWS_PROFILE": "dev",
        "AWS_REGION": "eu-west-1"
      },
      "autoApprove": ["read", "list", "describe"],
      "disabledTools": ["delete", "terminate"]
    }
  }
}
```

### Exemple 3 : Hook de tests automatiques

```yaml
# .kiro/hooks/hooks.yaml
hooks:
  - name: auto-test
    description: Exécute les tests après modification
    trigger: file-saved
    patterns:
      - "src/**/*.py"
    instructions: |
      Exécuter pytest sur le module correspondant.
      Reporter les erreurs de façon claire.

  - name: lint-on-save
    description: Lint automatique après sauvegarde
    trigger: file-saved
    patterns:
      - "**/*.py"
    instructions: |
      Exécuter ruff check sur le fichier modifié.
      Proposer les corrections automatiques.

  - name: run-tests
    description: Exécuter les tests manuellement
    trigger: manual
    instructions: |
      Exécuter pytest avec coverage et reporter les résultats.
```

Utilisation du hook manuel :
```bash
# En mode interactif Kiro
/run-tests
```

### Exemple 4 : Workflow complet de feature

```bash
# 1. Créer une spec pour la feature
mkdir -p .kiro/specs/feature-auth

# 2. Définir les requirements
cat > .kiro/specs/feature-auth/requirements.md << 'EOF'
# Feature: Authentification

## US-001: Login email/password
**En tant que** utilisateur
**Je veux** me connecter avec email/mot de passe
**Afin de** accéder à mon compte

### Critères d'acceptation
- [ ] Validation format email
- [ ] Mot de passe masqué
- [ ] Message d'erreur clair
- [ ] Rate limiting (5 tentatives)
EOF

# 3. Lancer Kiro et utiliser la spec
kiro-cli

# En mode interactif:
# /agent code-reviewer
# Analyse la spec et génère le design
```

### Exemple 5 : Agent personnalisé pour le projet

```json
// .kiro/agents/whisper-dev.json
{
  "name": "whisper-dev",
  "description": "Agent spécialisé développement Whisper",
  "prompt": "Tu es un expert en traitement audio et transcription. Tu connais faster-whisper, whisper.cpp et les optimisations GPU.",
  "tools": ["read", "write", "shell", "grep"],
  "allowedTools": ["read", "grep"],
  "resources": [
    "file://./README.md",
    "file://./GUIDE_INSTALLATION_FASTER_WHISPER.md"
  ],
  "hooks": {
    "onSpawn": "python --version && pip show faster-whisper"
  }
}
```

---

## 📚 Ressources supplémentaires

| Ressource | URL |
|-----------|-----|
| **Documentation officielle** | [kiro.dev/docs](https://kiro.dev/docs/) |
| **CLI Reference** | [kiro.dev/docs/cli](https://kiro.dev/docs/cli/) |
| **Slash Commands** | [kiro.dev/docs/cli/reference/slash-commands](https://kiro.dev/docs/cli/reference/slash-commands/) |
| **MCP Configuration** | [kiro.dev/docs/cli/mcp/configuration](https://kiro.dev/docs/cli/mcp/configuration/) |
| **Custom Agents** | [kiro.dev/docs/cli/custom-agents](https://kiro.dev/docs/cli/custom-agents/) |
| **Steering** | [kiro.dev/docs/steering](https://kiro.dev/docs/steering/) |
| **Specs** | [kiro.dev/docs/specs](https://kiro.dev/docs/specs/) |
| **Hooks** | [kiro.dev/docs/hooks](https://kiro.dev/docs/hooks/) |

---

## 🔄 Notes de version

**v1.0 (24-01-2026)**
- Création du guide initial
- Documentation installation et mise à jour
- Documentation Specs, Steering, Hooks
- Documentation MCP et Agents personnalisés
- Tableaux récapitulatifs
- Exemples pratiques

---

**Note** : Ce document est une référence pratique. Certaines commandes peuvent évoluer. Consultez la documentation officielle Kiro pour les informations à jour.

<<<END>>>
