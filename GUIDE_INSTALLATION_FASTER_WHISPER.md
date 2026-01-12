# Guide d'Installation - Faster-Whisper

## Problème : Erreur Rust/Cargo

L'installation de `faster-whisper` peut échouer si Rust n'est pas installé, car certaines dépendances nécessitent une compilation.

## Solutions

### Solution 1 : Installer Rust (Recommandé)

**Méthode automatique** :
```bash
# Utiliser le script d'installation
scripts\install_rust.bat
```

**Méthode manuelle** :
1. **Installer Rust** :
   ```bash
   # Via winget
   winget install Rustlang.Rustup

   # Ou télécharger depuis https://rustup.rs/
   ```

2. **Redémarrer le terminal** après l'installation (important !)

3. **Vérifier l'installation** :
   ```bash
   rustc --version
   ```

4. **Installer faster-whisper** :
   ```bash
   pip install faster-whisper
   ```

### Solution 2 : Utiliser une version précompilée (Plus simple)

Installer les dépendances précompilées :

```bash
# Installer les dépendances binaires d'abord
pip install --only-binary :all: faster-whisper
```

Si cela ne fonctionne pas, essayer :

```bash
# Installer avec des wheels précompilés
pip install faster-whisper --prefer-binary
```

### Solution 3 : Utiliser Whisper standard (Temporaire)

Si vous ne voulez pas installer Rust, vous pouvez utiliser Whisper standard qui fonctionne déjà :

Modifier `config.json` :
```json
{
  "whisper": {
    "engine": "whisper",  // ← Whisper standard
    "model": "large",
    "language": "fr",
    "device": "cpu"
  }
}
```

### Solution 4 : Installation alternative avec conda

Si vous utilisez conda :

```bash
conda install -c conda-forge faster-whisper
```

## Vérification de l'installation

Après installation, vérifier :

```bash
python -c "from faster_whisper import WhisperModel; print('OK')"
```

## Recommandation

**Pour Windows** : La solution la plus simple est d'installer Rust via `winget` ou depuis https://rustup.rs/, puis réinstaller faster-whisper.

**Alternative rapide** : Utiliser Whisper standard qui fonctionne déjà bien et ne nécessite pas Rust.
