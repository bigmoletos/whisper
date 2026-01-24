# Guide des Extensions CLI Claude Code

**Auteur** : Bigmoletos  
**Version** : 1.0  
**Date** : 24-01-2026  
**Contexte** : Guide de référence pour enrichir Claude Code avec MCP, Skills, Tasks, Agents et Plugins.

---

## 📋 Table des matières

1. [Tableau récapitulatif des commandes](#-tableau-récapitulatif-des-commandes)
2. [MCP - Model Context Protocol](#-mcp---model-context-protocol)
3. [Skills - Compétences](#-skills---compétences)
4. [Tasks - Tâches](#-tasks---tâches)
5. [Agents - Sous-agents](#-agents---sous-agents)
6. [Plugins - Extensions](#-plugins---extensions)
7. [Configuration globale](#-configuration-globale)
8. [Exemples pratiques](#-exemples-pratiques)

---

## 📊 Tableau récapitulatif des commandes

### Commandes slash principales (Mode interactif)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/help` | Afficher l'aide | `/help` |
| `/mcp` | Menu MCP interactif | `/mcp` |
| `/plugin` | Menu plugins interactif | `/plugin` |
| `/agents` | Menu agents interactif | `/agents` |
| `/tasks` | Gérer les tâches d'arrière-plan | `/tasks` |
| `/todos` | Afficher les TODO items | `/todos` |
| `/plan` | Entrer en mode Plan | `/plan` |
| `/model` | Sélectionner le modèle | `/model` |
| `/context` | Visualiser l'utilisation du contexte | `/context` |
| `/clear` | Effacer la conversation | `/clear` |
| `/resume [session]` | Reprendre une session | `/resume` |
| `/init` | Initialiser CLAUDE.md | `/init` |

### Commandes MCP (CLI)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `claude mcp list` | Lister les serveurs MCP configurés | `claude mcp list` |
| `claude mcp add <name> -- <command>` | Ajouter un serveur MCP local | `claude mcp add myserver -- npx server` |
| `claude mcp add --transport http <name> <url>` | Ajouter un serveur MCP distant HTTP | `claude mcp add --transport http api https://api.example.com` |
| `claude mcp remove <server>` | Supprimer un serveur MCP | `claude mcp remove filesystem` |
| `claude mcp get <server>` | Détails d'un serveur MCP | `claude mcp get filesystem` |
| `claude mcp add-from-claude-desktop` | Importer depuis Claude Desktop | `claude mcp add-from-claude-desktop` |
| `claude mcp reset-project-choices` | Réinitialiser les choix d'approbation | `claude mcp reset-project-choices` |

### Commandes Plugins et Skills (CLI)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `claude plugin install <plugin>` | Installer un plugin | `claude plugin install anthropics/skills` |
| `claude plugin uninstall <plugin>` | Désinstaller un plugin | `claude plugin uninstall anthropics/skills` |
| `claude plugin list` | Lister les plugins installés | `claude plugin list` |
| `claude plugin update <plugin>` | Mettre à jour un plugin | `claude plugin update anthropics/skills` |
| `claude plugin enable <plugin>` | Activer un plugin désactivé | `claude plugin enable anthropics/skills` |
| `claude plugin disable <plugin>` | Désactiver un plugin | `claude plugin disable anthropics/skills` |

### Invocation des Skills (Mode interactif)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/skill-name` | Invoquer une skill par son nom | `/explain-code` |
| `/plugin` | Menu interactif plugins | `/plugin` |

**Note** : Il n'existe pas de commandes `/skills list` ou `/skills add`. Les skills s'invoquent directement par leur nom après installation du plugin.

### Commandes Tasks (Tâches d'arrière-plan)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/tasks` | Lister et gérer les tâches d'arrière-plan | `/tasks` |
| `/todos` | Lister les TODO items du projet | `/todos` |

**Note** : Il n'existe pas de commandes `/task create` ou `/task list` (singulier). Utilisez `/tasks` (pluriel) pour gérer les background tasks, et `/todos` pour les TODO items

### Commandes Agents (Sous-agents)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/agents` | Menu interactif pour gérer les sous-agents | `/agents` |
| `claude --agent <name>` | Démarrer une session avec un agent spécifique (CLI) | `claude --agent security-auditor` |

**Note** : Il n'existe pas de commandes `/agents list`, `/agents create`, etc. Utilisez `/agents` pour ouvrir le menu interactif où vous pouvez créer, éditer, supprimer et sélectionner des agents

### Commandes Plugins

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/plugin` | Menu interactif pour gérer les plugins | `/plugin` |
| `claude plugin install <plugin>` | Installer un plugin (CLI) | `claude plugin install anthropics/skills` |
| `claude plugin uninstall <plugin>` | Désinstaller un plugin (CLI) | `claude plugin uninstall anthropics/skills` |
| `claude plugin list` | Lister les plugins installés (CLI) | `claude plugin list` |
| `claude plugin update <plugin>` | Mettre à jour un plugin (CLI) | `claude plugin update anthropics/skills` |
| `claude plugin enable <plugin>` | Activer un plugin désactivé (CLI) | `claude plugin enable anthropics/skills` |
| `claude plugin disable <plugin>` | Désactiver un plugin (CLI) | `claude plugin disable anthropics/skills` |

**Note** : Il n'existe pas de commandes `/plugin marketplace add` ou `/plugin list` en mode interactif. Utilisez `/plugin` pour le menu interactif, ou `claude plugin install` en ligne de commande

### Commandes de gestion et maintenance (CLI)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `claude` | Démarrer en mode interactif | `claude` |
| `claude "prompt"` | Démarrer avec un prompt initial | `claude "Analyse ce projet"` |
| `claude -c` | Continuer la dernière conversation | `claude -c` |
| `claude --resume <session>` | Reprendre une session par ID/nom | `claude --resume auth-refactor` |
| `claude --agent <name>` | Démarrer avec un agent spécifique | `claude --agent security-auditor` |
| `claude --model <model>` | Spécifier le modèle | `claude --model opus` |
| `claude update` | Mettre à jour Claude CLI | `claude update` |
| `claude --version` | Afficher la version actuelle | `claude --version` |
| `claude doctor` | Diagnostiquer l'installation | `claude doctor` |
| `claude --init` | Initialiser le projet | `claude --init` |

---

## 🔌 MCP - Model Context Protocol

### Description
Le MCP (Model Context Protocol) permet d'étendre les capacités de Claude en connectant des serveurs externes qui fournissent des outils supplémentaires (accès fichiers, navigateur, bases de données, APIs, etc.).

### Serveurs MCP populaires

| Serveur | Description | Installation |
|---------|-------------|--------------|
| `filesystem` | Accès aux fichiers locaux | `claude mcp add filesystem -s user` |
| `browser` | Contrôle du navigateur web | `claude mcp add puppeteer -s user` |
| `github` | Intégration GitHub | `claude mcp add github -s user` |
| `postgres` | Connexion PostgreSQL | `claude mcp add postgres -s project` |
| `sqlite` | Connexion SQLite | `claude mcp add sqlite -s project` |
| `brave-search` | Recherche web Brave | `claude mcp add brave-search -s user` |
| `memory` | Mémoire persistante | `claude mcp add memory -s user` |

### Configuration MCP

La configuration MCP se trouve dans :
- **Global** : `~/.claude/settings/mcp_servers.json`
- **Projet** : `./.claude/settings/mcp_servers.json`

**Exemple de configuration (stdio - serveur local) :**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Exemple de configuration (HTTP - serveur distant) :**

```json
{
  "mcpServers": {
    "remote-api": {
      "transport": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### Commandes détaillées

#### `/mcp` (Mode interactif)
Ouvre un menu interactif pour gérer les serveurs MCP : connexion, OAuth, configuration.

```bash
# En mode interactif Claude Code
/mcp
```

#### `claude mcp add` (CLI)
Ajoute un serveur MCP. Les options doivent venir AVANT le nom du serveur.

```bash
# Serveur local (stdio)
claude mcp add myserver -- npx @modelcontextprotocol/server-filesystem /path/to/dir

# Serveur distant (HTTP)
claude mcp add --transport http api https://api.example.com

# Avec variables d'environnement
claude mcp add --env KEY=value myserver -- npx server

# Importer depuis Claude Desktop
claude mcp add-from-claude-desktop
```

#### `claude mcp list` (CLI)
Affiche tous les serveurs MCP configurés.

#### `claude mcp get <server>` (CLI)
Affiche les détails d'un serveur MCP spécifique.

---

## 🎯 Skills - Compétences

### Description
Les Skills sont des modules de compétences qui enrichissent Claude avec des connaissances spécialisées (Angular, React, Python best practices, etc.).

### Installation des Skills officielles

```bash
# En ligne de commande
claude plugin install anthropics/skills

# En mode interactif
/plugin
# Puis sélectionner le plugin dans le marketplace
```

### Structure d'une Skill

Les skills sont définies dans des fichiers `SKILL.md` :

```
.cursor/skills/
├── angular/
│   └── SKILL.md
├── react/
│   └── SKILL.md
└── python/
    └── SKILL.md
```

### Exemple de SKILL.md

```markdown
# Skill: Angular Development

## Description
Compétences pour le développement Angular moderne.

## Règles
- Utiliser les standalone components
- Préférer les signals aux observables simples
- Suivre le guide de style Angular officiel

## Commandes
- `ng generate component` pour créer des composants
- `ng build --configuration production` pour le build
```

### Commandes détaillées

#### Invoquer une skill
Les skills sont invoquées directement par leur nom précédé de `/`.

```bash
# Exemple : invoquer une skill nommée "explain-code"
/explain-code

# Exemple : invoquer une skill nommée "security-review"
/security-review

# Lister toutes les commandes et skills disponibles
/help
```

#### Installer des skills via plugins
```bash
# Installer le plugin skills officiel
claude plugin install anthropics/skills

# Ou en mode interactif
/plugin
```

**Note** : Il n'y a pas de commandes `/skills list` ou `/skills add`. Tapez `/` puis [TAB] pour voir toutes les skills disponibles.

---

## 📋 Tasks - Tâches

### Description
Les Tasks permettent de définir et gérer des tâches complexes de manière structurée. Claude peut créer des sous-tâches et suivre leur progression.

### Commandes détaillées

#### `/tasks` - Gérer les tâches d'arrière-plan
Affiche et gère les tâches en arrière-plan (agents, shells, sessions distantes).

```bash
# En mode interactif
/tasks

# Affiche les tâches avec leur statut:
# - running (en cours)
# - completed (terminée)
# - failed (échouée)
```

#### `/todos` - Liste des TODO items
Affiche les TODO items du projet actuel.

```bash
# En mode interactif
/todos
```

**Note** : Il n'existe pas de commandes `/task create` ou `/task list` (singulier). Claude Code gère automatiquement les tâches d'arrière-plan via l'outil TodoWrite.

---

## 🤖 Agents - Sous-agents

### Description
Les Agents sont des instances secondaires de Claude qui peuvent travailler en parallèle sur des tâches spécifiques (tests, revue de code, documentation, etc.).

### Types d'agents

| Type | Description | Utilisation |
|------|-------------|-------------|
| `generalPurpose` | Agent polyvalent | Recherche, analyse, tâches complexes |
| `explore` | Exploration de codebase | Recherche de fichiers, analyse de structure |
| `fast` | Agent rapide | Tâches simples, modifications ciblées |

### Commandes détaillées

#### `/agents` - Menu interactif des sous-agents
Ouvre un menu interactif pour gérer les sous-agents.

```bash
# En mode interactif Claude Code
/agents

# Actions disponibles dans le menu:
# - Voir tous les agents disponibles (built-in, user, project, plugin)
# - Créer un nouvel agent (avec setup guidé ou génération par Claude)
# - Éditer la configuration d'un agent existant
# - Supprimer un agent personnalisé
# - Voir quels agents sont actifs
```

#### Utiliser un agent en CLI
```bash
# Démarrer une session avec un agent spécifique
claude --agent security-auditor

# Définir des sous-agents pour la session
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"..."}}'
```

**Note** : Il n'existe pas de commandes `/agents list`, `/agents create`, etc. en mode slash. Tout se fait via le menu interactif `/agents`.

---

## 🧩 Plugins - Extensions

### Description
Les Plugins étendent les fonctionnalités de Claude Code avec des outils communautaires ou officiels.

### Marketplace

Le marketplace contient des plugins officiels et communautaires :

```bash
# En mode interactif - ouvrir le marketplace
/plugin

# En CLI - installer un plugin
claude plugin install anthropics/skills

# En CLI - lister les plugins
claude plugin list
```

### Plugins populaires

| Plugin | Description | Commande d'installation |
|--------|-------------|-------------------------|
| `anthropics/skills` | Skills officielles Anthropic | `claude plugin install anthropics/skills` |
| `anthropics/mcp-servers` | Serveurs MCP officiels | `claude plugin install anthropics/mcp-servers` |
| `community/git-enhanced` | Outils Git avancés | `claude plugin install community/git-enhanced` |
| `community/docker-tools` | Intégration Docker | `claude plugin install community/docker-tools` |

### Gestion des plugins

```bash
# En mode interactif - menu des plugins
/plugin

# En CLI - Lister les plugins installés
claude plugin list

# En CLI - Mettre à jour un plugin
claude plugin update anthropics/skills

# En CLI - Supprimer un plugin
claude plugin uninstall anthropics/skills

# En CLI - Désactiver un plugin (sans le supprimer)
claude plugin disable anthropics/skills

# En CLI - Réactiver un plugin
claude plugin enable anthropics/skills
```

---

## ⚙️ Configuration globale

### Fichiers de configuration

| Fichier | Emplacement | Description |
|---------|-------------|-------------|
| `CLAUDE.md` | Racine du projet | Instructions projet |
| `mcp_servers.json` | `~/.claude/` ou `./.claude/` | Configuration MCP |
| `settings.json` | `~/.claude/` | Paramètres globaux |
| `SKILL.md` | `.cursor/skills/<nom>/` | Définition des skills |

### Exemple de settings.json

```json
{
  "model": "opus",
  "autoCompact": true,
  "verboseMode": false,
  "theme": "dark",
  "plugins": [
    "anthropics/skills",
    "community/git-enhanced"
  ],
  "mcp": {
    "autoConnect": ["filesystem", "github"]
  }
}
```

---

## 📝 Exemples pratiques

### Exemple 1 : Configuration complète d'un projet Angular

```bash
# 1. Initialiser le projet
/init

# 2. Installer les skills Angular (depuis la CLI)
claude plugin install anthropics/skills

# 3. Configurer MCP pour le navigateur (tests)
claude mcp add puppeteer -- npx @anthropic/mcp-server-puppeteer

# 4. En mode interactif, créer un agent de tests
/agents
# Puis suivre le menu pour créer un agent "test-runner"
```

### Exemple 2 : Workflow de revue de code

```bash
# 1. Ajouter les outils GitHub (CLI)
claude mcp add github -- npx @modelcontextprotocol/server-github

# 2. En mode interactif, récupérer les commentaires PR
/pr-comments 123

# 3. Les tâches sont gérées automatiquement par Claude
# Pas besoin de /task create

# 4. Lancer la revue
/review src/
```

### Exemple 3 : Recherche et exploration de codebase

```bash
# 1. Ajouter le MCP filesystem (CLI)
claude mcp add filesystem -- npx @modelcontextprotocol/server-filesystem /chemin/vers/projet

# 2. Utiliser l'agent d'exploration intégré (en mode interactif)
# Claude utilise automatiquement le sous-agent "Explore" pour l'exploration

# 3. Demander l'analyse
> Analyse la structure du projet et identifie les patterns
```

### Exemple 4 : Automatisation avec scripts

```bash
# Script bash pour CI/CD
claude --dangerously-skip-permissions \
  --print "Analyser les changements et générer un changelog" \
  --output-format json \
  --max-turns 5 \
  | jq '.changelog'
```

---

## 🔄 Mise à jour de Claude CLI

### Commande de mise à jour

```bash
claude update
```

### Vérifier la version

```bash
claude --version
```

### Diagnostiquer les problèmes

```bash
claude doctor
```

**Note** : La commande `claude update` nécessite une connexion API active. En cas d'erreur de quota, attendez la réinitialisation ou augmentez votre limite sur [console.anthropic.com](https://console.anthropic.com/).

---

## 📚 Ressources supplémentaires

- **Documentation officielle MCP** : [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **Serveurs MCP officiels** : [github.com/anthropics/mcp-servers](https://github.com/anthropics/mcp-servers)
- **Documentation Claude Code** : [docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code)

---

## 🔄 Notes de version

**v1.0 (24-01-2026)**
- Création du guide initial
- Documentation MCP, Skills, Tasks, Agents, Plugins
- Tableaux récapitulatifs
- Exemples pratiques

---

**Note** : Ce document est une référence pratique. Certaines commandes peuvent évoluer. Consultez la documentation officielle pour les informations à jour.

<<<END>>>
