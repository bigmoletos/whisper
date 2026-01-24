# Résumé des Corrections Effectuées

**Date** : 24-01-2026
**Fichiers corrigés** : 5 guides CLI d'IA + 1 comparatif créé

---

## 📝 Vue d'ensemble

Toutes les commandes incorrectes dans les 5 guides CLI ont été corrigées en s'appuyant sur les documentations officielles de chaque outil.

---

## ✅ Fichiers corrigés

### 1. **claude_cli_extensions.md** (Claude Code CLI)

#### Corrections principales :

**MCP**
- ❌ `/mcp add`, `/mcp remove`, `/mcp list` → ✅ `/mcp` (menu interactif)
- ✅ Ajout des vraies commandes CLI : `claude mcp add`, `claude mcp list`, `claude mcp get`, `claude mcp add-from-claude-desktop`
- ✅ Correction de la syntaxe : options AVANT le nom du serveur
- ✅ Ajout support HTTP : `claude mcp add --transport http <name> <url>`

**Skills**
- ❌ `/skills list`, `/skills add`, `/skills remove`, `/skills info` → ✅ Supprimées (n'existent pas)
- ✅ Skills s'invoquent directement : `/skill-name` (ex: `/explain-code`)
- ❌ `/plugin marketplace add` → ✅ `claude plugin install` (CLI) ou `/plugin` (interactif)

**Tasks**
- ❌ `/task create`, `/task list`, `/task status`, `/task cancel` → ✅ Supprimées
- ✅ Remplacé par : `/tasks` (pluriel) pour background tasks et `/todos` pour TODO items

**Agents**
- ❌ `/agents list`, `/agents create`, `/agents stop`, `/agents logs`, `/agents switch` → ✅ Supprimées
- ✅ Remplacé par : `/agents` (menu interactif unique)
- ✅ CLI : `claude --agent <name>`

**Plugins**
- ❌ `/plugin marketplace add`, `/plugin marketplace remove`, `/plugin marketplace search` → ✅ Supprimées
- ✅ CLI : `claude plugin install`, `claude plugin uninstall`, `claude plugin list`, `claude plugin update`
- ✅ Interactif : `/plugin` (menu)

**Configuration**
- ✅ Correction des chemins : `~/.claude/settings/mcp_servers.json` (au lieu de `~/.claude/mcp_servers.json`)
- ✅ Ajout des exemples HTTP pour serveurs distants

**Exemples pratiques**
- ✅ Exemple 1 : Correction des commandes pour projet Angular
- ✅ Exemple 2 : Correction workflow revue de code
- ✅ Exemple 3 : Correction exploration codebase

---

### 2. **cursor_cli_extensions.md** (Cursor IDE)

#### Corrections principales :

**Nouvelles commandes janvier 2026**
- ✅ Ajout `/models` - lister et changer de modèle
- ✅ Ajout `/rules` - créer et éditer des règles
- ✅ Ajout `/mcp list` - menu MCP interactif
- ✅ Ajout `/mcp enable <server>` et `/mcp disable <server>`

**Commandes MCP**
- ❌ `agent mcp list`, `agent mcp status`, `agent mcp add`, `agent mcp remove` → ✅ Supprimées
- ✅ Note ajoutée : Pas de commandes CLI, configuration via JSON uniquement
- ✅ Configuration dans `~/.cursor/mcp.json` ou `.cursor/mcp.json`

**Modes**
- ✅ Clarification : `/plan` ou `--mode=plan`
- ✅ Clarification : `/ask` ou `--mode=ask`

**Commandes personnalisées**
- ✅ Clarification : Fichiers `.cursor/commands/*.md` → commandes slash automatiques

**Exemples**
- ✅ Exemple 2 : Ajout utilisation `/mcp enable` après configuration JSON

---

### 3. **gemini_cli_extensions.md** (Gemini CLI Google)

#### Corrections principales :

**Commandes slash**
- ✅ Conservées (documentées) : `/help`, `/settings`, `/memory`, `/mcp`, `/stats`, `/chat`
- ❌ `/clear`, `/compress`, `/copy`, `/directory`, `/dir`, `/tools`, `/theme`, `/bug`, `/logout` → ✅ Supprimées (non documentées)

**Commandes CLI**
- ✅ Amélioration du tableau : ajout `gemini extensions install/uninstall/enable/disable/update`
- ✅ Clarification sur les versions (latest, preview, nightly)

**Détails slash commands**
- ✅ Réécriture complète de la section avec description précise de chaque commande documentée
- ✅ Note explicite sur les commandes non-officielles supprimées

---

### 4. **kiro_cli_extensions.md** (Kiro CLI AWS)

#### Corrections principales :

**Commandes système**
- ✅ Documentées officiellement : `/model`, `/agent`, `/chat`, `/mcp`, `/billing`
- ✅ Note : Autres commandes possibles mais non documentées

**Commandes Steering**
- ❌ `/accessibility`, `/code-review`, `/performance`, `/refactor`, `/testing` présentées comme intégrées
- ✅ Clarification : Ce sont des **exemples de steering personnalisés** à créer dans `.kiro/steering/*.md` avec `inclusion: manual`

**Commandes Hooks**
- ❌ `/sync-source-to-docs`, `/run-tests`, `/generate-changelog` présentées comme intégrées
- ✅ Clarification : Ce sont des **exemples de hooks personnalisés** à créer dans `.kiro/hooks/hooks.yaml` avec `trigger: manual`

**Documentation**
- ✅ Ajout tableau distinguant : Commandes système, Steering manuels, Hooks manuels
- ✅ Exemple 3 amélioré avec hook manuel `/run-tests`

---

### 5. **vibe_cli_extensions.md** (Mistral Vibe CLI)

#### Corrections principales :

**Commandes slash**
- ✅ Conservées (documentées) : `/config`, `/theme`
- ❌ `/help`, `/clear`, `/quit`, `/exit`, `/model`, `/tools`, `/history`, `/undo`, `/diff`, `/save`, `/load` → ✅ Supprimées (non documentées)

**Note importante**
- ✅ Ajout clarification : Vibe est très minimaliste, se concentre sur `@` (fichiers) et `!` (shell)

**Exemples**
- ✅ Exemple 1 : Correction, suppression de `/diff` (n'existe pas)

---

## 📚 Fichier créé

### 6. **comparatif_cli_ia.md** (NOUVEAU)

Création d'un tableau comparatif complet des 5 CLI :

**Contenu :**
- ✅ Comparaison rapide : 12 critères (Open Source, MCP, Plugins, Agents, etc.)
- ✅ Commandes MCP par outil
- ✅ Gestion plugins/extensions par outil
- ✅ Agents et sous-agents par outil
- ✅ Commandes slash principales par outil
- ✅ Cas d'usage recommandés
- ✅ Recommandations par profil développeur
- ✅ Liens vers ressources officielles

---

## 🎯 Méthode de correction

### Sources utilisées

1. **Claude Code** : Agent claude-code-guide + documentation officielle
2. **Cursor** : [Slash commands docs](https://cursor.com/docs/cli/reference/slash-commands), [Changelog jan. 2026](https://cursor.com/changelog/cli-jan-08-2026)
3. **Gemini** : [CLI Commands](https://google-gemini.github.io/gemini-cli/docs/cli/commands.html), [Codelabs](https://codelabs.developers.google.com/gemini-cli-hands-on)
4. **Kiro** : [Slash commands](https://kiro.dev/docs/cli/reference/slash-commands/), [CLI commands](https://kiro.dev/docs/cli/reference/cli-commands/)
5. **Vibe** : [GitHub](https://github.com/mistralai/mistral-vibe), [Docs](https://docs.mistral.ai/mistral-vibe/introduction)

### Approche

1. ✅ Recherche des documentations officielles via WebSearch
2. ✅ Consultation de l'agent spécialisé claude-code-guide pour Claude Code
3. ✅ Vérification croisée entre documentation et implémentation
4. ✅ Suppression des commandes non documentées
5. ✅ Ajout de notes explicatives pour éviter la confusion
6. ✅ Mise à jour des exemples pratiques

---

## 📊 Statistiques des corrections

| Fichier | Commandes supprimées | Commandes corrigées | Commandes ajoutées | Notes ajoutées |
|---------|---------------------|--------------------|--------------------|----------------|
| claude_cli_extensions.md | 20+ | 15+ | 10+ | 8 |
| cursor_cli_extensions.md | 4 | 3 | 4 | 3 |
| gemini_cli_extensions.md | 9 | 2 | 5 | 2 |
| kiro_cli_extensions.md | 8 | 5 | 2 | 5 |
| vibe_cli_extensions.md | 10 | 1 | 0 | 2 |
| **TOTAL** | **51+** | **26+** | **21+** | **20** |

---

## ⚠️ Points d'attention importants

### Claude Code
- **Ne PAS utiliser** `/skills list` ou `/skills add` (n'existent pas)
- **Utiliser** directement `/skill-name` pour invoquer une skill
- **Options MCP** doivent venir AVANT le nom du serveur dans `claude mcp add`

### Cursor IDE
- **Pas de CLI** pour les commandes MCP
- **Nouvelles commandes** janvier 2026 : `/models`, `/rules`, `/mcp enable/disable`
- **Configuration MCP** via fichiers JSON uniquement

### Gemini CLI
- **Très peu de commandes slash** documentées (seulement 5-6)
- **Forces** : Extensions (300+), pas les commandes slash
- **Préfixes** : `@` pour fichiers, pas de commandes slash correspondantes

### Kiro CLI
- **Commandes steering et hooks** ne sont PAS intégrées
- **Il faut créer** les fichiers `.kiro/steering/*.md` et `.kiro/hooks/hooks.yaml`
- **Uniquement 5 commandes système** documentées officiellement

### Vibe CLI
- **Très minimaliste** : seulement `/config` et `/theme`
- **Préférer** les préfixes `@` (fichiers) et `!` (shell)
- **Pas de commandes** type `/help`, `/clear`, `/quit` documentées

---

## 🔄 Mises à jour futures recommandées

1. **Cursor** : Vérifier après chaque release mensuelle (nouvelles commandes fréquentes)
2. **Gemini** : Suivre le changelog (projet en développement actif)
3. **Kiro** : Surveiller la documentation AWS (évolutions liées à Bedrock)
4. **Claude Code** : Vérifier après chaque mise à jour majeure
5. **Vibe** : Projet jeune, peu de changements attendus

---

## ✅ Validation

Toutes les commandes dans les 5 guides ont été :
- ✅ Vérifiées contre les documentations officielles
- ✅ Testées quand possible via les outils disponibles
- ✅ Corrigées avec la syntaxe exacte
- ✅ Annotées avec des notes explicatives

**État** : Tous les fichiers sont maintenant conformes aux documentations officielles au 24 janvier 2026.

---

<<<END>>>
