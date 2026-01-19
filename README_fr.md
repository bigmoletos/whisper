[English](README.md)

# Whisper STT Global (Français)

Ceci est un service global de reconnaissance vocale (STT) pour Windows qui utilise Whisper d'OpenAI pour transcrire l'audio de votre microphone et injecter le texte dans n'importe quelle application.

## Fonctionnalités

- **Raccourci clavier global :** Utilisez un raccourci clavier configurable (par défaut : `Ctrl+Alt+7`) pour démarrer et arrêter l'enregistrement depuis n'importe où dans Windows.
- **Plusieurs moteurs Whisper :** Prend en charge `openai-whisper` standard, `faster-whisper` optimisé et `whisper-cpp` haute performance. L'application se rabattra automatiquement sur un moteur fonctionnel si votre moteur préféré n'est pas disponible.
- **Notifications de bureau :** Fournit des notifications de bureau pour les états d'enregistrement, de traitement et d'erreur.
- **Installation facile :** Livré avec un script d'installation simple pour configurer toutes les dépendances.
- **Configurable :** Tous les paramètres, y compris le raccourci clavier, le modèle Whisper et la langue, peuvent être configurés dans un fichier `config.json`.

## Installation

1.  **Installez Python :** Assurez-vous d'avoir Python 3.10 ou une version ultérieure installée et ajoutée à votre `PATH`. Vous pouvez le télécharger sur [python.org](https://www.python.org/).
2.  **Installez ffmpeg :** Whisper nécessite ffmpeg. Vous pouvez l'installer depuis [ffmpeg.org](https://ffmpeg.org/download.html) ou en utilisant winget :
    ```bash
    winget install ffmpeg
    ```
3.  **(Facultatif) Installez Rust :** Si vous souhaitez utiliser le moteur `faster-whisper` (qui est plus rapide que le standard), vous devez installer Rust. Vous pouvez l'installer depuis [rustup.rs](https://rustup.rs/) ou en utilisant winget :
    ```bash
    winget install Rustlang.Rustup
    ```
4.  **Exécutez le script d'installation :**
    ```bash
    .\scripts\install.bat
    ```
    Cela créera un environnement virtuel dans le répertoire `venv_whisper` et installera toutes les dépendances nécessaires.

## Utilisation

1.  **Démarrez le service :**
    ```bash
    .\scripts\start_service.bat
    ```
2.  **Appuyez sur le raccourci clavier** (par défaut : `Ctrl+Alt+7`) pour démarrer l'enregistrement. La notification de bureau indiquera que l'enregistrement a commencé.
3.  **Appuyez à nouveau sur le raccourci clavier** pour arrêter l'enregistrement. L'audio capturé sera transcrit et le texte sera injecté dans votre application active.
4.  **Appuyez sur `Ctrl+C`** dans la console pourarrêter le service.

## Exécution en tant que service

Vous pouvez également exécuter l'application en tant que service Windows. Cela permettra à l'application de s'exécuter en arrière-plan et de démarrer automatiquement lorsque vous démarrez votre ordinateur.

1.  **Installez le service :**
    ```bash
    .\scripts\run_as_service.bat install
    ```
2.  **Démarrez le service :**
    ```bash
    sc start WhisperSTTService
    ```
3.  **Arrêtez le service :**
    ```bash
    sc stop WhisperSTTService
    ```
4.  **Supprimez le service :**
    ```bash
    .\scripts\run_as_service.bat remove
    ```

## Scripts utilitaires

-   **`scripts\open_config.bat` :** Ouvre le fichier de configuration de l'application.
-   **`scripts\open_log.bat` :** Ouvre le fichier journal de l'application.
-   **`scripts\clean_all.bat` :** Nettoie le projet de tous les fichiers générés.
-   **`scripts\update.bat` :** Vérifie les mises à jour des dépendances et les installe.
-   **`scripts\open_documentation.bat` :** Ouvre le fichier `README.md` dans votre navigateur Web par défaut.
-   **`scripts\open_logs.bat` :** Ouvre le fichier `whisper_stt.log` dans votre éditeur de texte par défaut pour le débogage.
-   **`scripts\clean.bat` :** Supprime le répertoire `__pycache__` pour nettoyer le projet.

## Configuration

Vous pouvez personnaliser l'application en modifiant le fichier `config.json`. Voici les options disponibles :

