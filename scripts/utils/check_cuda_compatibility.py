#!/usr/bin/env python3
"""
Script de vérification de compatibilité CUDA
Vérifie si votre système peut utiliser CUDA sans droits admin
"""

import subprocess
import sys
import platform
import json
from pathlib import Path

def check_nvidia_driver():
    """Vérifie si les pilotes NVIDIA sont installés"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Driver Version:' in line:
                    driver_version = line.split('Driver Version:')[1].split()[0]
                    return True, driver_version
        return False, None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, None

def check_gpu_compatibility():
    """Vérifie la compatibilité CUDA du GPU"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,compute_cap', '--format=csv,noheader'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            gpus = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split(',')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        compute_cap = parts[1].strip()
                        # CUDA 11.8 nécessite compute capability >= 3.5
                        major, minor = map(int, compute_cap.split('.'))
                        compatible = major > 3 or (major == 3 and minor >= 5)
                        gpus.append({
                            'name': name,
                            'compute_capability': compute_cap,
                            'cuda_compatible': compatible
                        })
            return gpus
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []

def check_python_environment():
    """Vérifie l'environnement Python"""
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'architecture': platform.architecture()[0],
        'pip_available': False,
        'conda_available': False
    }
    
    # Vérifier pip
    try:
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      capture_output=True, timeout=5)
        info['pip_available'] = True
    except:
        pass
    
    # Vérifier conda
    try:
        subprocess.run(['conda', '--version'], capture_output=True, timeout=5)
        info['conda_available'] = True
    except:
        pass
    
    return info

def check_existing_cuda():
    """Vérifie si CUDA est déjà installé"""
    cuda_info = {
        'system_cuda': False,
        'pytorch_cuda': False,
        'faster_whisper': False
    }
    
    # CUDA système
    try:
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            cuda_info['system_cuda'] = True
    except:
        pass
    
    # PyTorch CUDA
    try:
        import torch
        cuda_info['pytorch_cuda'] = torch.cuda.is_available()
        if cuda_info['pytorch_cuda']:
            cuda_info['pytorch_version'] = torch.__version__
            cuda_info['cuda_version'] = torch.version.cuda
            cuda_info['gpu_count'] = torch.cuda.device_count()
    except ImportError:
        pass
    
    # Faster-Whisper
    try:
        from faster_whisper import WhisperModel
        cuda_info['faster_whisper'] = True
    except ImportError:
        pass
    
    return cuda_info

def get_recommendations(driver_ok, gpus, python_info, cuda_info):
    """Génère des recommandations basées sur l'analyse"""
    recommendations = []
    
    if not driver_ok:
        recommendations.append({
            'type': 'error',
            'message': 'Pilotes NVIDIA non détectés',
            'action': 'Installez les pilotes NVIDIA depuis le site officiel'
        })
        return recommendations
    
    if not gpus:
        recommendations.append({
            'type': 'error',
            'message': 'Aucun GPU NVIDIA détecté',
            'action': 'Vérifiez que votre GPU est bien connecté'
        })
        return recommendations
    
    compatible_gpus = [gpu for gpu in gpus if gpu['cuda_compatible']]
    if not compatible_gpus:
        recommendations.append({
            'type': 'warning',
            'message': 'GPU non compatible avec CUDA 11.8',
            'action': 'Utilisez CUDA 10.2 ou restez en mode CPU'
        })
        return recommendations
    
    # Recommandations d'installation
    if cuda_info['pytorch_cuda']:
        recommendations.append({
            'type': 'success',
            'message': 'CUDA déjà configuré et fonctionnel',
            'action': 'Modifiez config.json pour utiliser "device": "cuda"'
        })
    elif python_info['pip_available']:
        recommendations.append({
            'type': 'info',
            'message': 'Installation recommandée via pip',
            'action': 'Exécutez scripts\\install_cuda_pip.bat'
        })
    elif python_info['conda_available']:
        recommendations.append({
            'type': 'info',
            'message': 'Installation recommandée via conda',
            'action': 'Exécutez scripts\\install_cuda_portable.bat'
        })
    else:
        recommendations.append({
            'type': 'warning',
            'message': 'Ni pip ni conda disponibles',
            'action': 'Installez Miniconda puis relancez ce script'
        })
    
    return recommendations

