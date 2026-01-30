# Guide d'Adaptation Vocale - Whisper STT

## 🎯 Problème identifié

D'après vos tests, le système ne reconnaît pas correctement les termes techniques :
- "Angular" → "en boulard" / "angular" ✅
- "OpenRewrite" → "Open Wheelright" / "Open-Rewrite" ✅  
- "coq-of-js" → "Koch of GES" / "Cocovgs"
- "strands-agent" → "Strings agents" / "Strings Agent"
- "low-complexity" → "low complexity" / "locomplexity"

## 🔍 Causes identifiées

### 1. **Mauvaise configuration**
```
❌ Utilise le modèle "base" au lieu de "large-v3"
❌ Ignore votre prompt personnalisé
❌ Charge la config par défaut au lieu de votre config
```

### 2. **Pas d'adaptation à votre voix**
Le modèle n'est pas habitué à :
- Votre accent/prononciation
- Votre débit de parole
- Votre environnement audio

## 🛠️ Solutions immédiates

### 1. **Utiliser le bon projet**
```bash
# Au lieu de voice-to-text-turbo, utilisez :
cd whisper/projects/voice-to-text-turbo
start.bat
```

### 2. **Vérifier la configuration**
Le fichier `projects/voice-to-text-turbo/config.json` doit contenir :
```json
{
    "whisper": {
        "model": "large-v3",  // ✅ Pas "base"
        "initial_prompt": "... Angular, OpenRewrite, coq-of-js ..."  // ✅ Vos termes
    }
}
```

### 3. **Lancer l'adaptation vocale**
```bash
cd whisper
scripts\voice_adaptation.bat
```

## 🎤 Session d'adaptation vocale

### Étape 1 : Préparation
1. **Environnement calme** (pas de bruit de fond)
2. **Microphone proche** (15-20 cm de la bouche)
3. **Position constante** (même distance/angle)

### Étape 2 : Entraînement guidé
Le script vous fera lire ces phrases :

```
1. "Je migre le projet Angular avec TypeScript"
2. "J'utilise OpenRewrite pour la transformation automatique"  
3. "Coq-of-js génère les preuves formelles"
4. "Strands-agent d'Amazon aide à l'automation"
5. "Kiro IDE avec MCP facilite le développement"
```

### Étape 3 : Analyse des résultats
- **Similarité > 80%** : Excellente adaptation ✅
- **Similarité 60-80%** : Bonne, à améliorer 🟡
- **Similarité < 60%** : Problème technique ❌

## 📊 Conseils de prononciation

### Termes problématiques identifiés :

| Terme | Prononciation | Conseil |
|-------|---------------|---------|
| **Angular** | "Ann-gou-laire" | Bien séparer les syllabes |
| **OpenRewrite** | "O-penne Ri-raïte" | Pause entre les mots |
| **coq-of-js** | "Coque-of-Jay-Esse" | Épeler "JS" |
| **strands-agent** | "Strands A-jente" | Bien articuler le "d" |
| **low-complexity** | "Low Com-plex-i-ty" | Séparer avec tiret |
| **MCP** | "M-C-P" | Épeler lettre par lettre |
| **TypeScript** | "Taïpe-Scripte" | Bien séparer |

### Techniques générales :
1. **Débit** : Parlez 20% plus lentement que normal
2. **Articulation** : Exagérez légèrement les consonnes
3. **Pauses** : Marquez les tirets et espaces
4. **Répétition** : Si mal reconnu, répétez identiquement

## 🔧 Optimisations techniques

### 1. **Améliorer le prompt**
Ajoutez vos termes spécifiques les plus utilisés en début de prompt :

```json
"initial_prompt": "Vocabulaire prioritaire : Angular, TypeScript, OpenRewrite, coq-of-js, strands-agent, Kiro IDE, MCP, low-complexity, Jira. [reste du prompt...]"
```

### 2. **Ajuster les paramètres audio**
```json
"audio": {
    "silence_threshold": 0.02,  // Plus sensible
    "silence_duration": 1.0,    // Moins d'attente
    "chunk_duration": 2.0       // Segments plus courts
}
```

### 3. **Utiliser la correction de texte**
Activez la correction automatique dans `config.json` :
```json
"text_correction": {
    "enabled": true,
    "backend": "ollama"  // Si vous avez Ollama installé
}
```

## 📈 Plan d'amélioration progressive

### Semaine 1 : Adaptation de base
- [ ] Lancer `voice_adaptation.bat`
- [ ] Enregistrer les 5 phrases de test
- [ ] Analyser les résultats
- [ ] Ajuster la prononciation

### Semaine 2 : Optimisation
- [ ] Ajouter vos termes les plus fréquents au prompt
- [ ] Tester avec des phrases plus longues
- [ ] Affiner les paramètres audio

### Semaine 3 : Validation
- [ ] Test en conditions réelles
- [ ] Mesurer l'amélioration
- [ ] Documenter les meilleures pratiques

## 🚨 Dépannage rapide

### Problème : "Modèle base au lieu de large-v3"
```bash
# Solution : Utiliser le bon dossier
cd whisper/projects/voice-to-text-turbo
start.bat
```

### Problème : "Termes techniques mal reconnus"
```bash
# Solution : Adaptation vocale
cd whisper
scripts\voice_adaptation.bat
```

### Problème : "Configuration ignorée"
```bash
# Vérifier que le fichier existe :
dir projects\voice-to-text-turbo\config.json
```

## 📞 Support

Si les problèmes persistent :
1. Vérifiez les logs dans `whisper_stt.log`
2. Testez avec le modèle "medium" si "large-v3" est trop lent
3. Considérez l'utilisation de Faster-Whisper avec GPU

---

**🎯 Objectif** : Passer de 30% à 90%+ de reconnaissance correcte des termes techniques en 1-2 semaines d'adaptation.