#!/usr/bin/env python3
"""
Script de test PyTorch CUDA pour VTT
Vérifie que PyTorch et CUDA fonctionnent correctement
"""

import sys
import traceback

def test_pytorch_cuda():
    """Test PyTorch et CUDA"""
    try:
        import torch
        print(f'[INFO] PyTorch version: {torch.__version__}')
        print(f'[INFO] CUDA disponible: {torch.cuda.is_available()}')
        
        if torch.cuda.is_available():
            print(f'[INFO] Version CUDA: {torch.version.cuda}')
            print(f'[INFO] GPU: {torch.cuda.get_device_name(0)}')
            memory_gb = torch.cuda.get_device_properties(0).total_memory // (1024**3)
            print(f'[INFO] Mémoire GPU: {memory_gb} GB')
            return True
        else:
            print('[ERREUR] CUDA non disponible')
            return False
            
    except ImportError as e:
        print(f'[ERREUR] PyTorch non installé: {e}')
        return False
    except Exception as e:
        print(f'[ERREUR] Test PyTorch échoué: {e}')
        traceback.print_exc()
        return False

def test_faster_whisper_cuda():
    """Test Faster-Whisper avec CUDA"""
    try:
        import faster_whisper
        import torch
        
        print('[INFO] Test Faster-Whisper avec CUDA...')
        
        # Test avec le modèle tiny d'abord (plus rapide)
        model = faster_whisper.WhisperModel('tiny', device='cuda', compute_type='float16')
        print('[SUCCESS] Modèle tiny chargé avec CUDA')
        
        # Test avec large-v3 (configuration utilisateur)
        del model
        model = faster_whisper.WhisperModel('large-v3', device='cuda', compute_type='float16')
        print('[SUCCESS] Modèle large-v3 chargé avec CUDA')
        print('[SUCCESS] Faster-Whisper avec CUDA fonctionne parfaitement !')
        
        del model
        return True
        
    except ImportError as e:
        print(f'[ERREUR] Faster-Whisper non installé: {e}')
        return False
    except Exception as e:
        print(f'[ERREUR] Faster-Whisper CUDA: {e}')
        print('[INFO] Vérifiez les drivers NVIDIA')
        return False

if __name__ == "__main__":
    # Test PyTorch CUDA
    if len(sys.argv) > 1 and sys.argv[1] == "pytorch":
        success = test_pytorch_cuda()
        sys.exit(0 if success else 1)
    
    # Test Faster-Whisper CUDA
    elif len(sys.argv) > 1 and sys.argv[1] == "faster-whisper":
        success = test_faster_whisper_cuda()
        sys.exit(0 if success else 1)
    
    # Test complet
    else:
        pytorch_ok = test_pytorch_cuda()
        if pytorch_ok:
            faster_whisper_ok = test_faster_whisper_cuda()
            sys.exit(0 if faster_whisper_ok else 1)
        else:
            sys.exit(1)