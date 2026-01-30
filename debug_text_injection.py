#!/usr/bin/env python3
"""
Debug de l'injection de texte
Diagnostique pourquoi le texte n'est pas restitué
"""

import sys
import time
import json
from pathlib import Path

# Ajouter le répertoire shared au PYTHONPATH
shared_dir = Path(__file__).parent / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))


def test_audio_capture():
    """Test du module de capture audio"""
    print("🎤 Test capture audio...")
    
    try:
        from src.audio_capture import AudioCapture
        
        # Configuration audio par défaut
        audio_capture = AudioCapture(
            sample_rate=16000,
            channels=1,
            chunk_duration=3.0
        )
        
        print("✅ Module AudioCapture initialisé")
        
        # Test rapide d'enregistrement
        print("📍 Test enregistrement 2 secondes...")
        audio_capture.start_recording()
        time.sleep(2)
        audio_data = audio_capture.stop_recording()
        
        print(f"✅ Audio capturé: {len(audio_data)} échantillons")
        
        if len(audio_data) == 0:
            print("⚠️  Aucun audio capturé - vérifiez le microphone")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur capture audio: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_whisper_transcriber():
    """Test du transcripteur Whisper"""
    print("\n🤖 Test transcripteur Whisper...")
    
    try:
        # Charger la configuration
        config_path = Path("projects/voice-to-text-turbo/config.json")
        if not config_path.exists():
            print("❌ Configuration non trouvée")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        whisper_config = config.get("whisper", {})
        engine = whisper_config.get("engine", "faster-whisper")
        
        print(f"📍 Moteur configuré: {engine}")
        
        if engine == "faster-whisper":
            try:
                from src.faster_whisper_transcriber import FasterWhisperTranscriber
                
                transcriber = FasterWhisperTranscriber(
                    model_name=whisper_config.get("model", "medium"),
                    language=whisper_config.get("language", "fr"),
                    device=whisper_config.get("device", "cpu"),
                    compute_type=whisper_config.get("compute_type", "int8")
                )
                
                print("✅ FasterWhisperTranscriber initialisé")
                
                # Test de chargement du modèle
                print("📍 Chargement du modèle...")
                transcriber.load_model()
                print("✅ Modèle chargé")
                
                return True
                
            except Exception as e:
                print(f"❌ Erreur Faster-Whisper: {e}")
                print("📍 Tentative avec Whisper standard...")
                
                from src.whisper_transcriber import WhisperTranscriber
                
                transcriber = WhisperTranscriber(
                    model_name=whisper_config.get("model", "medium"),
                    language=whisper_config.get("language", "fr"),
                    device=whisper_config.get("device", "cpu")
                )
                
                print("✅ WhisperTranscriber (fallback) initialisé")
                transcriber.load_model()
                print("✅ Modèle chargé")
                
                return True
        
        else:
            from src.whisper_transcriber import WhisperTranscriber
            
            transcriber = WhisperTranscriber(
                model_name=whisper_config.get("model", "medium"),
                language=whisper_config.get("language", "fr"),
                device=whisper_config.get("device", "cpu")
            )
            
            print("✅ WhisperTranscriber initialisé")
            transcriber.load_model()
            print("✅ Modèle chargé")
            
            return True
        
    except Exception as e:
        print(f"❌ Erreur transcripteur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_text_injector():
    """Test de l'injecteur de texte"""
    print("\n📝 Test injecteur de texte...")
    
    try:
        from src.text_injector import TextInjector
        
        injector = TextInjector(use_clipboard=True)
        print("✅ TextInjector initialisé")
        
        # Test d'injection
        test_text = "Test d'injection de texte VTT"
        print(f"📍 Test injection: '{test_text}'")
        
        success = injector.inject_text(test_text)
        
        if success:
            print("✅ Injection réussie")
            print("💡 Vérifiez si le texte est apparu dans l'application active")
            return True
        else:
            print("❌ Injection échouée")
            return False
        
    except Exception as e:
        print(f"❌ Erreur injecteur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_workflow():
    """Test du workflow complet"""
    print("\n🔄 Test workflow complet...")
    
    try:
        # Import des modules
        from src.audio_capture import AudioCapture
        from src.text_injector import TextInjector
        
        # Charger la configuration
        config_path = Path("projects/voice-to-text-turbo/config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Initialiser les composants
        audio_config = config.get("audio", {})
        audio_capture = AudioCapture(
            sample_rate=audio_config.get("sample_rate", 16000),
            channels=audio_config.get("channels", 1),
            chunk_duration=audio_config.get("chunk_duration", 3.0)
        )
        
        whisper_config = config.get("whisper", {})
        engine = whisper_config.get("engine", "faster-whisper")
        
        if engine == "faster-whisper":
            try:
                from src.faster_whisper_transcriber import FasterWhisperTranscriber
                transcriber = FasterWhisperTranscriber(
                    model_name=whisper_config.get("model", "medium"),
                    language=whisper_config.get("language", "fr"),
                    device=whisper_config.get("device", "cpu"),
                    compute_type=whisper_config.get("compute_type", "int8")
                )
            except:
                from src.whisper_transcriber import WhisperTranscriber
                transcriber = WhisperTranscriber(
                    model_name=whisper_config.get("model", "medium"),
                    language=whisper_config.get("language", "fr"),
                    device=whisper_config.get("device", "cpu")
                )
        else:
            from src.whisper_transcriber import WhisperTranscriber
            transcriber = WhisperTranscriber(
                model_name=whisper_config.get("model", "medium"),
                language=whisper_config.get("language", "fr"),
                device=whisper_config.get("device", "cpu")
            )
        
        text_injector = TextInjector(use_clipboard=True)
        
        print("✅ Tous les composants initialisés")
        
        # Charger le modèle
        print("📍 Chargement du modèle Whisper...")
        transcriber.load_model()
        print("✅ Modèle chargé")
        
        # Test d'enregistrement
        print("📍 Enregistrement 3 secondes - PARLEZ MAINTENANT!")
        audio_capture.start_recording()
        time.sleep(3)
        audio_data = audio_capture.stop_recording()
        
        print(f"✅ Audio capturé: {len(audio_data)} échantillons")
        
        if len(audio_data) == 0:
            print("❌ Aucun audio capturé")
            return False
        
        # Transcription
        print("📍 Transcription en cours...")
        text = transcriber.transcribe(audio_data, sample_rate=audio_capture.sample_rate)
        
        print(f"✅ Texte transcrit: '{text}'")
        
        if not text or text.strip() == "":
            print("❌ Aucun texte transcrit")
            return False
        
        # Injection
        print("📍 Injection du texte...")
        success = text_injector.inject_text(text)
        
        if success:
            print("✅ Workflow complet réussi!")
            print(f"💡 Texte injecté: '{text}'")
            return True
        else:
            print("❌ Injection échouée")
            return False
        
    except Exception as e:
        print(f"❌ Erreur workflow: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Diagnostic principal"""
    print("🔍 DIAGNOSTIC - Injection de Texte VTT")
    print("=" * 60)
    
    # Tests individuels
    audio_ok = test_audio_capture()
    whisper_ok = test_whisper_transcriber()
    injector_ok = test_text_injector()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS TESTS INDIVIDUELS:")
    print(f"   Capture audio: {'✅' if audio_ok else '❌'}")
    print(f"   Transcripteur: {'✅' if whisper_ok else '❌'}")
    print(f"   Injecteur: {'✅' if injector_ok else '❌'}")
    
    if not all([audio_ok, whisper_ok, injector_ok]):
        print("\n❌ Tests individuels échoués - Corrigez avant le test complet")
        return False
    
    # Test complet
    print("\n" + "=" * 60)
    print("🎯 TEST WORKFLOW COMPLET")
    print("📢 Préparez-vous à parler pendant 3 secondes...")
    input("Appuyez sur Entrée quand vous êtes prêt...")
    
    workflow_ok = test_complete_workflow()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTAT FINAL:")
    print(f"   Workflow complet: {'✅' if workflow_ok else '❌'}")
    
    if workflow_ok:
        print("\n🎉 SUCCÈS ! Le système fonctionne correctement")
        print("💡 Si le problème persiste dans l'app, vérifiez les logs")
    else:
        print("\n❌ PROBLÈME IDENTIFIÉ")
        print("🔧 Consultez les erreurs ci-dessus pour le diagnostic")
    
    return workflow_ok


if __name__ == "__main__":
    success = main()
    input(f"\nAppuyez sur Entrée pour quitter... ({'✅' if success else '❌'})")