def main():
    print("🔍 VÉRIFICATION DE COMPATIBILITÉ CUDA")
    print("=" * 50)
    
    # Vérifications
    print("\n1. Vérification des pilotes NVIDIA...")
    driver_ok, driver_version = check_nvidia_driver()
    if driver_ok:
        print(f"   ✅ Pilotes NVIDIA détectés (version {driver_version})")
    else:
        print("   ❌ Pilotes NVIDIA non détectés")
    
    print("\n2. Vérification des GPU...")
    gpus = check_gpu_compatibility()
    if gpus:
        for gpu in gpus:
            status = "✅" if gpu['cuda_compatible'] else "❌"
            print(f"   {status} {gpu['name']} (Compute {gpu['compute_capability']})")
    else:
        print("   ❌ Aucun GPU NVIDIA détecté")
    
    print("\n3. Vérification de l'environnement Python...")
    python_info = check_python_environment()
    print(f"   Python: {python_info['python_version'].split()[0]}")
    print(f"   Plateforme: {python_info['platform']}")
    print(f"   pip: {'✅' if python_info['pip_available'] else '❌'}")
    print(f"   conda: {'✅' if python_info['conda_available'] else '❌'}")
    
    print("\n4. Vérification CUDA existant...")
    cuda_info = check_existing_cuda()
    print(f"   CUDA système: {'✅' if cuda_info['system_cuda'] else '❌'}")
    print(f"   PyTorch CUDA: {'✅' if cuda_info['pytorch_cuda'] else '❌'}")
    if cuda_info['pytorch_cuda']:
        print(f"   Version PyTorch: {cuda_info.get('pytorch_version', 'N/A')}")
        print(f"   Version CUDA: {cuda_info.get('cuda_version', 'N/A')}")
        print(f"   Nombre de GPU: {cuda_info.get('gpu_count', 0)}")
    print(f"   Faster-Whisper: {'✅' if cuda_info['faster_whisper'] else '❌'}")
    
    # Recommandations
    print("\n📋 RECOMMANDATIONS")
    print("=" * 50)
    recommendations = get_recommendations(driver_ok, gpus, python_info, cuda_info)
    
    for i, rec in enumerate(recommendations, 1):
        icon = {"success": "✅", "info": "💡", "warning": "⚠️", "error": "❌"}[rec['type']]
        print(f"{i}. {icon} {rec['message']}")
        print(f"   Action: {rec['action']}")
    
    # Sauvegarde du rapport
    report = {
        'timestamp': str(Path(__file__).stat().st_mtime),
        'driver': {'available': driver_ok, 'version': driver_version},
        'gpus': gpus,
        'python': python_info,
        'cuda': cuda_info,
        'recommendations': recommendations
    }
    
    report_file = Path(__file__).parent.parent / 'cuda_compatibility_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport sauvegardé: {report_file}")
    
    # Résumé final
    if cuda_info['pytorch_cuda']:
        print("\n🎉 CUDA est prêt à utiliser !")
        print("   Modifiez config.json: \"device\": \"cuda\"")
    elif driver_ok and gpus and any(gpu['cuda_compatible'] for gpu in gpus):
        print("\n🚀 Votre système est compatible CUDA")
        if python_info['pip_available']:
            print("   Exécutez: scripts\\install_cuda_pip.bat")
        else:
            print("   Installez d'abord Miniconda")
    else:
        print("\n⚠️  CUDA non disponible")
        print("   Utilisez le mode CPU uniquement")

if __name__ == "__main__":
    main()