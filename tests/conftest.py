"""
Configuration pytest pour les tests VTT
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock

# Configuration pytest
pytest_plugins = []

@pytest.fixture
def temp_dir():
    """Répertoire temporaire pour les tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def sample_audio():
    """Échantillon audio pour les tests."""
    # Générer 1 seconde d'audio à 16kHz
    sample_rate = 16000
    duration = 1.0
    samples = np.random.random(int(sample_rate * duration)).astype(np.float32)
    return samples, sample_rate

@pytest.fixture
def mock_config():
    """Configuration mock pour les tests."""
    return {
        "whisper": {
            "engine": "whisper",
            "model": "tiny",
            "language": "fr",
            "device": "cpu"
        },
        "audio": {
            "sample_rate": 16000,
            "channels": 1,
            "chunk_duration": 3.0
        },
        "logging": {
            "level": "INFO"
        }
    }

@pytest.fixture
def mock_transcriber():
    """Transcriber mock pour les tests."""
    mock = Mock()
    mock.transcribe.return_value = "Texte transcrit de test"
    mock.load_model.return_value = None
    return mock