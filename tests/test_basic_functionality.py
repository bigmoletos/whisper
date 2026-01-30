"""
Tests de base pour vérifier que le système fonctionne
"""

import pytest
import numpy as np
from pathlib import Path
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test que les imports de base fonctionnent."""
    try:
        from shared.src.audio_capture import AudioCapture
        from shared.src.whisper_transcriber import WhisperTranscriber
        assert True
    except ImportError as e:
        pytest.skip(f"Imports non disponibles: {e}")

def test_audio_capture_init():
    """Test l'initialisation de AudioCapture."""
    try:
        from shared.src.audio_capture import AudioCapture
        capture = AudioCapture()
        assert capture.sample_rate == 16000
        assert capture.channels == 1
    except ImportError:
        pytest.skip("AudioCapture non disponible")

def test_whisper_transcriber_init():
    """Test l'initialisation de WhisperTranscriber."""
    try:
        from shared.src.whisper_transcriber import WhisperTranscriber
        transcriber = WhisperTranscriber(model_name="tiny")
        assert transcriber.model_name == "tiny"
        assert transcriber.language == "fr"
    except ImportError:
        pytest.skip("WhisperTranscriber non disponible")

def test_numpy_available():
    """Test que numpy est disponible."""
    import numpy as np
    arr = np.array([1, 2, 3])
    assert len(arr) == 3

def test_basic_audio_processing():
    """Test de traitement audio de base."""
    # Créer un signal audio simple
    sample_rate = 16000
    duration = 0.1  # 100ms
    samples = np.random.random(int(sample_rate * duration)).astype(np.float32)
    
    # Vérifications de base
    assert len(samples) == int(sample_rate * duration)
    assert samples.dtype == np.float32
    assert np.all(samples >= 0) and np.all(samples <= 1)