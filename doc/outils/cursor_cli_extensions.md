# Guide des Extensions CLI Cursor IDE

**Auteur** : Bigmoletos  
**Version** : 1.0  
**Date** : 24-01-2026  
**Contexte** : Guide de référence pour enrichir Cursor avec MCP, Rules, Commands, Subagents et configurations.

---

## 📋 Table des matières

1. [Tableau récapitulatif des commandes](#-tableau-récapitulatif-des-commandes)
2. [Modes de l'agent](#-modes-de-lagent)
3. [Commandes slash](#-commandes-slash)
4. [Rules - Règles](#-rules---règles)
5. [Commands - Commandes personnalisées](#-commands---commandes-personnalisées)
6. [Subagents - Sous-agents](#-subagents---sous-agents)
7. [MCP - Model Context Protocol](#-mcp---model-context-protocol)
8. [Skills - Compétences](#-skills---compétences)
9. [Configuration globale](#-configuration-globale)
10. [Exemples pratiques](#-exemples-pratiques)

---

## 📊 Tableau récapitulatif des commandes

### Commandes slash principales (Mode interactif)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/plan` ou `--mode=plan` | Basculer en mode Plan | `/plan` |
| `/ask` ou `--mode=ask` | Basculer en mode Ask (lecture seule) | `/ask` |
| `/agent` | Basculer en mode Agent (défaut) | `/agent` |
| `/debug` | Basculer en mode Debug | `/debug` |
| `/models` | Lister et changer de modèle (jan. 2026) | `/models` |
| `/rules` | Créer et éditer des règles (jan. 2026) | `/rules` |
| `/mcp list` | Menu interactif MCP (jan. 2026) | `/mcp list` |
| `/mcp enable <server>` | Activer un serveur MCP (jan. 2026) | `/mcp enable filesystem` |
| `/mcp disable <server>` | Désactiver un serveur MCP (jan. 2026) | `/mcp disable filesystem` |
| `/auto-run [state]` | Activer/désactiver l'auto-run | `/auto-run on` |
| `/clear` | Effacer la conversation | `/clear` |
| `/help` | Afficher l'aide | `/help` |

### Commandes personnalisées (Slash commands)

Les fichiers `.cursor/commands/*.md` deviennent automatiquement des commandes slash.

| Fichier | Commande générée | Exemple |
|---------|------------------|---------|
| `.cursor/commands/review.md` | `/review` | `/review` |
| `.cursor/commands/test.md` | `/test` | `/test` |

**Note** : Il n'y a pas de commandes CLI pour Cursor. Toute l'interaction se fait via l'IDE ou le mode interactif.

### Raccourcis clavier

| Raccourci | Description |
|-----------|-------------|
| `Cmd/Ctrl + K` | Ouvrir le menu Cmd K |
| `Cmd/Ctrl + L` | Ouvrir le chat |
| `Cmd/Ctrl + I` | Ouvrir Composer |
| `Cmd/Ctrl + Shift + P` | Palette de commandes |
| `Cmd/Ctrl + .` | Ouvrir les paramètres |

---

## 🎭 Modes de l'agent

### Description
Cursor propose plusieurs modes d'interaction avec l'IA, chacun optimisé pour un type de tâche spécifique.

### Tableau des modes

| Mode | Description | Cas d'utilisation |
|------|-------------|-------------------|
| **Agent** | Mode par défaut avec tous les outils | Implémentation, refactoring, debug |
| **Plan** | Mode lecture seule pour concevoir | Conception, architecture, planification |
| **Ask** | Mode lecture seule pour explorer | Questions, exploration de code |
| **Debug** | Mode spécialisé pour le débogage | Investigation de bugs, analyse d'erreurs |

### Mode Agent (défaut)

Le mode Agent est équipé de tous les outils pour les tâches complexes :
- Exploration autonome du codebase
- Éditions multi-fichiers
- Exécution de commandes shell
- Création/modification de fichiers

```
/agent
```

### Mode Plan

Mode collaboratif en lecture seule pour concevoir avant de coder :
- Analyse des approches possibles
- Identification des trade-offs
- Planification des étapes

```
/plan
```

### Mode Ask

Mode lecture seule pour explorer et poser des questions :
- Compréhension du code
- Recherche d'informations
- Analyse sans modification

```
/ask
```

### Mode Debug

Mode spécialisé pour le débogage systématique :
- Investigation des bugs
- Analyse des traces d'erreur
- Collecte de preuves runtime

```
/debug
```

---

## ⌨️ Commandes slash

### Commandes de mode

| Commande | Description |
|----------|-------------|
| `/plan` | Passe en mode Plan (conception) |
| `/ask` | Passe en mode Ask (exploration) |
| `/agent` | Passe en mode Agent (implémentation) |
| `/debug` | Passe en mode Debug (débogage) |

### Commandes de gestion

| Commande | Description |
|----------|-------------|
| `/models` | Liste et change le modèle IA (nouveau jan. 2026) |
| `/rules` | Crée et édite des règles (nouveau jan. 2026) |
| `/auto-run [on\|off]` | Active/désactive l'exécution automatique |
| `/clear` | Efface l'historique de conversation |
| `/help` | Affiche l'aide des commandes |

### Commandes personnalisées

Les commandes personnalisées sont définies dans `.cursor/commands/` et apparaissent comme commandes slash. Par exemple, si vous créez un fichier `.cursor/commands/review.md`, il sera accessible via `/review`.

---

## 📏 Rules - Règles

### Description
Les Rules (règles) personnalisent le comportement de l'IA. Elles peuvent être définies au niveau projet ou global.

### Types de règles

| Type | Emplacement | Scope |
|------|-------------|-------|
| **Projet** | `.cursor/rules/` | Ce projet uniquement |
| **Global** | Cursor Settings > General > Rules for AI | Tous les projets |
| **Legacy** | `.cursorrules` (racine projet) | Ce projet |

### Structure des règles projet

```
.cursor/
├── rules/
│   ├── general.mdc
│   ├── typescript.mdc
│   ├── testing.mdc
│   └── security.mdc
└── commands/
    └── ...
```

### Format d'un fichier règle (.mdc)

```markdown
---
description: "Règles pour les fichiers TypeScript"
globs: ["**/*.ts", "**/*.tsx"]
alwaysApply: false
---

# TypeScript Rules

## Conventions de code
- Utiliser des types stricts (no `any`)
- Préférer les interfaces aux types pour les objets
- Documenter les fonctions publiques avec JSDoc

## Patterns
- Utiliser async/await plutôt que les callbacks
- Gérer les erreurs avec try/catch
- Valider les entrées utilisateur

## Imports
- Grouper les imports par catégorie
- Éviter les imports circulaires
```

### Propriétés du frontmatter

| Propriété | Type | Description |
|-----------|------|-------------|
| `description` | string | Description sémantique de la règle |
| `globs` | array | Patterns de fichiers concernés |
| `alwaysApply` | boolean | Appliquer toujours, même sans match |

### Créer une nouvelle règle

Via la palette de commandes :
```
Cmd/Ctrl + Shift + P > "New Cursor Rule"
```

### Exemple de règle globale

Dans `Cursor Settings > General > Rules for AI` :

```
Toujours répondre en français.
Utiliser des commentaires clairs et concis.
Respecter les principes SOLID.
Ne jamais supprimer de code sans confirmation.
```

---

## 🛠️ Commands - Commandes personnalisées

### Description
Les Commands sont des prompts réutilisables qui apparaissent comme commandes slash.

### Emplacement

```
.cursor/commands/
├── review.md
├── test.md
├── document.md
└── refactor.md
```

### Format d'une commande

```markdown
---
description: "Revue de code complète"
---

Effectue une revue de code approfondie sur le fichier sélectionné.

Vérifie :
1. La qualité du code (lisibilité, maintenabilité)
2. Les potentiels bugs ou edge cases
3. La conformité aux best practices
4. La couverture de tests
5. La sécurité

Fournis un rapport structuré avec :
- Points positifs
- Points à améliorer
- Suggestions concrètes
```

### Utilisation

La commande apparaît comme `/review` dans le chat.

---

## 🤖 Subagents - Sous-agents

### Description
Les Subagents sont des assistants IA spécialisés auxquels l'agent principal peut déléguer des tâches.

### Avantages

| Avantage | Description |
|----------|-------------|
| **Isolation du contexte** | Chaque subagent a sa propre fenêtre de contexte |
| **Exécution parallèle** | Plusieurs subagents peuvent travailler simultanément |
| **Expertise spécialisée** | Configuration personnalisée par domaine |
| **Réutilisabilité** | Subagents utilisables dans tous les projets |

### Types de subagents intégrés

| Type | Description | Utilisation |
|------|-------------|-------------|
| `generalPurpose` | Agent polyvalent | Recherche, analyse, tâches complexes |
| `explore` | Exploration rapide | Recherche de fichiers, analyse de structure |
| `fast` | Agent rapide | Tâches simples, modifications ciblées |

### Configuration d'un subagent personnalisé

```json
{
  "name": "security-auditor",
  "description": "Agent spécialisé en audit de sécurité",
  "model": "claude-4",
  "prompt": "Tu es un expert en sécurité. Analyse le code pour identifier les vulnérabilités.",
  "tools": ["read", "grep", "glob"],
  "allowedTools": ["read"]
}
```

### Utilisation dans le code

L'agent principal délègue automatiquement aux subagents quand nécessaire, ou vous pouvez demander explicitement :

```
Utilise un subagent pour explorer la structure du projet et identifier tous les endpoints API.
```

---

## 🔌 MCP - Model Context Protocol

### Description
Le MCP permet d'étendre les capacités de Cursor en connectant des serveurs externes.

### Configuration

La configuration MCP est partagée entre le CLI et l'éditeur.

### Emplacement

```
~/.cursor/mcp.json          # Global
.cursor/mcp.json            # Projet
```

### Structure de configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "browser": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Serveurs MCP populaires

| Serveur | Description | Package |
|---------|-------------|---------|
| `filesystem` | Accès fichiers | `@modelcontextprotocol/server-filesystem` |
| `github` | Intégration GitHub | `@modelcontextprotocol/server-github` |
| `puppeteer` | Contrôle navigateur | `@anthropic/mcp-server-puppeteer` |
| `postgres` | Base PostgreSQL | `@modelcontextprotocol/server-postgres` |
| `sqlite` | Base SQLite | `@modelcontextprotocol/server-sqlite` |
| `brave-search` | Recherche web | `@anthropic/mcp-server-brave-search` |
| `memory` | Mémoire persistante | `@modelcontextprotocol/server-memory` |

### Commandes de gestion (Mode interactif)

```bash
# Menu interactif MCP (mise à jour janvier 2026)
/mcp list

# Activer un serveur MCP
/mcp enable filesystem

# Désactiver un serveur MCP
/mcp disable filesystem
```

**Note** : La configuration des serveurs MCP se fait via les fichiers `.cursor/mcp.json` ou `~/.cursor/mcp.json`. Il n'y a pas de commandes CLI `agent mcp` pour Cursor.

---

## 🎯 Skills - Compétences

### Description
Les Skills sont des modules de compétences qui enrichissent l'agent avec des connaissances spécialisées.

### Emplacement

```
~/.cursor/skills/           # Global
.cursor/skills/             # Projet
```

### Structure d'une Skill

```
.cursor/skills/
├── angular/
│   └── SKILL.md
├── react/
│   └── SKILL.md
└── python/
    └── SKILL.md
```

### Format SKILL.md

```markdown
# Skill: Angular Development

## Description
Compétences pour le développement Angular moderne.

## Quand utiliser
- Lors de la création de composants Angular
- Pour les fichiers .ts, .html, .scss dans un projet Angular
- Quand l'utilisateur mentionne Angular

## Règles
- Utiliser les standalone components
- Préférer les signals aux observables simples
- Suivre le guide de style Angular officiel
- Utiliser le nouveau control flow (@if, @for)

## Patterns recommandés
- Injection de dépendances via inject()
- Typed reactive forms
- Lazy loading des modules

## Commandes utiles
- `ng generate component` pour créer des composants
- `ng build --configuration production` pour le build
```

---

## ⚙️ Configuration globale

### Arborescence de configuration

```
~/.cursor/
├── mcp.json                # Configuration MCP globale
├── settings.json           # Paramètres globaux
└── skills/
    └── ...

.cursor/                    # Dans le workspace
├── mcp.json               # Configuration MCP projet
├── rules/
│   ├── general.mdc
│   ├── typescript.mdc
│   └── security.mdc
├── commands/
│   ├── review.md
│   └── test.md
└── skills/
    └── ...
```

### Fichier settings.json

Accès via `Cursor Settings > General` ou fichier JSON :

```json
{
  "general": {
    "rulesForAI": "Toujours répondre en français...",
    "autoRun": true,
    "autoFixErrors": true
  },
  "models": {
    "default": "claude-4-sonnet",
    "agent": "claude-4-opus"
  },
  "keybindings": {
    "openChat": "ctrl+l",
    "openComposer": "ctrl+i"
  }
}
```

### Variables de template

| Variable | Description |
|----------|-------------|
| `{{serverInstructions}}` | Instructions des serveurs MCP |
| `{{agentSkills}}` | Manifestes des skills |
| `{{file:path}}` | Contenu d'un fichier |
| `{{url:...}}` | Contenu d'une URL |
| `{{currentDate}}` | Date actuelle |
| `{{env}}` | Variables d'environnement |
| `{{workspaceRoot}}` | Racine du workspace |

---

## 📝 Exemples pratiques

### Exemple 1 : Configuration complète d'un projet

```bash
# 1. Créer la structure Cursor
mkdir -p .cursor/rules .cursor/commands .cursor/skills

# 2. Créer une règle générale
cat > .cursor/rules/general.mdc << 'EOF'
---
description: "Règles générales du projet"
alwaysApply: true
---

# Règles générales

- Répondre en français
- Code propre et commenté
- Tests obligatoires
- Pas de console.log en production
EOF

# 3. Créer une commande de revue
cat > .cursor/commands/review.md << 'EOF'
---
description: "Revue de code"
---

Effectue une revue de code complète.
Vérifie qualité, sécurité, tests.
EOF
```

### Exemple 2 : Configuration MCP multi-services

```json
// .cursor/mcp.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

Puis en mode interactif :
```bash
# Activer les serveurs MCP
/mcp enable filesystem
/mcp enable github
/mcp enable brave-search

# Vérifier le statut
/mcp list
```

### Exemple 3 : Règles par type de fichier

```markdown
<!-- .cursor/rules/typescript.mdc -->
---
description: "Règles TypeScript"
globs: ["**/*.ts", "**/*.tsx"]
---

# TypeScript Rules

- Types stricts obligatoires
- No `any`
- Interfaces pour les objets
- JSDoc pour les fonctions publiques
```

```markdown
<!-- .cursor/rules/python.mdc -->
---
description: "Règles Python"
globs: ["**/*.py"]
---

# Python Rules

- PEP 8 obligatoire
- Type hints
- Docstrings Google style
- Logging structuré
```

### Exemple 4 : Skill personnalisée

```markdown
<!-- .cursor/skills/whisper/SKILL.md -->
# Skill: Whisper Development

## Description
Compétences pour le développement avec faster-whisper.

## Contexte
- Projet de transcription vocale locale
- Python 3.12+
- GPU optionnel (CUDA)

## Patterns
- Utiliser faster-whisper pour la transcription
- Gérer les modèles (tiny, base, small, medium, large)
- Optimiser pour la latence temps réel
```

---

## 📚 Ressources supplémentaires

| Ressource | URL |
|-----------|-----|
| **Documentation officielle** | [cursor.com/docs](https://cursor.com/docs) |
| **Rules** | [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules) |
| **MCP** | [cursor.com/docs/context/mcp](https://cursor.com/docs/context/mcp) |
| **Subagents** | [cursor.com/docs/context/subagents](https://cursor.com/docs/context/subagents) |
| **Slash Commands** | [cursor.com/docs/cli/reference/slash-commands](https://cursor.com/docs/cli/reference/slash-commands) |
| **Modes** | [cursor.com/docs/agent/modes](https://cursor.com/docs/agent/modes) |

---

## 🔄 Notes de version

**v1.0 (24-01-2026)**
- Création du guide initial
- Documentation Modes, Rules, Commands
- Documentation MCP et Subagents
- Documentation Skills
- Tableaux récapitulatifs
- Exemples pratiques

---

**Note** : Ce document est une référence pratique. Certaines commandes peuvent évoluer. Consultez la documentation officielle Cursor pour les informations à jour.

<<<END>>>
