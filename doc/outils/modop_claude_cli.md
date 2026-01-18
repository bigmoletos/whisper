# MODOP - Commandes CLI Claude Code

**Auteur** : Bigmoletos
**Version** : 1.0
**Date** : 27-01-2025
**Contexte** : Guide de référence pour l'utilisation du CLI Claude Code avec les commandes slash et les flags de ligne de commande.

---

## 📋 Table des matières

1. [Commandes slash (interactives)](#commandes-slash-interactives)
2. [Flags de ligne de commande](#flags-de-ligne-de-commande)
3. [Exemples d'utilisation](#exemples-dutilisation)
4. [Mode YOLO](#mode-yolo)

---

## 🛠️ Commandes slash (interactives)

Ces commandes s'utilisent dans une session interactive Claude Code ou dans les fichiers de commande (`.claude/commands`).

### 1. `/cost`
**Description** : Afficher l'usage de tokens et les coûts associés à la session actuelle.
**Usage** :
```
/cost
```
**Exemple** : Vérifier le coût d'une session avant de continuer.

---

### 2. `/compact [instructions]`
**Description** : Résumer la conversation pour libérer de la mémoire et réduire le contexte.
**Usage** :
```
/compact
/compact focus on auth logic
```
**Exemple** : Utiliser `/compact` lorsque la conversation devient trop longue et que vous voulez garder uniquement les éléments essentiels.

---

### 3. `/add-dir <path>`
**Description** : Ajouter un répertoire de travail supplémentaire à la session.
**Usage** :
```
/add-dir ../backend
/add-dir ./src/components
```
**Exemple** : Permet à Claude d'accéder à des fichiers en dehors du répertoire de travail initial.

---

### 4. `/agents`
**Description** : Gérer des agents secondaires pour des tâches parallèles.
**Usage** :
```
/agents list
/agents create <nom>
```
**Exemple** : Créer un agent dédié pour tester une fonctionnalité pendant que vous continuez à développer.

---

### 5. `/bug <problème>`
**Description** : Signaler un bug directement à Anthropic.
**Usage** :
```
/bug Le modèle ne répond pas correctement aux prompts en français
```
**Exemple** : Rapporter un problème rencontré avec Claude Code.

---

### 6. `/clear`
**Description** : Effacer l'historique de conversation actuel.
**Usage** :
```
/clear
```
**Exemple** : Recommencer une nouvelle session sans quitter Claude Code.

---

### 7. `/config`
**Description** : Ouvrir ou modifier les réglages de Claude Code.
**Usage** :
```
/config
/config set autoCompact false
/config set model opus
```
**Exemple** : Désactiver la compaction automatique ou changer le modèle par défaut.

---

### 8. `/doctor`
**Description** : Vérifier l'intégrité et la santé de l'installation Claude Code.
**Usage** :
```
/doctor
```
**Exemple** : Diagnostiquer des problèmes d'installation ou de configuration.

---

### 9. `/help`
**Description** : Afficher l'aide intégrée pour toutes les commandes disponibles.
**Usage** :
```
/help
/help /cost
```
**Exemple** : Obtenir de l'aide sur une commande spécifique.

---

### 10. `/init`
**Description** : Initialiser un projet avec le guide `CLAUDE.md`.
**Usage** :
```
/init
```
**Exemple** : Créer la structure de base pour un nouveau projet avec Claude Code.

---

### 11. `/login`
**Description** : Changer de compte Anthropic ou se connecter.
**Usage** :
```
/login
```
**Exemple** : Basculer entre différents comptes Anthropic.

---

### 12. `/logout`
**Description** : Se déconnecter du compte actuel.
**Usage** :
```
/logout
```
**Exemple** : Déconnexion avant de changer de compte.

---

### 13. `/mcp`
**Description** : Gérer les connexions aux serveurs MCP (Model Context Protocol).
**Usage** :
```
/mcp add <server>
/mcp list
/mcp remove <server>
```
**Exemple** : Ajouter un serveur MCP personnalisé pour étendre les capacités de Claude.

---

### 14. `/memory`
**Description** : Éditer les fichiers de mémoire (`CLAUDE.md`) pour la persistance des connaissances.
**Usage** :
```
/memory
/memory edit
```
**Exemple** : Mettre à jour les informations de contexte du projet.

---

### 15. `/model`
**Description** : Changer le modèle utilisé (ex : Sonnet, Opus).
**Usage** :
```
/model opus
/model sonnet
/model haiku
```
**Exemple** : Basculer vers un modèle plus puissant pour des tâches complexes.

---

### 16. `/permissions`
**Description** : Voir ou modifier les permissions (outils autorisés, accès fichiers, etc.).
**Usage** :
```
/permissions view
/permissions edit
```
**Exemple** : Vérifier quels outils Claude peut utiliser dans la session actuelle.

---

### 17. `/pr_comments <pr>`
**Description** : Voir les commentaires sur une pull request GitHub.
**Usage** :
```
/pr_comments 123
/pr_comments https://github.com/user/repo/pull/123
```
**Exemple** : Analyser les retours sur une PR avant de la merger.

---

### 18. `/review <file>`
**Description** : Demander une revue de code sur un fichier ou dossier spécifique.
**Usage** :
```
/review src/auth.ts
/review ./components
```
**Exemple** : Obtenir une analyse de code détaillée avant un commit.

---

### 19. `/status`
**Description** : Afficher le statut système et du compte.
**Usage** :
```
/status
```
**Exemple** : Vérifier l'état de la connexion, le modèle actif, etc.

---

### 20. `/terminal-setup`
**Description** : Installer les raccourcis pour l'entrée multi-lignes (ex : Shift+Enter).
**Usage** :
```
/terminal-setup
```
**Exemple** : Configurer le terminal pour une meilleure expérience de saisie.

---

## ⚙️ Flags de ligne de commande

Ces flags se combinent à `claude` pour personnaliser le comportement en mode script ou interactif.

### Flags principaux

| Flag | Abréviation | Description | Exemple |
|------|-------------|-------------|---------|
| `--print`, `-p` | `-p` | Mode non interactif : exécute une requête puis quitte | `claude -p "Explique ce code"` |
| `--verbose` | — | Log verbose pour debug détaillé | `claude --verbose` |
| `--resume`, `-r` | `-r` | Reprendre une session existante via son ID | `claude --resume abc123` |
| `--continue` | `-c` | Continuer la dernière session | `claude --continue` |
| `--max-turns` | — | Limiter le nombre de tours d'agent | `claude -p --max-turns 5 "Analyse rapide"` |
| `--model <modèle>` | — | Spécifier le modèle (sonnet, opus, haiku) | `claude --model opus` |
| `--output-format <format>` | — | Format de sortie (`text`, `json`, `stream-json`) | `claude -p "query" --output-format json` |
| `--input-format <format>` | — | Format d'entrée dans mode print | `claude -p --input-format json "query"` |
| `--include-partial-messages` | — | Inclure messages partiels dans le streaming JSON | `claude --include-partial-messages` |
| `--add-dir <path>` | — | Ajouter des répertoires accessibles pour la session | `claude --add-dir ./backend` |
| `--dangerously-skip-permissions` | — | ⚠️ **Risque élevé** – désactive les prompts de permissions | `claude --dangerously-skip-permissions` |

---

## 📝 Exemples d'utilisation

### Exemple 1 : Requête simple en mode non interactif
```bash
claude --print "Explique-moi ce que fait cette fonction" --model sonnet
```

### Exemple 2 : Reprendre une session avec verbose
```bash
claude --resume abc123 --verbose
```

### Exemple 3 : Analyser un projet avec plusieurs répertoires
```bash
claude --add-dir ./backend --add-dir ./frontend --print "Analyse l'architecture du projet"
```

### Exemple 4 : Sortie JSON pour traitement automatisé
```bash
claude --print "Liste les fichiers modifiés" --output-format json | jq
```

### Exemple 5 : Limiter les interactions pour un script
```bash
claude --print "Génère un résumé" --max-turns 3 --model haiku
```

---

## 🚨 Mode YOLO

Le mode YOLO désactive toutes les vérifications de sécurité et permet à Claude d'exécuter des commandes sans demander confirmation.

### ⚠️ Avertissement important

- **Risque élevé** : Ce mode peut causer des dommages (suppression de fichiers, accès non souhaité, etc.)
- **Utilisation recommandée** : Uniquement dans un environnement isolé (Docker, VM, répertoire de travail dédié)
- **Première exécution** : Un message d'avertissement apparaît et vous devrez accepter explicitement les risques

### Commande de base
```bash
claude --dangerously-skip-permissions
```

### Commande complète avec options
```bash
claude --dangerously-skip-permissions \
  --continue \
  --print "[VOTRE PROMPT]" \
  --verbose \
  --model opus \
  --output-format text
```

### Exemple d'utilisation en mode YOLO
```bash
# Mode YOLO avec prompt direct
claude --dangerously-skip-permissions --print "Modifie tous les fichiers .ts pour ajouter des commentaires JSDoc" --verbose

# Mode YOLO avec continuation de session
claude --dangerously-skip-permissions --continue --verbose

# Mode YOLO avec sortie JSON pour traitement
claude --dangerously-skip-permissions --print "Analyse le code" --output-format stream-json | jq
```

### Combinaison avec d'autres flags
```bash
# YOLO + modèle Opus + max 10 tours + verbose
claude --dangerously-skip-permissions \
  --model opus \
  --max-turns 10 \
  --verbose \
  --print "Refactorise le code selon les principes SOLID"
```

---

## 📚 Ressources supplémentaires

- **Documentation officielle** : [docs.claude.com](https://docs.claude.com/en/docs/claude-code)
- **Commandes slash** : [docs.claude.com/slash-commands](https://docs.claude.com/en/docs/claude-code/slash-commands)
- **CLI usage** : [docs.claude.com/cli-usage](https://docs.claude.com/en/docs/claude-code/cli-usage)

---

## 🔄 Notes de version

**v1.0 (27-01-2025)**
- Création du MODOP initial
- Documentation des 20 commandes slash principales
- Documentation des flags de ligne de commande
- Section dédiée au mode YOLO avec avertissements

---

**Note** : Ce document est une référence pratique. Pour des informations à jour, consultez la documentation officielle d'Anthropic.

<<<END>>>
