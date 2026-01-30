#!/usr/bin/env python3
"""
Script de test des dépendances principales
Conforme aux standards de développement VTT
"""

import logging
import sys

# Configuration du logging selon les standards VTT
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def test_dependencies():
    """
    Teste toutes les dépendances principales de VTT.
    
    Returns:
        dict: Résultats des tests par module
    """
    modules = {
        'torch': 'PyTorch pour CUDA',
        'whisper': 'OpenAI Whisper',
        'faster_whisper': 'Faster-Whisper optimisé',
        'pyaudio': 'Capture audio',
        'numpy': 'Calculs numériques'
    }
    
    results = {}
    
    logger.info("=== TEST DES DÉPENDANCES ===")
    
    for module, description in modules.items():
        try:
            __import__(module)
            logger.info(f"✅ {module} - {description}")
            results[module] = True
        except ImportError as e:
            logger.error(f"❌ {module} - Non installé: {e}")
            results[module] = False
        except Exception as e:
            logger.error(f"⚠️ {module} - Erreur: {e}")
            results[module] = False
    
    return results

def check_whisper_models():
    """Vérifie les modèles Whisper en cache."""
    try:
        import os
        from pathlib import Path
        
        cache_dir = Path.home() / '.cache' / 'whisper'
        if cache_dir.exists():
            models = list(cache_dir.glob('*.pt'))
            if models:
                logger.info(f"Modèles Whisper trouvés: {len(models)}")
                for model in models:
                    logger.info(f"  - {model.name}")
                return len(models)
            else:
                logger.warning("Aucun modèle Whisper en cache")
                return 0
        else:
            logger.warning("Dossier cache Whisper non trouvé")
            return 0
    except Exception as e:
        logger.error(f"Erreur lors de la vérification des modèles: {e}")
        return -1

def main():
    """Point d'entrée principal."""
    results = test_dependencies()
    model_count = check_whisper_models()
    
    # Résumé
    total_modules = len(results)
    working_modules = sum(results.values())
    
    print(f"\n📊 RÉSUMÉ: {working_modules}/{total_modules} modules fonctionnels")
    
    if working_modules == total_modules:
        print("✅ Toutes les dépendances sont installées")
        sys.exit(0)
    elif working_modules >= total_modules * 0.8:
        print("⚠️ La plupart des dépendances sont installées")
        sys.exit(1)
    else:
        print("❌ Plusieurs dépendances manquantes")
        sys.exit(2)

if __name__ == "__main__":
    main()