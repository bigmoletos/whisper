#!/usr/bin/env python3
"""
Script de test pour PyAudio
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

def test_pyaudio_installation():
    """
    Teste l'installation et le fonctionnement de PyAudio.
    
    Returns:
        bool: True si PyAudio fonctionne correctement
    """
    try:
        import pyaudio
        logger.info("PyAudio importé avec succès")
        
        # Initialiser PyAudio
        p = pyaudio.PyAudio()
        logger.info("PyAudio initialisé avec succès")
        
        # Compter les périphériques
        device_count = p.get_device_count()
        logger.info(f"Nombre de périphériques audio: {device_count}")
        
        # Lister les périphériques d'entrée
        input_devices = []
        for i in range(device_count):
            try:
                info = p.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    input_devices.append({
                        'index': i,
                        'name': info['name'],
                        'channels': info['maxInputChannels']
                    })
                    logger.info(f"Périphérique d'entrée {i}: {info['name']} ({info['maxInputChannels']} canaux)")
            except Exception as e:
                logger.warning(f"Erreur lors de la lecture du périphérique {i}: {e}")
        
        # Nettoyer
        p.terminate()
        
        if input_devices:
            logger.info(f"✅ PyAudio fonctionne correctement - {len(input_devices)} périphériques d'entrée trouvés")
            return True
        else:
            logger.error("❌ Aucun périphérique d'entrée trouvé")
            return False
            
    except ImportError as e:
        logger.error(f"❌ PyAudio non installé: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Erreur PyAudio: {e}", exc_info=True)
        return False

def main():
    """Point d'entrée principal."""
    logger.info("=== TEST PYAUDIO ===")
    
    success = test_pyaudio_installation()
    
    if success:
        print("\n✅ PyAudio est prêt pour l'adaptation vocale")
        sys.exit(0)
    else:
        print("\n❌ PyAudio ne fonctionne pas correctement")
        print("Exécutez: scripts\\install_pyaudio_windows.bat")
        sys.exit(1)

if __name__ == "__main__":
    main()