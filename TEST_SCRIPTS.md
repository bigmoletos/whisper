# Tests des scripts - À exécuter dans l'ordre

## ✅ Corrections appliquées dans start_fast.bat

1. **Supprimé les parenthèses problématiques** dans `if/else`
2. **Remplacé `else` par `goto`** pour éviter les bugs de parsing
3. **Supprimé les guillemets** dans les messages echo

## 🧪 Tests à effectuer

### Test 1: Syntaxe de base
```cmd
.\test_syntax.bat
```
**Attendu:** Doit afficher la version Python et "Tous les tests OK"

### Test 2: Script simplifié
```cmd
.\scripts\start_fast.bat
```

**Attendu:**
```
Detection de Python...
[OK] Python 3.11 trouve
Python 3.11.9

Commande Python: py -3.11

Verification de la configuration...
[OK] Configuration correcte (faster-whisper)

Verification de faster-whisper...
```

Si faster-whisper n'est pas installé:
```
[INFO] faster-whisper n'est pas installe

Installation de faster-whisper en mode utilisateur...
[... progression pip ...]
```

### Test 3: Script à la racine (alternative)
```cmd
.\start.bat
```

## 📋 Checklist de validation

- [ ] Test 1 réussit sans erreur "... était inattendu"
- [ ] Test 2 détecte Python 3.11 ou 3.12
- [ ] Test 2 vérifie config.json avec succès
- [ ] Test 2 installe faster-whisper OU lance l'application

## 🐛 En cas d'erreur

### Erreur: "... était inattendu"
→ Parenthèses ou guillemets mal échappés
→ Vérifier qu'il n'y a pas de `(` ou `)` dans les `echo`

### Erreur: "PYTHON_CMD is not defined"
→ La détection Python a échoué
→ Exécuter: `.\scripts\debug_python.bat`

### Erreur: "config_checker.py not found"
→ Mauvais répertoire de travail
→ Le script doit être dans `scripts\`

## 📊 Résultat attendu final

```
============================================
  Whisper STT - Faster-Whisper
============================================

Detection de Python...
[OK] Python 3.11 trouve
Python 3.11.9

Commande Python: py -3.11

Verification de la configuration...
[OK] Configuration correcte (faster-whisper)

Verification de faster-whisper...
[OK] faster-whisper est installe

============================================
  Demarrage de l'application
============================================

Raccourci: Ctrl+Alt+7
Arret: Ctrl+C

[... Application démarre ...]
```
