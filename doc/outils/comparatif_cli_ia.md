# Comparatif des CLI d'IA pour développeurs

**Auteur** : Bigmoletos
**Version** : 1.0
**Date** : 24-01-2026
**Contexte** : Tableau comparatif des principales CLI d'IA (Claude Code, Cursor, Gemini, Kiro, Vibe).

---

## 📊 Comparaison rapide

| Fonctionnalité | Claude Code | Cursor IDE | Gemini CLI | Kiro CLI | Vibe CLI |
|----------------|-------------|------------|------------|----------|----------|
| **Éditeur** | Anthropic | Cursor | Google | AWS | Mistral |
| **Open Source** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **CLI standalone** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **IDE intégré** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **MCP Support** | ✅ Natif | ✅ Natif | ✅ Natif | ✅ Natif | ❌ |
| **Plugins/Extensions** | ✅ Marketplace | ❌ | ✅ 300+ extensions | ❌ | ❌ |
| **Skills** | ✅ Via plugins | ✅ SKILL.md | ❌ | ❌ | ❌ |
| **Agents personnalisés** | ✅ Subagents | ✅ Subagents | ❌ | ✅ Custom agents | ✅ Config agents |
| **Hooks/Automations** | ✅ Via config | ❌ | ❌ | ✅ Natif | ❌ |
| **Modes (Plan/Ask)** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Sandbox** | ✅ Via settings | ❌ | ✅ Docker/Podman | ❌ | ❌ |
| **Mémoire persistante** | ✅ CLAUDE.md | ❌ | ✅ GEMINI.md | ✅ Steering | ❌ |
| **Installation** | npm/script | Téléchargement | npm/uv | Script/deb | pip/uv/pipx |

---

## 🔌 Commandes MCP

### Claude Code

```bash
# CLI
claude mcp list
claude mcp add myserver -- npx server
claude mcp remove myserver

# Interactif
/mcp
```

### Cursor IDE

```bash
# Configuration via fichiers JSON uniquement
# ~/.cursor/mcp.json ou .cursor/mcp.json

# Interactif (nouveau jan. 2026)
/mcp list
/mcp enable filesystem
/mcp disable filesystem
```

### Gemini CLI

```bash
# Configuration via settings.json

# Interactif
/mcp
```

### Kiro CLI

```bash
# Configuration via .kiro/settings/mcp.json

# Interactif
/mcp
```

### Vibe CLI

```bash
# Pas de support MCP natif
```

---

## 🧩 Gestion des plugins/extensions

### Claude Code

```bash
# CLI
claude plugin install anthropics/skills
claude plugin list
claude plugin uninstall anthropics/skills

# Interactif
/plugin
```

### Cursor IDE

```bash
# Pas de système de plugins
# Skills via .cursor/skills/*/SKILL.md
```

### Gemini CLI

```bash
# CLI
gemini extensions install https://github.com/user/ext
gemini extensions list
gemini extensions uninstall ext-name

# 300+ extensions disponibles (Figma, Stripe, Shopify, Snyk, etc.)
```

### Kiro CLI

```bash
# Pas de système de plugins
# Configuration via steering et hooks
```

### Vibe CLI

```bash
# Pas de système de plugins
# Configuration via agents TOML
```

---

## 🤖 Agents et sous-agents

### Claude Code

```bash
# CLI
claude --agent security-auditor

# Interactif
/agents

# Agents intégrés: Explore, Plan, General-purpose, etc.
```

### Cursor IDE

```bash
# Subagents configurés dans .cursor/
# Types: generalPurpose, explore, fast
```

### Gemini CLI

```bash
# Pas de système d'agents personnalisés
# Un seul agent configurable
```

### Kiro CLI

```bash
# Interactif
/agent

# Agents personnalisés dans .kiro/agents/*.json
```

### Vibe CLI

```bash
# CLI
vibe --agent security

# Agents dans .vibe/agents/*.toml
```

---

## 📝 Commandes slash principales

### Claude Code

| Commande | Description |
|----------|-------------|
| `/help` | Aide |
| `/mcp` | Menu MCP |
| `/plugin` | Menu plugins |
| `/agents` | Menu agents |
| `/tasks` | Tâches d'arrière-plan |
| `/plan` | Mode Plan |
| `/model` | Sélection modèle |
| `/init` | Initialiser CLAUDE.md |

