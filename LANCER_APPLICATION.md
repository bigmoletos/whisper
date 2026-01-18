# Comment lancer l'application Whisper STT

## 🚀 Méthode recommandée (PowerShell - Windows 11)

```powershell
.\start.ps1
```

### Si vous avez une erreur de politique d'exécution

**Erreur:** `... ne peut pas être chargé, car l'exécution de scripts est désactivée`

**Solution 1 (une seule fois):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Solution 2 (juste pour ce script):**
```powershell
PowerShell -ExecutionPolicy Bypass -File .\start.ps1
```

**Solution 3 (débloquer le fichier):**
```powershell
Unblock-File .\start.ps1
.\start.ps1
```

## 📝 Méthode alternative (Batch)

```cmd
.\scripts\start_fast.bat
```

Fonctionne sans configuration supplémentaire.

## 🆚 Comparaison

| Critère | PowerShell (.ps1) | Batch (.bat) |
|---------|-------------------|--------------|
| **Robustesse** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Messages colorés** | ✅ | ❌ |
| **Gestion erreurs** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Configuration** | Peut nécessiter ExecutionPolicy | Aucune |
| **Recommandé pour** | Windows 10/11 PowerShell | Tous Windows |

## 🎯 Ce que font les scripts

1. **Détectent Python** (priorité à 3.12, 3.11, 3.10)
2. **Vérifient config.json**
3. **Installent faster-whisper** si nécessaire
4. **Lancent l'application**

## 🔧 Dépannage

### Python non trouvé
```powershell
# Vérifier les versions installées
py --list

# Tester manuellement
py -3.12 --version
py -3.11 --version
```

### faster-whisper ne s'installe pas
1. Installez Rust: https://rustup.rs/
2. OU modifiez `config.json`:
   ```json
   "whisper": {
     "engine": "whisper"
   }
   ```

### L'application ne démarre pas
Vérifiez les logs dans `whisper_stt.log`

## 📊 Ordre de priorité Python

Les scripts cherchent Python dans cet ordre:
1. `py -3.12` ⭐ Recommandé
2. `py -3.11`
3. `py -3.10`
4. `python` (version par défaut)
5. `py` (sans version)

## ✅ Raccourcis une fois lancé

- **Ctrl+Alt+7** : Démarrer/arrêter l'enregistrement
- **Ctrl+C** : Quitter l'application

## 📁 Structure du projet

```
whisper_local_STT/
├── start.ps1           ← Script PowerShell (RECOMMANDÉ)
├── start.bat           ← Script Batch (alternative)
├── scripts/
│   └── start_fast.bat  ← Ancien script
├── src/
│   └── main.py        ← Application principale
└── config.json        ← Configuration
```

## 🆘 Support

Si vous rencontrez des problèmes:
1. Lisez les messages d'erreur
2. Vérifiez `whisper_stt.log`
3. Testez avec `.\scripts\test_python.bat`
