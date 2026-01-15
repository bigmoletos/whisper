# Guide Git : Commandes et Workflow

## Initialisation et Clonage

- **Initialiser git**

git config --global user.name "Franck Desmedt"
git config --global user.email "franck.desmedt@hps-wordlwide.com"

- **Pour confirmer que les informations ont bien été enregistrées, exécutez :**
git config --global --list

- **Initialiser un dépôt local**
  ```bash
  git init
  ```
  *Effet* : Initialise un dépôt Git dans le répertoire courant.
  [Doc Git Init](https://git-scm.com/docs/git-init)

- **Cloner un dépôt distant**
  ```bash
  git clone https://github.com/bigmoletos/whisper.git
  ```
  *Effet* : Clone un dépôt distant en local.
  [Doc Git Clone](https://git-scm.com/docs/git-clone)

---

## Configuration des Remotes
- **Ajouter un remote**
  ```bash
  git remote add origin https://github.com/bigmoletos/whisper.git
  ```
  *Effet* : Ajoute un lien vers un dépôt distant (sans push automatique).
  [Doc Git Remote](https://git-scm.com/docs/git-remote)

- **Vérifier les remotes configurés**
  ```bash
  git remote -v
  ```
  *Effet* : Liste les dépôts distants configurés.
  [Doc Git Remote](https://git-scm.com/docs/git-remote)

---

## Gestion des Branches
- **Renommer une branche locale**
  ```bash
  git branch -m master main
  ```
  *Effet* : Renomme la branche locale active (ex: `master` → `main`).
  [Doc Git Branch](https://git-scm.com/docs/git-branch)

- **Créer une nouvelle branche `dev`**
  ```bash
  git checkout -b dev
  ```
  *Effet* : Crée et bascule sur une nouvelle branche `dev` depuis la branche actuelle.
  [Doc Git Checkout](https://git-scm.com/docs/git-checkout)

- **Créer une nouvelle branche `fix`**
  ```bash
  git checkout -b fix
  ```
  *Effet* : Crée et bascule sur une nouvelle branche `fix` depuis la branche actuelle.
  [Doc Git Checkout](https://git-scm.com/docs/git-checkout)

- **Lister toutes les branches**
  ```bash
  git branch -a
  ```
  *Effet* : Liste toutes les branches locales et distantes.
  [Doc Git Branch](https://git-scm.com/docs/git-branch)

- **Vérifier le tracking des branches**
  ```bash
  git branch -vv
  ```
  *Effet* : Affiche les branches locales et leur branche distante associée.
  [Doc Git Branch](https://git-scm.com/docs/git-branch)

---

## Synchronisation et Mise à Jour
- **Vérifier l'état du dépôt**
  ```bash
  git status
  ```
  *Effet* : Affiche l'état des fichiers (modifiés, stagés, etc.).
  [Doc Git Status](https://git-scm.com/docs/git-status)

- **Récupérer les modifications distantes**
  ```bash
  git pull origin main
  ```
  *Effet* : Récupère et fusionne les modifications distantes dans la branche locale.
  [Doc Git Pull](https://git-scm.com/docs/git-pull)

- **Nettoyer les références distantes obsolètes**
  ```bash
  git fetch --prune
  ```
  *Effet* : Supprime les références distantes obsolètes (ex: `master` si supprimée).
  [Doc Git Fetch](https://git-scm.com/docs/git-fetch)

- **Récupérer toutes les branches distantes**
  ```bash
  git fetch origin
  ```
  *Effet* : Récupère toutes les branches distantes sans fusion.
  [Doc Git Fetch](https://git-scm.com/docs/git-fetch)

---

## Staging et Commits
- **Stager les changements**
  ```bash
  git add .
  ```
  *Effet* : Ajoute tous les fichiers modifiés au staging area.
  [Doc Git Add](https://git-scm.com/docs/git-add)

- **Commiter les changements**
  ```bash
  git commit -m "Ma feature ou fix 😎"
  ```
  *Effet* : Crée un commit local avec les fichiers stagés.
  [Doc Git Commit](https://git-scm.com/docs/git-commit)

- **Vérifier les commits**
  ```bash
  git log --oneline -5
  ```
  *Effet* : Affiche les 5 derniers commits de manière concise.
  [Doc Git Log](https://git-scm.com/docs/git-log)

---

## Fusion et Push
- **Fusionner `main` dans `dev`**
  ```bash
  git checkout dev && git merge main && git push origin dev
  ```
  *Effet* : Fusionne `main` dans `dev` et push les changements.
  [Doc Git Merge](https://git-scm.com/docs/git-merge)

- **Pousser une branche locale vers le remote**
  ```bash
  git push --set-upstream origin main
  ```
  *Effet* : Push la branche locale `main` et définit le tracking avec la branche distante.
  [Doc Git Push](https://git-scm.com/docs/git-push)

- **Pousser les commits locaux**
  ```bash
  git push origin main
  ```
  *Effet* : Push les commits locaux vers la branche distante `main`.
  [Doc Git Push](https://git-scm.com/docs/git-push)

---

## Suppression de Branches
- **Supprimer une branche locale**
  ```bash
  git branch -d master
  ```
  *Effet* : Supprime la branche locale `master` (si fusionnée).
  [Doc Git Branch](https://git-scm.com/docs/git-branch)

- **Supprimer une branche distante**
  ```bash
  git push origin --delete master
  ```
  *Effet* : Supprime la branche `master` sur le dépôt distant.
  [Doc Git Push](https://git-scm.com/docs/git-push)

---

## Bonnes Pratiques
- Toujours faire un `git pull` avant de pousser (`git push`) pour éviter les conflits.
- Utiliser des messages de commit clairs et descriptifs.
- Vérifier l’état avec `git status` avant toute opération critique.