### Cursor IDE

| Commande | Description |
|----------|-------------|
| `/plan` | Mode Plan |
| `/ask` | Mode Ask |
| `/agent` | Mode Agent |
| `/models` | Lister/changer modèle |
| `/rules` | Gérer les règles |
| `/mcp list` | Menu MCP |

### Gemini CLI

| Commande | Description |
|----------|-------------|
| `/help` | Aide |
| `/settings` | Paramètres |
| `/memory` | Gestion GEMINI.md |
| `/mcp` | Serveurs MCP |
| `/stats` | Statistiques |

### Kiro CLI

| Commande | Description |
|----------|-------------|
| `/model` | Changer de modèle |
| `/agent` | Gérer agents |
| `/chat` | Sessions de chat |
| `/mcp` | Serveurs MCP |
| `/billing` | Facturation |

### Vibe CLI

| Commande | Description |
|----------|-------------|
| `/config` | Configuration |
| `/theme` | Changer thème |

**Note** : Vibe est très minimaliste, utilise `@` (fichiers) et `!` (shell)

---

## 🎯 Cas d'usage recommandés

### Claude Code
- **Meilleur pour** : Développement général, intégration plugins, workflows complexes
- **Forces** : Marketplace plugins, subagents, MCP natif, modes Plan/Ask
- **Faiblesses** : Propriétaire, nécessite compte Anthropic

### Cursor IDE
- **Meilleur pour** : Développement dans un IDE complet, editing en contexte
- **Forces** : IDE intégré, modes multiples, MCP natif, rules par fichier
- **Faiblesses** : Propriétaire, moins de plugins que Claude Code

### Gemini CLI
- **Meilleur pour** : Recherche web (Grounding), extensions tierces, Google ecosystem
- **Forces** : 300+ extensions, open source, Google Search intégré, sandbox
- **Faiblesses** : Moins mature, documentation en construction

### Kiro CLI
- **Meilleur pour** : Infrastructure AWS, specs formelles, hooks automatisés
- **Forces** : Intégration AWS native, steering files, specs (requirements/design/tasks), hooks
- **Faiblesses** : Spécialisé AWS, moins de plugins

### Vibe CLI
- **Meilleur pour** : Rapidité, simplicité, workflows minimalistes
- **Forces** : Très léger, démarrage rapide, syntaxe simple (@, !)
- **Faiblesses** : Peu de fonctionnalités avancées, pas de MCP, pas d'extensions

---

## 💡 Recommandations par profil

### Développeur Full-stack
**Choix recommandé** : Claude Code ou Cursor IDE
- Support MCP complet
- Plugins/Skills
- Modes Plan/Ask pour conception

### DevOps / Infrastructure
**Choix recommandé** : Kiro CLI
- Intégration AWS native
- Hooks pour automatisation
- Steering pour best practices

### Recherche / Prototypage rapide
**Choix recommandé** : Vibe CLI ou Gemini CLI
- Démarrage rapide
- Syntaxe simple
- Léger en ressources

### Développeur nécessitant des extensions tierces
**Choix recommandé** : Gemini CLI
- 300+ extensions (Figma, Stripe, Shopify, etc.)
- Open source
- Communauté active

---

## 🔗 Ressources

| CLI | Documentation | GitHub/Source |
|-----|---------------|---------------|
| **Claude Code** | [docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code) | Propriétaire |
| **Cursor** | [cursor.com/docs](https://cursor.com/docs) | Propriétaire |
| **Gemini** | [google-gemini.github.io/gemini-cli](https://google-gemini.github.io/gemini-cli/) | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) |
| **Kiro** | [kiro.dev/docs](https://kiro.dev/docs/) | [github.com/aws/kiro](https://kiro.dev/) |
| **Vibe** | [docs.mistral.ai/mistral-vibe](https://docs.mistral.ai/mistral-vibe) | [github.com/mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe) |

---

## 🔄 Notes de version

**v1.0 (24-01-2026)**
- Création du comparatif
- Analyse de 5 CLI majeures
- Recommandations par profil

---

**Note** : Ce document est un comparatif à jour au 24 janvier 2026. Les fonctionnalités peuvent évoluer rapidement.

<<<END>>>
