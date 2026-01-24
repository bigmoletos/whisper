# Guide des Extensions CLI Gemini (Google)

**Auteur** : Bigmoletos  
**Version** : 1.0  
**Date** : 24-01-2026  
**Contexte** : Guide de référence pour utiliser Gemini CLI avec ses outils, extensions, MCP et configurations.

---

## 📋 Table des matières

1. [Tableau récapitulatif des commandes](#-tableau-récapitulatif-des-commandes)
2. [Installation et mise à jour](#-installation-et-mise-à-jour)
3. [Commandes slash](#-commandes-slash)
4. [Outils intégrés](#-outils-intégrés)
5. [Extensions](#-extensions)
6. [MCP - Model Context Protocol](#-mcp---model-context-protocol)
7. [Mémoire et persistance](#-mémoire-et-persistance)
8. [Sandbox - Isolation](#-sandbox---isolation)
9. [Configuration](#-configuration)
10. [Exemples pratiques](#-exemples-pratiques)

---

## 📊 Tableau récapitulatif des commandes

### Commandes CLI principales

| Commande | Description | Exemple |
|----------|-------------|---------|
| `gemini` | Lancer en mode interactif | `gemini` |
| `gemini "prompt"` | Exécuter un prompt | `gemini "Explique ce code"` |
| `gemini -s` ou `--sandbox` | Mode sandbox | `gemini -s` |
| `gemini extensions list` | Lister les extensions installées | `gemini extensions list` |
| `gemini extensions install <url>` | Installer une extension | `gemini extensions install https://github.com/user/ext` |
| `gemini extensions uninstall <name>` | Désinstaller une extension | `gemini extensions uninstall ext-name` |
| `gemini extensions enable <name>` | Activer une extension | `gemini extensions enable ext-name` |
| `gemini extensions disable <name>` | Désactiver une extension | `gemini extensions disable ext-name` |
| `gemini extensions update` | Mettre à jour les extensions | `gemini extensions update` |
| `gemini --help` | Afficher l'aide | `gemini --help` |
| `gemini --version` | Afficher la version | `gemini --version` |

### Commandes slash

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/help` | Afficher l'aide | `/help` |
| `/settings` | Ouvrir l'éditeur de paramètres | `/settings` |
| `/memory` | Gérer la mémoire instructionnelle (GEMINI.md) | `/memory` |
| `/mcp` | Lister les serveurs MCP configurés | `/mcp` |
| `/stats` | Afficher les statistiques de session | `/stats` |
| `/chat` | Gérer les conversations | `/chat save myconv` |

**Note** : Les commandes `/clear`, `/compress`, `/copy`, `/directory`, `/theme`, `/bug`, `/logout` ne sont pas des commandes slash officielles de Gemini CLI selon la documentation.

### Commandes de gestion des extensions

| Commande | Description | Exemple |
|----------|-------------|---------|
| `gemini extensions list` | Lister les extensions | `gemini extensions list` |
| `gemini extensions install` | Installer une extension | `gemini extensions install <url>` |
| `gemini extensions uninstall` | Désinstaller | `gemini extensions uninstall <name>` |
| `gemini extensions enable` | Activer | `gemini extensions enable <name>` |
| `gemini extensions disable` | Désactiver | `gemini extensions disable <name>` |
| `gemini extensions update` | Mettre à jour | `gemini extensions update` |

---

## 🚀 Installation et mise à jour

### Installation

| Méthode | Commande |
|---------|----------|
| **npm (recommandé)** | `npm install -g @google/gemini-cli` |
| **npm (latest)** | `npm install -g @google/gemini-cli@latest` |
| **npx (sans install)** | `npx @google/gemini-cli` |
| **Homebrew (macOS)** | `brew install gemini-cli` |

**Prérequis** : Node.js 20+

### Mise à jour

```bash
# Via npm
npm update -g @google/gemini-cli

# Ou réinstaller la dernière version
npm install -g @google/gemini-cli@latest
```

### Versions disponibles

| Version | Description | Fréquence |
|---------|-------------|-----------|
| **Latest** | Version stable | Stable |
| **Preview** | Avant-première | Mardi (UTC 23:59) |
| **Nightly** | Développement | Quotidien |

### Configuration initiale

```bash
# Lancer Gemini (authentification automatique)
gemini

# Ou avec une clé API
export GOOGLE_API_KEY="your-api-key"
gemini
```

---

## ⌨️ Commandes slash

### Commandes détaillées

#### `/help`
Affiche l'aide complète sur Gemini CLI, y compris les commandes disponibles et leur utilisation.

#### `/settings`
Ouvre l'éditeur de paramètres pour voir et modifier la configuration de Gemini CLI avec une interface conviviale.

#### `/memory`
Gère le contexte instructionnel de l'IA (mémoire hiérarchique chargée depuis les fichiers GEMINI.md).

#### `/mcp`
Liste les serveurs Model Context Protocol (MCP) configurés, leur statut de connexion et les outils disponibles.

#### `/stats`
Affiche les statistiques détaillées de la session actuelle, incluant l'utilisation des tokens et la durée de session.

#### `/chat` (Gestion des conversations)
Gère les sessions de conversation :
- Sauvegarder, charger et supprimer des conversations
- Exporter en Markdown ou JSON

**Note** : La documentation officielle ne mentionne pas les commandes `/clear`, `/compress`, `/copy`, `/directory`, `/dir`, `/tools`, `/theme`, `/bug`, ou `/logout` comme commandes slash standards.

---

## 🔧 Outils intégrés

### Description
Gemini CLI dispose d'outils intégrés que le modèle utilise automatiquement selon les besoins.

### Tableau des outils

| Outil | Description | Utilisation |
|-------|-------------|-------------|
| `read_file` | Lire des fichiers | Automatique |
| `write_file` | Écrire des fichiers | Avec confirmation |
| `edit_file` | Modifier des fichiers | Avec confirmation |
| `shell` | Exécuter des commandes | Avec confirmation |
| `web_fetch` | Récupérer du contenu web | Automatique |
| `google_search` | Recherche Google | Automatique |
| `save_memory` | Sauvegarder en mémoire | Automatique |

### Outil `save_memory`

Stocke des informations pour les sessions futures.

```
Usage : save_memory(fact="Votre fait ici.")
Stockage : ~/.gemini/GEMINI.md
Section : ## Gemini Added Memories
```

### Grounding avec Google Search

Gemini peut utiliser Google Search pour des informations en temps réel :

```
> Quelles sont les dernières actualités sur Python 3.13 ?
# Gemini utilise automatiquement google_search
```

---

## 🧩 Extensions

### Description
Les extensions enrichissent Gemini CLI avec des outils et commandes supplémentaires. Plus de 300 extensions sont disponibles.

### Gestion des extensions

```bash
# Lister les extensions installées
gemini extensions list

# Installer depuis GitHub
gemini extensions install https://github.com/user/extension

# Installer depuis un chemin local
gemini extensions install ./my-extension

# Désinstaller
gemini extensions uninstall extension-name

# Activer/Désactiver
gemini extensions enable extension-name
gemini extensions disable extension-name

# Mettre à jour toutes les extensions
gemini extensions update
```

### Extensions populaires

| Extension | Description | Source |
|-----------|-------------|--------|
| **Figma** | Intégration Figma | Officiel (Figma) |
| **Stripe** | API Stripe | Officiel (Stripe) |
| **Shopify** | Intégration Shopify | Officiel (Shopify) |
| **Snyk** | Sécurité code | Officiel (Snyk) |
| **Postman** | Tests API | Officiel (Postman) |
| **Elastic** | Elasticsearch | Officiel (Elastic) |
| **Dynatrace** | Monitoring | Officiel (Dynatrace) |
| **Harness** | CI/CD | Officiel (Harness) |

### Structure d'une extension

Une extension peut contenir :
- **Prompts** : Instructions système
- **MCP Servers** : Serveurs d'outils
- **Custom Commands** : Commandes slash personnalisées

### FastMCP Integration

Installer des serveurs MCP Python directement :

```bash
# Installer un serveur FastMCP
fastmcp install gemini-cli server.py
```

---

## 🔌 MCP - Model Context Protocol

### Description
Le MCP permet de connecter des serveurs externes pour étendre les capacités de Gemini.

### Configuration

Les serveurs MCP sont configurés dans `settings.json` :

```json
{
  "mcp": {
    "discoveryEnabled": true,
    "allowedServers": ["*"],
    "excludedServers": []
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Types de transport

| Transport | Description | Configuration |
|-----------|-------------|---------------|
| **Stdio** | Subprocess stdin/stdout | `command` + `args` |
| **SSE** | Server-Sent Events | `url` (https) |
| **Streamable HTTP** | HTTP streaming | `url` (https) |

### Configuration Stdio (local)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["./server.js"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      },
      "timeout": 120000
    }
  }
}
```

### Configuration SSE (distant)

```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://api.example.com/mcp/sse",
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
| `command` | string | Commande pour serveurs locaux |
| `args` | array | Arguments de la commande |
| `url` | string | URL pour serveurs distants |
| `env` | object | Variables d'environnement |
| `headers` | object | Headers HTTP (serveurs distants) |
| `timeout` | number | Timeout en ms (défaut: 120000) |
| `autoApprove` | array | Outils approuvés automatiquement |
| `disabledTools` | array | Outils désactivés |

---

## 🧠 Mémoire et persistance

### Fichier GEMINI.md

Gemini stocke les informations persistantes dans `~/.gemini/GEMINI.md`.

### Structure

```markdown
# GEMINI.md

## User Preferences
- Langue préférée : Français
- Style de code : Clean Code, SOLID

## Project Context
- Projet actuel : whisper_local_STT
- Stack : Python, faster-whisper

## Gemini Added Memories
- L'utilisateur préfère les réponses concises
- Le projet utilise Python 3.12
```

### Sauvegarder manuellement

```
> Souviens-toi que je préfère les réponses en français
# Gemini utilise save_memory automatiquement
```

### Conversations sauvegardées

```bash
# Sauvegarder
/chat save my-feature

# Reprendre plus tard
/chat resume my-feature

# Lister
/chat list

# Exporter
/chat share
```

---

## 🔒 Sandbox - Isolation

### Description
Le sandbox isole les opérations potentiellement dangereuses du système hôte.

### Activation

| Méthode | Commande/Configuration |
|---------|------------------------|
| **Flag CLI** | `gemini -s` ou `gemini --sandbox` |
| **Variable env** | `GEMINI_SANDBOX=true` |
| **settings.json** | `"sandbox": true` dans `tools` |

### Configuration sandbox

```json
{
  "tools": {
    "sandbox": true,
    "sandboxType": "docker"
  }
}
```

### Types de sandbox

| Type | Description | Configuration |
|------|-------------|---------------|
| `docker` | Container Docker | `GEMINI_SANDBOX=docker` |
| `podman` | Container Podman | `GEMINI_SANDBOX=podman` |
| `sandbox-exec` | macOS Seatbelt | `GEMINI_SANDBOX=sandbox-exec` |
| `true` | Auto-détection | `GEMINI_SANDBOX=true` |

### Profils Seatbelt (macOS)

| Profil | Description |
|--------|-------------|
| `permissive-open` | Défaut, réseau ouvert |
| `permissive-closed` | Réseau fermé |
| `permissive-proxied` | Réseau via proxy |
| `restrictive` | Restrictions maximales |

---

## ⚙️ Configuration

### Fichiers de configuration

| Fichier | Emplacement | Description |
|---------|-------------|-------------|
| `settings.json` | `~/.gemini/` | Configuration globale |
| `GEMINI.md` | `~/.gemini/` | Mémoire persistante |
| `mcp.json` | `~/.gemini/` | Configuration MCP |

### Structure settings.json

```json
{
  "ui": {
    "theme": "dark",
    "colors": true,
    "suggestions": true
  },
  "keybindings": {
    "clear": "ctrl+l",
    "copy": "ctrl+c",
    "paste": "ctrl+v"
  },
  "accessibility": {
    "screenReader": false,
    "reducedMotion": false
  },
  "tools": {
    "sandbox": false,
    "autoApprove": ["read_file", "web_fetch"],
    "blocked": []
  },
  "mcp": {
    "discoveryEnabled": true,
    "allowedServers": ["*"],
    "excludedServers": []
  },
  "mcpServers": {
    // Définitions des serveurs MCP
  },
  "model": {
    "default": "gemini-2.0-flash",
    "temperature": 0.7
  }
}
```

### Variables d'environnement

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Clé API Google |
| `GEMINI_SANDBOX` | Activer le sandbox |
| `GEMINI_MODEL` | Modèle par défaut |
| `GEMINI_THEME` | Thème (dark/light) |

---

## 📝 Exemples pratiques

### Exemple 1 : Session de développement

```bash
# Démarrer Gemini
gemini

# Analyser un projet
> Analyse la structure de ce projet Python

# Ajouter un répertoire
/dir add ./src

# Rechercher dans le code
> Trouve toutes les fonctions async dans le projet

# Sauvegarder la session
/chat save dev-session

# Reprendre plus tard
/chat resume dev-session
```

### Exemple 2 : Configuration MCP complète

```json
// ~/.gemini/settings.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "autoApprove": ["read_file", "list_directory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      },
      "disabledTools": ["delete", "drop"]
    }
  },
  "tools": {
    "sandbox": true,
    "autoApprove": ["read_file", "web_fetch", "google_search"]
  }
}
```

### Exemple 3 : Installation d'extensions

```bash
# Installer des extensions populaires
gemini extensions install https://github.com/anthropics/mcp-servers

# Lister les extensions
gemini extensions list

# Utiliser une extension
gemini
> Utilise l'extension Stripe pour vérifier les paiements récents
```

### Exemple 4 : Mode sandbox sécurisé

```bash
# Lancer en mode sandbox
gemini --sandbox

# Ou configurer via variable
export GEMINI_SANDBOX=docker
gemini

# Les opérations sont isolées dans un container
> Exécute ce script Python potentiellement dangereux
```

### Exemple 5 : Statistiques d'utilisation

```bash
# Voir les statistiques wrapped
npx gemini-wrapped

# Affiche :
# - Tokens utilisés
# - Modèles les plus utilisés
# - Langages principaux
# - Temps de session
```

### Exemple 6 : Mémoire personnalisée

```bash
gemini

# Ajouter des préférences
> Souviens-toi que je travaille sur un projet Python nommé whisper_local_STT

# Vérifier le fichier mémoire
# ~/.gemini/GEMINI.md contient maintenant cette information

# Les sessions futures utiliseront ce contexte
```

---

## 📚 Ressources supplémentaires

| Ressource | URL |
|-----------|-----|
| **Documentation officielle** | [google-gemini.github.io/gemini-cli](https://google-gemini.github.io/gemini-cli/) |
| **CLI Commands** | [geminicli.com/docs/cli/commands](https://geminicli.com/docs/cli/commands/) |
| **MCP Configuration** | [geminicli.com/docs/tools/mcp-server](https://geminicli.com/docs/tools/mcp-server) |
| **Extensions** | [geminicli.com/extensions](https://geminicli.com/extensions) |
| **GitHub** | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) |
| **Settings** | [geminicli.com/docs/cli/settings](https://geminicli.com/docs/cli/settings/) |

---

## 🔄 Notes de version

**v1.0 (24-01-2026)**
- Création du guide initial
- Documentation installation et configuration
- Documentation commandes slash
- Documentation MCP et Extensions
- Documentation Sandbox
- Tableaux récapitulatifs
- Exemples pratiques

**Fonctionnalités récentes (v0.23.0 - Janvier 2026)**
- Support expérimental Agent Skills
- Support clipboard images Windows
- Nouvelle commande `/logout`

---

**Note** : Ce document est une référence pratique. Certaines commandes peuvent évoluer. Consultez la documentation officielle Google pour les informations à jour.

<<<END>>>
