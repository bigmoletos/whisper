"""
Pytest configuration and fixtures for VTT modernization tests.

This module provides shared fixtures and configuration for property-based
testing of the VTT modernization components.
"""

import pytest
import numpy as np
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
import tempfile
import json
from pathlib import Path

from ..config.modernization_config import ModernizationConfig
from ..models.audio_models import (
    EnhancedAudioData, AudioMetadata, ProcessingContext,
    AudioFormat, ProcessingMode, QualityMetrics, 
    PerformanceConstraints, FallbackStrategy
)
from ..core.property_testing import AudioGeneratorSet, AudioGeneratorConfig


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "enabled": True,
            "debug_mode": True,
            "config_version": "1.0.0",
            "spec_compliance": {
                "requirements_validation": True,
                "ears_pattern_enforcement": True,
                "property_generation": True
            },
            "amazon_integration": {
                "codewhisperer_enabled": False,  # Disabled for testing
                "formal_verification": False
            },
            "property_testing": {
                "hypothesis_iterations": 100,  # Minimum 100 iterations as requested
                "testing_framework": "hypothesis"
            }
        }
        json.dump(config_data, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def modernization_config():
    """Provide a test modernization configuration."""
    return ModernizationConfig(
        enabled=True,
        debug_mode=True
    )


@pytest.fixture
def audio_generator_config():
    """Provide audio generator configuration for testing."""
    return AudioGeneratorConfig(
        sample_rates=[16000, 22050],  # Reduced for faster tests
        durations=[0.1, 0.5, 1.0],
        channels=[1, 2],
        noise_levels=[0.0, 0.01]
    )


@pytest.fixture
def audio_generators(audio_generator_config):
    """Provide audio generators for testing."""
    return AudioGeneratorSet(audio_generator_config)


@pytest.fixture
def sample_audio_metadata():
    """Provide sample audio metadata for testing."""
    return AudioMetadata(
        duration=1.0,
        format=AudioFormat.WAV,
        bit_depth=16,
        encoding="pcm",
        source="test"
    )


@pytest.fixture
def sample_processing_context():
    """Provide sample processing context for testing."""
    return ProcessingContext(
        mode=ProcessingMode.BATCH,
        quality_requirements=QualityMetrics(),
        performance_constraints=PerformanceConstraints(),
        fallback_strategy=FallbackStrategy()
    )


@pytest.fixture
def sample_enhanced_audio(sample_audio_metadata, sample_processing_context):
    """Provide sample enhanced audio data for testing."""
    # Create simple sine wave
    sample_rate = 16000
    duration = 1.0
    frequency = 440.0  # A4
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    samples = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    
    return EnhancedAudioData(
        samples=samples,
        sample_rate=sample_rate,
        channels=1,
        metadata=sample_audio_metadata,
        processing_context=sample_processing_context
    )


@pytest.fixture
def mock_transcription_engine():
    """Provide a mock transcription engine for testing."""
    def mock_transcribe(audio_samples, sample_rate):
        """Mock transcription function."""
        if isinstance(audio_samples, np.ndarray) and audio_samples.size > 0:
            # Return mock transcription based on audio length
            duration = len(audio_samples) / sample_rate
            if duration < 0.5:
                return "short"
            elif duration < 2.0:
                return "medium length transcription"
            else:
                return "this is a longer transcription result for extended audio"
        return ""
    
    return mock_transcribe


# Hypothesis strategies for testing
@st.composite
def valid_sample_rates(draw):
    """Generate valid sample rates."""
    return draw(st.sampled_from([8000, 16000, 22050, 44100, 48000]))


@st.composite
def valid_audio_durations(draw):
    """Generate valid audio durations."""
    return draw(st.floats(min_value=0.1, max_value=10.0))


@st.composite
def valid_channel_counts(draw):
    """Generate valid channel counts."""
    return draw(st.integers(min_value=1, max_value=8))


@st.composite
def valid_audio_samples(draw, sample_rate=16000, duration=1.0, channels=1):
    """Generate valid audio sample arrays."""
    num_samples = int(sample_rate * duration)
    
    if channels == 1:
        return draw(arrays(
            dtype=np.float32,
            shape=num_samples,
            elements=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)
        ))
    else:
        return draw(arrays(
            dtype=np.float32,
            shape=(num_samples, channels),
            elements=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)
        ))


@st.composite
def invalid_audio_samples(draw):
    """Generate invalid audio sample arrays."""
    return draw(st.one_of([
        st.none(),
        st.just(np.array([])),
        st.just(np.array([np.inf, np.nan])),
        arrays(np.float32, shape=st.integers(0, 5), elements=st.floats(-10, 10))
    ]))


# Pytest markers for different test categories
pytest.mark.property = pytest.mark.property
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.performance = pytest.mark.performance


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "property: property-based tests")
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "performance: performance tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add property marker to property-based tests
        if "property" in item.name.lower() or "test_property" in item.name:
            item.add_marker(pytest.mark.property)
        
        # Add unit marker to unit tests
        if "test_unit" in item.name or item.fspath.basename.startswith("test_unit"):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to integration tests
        if "test_integration" in item.name or "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add performance marker to performance tests
        if "test_performance" in item.name or "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)