-   **`whisper` :**
    -   `engine` : Le moteur Whisper à utiliser (`whisper`, `faster-whisper` ou `whisper-cpp`).
    -   `model` : Le modèle Whisper à utiliser (`tiny`, `base`, `small`, `medium`, `large`).
    -   `language` : La langue de l'audio (par exemple, `en`, `fr`, `es`).
    -   `device` : L'appareil sur lequel exécuter le modèle (`cpu` ou `cuda`).
    -   `compute_type` : Le type de calcul pour `faster-whisper` (`int8`, `float16`, `float32`).
-   **`audio` :**
    -   `sample_rate` : Le taux d'échantillonnage de l'audio.
    -   `channels` : Le nombre de canaux audio.
    -   `chunk_duration` : La durée de chaque bloc audio en secondes.
    -   `silence_threshold` : Le seuil de silence pour détecter la fin de la parole.
    -   `silence_duration` : La durée du silence à attendre avant d'arrêter l'enregistrement.
-   **`hotkey` :**
    -   `modifiers` : Les touches de modification pour le raccourci clavier (`ctrl`, `alt`, `shift`).
    -   `key` : La touche pour le raccourci clavier.
-   **`logging` :**
    -   `level` : Le niveau de journalisation (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
    -   `file` : Le fichier dans lequel écrire les journaux.

## Vérification de la configuration

Le script `start_service.bat` exécutera automatiquement une vérification de la configuration à l'aide du script `check_config.py`. Ce script validera le fichier `config.json` et vous avertira de toute erreur. Il vérifiera également si Rust est installé lorsque `faster-whisper` est configuré. Si vous souhaitez exécuter la vérification manuellement, vous pouvez utiliser la commande suivante :
```bash
python check_config.py
```

## Tests

Pour exécuter les tests, vous devez avoir `pytest` installé. Vous pouvez l'installer avec pip :
```bash
pip install pytest
```

Ensuite, vous pouvez exécuter les tests à l'aide du script suivant :
```bash
.\scripts\run_tests.bat
```

## Empaquetage

Pour empaqueter l'application dans un seul fichier exécutable, vous devez avoir `PyInstaller` installé. Vous pouvez l'installer avec pip :
```bash
pip install pyinstaller
```

Ensuite, vous pouvez exécuter le script d'empaquetage :
```bash
.\scripts\package.bat
```
Cela créera un répertoire `dist` avec le fichier `WhisperSTT.exe`.

## Développement

Pour configurer l'environnement de développement, vous pouvez utiliser le script `install_dev.bat`. Cela installera toutes les dépendances nécessaires, y compris `pytest` et `pyinstaller`.
```bash
.\scripts\install_dev.bat
```

Pour générer un fichier `requirements.txt` avec les versions exactes des dépendances, vous pouvez utiliser le script `generate_requirements.bat`.
```bash
.\scripts\generate_requirements.bat
```

Pour ouvrir le projet dans Visual Studio Code, vous pouvez utiliser le script `open_in_vscode.bat`.
```bash
.\scripts\open_in_vscode.bat
```

Pour vérifier le code pour les erreurs de style, vous pouvez utiliser le script `lint.bat`. Cela utilisera flake8 pour vérifier le code dans le répertoire `src`.
```bash
.\scripts\lint.bat
```

Pour formater automatiquement le code, vous pouvez utiliser le script `format.bat`. Cela utilisera black pour formater le code dans le répertoire `src`.
```bash
.\scripts\format.bat
```

Pour vérifier le code pour les erreurs de type, vous pouvez utiliser le script `type_check.bat`. Cela utilisera mypy pour vérifier le code dans le répertoire `src`.
```bash
.\scripts\type_check.bat
```

Pour exécuter toutes les vérifications (lint, vérification de type et tests) en séquence, vous pouvez utiliser le script `run_all_checks.bat`.
```bash
.\scripts\run_all_checks.bat
```

Pour générer la documentation, vous pouvez utiliser le script `generate_documentation.bat`. Cela utilisera Sphinx pour générer la documentation dans le répertoire `docs`.
```bash
.\scripts\generate_documentation.bat
```

Pour ouvrir la documentation générée, vous pouvez utiliser le script `open_generated_documentation.bat`.
```bash
.\scripts\open_generated_documentation.bat
```

Pour nettoyer la documentation générée, vous pouvez utiliser le script `clean_documentation.bat`.
```bash
.\scripts\clean_documentation.bat
```

Pour créer un fichier zip de version du projet, vous pouvez utiliser le script `create_release.bat`.
```bash
.\scripts\create_release.bat
```

## Désinstallation

Pour désinstaller l'application, vous pouvez utiliser le script `uninstall.bat`. Cela supprimera tous les fichiers et répertoires créés par l'application, à l'exception du fichier `config.json`.
```bash
.\scripts\uninstall.bat
```
