#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation CUDA
Conforme aux standards de développement VTT
"""

import logging
import sys
from pathlib import Path

# Configuration du logging selon les standards VTT
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CudaInstallationTester:
    """
    Testeur d'installation CUDA selon les standards VTT.
    
    Vérifie la disponibilité et le bon fonctionnement de CUDA
    pour les outils de transcription vocale.
    """
    
    def __init__(self):
        """Initialise le testeur CUDA."""
        self.results = {
            'pytorch_available': False,
            'cuda_available': False,
            'faster_whisper_available': False,
            'gpu_count': 0,
            'cuda_version': None,
            'pytorch_version': None
        }
    
    def test_pytorch_cuda(self) -> bool:
        """
        Teste la disponibilité de PyTorch avec support CUDA.
        
        Returns:
            bool: True si PyTorch CUDA est disponible
            
        Raises:
            ImportError: Si PyTorch n'est pas installé
        """
        try:
            import torch
            self.results['pytorch_available'] = True
            self.results['pytorch_version'] = torch.__version__
            
            if torch.cuda.is_available():
                self.results['cuda_available'] = True
                self.results['gpu_count'] = torch.cuda.device_count()
                self.results['cuda_version'] = torch.version.cuda
                
                logger.info(f"PyTorch version: {torch.__version__}")
                logger.info(f"CUDA disponible: {torch.cuda.is_available()}")
                logger.info(f"Version CUDA: {torch.version.cuda}")
                logger.info(f"Nombre de GPU: {torch.cuda.device_count()}")
                
                # Afficher les informations des GPU
                for i in range(torch.cuda.device_count()):
                    gpu_name = torch.cuda.get_device_name(i)
                    logger.info(f"GPU {i}: {gpu_name}")
                
                return True
            else:
                logger.warning("CUDA non détecté - vérification...")
                return False
                
        except ImportError as e:
            logger.error(f"PyTorch non installé: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Erreur lors du test PyTorch: {e}", exc_info=True)
            return False
    
    def test_faster_whisper(self) -> bool:
        """
        Teste la disponibilité de Faster-Whisper.
        
        Returns:
            bool: True si Faster-Whisper est disponible
        """
        try:
            from faster_whisper import WhisperModel
            self.results['faster_whisper_available'] = True
            logger.info("Faster-Whisper: OK")
            
            # Test avec un petit modèle si CUDA est disponible
            if self.results['cuda_available']:
                try:
                    model = WhisperModel('tiny', device='cuda', compute_type='float16')
                    logger.info("Faster-Whisper avec CUDA: OK")
                    return True
                except Exception as e:
                    logger.warning(f"Faster-Whisper CUDA échoué: {e}")
                    logger.info("Utilisation CPU par défaut")
                    return False
            else:
                logger.info("Test Faster-Whisper en mode CPU uniquement")
                return True
                
        except ImportError as e:
            logger.error(f"Faster-Whisper non installé: {e}")
            return False
        except Exception as e:
            logger.error(f"Erreur Faster-Whisper: {e}", exc_info=True)
            return False
    
    def generate_config_recommendation(self) -> dict:
        """
        Génère une recommandation de configuration basée sur les tests.
        
        Returns:
            dict: Configuration recommandée pour config.json
        """
        config = {
            "whisper": {
                "engine": "faster-whisper",
                "model": "medium",  # Compromis vitesse/qualité selon standards VTT
                "language": "fr",
                "device": "cuda" if self.results['cuda_available'] else "cpu"
            }
        }
        
        if self.results['cuda_available']:
            config["whisper"]["compute_type"] = "float16"
            config["whisper"]["vad_filter"] = True  # Optimisation selon standards VTT
        else:
            config["whisper"]["compute_type"] = "int8"
        
        return config
    
    def run_full_test(self) -> dict:
        """
        Exécute tous les tests et retourne un rapport complet.
        
        Returns:
            dict: Rapport de test complet
        """
        logger.info("=== TEST INSTALLATION CUDA ===")
        
        # Test PyTorch CUDA
        try:
            pytorch_ok = self.test_pytorch_cuda()
        except ImportError:
            pytorch_ok = False
        
        # Test Faster-Whisper
        faster_whisper_ok = self.test_faster_whisper()
        
        # Générer recommandations
        config_recommendation = self.generate_config_recommendation()
        
        # Rapport final
        report = {
            'status': 'success' if pytorch_ok and faster_whisper_ok else 'partial' if faster_whisper_ok else 'failed',
            'results': self.results,
            'config_recommendation': config_recommendation,
            'next_steps': self._get_next_steps()
        }
        
        self._print_summary(report)
        return report
    
    def _get_next_steps(self) -> list:
        """Retourne les prochaines étapes recommandées."""
        steps = []
        
        if not self.results['pytorch_available']:
            steps.append("Installer PyTorch: pip install torch torchvision torchaudio")
        
        if not self.results['faster_whisper_available']:
            steps.append("Installer Faster-Whisper: pip install faster-whisper")
        
        if self.results['cuda_available']:
            steps.append("Modifier config.json: \"device\": \"cuda\"")
            steps.append("Tester avec voice-to-text-turbo")
        else:
            steps.append("Utiliser voice-to-text-basic (CPU)")
            steps.append("Considérer l'installation de CUDA pour de meilleures performances")
        
        return steps
    
    def _print_summary(self, report: dict) -> None:
        """Affiche un résumé des résultats."""
        print("\n" + "="*50)
        print("RÉSUMÉ DU TEST CUDA")
        print("="*50)
        
        status_icon = {
            'success': '✅',
            'partial': '⚠️',
            'failed': '❌'
        }
        
        print(f"Statut global: {status_icon[report['status']]} {report['status'].upper()}")
        print(f"PyTorch: {'✅' if self.results['pytorch_available'] else '❌'}")
        print(f"CUDA: {'✅' if self.results['cuda_available'] else '❌'}")
        print(f"Faster-Whisper: {'✅' if self.results['faster_whisper_available'] else '❌'}")
        
        if self.results['cuda_available']:
            print(f"GPU disponibles: {self.results['gpu_count']}")
        
        print("\nPROCHAINES ÉTAPES:")
        for i, step in enumerate(report['next_steps'], 1):
            print(f"{i}. {step}")
        
        print("\nCONFIGURATION RECOMMANDÉE:")
        config = report['config_recommendation']
        print(f"Engine: {config['whisper']['engine']}")
        print(f"Device: {config['whisper']['device']}")
        print(f"Model: {config['whisper']['model']}")

def main():
    """Point d'entrée principal du script."""
    try:
        tester = CudaInstallationTester()
        report = tester.run_full_test()
        
        # Sauvegarder le rapport
        report_file = Path(__file__).parent.parent / 'cuda_test_report.json'
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Rapport sauvegardé: {report_file}")
        
        # Code de sortie selon le résultat
        if report['status'] == 'success':
            sys.exit(0)
        elif report['status'] == 'partial':
            sys.exit(1)
        else:
            sys.exit(2)
            
    except Exception as e:
        logger.critical(f"Erreur critique lors du test: {e}", exc_info=True)
        sys.exit(3)

if __name__ == "__main__":
    main()