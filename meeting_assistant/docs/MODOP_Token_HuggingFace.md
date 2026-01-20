# Mode Opératoire : Configuration du Token Hugging Face pour Pyannote

## Objectif
Configurer l'accès au modèle de diarisation pyannote pour identifier automatiquement les différents locuteurs dans les réunions.

## Prérequis
- Un navigateur web
- Accès administrateur pour les variables d'environnement Windows (optionnel)

## Durée estimée
5 minutes

---

## Étape 1 : Créer un compte Hugging Face (si nécessaire)

1. Ouvrir https://huggingface.co/join
2. Remplir le formulaire d'inscription :
   - Username
   - Email
   - Password
3. Valider l'email de confirmation

---

## Étape 2 : Accepter les conditions du modèle Pyannote

**Important** : Cette étape est obligatoire, sinon le modèle ne pourra pas être téléchargé.

1. Se connecter à Hugging Face
2. Aller sur https://huggingface.co/pyannote/speaker-diarization-3.1
3. Lire les conditions d'utilisation
4. Cliquer sur **"Agree and access repository"**
5. Répéter pour le modèle de segmentation : https://huggingface.co/pyannote/segmentation-3.0
   - Cliquer sur **"Agree and access repository"**

---

## Étape 3 : Créer un token d'accès

1. Aller sur https://huggingface.co/settings/tokens
2. Cliquer sur **"Create new token"**
3. Configurer le token :
   - **Token name** : `meeting-assistant` (ou autre nom descriptif)
   - **Token type** : `Read` (suffisant pour télécharger les modèles)
4. Cliquer sur **"Create token"**
5. **IMPORTANT** : Copier le token affiché (il commence par `hf_...`)
   - Ce token ne sera plus visible après avoir quitté la page !

---

## Étape 4 : Configurer le token sur Windows

### Option A : Variable d'environnement permanente (recommandé)

1. Ouvrir un terminal **CMD en administrateur**
2. Exécuter :
   ```cmd
   setx HF_TOKEN "hf_votre_token_ici" /M
   ```
3. Fermer et rouvrir le terminal pour que la variable soit prise en compte

### Option B : Variable d'environnement utilisateur

1. Ouvrir un terminal CMD
2. Exécuter :
   ```cmd
   setx HF_TOKEN "hf_votre_token_ici"
   ```
3. Fermer et rouvrir le terminal

### Option C : Via l'interface Windows

1. Appuyer sur `Win + R`
2. Taper `sysdm.cpl` et valider
3. Onglet **"Avancé"** → **"Variables d'environnement"**
4. Dans "Variables utilisateur", cliquer **"Nouvelle..."**
   - Nom : `HF_TOKEN`
   - Valeur : `hf_votre_token_ici`
5. OK → OK → OK

---

## Étape 5 : Activer Pyannote dans la configuration

1. Ouvrir le fichier :
   ```
   C:\programmation\outils\vtt\whisper\meeting_assistant\config.json
   ```

2. Modifier la section `diarization` :
   ```json
   "diarization": {
     "enabled": true,
     "speaker_change_pause": 2.0,
     "max_speakers": 10,
     "participant_names": [],
     "use_pyannote": true,
     "hf_token_env": "HF_TOKEN"
   }
   ```

3. Sauvegarder le fichier

---

## Étape 6 : Vérifier la configuration

1. Ouvrir un **nouveau** terminal CMD
2. Vérifier que le token est configuré :
   ```cmd
   echo %HF_TOKEN%
   ```
   → Doit afficher votre token (commençant par `hf_...`)

3. Tester la connexion Hugging Face :
   ```cmd
   huggingface-cli whoami
   ```
   → Doit afficher votre username

---

## Étape 7 : Premier lancement

Au premier lancement avec pyannote activé, le modèle sera téléchargé automatiquement (~1 Go).

```cmd
c:\programmation\outils\vtt\whisper\scripts\start_meeting_assistant.bat
```

---

## Dépannage

### "Access denied" ou "Gated model"
- Vérifier que vous avez bien accepté les conditions à l'étape 2
- Attendre quelques minutes après avoir accepté (propagation)

### "Token not found"
- Vérifier que la variable d'environnement est bien définie
- Rouvrir le terminal après avoir défini la variable

### Le modèle ne se télécharge pas
- Vérifier la connexion internet
- Vérifier que le token a les droits "Read"

---

## Liens utiles

- Hugging Face : https://huggingface.co
- Tokens : https://huggingface.co/settings/tokens
- Modèle pyannote : https://huggingface.co/pyannote/speaker-diarization-3.1
- Documentation pyannote : https://github.com/pyannote/pyannote-audio

---

*Document créé le 19/01/2026 pour Meeting Assistant*
