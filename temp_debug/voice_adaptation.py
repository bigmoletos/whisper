#!/usr/bin/env python3
"""
Script d'adaptation vocale pour améliorer la reconnaissance
Permet d'entraîner le modèle sur votre voix spécifique
"""

import os
import json
import wave
import sys
from pathlib import Path
from datetime import datetime

# Vérifier les dépendances
try:
    import pyaudio
except ImportError:
    print("❌ PyAudio non installé. Installation en cours...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
    import pyaudio

try:
    import whisper
except ImportError:
    print("❌ Whisper non installé. Installation en cours...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
    import whisper

try:
    import numpy as np
except ImportError:
    print("❌ NumPy non installé. Installation en cours...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np

class VoiceAdaptation:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.adaptation_dir = self.base_dir / "voice_adaptation"
        self.adaptation_dir.mkdir(exist_ok=True)
        
        # Textes d'entraînement pour les termes techniques
        self.training_texts = [
            "Je migre le projet Angular avec TypeScript",
            "J'utilise OpenRewrite pour la transformation automatique",
            "Coq-of-js génère les preuves formelles",
            "Strands-agent d'Amazon aide à l'automation",
            "Kiro IDE avec MCP facilite le développement",
            "Les skills d'IA réduisent la low-complexity",
            "Jira track les tickets de migration",
            "GitHub Copilot suggère le code TypeScript",
            "VS Code avec IntelliCode améliore la QA",
            "npm installe les dépendances du package.json",
            "Maven compile le projet Java Spring Boot",
            "SonarQube analyse la qualité du code",
            "Playwright teste l'interface utilisateur",
            "Docker build l'image de l'application"
        ]
    
    def record_training_sample(self, text, duration=10):
        """Enregistre un échantillon vocal pour un texte donné"""
        print(f"\n📝 Texte à lire :")
        print(f"'{text}'")
        print(f"\n🎤 Préparez-vous à enregistrer pendant {duration} secondes...")
        input("Appuyez sur Entrée quand vous êtes prêt...")
        
        # Configuration audio
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 16000
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=format,
                       channels=channels,
                       rate=rate,
                       input=True,
                       frames_per_buffer=chunk)
        
        print("🔴 ENREGISTREMENT EN COURS...")
        frames = []
        
        for i in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        
        print("⏹️ Enregistrement terminé")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Sauvegarder l'audio
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = self.adaptation_dir / f"sample_{timestamp}.wav"
        
        wf = wave.open(str(audio_file), 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return audio_file, text
    
    def test_transcription(self, audio_file, expected_text):
        """Teste la transcription d'un échantillon"""
        print(f"\n🔍 Test de transcription...")
        
        # Charger le modèle Whisper
        model = whisper.load_model("large-v3")
        
        # Transcription avec prompt personnalisé
        result = model.transcribe(
            str(audio_file),
            language="fr",
            initial_prompt=self.get_technical_prompt()
        )
        
        transcribed = result["text"].strip()
        
        print(f"📝 Texte attendu : '{expected_text}'")
        print(f"🎯 Transcription  : '{transcribed}'")
        
        # Calcul de similarité simple
        similarity = self.calculate_similarity(expected_text.lower(), transcribed.lower())
        print(f"📊 Similarité : {similarity:.1f}%")
        
        return transcribed, similarity
    
    def calculate_similarity(self, text1, text2):
        """Calcule la similarité entre deux textes"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 100.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return (len(intersection) / len(union)) * 100 if union else 0.0
    
    def get_technical_prompt(self):
        """Retourne le prompt technique optimisé"""
        return """Transcription technique professionnelle. Migration et IA : Angular, AngularJS, Angular CLI, TypeScript, JavaScript, migration, modernisation, refactoring, legacy, low-complexity, automation, formal verification, coq-of-js, Coq, OpenRewrite, strands-agent, Amazon CodeWhisperer, Microsoft Copilot. IDE et IA : Kiro, Kiro IDE, Cursor, VS Code, Visual Studio Code, GitHub Copilot, IntelliJ IDEA, WebStorm, PyCharm, MCP, Model Context Protocol, skills, capabilities, agents, autonomous agents. Gestion projet : Jira, Atlassian, ticket, issue, epic, story, sprint, Agile, Scrum, Kanban, npm, yarn, pnpm, package.json, Maven, Gradle, pip, requirements.txt."""
    
    def run_adaptation_session(self):
        """Lance une session complète d'adaptation vocale"""
        print("🎯 SESSION D'ADAPTATION VOCALE")
        print("=" * 50)
        print("Cette session va vous aider à améliorer la reconnaissance")
        print("de votre voix pour les termes techniques.")
        print()
        
        results = []
        
        for i, text in enumerate(self.training_texts[:5], 1):  # Limiter à 5 pour commencer
            print(f"\n📍 Échantillon {i}/{min(5, len(self.training_texts))}")
            print("-" * 30)
            
            try:
                audio_file, expected = self.record_training_sample(text)
                transcribed, similarity = self.test_transcription(audio_file, expected)
                
                results.append({
                    'text': expected,
                    'transcribed': transcribed,
                    'similarity': similarity,
                    'audio_file': str(audio_file)
                })
                
                if similarity < 70:
                    print("⚠️  Faible similarité. Conseils :")
                    print("   - Parlez plus lentement")
                    print("   - Articulez bien les termes techniques")
                    print("   - Rapprochez-vous du microphone")
                
            except Exception as e:
                print(f"❌ Erreur : {e}")
                continue
        
        # Rapport final
        self.generate_report(results)
    
    def generate_report(self, results):
        """Génère un rapport d'adaptation"""
        print("\n📊 RAPPORT D'ADAPTATION VOCALE")
        print("=" * 50)
        
        if not results:
            print("❌ Aucun résultat à analyser")
            return
        
        avg_similarity = sum(r['similarity'] for r in results) / len(results)
        print(f"📈 Similarité moyenne : {avg_similarity:.1f}%")
        
        # Termes problématiques
        problematic = [r for r in results if r['similarity'] < 70]
        if problematic:
            print(f"\n⚠️  Termes à améliorer ({len(problematic)}) :")
            for r in problematic:
                print(f"   - '{r['text']}' → '{r['transcribed']}' ({r['similarity']:.1f}%)")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS :")
        if avg_similarity < 60:
            print("   🔴 Qualité faible - Vérifiez votre microphone et l'environnement")
        elif avg_similarity < 80:
            print("   🟡 Qualité moyenne - Continuez l'entraînement")
        else:
            print("   🟢 Bonne qualité - Votre voix est bien adaptée")
        
        print("\n📝 Conseils généraux :")
        print("   - Parlez à vitesse normale, pas trop vite")
        print("   - Articulez bien les consonnes")
        print("   - Maintenez une distance constante du micro")
        print("   - Évitez les bruits de fond")
        
        # Sauvegarder le rapport
        report_file = self.adaptation_dir / f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'average_similarity': avg_similarity,
                'results': results,
                'recommendations': self.get_recommendations(avg_similarity)
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rapport sauvegardé : {report_file}")
    
    def get_recommendations(self, avg_similarity):
        """Retourne des recommandations basées sur la performance"""
        if avg_similarity < 60:
            return [
                "Vérifiez la qualité de votre microphone",
                "Réduisez les bruits de fond",
                "Parlez plus lentement et distinctement",
                "Rapprochez-vous du microphone"
            ]
        elif avg_similarity < 80:
            return [
                "Continuez à vous entraîner avec les termes techniques",
                "Maintenez une prononciation constante",
                "Pratiquez les mots les plus difficiles"
            ]
        else:
            return [
                "Excellente adaptation vocale",
                "Continuez à utiliser le même environnement d'enregistrement",
                "Votre configuration est optimale"
            ]

if __name__ == "__main__":
    try:
        adapter = VoiceAdaptation()
        adapter.run_adaptation_session()
    except KeyboardInterrupt:
        print("\n\n👋 Session interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")